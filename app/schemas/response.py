from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.response import ResponseType

class ResponseBase(BaseModel):
    ticket_id: int
    response_type: ResponseType
    response_text: str

class ResponseCreate(ResponseBase):
    agent_id: Optional[int] = None

class ResponseResponse(ResponseBase):
    id: int
    agent_id: Optional[int]
    date_creation: datetime
    
    class Config:
        from_attributes = True