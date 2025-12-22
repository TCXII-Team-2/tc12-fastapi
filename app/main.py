from fastapi import FastAPI
from app.services.database import Base, engine
app= FastAPI()
from app.api.v1.router import router



Base.metadata.create_all(bind=engine)
app.include_router(router, prefix="/api/v1")