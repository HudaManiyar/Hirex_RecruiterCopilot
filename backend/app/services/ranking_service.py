from app.services.embedding_service import EmbeddingService
from app.services.llm import generate_json
from app.models.ranking_schema import CandidateEvaluation, RankingResponse
from app.prompts.explainable_ranking import EXPLAINABLE_RANKING_PROMPT


class RankingService:
    def __init__(self):
        self.embedding_service = EmbeddingService()

    def _format_candidates_block(self, results) -> str:
        blocks = []
        for doc_id, doc, meta in zip(
            results["ids"][0], results["documents"][0], results["metadatas"][0]
        ):
            name = meta.get("name") or f"Candidate {doc_id}"
            blocks.append(f"--- Candidate: {name} (source_file: {doc_id}) ---\n{doc}\n")
        return "\n".join(blocks)

    def _attach_source_files(self, response: RankingResponse, results) -> RankingResponse:
        """Make sure every evaluation points to a file that was actually retrieved.

        The model is asked to copy each candidate's source_file ID. If it returns
        an ID that wasn't retrieved, fall back to matching the candidate name.
        """
        retrieved_ids = set(results["ids"][0])
        name_to_source = {
            (meta.get("name") or f"Candidate {doc_id}"): doc_id
            for doc_id, meta in zip(results["ids"][0], results["metadatas"][0])
        }
        for ev in response.evaluations:
            if ev.source_file not in retrieved_ids:
                ev.source_file = name_to_source.get(ev.candidate_name, "unknown")
        return response

    def rank(self, job_requirement: str, top_k: int = 5) -> RankingResponse:
        results = self.embedding_service.search(job_requirement, top_k=top_k)
        candidates_block = self._format_candidates_block(results)

        # One filled-in example so the model sees every field it must return
        schema_example = RankingResponse(evaluations=[
            CandidateEvaluation(
                candidate_name="<name from the candidate header>",
                source_file="<source_file ID from the candidate header>",
                grade="A|B|C|D",
                reasoning="...",
                confidence="High|Medium|Low",
            )
        ]).model_dump_json(indent=2)

        prompt = EXPLAINABLE_RANKING_PROMPT.format(
            schema=schema_example,
            job_requirement=job_requirement,
            candidates_block=candidates_block,
        )

        response = generate_json(prompt, RankingResponse)
        return self._attach_source_files(response, results)
