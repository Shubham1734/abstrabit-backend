class PromptService:

    @staticmethod
    def build(contexts, question):

        context = "\n\n".join(
            row.chunk_text
            for row in contexts
        )

        return f"""
You are an AI assistant.

Answer ONLY using the context below.

If the answer is not present, reply:
"I couldn't find that information in the uploaded documents."

Context:
{context}

Question:
{question}
"""