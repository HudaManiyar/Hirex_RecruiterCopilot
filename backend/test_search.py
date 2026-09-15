from app.services.embedding_service import EmbeddingService

service = EmbeddingService()
results = service.search("Python developer with SQL experience", top_k=5)

for i, (doc_id, doc, meta) in enumerate(zip(
    results["ids"][0], results["documents"][0], results["metadatas"][0]
), start=1):
    print(f"\n[{i}] {meta['name']} ({doc_id})")
    print(doc[:200], "...")