from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.database import get_db
from app.schemas.ai_stats import AIStatsResponse
from app.services.ai_stats import get_stats, calculate_ai_stats
from app.core.dependencies import require_role
from app.models.user import User

router = APIRouter(prefix="")

@router.get("/", response_model=AIStatsResponse)
def get_ai_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "agent"]))
):
    """Get global AI stats"""
    stats = get_stats(db)
    if not stats:
        stats = calculate_ai_stats(db)
    return stats

@router.post("/refresh", response_model=AIStatsResponse)
def refresh_ai_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    """Recalculate AI stats"""
    return calculate_ai_stats(db)