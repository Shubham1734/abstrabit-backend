import uuid

from fastapi import UploadFile
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.tool_log import ToolLog
from app.models.workspace import Workspace

from app.utils.supabase_client import supabase
from app.models.document_chunk import DocumentChunk
from app.services.chunk_service import ChunkService
from app.services.pdf_service import PdfService
from app.services.embedding_service import EmbeddingService

class DocumentService:

    @staticmethod
    async def upload_document(
        db: Session,
        file: UploadFile,
        workspace_id: int,
        current_user
    ):

        workspace = db.query(Workspace).filter(
            Workspace.id == workspace_id,
            Workspace.user_id == current_user.id
        ).first()

        if workspace is None:
            raise HTTPException(
                status_code=404,
                detail="Workspace not found"
            )

        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed"
            )

        unique_name = f"{uuid.uuid4()}_{file.filename}"

        storage_path = (
            f"workspace-{workspace_id}/{unique_name}"
        )

        file_bytes = await file.read()

        try:

            supabase.storage \
                .from_("documents") \
                .upload(
                    path=storage_path,
                    file=file_bytes,
                    file_options={
                        "content-type": "application/pdf"
                    }
                )
            print("UPLOAD RESPONSE")

        except Exception as e:
            traceback.print_exc()

            print(type(e))
            print(e)

            raise

        document = Document(
            workspace_id=workspace_id,
            file_name=file.filename,
            storage_path=storage_path
        )

        db.add(document)

        db.commit()

        db.refresh(document)
        # Extract text from uploaded PDF
        text = PdfService.extract_text(file_bytes)

        print("=" * 50)
        print("Extracted Text")
        print("=" * 50)
        print(text)

        if not text.strip():
            raise HTTPException(
                status_code=400,
                detail="No readable text found in PDF."
            )

        # Split into chunks
        chunks = ChunkService.split_text(text)

        print(f"Total Chunks: {len(chunks)}")

        # Save chunks
        for index, chunk in enumerate(chunks):

            embedding = EmbeddingService.generate_embedding(chunk)

            db_chunk = DocumentChunk(
                document_id=document.id,
                workspace_id=workspace_id,
                chunk_index=index,
                chunk_text=chunk,
                embedding=embedding
            )

            db.add(db_chunk)

        db.commit()

        return {
            "message": "Document uploaded successfully",
            "document_id": document.id,
            "chunks": len(chunks)
        }

    @staticmethod
    def get_documents(
        db: Session,
        workspace_id: int,
        current_user
    ):

        workspace = (
            db.query(Workspace)
            .filter(
                Workspace.id == workspace_id,
                Workspace.user_id == current_user.id
            )
            .first()
        )

        if not workspace:
            raise HTTPException(
                status_code=404,
                detail="Workspace not found"
            )

        return (
            db.query(Document)
            .filter(Document.workspace_id == workspace_id)
            .all()
        )
        
    @staticmethod
    def get_download_url(
        db: Session,
        document_id: int,
        current_user
    ):

        document = (
            db.query(Document)
            .join(Workspace)
            .filter(
                Document.id == document_id,
                Workspace.user_id == current_user.id
            )
            .first()
        )

        if not document:
            raise HTTPException(
                status_code=404,
                detail="Document not found"
            )

        result = supabase.storage.from_("documents").create_signed_url(
            document.file_path,
            3600
        )

        return {
            "url": result["signedURL"]
        }


    @staticmethod
    def delete_document(
        db: Session,
        document_id: int,
        current_user
    ):

        document = (
            db.query(Document)
            .join(Workspace)
            .filter(
                Document.id == document_id,
                Workspace.user_id == current_user.id
            )
            .first()
        )

        if not document:
            raise HTTPException(
                status_code=404,
                detail="Document not found"
            )

        supabase.storage.from_("documents").remove(
            [document.file_path]
        )

        db.delete(document)

        db.commit()

        return {
            "message": "Document deleted successfully"
        }
    
    @staticmethod
    def get_recent_tool_logs(
        db: Session,
        workspace_id: int
    ):

        logs = (
            db.query(ToolLog)
            .filter(ToolLog.workspace_id == workspace_id)
            .order_by(ToolLog.id.desc())
            .limit(5)
            .all()
        )

        return {
            "success": True,
            "tool_logs": [
                {
                    "id": log.id,
                    "tool_name": log.tool_name,
                    "status": log.status,
                    "arguments": log.arguments,
                    "created_at": log.created_at
                }
                for log in logs
            ]
        }