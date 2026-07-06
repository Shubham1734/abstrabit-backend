from sqlalchemy.orm import Session

from app.models.workspace import Workspace
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.models.chat_history import ChatHistory
from app.models.tool_log import ToolLog


class DashboardService:

    @staticmethod
    def get_dashboard(db: Session, workspace_id: int):

        workspace = db.query(Workspace).filter(
            Workspace.id == workspace_id
        ).first()

        if not workspace:
            return {
                "success": False,
                "message": "Workspace not found."
            }

        return {
            "success": True,
            "workspace": {
                "id": workspace.id,
                "name": workspace.name
            },
            "statistics": {
                "documents": db.query(Document).filter(
                    Document.workspace_id == workspace_id
                ).count(),

                "chunks": db.query(DocumentChunk).filter(
                    DocumentChunk.workspace_id == workspace_id
                ).count(),

                "chats": db.query(ChatHistory).filter(
                    ChatHistory.workspace_id == workspace_id
                ).count(),

                "tool_calls": db.query(ToolLog).filter(
                    ToolLog.workspace_id == workspace_id
                ).count()
            }
        }

    @staticmethod
    def get_recent_documents(db: Session, workspace_id: int):

        documents = (
            db.query(Document)
            .filter(Document.workspace_id == workspace_id)
            .order_by(Document.id.desc())
            .limit(5)
            .all()
        )

        return {
            "success": True,
            "documents": [
                {
                    "id": doc.id,
                    "file_name": doc.file_name
                }
                for doc in documents
            ]
        }

    @staticmethod
    def get_recent_chats(db: Session, workspace_id: int):

        chats = (
            db.query(ChatHistory)
            .filter(ChatHistory.workspace_id == workspace_id)
            .order_by(ChatHistory.id.desc())
            .limit(5)
            .all()
        )

        return {
            "success": True,
            "chats": [
                {
                    "id": chat.id,
                    "question": chat.user_message,
                    "answer": chat.assistant_message
                }
                for chat in chats
            ]
        }

    @staticmethod
    def get_recent_tool_logs(db: Session, workspace_id: int):

        logs = (
            db.query(ToolLog)
            .filter(ToolLog.workspace_id == workspace_id)
            .order_by(ToolLog.id.desc())
            .limit(10)
            .all()
        )

        return {
            "success": True,
            "logs": [
                {
                    "id": log.id,
                    "tool_name": log.tool_name,
                    "status": log.status,
                    "created_at": log.created_at
                }
                for log in logs
            ]
        }