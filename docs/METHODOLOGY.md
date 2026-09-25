# Methodology, units and model boundaries

## Model posture
All functions are transparent, deterministic arithmetic under caller-supplied assumptions. They do not estimate missing values, fit probabilities or validate the economic model. A number can pass unit and recomputation checks while its assumptions or causal interpretation remain wrong. Inspect `sf_agent/analytics.py` and the operation registry below.

Money uses one declared three-letter currency per calculation. FX conversions must be explicit and sourced. Percentages are decimal fractions unless a field explicitly says basis points. Scalar source metrics bind to their disclosed period, entity and unit. A series supplied as an assumption must have its period convention and underlying source work explained; the v0.1 schema does not independently reconcile a time-series spreadsheet. `scale` records explicit conversion arithmetic, but a reviewer must validate the declared units and factor.

Common helpers: `npv` uses cashflows[0] at time zero followed by annual periods; it is not XNPV and ignores irregular dates. `dscr` divides supplied cash available by positive debt service and does not normalize accounting definitions. `holding_period_return` uses consistent dirty-price money amounts, income, funding and transaction costs without annualizing or adding default probabilities. `scale` applies an explicit positive conversion factor; its semantics require human review.

## Standards maintenance
`references/standards.json` is a dated metadata register, not an embedded legal database or a substitute for the source text. Edition dates known only to the month are normalized to day 01 for indexing and must not be used as exact legal effective dates. Webpage update dates are distinguished from methodology editions. Reviewed references are checked as of September 24, 2026. Applicable adopted law, proposed reforms, voluntary guidance, reporting methodology and instrument contracts must remain separate. Reverify whenever material, before historical analysis and when the configured review age expires. The runtime blocks stale considered references at approval, but does not itself recheck a website.

## Financial and sustainability judgments
Make separate conclusions for financial attractiveness, sustainability/impact evidence and mandate compatibility. Use independent evidence for market prices, legal rights and outcomes. Report unassessed exposure and confidence limits rather than imputing zero. Document how uncertainty changes the investment decision; do not solve uncertainty by adding an unsupported discount or ESG score. “All checks pass” records an analyst's attestation and required inputs, not an independent suitability determination.

## Domain operation registry

## Bond-specific boundaries
`bond_price` and `bond_risk` handle a regular, fixed-rate, option-free schedule valued on a coupon date (zero accrued interest); face value and price use the declared currency. Coupons and yields are decimal annual rates, periodic compounding uses frequency 1, 2, 4 or 12, and only 1–600 whole payment periods are supported. Modified duration is in years; convexity in years squared; DV01 in currency per basis point. These are not OAS, yield-curve, default-intensity, settlement/day-count, callable, floating-rate or distressed-bond models. Obtain a validated pricing system for those cases.

`slb_stepup_pv` discounts the incremental coupon cash flows **conditional on** the contractual trigger occurring, from the supplied first to last payment period inclusive. It does not estimate the chance of failure, the credit damage associated with failure, contractual call exercise or net expected return. `greenium` is matched conventional spread minus labelled spread in basis points; positive means a tighter labelled spread. The function does not establish comparability. `allocation_coverage` is eligible allocation divided by net proceeds and rejects allocation above proceeds; refinancing, FX and double-counting adjustments remain human-reviewed.

| Operation | Input unit contract | Output unit/structure |
|---|---|---|
| `npv` | `cashflows: $money`, `annual_discount: decimal` | `$money` |
| `dscr` | `cash_available: $money`, `debt_service: $money` | `multiple` |
| `scale` | `value: $input_unit`, `factor: conversion_factor` | `$output_unit` |
| `holding_period_return` | `initial_dirty_price: $money`, `exit_dirty_price: $money`, `cash_income: $money`, `funding_cost: $money`, `transaction_cost: $money` | `decimal_return` |
| `bond_price` | `face: $money`, `annual_coupon: decimal`, `yield_to_maturity: decimal`, `years: years`, `frequency: payments_per_year` | `$money` |
| `bond_risk` | `face: $money`, `annual_coupon: decimal`, `yield_to_maturity: decimal`, `years: years`, `frequency: payments_per_year` | `bond_risk_metrics` |
| `slb_stepup_pv` | `face: $money`, `step_up_bps: basis_points`, `first_payment_period: period_index`, `last_payment_period: period_index`, `annual_discount: decimal`, `frequency: payments_per_year` | `$money` |
| `greenium` | `labelled_spread_bps: basis_points`, `matched_conventional_spread_bps: basis_points` | `basis_points` |
| `allocation_coverage` | `eligible_allocated: $money`, `net_proceeds: $money` | `decimal_fraction` |

`$money` resolves to the declared currency; `$outcome` resolves to the named outcome measurement unit. Compound `money_per_outcome` resolves to currency/outcome unit. Multi-output metric dictionaries have field-level meanings described above and in the implementation. Code validates input units and recomputed results, not the scientific or economic validity of those inputs.
