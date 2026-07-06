from sqlalchemy.orm import Session

from app.models.tool_log import ToolLog


class ToolLogService:

    @staticmethod
    def log(
            db: Session,
            workspace_id: int,
            tool_name: str,
            arguments: dict,
            result: dict
    ):

        log = ToolLog(
            workspace_id=workspace_id,
            tool_name=tool_name,
            arguments=arguments,
            result=result
        )

        db.add(log)
        db.commit()

        return log