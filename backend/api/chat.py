from fastapi import APIRouter, HTTPException
from schemas.requests import ChatRequest
from schemas.responses import ChatResponse

from core.llm_engine import get_llm_response
from core.validator import validate_command

from gee.executor import execute_command

import uuid

router = APIRouter(prefix="/api", tags=["chat"])

# In-memory session store (later DB se replace karenge)
sessions: dict = {}


def build_analysis_metadata(command):

    operation = command.operation.upper()

    if operation == "NDVI":

        return {
            "dataset_info": {
                "dataset_name": "Sentinel-2 Level-2A",
                "gee_collection": "COPERNICUS/S2_SR_HARMONIZED",
                "resolution": "10 m",
                "date_range": f"{command.date_range.start} to {command.date_range.end}",
                "bands_used": [
                    "B4 (Red)",
                    "B8 (Near Infrared)"
                ],
                "cloud_mask": True,
                "composite_method": "Median Composite"
            },

            "methodology":
                "NDVI was calculated using Sentinel-2 Red (B4) and Near Infrared (B8) bands. "
                "Cloud masking was applied and a median composite was generated for the selected date range.",

            "interpretation":
                "NDVI measures vegetation health and density. Higher values indicate healthier and denser vegetation, "
                "while lower values generally correspond to urban areas, barren land, rocky terrain, or water bodies.",

            "legend": {
                "Red": "Sparse vegetation / barren land",
                "Orange": "Low vegetation",
                "Yellow": "Moderate vegetation",
                "Light Green": "Healthy vegetation",
                "Dark Green": "Dense and healthy vegetation"
            }
        }

    elif operation == "NDWI":

        return {
            "dataset_info": {
                "dataset_name": "Sentinel-2 Level-2A",
                "gee_collection": "COPERNICUS/S2_SR_HARMONIZED",
                "resolution": "10 m",
                "date_range": f"{command.date_range.start} to {command.date_range.end}",
                "bands_used": [
                    "B3 (Green)",
                    "B8 (Near Infrared)"
                ]
            },

            "methodology":
                "NDWI was calculated using Green and Near Infrared bands to identify water bodies.",

            "interpretation":
                "Higher NDWI values generally indicate water presence, while lower values represent land surfaces.",

            "legend": {
                "Dark Blue": "Water",
                "Light Blue": "Possible water",
                "Yellow": "Land",
                "Brown": "Dry surface"
            }
        }

    elif operation == "SAR":

        return {
            "dataset_info": {
                "dataset_name": "Sentinel-1 GRD",
                "gee_collection": "COPERNICUS/S1_GRD",
                "resolution": "10 m",
                "date_range": f"{command.date_range.start} to {command.date_range.end}",
            },

            "methodology":
                "Synthetic Aperture Radar (SAR) backscatter analysis was performed using Sentinel-1 observations.",

            "interpretation":
                "Bright regions indicate stronger radar backscatter while darker regions indicate weaker returns.",

            "legend": {
                "White": "High backscatter",
                "Gray": "Moderate backscatter",
                "Black": "Low backscatter"
            }
        }

    elif operation == "URBAN_HEAT":

        return {
            "dataset_info": {
                "dataset_name": "Landsat 8 Collection 2",
                "resolution": "30 m",
                "date_range": f"{command.date_range.start} to {command.date_range.end}",
            },

            "methodology":
                "Land Surface Temperature analysis was performed using thermal infrared bands.",

            "interpretation":
                "Hotter regions generally correspond to dense urban areas, exposed soil, or industrial zones.",

            "legend": {
                "Blue": "Cool area",
                "Green": "Moderate temperature",
                "Yellow": "Warm area",
                "Red": "Hot area"
            }
        }

    return {
        "dataset_info": {
            "dataset_name": "Satellite Dataset",
            "date_range": f"{command.date_range.start} to {command.date_range.end}",
        },

        "methodology":
            f"{operation} analysis executed using Google Earth Engine.",

        "interpretation":
            "Analysis completed successfully.",

        "legend": {}
    }


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):

    # Session handle karo
    session_id = request.session_id or str(uuid.uuid4())
    history = sessions.get(session_id, [])

    # Step 1: LLM se JSON lo
    raw_command = get_llm_response(
        user_message=request.message,
        history=history
    )

    if not raw_command:
        raise HTTPException(
            status_code=500,
            detail="LLM se response nahi aaya. Dobara try karo."
        )

    # Step 2: Validate karo
    command, error = validate_command(raw_command)

    if error:

        raw_command = get_llm_response(
            user_message=request.message,
            history=history,
            retry_error=error
        )

        command, error = validate_command(raw_command or {})

        if error:
            raise HTTPException(
                status_code=422,
                detail=f"Invalid command after retry: {error}"
            )

    # Step 3: GEE execute karo
    result = await execute_command(command)

    # Step 4: History update karo
    history.append({
        "role": "user",
        "content": request.message
    })

    history.append({
        "role": "assistant",
        "content": str(raw_command)
    })

    sessions[session_id] = history[-10:]

    # Step 5: Response return karo
    if command.output_mode == "tile_preview":

        metadata = build_analysis_metadata(command)

        return ChatResponse(
            reply=f"{command.operation} analysis completed for {command.region.value}.",

            preview_url=result.get("preview_url"),

            dataset_info=metadata["dataset_info"],

            methodology=metadata["methodology"],

            interpretation=metadata["interpretation"],

            legend=metadata["legend"],

            session_id=session_id,
        )

    return ChatResponse(
        reply=f"Export shuru ho gaya! Job ID: {result.get('job_id')}",
        job_id=result.get("job_id"),
        session_id=session_id,
    )