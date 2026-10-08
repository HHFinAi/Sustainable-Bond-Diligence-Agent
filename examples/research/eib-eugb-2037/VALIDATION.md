# Validation and reproducibility

Validated with Python 3 using only standard-library modules and the Linux system IANA timezone database for Europe/Paris. There is no network dependency, package installation, market-data feed or trading connection.

```bash
python3 calculate.py
python3 calculate.py --check
```

The first command writes nine model outputs. The second recomputes and compares their full contents without modifying them. `results.json` stores the SHA-256 hash of `inputs.json`; `holding-period-results.json` hashes the separate dated inputs and quote-request packet.

The following checks address substantive arithmetic risks:

- Cash-flow count, maturity, principal sum and the 36-day assumed short stub reconcile. The alternative long-first-coupon schedule contains the same undiscounted coupons and principal at different dates.
- Bisection reconstructs the provisional historical price to within `1e-10` per 100.
- Analytical modified duration and convexity agree with symmetric finite-difference derivatives; tolerances are `1e-6` years and `1e-4` years² respectively.
- A separate zero-coupon identity checks discounting and risk formulas against closed-form values.
- Price falls when yield rises, convexity is positive, and modified duration is below the final payment time.
- The generated CSV/JSON files reproduce exactly on the validation runtime.

Observed base result: price **99.627**, annual yield **3.163016%**, modified duration **9.937719**, convexity **119.013328**, DV01 **EUR 990.065 per EUR 1 million face**. Price reconstruction error was below `2e-13`. These figures depend on the stated schedule and provisional price evidence.

The dated extension adds substantive checks in `tests/test_eib_case.py`:

- Independently counted accrued-interest days and the coupon-date reset; clean plus accrued equals dirty.
- Flat continuous zero-curve discounting agrees with a separate dated exponential sum; a known z-spread is recovered by the solver. A flat curve produces zero static-versus-forward roll-down.
- Exact coupon receipt, reinvestment from each payment date, entry/exit costs and the entire holding-period P&L reconcile independently.
- A flat rate shock and a common EIB spread shock have equal price effects when equal in size, with different attribution. A slope shock remains a separate scenario.
- Identical instruments with identical costs give zero relative P&L under flat and nonparallel curve moves. Initial DV01 matching and the signed funding balance are tested.
- The entry hurdle solves net relative P&L to zero, with negative P&L one bp below the required terminal greenium and positive P&L one bp above.
- Historical quote controls require the exact cutoff date in Europe/Paris, reject older stale packets as well as hindsight, cap the finite positive pair tolerance at 60 seconds, and reject missing or crossed sides, unmatched timestamps/settlements, missing timezone, non-EUR currency, zero size and nonfinite prices. Separately unverified pricing terms also block quote valuation. The checked-in null packet remains `NEEDS_DATA` and generates no entry recommendation.
- Curve extrapolation and matured-settlement accrual are rejected.

Run these checks from the repository root with `python3 -m unittest discover -s tests -p test_eib_case.py -v`. The original source-study fixtures remain untouched. The dated scenario model is not a market-data backtest or independently validated pricing library.

The credit stress uses EUR million consistently. Own funds reconcile to `22,190.715 + 58,519.222 + 2,891.475 = 83,601.412` from the standalone statutory balance sheet. The loan-at-cost denominator is the auditor's EUR 437,865 million population. Neither the disbursed-loan headline nor Group IFRS equity is substituted.

Source-review checks distinguish the October evidence cut from the April model date, issuer commentary from independent prices, later exchange screens from historical observations, and the future-issue pre-issuance annex from the April bond's original factsheet.

**Scope:** these checks establish arithmetic and internal consistency. They do not verify legal terms, executable prices, impact attribution, independent model validation or institutional approval. The script is a standalone analysis artifact. It is not an approved runtime calculation, does not import results into workflow state, and cannot clear a research gate. No human reviewer or approved status is recorded.

The original generated source-study packet and `NEEDS_DATA` fixtures remain unchanged. No results from after 16 October 2025 are used to claim subsequent investment performance. The 2027 exit is a hypothetical future horizon, not an observed outcome. Historical primary daily-sheet notations are excluded from entry inputs because their execution and settlement conventions are unresolved. Retrieval status is recorded in `sources.json` and open material gaps in `evidence-gaps.json`.
