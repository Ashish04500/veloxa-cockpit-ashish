# Veloxa CXO Cockpit — Architecture

## 1. Objective

Veloxa CXO Cockpit is an evidence-grounded executive dashboard for Veloxa Technologies.

It allows the CEO to:
- View prioritized business risks.
- Ask questions about company operations.
- Receive answers supported by source evidence.
- Inspect evidence references and source excerpts.
- Identify uncertainty and distinguish documented facts from unverified claims.

The system prioritizes evidence traceability, privacy safeguards, explainability, and reliable handling of incomplete information.

The current implementation is a working evidence-grounded CEO cockpit. It does not yet implement 14 independently conversational AI employee agents.

## 2. Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| Frontend | React, Vite, CSS | Executive dashboard and CEO Q&A interface |
| Backend | Python, FastAPI | API endpoints and application logic |
| Data extraction | OpenPyXL, python-docx, pypdf, Python CSV | Extract content from source documents |
| Document storage | JSONL | Store extracted documents |
| Evidence store | Python-based normalized evidence records | Preserve source metadata and searchable text |
| Retrieval | Custom keyword-based retrieval | Find relevant evidence using tokens, synonyms, source weights and filters |
| Answer engine | Python rule-based logic | Identify supported topics, apply safeguards and construct grounded answers |
| Risk engine | Python heuristic scoring | Prioritize evidence-supported business risks |
| Testing | Pytest | Validate ingestion, retrieval, API, privacy and risk behaviour |

OpenPyXL is used for Excel extraction rather than Pandas because of a Windows Application Control restriction affecting NumPy compiled DLL imports in the development environment.

### 2.1 Current Implementation Status

| Component | Status |
|---|---|
| Project structure | Implemented |
| Day 1–Day 4 ingestion | Implemented |
| Excel, DOCX, PDF, CSV, TXT and EML extraction | Implemented |
| JSONL document storage | Implemented |
| Normalized evidence store | Implemented |
| 14 employee identity profiles | Implemented |
| Keyword-based evidence retrieval | Implemented |
| Source and release-day filtering | Implemented |
| CEO Q&A for supported topics | Implemented |
| Question-level privacy safeguards | Implemented |
| Evidence citations and excerpts | Implemented |
| Heuristic business risk ranking | Implemented |
| React CEO dashboard | Implemented |
| Automated test suite | Implemented |
| Conversational employee-agent runtime | Planned |
| LLM-based answer generation | Planned |
| SQLite database and FTS5 | Planned |
| Vector search and semantic retrieval | Planned |
| Role-based authorization | Planned |

## 3. High-Level Architecture

```text
          Release Packs (Day 1–Day 4)
                       |
                       v
                Ingestion Layer
                       |
                       v
             File Extraction Layer
                       |
                       v
               JSONL Documents
                       |
                       v
               Evidence Store
                       |
             +---------+---------+
             |                   |
             v                   v
       Evidence Retrieval    Risk Engine
             |                   |
             v                   |
        CEO Answer Engine <------+
             |
             v
          FastAPI
             |
             v
        React Dashboard
```

The current application uses a shared evidence store for Q&A and risk analysis.

The diagram represents the implemented application flow. Conversational employee agents, vector databases and LLM orchestration are not part of the current runtime.

## 4. Data Ingestion

The ingestion layer processes source files released in four daily release packs.

| Release | Documents processed |
|---|---:|
| Day 1 | 15 |
| Day 2 | 10 |
| Day 3 | 14 |
| Day 4 | 2 |
| **Total** | **41** |

The current ingestion pipeline supports:

- Excel workbooks through OpenPyXL.
- Word documents through python-docx.
- PDF documents through pypdf.
- CSV files through Python's built-in CSV module.
- TXT and EML files through built-in file reading.

Extracted documents are stored in:

`data/processed/`

Each JSONL record preserves:
- Source filename.
- Relative source path.
- File type.
- Release day.
- Extracted content.
- Ingestion status.

The Day 4 ingestion script processes the newly released files and writes its output atomically using a temporary file before replacing the processed JSONL output.

The original source files remain unchanged.

### 4.1 Evidence Store

The evidence store loads all successfully processed JSONL documents and normalizes their content into evidence records.

The latest verified local dataset contains:

- 41 processed documents.
- 339 normalized evidence records.
- 2 evidence records originating from Day 4.

