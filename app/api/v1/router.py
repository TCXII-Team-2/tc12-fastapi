from app.api.v1.endpoints import task  
from fastapi import APIRouter

router = APIRouter()

router.include_router(task.router, prefix="/tasks", tags=["tasks"])

