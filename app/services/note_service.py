from sqlalchemy.orm import Session

from app.models.note import Note


class NoteService:

    @staticmethod
    def save_note(
        db: Session,
        title: str,
        user_id: int,
        workspace_id: int
    ):

        note = Note(
            title=title,
            user_id=user_id,
            workspace_id=workspace_id
        )

        db.add(note)
        db.commit()
        db.refresh(note)

        return note

    @staticmethod
    def get_notes(
        db: Session,
        workspace_id: int
    ):

        return (
            db.query(Note)
            .filter(Note.workspace_id == workspace_id)
            .all()
        )