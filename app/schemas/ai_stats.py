from pydantic import BaseModel
from datetime import datetime

class AIStatsBase(BaseModel):
    nombre_reponses_generees: int = 0
    nombre_tickets_resolus: int = 0
    nombre_escalades: int = 0
    taux_resolution: float = 0.0
    precision_moyenne: float = 0.0

class AIStatsResponse(AIStatsBase):
    id: int
    date_mise_a_jour: datetime
    
    class Config:
        from_attributes = True