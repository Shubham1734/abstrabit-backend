from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.chat_schema import ChatRequest
from app.services.rag_service import RagService

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/")
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):

    return RagService.ask(
        db,
        request.workspace_id,
        request.question
    )