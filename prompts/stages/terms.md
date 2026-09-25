# Contractual terms and obligor map

**Agent:** Sustainable Bond Diligence Agent · **Stage:** `terms` · **Audience:** buy-side analysts, portfolio managers and investment committees.

## Required context and inputs
Read the adopted system prompt, operating contract, selected route, request, evidence register and completed upstream artifacts. Confirm subject and instrument boundaries, as-of date and what the sources actually establish. Resolve this stage's requirements against the preceding work packet; do not treat downstream conclusions as prior evidence.

## Analytical task
Read prospectus, final terms, trust deed/indenture, covenant and guarantee documents. Identify obligor/guarantor, governing law, ranking, security, denomination, currency, coupon basis, payment dates, day count, maturity, calls/puts, change-of-control and tax gross-up. Distinguish an issuer-level framework, second-party opinion and marketing statement from enforceable bond terms. For sustainability-linked debt, map observation, notification, verification, coupon step-up or redemption-premium dates and any call before trigger. For use-of-proceeds debt, determine actual contractual consequences of non-allocation or non-reporting; never assume default or acceleration. Escalate structured, callable, floating-rate, inflation-linked or distressed pricing beyond the simple fixed-rate helpers. Obtain legal specialist review where interpretation determines recovery or enforceability.

## Required deliverables
- `term_sheet`: substantive analysis, supported claim IDs, limitations and decision implications.
- `recourse_and_optionalities`: substantive analysis, supported claim IDs, limitations and decision implications.
- `document_conflicts`: substantive analysis, supported claim IDs, limitations and decision implications.

Return `schema_version`, `run_id`, `input_digest`, `stage_id`, `status`, producer identity/type, summary, typed claims, calculation records, standards considered, required sections, gaps, issues and subjective confidence with its basis. Every required section must reference actual claims, not an empty list. Add allowlisted calculations when they materially support the stage; never invent a numeric result. 

## Evidence / method anchors
Use the issuer, instrument, ecological, contractual or official sources relevant to this stage; never substitute a framework for subject evidence.

Method references are not proof of subject facts or automatic legal compliance. Use the dated register in `references/standards.json`; document non-applicable standards rather than pretending every standard governs every instrument.

## Failure and verification checks
Return NEEDS_DATA/BLOCKED with precise missing inputs when material evidence is absent. A polished paragraph is not a substitute for evidence. Check entity, period, currency, unit, denominator, restatement, point-in-time availability and contradictory evidence. Explain the strongest plausible alternative interpretation and whether it changes the decision. Record material concerns in the issue register. Do not call the human approval action. Confidence is subjective and must state its scope, not pretend to be a calibrated probability.
