from fastapi import FastAPI
app= FastAPI()
from app.api.v1.router import router



#how to import router from router.py file
app.include_router(router, prefix="/api/v1")