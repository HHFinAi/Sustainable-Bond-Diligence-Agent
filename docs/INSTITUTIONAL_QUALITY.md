# Institutional-quality controls and claim boundaries

**Positioning:** institutional-quality buy-side research, designed to support tradable investment decisions through a traceable, auditable workflow. The claim describes the research-process design and the inspectable controls below. It is not independent certification, production approval, institutional adoption, proven alpha or guaranteed suitability.

| Claim | Implemented control | Evidence to inspect | Boundary |
|---|---|---|---|
| Traceable evidence | Typed evidence IDs, locators, dates, scope and review status; metric binding | `sf_agent/validation.py`; `tests/test_controls.py` | No automatic retrieval, source authentication or semantic entailment proof |
| Reproducible calculations | Allowlisted functions, explicit units/provenance and result recomputation | `sf_agent/analytics.py`; `sf_agent/maths.py`; `tests/test_analytics.py` | Bounded scenario helpers, not a comprehensive pricing or risk library |
| Auditable workflow | Frozen prompts/request/runtime hashes, revisioned submissions, event hash chain, archived invalidations | `sf_agent/engine.py`; control tests | Local administrator can rewrite records; not WORM or cryptographically authenticated recordkeeping |
| Safe incomplete research | Dependency ordering, NEEDS_DATA/BLOCKED, material issue gate | `tests/test_controls.py`; source-study example | Cannot detect an analyst who falsely declares evidence complete |
| Trade-aware research | Exact instrument, market-access, fresh quoted evidence for public candidates, contract gate for private candidates | `validate_expression`; investment template | PASS checks are attestations; no guaranteed liquidity, suitability, legal access or execution |
| Human accountability | Explicit review attestation; synthetic/source-study approval prohibited; review invalidation on revisions | `engine.review`; control tests | Reviewer identity and independence are not authenticated |
| Honest discovery | Answer-first README, FAQ, citation metadata, visible limitations and examples | `repository-metadata.json`; `docs/GEO_SEO.md` | No ranking, indexing or AI-citation guarantee |

## Release posture
Version 0.1.0 is a tested workflow prototype for research support. Inspect `docs/VALIDATION.md` for checks actually run. Synthetic tests demonstrate implemented mechanics, not correctness on real investment decisions. The primary-source studies intentionally stop on missing evidence; they are not completed due-diligence cases. No backtest, live pricing validation, model calibration, ecological validation, legal opinion, security penetration test or independent institutional audit has been performed.

## Three levels of assurance
**Enforced by code:** finite values, selected routes, workflow ordering, source-ID/scope binding, typed units, allowlisted recomputation, revision matching, state integrity and declared review gates.

**Procedural/human:** source truth and entailment; actual completion of analytical sections; verification standards; lawful data access; applicability of methods; independent challenge; appropriate portfolio/market/liquidity judgments.

**Not implemented:** live feeds, automatic document extraction, GIS layers, causal proof, official DSA templates, comprehensive bond/OAS models, authentication, immutable retention, portfolio optimization, broker orders or background monitoring. Do not describe these as working features.
