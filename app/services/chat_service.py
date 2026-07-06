from app.utils.gemini_client import client
from app.tools.tool_definition import TOOLS
import json

class ChatService:

    @staticmethod
    def ask(prompt):

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={
                "tools": TOOLS
            }
        )

        return response

    @staticmethod
    def generate_final_response(
        user_prompt: str,
        tool_result
    ):

        prompt = f"""
    User Request:
    {user_prompt}

    Tool Output:
    {json.dumps(tool_result, indent=2)}

    Respond naturally to the user.
    Do not return JSON.
    """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text