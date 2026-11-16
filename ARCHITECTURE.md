# Veloxa CXO Cockpit — Architecture

## 1. Objective

Build an evidence-grounded AI cockpit for Veloxa Technologies. The CEO should be able to ask questions about company operations, interview 14 AI employee agents, and identify important business risks.

The system must cite supporting records, distinguish facts from assumptions, surface conflicting evidence, and refuse to present unsupported information as fact.

The architecture prioritizes reliability, explainability, data privacy and traceability over unnecessary infrastructure.

## 2. Proposed Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| Frontend | React | CEO cockpit and employee-agent interface |
| Backend | Python, FastAPI | API endpoints and application logic |
| Data processing | OpenPyXL, python-docx, pypdf, Python CSV | Extract and process source files |
| Document storage | JSONL | Store extracted source documents |
| Database | SQLite | Store normalized records and evidence metadata |
| Retrieval | SQLite FTS5 initially | Search indexed source text |
| AI | LLM API with a replaceable provider layer | Generate grounded answers and agent responses |
| Testing | Pytest | Validate ingestion, retrieval, time filtering and answer quality |

The current implementation uses OpenPyXL instead of Pandas for Excel processing because Pandas could not import successfully in the development environment due to a Windows Application Control restriction affecting NumPy compiled DLLs.

The initial implementation will prioritize reliability and explainability. A vector database can be introduced if testing demonstrates that keyword-based retrieval is insufficient.

### 2.1 Current Implementation Status

| Component | Status |
|---|---|
| Project structure | Implemented |
| Day 1 file ingestion | Implemented |
| Excel, DOCX, PDF, CSV, TXT and EML readers | Implemented |
| JSONL document storage | Implemented |
| Initial 14 employee profiles | Implemented |
| Initial transcript and evidence analysis | Completed |
| Technical and evidence documentation | Initial version completed |
| SQLite database | Planned |
| SQLite FTS5 retrieval | Planned |
| RAG and LLM integration | Planned |
| Employee agent runtime | Planned |
| CEO Q&A and risk engine | Planned |
| React cockpit | Planned |
| Automated testing | Initial 10 tests passing |

Implementation status will be updated as components are developed and validated.

## 3. High-Level Architecture

```text
Release Packs (Day 1–Day 4)
          |
          v
    Ingestion Layer
          |
          v
 Extraction and Normalization
          |
          v
 Evidence and Company Database
          |
          +----------------------+
          |                      |
          v                      v
   Retrieval / RAG          Risk Analysis
          |                      |
          v                      |
    14 Employee Agents           |
          |                      |
          +----------+-----------+
                     |
                     v
             CEO Answer Engine
                     |
                     v
              React Cockpit
```

**Implementation note:** This diagram represents the target architecture. The current implementation has completed initial Day 1 ingestion, document extraction, JSONL storage, employee roster selection and initial employee profile generation. The remaining components are planned development stages.

## 4. Data Ingestion

The ingestion layer processes source files released each day.

Supported source formats:

- Excel: employee, payroll, finance and operational exports.
- Word: transcripts, briefs and CEO voice notes.
- PDF: board updates, invoices, letters and other documents.
- EML: email records.
- CSV: engineering and operational exports.
- TXT: data-room instructions and metadata.

Every extracted record preserves:

- Source filename.
- Source relative path.
- Source file type.
- Release day.
- Extracted content.
- Ingestion status.
- Extraction error details, when applicable.

Future ingestion improvements will add:

- Relevant event date.
- Extraction timestamp.
- Page, sheet, row or other source location.
- Normalized structured values.
- Validation and reconciliation metadata.

The original source files must remain unchanged.

### 4.1 Current Ingestion Implementation

The current file reader uses:

- OpenPyXL for Excel extraction.
- python-docx for Word document paragraphs and tables.
- pypdf for PDF text extraction.
- Python's built-in CSV module for CSV files.
- Built-in file reading for TXT and EML files.

Extracted documents are stored as JSONL records under `data/processed/`.

Day 1 ingestion successfully processed 15 files, including Excel workbooks, PDFs, Word documents and emails.

## 5. Core Data Model

The planned database will contain the following entities:

| Entity | Purpose |
|---|---|
| employees | Employee identity, department, role and employment status |
| sources | Source file metadata and release information |
| evidence | Extracted facts linked to original sources |
| events | Dated company events and activities |
| financial_records | Normalized financial transactions and metrics |
| agent_profiles | The 14 employee-agent profiles |
| assumptions | Invented or uncertain information with confidence and evidence |
| conflicts | Conflicting claims and their resolution status |
| agent_memory | Relevant, source-grounded agent context |
| audit_log | Questions, retrievals and answer provenance |

Evidence records must be traceable to their original sources.

Conflicting claims must not be silently overwritten. The system should retain the original claims, their sources and the reasoning behind any resolution.

The database model is planned and will be implemented as the application evolves.

## 6. Initial Employee-Agent Scope

The first 14 agents will be selected from the employee export.

| Department | Count |
|---|---:|
| Engineering | 5 |
| Finance | 3 |
| People & Ops | 3 |
| Marketing | 3 |
| **Total** | **14** |

Employee identity and employment status will come from `Employee_Master.xlsx`.

Each employee profile will distinguish:

- Verified identity and employment facts.
- Work context supported by source records.
- Personal-life details explicitly marked as assumptions.
- Evidence sources.
- Unresolved information.

