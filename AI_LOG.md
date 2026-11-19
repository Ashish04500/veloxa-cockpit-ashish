# AI Usage Log — Veloxa CEO Cockpit

## Date: 16 November 2026

### 1. Project planning and architecture
- Used ChatGPT to help break down the hackathon requirements into development tasks.
- Discussed project folder structure and responsibilities of ingestion, employee agents, evidence retrieval and cockpit modules.
- Reviewed the initial architecture and adjusted it to match the actual implementation.

### 2. File ingestion and extraction
- Used AI assistance to develop and debug Python file-reading logic.
- Implemented extraction using OpenPyXL, python-docx, pypdf and Python's built-in CSV functionality.
- Used AI assistance to investigate extraction issues involving Excel headers and DOCX tables.
- Validated extraction across all 15 Day 1 files.

### 3. Employee profiles
- Used AI assistance to structure employee records into initial agent profiles.
- Implemented selection of 14 employees from Engineering, Finance, People & Ops and Marketing.
- Verified the resulting roster against Employee_Master.xlsx.

### 4. Evidence analysis
- Used AI assistance to compare leadership transcripts, board updates, finance exports and HR records.
- Investigated discrepancies involving company headcount, ARR, monthly burn, hiring, summit expenditure and payroll.
- Reviewed findings against original source documents rather than treating AI-generated interpretations as verified facts.

### 5. Documentation
- Used AI assistance to draft and organise TRANSCRIPT_NOTES.md, ASSUMPTIONS.md and DECISIONS.md.
- Reviewed the content against extracted source evidence before saving.

### 6. Automated testing
- Used AI assistance to create initial pytest tests.
- Ran the tests locally and verified that all 10 initial tests passed.

### 7. Human verification and responsibility
- Executed commands and scripts locally.
- Reviewed terminal output and investigated errors.
- Verified extracted records and compared findings with source documents.
- Retained responsibility for implementation decisions, testing and final project validation.

### Remaining work
- Expand automated test coverage to at least 25 tests, including uncertainty and refusal tests.
- Implement evidence retrieval and citation support.
- Complete the employee agent behaviour and CEO question-answering functionality.
- Integrate the remaining release packs.

## Day 2 — 17 November 2026

- Used AI assistance to inspect and interpret the T3 Head of People transcript and T6a CEO voice note.
- Used AI assistance to compare HR transcript claims against hiring records, pulse survey data, emails, and Siddharth Mehta's resignation letter.
- Identified evidence-backed concerns around Engineering capacity and Marketing knowledge transfer.
- Recorded uncertainty around attrition figures, hiring metrics, and the unnamed engineer.
- Decided to preserve small-team survey privacy and avoid exposing individual comments.
- Translated the CEO's T6a request into a proactive top-three risk summary requirement.
- All evidence interpretations and implementation decisions are subject to verification against source files.


### Risk Engine Implementation
- Created a provisional CEO risk engine in `backend/app/cockpit/risk_engine.py`.
- Added source-specific and content-specific evidence filtering to prevent unrelated records from appearing under a risk.
- Implemented a transparent heuristic score using impact, manually assigned urgency, and distinct evidence-source count.
- Ranked engineering capacity, funding/runway, and marketing continuity risks using the calculated scores.
- Preserved evidence citations, confidence labels, recommended actions, and explicit uncertainty.
- Added six risk-engine tests covering risk count, ranking, priorities, evidence presence, payroll exclusion, and score calculation.
- Full test suite: 43 tests passed.
- Limitation: urgency is manually assigned, and evidence-source count is only a rough proxy for evidence strength. Scores are prioritisation heuristics, not probabilities.

### CEO Cockpit API and Question-Answering — 17 November 2026

#### 1. FastAPI backend
- Implemented the FastAPI application in `backend/app/main.py`.
- Added a health-check endpoint (`GET /`).
- Added a top-three risk endpoint (`GET /api/risks`) backed by the risk engine.
- Verified both endpoints locally using the API documentation and automated tests.

#### 2. Evidence-backed CEO question answering
- Implemented `backend/app/cockpit/answer_engine.py`.
- Added topic-specific evidence retrieval for engineering hiring, monthly burn, engineering pulse and Siddharth's resignation.
- Added source and record filtering so answers include only relevant evidence.
- Added citations, confidence labels and insufficient-evidence responses.
- Engineering hiring answers require five specific supporting records, including both paused requisitions and the relevant emails.

#### 3. Privacy and uncertainty safeguards
- Added refusal rules for individual salary information, private survey comments and identification of the unnamed engineer.
- Unsupported questions return an insufficient-evidence response instead of an invented answer.
- Engineering workload impact is explicitly described as unquantified rather than treated as a proven consequence of the hiring pause.

#### 4. Verification
- Manually tested four supported question categories and three privacy/unsupported-question cases.
- Verified that the engineering hiring answer returned all five required evidence records.
- Ran the complete pytest suite: 52 tests passed, with one non-blocking deprecation warning.
- Added API and answer-engine automated tests.

