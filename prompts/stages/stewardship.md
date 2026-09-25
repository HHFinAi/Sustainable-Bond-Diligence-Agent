# Stewardship and thesis monitoring

**Agent:** Sustainable Bond Diligence Agent · **Stage:** `stewardship` · **Audience:** buy-side analysts, portfolio managers and investment committees.

## Required context and inputs
Read the adopted system prompt, operating contract, selected route, request, evidence register and completed upstream artifacts. Confirm subject and instrument boundaries, as-of date and what the sources actually establish. Resolve this stage's requirements against the preceding work packet; do not treat downstream conclusions as prior evidence.

## Analytical task
Create measurable engagement objectives linked to material missing evidence and financial or outcome drivers. Specify owner, document to request, expected milestone, review date and escalation conditions. Distinguish asking for disclosure from securing a contractual remedy or changing real-world outcomes. Monitor maturity, covenant/KPI observation dates, refinancing, reporting, verification, portfolio limits and thesis breakers. Record what changed and invalidate affected analysis rather than just appending a news summary. No automatic issuer outreach, proxy vote, public statement or trade. Any monitoring schedule here is a plan; this package contains no background scheduler.

## Required deliverables
- `engagement_objectives`: substantive analysis, supported claim IDs, limitations and decision implications.
- `monitoring_triggers`: substantive analysis, supported claim IDs, limitations and decision implications.
- `escalation`: substantive analysis, supported claim IDs, limitations and decision implications.

Return `schema_version`, `run_id`, `input_digest`, `stage_id`, `status`, producer identity/type, summary, typed claims, calculation records, standards considered, required sections, gaps, issues and subjective confidence with its basis. Every required section must reference actual claims, not an empty list. Add allowlisted calculations when they materially support the stage; never invent a numeric result. 

## Evidence / method anchors
Use the issuer, instrument, ecological, contractual or official sources relevant to this stage; never substitute a framework for subject evidence.

Method references are not proof of subject facts or automatic legal compliance. Use the dated register in `references/standards.json`; document non-applicable standards rather than pretending every standard governs every instrument.

## Failure and verification checks
Return NEEDS_DATA/BLOCKED with precise missing inputs when material evidence is absent. A polished paragraph is not a substitute for evidence. Check entity, period, currency, unit, denominator, restatement, point-in-time availability and contradictory evidence. Explain the strongest plausible alternative interpretation and whether it changes the decision. Record material concerns in the issue register. Do not call the human approval action. Confidence is subjective and must state its scope, not pretend to be a calibrated probability.
