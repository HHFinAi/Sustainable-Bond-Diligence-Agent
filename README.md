# Sustainable Bond Research and Diligence

**Investment research by HHFinAi: underlying credit, contractual protections, sustainability claims and relative value.**

A credible label does not establish a good bond investment. What does the investor own, how is repayment supported, and is the entry price defensible?

## Start with the investment case

### EIB EuGB 2037 — credible label, unproven entry price

**Research assessment: WATCH.** The case separates issuer credit, allocation and impact evidence, contractual questions and the comparator screen. It does not treat a sustainability credential as a substitute for credit analysis or matched market evidence.

**Status:** historical real-bond research sample with an evidence cutoff of **16 October 2025**. It is not a live recommendation or an approved workflow packet. Exact issue documents and matched historical quotes remain material gaps.

The extension adds dated clean/dirty cash flows, carry, roll-down, curve/DV01 matching, funding and trading costs. At an assumed 5 bp entry premium, the unchanged-premium case loses **23.39 bp** relative to its matched comparator; the terminal premium must reach **7.795 bp** to break even under the stated assumptions. These are conditional calculations, not observed market returns.

The original **9.37% price decline for a +100 bp yield shock** remains a scoped sensitivity at a provisional original-settlement anchor. Primary historical zero-volume exchange markings are registered and excluded from executable entry prices.

[Read the investment memo](examples/research/eib-eugb-2037/MEMO.md) · [Inspect sources, assumptions and reproduction instructions](examples/research/eib-eugb-2037/README.md)

## Research judgment demonstrated

The case asks whether the evidence supports the investment, not merely whether the security has a sustainability label. It makes the distinction between a research conclusion and workflow approval explicit, preserves unresolved instrument and pricing questions, and supplies reproducible duration, convexity and yield-shock calculations.

The research record identifies the sources, assumptions and limits to review. It is not a claim of independent audit, client adoption, historical investment performance or authenticated human approval. [Selected research and portfolio standards](https://github.com/HHFinAi/HHFinAi).

## Research examples and control demonstrations

| Material | Purpose | Boundary |
|---|---|---|
| [EIB research sample](examples/research/eib-eugb-2037/MEMO.md) | Historical issuer, instrument and relative-value assessment | Material gaps remain; not a live trade |
| [Methodology-only source study](examples/reports/source-study-packet.md) | Shows how the workflow stops safely | Deliberately `NEEDS_DATA` |
| [Synthetic packet](examples/reports/synthetic-packet.md) | Exercises software and output structure | Fictional inputs; not completed diligence |

The source study remains unchanged. Publishing a standalone memo does not approve an incomplete workflow run.

## Workflow infrastructure

**Engine v0.1.0 · 13 specialist stages · 5 routes · Python 3.10+ target · Human review · No trade execution**

[Workflow](WORKFLOW.md) · [Prompts and skills](PROMPTS.md) · [Evidence trail](docs/AUDIT.md) · [Controls](docs/INSTITUTIONAL_QUALITY.md) · [Validation](docs/VALIDATION.md) · [FAQ](docs/FAQ.md)

The local engine freezes the request, instructions and methodology register; emits host work packets; validates structured evidence, units and calculations; enforces stage dependencies; archives superseded findings; invalidates downstream decisions; and exports the committee packet and evidence lineage.

A human or separately authorized AI host performs the actual research. There is **no embedded LLM, live market feed, automatic source extraction, scheduler or broker connection**. Research-process controls do not establish source truth or investment accuracy.

| Route | Stages | Asset type |
|---|---:|---|
| `green-bond` | 12 | bond |
| `social-bond` | 12 | bond |
| `sustainability-bond` | 12 | bond |
| `sustainability-linked-bond` | 12 | bond |
| `transition-bond` | 13 | bond |

## Run the local workflow

From the repository root:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/check_repository.py
python3 -m sf_agent routes
python3 -m sf_agent demo --out runs/demo-01
python3 -m sf_agent report --run runs/demo-01
python3 -m sf_agent export --run runs/demo-01 --out exports/demo-01
python3 -m sf_agent source-study --out runs/source-study-01
```

These commands require no third-party runtime packages, credentials or network access. Use fresh output directories. The demo uses deterministic fixtures, not live research. A source-study process exit of 0 means the command ran, not that diligence is complete; its research result remains `NEEDS_DATA`.

```bash
python3 -m sf_agent calc --operation bond_risk --arguments examples/calculation-arguments.json --currency USD
```

[Calculation inputs](examples/calculation-arguments.json) · [Method and operation boundaries](docs/METHODOLOGY.md).

## Conduct actual research

Replace all placeholders in `examples/research-request-template.json`, identify the actual instruments, register permitted evidence and set explicit freshness policies. Follow [the host workflow](WORKFLOW.md) and [artifact guide](templates/host-artifact-guide.md). `next` emits the stage contract and upstream evidence context; submit researched artifacts using the latest revision. Do not substitute fixtures for research.

Use `SKILL.md` with the complete adjacent folder in a filesystem-enabled agent host. Child skills are under `skills/`. Copying prompts into a text-only chat does not enforce the Python state machine. Host installation and activation are not certified. An autonomous host must not call the human approval command.

## Evidence controls and limitations

Numerical claims bind to evidence metrics and original units. Allowlisted calculations declare provenance and are recomputed. Revisions archive affected outputs and revoke prior review. Unknown data remains unknown; material open issues block approval. Demo and source-study modes cannot be research-approved.

Inspectable local records are not tamper-proof, and reviewer attestations are not authenticated identities. The engine does not certify source truth, legal compliance, impact causality, current trade suitability, production security or investment alpha. Many projects and programmes are not liquid or investable. Read the [enforced-versus-procedural control map](docs/INSTITUTIONAL_QUALITY.md).

## Maintenance, sources and licence

The original engine, research case, numerical results and approval controls are preserved. In GitHub Desktop, fetch and pull before editing an existing clone, preserve `.git` and review changes on a working branch.

[Desktop guide](START_HERE_GITHUB_DESKTOP.md) · [Repository metadata](repository-metadata.json) · [Discoverability](docs/GEO_SEO.md) · [Method sources](references/SOURCES.md) · [Data requirements](docs/DATA_SOURCES.md) · [Security](SECURITY.md)

Original code, prompts and examples: MIT, Copyright 2026 HHFinAi. Third-party sources retain their rights. No affiliation with or endorsement by referenced institutions or standard setters is implied. [Licence](LICENSE) · [Notices](NOTICE.md).
