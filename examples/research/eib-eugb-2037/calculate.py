#!/usr/bin/env python3
"""Bounded historical EIB risk illustration; Python standard library only.

No market-data feed, execution, runtime approval, or contract verification.
The original-settlement cash-flow schedule is an explicit assumption.
Run: python3 calculate.py [--check]
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import importlib.util
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
_holding_spec = importlib.util.spec_from_file_location("eib_holding_period", ROOT / "holding_period.py")
holding_period = importlib.util.module_from_spec(_holding_spec)
_holding_spec.loader.exec_module(holding_period)


def schedule(data: dict, long_first: bool = False) -> list[dict]:
    instrument = data["instrument"]
    assumptions = data["model_assumptions"]
    settlement = date.fromisoformat(assumptions["valuation_date"])
    first = date.fromisoformat(assumptions["first_coupon_date"])
    maturity = date.fromisoformat(instrument["maturity_date"])
    start = date.fromisoformat(assumptions["stub_reference_start"])
    end = date.fromisoformat(assumptions["stub_reference_end"])
    stub = (first - settlement).days / (end - start).days
    if not 0 < stub < 1:
        raise ValueError("This bounded model requires a positive short initial stub")
    face = assumptions["face_value"]
    coupon = face * instrument["coupon_rate"]
    flows = []
    for year in range(first.year + int(long_first), maturity.year + 1):
        payment = date(year, assumptions["annual_coupon_month"], assumptions["annual_coupon_day"])
        ordinal = year - first.year
        coupon_fraction = 1.0
        if ordinal == 0:
            coupon_fraction = stub
        elif long_first and ordinal == 1:
            coupon_fraction = 1.0 + stub
        interest = coupon * coupon_fraction
        principal = assumptions["redemption_per_100"] if payment == maturity else 0.0
        flows.append({
            "payment_date": payment.isoformat(),
            "time_years": stub + ordinal,
            "coupon_per_100": interest,
            "principal_per_100": principal,
            "total_per_100": interest + principal,
            "schedule_status": "ASSUMED_NOT_CONTRACT_VERIFIED",
        })
    return flows


def price(flows: list[dict], annual_yield: float) -> float:
    if annual_yield <= -1:
        raise ValueError("Annual yield must exceed -100%")
    return math.fsum(f["total_per_100"] / (1 + annual_yield) ** f["time_years"] for f in flows)


def solve_yield(flows: list[dict], target: float) -> float:
    lo, hi = -0.5, 1.0
    if not price(flows, lo) > target > price(flows, hi):
        raise ValueError("Target price is outside the solver bracket")
    for _ in range(160):
        mid = (lo + hi) / 2
        if price(flows, mid) > target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def risk(flows: list[dict], annual_yield: float) -> dict:
    p = price(flows, annual_yield)
    d = math.fsum(f["time_years"] * f["total_per_100"] / (1 + annual_yield) ** (f["time_years"] + 1) for f in flows) / p
    c = math.fsum(f["time_years"] * (f["time_years"] + 1) * f["total_per_100"] / (1 + annual_yield) ** (f["time_years"] + 2) for f in flows) / p
    return {"price_per_100": p, "annual_yield_pct": annual_yield * 100,
            "modified_duration_years": d, "convexity_years_squared": c,
            "dv01_per_100": p * d / 10000,
            "dv01_eur_per_1m_face": p * d}


def csv_text(rows: list[dict]) -> str:
    import io
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue()


def build(data: dict) -> dict[str, str]:
    flows = schedule(data)
    target = data["instrument"]["reported_reoffer_price_per_100"]
    y = solve_yield(flows, target)
    base = risk(flows, y)
    d, c = base["modified_duration_years"], base["convexity_years_squared"]
    shocks = [
        ("rate_minus_100", -100, 0), ("rate_minus_50", -50, 0),
        ("base", 0, 0), ("spread_plus_25", 0, 25),
        ("rate_plus_50", 50, 0), ("rate_plus_100", 100, 0),
        ("rate_plus_100_spread_plus_50", 100, 50),
    ]
    sensitivity = []
    for label, rate_bp, spread_bp in shocks:
        dy = (rate_bp + spread_bp) / 10000
        p = price(flows, y + dy)
        sensitivity.append({"scenario": label, "rate_change_bps": rate_bp,
            "spread_change_bps": spread_bp, "total_yield_change_bps": rate_bp + spread_bp,
            "price_per_100": p, "price_return_pct": 100 * (p / target - 1),
            "duration_convexity_return_pct": 100 * (-d * dy + 0.5 * c * dy * dy),
            "pnl_eur_per_1m_face": (p - target) * 10000,
            "valuation_date": data["model_assumptions"]["valuation_date"],
            "input_status": "PROVISIONAL_PRICE_ASSUMED_CONTRACT_TERMS",
            "status": "SCENARIO_NOT_FORECAST"})
    rv = data["relative_value_assumptions"]
    relative_value = []
    for greenium in rv["hypothetical_greenium_bps"]:
        p = price(flows, y - greenium / 10000)
        drag = greenium * rv["holding_period_years"] + rv["round_trip_cost_bps_of_value"]
        relative_value.append({"hypothetical_greenium_bps": greenium,
            "hypothetical_conventional_yield_pct": y * 100,
            "hypothetical_green_yield_pct": (y - greenium / 10000) * 100,
            "hypothetical_green_price_per_100": p,
            "price_premium_per_100": p - target,
            "carry_drag_plus_cost_bps_of_value": drag,
            "additional_relative_tightening_to_break_even_bps": drag / d,
            "valuation_date": data["model_assumptions"]["valuation_date"],
            "input_status": "PROVISIONAL_PRICE_ASSUMED_CONTRACT_TERMS",
            "status": "HYPOTHETICAL_IDENTICAL_CASHFLOWS_NOT_OBSERVED_GREENIUM"})
    credit = data["credit_inputs_eur_million"]
    credit_stress = []
    for fraction in credit["additional_net_loss_fractions"]:
        loss = credit["loan_book_at_cost_2024"] * fraction
        credit_stress.append({"additional_net_loss_pct_of_loan_cost": fraction * 100,
            "loss_eur_million": loss,
            "own_funds_after_loss_eur_million": credit["own_funds_2024"] - loss,
            "loss_pct_of_starting_own_funds": 100 * loss / credit["own_funds_2024"],
            "status": "ONE_OFF_STATIC_STRESS_NO_CALLABLE_CAPITAL_OR_FUTURE_PROFIT"})
    alternative = schedule(data, long_first=True)
    alt_y = solve_yield(alternative, target)
    h = 1e-5
    numeric_duration = (price(flows, y - h) - price(flows, y + h)) / (2 * h * target)
    numeric_convexity = (price(flows, y - h) + price(flows, y + h) - 2 * target) / (h * h * target)
    # Independent functional checks resolve concrete schedule and derivative risks.
    assert len(flows) == 13 and len(alternative) == 12
    assert flows[-1]["payment_date"] == data["instrument"]["maturity_date"]
    assert abs(math.fsum(f["principal_per_100"] for f in flows) - 100) < 1e-12
    assert abs(flows[0]["coupon_per_100"] - 3.125 * 36 / 365) < 1e-12
    assert abs(price(flows, y) - target) < 1e-10
    assert abs(numeric_duration - d) < 1e-6
    assert abs(numeric_convexity - c) < 0.0001
    assert price(flows, y - 0.01) > target > price(flows, y + 0.01)
    assert c > 0 and 0 < d < flows[-1]["time_years"]
    assert abs(math.fsum(f["coupon_per_100"] for f in flows) - math.fsum(f["coupon_per_100"] for f in alternative)) < 1e-12
    # Independent zero-coupon identity checks discounting and derivative formulas.
    zero = [{"time_years": 10.0, "total_per_100": 100.0}]
    zr = risk(zero, 0.04)
    assert abs(zr["price_per_100"] - 100 / 1.04**10) < 1e-12
    assert abs(zr["modified_duration_years"] - 10 / 1.04) < 1e-12
    assert abs(zr["convexity_years_squared"] - 110 / 1.04**2) < 1e-10
    results = {
        "research_as_of": data["research_as_of"],
        "model_valuation_date": data["model_assumptions"]["valuation_date"],
        "status": "STANDALONE_HISTORICAL_SCENARIO_NOT_RUNTIME_APPROVED",
        "interpretation": "Computed annual yield is schedule-conditional, not verified published yield or an October 2025 market yield.",
        "price_evidence_status": data["instrument"]["price_evidence_status"],
        "contract_status": "Final issue documents not retrieved; payment schedule, day count, redemption, optionality and legal recourse remain unverified. Material transaction-use blocker.",
        "base": base,
        "first_coupon_days": 36,
        "first_coupon_per_100": flows[0]["coupon_per_100"],
        "long_first_coupon_alternative": {
            "first_payment_date": alternative[0]["payment_date"],
            "first_coupon_per_100": alternative[0]["coupon_per_100"],
            "annual_yield_pct": alt_y * 100,
            "yield_difference_bps": (alt_y - y) * 10000,
            "price_at_base_yield_per_100": price(alternative, y),
        },
        "sensitivity": sensitivity,
        "relative_value": relative_value,
        "credit_stress": credit_stress,
        "validation": {"checks_passed": True,
            "price_reconstruction_absolute_error": abs(price(flows, y) - target),
            "numeric_duration_years": numeric_duration,
            "numeric_convexity_years_squared": numeric_convexity,
            "scope": "Arithmetic and internal consistency only; no external model validation or human approval"},
        "inputs_sha256": hashlib.sha256((ROOT / "inputs.json").read_bytes()).hexdigest(),
    }
    hp_inputs = json.loads((ROOT / "holding-period-inputs.json").read_text())
    quotes = json.loads((ROOT / "quote-request.json").read_text())
    holding = holding_period.build(hp_inputs, quotes, data["research_as_of"])
    holding["inputs_sha256"] = hashlib.sha256((ROOT / "holding-period-inputs.json").read_bytes()).hexdigest()
    holding["quote_request_sha256"] = hashlib.sha256((ROOT / "quote-request.json").read_bytes()).hexdigest()
    hp_rows = []
    for row in holding["scenarios"]:
        hp_rows.append({"scenario": row["scenario"],
                       "initial_greenium_bps": row["initial_greenium_bps_of_z_spread"],
                       "terminal_greenium_bps": row["terminal_greenium_bps_of_z_spread"],
                       "rate_shift_bps": row["rate_shift_bps"],
                       "slope_shift_bps_at_10y": row["slope_shift_bps_at_10y"],
                       "common_eib_spread_shift_bps": row["common_eib_spread_shift_bps"],
                       "green_net_return_pct": row["green"]["net_holding_return_pct"],
                       "conventional_net_return_pct": row["conventional"]["net_holding_return_pct"],
                       "dv01_matched_excess_return_bps": row["dv01_matched_excess_return_bps_of_initial_green_outlay"],
                       "status": row["status"]})
    results["dated_relative_value_model"] = {"file": "holding-period-results.json",
                                            "historical_entry_status": holding["quote_gate"]["status"],
                                            "contract_status": "UNVERIFIED_MATERIAL_FOR_TRANSACTION_USE"}
    dated_flows = []
    for side, terms in hp_inputs["instruments"].items():
        for f in holding_period.cashflows(terms, date.fromisoformat(hp_inputs["settlement_date"])):
            dated_flows.append({"instrument": side, "isin": terms["isin"], **f,
                                "schedule_status": "ASSUMED_NOT_CONTRACT_VERIFIED"})
    return {"results.json": json.dumps(results, indent=2, sort_keys=True) + "\n",
            "cashflows.csv": csv_text(flows), "sensitivity.csv": csv_text(sensitivity),
            "relative-value.csv": csv_text(relative_value), "credit-stress.csv": csv_text(credit_stress),
            "holding-period-results.json": json.dumps(holding, indent=2, sort_keys=True) + "\n",
            "holding-period-scenarios.csv": csv_text(hp_rows),
            "entry-hurdles.csv": csv_text(holding["entry_hurdles"]),
            "dated-cashflows.csv": csv_text(dated_flows)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify committed outputs without changing files")
    args = parser.parse_args()
    outputs = build(json.loads((ROOT / "inputs.json").read_text()))
    if args.check:
        stale = [name for name, value in outputs.items() if not (ROOT / name).is_file() or (ROOT / name).read_text() != value]
        if stale:
            raise SystemExit("Outputs missing or stale: " + ", ".join(stale))
        print(f"PASS: arithmetic checks and all {len(outputs)} generated outputs reproduce exactly")
    else:
        for name, value in outputs.items():
            (ROOT / name).write_text(value)
        print(f"Wrote {len(outputs)} deterministic model outputs; arithmetic checks passed")


if __name__ == "__main__":
    main()
