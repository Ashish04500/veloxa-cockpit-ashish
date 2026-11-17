# Technical Decisions — Veloxa CEO Cockpit

## 1. Project structure

**Decision:** Separate the application into ingestion, agents, database, RAG and cockpit modules.

**Reason:** Each module has a distinct responsibility. This makes the system easier to test, maintain and extend as new data arrives.

**Status:** Initial structure created.

## 2. Data ingestion

**Decision:** Use Python-based file readers for DOCX, PDF, XLSX, CSV, TXT and EML files.

**Libraries:**
- OpenPyXL for Excel files.
- python-docx for Word documents.
- pypdf for PDF extraction.
- Python's built-in csv module for CSV files.

**Reason:** These libraries provide the required extraction capabilities without introducing unnecessary dependencies.

## 3. Pandas dependency

**Decision:** Use OpenPyXL and built-in Python functionality for current Excel processing instead of relying on Pandas.

**Reason:** Pandas could not import successfully in the development environment because Windows Application Control blocked NumPy compiled DLLs.

**Trade-off:** Some data-processing operations require more manual Python code.

## 4. Processed document storage

**Decision:** Store extracted documents as JSON Lines (JSONL).

**Reason:** Each source file is stored as an individual JSON record containing its filename, path, release day, file type, extracted content and ingestion status.

**Benefit:** Documents can be processed independently, inspected and used by later application modules.

## 5. Source evidence preservation

**Decision:** Preserve source filenames and relative paths alongside extracted content.

**Reason:** Every factual response should be traceable to its original source.

**Future requirement:** Add page, sheet, row and cell-level references to the evidence retrieval layer.

## 6. Employee agent selection

**Decision:** Create 14 initial employee profiles using employees from Engineering, Finance, People & Ops and Marketing.

**Reason:** The Candidate Brief explicitly specifies 14 people across these departments.

**Implementation:** Employee_Master.xlsx is the source of employee identity, department, role, manager and employment status.

## 7. Agent profile structure

**Decision:** Separate verified employee facts, work context, personal-life details, assumptions and evidence sources.

**Reason:** Verified facts must not be confused with generated or assumed information.

**Implementation status:** Initial identity profiles created. Richer work histories and agent behaviour remain future work.

## 8. Conflicting evidence

**Decision:** Do not silently correct conflicting information from machine-generated transcripts.

**Reason:** Transcripts can contain incorrect names, numbers, units and speaker attribution.

**Approach:** Preserve conflicting statements, compare them with system exports and formal documents, and report unresolved discrepancies with confidence and unknowns.

## 9. Sensitive payroll information

**Decision:** Do not expose individual employee salary figures in CEO-facing responses.

**Reason:** The CFO explicitly requested aggregate-only payroll visibility.

**Approach:** Use aggregate payroll information for executive reporting and restrict employee-level details to authorised investigations.

## 10. Blank templates

**Decision:** Preserve intentionally blank templates such as Entity_Resolution.xlsx without treating them as extraction failures.

**Reason:** An empty template is different from a failed file extraction.

## 11. Testing strategy

**Decision:** Use pytest for automated validation.

**Initial coverage:** Day 1 document count, ingestion status, duplicate source paths, employee count, agent selection, employee ID uniqueness, department validity, notice-period inclusion, PDF extraction and blank template handling.

**Current result:** 10 tests passing.

**Future requirement:** At least 25 automated tests, including at least five tests covering uncertainty, conflicting evidence and appropriate refusal.

## 12. Data privacy and repository management

**Decision:** Keep raw release files, processed documents, virtual environments and environment secrets out of Git.

**Reason:** Source material includes confidential business information and individual payroll data.

**Implementation:** `.gitignore` excludes `data/raw/`, `data/processed/`, `.env` files, virtual environments and generated database files.

## Day 2 Decisions

### 1. Proactive CEO Risk Summary
The cockpit will display the top three current business risks on opening, without requiring a CEO question. Each risk must include evidence, confidence, impact, and a recommended action.

### 2. Employee Survey Privacy
Individual pulse survey comments will not be exposed for small teams. Aggregate scores and response counts may be displayed, but the unnamed employee mentioned in T3 will not be identified.

### 3. Evidence-Based Risk Ranking
Risk ranking must distinguish verified evidence from assumptions. Unverified transcript figures will not be used as established facts. Rankings remain provisional as new evidence arrives.

### 4. Marketing Handover
Siddharth Mehta's departure is confirmed. The cockpit may flag a potential marketing knowledge-transfer risk, but must not claim a launch failure without further evidence.