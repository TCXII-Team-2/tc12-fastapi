from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.services.database import Base, engine
from app.core.config import settings

# Import all models for table creation
from app.models.user import User
from app.models.ticket import Ticket
from app.models.response import Response
from app.models.feedback import Feedback
from app.models.customer_plan import CustomerPlan
from app.models.agent_stats import AgentStats
from app.models.ai_stats import AIStats

from app.api.v1.router import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API de gestion de tickets de support avec IA et agents",
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")

@app.get("/")
def root():
    return {
        "message": f"Bienvenue sur {settings.PROJECT_NAME}",
    }