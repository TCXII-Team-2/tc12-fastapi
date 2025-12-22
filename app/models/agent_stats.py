from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.services.database import Base

class AgentStats(Base):
    __tablename__ = "agent_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    nombre_tickets_traites = Column(Integer, default=0)
    temps_moyen_reponse = Column(Float, default=0.0)  # en minutes
    taux_satisfaction = Column(Float, default=0.0)  # pourcentage
    date_mise_a_jour = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    agent = relationship("User", backref="agent_stats")