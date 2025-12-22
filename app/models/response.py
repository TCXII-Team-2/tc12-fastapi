from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.services.database import Base
import enum

class ResponseType(str, enum.Enum):
    AI = "AI"
    AGENT = "agent"

class Response(Base):
    __tablename__ = "responses"
    
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    response_type = Column(Enum(ResponseType), nullable=False)
    agent_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    response_text = Column(Text, nullable=False)
    date_creation = Column(DateTime, default=datetime.utcnow)
    
    # Relations
    ticket = relationship("Ticket", back_populates="responses")
    agent = relationship("User", backref="responses")
    feedback = relationship("Feedback", back_populates="response", uselist=False, cascade="all, delete-orphan")