from app.api.v1.endpoints import users, auth, tickets, responses, feedbacks, customer_plans, agents_stats, ai_stats, workflow
from fastapi import APIRouter

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(tickets.router, prefix="/tickets", tags=["tickets"])
router.include_router(responses.router, prefix="/responses", tags=["responses"])
router.include_router(feedbacks.router, prefix="/feedbacks", tags=["feedbacks"])
router.include_router(customer_plans.router, prefix="/customer-plans", tags=["customer-plans"])
router.include_router(agents_stats.router, prefix="/agent-stats", tags=["agent-stats"])
router.include_router(ai_stats.router, prefix="/ai-stats", tags=["ai-stats"])
router.include_router(workflow.router, prefix="/workflow", tags=["workflow"])
