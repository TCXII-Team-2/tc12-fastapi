from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.ticket import Ticket, TicketStatus
from app.schemas.ticket import TicketCreate, TicketUpdate

def create_ticket(db: Session, ticket: TicketCreate, user_id: int) -> Ticket:
    db_ticket = Ticket(**ticket.model_dump(), user_id=user_id)
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

def get_ticket(db: Session, ticket_id: int) -> Optional[Ticket]:
    return db.query(Ticket).filter(Ticket.id == ticket_id).first()

def get_tickets(db: Session, skip: int = 0, limit: int = 100) -> List[Ticket]:
    return db.query(Ticket).offset(skip).limit(limit).all()

def get_tickets_by_user(db: Session, user_id: int) -> List[Ticket]:
    return db.query(Ticket).filter(Ticket.user_id == user_id).all()

def get_tickets_by_status(db: Session, status: TicketStatus) -> List[Ticket]:
    return db.query(Ticket).filter(Ticket.statut == status).all()

def update_ticket(db: Session, ticket_id: int, ticket: TicketUpdate) -> Optional[Ticket]:
    db_ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not db_ticket:
        return None
    
    update_data = ticket.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_ticket, key, value)
    
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

def delete_ticket(db: Session, ticket_id: int) -> bool:
    db_ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not db_ticket:
        return False
    db.delete(db_ticket)
    db.commit()
    return True