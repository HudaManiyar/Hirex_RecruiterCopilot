import json
import re
import os
import google.generativeai as genai
from dotenv import load_dotenv
from app.services.embedding_service import EmbeddingService
from app.services.gemini_service import GENERATION_CONFIG
from app.models.ranking_schema import RankingResponse
from app.prompts.explainable_ranking import EXPLAINABLE_RANKING_PROMPT

load_dotenv()


class RankingService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        model_name = os.getenv("MODEL_NAME", "gemini-flash-lite-latest")
        self.model = genai.GenerativeModel(model_name)

    def _clean_json_response(self, raw_text: str) -> str:
        cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw_text.strip(), flags=re.MULTILINE)
        return cleaned.strip()

    def _format_candidates_block(self, results) -> str:
        blocks = []
        for doc_id, doc, meta in zip(
            results["ids"][0], results["documents"][0], results["metadatas"][0]
        ):
            name = meta.get("name") or f"Candidate {doc_id}"
            blocks.append(f"--- Candidate: {name} (source_file: {doc_id}) ---\n{doc}\n")
        return "\n".join(blocks)

    def rank(self, job_requirement: str, top_k: int = 5) -> RankingResponse:
        results = self.embedding_service.search(job_requirement, top_k=top_k)
        candidates_block = self._format_candidates_block(results)

        # Build a name -> source_file lookup from the retrieval results
        name_to_source = {}
        for doc_id, meta in zip(results["ids"][0], results["metadatas"][0]):
            name = meta.get("name") or f"Candidate {doc_id}"
            name_to_source[name] = doc_id

        schema_example = RankingResponse(evaluations=[]).model_dump_json(indent=2)

        prompt = EXPLAINABLE_RANKING_PROMPT.format(
            schema=schema_example,
            job_requirement=job_requirement,
            candidates_block=candidates_block,
        )

        response = self.model.generate_content(prompt, generation_config=GENERATION_CONFIG)
        cleaned = self._clean_json_response(response.text)

        data = json.loads(cleaned)

        # Inject source_file by matching candidate_name back to the retrieval results
        for ev in data.get("evaluations", []):
            matched_source = name_to_source.get(ev.get("candidate_name"))
            ev["source_file"] = matched_source if matched_source else "unknown"

        return RankingResponse(**data)