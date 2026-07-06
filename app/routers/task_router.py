from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database import get_db
from app.services.task_service import TaskService

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.post("/")
def create_task(
        workspace_id: int,
        title: str,
        db: Session = Depends(get_db)
):

    return TaskService.create_task(
        db,
        workspace_id,
        title
    )


@router.get("/{workspace_id}")
def get_tasks(
        workspace_id: int,
        db: Session = Depends(get_db)
):

    return TaskService.get_tasks(
        db,
        workspace_id
    )