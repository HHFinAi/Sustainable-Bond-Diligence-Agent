# EIB EuGB 2037 — historical investment research case

**Research conclusion: WATCH.** A credible green allocation process and substantial issuer buffers support further diligence; the available evidence does not establish a tradable relative-value opportunity.

[Read the research memo](MEMO.md) · [Inspect the inputs](inputs.json) · [Review the evidence ledger](sources.csv) · [Review assumptions](assumptions.csv) · [Inspect calculated results](results.json)

The real instrument is EIB's EUR 3 billion, 3.125% European Green Bond due 15 May 2037, ISIN **EU000A3K4EG9**. This case reconstructs a review with an information cut of **16 October 2025**. It was prepared retrospectively on **3 October 2026**. The dated primary sources, a financial-credit assessment, label and impact judgments, a comparator screen, risk calculations, and explicit decision thresholds are included.

The pricing illustration uses an **April 2025 original-settlement anchor**, with an assumed coupon schedule. It is not an October 2025 market valuation. Exact issue documentation and historical executable comparator quotes remain material gaps. This is a standalone research sample, not a completed runtime workflow or approved recommendation.

Run with Python 3.10+; no packages or network calls are needed:

```bash
python3 examples/research/eib-eugb-2037/calculate.py
python3 examples/research/eib-eugb-2037/calculate.py --check
```

The script writes `cashflows.csv`, `sensitivity.csv`, `relative-value.csv`, `credit-stress.csv`, and `results.json`. See [validation and scope](VALIDATION.md). The calculations distinguish sourced data, provisional evidence, assumptions, and outputs. Assumptions remain assumptions even when their numerical effect is small.

The original [source-study packet](../../reports/source-study-packet.md) remains a useful `NEEDS_DATA` control. This separate case adds completed, bounded analysis without changing that packet, manufacturing historical workflow state, or asserting human approval.
