import json
from pathlib import Path
from datetime import datetime
from app.services.gemini_service import GeminiService

# backend/app/services/ -> up 3 levels -> project root
BASE_DIR = Path(__file__).resolve().parents[3]
PARSED_JSON_DIR = BASE_DIR / "data" / "parsed_json"
PARSED_JSON_DIR.mkdir(parents=True, exist_ok=True)


def parse_and_save_resume(pdf_path: Path, resume_text: str, gemini_service: GeminiService) -> dict:
    parsed = gemini_service.extract_resume(resume_text)

    output_path = PARSED_JSON_DIR / f"{pdf_path.stem}.json"
    output_data = parsed.model_dump()
    output_data["_source_pdf"] = str(pdf_path)
    output_data["_raw_text"] = resume_text
    output_data["_parsed_at"] = datetime.now().isoformat()

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    return output_data, output_path