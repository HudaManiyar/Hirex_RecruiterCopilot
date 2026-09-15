from pathlib import Path
import time
import fitz
from app.services.gemini_service import GeminiService
from app.services.parser_service import parse_and_save_resume, PARSED_JSON_DIR


def extract_text_from_pdf(pdf_path: Path) -> str:
    doc = fitz.open(pdf_path)
    text = "\n".join(page.get_text() for page in doc)
    doc.close()
    return text


def main():
    gemini_service = GeminiService()

    BASE_DIR = Path(__file__).resolve().parent      # backend/
    PROJECT_ROOT = BASE_DIR.parent                   # Recruitement_Copilot/
    pdf_dir = PROJECT_ROOT / "data" / "resumes" / "raw_data"

    print(f"Looking in: {pdf_dir}")
    pdf_paths = list(pdf_dir.rglob("*.pdf"))
    total = len(pdf_paths)
    print(f"Found {total} PDF(s).\n")

    if not pdf_paths:
        print("No PDFs found. Check the folder path.")
        return

    succeeded = 0
    skipped = 0
    failed = 0

    for i, pdf_path in enumerate(pdf_paths, start=1):
        output_path = PARSED_JSON_DIR / f"{pdf_path.stem}.json"
        if output_path.exists():
            print(f"[{i}/{total}] Skipping (already processed): {pdf_path.name}")
            skipped += 1
            continue

        print(f"[{i}/{total}] Processing: {pdf_path.name}")
        try:
            text = extract_text_from_pdf(pdf_path)
            if not text.strip():
                print("  Skipped (No extractable text)\n")
                skipped += 1
                continue
            result, saved_path = parse_and_save_resume(pdf_path, text, gemini_service)
            print(f"  Saved JSON for: {result.get('name', 'UNKNOWN')} -> {saved_path}\n")
            succeeded += 1
        except Exception as e:
            print(f"  FAILED: {e}\n")
            failed += 1

        time.sleep(2)

    print("=" * 60)
    print(f"Done. Succeeded: {succeeded} | Skipped: {skipped} | Failed: {failed} | Total: {total}")
    print("=" * 60)


if __name__ == "__main__":
    main()