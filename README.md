
# Veloxa — Evidence-Grounded CEO Cockpit

An executive decision-support cockpit that consolidates company information, highlights business risks and presents evidence-backed insights with confidence levels and explicit uncertainty.

Built for the Veloxa CXO Cockpit Hackathon, November 2026.

## Problem

Company information is distributed across HR records, finance exports, engineering updates, emails, board reports and meeting transcripts.

The cockpit aims to help the CEO:
- Understand the most important business risks.
- Review supporting evidence and source citations.
- Ask questions about company operations.
- Distinguish verified facts from assumptions.
- Identify missing, conflicting or insufficient evidence.

## Current Implementation

### Backend
- FastAPI application with health-check and risk-summary endpoints.
- Document ingestion for PDF, DOCX, XLSX, CSV, TXT and EML.
- Day 1 through Day 4 release-pack ingestion.
- JSONL-based processed document storage.
- Evidence retrieval with source references and citations.
- Profiles for 14 employees with available, evidence-backed context.
- Provisional risk-ranking engine.
- Topic-specific CEO question-answering with confidence and evidence.
- Privacy safeguards for individual salary data, private survey comments and unnamed employees.
- Insufficient-evidence responses for unsupported questions.

### Frontend
- React application built with Vite.
- Automatically loads the top three business risks on dashboard opening.
- Displays risk priority, impact, confidence and heuristic score.
- Shows recommended actions and uncertainty.
- Expandable evidence sections with source citations.
- Refresh control, API connection status and error handling.

### Current Risk Categories
1. Engineering capacity and delivery.
2. Funding and runway.
3. Marketing continuity and knowledge transfer.

Risk rankings are provisional and based on a transparent heuristic. Scores are not statistical probabilities.

## Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React, Vite, JavaScript, CSS |
| Backend | Python, FastAPI |
| Data processing | OpenPyXL, python-docx, pypdf |
| API server | Uvicorn |
| Testing | pytest |
| Frontend validation | ESLint, Vite production build |
| Evidence storage | JSONL |
| Version control | Git, GitHub |

## Project Structure

```text
veloxa-cockpit-ashish/
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   ├── cockpit/
│   │   ├── database/
│   │   ├── ingestion/
│   │   └── rag/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
├── tests/
├── data/
│   ├── raw/
│   └── processed/
├── ARCHITECTURE.md
├── ASSUMPTIONS.md
├── TRANSCRIPT_NOTES.md
├── DECISIONS.md
├── AI_LOG.md
├── CEO_VOICE_NOTE_RESPONSES.md
└── README.md
```

## Local Setup

Requirements:
- Python 3.10 or later.
- Node.js 20.19+ or 22.12+.
- npm.

### 1. Clone the repository

```powershell
git clone https://github.com/Ashish04500/veloxa-cockpit-ashish.git
cd veloxa-cockpit-ashish
```

### 2. Install backend dependencies

```powershell
python -m venv backend/venv
backend/venv/Scripts/python.exe -m pip install -r backend/requirements.txt
```

### 3. Install frontend dependencies

```powershell
cd frontend
npm.cmd install
cd ..
```

### 4. Add the hackathon release data

Extract the supplied release packs into:

```text
data/raw/Veloxa_Hackathon_Release_Packs/
```

Do not commit private source data or processed records.

### 5. Start the backend

From the project root:

```powershell
backend/venv/Scripts/python.exe -m uvicorn app.main:app --app-dir backend --reload
```

Backend:
`http://127.0.0.1:8000`

API documentation:
`http://127.0.0.1:8000/docs`

### 6. Start the frontend

Open another terminal from the project root:

```powershell
cd frontend
npm.cmd run dev
```

Frontend:
`http://localhost:5173`

The Vite development server proxies `/api` requests to the backend.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Backend health check |
| GET | `/api/risks` | Retrieve the top three ranked risks |
| POST | `/api/ask` | Ask an evidence-backed CEO question |

## Testing

Run the backend test suite from the project root:

```powershell
backend/venv/Scripts/python.exe -m pytest -q
```

Latest verified backend result: **81 tests passed**, with one non-blocking Starlette deprecation warning.

Run frontend checks from the `frontend` directory:

```powershell
npm.cmd run lint
npm.cmd run build
```

Both checks have passed.

## Evidence and Privacy Principles

- Preserve original source filenames and citations.
- Prefer formal records over unreliable machine-generated transcripts when sources conflict.
- Do not silently resolve conflicting information.
- Separate verified facts from assumptions and inferences.
- Communicate confidence, uncertainty and missing evidence.
- Do not expose private individual survey comments or unsupported employee identities.
- Treat heuristic risk scores as prioritisation aids, not probabilities.

## Known Limitations

- CEO question answering currently uses deterministic, topic-specific logic rather than a general-purpose LLM.
- Risk scores use manually assigned urgency and a rough evidence-strength measure.
- Historical point-in-time filtering is not fully implemented.
- Comprehensive role-based access control is not implemented.
- Employee profiles contain only context supported by available evidence; they are not fully autonomous AI agents.
- API connection status reflects the latest request rather than continuous monitoring.

## Documentation

- `ARCHITECTURE.md` — System architecture.
- `ASSUMPTIONS.md` — Assumptions and confidence.
- `TRANSCRIPT_NOTES.md` — Transcript discrepancies and source reconciliation.
- `DECISIONS.md` — Technical and product decisions.
- `AI_LOG.md` — AI assistance and human verification.
- `CEO_VOICE_NOTE_RESPONSES.md` — Written responses to CEO voice notes.

### Recommended startup
Run both services from the repository root:

`powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\run.ps1`

The script creates the Python environment and installs dependencies when needed, ingests Day 1 to Day 4 data when processed files are missing, and starts the backend and frontend.

Useful options:
- `-Reingest`: re-ingest all four release packs.
- `-InstallDependencies`: reinstall backend and frontend dependencies.

The script writes service output and error logs to `logs/`.
