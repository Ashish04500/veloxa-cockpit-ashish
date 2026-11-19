from pathlib import Path
import sys
import json

APP_DIR = Path(__file__).resolve().parent
BACKEND_DIR = APP_DIR.parent
ROOT = BACKEND_DIR.parent

sys.path.insert(0, str(APP_DIR))

from ingestion.file_reader import read_file

DAY4_FOLDER = (
    ROOT / "data" / "raw" / "Veloxa_Hackathon_Release_Packs" / "Day4_Thu_19Nov"
)
OUTPUT_FOLDER = ROOT / "data" / "processed"
OUTPUT_FILE = OUTPUT_FOLDER / "day4_documents.jsonl"


def ingest_day4():
    if not DAY4_FOLDER.exists():
        raise FileNotFoundError(f"Day 4 folder not found: {DAY4_FOLDER}")

    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

    files = sorted(path for path in DAY4_FOLDER.rglob("*") if path.is_file())

    if not files:
        raise SystemExit("No Day 4 files found.")

    temp_file = OUTPUT_FILE.with_suffix(".jsonl.tmp")
    successful = 0
    failed = 0

    try:
        with temp_file.open("w", encoding="utf-8") as output:
            for file_path in files:
                relative_path = file_path.relative_to(ROOT)
                print(f"Processing: {file_path.name}")

                try:
                    extracted_content = read_file(file_path)

                    record = {
                        "source_file": file_path.name,
                        "source_path": str(relative_path),
                        "release_day": "Day4",
                        "file_type": file_path.suffix.lower(),
                        "content": extracted_content,
                        "status": "success",
                    }

                    output.write(
                        json.dumps(record, ensure_ascii=False, default=str) + "\n"
                    )
                    successful += 1

                except Exception as error:
                    failed += 1
                    print("ERROR:", repr(error))

        if failed:
            raise SystemExit(
                f"Day 4 ingestion failed for {failed} file(s). "
                "Previous output was preserved."
            )

        temp_file.replace(OUTPUT_FILE)

    finally:
        if temp_file.exists():
            temp_file.unlink()

    print("\nDAY 4 INGESTION SUMMARY")
    print("Files found:", len(files))
    print("Successful:", successful)
    print("Failed:", failed)
    print("Output:", OUTPUT_FILE)

    return successful, failed


if __name__ == "__main__":
    ingest_day4()
