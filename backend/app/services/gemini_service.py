from app.models.resume_schema import ResumeSchema
from app.prompts.resume_extraction import RESUME_EXTRACTION_PROMPT
from app.services.llm import MODEL_NAME, generate_json


class GeminiService:
    def __init__(self):
        print(f"Using Gemini model: {MODEL_NAME}")

    def extract_resume(self, resume_text: str, max_retries: int = 3) -> ResumeSchema:
        schema_example = ResumeSchema().model_dump_json(indent=2)
        prompt = RESUME_EXTRACTION_PROMPT.format(
            schema=schema_example,
            resume_text=resume_text[:15000]
        )
        return generate_json(prompt, ResumeSchema, max_retries=max_retries)
