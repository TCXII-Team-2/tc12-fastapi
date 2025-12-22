from sqlalchemy import Column, Integer, String, ForeignKey, Text, CheckConstraint
from sqlalchemy.orm import relationship
from app.services.database import Base

class Feedback(Base):
    __tablename__ = "feedbacks"
    
    id = Column(Integer, primary_key=True, index=True)
    response_id = Column(Integer, ForeignKey("responses.id"), nullable=False, unique=True)
    rating = Column(Integer, nullable=False)
    feedback_text = Column(Text, nullable=True)
    
    # Contrainte pour le rating entre 1 et 5
    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='check_rating_range'),
    )
    
    # Relations
    response = relationship("Response", back_populates="feedback")