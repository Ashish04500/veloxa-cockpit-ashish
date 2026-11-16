# Veloxa CXO Cockpit — Architecture

## 1. Objective

Build an evidence-grounded AI cockpit for Veloxa Technologies. The CEO should be able to ask questions about company operations, interview 14 AI employee agents, and identify important business risks.

The system must cite supporting records, distinguish facts from assumptions, surface conflicting evidence, and refuse to present unsupported information as fact.

## 2. Proposed Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| Frontend | React | CEO cockpit and employee-agent interface |
| Backend | Python, FastAPI | API endpoints and application logic |
| Data processing | Pandas, openpyxl, python-docx | Process Excel, Word and structured data |
| Database | SQLite | Store normalized records and evidence metadata |
| Retrieval | SQLite FTS5 initially | Search indexed source text |
| AI | LLM API, with a replaceable provider layer | Generate grounded answers and agent responses |
| Testing | Pytest | Validate ingestion, retrieval, time filtering and answer quality |

The initial implementation will prioritize reliability and explainability over unnecessary infrastructure. A vector database can be introduced if testing shows that keyword-based retrieval is insufficient.

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

## 4. Data Ingestion

The ingestion layer will process the files released each day.

Supported source formats:
- Excel: employee, payroll, finance and operational exports.
- Word: transcripts, briefs and CEO voice notes.
- PDF: board updates, invoices, letters and other documents.
- EML: email records.
- CSV: engineering and operational exports.
- TXT: data-room instructions and metadata.

Every extracted record should preserve:
- Source filename
- Source type
- Release day
- Relevant event date, if available
- Extraction timestamp
- Page, sheet, row or other source location
- Original text or structured values
- Extraction status and validation errors

The original source files must remain unchanged.

## 5. Core Data Model

Initial database entities:

| Entity | Purpose |
|---|---|
| employees | Employee identity, department, role and employment status |
| sources | Source file metadata and release information |
| evidence | Extracted facts linked to their original sources |
| events | Dated company events and activities |
| financial_records | Normalized financial transactions and metrics |
| agent_profiles | The 14 employee-agent profiles |
| assumptions | Invented or uncertain information with confidence and evidence |
| conflicts | Conflicting claims and their resolution status |
| agent_memory | Relevant, source-grounded agent context |
| audit_log | Questions, retrievals and answer provenance |

Evidence records must be traceable to their original sources. Conflicting claims must not be silently overwritten.

## 6. Initial Employee-Agent Scope

The first 14 agents will be selected from the employee export:

| Department | Count |
|---|---:|
| Engineering | 5 |
| Finance | 3 |
| People & Ops | 3 |
| Marketing | 3 |
| Total | 14 |

Employee identity and employment status will come from the HR export. Personality, personal-life details and private thoughts that are not present in the data will be explicitly labeled as fictional assumptions and recorded in `ASSUMPTIONS.md`.

A shared agent runtime will serve all 14 profiles. Each agent will receive only relevant company evidence and its own approved profile context.

## 7. Evidence-Grounded Question Answering

For each CEO question:

1. Identify the subject and relevant time period.
2. Retrieve relevant structured records and source passages.
3. Apply release-date and access-control filters.
4. Check for conflicting or incomplete evidence.
5. Generate a concise answer using retrieved evidence.
6. Attach citations and a confidence assessment.
7. State clearly when the available evidence is insufficient.

The LLM must not be treated as the source of company facts. Retrieved evidence is the source of truth.

## 8. Conflict Resolution

When sources disagree, the system will retain both claims and record:

- The competing claims
- Their source files and locations
- The reliability and limitations of each source
- The resolution or unresolved status
- The reasoning behind the decision

A source will not automatically win merely because it is newer or machine-readable. The decision must consider the type of information and the reliability of the source.

## 9. Point-in-Time Data Control

Every source will have a release date. Where available, records will also have an event date.

For a question such as "What did we know on 17 November?", retrieval must exclude information released after 17 November, even if that information describes an earlier event.

This prevents future information from leaking into historical answers.

## 10. Risk Analysis

The risk engine will identify and rank risks using:

- Business impact
- Likelihood
- Urgency
- Evidence strength
- Uncertainty
- Relevant owners or departments

Each risk must include supporting evidence and explain why it matters. Unsupported speculation must not be presented as a confirmed risk.

## 11. Privacy and Access Control

Sensitive employee information, especially individual payroll figures, must be protected at the application and database-query layers.

CEO-facing financial answers should use permitted aggregate figures rather than exposing individual salary details. Prompt instructions alone are not sufficient security controls.

## 12. Testing Strategy

Automated tests will cover:

- File extraction and ingestion
- Data normalization and validation
- Evidence-to-source traceability
- Conflict detection
- Point-in-time filtering
- Employee-agent identity grounding
- Citation correctness
- Risk ranking
- Privacy and access restrictions
- Unsupported-question refusal and uncertainty handling

The final target is at least 25 automated tests, including at least 5 tests for uncertainty or refusal behavior.

## 13. Key Design Principles

1. Evidence before generated answers.
2. Preserve source provenance.
3. Never silently resolve conflicting information.
4. Keep assumptions separate from verified facts.
5. Enforce historical release-date boundaries.
6. Protect sensitive employee information.
7. Use a shared, maintainable agent runtime.
8. Prefer a working, explainable system over unnecessary complexity.

## 14. Implementation Plan

- Phase 1: Inspect release packs and define the data model.
- Phase 2: Build ingestion and evidence storage.
- Phase 3: Implement retrieval and source citations.
- Phase 4: Implement the 14 employee agents.
- Phase 5: Build CEO Q&A and risk analysis.
- Phase 6: Build the React cockpit.
- Phase 7: Add automated tests and process new releases.
- Phase 8: Validate CEO voice-note responses and final setup instructions.