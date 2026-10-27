from app.models.jd_schema import JDAnalysis
from app.prompts.jd_quality import JD_QUALITY_PROMPT
from app.services.llm import generate_json


class JDService:
    def analyze(self, jd_text: str) -> JDAnalysis:
        schema_example = JDAnalysis(
            quality_score=0, improved_jd=""
        ).model_dump_json(indent=2)

        prompt = JD_QUALITY_PROMPT.format(schema=schema_example, jd_text=jd_text)
        return generate_json(prompt, JDAnalysis)
