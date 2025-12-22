from app.api.v1.endpoints import task , users 
from fastapi import APIRouter

router = APIRouter()

router.include_router(task.router, prefix="/tasks", tags=["tasks"])
router.include_router(users.router, prefix="/users", tags=["users"])
