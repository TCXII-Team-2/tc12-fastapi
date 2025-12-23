from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Support Ticket System"
    VERSION: str = "1.0.0"
    DATABASE_URL: str = "sqlite:///./app.db"
    SECRET_KEY: str = "votre-cle-secrete-a-changer"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Workflow API Configuration
    WORKFLOW_API_URL: str = "http://localhost:8001"  # Update with your workflow API URL
    
    class Config:
        case_sensitive = True

settings = Settings()