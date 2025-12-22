from sqlalchemy import Column, Integer, Float, DateTime
from datetime import datetime
from app.services.database import Base

class AIStats(Base):
    __tablename__ = "ai_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre_reponses_generees = Column(Integer, default=0)
    nombre_tickets_resolus = Column(Integer, default=0)
    nombre_escalades = Column(Integer, default=0)
    taux_resolution = Column(Float, default=0.0)  # pourcentage
    precision_moyenne = Column(Float, default=0.0)  # pourcentage
    date_mise_a_jour = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)