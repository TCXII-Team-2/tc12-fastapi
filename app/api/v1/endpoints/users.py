from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services import database, crud
from app.schemas.user import UserCreate, UserRead

router = APIRouter()

#function to keep the db session alive until the user 
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UserRead, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_user(db, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/all", response_model=list[UserRead])
def list_users(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return crud.list_users(db, skip, limit)

@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_user(db, user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")
    return None
