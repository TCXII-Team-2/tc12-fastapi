from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.services.database import get_db
from app.schemas.agent_stats import AgentStatsResponse
from app.services.agent_stats import get_all_stats, get_stats_by_agent, calculate_agent_stats
from app.core.dependencies import get_current_user, require_role
from app.models.user import User

router = APIRouter(prefix="")

@router.get("/", response_model=List[AgentStatsResponse])
def get_all_agent_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    """Get stats for all agents (admin only)"""
    return get_all_stats(db)

@router.get("/agent/{agent_id}", response_model=AgentStatsResponse)
def get_agent_stats(
    agent_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["agent", "admin"]))
):
    """Get stats for a specific agent"""
    if current_user.role == "agent" and current_user.id != agent_id:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    stats = get_stats_by_agent(db, agent_id)
    if not stats:
        # Create and calculate stats if not exist
        stats = calculate_agent_stats(db, agent_id)
    return stats

@router.get("/me", response_model=AgentStatsResponse)
def get_my_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["agent"]))
):
    """Get own stats"""
    stats = calculate_agent_stats(db, current_user.id)
    return stats

@router.post("/agent/{agent_id}/refresh", response_model=AgentStatsResponse)
def refresh_agent_stats(
    agent_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    """Refresh stats for an agent"""
    stats = calculate_agent_stats(db, agent_id)
    return stats