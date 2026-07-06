from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from app.database import Base


class ToolLog(Base):

    __tablename__ = "tool_logs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    workspace_id = Column(
        Integer,
        ForeignKey("workspaces.id"),
        nullable=False
    )

    tool_name = Column(
        Text,
        nullable=False
    )

    arguments = Column(
        JSONB
    )

    result = Column(
        JSONB
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )