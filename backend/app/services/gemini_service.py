import os
import json
import re
import time
import google.generativeai as genai
from dotenv import load_dotenv
from app.models.resume_schema import ResumeSchema
from app.prompts.resume_extraction import RESUME_EXTRACTION_PROMPT

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

GENERATION_CONFIG = {
    "temperature": 0,
    "top_p": 0.95,
    "max_output_tokens": 4096,
}


class GeminiService:
    def __init__(self, model_name: str = None):
        resolved_model = model_name or os.getenv("MODEL_NAME", "gemini-2.5-flash")
        print(f"Using Gemini model: {resolved_model}")
        self.model = genai.GenerativeModel(resolved_model)

    def _clean_json_response(self, raw_text: str) -> str:
        cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw_text.strip(), flags=re.MULTILINE)
        return cleaned.strip()

    def _is_rate_limit_error(self, e: Exception) -> bool:
        msg = str(e).lower()
        return "429" in msg or "resource_exhausted" in msg or "quota" in msg

    def extract_resume(self, resume_text: str, max_retries: int = 3) -> ResumeSchema:
        schema_example = ResumeSchema().model_dump_json(indent=2)
        prompt = RESUME_EXTRACTION_PROMPT.format(
            schema=schema_example,
            resume_text=resume_text[:15000]
        )

        last_error = None

        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(
                    prompt,
                    generation_config=GENERATION_CONFIG,
                )

                if not response.text:
                    raise ValueError("Empty Gemini response")

                raw_text = response.text
                cleaned = self._clean_json_response(raw_text)

                try:
                    data = json.loads(cleaned)
                except json.JSONDecodeError as e:
                    raise ValueError(f"Gemini did not return valid JSON: {e}\nRaw output: {raw_text}")

                return ResumeSchema(**data)

            except Exception as e:
                last_error = e

                if self._is_rate_limit_error(e) and attempt < max_retries - 1:
                    wait = 15 * (attempt + 1)
                    print(f"    Rate limited, waiting {wait}s before retry ({attempt + 1}/{max_retries})...")
                    time.sleep(wait)
                    continue
                else:
                    break

        raise last_error