#### 5. Current limitations
- The answer engine currently uses deterministic, topic-specific responses; it is not an LLM-based conversational agent.
- The risk endpoint provides data to the frontend, but automatic display when the CEO opens a dashboard is not implemented yet.
- Point-in-time event-date filtering and comprehensive role-based access control are not yet complete.
- Risk scores remain heuristic prioritisation scores, not statistical probabilities.

#### 6. Human verification and responsibility
- Ran the implementation and tests locally.
- Checked returned evidence against the original source records.
- Reviewed privacy refusals and unsupported-question behaviour.
- Retained responsibility for reviewing the code, interpreting evidence and validating implementation decisions.

#### 7. Additional uncertainty test and final verification
- Added a test confirming that the ambiguous attrition statement ("about twelve") is not reported as a verified attrition rate.
- The test expects an insufficient-evidence response with Low confidence and no supporting evidence.
- Re-ran the complete pytest suite: 53 tests passed, with one non-blocking Starlette deprecation warning.
- The five uncertainty/refusal scenarios cover unsupported questions, ambiguous attrition, individual salary, private survey comments and unnamed employee identity.

 
### React CEO Dashboard Implementation — 18 November 2026

#### 1. Frontend setup
- Created a React frontend using Vite.
- Configured the Vite development proxy to forward `/api` requests to the FastAPI backend.
- Added a responsive executive dashboard with a dark visual theme.

#### 2. Dashboard functionality
- Integrated the frontend with `GET /api/risks`.
- Automatically fetches and displays the top three business risks when the dashboard opens.
- Added summary metrics for priority risks, high-impact risks and distinct evidence sources.
- Added risk cards showing priority, heuristic score, impact, confidence, urgency and evidence strength.
- Added recommended CEO actions and explicit uncertainty for each risk.
- Added expandable evidence sections with source citations.
- Added manual refresh functionality and last-updated timestamp.
- Implemented a time-aware greeting.

#### 3. API status and error handling
- Added a dynamic API connection indicator.
- Added error handling for failed API requests.
- Verified that stopping the backend changes the status to API DISCONNECTED and displays an error.
- Verified that restarting the backend restores successful API loading.

#### 4. Verification
- Verified the dashboard in the browser with all three risk records.
- Verified that supporting evidence expands correctly.
- Frontend ESLint check: passed.
- Frontend Vite production build: passed.
- Verified frontend-to-backend communication through the Vite proxy.

#### 5. Current limitations
- API status reflects the latest request and does not continuously monitor the backend.
- Risk scores remain heuristic prioritisation scores, not probabilities.
- Historical point-in-time filtering and comprehensive role-based access control remain incomplete.

#### 6. Human verification and responsibility
- Reviewed the dashboard output against the backend API response.
- Tested successful and failed API requests.
- Reviewed frontend code and verified lint and production build results.
- Retained responsibility for validating implementation decisions and evidence presentation.

### Frontend Dependency Security Audit — 18 November 2026

- Ran `npm audit` and identified five high-severity findings associated with the picomatch dependency in the Vite development toolchain.
- Dependency inspection confirmed Vite 8.3.8, @vitejs/plugin-react 6.3.0 and picomatch 4.0.7.
- npm proposed a forced fix that would downgrade Vite to 6.2.7, potentially introducing breaking changes.
- Avoided applying the forced downgrade without a verified compatible fix.
- Ran `npm audit --omit=dev`; result: zero production vulnerabilities.
- Current limitation: development dependency vulnerabilities remain unresolved and require monitoring for a compatible upstream patch.


### Day 3 Evidence Ingestion and Risk Reconciliation — 18 November 2026

#### 1. Day 3 ingestion
- Created `backend/app/ingest_day3.py` to process the Day 3 release pack.
- Successfully processed 14 files with no reported ingestion failures.
- Included engineering records, Jira exports, incident data, email correspondence, launch documents and CEO/department transcripts.
- Stored extracted content in the Day 3 processed evidence file.

#### 2. Evidence review and reconciliation
- Reviewed the Atlas Jira export and identified a formal GA date revision from 15 September 2026 to 15 December 2026, recorded on 2 September 2026.
- Identified 62 Jira issues: 35 Done, 8 In Progress and 19 To Do. Outstanding issues were not automatically classified as GA blockers.
- Reviewed the incident register and identified three August SEV1 routing-api incidents.
- Compared the incident register with the on-call rota and preserved the unresolved distinction between "Sneha" and "Snehal".
- Reviewed the SRE contractor invoice and treated it as evidence of a recorded monthly support charge, not proof of a budget overrun.
- Reviewed the Atlas launch kit and distinguished prepared materials from unpublished or draft materials.
- Reviewed T4, T5 and T6b transcripts and retained uncertainty around marketing metrics, engineering workload, audio gaps and the planned CRO reporting change.
- Did not infer that Siddharth's departure caused the Atlas delay or that Git commit counts establish individual productivity.

