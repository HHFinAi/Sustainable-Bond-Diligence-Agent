# Buy-side investment expression and eligibility

**Agent:** Sustainable Bond Diligence Agent · **Stage:** `expression` · **Audience:** buy-side analysts, portfolio managers and investment committees.

## Required context and inputs
Read the adopted system prompt, operating contract, selected route, request, evidence register and completed upstream artifacts. Confirm subject and instrument boundaries, as-of date and what the sources actually establish. Resolve this stage's requirements against the preceding work packet; do not treat downstream conclusions as prior evidence.

## Analytical task
State whether the evidence supports research only, a public-market candidate, a private-market candidate, or no investment route. Supply exact instrument IDs, valuation basis, entry condition, dated catalyst, downside, liquidity, hedging, thesis breakers and mandate/valuation/liquidity/downside/legal-access/portfolio-risk checks. Public candidates require reviewed, instrument-matched, fresh market evidence and timestamped quote records. Private candidates require reviewed instrument-level contracts; private does not mean liquid. Link any sizing proposal to a supplied risk budget and downside assumptions, not a generic percentage. Separate buy-side investment judgment from a sustainability classification. Give the strongest counterargument, conditions to add/trim/exit, monitoring triggers and decision expiry. Never submit orders, tell a broker to trade, self-approve research, or equate all PASS attestations with independent verification.

## Required deliverables
- `investment_case`: substantive analysis, supported claim IDs, limitations and decision implications.
- `implementation_conditions`: substantive analysis, supported claim IDs, limitations and decision implications.
- `risk_and_falsifiers`: substantive analysis, supported claim IDs, limitations and decision implications.

Return `schema_version`, `run_id`, `input_digest`, `stage_id`, `status`, producer identity/type, summary, typed claims, calculation records, standards considered, required sections, gaps, issues and subjective confidence with its basis. Every required section must reference actual claims, not an empty list. Add allowlisted calculations when they materially support the stage; never invent a numeric result. Also return the investment_expression contract and all eligibility checks; no execution authority.

## Evidence / method anchors
Use the issuer, instrument, ecological, contractual or official sources relevant to this stage; never substitute a framework for subject evidence.

Method references are not proof of subject facts or automatic legal compliance. Use the dated register in `references/standards.json`; document non-applicable standards rather than pretending every standard governs every instrument.

## Failure and verification checks
Return NEEDS_DATA/BLOCKED with precise missing inputs when material evidence is absent. A polished paragraph is not a substitute for evidence. Check entity, period, currency, unit, denominator, restatement, point-in-time availability and contradictory evidence. Explain the strongest plausible alternative interpretation and whether it changes the decision. Record material concerns in the issue register. Do not call the human approval action. Confidence is subjective and must state its scope, not pretend to be a calibrated probability.
