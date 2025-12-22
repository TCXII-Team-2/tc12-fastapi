from sqlalchemy.orm import Session
from app.services.models import User
from app.schemas.user import UserCreate



#USER CRUD OPERATIONS------------------------------------------------------------------------
def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def list_users(db: Session, skip: int = 0, limit: int = 50) -> list[User]:
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, payload: UserCreate) -> User:
    if get_user_by_email(db, payload.email):
        raise ValueError("Email already registered")
    user = User(name=payload.name, email=payload.email, hashed_password=payload.hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int) -> bool:
    user = get_user(db, user_id)
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True

#-------------------------------------------------------------------------------------------