Each evidence record includes source metadata, release day, file type, locator, status, and extracted text.

The evidence store is currently loaded through Python application logic. A persistent relational database has not yet been implemented.

## 5. Evidence Retrieval

The current retrieval engine uses keyword-based matching rather than embedding-based semantic search.

Its retrieval process includes:

1. Tokenizing the CEO's question.
2. Expanding selected terms using configured synonyms.
3. Matching query terms against evidence text.
4. Applying source weighting.
5. Applying a recency bonus where relevant.
6. Applying source and release-day filters when requested.
7. Returning ranked evidence records.

The retriever supports source filtering before the final top-k selection.

The Atlas-related Q&A path can search both Day 3 and Day 4 evidence by default, while explicit release-day filters can restrict retrieval.

### Current limitations

- Retrieval is keyword-based, not vector-based.
- Synonym expansion is manually configured.
- Keyword overlap can miss relevant evidence expressed using different terminology.
- A retrieval score is not a measure of factual certainty.
- Release-day filtering does not constitute a complete historical event database.

A vector search system may be introduced later if evaluation demonstrates that keyword retrieval is insufficient.

## 6. CEO Question Answering

The CEO answer engine is implemented using Python rules and supported-topic logic.

The current flow is:

1. Validate the question.
2. Apply question-level privacy and safety checks.
3. Identify a supported topic.
4. Retrieve relevant evidence.
5. Apply topic-specific evidence filters.
6. Check whether the required evidence is available.
7. Construct an answer with evidence references and confidence information.
8. Return an appropriate response status.

The current answer engine supports selected topics, including:

- Engineering hiring status.
- Monthly company burn.
- Engineering pulse.
- Siddharth's resignation.
- Atlas version-three resignation impact.
- Atlas version-three work ownership.

The API exposes:

| Endpoint | Method | Purpose |
|---|---|---|
| `/` | GET | Health/root response |
| `/api/risks` | GET | Retrieve prioritized risks |
| `/api/ask` | POST | Submit a CEO question |

The answer engine is not currently powered by an LLM. It uses predefined topic handling, evidence selection and answer construction.

Unsupported questions return an insufficient-evidence response rather than an invented answer.

### 6.1 Evidence and Confidence

Answers can include:
- Answer status.
- Confidence assessment.
- Supporting evidence.
- Source filename.
- Source location.
- Release day.
- Citation and source excerpt.

The system distinguishes between documented information and uncertain claims.

For example, machine-generated voice-note transcripts are treated cautiously. A name appearing in a transcript is not automatically assumed to identify an employee with a similar name in another source.

The current implementation has topic-specific safeguards rather than a general-purpose automated conflict-resolution engine.

## 7. Risk Analysis

The risk engine collects evidence from approved sources and constructs prioritized business risks.

Current risk areas include:
- Engineering capacity and delivery.
- Funding and runway.
- Marketing continuity and knowledge transfer.

Risk prioritization uses heuristic logic informed by factors such as:
- Business impact.
- Urgency.
- Evidence availability.
- Source coverage.
- Relevant operational signals.

The resulting score is a rule-based prioritization score, not a probability of an event occurring.

Evidence strength and source coverage should not be interpreted as independent corroboration.

Each risk includes supporting evidence to help the CEO inspect the underlying records.

## 8. Privacy and Safety

The application includes question-level safeguards to prevent certain sensitive or unsupported requests from being answered.

Examples include:
- Requests for individual salary information.
- Requests for private employee messages.
- Requests for individual pulse comments or scores.
- Requests to identify an unnamed employee.
- Requests to rank employees by likelihood of quitting or resigning.

The system can still handle appropriate aggregate workforce questions when evidence supports them.

For example, an aggregate attrition-rate question is not automatically treated as a prohibited individual prediction. If the required data is missing, the engine returns insufficient evidence.

These are application-level question safeguards, not a complete authorization system.

Role-based access control, authenticated user permissions, database-level restrictions and comprehensive audit logging remain future requirements before deployment with real sensitive company data.

## 9. Employee-Agent Scope

The initial employee roster contains 14 selected profiles from the employee master export.

| Department | Count |
|---|---:|
| Engineering | 5 |
| Finance | 3 |
| People & Ops | 3 |
| Marketing | 3 |
| **Total** | **14** |

Employee identity and employment information are derived from the employee master export.

