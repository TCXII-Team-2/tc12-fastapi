from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.database import get_db
from app.schemas.customer_plan import CustomerPlanResponse
from app.services.customer_plan import get_plan_by_agent, get_or_create_plan
from app.core.dependencies import get_current_user, require_role
from app.models.user import User

router = APIRouter(prefix="")

@router.get("/agent/{agent_id}", response_model=CustomerPlanResponse)
def get_customer_plan(
    agent_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["agent", "admin"]))
):
    """Get customer plan for an agent"""
    if current_user.role == "agent" and current_user.id != agent_id:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    plan = get_plan_by_agent(db, agent_id)
    if not plan:
        # Create plan if not exists
        plan = get_or_create_plan(db, agent_id)
    return plan

@router.get("/me", response_model=CustomerPlanResponse)
def get_my_customer_plan(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["agent"]))
):
    """Get own customer plan"""
    plan = get_or_create_plan(db, current_user.id)
    return plan