Personality, personal-life details and private thoughts that are not present in the data must not be presented as verified facts. Any fictional assumptions must be explicitly labeled and recorded in `ASSUMPTIONS.md`.

A shared agent runtime will serve all 14 profiles. Each agent will receive only relevant company evidence and its own approved profile context.

### 6.1 Current Agent Implementation

The initial employee roster and 14 identity profiles have been generated using the employee master export.

The current profiles contain employee identity, department, role, manager, joining date, location and employment status.

Richer work histories, agent memory, personality assumptions and conversational behaviour remain planned development tasks.

## 7. Evidence-Grounded Question Answering

For each CEO question, the planned answer engine will:

1. Identify the subject and relevant time period.
2. Retrieve relevant structured records and source passages.
3. Apply release-date and access-control filters.
4. Check for conflicting or incomplete evidence.
5. Generate a concise answer using retrieved evidence.
6. Attach citations and a confidence assessment.
7. State clearly when available evidence is insufficient.

The LLM must not be treated as the source of company facts. Retrieved evidence is the source of truth.

Answers should distinguish verified facts, reasonable inferences, assumptions and unknowns.

## 8. Conflict Resolution

When sources disagree, the system will retain both claims and record:

- The competing claims.
- Their source files and locations.
- The reliability and limitations of each source.
- The resolution or unresolved status.
- The reasoning behind the decision.
- Confidence in the conclusion.

A source will not automatically win merely because it is newer or machine-readable.

The decision must consider the type of information, source reliability, date and available corroborating evidence.

Machine-generated transcripts require additional caution because names, numbers, units and speaker attribution may be inaccurate.

## 9. Point-in-Time Data Control

Every source will have a release date. Where available, records will also have an event date.

For a question such as "What did we know on 17 November?", retrieval must exclude information released after 17 November, even if that information describes an earlier event.

This prevents future information from leaking into historical answers.

The system will distinguish:

- Event date: When something happened.
- Source date: When the source was created.
- Release date: When the information became available to the system.

Point-in-time filtering will be validated through automated tests.

## 10. Risk Analysis

The risk engine will identify and rank risks using:

- Business impact.
- Likelihood.
- Urgency.
- Evidence strength.
- Uncertainty.
- Relevant owners or departments.

Each risk must include supporting evidence and explain why it matters.

Unsupported speculation must not be presented as a confirmed risk.

Risks should be categorized as confirmed, potential or requiring further investigation, depending on the strength of available evidence.

## 11. Privacy and Access Control

Sensitive employee information, especially individual payroll figures, must be protected at the application and database-query layers.

CEO-facing financial answers should use permitted aggregate figures rather than exposing individual salary details.

Prompt instructions alone are not sufficient security controls.

Additional safeguards will include:

- Access restrictions for employee-level records.
- Role-based authorization where required.
- Restricted access to sensitive financial information.
- Audit logging for sensitive queries.
- Exclusion of raw and processed source data from public Git repositories.

Raw release files and processed source data are excluded from Git using `.gitignore`.

Application-level authorization and database-level access restrictions remain required before exposing sensitive records.

## 12. Testing Strategy

Automated tests will cover:

- File extraction and ingestion.
- Data normalization and validation.
- Evidence-to-source traceability.
- Conflict detection.
- Point-in-time filtering.
- Employee-agent identity grounding.
- Citation correctness.
- Risk ranking.
- Privacy and access restrictions.
- Unsupported-question refusal and uncertainty handling.

The final target is at least 25 automated tests, including at least 5 tests for uncertainty or refusal behaviour.

### 12.1 Current Test Coverage

The initial test suite contains 10 passing tests covering:

- Day 1 document count.
- Successful ingestion status.
- Duplicate source-path detection.
- Employee master record count.
- Correct selection of 14 employee agents.
- Unique employee IDs.
- Valid agent departments.
- Inclusion of the notice-period employee.
- Board PDF text extraction.
- Preservation of the blank Entity Resolution template.

Further tests will be added as retrieval, agent behaviour, historical filtering and risk analysis are implemented.

## 13. Key Design Principles

1. Evidence before generated answers.
2. Preserve source provenance.
3. Never silently resolve conflicting information.
4. Keep assumptions separate from verified facts.
5. Enforce historical release-date boundaries.
6. Protect sensitive employee information.
7. Use a shared, maintainable agent runtime.
8. Communicate uncertainty clearly.
9. Prefer a working, explainable system over unnecessary complexity.
10. Validate important behaviour through automated tests.

## 14. Implementation Plan

- Phase 1: Inspect release packs and define the data model.
- Phase 2: Build ingestion and evidence storage.
- Phase 3: Implement retrieval and source citations.
- Phase 4: Implement the 14 employee agents.
- Phase 5: Build CEO Q&A and risk analysis.
- Phase 6: Build the React cockpit.
- Phase 7: Add automated tests and process new releases.
- Phase 8: Validate CEO voice-note responses and final setup instructions.

## 15. Development and Repository Guidelines

- Keep raw source files and processed confidential data out of Git.
- Maintain documentation as implementation decisions change.
- Record AI assistance in `AI_LOG.md`.
- Record assumptions and their evidence in `ASSUMPTIONS.md`.
- Record transcript conflicts and source reconciliation in `TRANSCRIPT_NOTES.md`.
- Keep technical decisions documented in `DECISIONS.md`.
- Do not mark planned functionality as implemented until it has been developed and tested.

The project is under active development as part of the Veloxa CXO Cockpit Hackathon, November 2026.