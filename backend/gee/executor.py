import ee
from core.validator              import GEECommand
from gee.operations.ndvi         import run_ndvi
from gee.operations.sar          import run_sar
from gee.operations.land_cover   import run_land_cover
from gee.operations.flood        import run_flood
from gee.operations.burn_area    import run_burn_area
from gee.operations.urban_heat   import run_urban_heat
from gee.operations.ndwi         import run_ndwi
from gee.operations.evi          import run_evi
from utils.region_resolver       import resolve_region

# ── Operation router ─────────────────────────
OPERATION_MAP = {
    "NDVI"      : run_ndvi,
    "SAR"       : run_sar,
    "LAND_COVER": run_land_cover,
    "FLOOD"     : run_flood,
    "BURN_AREA" : run_burn_area,
    "URBAN_HEAT": run_urban_heat,
    "NDWI"      : run_ndwi,
    "EVI"       : run_evi,
}

# ── Visualization params per operation ───────
VIS_MAP = {
    "NDVI"      : {"min": -0.2, "max": 0.8,  "palette": ["red", "yellow", "lightgreen", "darkgreen"]},
    "EVI"       : {"min": -0.2, "max": 0.8,  "palette": ["red", "yellow", "lightgreen", "darkgreen"]},
    "NDWI"      : {"min": -0.5, "max": 0.5,  "palette": ["brown", "white", "blue"]},
    "SAR"       : {"min": -25,  "max": 0,    "palette": ["black", "white"]},
    "FLOOD"     : {"min": -25,  "max": 0,    "palette": ["white", "blue"]},
    "LAND_COVER": {"min": 1,    "max": 17,   "palette": ["blue", "green", "yellow", "orange", "red"]},
    "BURN_AREA" : {"min": -0.5, "max": 0,    "palette": ["yellow", "orange", "red", "darkred"]},
    "URBAN_HEAT": {"min": 20,   "max": 45,   "palette": ["blue", "yellow", "orange", "red"]},
}

async def execute_command(command: GEECommand) -> dict:
    region  = resolve_region(command.region.value)

    params = {
        "operation"  : command.operation,
        "satellite"  : command.satellite,
        "start_date" : command.date_range.start,
        "end_date"   : command.date_range.end,
        "output_mode": command.output_mode,
        "parameters" : command.parameters or {},
    }

    handler = OPERATION_MAP.get(command.operation)
    if not handler:
        raise ValueError(f"Operation '{command.operation}' ka handler nahi mila")

    image = handler(params, region)

    if command.output_mode == "tile_preview":
        preview_url = get_preview_url(image, region, command.operation)
        return {"preview_url": preview_url}
    else:
        return {"job_id": "export_coming_soon"}


def get_preview_url(image: ee.Image, region: ee.Geometry, operation: str) -> str:
    vis_params = VIS_MAP.get(operation, {"min": 0, "max": 1})

    url = image.visualize(**vis_params).getThumbURL({
        "region"    : region,
        "dimensions": 1024,
        "format"    : "png",
    })
    return url