from app.services.embedding_service import EmbeddingService


def main():
    service = EmbeddingService()
    service.embed_all_resumes()


if __name__ == "__main__":
    main()