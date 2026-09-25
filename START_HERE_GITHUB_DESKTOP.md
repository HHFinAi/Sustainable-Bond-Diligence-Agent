# Publish with GitHub Desktop — HHFinAi only

These files are prepared locally; no remote repository, topic, profile or GitHub Pages change was made during this build. Review the package and run the checks before publishing. Do not upload run folders, confidential source documents, API keys or the ZIP archive itself.

1. Extract the repository folder from its ZIP. In GitHub Desktop, confirm the active GitHub account is **HHFinAi**, not hh-health-AI. Select **File → New Repository** and use the exact suggested repository name in `repository-metadata.json`.
2. Choose a local parent directory so GitHub Desktop creates a new empty repository folder. Copy the extracted package's contents into that folder, including `.github`, `.gitignore` and `.gitattributes`. Keep the `.git` directory created by GitHub Desktop. Avoid accidentally nesting the entire package one level too deep: `README.md` and `sf_agent/` must be at the repository root.
3. Confirm repository-specific author identity in Git settings. Use your verified HHFinAi email or the exact GitHub-provided noreply address from your account settings. Do not invent an email or copy hh-health-AI attribution. Review the complete changes and commit with `Initial HHFinAi sustainable-finance agent v0.1.0`.
4. Click **Publish repository**, verify owner **HHFinAi**, and choose visibility deliberately. Public visibility is required for public search discovery; do not make anything public solely because this guide contains GEO metadata. No visibility change is automatic.
5. In the GitHub repository's About settings, paste the prepared description and topics from `repository-metadata.json`. Review the GitHub Actions result after publication; the included workflow has only been run locally here, not on your GitHub account. The static HTML page is optional and is not automatically deployed.

For an already existing repository, fetch/pull first and copy only intended package files. Do not replace `.git`, force-push, delete history or overwrite unrelated content. The packages are self-contained and do not require the existing climate repository to be modified. A full desktop publication walkthrough has not been tested on your machine; menu labels may vary by app version.

## Local verification
From the repository root, run:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/check_repository.py
python3 -m sf_agent demo --out runs/first-demo
python3 -m sf_agent report --run runs/first-demo
```

Use a new run directory for each demo. On systems where Python 3 is invoked as `python`, substitute that command. Runtime target: Python 3.10+; inspect `docs/VALIDATION.md` for the version actually tested.
