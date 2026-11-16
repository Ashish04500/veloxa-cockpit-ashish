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