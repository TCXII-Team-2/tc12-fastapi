from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


# Run Workflow Schemas
class TicketIn(BaseModel):
    id: Optional[str] = None
    subject: str
    content: str
    created_at: str = Field(..., description="ISO date string e.g. 2025-12-23")
    userPlan: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "123",
                "subject": "Billing issue",
                "content": "I was charged twice",
                "created_at": "2025-12-23",
                "userPlan": "Pro"
            }
        }


class WorkflowResponse(BaseModel):
    analysis: Dict[str, Any]
    validation: Dict[str, Any]
    rag: Any  # Can be dict or list
    confidence: Dict[str, Any]
    response: Dict[str, Any]

    class Config:
        json_schema_extra = {
            "example": {
                "analysis": {"intent": "billing_inquiry"},
                "validation": {"is_valid": True, "validation_status": "valid"},
                "rag": {"documents": [], "scores": []},
                "confidence": {"suggested_action": "respond", "should_escalate": False},
                "response": {
                    "response_text": "Here is the solution...",
                    "response_type": "solution",
                    "language": "English"
                }
            }
        }


# Bulk Q&A Schemas
class QuestionItem(BaseModel):
    id: str
    query: str


class QuestionsIn(BaseModel):
    Questions: List[QuestionItem]

    class Config:
        json_schema_extra = {
            "example": {
                "Questions": [
                    {"id": "q1", "query": "How do I reset password?"},
                    {"id": "q2", "query": "What are your plans?"}
                ]
            }
        }


class AnswerItem(BaseModel):
    id: str
    answer: str


class AnswersOut(BaseModel):
    Team: str
    Answers: List[AnswerItem]

    class Config:
        json_schema_extra = {
            "example": {
                "Team": "TEAM 02",
                "Answers": [
                    {"id": "q1", "answer": "To reset..."},
                    {"id": "q2", "answer": "We offer..."}
                ]
            }
        }


# Knowledge Base Upload Schemas
class KnowledgeUploadResponse(BaseModel):
    saved: List[str]
    rebuild_triggered: bool

    class Config:
        json_schema_extra = {
            "example": {
                "saved": ["C:\\...\\knowledge_base\\FAQ.md"],
                "rebuild_triggered": True
            }
        }


# Knowledge Base Rebuild Schemas
class KnowledgeRebuildResponse(BaseModel):
    status: str

    class Config:
        json_schema_extra = {
            "example": {
                "status": "rebuild started"
            }
        }
