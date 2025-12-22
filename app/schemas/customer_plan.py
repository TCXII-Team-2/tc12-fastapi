from pydantic import BaseModel

class CustomerPlanBase(BaseModel):
    nombre_reponses: int = 0
    nombre_reponses_satisfaisantes: int = 0

class CustomerPlanResponse(CustomerPlanBase):
    id: int
    agent_id: int
    
    class Config:
        from_attributes = True