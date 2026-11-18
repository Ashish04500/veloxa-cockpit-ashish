## HR data findings — 16 Nov 2026

| Finding | Classification | Confidence | Evidence |
|---|---|---|---|
| Engineering has two backend requisitions on hold. | Verified fact | High | Hiring_Tracker.xlsx, REQ-014 and REQ-015 |
| The Routing backend final round was cancelled on 14-Aug-2026. | Verified fact | High | Hiring_Tracker.xlsx, REQ-014 |
| Product Marketing Manager hiring is marked as a backfill. | Verified fact | High | Hiring_Tracker.xlsx, REQ-016 |
| REQ-016 may be related to Siddharth Mehta's notice period. | Inference | Medium | Employee_Master.xlsx and Hiring_Tracker.xlsx |
| The leave register uses abbreviated employee names. | Verified fact | High | Leave_Register.xlsx |
| Leave records do not establish employees' personal motivations or health conditions. | Data interpretation rule | High | Leave_Register.xlsx |

**Implementation rule:** Preserve the original source record and employee match. Do not infer individual performance, workload, health, or personality from leave records.

## Pulse survey findings — 16 Nov 2026

### Verified observations

1. Engineering engagement declined from 4.0 (Oct–Dec 2025) to 3.1 (Jul–Sep 2026).
2. Marketing engagement declined from 3.9 to 3.4 over the same period.
3. Finance increased from 3.8 to 3.9.
4. People & Ops remained at 4.1.
5. Sales remained broadly stable, increasing from 3.7 to 3.8.
6. Support remained stable at 4.0.

### Evidence

Source: `Pulse_Survey.xlsx`, sheet `Pulse by team`.

### Confidence

High confidence in the recorded team scores. The cause of the declines is unknown.

### Important limitations

- All teams have fewer than six employees.
- Individual comments are suppressed.
- Engineering's latest response count was 4 of 5.
- These scores must not be attributed to individual employees.

### Risk interpretation

Engineering is a priority area for investigation because it has the largest engagement decline. Marketing is a secondary area of concern.

These are warning signals, not proof of employee dissatisfaction, burnout, or management failure.

### What would change our assessment?

Newer pulse data, confidential employee feedback, workload records, incident trends, project delays, or direct employee statements.

## Finance and leadership assumptions — 16 Nov 2026

| Assumption / unresolved issue | Evidence and source reference | Confidence | What would change the assessment? |
|---|---|---|---|
| The CEO's "one-eighty" headcount statement may be a transcription error. | T1_CEO_Kickoff_Call.docx; Employee_Master.xlsx (19 employee records); both board updates (team size 19). | High that the sources conflict; low on the intended spoken number. | Original audio or a corrected leadership statement. |
| The CEO's ARR figure of ₹42–45 crore is inconsistent with the board-reported ARR of ₹5.8 crore and ₹6.1 crore. | T1_CEO_Kickoff_Call.docx; Board_Update_Apr-Jun_2026.pdf; Board_Update_Jul-Sep_2026.pdf. | High that a discrepancy exists; low on which transcript figure or unit is correct. | Audited revenue records, ARR reports or CFO confirmation. |
| The CFO's reported monthly burn of ₹2.2–2.5 lakh may have an incorrect unit or transcription. | T2_CFO_Call.docx; board updates report ₹46 lakh and ₹44 lakh monthly burn; GL records ₹31.75 lakh monthly payroll alone. | High that ₹2.2–2.5 lakh is not consistent with total burn if interpreted literally. | Reconciled cash-flow statement and CFO confirmation. |
| The board-reported reduction in monthly burn from ₹46 lakh to ₹44 lakh is an observed change, but its cause is not established. | Board_Update_Apr-Jun_2026.pdf and Board_Update_Jul-Sep_2026.pdf. | High for reported values; low for the cause. | Monthly financial statements and cash-flow reconciliation. |
| The two backend hiring roles were actively pursued before the later hiring pause. | GL_Export_Apr-Sep_2026.xlsx (30-Jun recruitment advance); T2_CFO_Call.docx; Board_Update_Jul-Sep_2026.pdf. | High. | Hiring correspondence, invoices and updated hiring decisions. |
| The September summit incurred recorded venue/AV and catering expenses totalling approximately ₹10.03 lakh. | GL_Export_Apr-Sep_2026.xlsx (29-Aug and 3-Sep entries). | High for recorded ledger entries; actual final event cost needs invoice reconciliation. | Original invoices, payment records and expense adjustments. |
| Rahul Verma's February payroll may have been incorrectly prorated. | Employee_Master.xlsx (joining date 3-Feb-2026); Payroll_Register_Jan-Mar_2026.xlsx (28 payable days); emails 01.eml, 02.eml and 03.eml. | High that the record warrants investigation; overpayment is unconfirmed. | Payroll policy, corrected register, adjustment records and Fatima's investigation outcome. |

