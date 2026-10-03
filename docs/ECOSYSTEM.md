# HHFinAi sustainable-finance agent ecosystem

These three specialist packages share identical local runtime modules and distinct domain instructions/calculations. Each can run alone from its repository root without an installed cross-repository dependency. This is a deliberate initial vendoring choice, not three independently developed orchestration engines. Shared files are versioned together and listed in `COMMON_CORE_MANIFEST.json`. Before any common-code release, synchronize the code across all three and rerun each domain's tests. Domain additions must preserve the shared contracts; a future separately versioned common package can replace vendoring after deployment needs are validated.

Published repositories:

- [Sustainable Bond Diligence Agent](https://github.com/HHFinAi/Sustainable-Bond-Diligence-Agent)
- [Nature and Biodiversity Investment Agent](https://github.com/HHFinAi/Nature-and-Biodiversity-Investment-Agent)
- [Sovereign and Social-Impact Finance Agent](https://github.com/HHFinAi/Sovereign-and-Social-Impact-Finance-Agent)

These are the current public repository names, checked on October 3, 2026. Existing climate workflow design lineage is pinned to `3e08518e3e75ede2a5391b4c685bbab52e0f4bb4`. The initial specialist build did not change its source repository or state files, and integration with its older state schema is not implemented. Methodology and findings may be reused only with explicit provenance and independent revalidation, not by treating incompatible state files as interchangeable.
