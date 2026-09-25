# Actual validation — Sustainable Bond Diligence Agent

**Build:** v0.1.0 · **Date:** September 24, 2026 · **Local environment:** Python 3.13.5 on Linux.

| Check actually performed | Result |
|---|---|
| Local unittest suite | **109 tests passed; 0 failures; 0 errors** |
| Route end-to-end synthetic fixtures | All **5** routes passed |
| Default synthetic run | `SYNTHETIC_COMPLETE_NOT_APPROVED`; not approved for research |
| Historical source-study stop case | `NEEDS_DATA`; material evidence gaps preserved |
| JSON Schema definitions and bundled examples | Validated; 14 exported stage artifacts checked |
| Packaged arithmetic operations | 9 allowlisted helpers; domain and shared arithmetic tests |
| CLI | routes, demo, source-study, calc, status, report, export, error paths and prohibited approval |
| Repository/package integrity | Checked separately by `scripts/check_repository.py`; result recorded in `PACKAGE_CHECK.json` |

Read [the actual test log](TEST_LOG.txt), [machine-readable record](VALIDATION.json) and [control boundaries](INSTITUTIONAL_QUALITY.md). The suite tests adverse inputs, source-unit/value mismatch, stale/mismatched quotes, invalid references, calculation recomputation, workflow ordering, revisions, review invalidation, local hashes and prohibited approvals. Shared tests are rerun in all three specialist packages; summing them counts executions, not unique independent validations.

## Not performed
No remote GitHub Actions run; no Windows/macOS run; no local Python 3.10/3.12 run; no host-specific LLM installation/integration; no current market feed validation; no completed live investment case; no backtest or alpha measurement; no independent legal, ecological, causal or regulatory validation; no penetration test; no authenticated reviewer or independent institutional audit. The CI matrix is prepared but not executed on GitHub. The declared Python 3.10+ target is not a claim that every supported version/platform has been tested here.

Historical source-study facts were read from primary/transaction-participant announcement pages and bounded to those statements. Original documents, contracts and full market data were not ingested into a completed live analysis. The study intentionally stops with material gaps rather than generating an apparent trade recommendation.

These results establish that the tested software mechanisms behave as specified on supplied fixtures. They do not establish that a model will correctly interpret unseen evidence, select sensible assumptions, infer impact or produce profitable/suitable investment decisions.
