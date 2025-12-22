from sqlalchemy.orm import Session
from typing import Optional
from app.models.ai_stats import AIStats
from app.models.response import Response, ResponseType
from app.models.ticket import Ticket, TicketStatus
from app.models.feedback import Feedback

def get_or_create_stats(db: Session) -> AIStats:
    stats = db.query(AIStats).first()
    if not stats:
        stats = AIStats()
        db.add(stats)
        db.commit()
        db.refresh(stats)
    return stats

def calculate_ai_stats(db: Session) -> AIStats:
    stats = get_or_create_stats(db)
    
    # Nombre de réponses générées par l'IA
    stats.nombre_reponses_generees = db.query(Response).filter(
        Response.response_type == ResponseType.AI
    ).count()
    
    # Nombre de tickets résolus par l'IA
    stats.nombre_tickets_resolus = db.query(Ticket).filter(
        Ticket.statut == TicketStatus.TRAITEE_AI
    ).count()
    
    # Nombre d'escalades
    stats.nombre_escalades = db.query(Ticket).filter(
        Ticket.statut == TicketStatus.ESCALADE
    ).count()
    
    # Calculer le taux de résolution
    total_ai_tickets = stats.nombre_reponses_generees
    if total_ai_tickets > 0:
        stats.taux_resolution = (stats.nombre_tickets_resolus / total_ai_tickets) * 100
    
    # Calculer la précision moyenne basée sur les feedbacks
    ai_responses = db.query(Response).filter(
        Response.response_type == ResponseType.AI
    ).all()
    
    total_ratings = 0
    count_ratings = 0
    
    for response in ai_responses:
        feedback = db.query(Feedback).filter(Feedback.response_id == response.id).first()
        if feedback:
            total_ratings += feedback.rating
            count_ratings += 1
    
    if count_ratings > 0:
        stats.precision_moyenne = (total_ratings / (count_ratings * 5)) * 100
    
    db.commit()
    db.refresh(stats)
    return stats

def get_stats(db: Session) -> Optional[AIStats]:
    return db.query(AIStats).first()

def increment_ai_response(db: Session):
    stats = get_or_create_stats(db)
    stats.nombre_reponses_generees += 1
    db.commit()
    return stats

def increment_escalation(db: Session):
    stats = get_or_create_stats(db)
    stats.nombre_escalades += 1
    db.commit()
    return stats