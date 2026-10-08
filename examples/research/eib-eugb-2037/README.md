# EIB EuGB 2037 — historical investment research case

**Research conclusion: WATCH.** A credible green allocation process and substantial issuer buffers support further diligence; the available evidence does not establish a tradable relative-value opportunity.

[Read the research memo](MEMO.md) · [Dated relative-value results](holding-period-results.json) · [Entry hurdles](entry-hurdles.csv) · [Evidence gaps](evidence-gaps.json) · [Evidence ledger](sources.csv)

The real instrument is EIB's EUR 3 billion, 3.125% European Green Bond due 15 May 2037, ISIN **EU000A3K4EG9**. This case reconstructs a review with an information cut of **16 October 2025**. It was prepared retrospectively on **3 October 2026**. The dated primary sources, a financial-credit assessment, label and impact judgments, a comparator screen, risk calculations, and explicit decision thresholds are included.

The 8 October 2026 extension completes the **conditional dated two-bond model**: clean/dirty prices and accrued interest; explicit cash flows; curve-adjusted z-spreads; matching initial parallel DV01 with residual key-rate risk; dated coupon carry and reinvestment; static-curve roll-down; separate rate/slope and spread shocks; transaction costs; signed cash/funding balances; and a solved entry hurdle. The [inputs](holding-period-inputs.json) label all assumed curves, spreads, costs and unverified contract conventions.

At an assumed 5 bp green yield concession, the model needs a **7.795 bp terminal concession** to break even against the cost-inclusive DV01-matched conventional/cash benchmark. Unchanged concession produces **−23.39 bp relative return**. Neither number is an observed greenium or forecast. See the [scenario table](holding-period-scenarios.csv) and [memo](MEMO.md) for the cash-flow reconciliation.

The older pricing illustration retains its **April 2025 original-settlement anchor**, with an assumed coupon schedule. The dated extension assumes settlement on **20 October 2025** and exit on **20 October 2027**; it does not claim these were actual trades. Exact issue documentation and historical executable comparator quotes remain material gaps. This is a standalone research sample, not a completed runtime workflow or approved recommendation.

New [primary historical observations](historical-observations.json) were found in Quotrix's 4 September and 12 August 2025 daily sheets for both exact ISINs. They are zero-volume M price notations, with no verified clean/dirty or executable two-way convention. They are recorded separately and excluded from model entry prices. **Historical entry status remains NEEDS_DATA.**

Run with Python 3.10+ and a system IANA timezone database containing Europe/Paris (available on the validated Linux runtime); no network calls are needed:

```bash
python3 examples/research/eib-eugb-2037/calculate.py
python3 examples/research/eib-eugb-2037/calculate.py --check
```

The first command writes nine deterministic outputs, including `holding-period-results.json`, `dated-cashflows.csv`, `holding-period-scenarios.csv` and `entry-hurdles.csv`. `--check` only reads and compares the committed results. See [validation and scope](VALIDATION.md). The calculations distinguish sourced data, provisional evidence, assumptions, and outputs. Assumptions remain assumptions even when their numerical effect is small.

To inspect the missing-data response without writing files:

```bash
python3 examples/research/eib-eugb-2037/analyze_quotes.py \
  --quotes examples/research/eib-eugb-2037/quote-request.json
```

The [quote-request template](quote-request.json) has null observations. It produces `NEEDS_DATA` and null pricing. A private reviewed packet can supply timestamped bid/ask prices, sizes, settlement and locators; the tool then computes conditional clean/dirty and bid/ask/mid z-spreads. It requires both quotes on exactly 16 October 2025 in the Europe/Paris clock and caps their separation at 60 seconds. Earlier stale quotes, later quotes, invalid/widened tolerances, mismatched settlements, missing sides, crossed markets and zero size are rejected. Completeness does not authenticate the source or approve a trade. The default assumed contracts cannot be certified by marking the quote packet reviewed: pricing also requires reviewed issue-specific terms via `--inputs`. Replace the illustrative curve after review; keep licensed quote packets private.

The original [source-study packet](../../reports/source-study-packet.md) remains a useful `NEEDS_DATA` control. This separate case adds completed, bounded analysis without changing that packet, manufacturing historical workflow state, or asserting human approval.
