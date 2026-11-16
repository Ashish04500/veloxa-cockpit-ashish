# Veloxa — AI-Powered CEO Cockpit

An evidence-grounded AI cockpit designed to help the CEO of Veloxa Technologies understand company operations, employee context, business risks and important decisions through a unified interface.

## Problem Statement

Company information is spread across HR records, finance exports, engineering updates, emails, board reports and meeting transcripts.

The goal is to build a system that brings these sources together and allows the CEO to ask questions, understand operational risks and receive answers backed by traceable evidence.

The system must distinguish verified facts from assumptions, identify conflicting information and clearly communicate uncertainty.

## Current Development Status

### Implemented
- Initial project structure.
- File readers for XLSX, DOCX, PDF, CSV, TXT and EML.
- Day 1 ingestion pipeline covering 15 source files.
- JSONL-based extracted document storage.
- Initial profiles for 14 employees across four departments.
- Initial source analysis and discrepancy documentation.
- 10 automated tests passing.

### In Progress
- Evidence retrieval and citation support.
- Employee agent behaviour and work context.
- CEO question-answering functionality.
- Risk identification and ranking.
- Integration of Day 2, Day 3 and Day 4 release packs.

## Technology Stack

**Backend:** Python, FastAPI

**Data Processing:** OpenPyXL, python-docx, pypdf, Python CSV

**Testing:** pytest

**Frontend:** To be finalised.

**AI and Retrieval:** To be finalised based on implementation and evaluation.

## Project Structure

```text
veloxa-cockpit-ashish/
│
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   ├── cockpit/
│   │   ├── database/
│   │   ├── ingestion/
│   │   └── rag/
│   └── requirements.txt
│
├── frontend/
├── data/
│   ├── raw/
│   └── processed/
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── ASSUMPTIONS.md
│   ├── DECISIONS.md
│   ├── TRANSCRIPT_NOTES.md
│   └── AI_LOG.md
│
├── tests/
├── README.md
└── .gitignore
```

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/Ashish04500/veloxa-cockpit-ashish.git
cd veloxa-cockpit-ashish
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv backend/venv
backend/venv/Scripts/Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r backend/requirements.txt
```

### 4. Add the hackathon release files

Extract the provided release packs into:

```text
data/raw/Veloxa_Hackathon_Release_Packs/
```

### 5. Run Day 1 ingestion

```powershell
cd backend
python app/ingest_day1.py
```

### 6. Run automated tests

```powershell
python -m pytest ../tests -v
```

## Evidence and Reliability Principles

- Preserve source filenames and traceability.
- Prefer formal exports and records over unreliable machine-generated transcripts when sources conflict.
- Do not silently correct conflicting information.
- Separate verified facts, inferences and assumptions.
- Include confidence and unknowns in decision-support answers.
- Protect confidential employee and payroll information.

## Documentation

- `ARCHITECTURE.md` — System architecture and design.
- `ASSUMPTIONS.md` — Assumptions, evidence and confidence.
- `TRANSCRIPT_NOTES.md` — Transcript discrepancies and source reconciliation.
- `DECISIONS.md` — Technical decisions and trade-offs.
- `AI_LOG.md` — AI assistance and human verification record.

## Testing

Run:

```powershell
python -m pytest tests -v
```

Initial Day 1 validation: **10 tests passing**.

The project is under active development as part of the Veloxa CXO Cockpit Hackathon, November 2026.