The current implementation includes employee identity profiles but does not yet provide 14 independently conversational agents.

Future agent functionality may include:
- Shared agent runtime.
- Evidence-grounded employee context.
- Approved profile-specific access.
- Conversation handling.
- Source-backed responses.
- Agent memory and auditability.

Personal thoughts, personality traits and private-life information must not be presented as verified facts without supporting evidence.

## 10. Point-in-Time and Evidence Limitations

The system preserves release-day metadata and supports release-day filtering in retrieval.

However, a complete point-in-time data model has not yet been implemented.

A fully historical system would need to distinguish:

- Event date: When something happened.
- Source date: When a source was created.
- Release date: When information became available to the system.

This distinction is important when answering questions about what the company knew at a particular historical point.

Future development should also improve source-level location metadata, structured date extraction and historical validation.

## 11. Frontend

The React and Vite frontend provides the executive dashboard.

Implemented functionality includes:
- CEO dashboard overview.
- Prioritized risk cards.
- Risk evidence inspection.
- CEO question input.
- API-based answer submission.
- Answer status and confidence display.
- Supporting evidence and source excerpts.
- Loading and error states.

The frontend communicates with the FastAPI backend through the configured API proxy during local development.

The dashboard is designed to make evidence inspection part of the answer workflow rather than treating generated answers as unquestionable facts.

## 12. Testing Strategy

The project includes automated tests covering:

- Document ingestion.
- Evidence-store construction.
- Retrieval and source filtering.
- Release-day filtering.
- Supported-topic identification.
- Answer construction.
- Privacy refusal behaviour.
- Insufficient-evidence handling.
- Risk construction and ranking.
- API responses and validation.

The latest verified full backend test run completed with:

**85 passed, 1 warning.**

The warning relates to a Starlette/httpx deprecation notice and does not indicate a test failure.

The repository currently contains seven test files.

The latest privacy regression check also verified that individual employee quit-likelihood ranking requests are refused while an unsupported aggregate attrition-rate question returns insufficient evidence.

Frontend production build has also passed in the development environment.

Test results should be re-run before final submission.

## 13. Development and Execution

The project uses a PowerShell startup script:

`run.ps1`

The startup script:
- Checks required release folders.
- Reuses the existing Python environment and frontend dependencies.
- Checks whether processed documents require ingestion.
- Supports forced re-ingestion.
- Starts the FastAPI backend.
- Starts the Vite frontend.
- Checks application availability.
- Stores process logs under `logs/`.

Start the application from the project root:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\run.ps1
```

The local application URLs are:

- Frontend: `http://127.0.0.1:5173/`
- Backend: `http://127.0.0.1:8000/`
- API documentation: `http://127.0.0.1:8000/docs`

## 14. Future Development

The following capabilities remain potential future improvements rather than completed functionality:

1. SQLite persistence and structured database models.
2. SQLite FTS5 or another indexed retrieval layer.
3. Embedding-based semantic retrieval.
4. LLM integration with a replaceable provider layer.
5. Conversational runtime for the 14 employee agents.
6. More comprehensive conflict detection and resolution.
7. Full event-date and point-in-time historical filtering.
8. Authentication and role-based access control.
9. Comprehensive audit logging.
10. Expanded integration and end-to-end testing.

These capabilities should only be marked implemented after development and validation.

## 15. Key Design Principles

1. Evidence before generated answers.
2. Preserve source provenance.
3. Never silently treat uncertain claims as verified facts.
4. Keep assumptions separate from documented information.
5. Apply release-day filters when appropriate.
6. Protect sensitive employee information.
7. Make risk prioritization explainable.
8. Communicate uncertainty clearly.
9. Prefer a working, maintainable system over unnecessary infrastructure.
10. Validate important behaviour through automated tests.

## 16. Repository Guidelines

- Keep raw source files and processed confidential data out of Git.
- Keep documentation aligned with actual implementation.
- Record AI assistance in `AI_LOG.md`.
- Record assumptions in `ASSUMPTIONS.md`.
- Record transcript conflicts and source reconciliation in `TRANSCRIPT_NOTES.md`.
- Keep technical decisions in `DECISIONS.md`.
- Do not describe planned features as implemented.
- Preserve original release-pack files.

The project is being developed as part of the Veloxa CXO Cockpit Hackathon, November 2026.