#### 3. Risk-engine update
- Updated the Engineering risk to focus on Atlas delivery and reliability.
- Added evidence retrieval for the Jira release-date revision and the three August SEV1 routing-api incidents.
- Updated the risk explanation, recommended action and uncertainty statements.
- Retained the existing heuristic scoring approach.
- The risk score is a prioritisation heuristic, not a probability or statistically calibrated forecast.

#### 4. Documentation
- Appended Day 3 evidence reconciliation notes to `TRANSCRIPT_NOTES.md`.
- Appended Day 3 assumptions and evidence limitations to `ASSUMPTIONS.md`.
- Appended Day 3 implementation and product decisions to `DECISIONS.md`.
- Added the T6b response to `CEO_VOICE_NOTE_RESPONSES.md`.
- Documented the CRO reporting change as planned, not effective.
- Recorded effective-dated organisational history as a future product requirement, not an implemented feature.

#### 5. Testing status
- Targeted risk-engine tests: 6 passed.
- Full backend test suite: 53 passed.
- One non-blocking Starlette/httpx deprecation warning remained.
- Runtime verification was completed; see Section 7.

#### 6. Human verification and responsibility
- Reviewed extracted source records and compared transcript statements with structured records.
- Reviewed the risk-engine changes and documented their evidence limitations.
- Preserved ambiguous identities, incomplete information and unsupported causal claims rather than presenting them as facts.
- Used AI assistance for code drafting, test guidance, evidence interpretation and documentation. Final responsibility for reviewing and validating the submitted implementation remains with the developer.

#### 7. Runtime verification
- Started the FastAPI backend and verified `GET /api/risks` successfully.
- Confirmed the Engineering risk returns the revised Atlas GA date (15 September to 15 December 2026).
- Confirmed all three August SEV1 routing-api incidents (INC-201, INC-203 and INC-205) appear with their source citations.
- Verified the corrected risk explanation attributes incidents to the incident register, not Jira.
- Started the React frontend and manually inspected the expanded Engineering risk evidence.
- Confirmed the dashboard displays the Jira release-date record, all three incident records, and the supporting Day1/Day2 hiring and pulse evidence.
- Re-ran the complete backend test suite: 53 passed, with one non-blocking deprecation warning.


#### 8. Regression testing
- Added a test confirming the Engineering risk includes the revised Atlas GA date and all three August SEV1 incident IDs.
- Added a test confirming evidence collection requires every specified required term.
- Complete backend test suite: 55 passed, with one non-blocking Starlette/httpx deprecation warning.
- Frontend ESLint passed.
- Frontend production build passed.
- Git whitespace check passed; only line-ending warnings remain.

### Day 4 Evidence Ingestion and Privacy Safeguards - 19 November 2026

#### 1. Day 4 ingestion
- Added `backend/app/ingest_day4.py` to process the Day 4 release pack.
- Processed the two available source files: `T6c_CEO_Voice_Note.docx` and `T6d_CEO_Voice_Note.docx`.
- Ingestion completed with two successful files and no reported failures.
- Confirmed that the combined evidence store loads 41 documents across Day 1 through Day 4 and 339 evidence records.

#### 2. CEO voice-note handling
- Reviewed T6c, in which the CEO requests employee quit-likelihood rankings and private Slack messages.
- Added refusal handling for individual employee quit-likelihood ranking requests and private-message disclosure requests.
- Reviewed T6d, which contains an auto-transcribed statement that an individual referred to as "Pria" has resigned.
- Preserved the statement as an unverified transcript claim rather than confirmed HR information.
- Did not resolve "Pria" to another employee based on name similarity.

#### 3. Privacy and uncertainty verification
- Runtime-checked multiple phrasings of individual quit-likelihood ranking requests.
- Confirmed those requests return a refusal.
- Confirmed an aggregate attrition-rate question is not incorrectly treated as an individual prediction request; it returns insufficient evidence where supporting data is unavailable.
- The reported two-month notice period in T6d remains uncertain because the speaker qualifies it with "I think."

#### 4. Current verification
- Complete backend test suite: 79 passed, with one non-blocking Starlette/httpx deprecation warning.
- Day 4 ingestion: two files processed successfully, zero failures.
- Combined evidence store: 41 documents and 339 evidence records.
- Frontend production build had passed in the preceding verification cycle; rerun before final submission.

#### 5. Human verification and responsibility
- Reviewed the Day 4 transcript claims as attributed statements, not independently verified employee records.
- Preserved identity ambiguity and uncertainty around the reported resignation and notice period.
- Used AI assistance for implementation guidance, test design, evidence interpretation and documentation. Final responsibility for reviewing and validating the submitted implementation remains with the developer.
