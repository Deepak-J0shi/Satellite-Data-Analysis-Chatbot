from pydantic import BaseModel
from typing import Optional

class ChatResponse(BaseModel):
    reply      : str
    preview_url: Optional[str] = None
    job_id     : Optional[str] = None
    session_id : str

class JobStatus(BaseModel):
    job_id    : str
    status    : str
    output_url: Optional[str] = None
    message   : str