from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.services.database import get_db
from app.schemas.response import ResponseCreate, ResponseResponse
from app.services.response import create_response, get_responses_by_ticket, get_responses_by_agent, get_response
from app.core.dependencies import get_current_user, require_role
from app.models.user import User

router = APIRouter(prefix="")

@router.post("/", response_model=ResponseResponse, status_code=201)
def create_response_endpoint(
    response: ResponseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["agent", "admin"]))
):
    return create_response(db, response)

@router.get("/ticket/{ticket_id}", response_model=List[ResponseResponse])
def get_responses_by_ticket_endpoint(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_responses_by_ticket(db, ticket_id)

@router.get("/agent/{agent_id}", response_model=List[ResponseResponse])
def get_responses_by_agent_endpoint(
    agent_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["agent", "admin"]))
):
    return get_responses_by_agent(db, agent_id)

@router.get("/{response_id}", response_model=ResponseResponse)
def get_response_endpoint(
    response_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_response = get_response(db, response_id)
    if not db_response:
        raise HTTPException(status_code=404, detail="Response not found")
    return db_response