from google.genai import types

tools = [
    types.Tool(
        function_declarations=[
            types.FunctionDeclaration(
                name="save_task",
                description="Save a reminder or task for the current workspace.",
                parameters={
                    "type": "OBJECT",
                    "properties": {
                        "title": {
                            "type": "STRING",
                            "description": "Task title"
                        }
                    },
                    "required": ["title"]
                }
            )
        ]
    )
]