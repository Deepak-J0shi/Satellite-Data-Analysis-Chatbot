from pydantic import BaseModel
from typing import Optional, Dict, Any


class ChatResponse(BaseModel):
    reply: str

    preview_url: Optional[str] = None
    job_id: Optional[str] = None

    dataset_info: Optional[Dict[str, Any]] = None
    methodology: Optional[str] = None
    interpretation: Optional[str] = None
    legend: Optional[Dict[str, str]] = None

    session_id: str


class JobStatus(BaseModel):
    job_id: str
    status: str
    output_url: Optional[str] = None
    message: str