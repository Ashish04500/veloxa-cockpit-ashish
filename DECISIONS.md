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


## Day 3 Decisions

### 1. Atlas GA Date Reconciliation
**Decision:** Use the Jira Versions record as the current formal Atlas GA date: 15 December 2026, revised from 15 September 2026 on 2 September 2026.

**Reason:** The structured Jira release record provides a formal date and change history. The optimistic T5 transcript does not override it.

**Limitation:** The reason for the revision is not established. Do not classify every unresolved Jira issue as a GA blocker.

### 2. Engineering Reliability Risk
**Decision:** Include the three August SEV1 routing-api incidents in the Engineering risk evidence.

**Reason:** The incident register records three SEV1 incidents, and the 24 August email confirms that Atlas performance work was paused to stabilise routing-api.

**Limitation:** Incident root causes, total engineering effort and individual workload are not established.

### 3. Employee Identity Resolution
**Decision:** Keep "Sneha" and "Snehal" as separate unresolved identity references.

**Reason:** The incident register and on-call rota use both names. There is insufficient evidence to merge them.

**Limitation:** Do not attribute all incidents or on-call activity to one employee without authoritative confirmation.

### 4. Workload and Productivity Claims
**Decision:** Do not use Git commit counts, rota assignments or incident responder counts as direct measures of employee productivity, overtime or workload.

**Reason:** These records show activity or assignments, not hours worked or individual capacity.

### 5. Contractor Invoice Interpretation
**Decision:** Treat invoice PIS-114 as evidence of September SRE support costing ₹1,20,000 before tax.

**Reason:** The invoice records a monthly support charge.

**Limitation:** It does not establish a budget overrun or prove the contractor's identity in relation to the incident and rota records.

### 6. Marketing Launch Readiness
**Decision:** Represent the Atlas launch kit as partially prepared, not fully launch-ready.

**Reason:** The launch kit records prepared materials, but the website page was unpublished and the press note remained a draft.

**Limitation:** Do not attribute the launch delay to Siddharth's departure without direct evidence.

### 7. Marketing Reporting Change
**Decision:** Preserve the current reporting structure until the new CRO transition is confirmed.

**Reason:** T6b describes a planned change but gives an uncertain effective date: next month or the month after.

**Implementation direction:** Support effective-dated reporting relationships so historical organisational structure can be reconstructed without rewriting past reporting lines.

**Unknowns:** CRO identity, approval status and exact effective date.

### 8. Evidence and Transcript Handling
**Decision:** Preserve unresolved statements and transcript limitations rather than filling gaps with assumptions.

**Reason:** T4 and T5 contain unverified claims, and T5 has an audio gap from 11:20 to 15:30.

**Implementation:** Prefer structured primary records for formal dates and incident counts, while retaining transcript claims as attributed statements.

## Day 4 Decisions

### 1. Individual Quit-Likelihood Requests
**Decision:** Refuse requests to rank individual employees by likelihood of quitting or resigning.

**Reason:** The available evidence does not justify individual predictions, and such rankings create unsupported personal inferences.

**Implementation:** Requests using variations of individual quit-likelihood ranking language are handled by the question-safety checks.

### 2. Private Employee Communications
**Decision:** Do not disclose private Slack messages or other private employee communications through the CEO question-answering interface.

**Reason:** A CEO request alone does not establish that private communications are appropriate evidence for disclosure.

**Implementation:** Such requests are refused rather than answered through evidence retrieval.

### 3. T6d Resignation Claim
**Decision:** Treat the reported resignation of "Pria" as an unverified transcript claim.

**Reason:** T6d is an auto-transcribed CEO voice note and is not, by itself, an authoritative HR resignation record.

**Limitation:** Do not update employee status, notice period or last working day based only on this statement.

### 4. Employee Identity Resolution
**Decision:** Preserve "Pria" as transcribed and do not automatically match it to "Priya" or another employee.

**Reason:** Similar names do not establish identity.

**Required confirmation:** An authoritative employee record or direct HR confirmation.

### 5. Notice Period
**Decision:** Treat the reported two-month notice period as uncertain.

**Reason:** The CEO qualifies the statement with "I think."

**Limitation:** Do not calculate a confirmed last working day from this estimate.

### 6. Evidence Attribution
**Decision:** Keep CEO voice-note statements distinct from independently verified HR facts.

**Reason:** A transcript records what a speaker said; it does not independently verify the underlying event.

**Implementation:** Preserve source attribution, uncertainty and the need for corroboration in answers and documentation.
