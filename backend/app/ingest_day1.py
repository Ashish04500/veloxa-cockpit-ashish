
from pathlib import Path
import sys
import json

# Make the app folder available for imports
APP_DIR = Path(__file__).resolve().parent
BACKEND_DIR = APP_DIR.parent
ROOT = BACKEND_DIR.parent

sys.path.insert(0, str(APP_DIR))

from ingestion.file_reader import read_file


DAY1_FOLDER = (
    ROOT
    / "data"
    / "raw"
    / "Veloxa_Hackathon_Release_Packs"
    / "Day1_Mon_16Nov"
)

OUTPUT_FOLDER = ROOT / "data" / "processed"
OUTPUT_FILE = OUTPUT_FOLDER / "day1_documents.jsonl"


def ingest_day1():
    if not DAY1_FOLDER.exists():
        raise FileNotFoundError(
            f"Day 1 folder not found: {DAY1_FOLDER}"
        )

    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

    files = sorted(
        path for path in DAY1_FOLDER.rglob("*")
        if path.is_file()
    )

    successful = 0
    failed = 0

    with open(OUTPUT_FILE, "w", encoding="utf-8") as output:
        for file_path in files:
            relative_path = file_path.relative_to(ROOT)

            print(f"Processing: {file_path.name}")

            try:
                extracted_content = read_file(file_path)

                record = {
                    "source_file": file_path.name,
                    "source_path": str(relative_path),
                    "release_day": "Day1",
                    "file_type": file_path.suffix.lower(),
                    "content": extracted_content,
                    "status": "success"
                }

                output.write(
                    json.dumps(record, ensure_ascii=False, default=str)
                    + "\n"
                )

                successful += 1

            except Exception as error:
                record = {
                    "source_file": file_path.name,
                    "source_path": str(relative_path),
                    "release_day": "Day1",
                    "status": "failed",
                    "error": repr(error)
                }

                output.write(
                    json.dumps(record, ensure_ascii=False)
                    + "\n"
                )

                failed += 1
                print("ERROR:", repr(error))

    print("\n" + "=" * 55)
    print("DAY 1 INGESTION SUMMARY")
    print("=" * 55)
    print("Total files:", len(files))
    print("Successfully ingested:", successful)
    print("Failed:", failed)
    print("Output:", OUTPUT_FILE)

    return successful, failed


if __name__ == "__main__":
    ingest_day1()
