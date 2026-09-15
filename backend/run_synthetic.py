from pathlib import Path
import time
from app.services.gemini_service import GeminiService
from app.services.parser_service import parse_and_save_resume, PARSED_JSON_DIR


def process_txt_resumes(txt_dir: Path, gemini_service):
    txt_paths = list(txt_dir.glob("*.txt"))
    total = len(txt_paths)
    print(f"Found {total} synthetic resume(s).\n")

    succeeded = 0
    skipped = 0
    failed = 0

    for i, txt_path in enumerate(txt_paths, start=1):
        output_path = PARSED_JSON_DIR / f"{txt_path.stem}.json"
        if output_path.exists():
            print(f"[{i}/{total}] Skipping (already processed): {txt_path.name}")
            skipped += 1
            continue

        print(f"[{i}/{total}] Processing: {txt_path.name}")
        try:
            text = txt_path.read_text(encoding="utf-8")
            result, saved_path = parse_and_save_resume(txt_path, text, gemini_service)
            print(f"  Saved JSON for: {result.get('name', 'UNKNOWN')} -> {saved_path}\n")
            succeeded += 1
        except Exception as e:
            print(f"  FAILED: {e}\n")
            failed += 1

        time.sleep(2)

    print("=" * 60)
    print(f"Done. Succeeded: {succeeded} | Skipped: {skipped} | Failed: {failed} | Total: {total}")
    print("=" * 60)


def main():
    gemini_service = GeminiService()
    BASE_DIR = Path(__file__).resolve().parent       # backend/
    PROJECT_ROOT = BASE_DIR.parent                     # Recruitement_Copilot/
    synthetic_dir = PROJECT_ROOT / "data" / "evaluation" / "synthetic_resumes"

    if not synthetic_dir.exists():
        print(f"Folder not found: {synthetic_dir}")
        print("Create it and save your 20 synthetic_XX.txt files there first.")
        return

    process_txt_resumes(synthetic_dir, gemini_service)


if __name__ == "__main__":
    main()