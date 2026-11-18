# Transcript Notes — Veloxa Technologies

## 1. Company headcount

- **Transcript:** T1 CEO kickoff mentions approximately "one-eighty, give or take."
- **Evidence:** Employee_Master.xlsx contains 19 employee records. Board updates also report a team size of 19.
- **Assessment:** Likely a transcription error, possibly "eighteen." However, the transcript cannot be silently corrected.
- **Confidence:** High that the transcript conflicts with the exports; exact intended number remains uncertain.

## 2. ARR discrepancy

- **Transcript:** CEO mentions approximately ₹42–45 crore. CFO mentions ARR of 48 at the start of the financial year, but the unit is unclear.
- **Evidence:** Board updates report ₹5.8 crore for Apr–Jun 2026 and ₹6.1 crore for Jul–Sep 2026.
- **Assessment:** Material unresolved discrepancy. The general ledger is an expense ledger and cannot independently verify ARR.
- **Confidence:** High that the sources conflict; actual ARR requires clarification.

## 3. Monthly burn discrepancy

- **Transcript:** CFO mentions ₹2.2–2.5 lakh per month. CEO mentions 2.2 without a clear unit.
- **Evidence:** Board update reports monthly burn of ₹46 lakh for Apr–Jun and ₹44 lakh for Jul–Sep. GL records monthly payroll of ₹31.75 lakh alone.
- **Assessment:** CFO transcript figure is inconsistent with recorded payroll if interpreted as total monthly burn. A transcription or unit error is possible.
- **Confidence:** High that the transcript figure is unreliable as a total burn figure; exact burn requires full financial reconciliation.

## 4. Atlas launch timeline

- **Transcript:** CEO expresses concern that routing engine version 3 may not launch by the promised festive-season timeline.
- **Evidence:** Jul–Sep board update says general availability was moved to accommodate unplanned reliability work.
- **Assessment:** Reliability work affected the launch timeline. This is corroborated by the board update.
- **Confidence:** High.

## 5. Backend hiring

- **Transcript:** CFO mentions two backend roles.
- **Evidence:** GL records a ₹177,000 recruitment search-fee advance for two backend roles on 30 June. Jul–Sep board update subsequently reports hiring paused.
- **Assessment:** Hiring activity is supported, followed by a later hiring pause. These events may reflect a change in decision over

## Day 2 — T3 Head of People and T6a CEO Voice Note

### T3: Head of People Call

- Engineering pulse decline is corroborated by the Pulse Survey and Deepa's email dated 29 September 2026.
- Engineering's score declined from 3.9 to 3.1 in the available quarterly results. The latest result has 4 responses from a team of 5.
- Deepa explicitly stated that the Engineering team is too small to share individual survey comments. Raw comments must remain hidden.
- REQ-014 and REQ-015 were paused on 12 August 2026 by Meera pending the funding round. Vikram acknowledged that the team would absorb the work.
- Siddharth Mehta's resignation is confirmed by his letter dated 15 September 2026. His last working day was 31 October 2026.
- Siddharth cited unclear launch timelines and work not reaching customers as reasons for seeking another role.
- T3's statements about 22 open roles, six lost roles, offer acceptance in the 50s, and attrition of "about twelve" remain unverified or ambiguous.
- The unnamed engineer mentioned by Deepa must not be identified through inference.
- The transcript contains conflicting statements about when manager training began. Do not treat either date as confirmed.

### T6a: CEO Voice Note

- CEO requests a proactive cockpit that displays the top three things requiring attention when opened.
- Product decision: provide a ranked top-three risk view without requiring the CEO to submit a question.
- Each risk should include supporting evidence, confidence, business impact, and recommended next action.
- The cockpit must distinguish verified facts from assumptions and explicitly show when evidence is insufficient.

### Evidence and Privacy Decisions

- Use aggregate pulse scores for small teams; do not expose individual survey comments.
- Do not identify the unnamed engineer.
- Do not present ambiguous attrition or hiring figures as established facts.
- Treat the Engineering workload/capacity concern and Marketing handover concern as evidence-backed risks, not proven causal conclusions.


## Day 3 — T4 Head of Marketing, T5 VP Engineering and T6b CEO Voice Note

### T4: Head of Marketing Call

- Nikhil described the September summit as a strong pipeline quarter, but this is a transcript claim and has not been independently validated against campaign or CRM data.
- Nikhil mentioned marketing spend of "one point eight"; the unit and reporting period are unclear. Do not treat this as a verified financial figure.
- Nikhil said the Atlas v3 launch kit had been ready since July and was waiting for an Engineering launch date.
- Email dated 22 July from Siddharth confirms that the launch materials were prepared and a date was awaited from Engineering.
- The Atlas Launch Kit document, dated 21 July, lists the sales deck, website page and customer email sequence as ready. The website page was unpublished, the press note was still a draft, and the launch date was TBC.
- The T4 transcript says Marketing may report to the new CRO, but does not establish an approved effective date or confirmed reporting change.
- The backfill owner for Siddharth's role remains unassigned in the transcript.

### T5: VP Engineering Call

- Vikram described Atlas v3 as on track but needing a possible buffer. This statement conflicts with the formal Jira release record, which shows the GA date changed from 15 September to 15 December 2026 on 2 September.
- The Jira export contains 62 issues: 35 Done, 8 In Progress and 19 To Do. There are 27 unresolved issues representing 115 story points.
- These unresolved issues are associated with the Atlas GA version, but the export does not establish that every unresolved issue is a GA blocker.
- The incident register confirms three August SEV1 incidents affecting routing-api: INC-201, INC-203 and INC-205. All three list Sneha as responder.
- Email dated 24 August from Sneha states that the third SEV1 incident that month led to pausing Atlas performance tickets to stabilise routing-api.
- The on-call rota contains both Sneha and Snehal. Their identities must not be merged without corroborating evidence.
- The rota shows changing primary and secondary assignments, but does not establish individual working hours or total workload.
- The invoice for September confirms a monthly on-call SRE support retainer of ₹1,20,000 before tax. It does not establish a cost overrun or the contractor's identity in relation to Sneha or Snehal.
- The 1 September email from Priya asks Vikram to discuss Atlas ownership. The reason and outcome are unknown.
- The transcript has an audio gap from approximately 11:20 to 15:30. Do not infer what was discussed during that period.
- Git commit counts are not a reliable measure of individual productivity, working hours or workload.

### T6b: CEO Voice Note

- CEO says Marketing will report to the new CRO, but gives two possible timings: next month or the month after.
- Treat this as a planned organisational change with an uncertain effective date, not as an already completed reporting change.
- The cockpit should support changes to reporting relationships without overwriting historical reporting information.
- The new CRO's identity, exact effective date and final approval status are not established by this voice note.

### Day 3 Evidence and Reconciliation Decisions

- Prefer the Jira release record over the optimistic T5 transcript when reporting the formal Atlas GA date.
- Report the revised GA date as 15 December 2026, changed on 2 September 2026 by Vikram.
- Use the incident register to substantiate the three August SEV1 routing-api incidents.
- Distinguish confirmed launch-kit components from full launch readiness. The website remained unpublished and the press note was a draft.
- Do not claim that Siddharth's departure caused the Atlas delay. The available evidence does not establish that causal link.
- Preserve the Sneha/Snehal identity discrepancy until independently resolved.
- Do not infer employee productivity, overtime or individual workload from Git commit counts or on-call assignments alone.
- Do not update current reporting relationships based solely on the uncertain T6b timing.
