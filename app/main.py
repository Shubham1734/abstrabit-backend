from fastapi import FastAPI

from app.database import Base, engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Models
from app.models.user import User
from app.models.workspace import Workspace
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.models.note import Note
from app.models.chat_history import ChatHistory
from app.models.tool_log import ToolLog

# Routers
from app.routers.auth_router import router as auth_router
from app.routers.workspace_router import router as workspace_router
from app.routers.document_router import router as document_router
from app.routers.chat_router import router as chat_router
from app.routers.dashboard_router import router as dashboard_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(workspace_router)
app.include_router(document_router)
app.include_router(chat_router)
app.include_router(dashboard_router)

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Backend Running"}




