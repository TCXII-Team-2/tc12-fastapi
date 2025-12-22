from sqlalchemy.orm import Session
from typing import Optional
from app.models.customer_plan import CustomerPlan

def get_or_create_plan(db: Session, agent_id: int) -> CustomerPlan:
    plan = db.query(CustomerPlan).filter(CustomerPlan.agent_id == agent_id).first()
    if not plan:
        plan = CustomerPlan(agent_id=agent_id)
        db.add(plan)
        db.commit()
        db.refresh(plan)
    return plan

def update_response_count(db: Session, agent_id: int, is_satisfying: bool = False):
    plan = get_or_create_plan(db, agent_id)
    plan.nombre_reponses += 1
    if is_satisfying:
        plan.nombre_reponses_satisfaisantes += 1
    db.commit()
    db.refresh(plan)
    return plan

def get_plan_by_agent(db: Session, agent_id: int) -> Optional[CustomerPlan]:
    return db.query(CustomerPlan).filter(CustomerPlan.agent_id == agent_id).first()