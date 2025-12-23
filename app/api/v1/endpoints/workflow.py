from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import List, Optional
from app.schemas.workflow import (
    TicketIn, WorkflowResponse, QuestionsIn, AnswersOut,
    KnowledgeUploadResponse, KnowledgeRebuildResponse
)
from app.services.workflow import (
    run_workflow, answer_bulk_questions,
    upload_knowledge_files, rebuild_knowledge_base
)
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="")


@router.post("/run", response_model=WorkflowResponse, status_code=200)
async def run_workflow_endpoint(
    ticket_data: TicketIn,
    current_user: User = Depends(get_current_user)
):
    """
    Run workflow to analyze and process a ticket.
    
    - **id**: Optional ticket identifier
    - **subject**: Ticket subject (required)
    - **content**: Ticket content/description (required)
    - **created_at**: ISO date string (required) e.g. "2025-12-23"
    - **userPlan**: Optional user plan (e.g. "Pro", "Basic")
    
    Returns detailed analysis, validation, RAG retrieval, confidence evaluation, and generated response.
    """
    return await run_workflow(ticket_data)


@router.post("/answer-questions", response_model=AnswersOut, status_code=200)
async def answer_questions_endpoint(
    questions: QuestionsIn,
    current_user: User = Depends(get_current_user)
):
    """
    Bulk Q&A endpoint (Jury format).
    
    Processes multiple questions and returns answers for each.
    
    - **Questions**: Array of question objects with id and query fields
    
    Returns team name and array of answers matching the input question IDs.
    """
    return await answer_bulk_questions(questions)


@router.post("/knowledge/upload", response_model=KnowledgeUploadResponse, status_code=200)
async def upload_knowledge_endpoint(
    files: List[UploadFile] = File(..., description="Markdown files (.md) to upload to knowledge base"),
    trigger_rebuild: bool = Form(True, description="Whether to trigger knowledge base rebuild"),
    current_user: User = Depends(get_current_user)
):
    """
    Upload knowledge base files.
    
    - **files**: One or more .md files to add to the knowledge base
    - **trigger_rebuild**: Whether to trigger automatic rebuild (default: true)
    
    Returns list of saved file paths and rebuild status.
    
    Note: Only .md files are accepted. Non-markdown files will be rejected.
    """
    # Validate that all files are markdown
    for file in files:
        if not file.filename.endswith('.md'):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type: {file.filename}. Only .md files are allowed."
            )
    
    # Check admin role (optional - adjust based on your requirements)
    if current_user.role not in ["admin", "agent"]:
        raise HTTPException(
            status_code=403,
            detail="Only admins and agents can upload knowledge base files"
        )
    
    return await upload_knowledge_files(files, trigger_rebuild)


@router.post("/knowledge/rebuild", response_model=KnowledgeRebuildResponse, status_code=200)
async def rebuild_knowledge_endpoint(
    async_run: bool = True,
    current_user: User = Depends(get_current_user)
):
    """
    Rebuild the knowledge base.
    
    - **async_run**: If true, starts rebuild in background and returns immediately (default: true)
    
    Returns status indicating whether rebuild started or completed.
    """
    # Check admin role (optional - adjust based on your requirements)
    if current_user.role not in ["admin", "agent"]:
        raise HTTPException(
            status_code=403,
            detail="Only admins and agents can rebuild the knowledge base"
        )
    
    return await rebuild_knowledge_base(async_run)
