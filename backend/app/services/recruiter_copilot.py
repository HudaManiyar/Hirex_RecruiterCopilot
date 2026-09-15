from app.services.embedding_service import EmbeddingService
from app.services.gemini_service import GeminiService
from app.prompts.recruiter_query import RECRUITER_QUERY_PROMPT


class RecruiterCopilot:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.gemini_service = GeminiService()

    def _format_candidates_block(self, results) -> str:
        blocks = []
        ids = results["ids"][0]
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]

        for doc_id, doc, meta in zip(ids, documents, metadatas):
            name = meta.get("name") or "Unknown"
            blocks.append(f"--- Candidate: {name} (source: {doc_id}) ---\n{doc}\n")

        return "\n".join(blocks)

    def query(self, recruiter_query: str, top_k: int = 5) -> str:
        results = self.embedding_service.search(recruiter_query, top_k=top_k)
        candidates_block = self._format_candidates_block(results)

        prompt = RECRUITER_QUERY_PROMPT.format(
            query=recruiter_query,
            candidates_block=candidates_block,
        )

        response = self.gemini_service.model.generate_content(prompt)
        return response.text