from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.services.database import Base

class CustomerPlan(Base):
    __tablename__ = "customer_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    nombre_reponses = Column(Integer, default=0)
    nombre_reponses_satisfaisantes = Column(Integer, default=0)
    
    # Relations
    agent = relationship("User", backref="customer_plan")