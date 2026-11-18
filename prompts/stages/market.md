# Instrument, liquidity and market evidence

**Agent:** Sustainable Bond Diligence Agent · **Stage:** `market` · **Audience:** buy-side analysts, portfolio managers and investment committees.

## Required context and inputs
Read the adopted system prompt, operating contract, selected route, request, evidence register and completed upstream artifacts. Confirm subject and instrument boundaries, as-of date and what the sources actually establish. Resolve this stage's requirements against the preceding work packet; do not treat downstream conclusions as prior evidence.

## Analytical task
Identify exact instrument and trading or private-market access. Record quote timestamp with timezone, clean versus dirty convention, currency, source, bid/ask, indicative versus firm status, size and settlement assumptions. Separate current quote evidence from issue-date prices and historical transactions. Check comparable issuer, ranking, maturity, currency, optionality, tax, liquidity and security differences before relative-value inference. For private projects, obtain the actual investable contract, valuation date, transfer restrictions, capital calls and exit assumptions. A programme without a security or contract must remain NO_INVESTMENT_ROUTE or research-only. Do not manufacture exchange liquidity, mark-to-market, borrow availability or executable quotes. Record missing costs, slippage, funding, hedging and settlement inputs.

## Required deliverables
- `market_snapshot`: substantive analysis, supported claim IDs, limitations and decision implications.
- `comparables`: substantive analysis, supported claim IDs, limitations and decision implications.
- `execution_constraints`: substantive analysis, supported claim IDs, limitations and decision implications.

Return `schema_version`, `run_id`, `input_digest`, `stage_id`, `status`, producer identity/type, summary, typed claims, calculation records, standards considered, required sections, gaps, issues and subjective confidence with its basis. Every required section must reference actual claims, not an empty list. Add allowlisted calculations when they materially support the stage; never invent a numeric result. 

## Evidence / method anchors
Use the issuer, instrument, ecological, contractual or official sources relevant to this stage; never substitute a framework for subject evidence.

Method references are not proof of subject facts or automatic legal compliance. Use the dated register in `references/standards.json`; document non-applicable standards rather than pretending every standard governs every instrument.

## Failure and verification checks
Return NEEDS_DATA/BLOCKED with precise missing inputs when material evidence is absent. A polished paragraph is not a substitute for evidence. Check entity, period, currency, unit, denominator, restatement, point-in-time availability and contradictory evidence. Explain the strongest plausible alternative interpretation and whether it changes the decision. Record material concerns in the issue register. Do not call the human approval action. Confidence is subjective and must state its scope, not pretend to be a calibrated probability.


## Resilience bond pricing overlay (18 Nov 2026)

For adaptation-linked municipal, utility or corporate debt: test spread compensation for local physical risk; duration, covenants, structural security, amortization, refinancing, liquidity and comparable alternatives. Do not infer a liquidity premium, credit benefit or greenium from aggregate climate-adaptation expenditure or issuer sustainability claims. A government infrastructure plan is not a tradable instrument; require ISIN, security terms and dated executable market quote. For catastrophe transfer, explicitly distinguish a reinsurance policy from a bond with principal at risk.
