from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["jobs"])

@router.get("/jobs/{job_id}")
async def get_job_status(job_id: str):
    return {
        "job_id" : job_id,
        "status" : "coming_soon",
        "message": "Async export coming in next step"
    }