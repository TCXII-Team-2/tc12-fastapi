from sqlalchemy.orm import Session
from typing import Optional
from app.models.feedback import Feedback
from app.schemas.feedback import FeedbackCreate

def create_feedback(db: Session, feedback: FeedbackCreate) -> Feedback:
    db_feedback = Feedback(**feedback.model_dump())
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

def get_feedback(db: Session, feedback_id: int) -> Optional[Feedback]:
    return db.query(Feedback).filter(Feedback.id == feedback_id).first()

def get_feedback_by_response(db: Session, response_id: int) -> Optional[Feedback]:
    return db.query(Feedback).filter(Feedback.response_id == response_id).first()