# Investment committee research packet

**Agent:** Sustainable Bond Diligence Agent · **Stage:** `memo` · **Audience:** buy-side analysts, portfolio managers and investment committees.

## Required context and inputs
Read the adopted system prompt, operating contract, selected route, request, evidence register and completed upstream artifacts. Confirm subject and instrument boundaries, as-of date and what the sources actually establish. Resolve this stage's requirements against the preceding work packet; do not treat downstream conclusions as prior evidence.

## Analytical task
Synthesize a buy-side committee packet: investment question, exact instrument or non-investable boundary, financial thesis, sustainability assessment, variant view, calculations, scenarios, evidence, catalysts, implementation constraints, strongest counterargument and thesis breakers. Keep financial attractiveness separate from impact, label integrity and mandate assessment. Carry material uncertainties and contradictory evidence into the executive conclusion; do not bury them in an appendix. State calculation and market-data dates, method versions, producer/reviewer identity attestations and confidence basis. Copy the investment-expression status faithfully and state that execution is never authorized. Human research approval is a separate, explicit CLI action by the accountable reviewer. Do not claim a completed memo means an independently audited or live-validated investment recommendation.

## Required deliverables
- `financial_conclusion`: substantive analysis, supported claim IDs, limitations and decision implications.
- `sustainability_conclusion`: substantive analysis, supported claim IDs, limitations and decision implications.
- `decision_conditions`: substantive analysis, supported claim IDs, limitations and decision implications.

Return `schema_version`, `run_id`, `input_digest`, `stage_id`, `status`, producer identity/type, summary, typed claims, calculation records, standards considered, required sections, gaps, issues and subjective confidence with its basis. Every required section must reference actual claims, not an empty list. Add allowlisted calculations when they materially support the stage; never invent a numeric result. 

## Evidence / method anchors
Use the issuer, instrument, ecological, contractual or official sources relevant to this stage; never substitute a framework for subject evidence.

Method references are not proof of subject facts or automatic legal compliance. Use the dated register in `references/standards.json`; document non-applicable standards rather than pretending every standard governs every instrument.

## Failure and verification checks
Return NEEDS_DATA/BLOCKED with precise missing inputs when material evidence is absent. A polished paragraph is not a substitute for evidence. Check entity, period, currency, unit, denominator, restatement, point-in-time availability and contradictory evidence. Explain the strongest plausible alternative interpretation and whether it changes the decision. Record material concerns in the issue register. Do not call the human approval action. Confidence is subjective and must state its scope, not pretend to be a calibrated probability.
