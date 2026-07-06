from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database import get_db

from app.services.document_service import DocumentService

from app.utils.oauth2 import get_current_user
from app.services.embedding_service import EmbeddingService
from app.services.vector_search_service import VectorSearchService
router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.post("/upload/{workspace_id}")
async def upload_document(
    workspace_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return await DocumentService.upload_document(
        db,
        file,
        workspace_id,
        current_user
    )


# @router.get("/test-search")
# def test_search(db: Session = Depends(get_db)):

#     embedding = EmbeddingService.generate_embedding(
#         "Define PPL?"
#     )

#     rows = VectorSearchService.search(
#         db=db,
#         workspace_id=1,
#         embedding=embedding
#     )

#     return rows
@router.get("/{workspace_id}")
def get_documents(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return DocumentService.get_documents(
        db,
        workspace_id,
        current_user
    )


@router.get("/download/{document_id}")
def download_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return DocumentService.get_download_url(
        db,
        document_id,
        current_user
    )


@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return DocumentService.delete_document(
        db,
        document_id,
        current_user
    )

