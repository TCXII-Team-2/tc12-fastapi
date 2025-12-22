from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.response import Response
from app.schemas.response import ResponseCreate

def create_response(db: Session, response: ResponseCreate) -> Response:
    db_response = Response(**response.model_dump())
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return db_response

def get_response(db: Session, response_id: int) -> Optional[Response]:
    return db.query(Response).filter(Response.id == response_id).first()

def get_responses_by_ticket(db: Session, ticket_id: int) -> List[Response]:
    return db.query(Response).filter(Response.ticket_id == ticket_id).all()

def get_responses_by_agent(db: Session, agent_id: int) -> List[Response]:
    return db.query(Response).filter(Response.agent_id == agent_id).all()