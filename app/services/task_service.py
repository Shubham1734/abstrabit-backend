from sqlalchemy.orm import Session

from app.models.task import Task


class TaskService:

    @staticmethod
    def create_task(
            db: Session,
            workspace_id: int,
            title: str
    ):

        task = Task(
            workspace_id=workspace_id,
            title=title
        )

        db.add(task)
        db.commit()
        db.refresh(task)

        return task

    @staticmethod
    def get_tasks(
            db: Session,
            workspace_id: int
    ):

        return db.query(Task).filter(
            Task.workspace_id == workspace_id
        ).all()