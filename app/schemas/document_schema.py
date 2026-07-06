class UploadResponse(BaseModel):

    message:str

    document_id:int

    from datetime import datetime
from pydantic import BaseModel


class DocumentResponse(BaseModel):

    id: int

    file_name: str

    storage_path: str

    uploaded_at: datetime

    class Config:
        from_attributes = True