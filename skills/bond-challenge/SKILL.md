---
name: bond-challenge
description: "Perform independent challenge and release control for Sustainable Bond Diligence Agent; use when this bounded buy-side research task is requested, not for trading or compliance certification."
license: MIT
---

# Independent challenge and release control

Read `../../prompts/stages/challenge.md`, `../../prompts/system.md` and `../../AGENTS.md` before using this skill. The complete repository must remain available; this file alone is not the workflow or its dependencies.

Apply the stage's research instructions to the supplied issuer/instrument/portfolio evidence. Return the structured stage artifact with these sections: `counter_case`, `control_review`, `unresolved_issues`. Follow the source, calculation, material-gap and human-review boundaries. Use the Python runtime from the repository root for enforced handoffs; text-only use is manual and does not enforce gates.

Do not auto-start a research run or call a broker. Host-specific discovery and activation are not certified. See `../../schemas/artifact.schema.json` and `../../templates/host-artifact-guide.md`.
