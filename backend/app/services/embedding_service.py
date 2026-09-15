import json
from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parents[3]  # project root
PARSED_JSON_DIR = BASE_DIR / "data" / "parsed_json"
VECTOR_DB_DIR = BASE_DIR / "vector_db"
VECTOR_DB_DIR.mkdir(parents=True, exist_ok=True)

COLLECTION_NAME = "resumes"


class EmbeddingService:
    def __init__(self):
        print("Loading embedding model (all-MiniLM-L6-v2)...")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        self.client = chromadb.PersistentClient(path=str(VECTOR_DB_DIR))
        self.collection = self.client.get_or_create_collection(name=COLLECTION_NAME)

    def resume_to_text(self, resume: dict) -> str:
        """Flatten a parsed resume JSON into a single text blob for embedding."""
        parts = []

        if resume.get("summary"):
            parts.append(f"Summary: {resume['summary']}")

        if resume.get("skills"):
            parts.append(f"Skills: {', '.join(resume['skills'])}")

        for exp in resume.get("experience", []):
            role = exp.get("role") or ""
            company = exp.get("company") or ""
            desc = exp.get("description") or ""
            parts.append(f"Experience: {role} at {company}. {desc}")

        for edu in resume.get("education", []):
            degree = edu.get("degree") or ""
            institution = edu.get("institution") or ""
            parts.append(f"Education: {degree}, {institution}")

        for proj in resume.get("projects", []):
            title = proj.get("title") or ""
            desc = proj.get("description") or ""
            parts.append(f"Project: {title}. {desc}")

        if resume.get("certifications"):
            parts.append(f"Certifications: {', '.join(resume['certifications'])}")

        if resume.get("total_years_experience"):
            parts.append(f"Total years experience: {resume['total_years_experience']}")

        return "\n".join(parts)

    def embed_all_resumes(self):
        json_paths = list(PARSED_JSON_DIR.glob("*.json"))
        print(f"Found {len(json_paths)} parsed resumes to embed.\n")

        ids, documents, metadatas = [], [], []

        for path in json_paths:
            with open(path, "r", encoding="utf-8") as f:
                resume = json.load(f)

            text = self.resume_to_text(resume)
            if not text.strip():
                print(f"Skipping {path.stem} — no usable text")
                continue

            ids.append(path.stem)
            documents.append(text)
            metadatas.append({
                "name": resume.get("name") or "Unknown",
                "source_file": path.stem,
                "total_years_experience": resume.get("total_years_experience") or 0.0,
            })

        # Embed in batch (much faster than one at a time)
        print("Generating embeddings...")
        embeddings = self.model.encode(documents, show_progress_bar=True).tolist()

        # Upsert into ChromaDB (safe to rerun — overwrites existing IDs)
        self.collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
        )

        print(f"\nEmbedded and stored {len(ids)} resumes in ChromaDB.")

    def search(self, query: str, top_k: int = 5):
        query_embedding = self.model.encode([query]).tolist()
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=top_k,
        )
        return results