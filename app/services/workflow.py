import httpx
from typing import Dict, Any, List
from fastapi import UploadFile, HTTPException
from app.core.config import settings
from app.schemas.workflow import (
    TicketIn, WorkflowResponse, QuestionsIn, AnswersOut,
    KnowledgeUploadResponse, KnowledgeRebuildResponse
)


async def run_workflow(ticket_data: TicketIn) -> WorkflowResponse:
    """
    Send ticket to workflow API for processing
    """
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(
                f"{settings.WORKFLOW_API_URL}/workflow/run",
                json=ticket_data.model_dump(exclude_none=True),
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return WorkflowResponse(**response.json())
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Workflow API error: {e.response.text}"
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to connect to workflow API: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error: {str(e)}"
            )


async def answer_bulk_questions(questions_data: QuestionsIn) -> AnswersOut:
    """
    Send bulk questions to workflow API for processing
    """
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            response = await client.post(
                f"{settings.WORKFLOW_API_URL}/workflow/answer-questions",
                json=questions_data.model_dump(),
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return AnswersOut(**response.json())
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Workflow API error: {e.response.text}"
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to connect to workflow API: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error: {str(e)}"
            )


async def upload_knowledge_files(
    files: List[UploadFile],
    trigger_rebuild: bool = True
) -> KnowledgeUploadResponse:
    """
    Upload knowledge base files to workflow API
    """
    async with httpx.AsyncClient(timeout=180.0) as client:
        try:
            # Prepare files for multipart upload
            files_data = []
            for file in files:
                content = await file.read()
                files_data.append(
                    ("files", (file.filename, content, file.content_type or "text/markdown"))
                )
                # Reset file pointer for potential reuse
                await file.seek(0)
            
            # Prepare form data
            data = {"trigger_rebuild": str(trigger_rebuild).lower()}
            
            response = await client.post(
                f"{settings.WORKFLOW_API_URL}/admin/knowledge/upload",
                files=files_data,
                data=data
            )
            response.raise_for_status()
            return KnowledgeUploadResponse(**response.json())
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Workflow API error: {e.response.text}"
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to connect to workflow API: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error: {str(e)}"
            )


async def rebuild_knowledge_base(async_run: bool = True) -> KnowledgeRebuildResponse:
    """
    Trigger knowledge base rebuild in workflow API
    """
    async with httpx.AsyncClient(timeout=300.0) as client:
        try:
            response = await client.post(
                f"{settings.WORKFLOW_API_URL}/admin/knowledge/rebuild",
                params={"async_run": async_run}
            )
            response.raise_for_status()
            return KnowledgeRebuildResponse(**response.json())
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Workflow API error: {e.response.text}"
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to connect to workflow API: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error: {str(e)}"
            )