### Data interpretation rules

1. Treat board updates and system exports as stronger evidence than machine-generated transcripts, while still checking their dates and limitations.
2. Do not silently correct conflicting transcript figures.
3. Do not treat an expense-only general ledger as proof of total company burn or ARR.
4. Distinguish recorded expenses from final reconciled costs.
5. Do not label Rahul's payroll discrepancy a confirmed overpayment without verifying the payroll policy and subsequent adjustments.
6. Keep individual salary information restricted. CEO-facing payroll responses

## Day 2 — HR and Employee Risk Assumptions

1. Engineering pulse decline is treated as a warning signal, not proof of employee dissatisfaction or its cause.
2. The latest Engineering pulse score is 3.1, with 4 responses from a team of 5.
3. The pause of REQ-014 and REQ-015 is confirmed. Its impact on workload is plausible but not independently measured.
4. Siddharth Mehta's resignation and stated reasons are confirmed by his resignation letter.
5. Siddharth's departure creates a potential Marketing knowledge-transfer and launch-continuity risk. The actual impact remains to be assessed.
6. Attrition described as "about twelve" is ambiguous and excluded from quantitative reporting.
7. Claims about 22 open roles, six lost roles, and offer acceptance in the 50s are unverified.
8. Individual pulse comments and the identity of the unnamed engineer must not be exposed.
9. Small-team survey scores are displayed only in aggregate, with response counts and appropriate uncertainty.
10. Risk rankings are provisional and must be updated when additional evidence arrives.


## Day 3 — Engineering, Marketing and Organisational Change Assumptions

1. The Jira Versions sheet is treated as the authoritative available record for the Atlas GA release date. It records a change from 15 September 2026 to 15 December 2026 on 2 September 2026 by Vikram. This does not establish the reason for the change.

2. The 27 unresolved Jira issues (19 To Do and 8 In Progress) represent outstanding work in the Atlas GA version. They are not automatically classified as GA blockers.

3. The three August SEV1 routing-api incidents are confirmed by the incident register. Their severity and listed responders are established, but their root causes and total engineering effort are not.

4. The T5 transcript's description of Atlas as on track is not used to override the formal Jira release date.

5. The Engineering hiring pause, incident history and release-date revision together indicate delivery and reliability pressure. The evidence does not prove that the hiring pause caused the delay or incidents.

6. The Atlas launch kit had several prepared components, but the website page was unpublished and the press note remained a draft. A completed launch kit must not be treated as proof of complete launch readiness.

7. Siddharth's departure is confirmed by his resignation letter, but its direct effect on launch execution has not been established.

8. The incident register and on-call rota use both "Sneha" and "Snehal". These names must remain separate until an authoritative employee record confirms whether they refer to the same person.

9. Git commit counts are not treated as measures of productivity, working hours, overtime or individual workload.

10. The September SRE contractor invoice confirms a recorded retainer of ₹1,20,000 before tax. It does not independently establish a budget overrun or the contractor's identity in relation to the names in the incident and rota records.

11. Priya's request to discuss Atlas ownership is a signal that ownership may need clarification. The reason for the request and any subsequent decision remain unknown.

12. The T6b voice note indicates a planned Marketing reporting change to a new CRO, but its effective date is uncertain. Current reporting relationships must not be changed based only on this transcript.

13. The identity of the new CRO, final approval status and exact effective date are unknown.

### Day 3 confidence and evidence rules

- Prefer structured Jira and incident records over optimistic or incomplete transcript statements when reporting formal dates and incident counts.
- Preserve source dates and distinguish event dates from document or export dates.
- Do not infer individual workload from commit counts, on-call assignments or incident ownership alone.
- Do not merge employee identities based on similar names.
- Do not claim causal relationships between hiring decisions, incidents, employee departures and delivery delays without direct evidence.
- Treat the new CRO reporting change as a future organisational scenario until confirmed.
