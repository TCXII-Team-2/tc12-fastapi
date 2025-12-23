from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.services.database import get_db
from app.schemas.ticket import TicketCreate, TicketUpdate, TicketResponse, TicketWithResponses
from app.services.ticket import create_ticket_with_workflow, get_tickets, get_tickets_by_user, get_tickets_by_status, get_ticket, update_ticket, delete_ticket, reprocess_ticket_with_workflow
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.ticket import TicketStatus

router = APIRouter(prefix="")

@router.post("/", response_model=TicketResponse, status_code=201)
async def create_ticket_endpoint(
    ticket: TicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await create_ticket_with_workflow(db, ticket, current_user)

@router.get("/", response_model=List[TicketResponse])
def get_tickets_endpoint(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == "client":
        return get_tickets_by_user(db, current_user.id)
    return get_tickets(db, skip, limit)

@router.get("/status/{status}", response_model=List[TicketResponse])
def get_tickets_by_status_endpoint(
    status: TicketStatus,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_tickets_by_status(db, status)

@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket_endpoint(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_ticket = get_ticket(db, ticket_id)
    if not db_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    if current_user.role == "client" and db_ticket.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    return db_ticket


@router.get("/{ticket_id}/details", response_model=TicketWithResponses)
def get_ticket_details_endpoint(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get ticket with all responses (AI and agent responses)
    """
    db_ticket = get_ticket(db, ticket_id)
    if not db_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    if current_user.role == "client" and db_ticket.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    return db_ticket

@router.put("/{ticket_id}", response_model=TicketResponse)
def update_ticket_endpoint(
    ticket_id: int,
    ticket: TicketUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_ticket = get_ticket(db, ticket_id)
    if not db_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    if current_user.role == "client" and db_ticket.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    updated_ticket = update_ticket(db, ticket_id, ticket)
    return updated_ticket

@router.delete("/{ticket_id}")
def delete_ticket_endpoint(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_ticket = get_ticket(db, ticket_id)
    if not db_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    if current_user.role not in ["admin", "agent"]:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    success = delete_ticket(db, ticket_id)
    return {"message": "Ticket deleted successfully"}


@router.post("/{ticket_id}/reprocess", response_model=TicketResponse, status_code=200)
async def reprocess_ticket_endpoint(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Manually reprocess an existing ticket through the workflow.
    Useful for tickets that need re-evaluation or failed initial processing.
    """
    db_ticket = get_ticket(db, ticket_id)
    if not db_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    # Only agents and admins can manually reprocess tickets
    if current_user.role not in ["admin", "agent"]:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    return await reprocess_ticket_with_workflow(db, db_ticket)