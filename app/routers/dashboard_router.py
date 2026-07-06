from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.utils.oauth2 import get_current_user

from app.services.chat_history_service import ChatHistoryService
from app.services.dashboard_service import DashboardService
from app.services.tool_log_service import ToolLogService

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

# ================= CHAT HISTORY =================
@router.get("/chat-history/{workspace_id}")
def get_chat_history(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)   
):

    history = ChatHistoryService.get_history(db, workspace_id)

    return [
        {
            "id": chat.id,
            "question": chat.user_message,
            "answer": chat.assistant_message,
            "created_at": chat.created_at
        }
        for chat in history
    ]


# ================= TOOL LOGS =================
@router.get("/tool-logs/{workspace_id}")
def get_tool_logs(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)   
):

    logs = ToolLogService.get_logs(db, workspace_id)

    return [
        {
            "id": log.id,
            "tool_name": log.tool_name,
            "arguments": log.arguments,
            "status": log.status,
            "created_at": log.created_at
        }
        for log in logs
    ]


# ================= DASHBOARD =================
@router.get("/{workspace_id}")
def get_dashboard(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)   
):
    return DashboardService.get_dashboard(db, workspace_id)


# ================= RECENT DOCUMENTS =================
@router.get("/{workspace_id}/documents")
def get_recent_documents(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)   
):
    return DashboardService.get_recent_documents(db, workspace_id)


# ================= RECENT CHATS =================
@router.get("/{workspace_id}/chats")
def get_recent_chats(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)   
):
    return DashboardService.get_recent_chats(db, workspace_id)


# ================= RECENT TOOL LOGS =================
@router.get("/{workspace_id}/tool-logs")
def get_recent_tool_logs(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)   
):
    return DashboardService.get_recent_tool_logs(db, workspace_id)