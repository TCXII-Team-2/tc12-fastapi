from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.database import get_db
from app.schemas.feedback import FeedbackCreate, FeedbackResponse
from app.services.feedback import create_feedback, get_feedback_by_response
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="")

@router.post("/", response_model=FeedbackResponse, status_code=201)
def create_feedback_endpoint(
    feedback: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if feedback already exists for this response
    existing_feedback = get_feedback_by_response(db, feedback.response_id)
    if existing_feedback:
        raise HTTPException(status_code=400, detail="Feedback already exists for this response")
    
    return create_feedback(db, feedback)

@router.get("/response/{response_id}", response_model=FeedbackResponse)
def get_feedback_by_response_endpoint(
    response_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_feedback = get_feedback_by_response(db, response_id)
    if not db_feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return db_feedback