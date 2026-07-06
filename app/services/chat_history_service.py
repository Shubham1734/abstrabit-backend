from sqlalchemy.orm import Session

from app.models.chat_history import ChatHistory


class ChatHistoryService:

    @staticmethod
    def save_chat(
        db: Session,
        workspace_id: int,
        user_message: str,
        assistant_message: str
    ):

        chat = ChatHistory(
            workspace_id=workspace_id,
            user_message=user_message,
            assistant_message=assistant_message
        )

        db.add(chat)
        db.commit()

        db.refresh(chat)

        return chat
    
    @staticmethod
    def get_history(
        db: Session,
        workspace_id: int
    ):

        return db.query(ChatHistory)\
            .filter(
                ChatHistory.workspace_id == workspace_id
            )\
            .order_by(ChatHistory.created_at.desc())\
            .all()