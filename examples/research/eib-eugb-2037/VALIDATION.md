# Validation and reproducibility

Validated with Python 3 using only standard-library modules. There is no network dependency, package installation, market-data feed or trading connection.

```bash
python3 calculate.py
python3 calculate.py --check
```

The first command writes five model outputs. The second recomputes and compares their full contents without modifying them. `results.json` also stores the SHA-256 hash of `inputs.json`.

The following checks address substantive arithmetic risks:

- Cash-flow count, maturity, principal sum and the 36-day assumed short stub reconcile. The alternative long-first-coupon schedule contains the same undiscounted coupons and principal at different dates.
- Bisection reconstructs the provisional historical price to within `1e-10` per 100.
- Analytical modified duration and convexity agree with symmetric finite-difference derivatives; tolerances are `1e-6` years and `1e-4` years² respectively.
- A separate zero-coupon identity checks discounting and risk formulas against closed-form values.
- Price falls when yield rises, convexity is positive, and modified duration is below the final payment time.
- The generated CSV/JSON files reproduce exactly on the validation runtime.

Observed base result: price **99.627**, annual yield **3.163016%**, modified duration **9.937719**, convexity **119.013328**, DV01 **EUR 990.065 per EUR 1 million face**. Price reconstruction error was below `2e-13`. These figures depend on the stated schedule and provisional price evidence.

The credit stress uses EUR million consistently. Own funds reconcile to `22,190.715 + 58,519.222 + 2,891.475 = 83,601.412` from the standalone statutory balance sheet. The loan-at-cost denominator is the auditor's EUR 437,865 million population. Neither the disbursed-loan headline nor Group IFRS equity is substituted.

Source-review checks distinguish the October evidence cut from the April model date, issuer commentary from independent prices, later exchange screens from historical observations, and the future-issue pre-issuance annex from the April bond's original factsheet.

**Scope:** these checks establish arithmetic and internal consistency. They do not verify legal terms, executable prices, impact attribution, independent model validation or institutional approval. The script is a standalone analysis artifact. It is not an approved runtime calculation, does not import results into workflow state, and cannot clear a research gate. No human reviewer or approved status is recorded.

The original generated source-study packet and `NEEDS_DATA` fixtures remain unchanged. No results from after 16 October 2025 are used to claim subsequent investment performance.
