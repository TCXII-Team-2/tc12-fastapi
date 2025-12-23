from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from fastapi import HTTPException
from app.models.ticket import Ticket, TicketStatus
from app.models.response import Response, ResponseType
from app.models.user import User
from app.schemas.ticket import TicketCreate, TicketUpdate
from app.schemas.workflow import TicketIn
from app.services.workflow import run_workflow
import logging

logger = logging.getLogger(__name__)

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


async def create_ticket_with_workflow(db: Session, ticket: TicketCreate, user: User) -> Ticket:
    """
    Create a ticket, send it to the workflow for AI processing, and store the response
    """
    # 1. Create ticket in database
    db_ticket = Ticket(**ticket.model_dump(), user_id=user.id)
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    
    # 2. Get user plan if available (you may need to adjust this based on your user/plan model)
    user_plan = getattr(user, 'plan', None) or "Basic"
    
    try:
        # 3. Prepare workflow input
        workflow_input = TicketIn(
            id=str(db_ticket.id),
            subject=db_ticket.sujet,
            content=db_ticket.description,
            created_at=db_ticket.date_creation.strftime("%Y-%m-%d"),
            userPlan=user_plan
        )
        
        # 4. Send to workflow for processing
        workflow_result = await run_workflow(workflow_input)
        
        # 5. Extract response and validation from workflow result
        response_data = workflow_result.response
        response_text = response_data.get("response_text", "")
        response_type_str = response_data.get("response_type", "solution")
        validation = workflow_result.validation or {}

        # 5.1 If the workflow says the query is invalid/ambiguous or needs clarification,
        # delete the created ticket and do not store any AI response
        is_valid = bool(validation.get("is_valid", True))
        needs_clarification = response_type_str == "clarification_request"
        if not is_valid or needs_clarification:
            message = validation.get("message_to_client") or "Ticket requires clarification or is invalid."
            try:
                db.delete(db_ticket)
                db.commit()
                logger.info(
                    f"Ticket {db_ticket.id} deleted due to validation failure or clarification needed"
                )
            except Exception as del_err:
                logger.error(f"Failed to delete invalid ticket {db_ticket.id}: {del_err}")
            # Surface a clear error to the client so the UI can prompt for more details
            raise HTTPException(status_code=400, detail=message)
        
        # 6. Store AI response in database
        if response_text:
            ai_response = Response(
                ticket_id=db_ticket.id,
                response_type=ResponseType.AI,
                response_text=response_text,
                agent_id=None
            )
            db.add(ai_response)
        
        # 7. Update ticket status based on workflow result
        confidence = workflow_result.confidence
        
        if response_type_str == "escalation_notice" or confidence.get("should_escalate", False):
            db_ticket.statut = TicketStatus.ESCALADE
        elif response_type_str == "solution":
            db_ticket.statut = TicketStatus.TRAITEE_AI
        elif response_type_str in ["clarification_request", "out_of_scope"]:
            db_ticket.statut = TicketStatus.EN_TRAITEMENT
        else:
            db_ticket.statut = TicketStatus.TRAITEE_AI
        
        db.commit()
        db.refresh(db_ticket)
        
        logger.info(f"Ticket {db_ticket.id} processed by workflow with status {db_ticket.statut}")
        
    except HTTPException:
        # Re-raise HTTPExceptions (validation errors, etc.)
        raise
    except Exception as e:
        # If workflow fails, keep ticket in processing status
        logger.error(f"Workflow processing failed for ticket {db_ticket.id}: {str(e)}")
        db_ticket.statut = TicketStatus.EN_TRAITEMENT
        db.commit()
        db.refresh(db_ticket)
    
    return db_ticket


async def reprocess_ticket_with_workflow(db: Session, ticket: Ticket) -> Ticket:
    """
    Reprocess an existing ticket through the workflow
    """
    # Get the ticket owner
    user = db.query(User).filter(User.id == ticket.user_id).first()
    if not user:
        logger.error(f"User not found for ticket {ticket.id}")
        return ticket
    
    user_plan = getattr(user, 'plan', None) or "Basic"
    
    try:
        # Prepare workflow input
        workflow_input = TicketIn(
            id=str(ticket.id),
            subject=ticket.sujet,
            content=ticket.description,
            created_at=ticket.date_creation.strftime("%Y-%m-%d"),
            userPlan=user_plan
        )
        
        # Send to workflow for processing
        workflow_result = await run_workflow(workflow_input)
        
        # Extract response from workflow result
        response_data = workflow_result.response
        response_text = response_data.get("response_text", "")
        response_type_str = response_data.get("response_type", "solution")
        
        # Store new AI response in database
        if response_text:
            ai_response = Response(
                ticket_id=ticket.id,
                response_type=ResponseType.AI,
                response_text=response_text,
                agent_id=None
            )
            db.add(ai_response)
        
        # Update ticket status based on workflow result
        validation = workflow_result.validation
        confidence = workflow_result.confidence
        
        if response_type_str == "escalation_notice" or confidence.get("should_escalate", False):
            ticket.statut = TicketStatus.ESCALADE
        elif response_type_str == "solution":
            ticket.statut = TicketStatus.TRAITEE_AI
        elif response_type_str in ["clarification_request", "out_of_scope"]:
            ticket.statut = TicketStatus.EN_TRAITEMENT
        else:
            ticket.statut = TicketStatus.TRAITEE_AI
        
        db.commit()
        db.refresh(ticket)
        
        logger.info(f"Ticket {ticket.id} reprocessed by workflow with status {ticket.statut}")
        
    except Exception as e:
        # If workflow fails, log error but don't change status
        logger.error(f"Workflow reprocessing failed for ticket {ticket.id}: {str(e)}")
        raise
    
    return ticket