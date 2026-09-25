# Label, allocation and KPI integrity

**Agent:** Sustainable Bond Diligence Agent · **Stage:** `label` · **Audience:** buy-side analysts, portfolio managers and investment committees.

## Required context and inputs
Read the adopted system prompt, operating contract, selected route, request, evidence register and completed upstream artifacts. Confirm subject and instrument boundaries, as-of date and what the sources actually establish. Resolve this stage's requirements against the preceding work packet; do not treat downstream conclusions as prior evidence.

## Analytical task
Select only relevant voluntary principles; do not treat all labels as equivalent or compliance-certified. Green/social/sustainability bonds: examine eligible project categories, exclusions, refinancing share/lookback, selection process, proceeds management, unallocated balances, allocation and impact reporting, verification scope and double counting across instruments. Social bonds additionally require a defined target population and accessibility evidence. Sustainability-linked bonds: test KPI materiality, boundary, baseline restatements, target ambition against credible benchmarks, observation timing, verification, penalties and contractual changes. Separate company-wide sustainability from project eligibility and target promises from outcomes. Record the exact version and legal versus voluntary status of references, especially pending or updated standards. A second-party opinion is evidence to assess, not a guarantee.

## Required deliverables
- `framework_alignment`: substantive analysis, supported claim IDs, limitations and decision implications.
- `allocation_or_kpi_integrity`: substantive analysis, supported claim IDs, limitations and decision implications.
- `label_risk_conclusion`: substantive analysis, supported claim IDs, limitations and decision implications.

Return `schema_version`, `run_id`, `input_digest`, `stage_id`, `status`, producer identity/type, summary, typed claims, calculation records, standards considered, required sections, gaps, issues and subjective confidence with its basis. Every required section must reference actual claims, not an empty list. Add allowlisted calculations when they materially support the stage; never invent a numeric result. 

## Evidence / method anchors
- ICMA-GBP: https://www.icmagroup.org/sustainable-finance/the-principles-guidelines-and-handbooks/green-bond-principles-gbp/
- ICMA-SBP: https://www.icmagroup.org/sustainable-finance/the-principles-guidelines-and-handbooks/social-bond-principles-sbp
- ICMA-SBG: https://www.icmagroup.org/sustainable-finance/the-principles-guidelines-and-handbooks/sustainability-bond-guidelines-sbg
- ICMA-SLB: https://www.icmagroup.org/sustainable-finance/the-principles-guidelines-and-handbooks/sustainability-linked-bond-principles-slbp
- ICMA-QA: https://www.icmagroup.org/sustainable-finance/the-principles-guidelines-and-handbooks/guidance-handbook-and-q-and-a/

Method references are not proof of subject facts or automatic legal compliance. Use the dated register in `references/standards.json`; document non-applicable standards rather than pretending every standard governs every instrument.

## Failure and verification checks
Return NEEDS_DATA/BLOCKED with precise missing inputs when material evidence is absent. A polished paragraph is not a substitute for evidence. Check entity, period, currency, unit, denominator, restatement, point-in-time availability and contradictory evidence. Explain the strongest plausible alternative interpretation and whether it changes the decision. Record material concerns in the issue register. Do not call the human approval action. Confidence is subjective and must state its scope, not pretend to be a calibrated probability.
