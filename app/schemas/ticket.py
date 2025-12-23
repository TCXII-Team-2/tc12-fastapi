from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.models.ticket import TicketStatus

class TicketBase(BaseModel):
    sujet: str
    description: str
    date_probleme: datetime

class TicketCreate(TicketBase):
    pass

class TicketUpdate(BaseModel):
    sujet: Optional[str] = None
    description: Optional[str] = None
    statut: Optional[TicketStatus] = None

class TicketResponse(TicketBase):
    id: int
    date_creation: datetime
    user_id: int
    statut: TicketStatus
    
    class Config:
        from_attributes = True


class ResponseItem(BaseModel):
    id: int
    response_type: str
    response_text: str
    date_creation: datetime
    agent_id: Optional[int] = None
    
    class Config:
        from_attributes = True


class TicketWithResponses(TicketResponse):
    responses: List[ResponseItem] = []
    
    class Config:
        from_attributes = True