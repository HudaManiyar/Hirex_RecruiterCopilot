import json
from collections import Counter
from pathlib import Path

import chromadb

from app.services.embedding_service import COLLECTION_NAME, PARSED_JSON_DIR, VECTOR_DB_DIR


class StatsService:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=str(VECTOR_DB_DIR))
        self.collection = self.client.get_or_create_collection(name=COLLECTION_NAME)

    def _category_for(self, resume_id: str) -> tuple[str | None, bool]:
        """Returns (category, is_real) for a resume by inspecting the _source_pdf path
        recorded in its parsed JSON. Real resumes live under raw_data/{category}/...;
        synthetic ones live under evaluation/synthetic_resumes/ and have no category."""
        path = PARSED_JSON_DIR / f"{resume_id}.json"
        if not path.exists():
            return None, True

        with open(path, "r", encoding="utf-8") as f:
            resume = json.load(f)

        parts = Path(resume.get("_source_pdf") or "").parts
        if "raw_data" not in parts:
            return None, False

        idx = parts.index("raw_data")
        if idx + 1 >= len(parts):
            return None, True

        category = parts[idx + 1].replace("_", " ")
        return category, True

    def get_stats(self) -> dict:
        ids = self.collection.get(include=[])["ids"]

        category_counts: Counter = Counter()
        real_count = 0
        synthetic_count = 0

        for resume_id in ids:
            category, is_real = self._category_for(resume_id)
            if is_real:
                real_count += 1
                if category:
                    category_counts[category] += 1
            else:
                synthetic_count += 1

        categories = [
            {"category": category, "count": count}
            for category, count in sorted(category_counts.items(), key=lambda kv: kv[1], reverse=True)
        ]

        return {
            "total_resumes": len(ids),
            "categories": categories,
            "source_breakdown": {"real": real_count, "synthetic": synthetic_count},
        }
