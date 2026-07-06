from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.workspace_schema import (
    WorkspaceCreate,
    WorkspaceUpdate
)
from app.services.workspace_service import WorkspaceService
from app.utils.oauth2 import get_current_user

router = APIRouter(
    prefix="/workspaces",
    tags=["Workspaces"]
)


@router.post("/")
def create_workspace(
    request: WorkspaceCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return WorkspaceService.create(
        db,
        request.name,
        current_user.id
    )


@router.get("/")
def get_workspaces(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return WorkspaceService.get_all(
        db,
        current_user.id
    )


@router.get("/{workspace_id}")
def get_workspace(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return WorkspaceService.get_by_id(
        db,
        workspace_id,
        current_user.id
    )


@router.put("/{workspace_id}")
def update_workspace(
    workspace_id: int,
    request: WorkspaceUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return WorkspaceService.update(
        db,
        workspace_id,
        request.name,
        current_user.id
    )


@router.delete("/{workspace_id}")
def delete_workspace(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return WorkspaceService.delete(
        db,
        workspace_id,
        current_user.id
    )