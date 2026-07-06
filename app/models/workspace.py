from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base

from sqlalchemy.orm import relationship
class Workspace(Base):

    __tablename__ = "workspaces"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    owner = relationship(
    "User",
    back_populates="workspaces"
    )

    documents = relationship(
    "Document",
    back_populates="workspace",
    cascade="all, delete-orphan"
    )