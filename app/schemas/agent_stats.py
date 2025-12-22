from pydantic import BaseModel
from datetime import datetime

class AgentStatsBase(BaseModel):
    nombre_tickets_traites: int = 0
    temps_moyen_reponse: float = 0.0
    taux_satisfaction: float = 0.0

class AgentStatsResponse(AgentStatsBase):
    id: int
    agent_id: int
    date_mise_a_jour: datetime
    
    class Config:
        from_attributes = True