from app.utils.gemini_client import client


class EmbeddingService:

    @staticmethod
    def generate_embedding(text: str):

        response = client.models.embed_content(
            model="gemini-embedding-001",
            contents=text
        )

        return response.embeddings[0].values