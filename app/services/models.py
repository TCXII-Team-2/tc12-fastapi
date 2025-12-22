from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates
from app.services.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String(50), default="user", nullable=False);
    @validates("email")
    def validate_email(self, key, value):
        if "@" not in value:
            raise ValueError("Invalid email")
        return value