from sqlalchemy import text


class VectorSearchService:

    @staticmethod
    def search(db, workspace_id, embedding, limit=5):

        sql = text("""
            SELECT
                id,
                chunk_text
            FROM document_chunks
            WHERE workspace_id = :workspace_id
            ORDER BY embedding <=> CAST(:embedding AS vector)
            LIMIT :limit
        """)

        result = db.execute(
            sql,
            {
                "workspace_id": workspace_id,
                "embedding": str(embedding),
                "limit": limit
            }
        )

        # Convert SQLAlchemy Row objects to dictionaries
        return result.mappings().all()