# Sustainable Bond Diligence Agent workflow

```mermaid
flowchart TD
    mandate["Mandate and investable question"]
    evidence["Evidence intake and reconciliation"]
    terms["Contractual terms and obligor map"]
    credit["Underlying credit underwriting"]
    label["Label, allocation and KPI integrity"]
    transition["Transition credibility and lock-in"]
    impact["Impact evidence and financial linkage"]
    market["Instrument, liquidity and market evidence"]
    valuation["Financial valuation and scenario underwriting"]
    expression["Buy-side investment expression and eligibility"]
    stewardship["Stewardship and thesis monitoring"]
    challenge["Independent challenge and release control"]
    memo["Investment committee research packet"]
    mandate --> evidence
    evidence --> terms
    terms --> credit
    credit --> label
    label --> transition
    transition --> impact
    impact --> market
    market --> valuation
    valuation --> expression
    expression --> stewardship
    stewardship --> challenge
    challenge --> memo
    memo --> HUMAN["Human research review — no execution"]
```

The diagram shows the full specialist route. The bond transition stage applies only to the transition-bond route. Each route in `agent.json` is an explicit sequential DAG: the next stage waits for the prior stage to complete. This design avoids implying automatic independent parallel research. There are no hidden model calls or background agents. See each stage prompt for actual analytical requirements.

## Routes
- `green-bond`: 12 stages; supported asset types: bond.
- `social-bond`: 12 stages; supported asset types: bond.
- `sustainability-bond`: 12 stages; supported asset types: bond.
- `sustainability-linked-bond`: 12 stages; supported asset types: bond.
- `transition-bond`: 13 stages; supported asset types: bond.

## Operating commands
```bash
python3 -m sf_agent init --request your-request.json --out runs/issuer-01
python3 -m sf_agent next --run runs/issuer-01
# Read the returned packet and actual source documents; write a stage artifact.
python3 -m sf_agent submit --run runs/issuer-01 --stage mandate --artifact mandate.json --revision 0
python3 -m sf_agent status --run runs/issuer-01
```

Repeat `next`, actual research and `submit` using the current revision. Change the stage ID and artifact file as appropriate. A failed stage returns NEEDS_DATA/BLOCKED; do not substitute a fixture to complete it. After a material upstream revision, downstream work and any review are invalidated. Add newly obtained evidence by creating a new request/run; references and source history must not be silently edited.

Human-only review after all substantive work is complete:
```bash
python3 -m sf_agent review --run runs/issuer-01 --reviewer "Accountable reviewer" --decision APPROVE_RESEARCH --rationale "Describe checks actually performed" --revision CURRENT_REVISION --attest-human
```
`CURRENT_REVISION` is a placeholder for the integer in `status`. This command records an attestation, not an authenticated identity or a trade decision. Hosts must never use it to impersonate human review.
