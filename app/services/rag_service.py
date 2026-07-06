from app.services.embedding_service import EmbeddingService
from app.services.vector_search_service import VectorSearchService
from app.services.prompt_service import PromptService
from app.services.chat_service import ChatService
from app.tools.note_tool import NoteTool
from app.services.chat_history_service import ChatHistoryService

class RagService:

    @staticmethod
    def ask(db, workspace_id, question):

        question_embedding = EmbeddingService.generate_embedding(question)

        chunks = VectorSearchService.search(
            db,
            workspace_id,
            question_embedding
        )

        prompt = PromptService.build(
            chunks,
            question
        )

        response = ChatService.ask(prompt)

        answer = response.text
        candidate = response.candidates[0]
        part = candidate.content.parts[0]

        if hasattr(part, "function_call") and part.function_call:

            tool_name = part.function_call.name
            args = dict(part.function_call.args)

            if tool_name == "save_note":

                result = NoteTool.save_note(
                    db=db,
                    title=args["title"],
                    user_id=1,
                    workspace_id=workspace_id
                )

            elif tool_name == "get_notes":

                result = NoteTool.get_notes(
                    db=db,
                    workspace_id=workspace_id
                )

            answer = ChatService.generate_final_response(
                question,
                result
            )

            ChatHistoryService.save_chat(
                db=db,
                workspace_id=workspace_id,
                user_message=question,
                assistant_message=answer
            )

            return {
                "answer": answer
            }

        ChatHistoryService.save_chat(
            db=db,
            workspace_id=workspace_id,
            user_message=question,
            assistant_message=answer
        )

        return {
            "answer": answer
        }