from fastapi          import APIRouter, HTTPException
from schemas.requests  import ChatRequest
from schemas.responses import ChatResponse
from core.llm_engine   import get_llm_response
from core.validator    import validate_command
from gee.executor      import execute_command
import uuid

router = APIRouter(prefix="/api", tags=["chat"])

# In-memory session store (baad mein DB se replace karenge)
sessions: dict = {}

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):

    # Session handle karo
    session_id = request.session_id or str(uuid.uuid4())
    history    = sessions.get(session_id, [])

    # ── Step 1: LLM se JSON lo ──
    raw_command = get_llm_response(
        user_message=request.message,
        history=history
    )

    if not raw_command:
        raise HTTPException(
            status_code=500,
            detail="LLM se response nahi aaya. Dobara try karo."
        )

    # ── Step 2: Validate karo ──
    command, error = validate_command(raw_command)

    if error:
        # Retry with error context
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

    # ── Step 3: GEE execute karo ──
    result = await execute_command(command)

    # ── Step 4: History update karo ──
    history.append({"role": "user",      "content": request.message})
    history.append({"role": "assistant", "content": str(raw_command)})
    sessions[session_id] = history[-10:]  # last 10 turns

    # ── Step 5: Response return karo ──
    if command.output_mode == "tile_preview":
        return ChatResponse(
            reply      = f"Yeh lo {command.operation} analysis for {command.region.value}!",
            preview_url= result.get("preview_url"),
            session_id = session_id,
        )
    else:
        return ChatResponse(
            reply     = f"Export shuru ho gaya! Job ID: {result.get('job_id')}",
            job_id    = result.get("job_id"),
            session_id= session_id,
        )   