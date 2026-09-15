import json
import re
import os
import google.generativeai as genai
from dotenv import load_dotenv
from app.services.gemini_service import GENERATION_CONFIG
from app.models.jd_schema import JDAnalysis
from app.prompts.jd_quality import JD_QUALITY_PROMPT

load_dotenv()


class JDService:
    def __init__(self):
        model_name = os.getenv("MODEL_NAME", "gemini-flash-lite-latest")
        self.model = genai.GenerativeModel(model_name)

    def _clean_json_response(self, raw_text: str) -> str:
        cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw_text.strip(), flags=re.MULTILINE)
        return cleaned.strip()

    def analyze(self, jd_text: str) -> JDAnalysis:
        schema_example = JDAnalysis(
            quality_score=0, improved_jd=""
        ).model_dump_json(indent=2)

        prompt = JD_QUALITY_PROMPT.format(schema=schema_example, jd_text=jd_text)
        response = self.model.generate_content(prompt, generation_config=GENERATION_CONFIG)
        cleaned = self._clean_json_response(response.text)

        data = json.loads(cleaned)
        return JDAnalysis(**data)