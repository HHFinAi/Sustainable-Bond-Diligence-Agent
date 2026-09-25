# Sustainable Bond Diligence Agent

**Institutional-quality buy-side research, designed to support tradable investment decisions through a traceable, auditable workflow.**

Separates underlying credit, contractual protections, label integrity, verified impact and relative value before a buy-side investment decision. Built by **HHFinAi** for investment analysts, fixed-income/equity specialists, portfolio managers and investment committees.

**Institutional quality describes the designed process controls—not independent audit certification, production readiness, client adoption or guaranteed investment accuracy.** “Tradable” requires a verified investment instrument and appropriate market, legal and portfolio evidence; many private projects and programmes are not liquid or investable. “Auditable” means inspectable local records, not authenticated or tamper-proof recordkeeping. No trade execution is provided.

Version **0.1.0** · **13 specialist stages** · **5 routes** · Python **3.10+ target** · **Human review**

[Workflow](WORKFLOW.md) · [Prompts and skills](PROMPTS.md) · [Evidence trail](docs/AUDIT.md) · [Institutional-quality controls](docs/INSTITUTIONAL_QUALITY.md) · [Validation](docs/VALIDATION.md) · [FAQ](docs/FAQ.md)

## What does this buy-side agent do?
Green, social, sustainability, transition and sustainability-linked bond research. The local engine freezes the research request, prompts and methodology register; emits host work packets; validates structured evidence, units and calculations; enforces stage dependencies; archives superseded findings; invalidates downstream decisions; and records explicit human research review. It exports a committee packet, claim ledger, evidence ledger and complete JSON lineage.

The host AI or human performs the actual research through separately authorized tools. **No embedded LLM, live data feed, automatic source extraction, scheduler or broker connection is included.** Synthetic demonstrations test workflow mechanics; they do not run live investment analysis. The incomplete primary-source study demonstrates safe stopping, not completed diligence.

## Choose a research route
| Route | Stages | Asset types |
|---|---:|---|
| `green-bond` | 12 | bond |
| `social-bond` | 12 | bond |
| `sustainability-bond` | 12 | bond |
| `sustainability-linked-bond` | 12 | bond |
| `transition-bond` | 13 | bond |

## Run the tested local workflow
From this repository's root, with Python 3.10 or later:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/check_repository.py
python3 -m sf_agent routes
python3 -m sf_agent demo --out runs/demo-01
python3 -m sf_agent report --run runs/demo-01
python3 -m sf_agent export --run runs/demo-01 --out exports/demo-01
python3 -m sf_agent source-study --out runs/source-study-01
```

No third-party runtime packages, credentials or network access are required for these commands. Use a fresh output directory each time. The `source-study` command deliberately returns a NEEDS_DATA research status because material evidence is absent; that is the intended control demonstration, not an analysis to trade on. Process exit 0 means the command ran, not that the investment research is approved.

## Inspect actual example outputs
[Synthetic packet](examples/reports/synthetic-packet.md) · [Incomplete historical source study](examples/reports/source-study-packet.md) · [Calculation input](examples/calculation-arguments.json)

```bash
python3 -m sf_agent calc --operation bond_risk --arguments examples/calculation-arguments.json --currency USD
```

The calculation is illustrative and uses explicit assumptions. See [methodology and operation boundaries](docs/METHODOLOGY.md). The test suite is not evidence of investment alpha, impact causality, regulatory compliance or current trade suitability.

## Use the prompts for real research
Start with `examples/research-request-template.json`, replace every placeholder, identify actual instruments, register reviewed permitted evidence and set explicit freshness policies. Follow the [host workflow](WORKFLOW.md) and [artifact guide](templates/host-artifact-guide.md). `next` emits the stage contract and upstream evidence context; submit actual research artifacts using the latest revision. Do not use deterministic fixtures to complete a research run.

Use the complete folder with `SKILL.md` in a filesystem-enabled agent host. Child skills are under `skills/`. Host installation/activation is not certified, and copying a prompt into a text-only chat does not enforce the Python state machine. Do not call the human approval command from an autonomous host agent.

## What makes the evidence layer auditable?
Every numerical source claim binds to its evidence metric and original unit. Every allowlisted calculation declares input provenance and is recomputed. The run freezes adopted instructions and input metadata; revisions archive affected outputs and revoke prior review. Unknown data remains unknown, open material issues block approval, and synthetic/source-study modes cannot be research-approved. See the [claim-to-control matrix](docs/INSTITUTIONAL_QUALITY.md) for enforced versus procedural controls and missing capabilities.

## Publish under HHFinAi
These are publication-ready local files, **not a confirmation of a live GitHub repository**. Follow [GitHub Desktop setup](START_HERE_GITHUB_DESKTOP.md), choose visibility deliberately and use `repository-metadata.json` for the About description and topics. No existing repository or profile was changed. [GEO/search documentation](docs/GEO_SEO.md) uses visible content, citations and clear structure; it does not promise search rankings or AI citations.

## Licence, sources and limitations
Original code, prompts and examples: MIT, Copyright 2026 HHFinAi. See [NOTICE](NOTICE.md) for upstream lineage and third-party rights. No affiliation with or endorsement by referenced standard setters or institutions. Read [method sources](references/SOURCES.md), [data requirements](docs/DATA_SOURCES.md), [security](SECURITY.md), [FAQ](docs/FAQ.md) and the actual [validation record](docs/VALIDATION.md) before use.
