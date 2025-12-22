from pydantic import BaseModel, Field
from typing import Optional

class FeedbackBase(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    feedback_text: Optional[str] = None

class FeedbackCreate(FeedbackBase):
    response_id: int

class FeedbackResponse(FeedbackBase):
    id: int
    response_id: int
    
    class Config:
        from_attributes = True