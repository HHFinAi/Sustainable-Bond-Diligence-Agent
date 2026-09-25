# Start here

Read [README](README.md), then run the local validation and synthetic demo. Inspect [institutional-quality controls](docs/INSTITUTIONAL_QUALITY.md) and [workflow](WORKFLOW.md) before using the agent for research.

```bash
python3 -m unittest discover -s tests -v
python3 scripts/check_repository.py
python3 -m sf_agent routes
python3 -m sf_agent demo --out runs/demo-01
```

For real research, populate [the research request template](examples/research-request-template.json) with actual instruments, reviewed evidence and explicit freshness policies. Synthetic fixtures are workflow demonstrations, not investment research.
