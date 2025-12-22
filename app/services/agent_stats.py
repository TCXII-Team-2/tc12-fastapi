from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.agent_stats import AgentStats
from app.models.response import Response
from app.models.feedback import Feedback
from sqlalchemy import func

def get_or_create_stats(db: Session, agent_id: int) -> AgentStats:
    stats = db.query(AgentStats).filter(AgentStats.agent_id == agent_id).first()
    if not stats:
        stats = AgentStats(agent_id=agent_id)
        db.add(stats)
        db.commit()
        db.refresh(stats)
    return stats

def calculate_agent_stats(db: Session, agent_id: int) -> AgentStats:
    stats = get_or_create_stats(db, agent_id)
    
    # Compter le nombre de tickets traités
    nombre_tickets = db.query(Response).filter(Response.agent_id == agent_id).count()
    stats.nombre_tickets_traites = nombre_tickets
    
    # Calculer le taux de satisfaction
    responses = db.query(Response).filter(Response.agent_id == agent_id).all()
    total_ratings = 0
    count_ratings = 0
    
    for response in responses:
        feedback = db.query(Feedback).filter(Feedback.response_id == response.id).first()
        if feedback:
            total_ratings += feedback.rating
            count_ratings += 1
    
    if count_ratings > 0:
        stats.taux_satisfaction = (total_ratings / (count_ratings * 5)) * 100
    
    db.commit()
    db.refresh(stats)
    return stats

def get_stats_by_agent(db: Session, agent_id: int) -> Optional[AgentStats]:
    return db.query(AgentStats).filter(AgentStats.agent_id == agent_id).first()

def get_all_stats(db: Session) -> List[AgentStats]:
    return db.query(AgentStats).all()