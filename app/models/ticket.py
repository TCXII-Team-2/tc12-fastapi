from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.services.database import Base
import enum

class TicketStatus(str, enum.Enum):
    EN_TRAITEMENT = "en_traitement"
    TRAITEE_AI = "traitee_ai"
    TRAITEE_AGENT = "traitee_agent"
    ESCALADE = "escalade"
    REJETEE = "rejetee"

class Ticket(Base):
    __tablename__ = "tickets"
    
    id = Column(Integer, primary_key=True, index=True)
    date_creation = Column(DateTime, default=datetime.utcnow)
    sujet = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    date_probleme = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    statut = Column(Enum(TicketStatus), default=TicketStatus.EN_TRAITEMENT, nullable=False)
    
    # Relations
    user = relationship("User", backref="tickets")
    responses = relationship("Response", back_populates="ticket", cascade="all, delete-orphan")