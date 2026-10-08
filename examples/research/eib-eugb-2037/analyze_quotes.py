#!/usr/bin/env python3
"""Read a private quote packet and print conditional analysis; never edit files."""
import argparse
import json
from pathlib import Path
from holding_period import evaluate_quote_packet


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quotes", type=Path, required=True, help="Local reviewed two-way quote JSON; do not commit licensed data")
    parser.add_argument("--inputs", type=Path, default=Path(__file__).resolve().parent / "holding-period-inputs.json",
                        help="Reviewed terms and zero curve; defaults are labelled illustrative assumptions")
    args = parser.parse_args()
    config = json.loads(args.inputs.read_text())
    packet = json.loads(args.quotes.read_text())
    print(json.dumps(evaluate_quote_packet(config, packet, config["research_as_of"]), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
