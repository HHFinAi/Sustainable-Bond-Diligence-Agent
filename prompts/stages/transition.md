# Transition credibility and lock-in

**Agent:** Sustainable Bond Diligence Agent · **Stage:** `transition` · **Audience:** buy-side analysts, portfolio managers and investment committees.

## Required context and inputs
Read the adopted system prompt, operating contract, selected route, request, evidence register and completed upstream artifacts. Confirm subject and instrument boundaries, as-of date and what the sources actually establish. Resolve this stage's requirements against the preceding work packet; do not treat downstream conclusions as prior evidence.

## Analytical task
Assess transition use of proceeds alongside issuer-level implementation, not a relabelled green checklist. Reconcile asset retirement, abatement technology, scope coverage, capital allocation, target pathways, governance and financing dependencies. Test alternatives, carbon lock-in, fossil expansion assumptions, technology readiness, energy/security dependencies and sensitivity to policy or demand shocks. Distinguish ICMA Climate Transition Bond guidance from legal taxonomy eligibility and from alignment to a chosen scenario. Attribute policy facts neutrally with dates; do not rank political actors or advocate policies. Explain cash-flow and credit implications of delay, stranded capex, demand shifts and uncertain funding. Unsupported feasibility or targets require explicit qualification, not a categorical transition endorsement.

## Required deliverables
- `transition_plan`: substantive analysis, supported claim IDs, limitations and decision implications.
- `capex_and_lock_in`: substantive analysis, supported claim IDs, limitations and decision implications.
- `implementation_dependencies`: substantive analysis, supported claim IDs, limitations and decision implications.

Return `schema_version`, `run_id`, `input_digest`, `stage_id`, `status`, producer identity/type, summary, typed claims, calculation records, standards considered, required sections, gaps, issues and subjective confidence with its basis. Every required section must reference actual claims, not an empty list. Add allowlisted calculations when they materially support the stage; never invent a numeric result. 

## Evidence / method anchors
- ICMA-CTB: https://www.icmagroup.org/sustainable-finance/the-principles-guidelines-and-handbooks/climate-transition-finance-handbook
- ICMA-QA: https://www.icmagroup.org/sustainable-finance/the-principles-guidelines-and-handbooks/guidance-handbook-and-q-and-a/

Method references are not proof of subject facts or automatic legal compliance. Use the dated register in `references/standards.json`; document non-applicable standards rather than pretending every standard governs every instrument.

## Failure and verification checks
Return NEEDS_DATA/BLOCKED with precise missing inputs when material evidence is absent. A polished paragraph is not a substitute for evidence. Check entity, period, currency, unit, denominator, restatement, point-in-time availability and contradictory evidence. Explain the strongest plausible alternative interpretation and whether it changes the decision. Record material concerns in the issue register. Do not call the human approval action. Confidence is subjective and must state its scope, not pretend to be a calibrated probability.
