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