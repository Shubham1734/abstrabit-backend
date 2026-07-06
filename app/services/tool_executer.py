from sqlalchemy.orm import Session

from app.services.task_service import TaskService
from app.services.tool_log_service import ToolLogService

class ToolExecutor:

    @staticmethod
    def execute(
            db: Session,
            workspace_id: int,
            tool_name: str,
            arguments: dict
    ):

        if tool_name == "save_task":

            task = TaskService.create_task(
                db=db,
                workspace_id=workspace_id,
                title=arguments["title"]
            )

            result = {
                "success": True,
                "task_id": task.id,
                "message": "Task saved successfully"
            }

            ToolLogService.log(
                db=db,
                workspace_id=workspace_id,
                tool_name=tool_name,
                arguments=arguments,
                result=result
            )

            return result

        raise Exception(f"Unknown tool: {tool_name}")