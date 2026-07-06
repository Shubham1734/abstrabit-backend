from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.workspace import Workspace


class WorkspaceService:

    @staticmethod
    def create(db: Session, name: str, user_id: int):

        workspace = Workspace(
            name=name,
            user_id=user_id
        )

        db.add(workspace)
        db.commit()
        db.refresh(workspace)

        return workspace

    @staticmethod
    def get_all(db: Session, user_id: int):

        return db.query(
            Workspace
        ).filter(
            Workspace.user_id == user_id
        ).all()

    @staticmethod
    def get_by_id(
            db: Session,
            workspace_id: int,
            user_id: int
    ):

        workspace = db.query(
            Workspace
        ).filter(
            Workspace.id == workspace_id,
            Workspace.user_id == user_id
        ).first()

        if not workspace:
            raise HTTPException(
                status_code=404,
                detail="Workspace not found"
            )

        return workspace

    @staticmethod
    def update(
            db: Session,
            workspace_id: int,
            name: str,
            user_id: int
    ):

        workspace = WorkspaceService.get_by_id(
            db,
            workspace_id,
            user_id
        )

        workspace.name = name

        db.commit()
        db.refresh(workspace)

        return workspace

    @staticmethod
    def delete(
            db: Session,
            workspace_id: int,
            user_id: int
    ):

        workspace = WorkspaceService.get_by_id(
            db,
            workspace_id,
            user_id
        )

        db.delete(workspace)

        db.commit()

        return {
            "message": "Workspace deleted successfully"
        }