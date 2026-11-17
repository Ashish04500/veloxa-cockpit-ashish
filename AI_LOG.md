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

### CEO Cockpit API and Question-Answering � 17 November 2026

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