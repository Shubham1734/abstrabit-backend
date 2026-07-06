from google.genai import types
from app.services.tool_log_service import ToolLogService
TOOLS = [
    types.Tool(
        function_declarations=[
            types.FunctionDeclaration(
                name="save_note",
                description="Save a note",
                parameters={
                    "type": "OBJECT",
                    "properties": {
                        "title": {
                            "type": "STRING"
                        }
                    },
                    "required": ["title"]
                }
            ),
            types.FunctionDeclaration(
                name="get_notes",
                description="Retrieve all notes",
                parameters={
                    "type": "OBJECT",
                    "properties": {}
                }
            )
        ]
    )
]