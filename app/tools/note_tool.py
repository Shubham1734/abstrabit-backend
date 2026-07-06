from sqlalchemy.orm import Session

from app.services.note_service import NoteService
from app.services.tool_log_service import ToolLogService


class NoteTool:

    @staticmethod
    def save_note(
        db: Session,
        title: str,
        user_id: int,
        workspace_id: int
    ):

        note = NoteService.save_note(
            db=db,
            title=title,
            user_id=user_id,
            workspace_id=workspace_id
        )

        ToolLogService.save_log(
            db=db,
            workspace_id=workspace_id,
            tool_name="save_note",
            arguments={
                "title": title
            },
            status="SUCCESS"
        )

        return {
            "success": True,
            "message": "Note saved successfully.",
            "note_id": note.id,
            "title": note.title
        }

    @staticmethod
    def get_notes(
        db: Session,
        workspace_id: int
    ):

        notes = NoteService.get_notes(
            db=db,
            workspace_id=workspace_id
        )

        return {
            "success": True,
            "notes": [
                {
                    # "id": note.id,
                    "title": note.title
                }
                for note in notes
            ]
        }