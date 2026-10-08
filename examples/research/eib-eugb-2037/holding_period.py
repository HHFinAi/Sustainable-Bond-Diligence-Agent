#!/usr/bin/env python3
"""Conditional dated bond comparison. No historical quotes are manufactured.

Coupon accrual uses an assumed Actual/Actual annual reference period; the
discount curve uses continuously compounded ACT/365F zero rates. These are
separate clocks. Contract verification is a prerequisite for transaction use.
"""
from __future__ import annotations

from datetime import date, datetime
import math
from zoneinfo import ZoneInfo


def annual_dates(terms: dict, start: date) -> list[date]:
    maturity = date.fromisoformat(terms["maturity_date"])
    first = date.fromisoformat(terms["first_coupon_date"])
    dates = [date(y, first.month, first.day) for y in range(first.year, maturity.year + 1)]
    return [d for d in dates if start < d <= maturity]


def accrual(terms: dict, settlement: date) -> float:
    first = date.fromisoformat(terms["first_coupon_date"])
    maturity = date.fromisoformat(terms["maturity_date"])
    if settlement >= maturity:
        raise ValueError("Settlement must precede maturity")
    if settlement < date.fromisoformat(terms["interest_commencement_date"]):
        raise ValueError("Settlement precedes interest commencement")
    next_date = date(settlement.year, first.month, first.day)
    if next_date <= settlement:
        next_date = date(settlement.year + 1, first.month, first.day)
    previous = date(next_date.year - 1, first.month, first.day)
    accrual_start = max(previous, date.fromisoformat(terms["interest_commencement_date"]))
    return 100 * terms["coupon_rate"] * (settlement - accrual_start).days / (next_date - previous).days


def cashflows(terms: dict, settlement: date) -> list[dict]:
    first = date.fromisoformat(terms["first_coupon_date"])
    commencement = date.fromisoformat(terms["interest_commencement_date"])
    maturity = date.fromisoformat(terms["maturity_date"])
    flows = []
    for payment in annual_dates(terms, settlement):
        reference_start = date(payment.year - 1, payment.month, payment.day)
        fraction = 1.0
        if payment == first:
            fraction = (payment - max(reference_start, commencement)).days / (payment - reference_start).days
        interest = 100 * terms["coupon_rate"] * fraction
        principal = terms["redemption_per_100"] if payment == maturity else 0.0
        flows.append({"payment_date": payment.isoformat(),
                      "time_years_act365f": (payment - settlement).days / 365,
                      "coupon_per_100": interest, "principal_per_100": principal,
                      "total_per_100": interest + principal})
    if not flows:
        raise ValueError("No future cash flows")
    return flows


def interpolate(curve: list[dict], tenor: float) -> float:
    if not curve or any(curve[i]["tenor_years"] >= curve[i + 1]["tenor_years"] for i in range(len(curve) - 1)):
        raise ValueError("Curve tenors must be strictly increasing")
    if tenor < 0 or tenor > curve[-1]["tenor_years"]:
        raise ValueError("Tenor is outside the supplied curve; no extrapolation")
    if tenor <= curve[0]["tenor_years"]:
        return curve[0]["zero_rate_cc"]
    for a, b in zip(curve, curve[1:]):
        if tenor <= b["tenor_years"]:
            weight = (tenor - a["tenor_years"]) / (b["tenor_years"] - a["tenor_years"])
            return a["zero_rate_cc"] + weight * (b["zero_rate_cc"] - a["zero_rate_cc"])
    raise ValueError("No interpolation interval")


def dirty_price(terms: dict, settlement: date, curve: list[dict], spread: float,
                rate_shift: float = 0.0, slope_shift: float = 0.0,
                forward_years: float = 0.0) -> float:
    def zero(t):
        if forward_years:
            h = forward_years
            z = ((h + t) * interpolate(curve, h + t) - h * interpolate(curve, h)) / t
        else:
            z = interpolate(curve, t)
        return z + rate_shift + slope_shift * t / 10
    return math.fsum(f["total_per_100"] * math.exp(-(zero(f["time_years_act365f"]) + spread) * f["time_years_act365f"])
                     for f in cashflows(terms, settlement))


def solve_spread(terms: dict, settlement: date, curve: list[dict], dirty: float) -> float:
    if not math.isfinite(dirty) or dirty <= 0:
        raise ValueError("Dirty price must be positive and finite")
    lo, hi = -0.2, 0.5
    if not dirty_price(terms, settlement, curve, hi) < dirty < dirty_price(terms, settlement, curve, lo):
        raise ValueError("Price outside spread solver bracket")
    for _ in range(100):
        mid = (lo + hi) / 2
        if dirty_price(terms, settlement, curve, mid) > dirty:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def parallel_dv01(terms: dict, settlement: date, curve: list[dict], spread: float) -> float:
    # Per 100 face; 1 bp symmetric numerical change, rather than a YTM duration.
    return (dirty_price(terms, settlement, curve, spread, -0.0001) -
            dirty_price(terms, settlement, curve, spread, 0.0001)) / 2


def key_rate_dv01(terms: dict, settlement: date, curve: list[dict], spread: float) -> list[dict]:
    values = []
    for index, node in enumerate(curve):
        down, up = [dict(x) for x in curve], [dict(x) for x in curve]
        down[index]["zero_rate_cc"] -= 0.0001
        up[index]["zero_rate_cc"] += 0.0001
        values.append({"tenor_years": node["tenor_years"],
                       "dv01_per_100": (dirty_price(terms, settlement, down, spread) -
                                        dirty_price(terms, settlement, up, spread)) / 2})
    return values


def holding_return(terms: dict, start: date, end: date, curve: list[dict], initial_spread: float,
                   final_spread: float, costs: dict, reinvestment_rate: float,
                   rate_shift_bps: float = 0, slope_shift_bps_at_10y: float = 0) -> dict:
    if end <= start or end >= date.fromisoformat(terms["maturity_date"]):
        raise ValueError("Horizon must lie after settlement and before maturity")
    h = (end - start).days / 365
    p0 = dirty_price(terms, start, curve, initial_spread)
    p_forward = dirty_price(terms, end, curve, initial_spread, forward_years=h)
    p_static = dirty_price(terms, end, curve, initial_spread)
    p_rate = dirty_price(terms, end, curve, initial_spread,
                        rate_shift_bps / 10000, slope_shift_bps_at_10y / 10000)
    p_final = dirty_price(terms, end, curve, final_spread,
                         rate_shift_bps / 10000, slope_shift_bps_at_10y / 10000)
    payments = [f for f in cashflows(terms, start) if date.fromisoformat(f["payment_date"]) <= end]
    cash = math.fsum(f["coupon_per_100"] for f in payments)
    coupon_value = math.fsum(f["coupon_per_100"] * math.exp(reinvestment_rate * (end - date.fromisoformat(f["payment_date"])).days / 365) for f in payments)
    entry_cost = p0 * costs["entry_bps_of_dirty_value"] / 10000
    exit_cost = p_final * costs["exit_bps_of_dirty_value"] / 10000
    components = {
        "carry_forward_curve_per_100": p_forward - p0 + coupon_value,
        "static_curve_roll_down_per_100": p_static - p_forward,
        "rate_curve_change_per_100": p_rate - p_static,
        "spread_change_after_rate_shift_per_100": p_final - p_rate,
        "transaction_cost_per_100": -entry_cost - exit_cost,
    }
    pnl = p_final + coupon_value - p0 - entry_cost - exit_cost
    if not math.isclose(math.fsum(components.values()), pnl, abs_tol=1e-10):
        raise AssertionError("Holding period decomposition does not reconcile")
    return {"entry_dirty_per_100": p0, "entry_accrued_per_100": accrual(terms, start),
            "entry_clean_per_100": p0 - accrual(terms, start),
            "exit_dirty_per_100": p_final, "exit_accrued_per_100": accrual(terms, end),
            "exit_clean_per_100": p_final - accrual(terms, end),
            "coupon_cash_per_100": cash, "coupon_reinvestment_per_100": coupon_value - cash,
            "entry_cost_per_100": entry_cost, "exit_cost_per_100": exit_cost,
            "initial_outlay_per_100": p0 + entry_cost, "net_pnl_per_100": pnl,
            "net_holding_return_pct": 100 * pnl / (p0 + entry_cost),
            "components": components}


def matched_comparison(config: dict, initial_greenium: float, final_greenium: float,
                       rate_shift: float = 0, slope_shift: float = 0,
                       common_spread_shift: float = 0) -> dict:
    start, end = date.fromisoformat(config["settlement_date"]), date.fromisoformat(config["exit_settlement_date"])
    curve, terms = config["zero_curve_assumption"], config["instruments"]
    cspread = config["conventional_z_spread_bps"] / 10000
    gspread = cspread - initial_greenium / 10000
    kwargs = {"start": start, "end": end, "curve": curve,
              "reinvestment_rate": config["reinvestment_rate_cc"],
              "rate_shift_bps": rate_shift, "slope_shift_bps_at_10y": slope_shift}
    green = holding_return(terms["green"], initial_spread=gspread,
                           final_spread=cspread + (common_spread_shift - final_greenium) / 10000,
                           costs=config["costs"]["green"], **kwargs)
    conventional = holding_return(terms["conventional"], initial_spread=cspread,
                                  final_spread=cspread + common_spread_shift / 10000,
                                  costs=config["costs"]["conventional"], **kwargs)
    gdv = parallel_dv01(terms["green"], start, curve, gspread)
    cdv = parallel_dv01(terms["conventional"], start, curve, cspread)
    hedge_face = gdv / cdv
    cash_balance = green["initial_outlay_per_100"] - hedge_face * conventional["initial_outlay_per_100"]
    funding_gain = cash_balance * (math.exp(config["funding_rate_cc"] * (end - start).days / 365) - 1)
    benchmark_pnl = hedge_face * conventional["net_pnl_per_100"] + funding_gain
    excess = green["net_pnl_per_100"] - benchmark_pnl
    return {"status": "CONDITIONAL_ASSUMPTIONS_NO_OBSERVED_TRADE",
            "initial_greenium_bps_of_z_spread": initial_greenium,
            "terminal_greenium_bps_of_z_spread": final_greenium,
            "rate_shift_bps": rate_shift, "slope_shift_bps_at_10y": slope_shift,
            "common_eib_spread_shift_bps": common_spread_shift,
            "green": green, "conventional": conventional,
            "green_curve_duration_years": gdv * 10000 / green["entry_dirty_per_100"],
            "conventional_curve_duration_years": cdv * 10000 / conventional["entry_dirty_per_100"],
            "conventional_face_per_100_green_for_equal_parallel_dv01": 100 * hedge_face,
            "benchmark_cash_balance_per_100_green": cash_balance,
            "benchmark_cash_interest_or_financing_cost_per_100_green": funding_gain,
            "dv01_matched_benchmark_pnl_per_100_green": benchmark_pnl,
            "dv01_matched_excess_pnl_per_100_green": excess,
            "dv01_matched_excess_return_bps_of_initial_green_outlay": excess / green["initial_outlay_per_100"] * 10000}


def quote_gate(packet: dict, historical_cut: str) -> dict:
    reasons = []
    comparison_clock = ZoneInfo("Europe/Paris")
    required_quote_date = date.fromisoformat(historical_cut)
    tolerance = packet.get("maximum_timestamp_gap_seconds", 60)
    if not isinstance(tolerance, (int, float)) or isinstance(tolerance, bool) or not math.isfinite(tolerance) or not 0 < tolerance <= 60:
        reasons.append("Quote-pair tolerance must be finite, positive and no greater than the 60-second policy cap")
        tolerance = 60
    if packet.get("comparison_timezone", "Europe/Paris") != "Europe/Paris":
        reasons.append("Historical quote comparison clock must be Europe/Paris")
    if packet.get("contract_status") != "ISSUE_SPECIFIC_TERMS_VERIFIED":
        reasons.append("Issue-specific contractual terms and comparator equivalence remain unverified")
    timestamps = []
    settlements = []
    for side, expected in [("green", "EU000A3K4EG9"), ("conventional", "XS0219724878")]:
        quote = packet.get(side, {})
        stamp = None
        if quote.get("isin") != expected:
            reasons.append(f"{side}: exact ISIN mismatch")
        try:
            stamp = datetime.fromisoformat(quote["timestamp"])
            if stamp.utcoffset() is None:
                raise ValueError("timezone absent")
            if stamp.astimezone(comparison_clock).date() != required_quote_date:
                reasons.append(f"{side}: quote must be on the exact historical comparison date in Europe/Paris")
            timestamps.append(stamp)
        except (KeyError, TypeError, ValueError):
            reasons.append(f"{side}: dated timezone-aware quote missing")
        for field in ["bid_clean", "ask_clean", "bid_size_eur", "ask_size_eur"]:
            value = quote.get(field)
            if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value) or value <= 0:
                reasons.append(f"{side}: positive finite {field} missing")
        if all(isinstance(quote.get(k), (float, int)) for k in ["bid_clean", "ask_clean"]):
            if quote["bid_clean"] > quote["ask_clean"]:
                reasons.append(f"{side}: crossed bid/ask")
        if quote.get("currency") != "EUR" or quote.get("price_convention") != "CLEAN_PER_100":
            reasons.append(f"{side}: EUR clean-price convention unverified")
        if quote.get("quote_type") != "EXECUTABLE_TWO_WAY" or quote.get("review_status") != "REVIEWED":
            reasons.append(f"{side}: executable reviewed two-way evidence missing")
        if not quote.get("source_url") or not quote.get("document_locator"):
            reasons.append(f"{side}: source and locator missing")
        try:
            settlement = date.fromisoformat(quote["settlement_date"])
            settlements.append(settlement)
            if stamp is not None and settlement < stamp.astimezone(comparison_clock).date():
                reasons.append(f"{side}: settlement before quote")
        except (KeyError, TypeError, ValueError):
            reasons.append(f"{side}: settlement date missing")
    if len(timestamps) == 2 and abs((timestamps[0] - timestamps[1]).total_seconds()) > tolerance:
        reasons.append("Quote timestamps are not matched within the supplied tolerance")
    if len(settlements) == 2 and settlements[0] != settlements[1]:
        reasons.append("Quote settlement dates differ")
    return {"status": "NEEDS_DATA" if reasons else "QUOTE_PACKET_COMPLETE_REQUIRES_ACCOUNTABLE_REVIEW",
            "reasons": reasons, "entry_recommendation": None,
            "historical_cut": historical_cut,
            "required_quote_date": historical_cut,
            "comparison_timezone": "Europe/Paris",
            "maximum_timestamp_gap_seconds_policy_cap": 60,
            "scope": "Field and chronology checks only; source authenticity, legal equivalence and liquidity require review"}


def evaluate_quote_packet(config: dict, packet: dict, historical_cut: str) -> dict:
    """Price a supplied, attested packet only after chronology/field checks.

    No stored sample observations can be promoted automatically to executable
    evidence. The curve and coupon conventions remain explicitly supplied model
    inputs; a complete packet does not establish independent source authenticity.
    """
    gate = quote_gate(packet, historical_cut)
    for side, terms in config["instruments"].items():
        if terms.get("contract_status") != "ISSUE_SPECIFIC_TERMS_VERIFIED":
            gate["reasons"].append(f"{side}: supplied pricing terms remain unverified; provide reviewed issue-specific --inputs")
    if gate["reasons"]:
        gate["status"] = "NEEDS_DATA"
    if gate["reasons"]:
        return {"status": "NEEDS_DATA", "gate": gate, "pricing": None,
                "holding_period_projection": None}
    settlement = date.fromisoformat(packet["green"]["settlement_date"])
    pricing = {}
    for side, terms in config["instruments"].items():
        quote = packet[side]
        ai = accrual(terms, settlement)
        bid, ask = quote["bid_clean"], quote["ask_clean"]
        pricing[side] = {"isin": quote["isin"], "settlement_date": settlement.isoformat(),
                         "bid_clean_per_100": bid, "ask_clean_per_100": ask,
                         "accrued_per_100_under_supplied_conventions": ai,
                         "bid_dirty_per_100": bid + ai, "ask_dirty_per_100": ask + ai,
                         "mid_dirty_per_100": (bid + ask) / 2 + ai,
                         "bid_z_spread_bps": solve_spread(terms, settlement, config["zero_curve_assumption"], bid + ai) * 10000,
                         "ask_z_spread_bps": solve_spread(terms, settlement, config["zero_curve_assumption"], ask + ai) * 10000,
                         "mid_z_spread_bps": solve_spread(terms, settlement, config["zero_curve_assumption"], (bid + ask) / 2 + ai) * 10000,
                         "entry_ask_minus_mid_per_100": (ask - bid) / 2,
                         "bid_ask_width_per_100": ask - bid,
                         "source_url": quote["source_url"], "document_locator": quote["document_locator"]}
    return {"status": "SUPPLIED_QUOTE_ANALYSIS_REQUIRES_ACCOUNTABLE_REVIEW", "gate": gate,
            "pricing": pricing,
            "curve_adjusted_mid_greenium_bps": pricing["conventional"]["mid_z_spread_bps"] - pricing["green"]["mid_z_spread_bps"],
            "entry_ask_curve_adjusted_yield_concession_bps": pricing["conventional"]["ask_z_spread_bps"] - pricing["green"]["ask_z_spread_bps"],
            "holding_period_projection": None,
            "limitations": "Price/yield computations depend on supplied zero curve and contract conventions. Bid/ask are distinct from midpoint. Future exit quotes, costs and rates are still unknown; no recommendation or realized return is generated."}


def build(config: dict, quotes: dict, historical_cut: str) -> dict:
    scenarios = []
    definitions = [("unchanged_5bp", 5, 5, 0, 0, 0),
                   ("greenium_reverts_to_zero", 5, 0, 0, 0, 0),
                   ("greenium_widens_to_10bp", 5, 10, 0, 0, 0),
                   ("rates_up_100bp", 5, 5, 100, 0, 0),
                   ("eib_spreads_up_25bp", 5, 5, 0, 0, 25),
                   ("curve_steepens_25bp_at_10y", 5, 5, 0, 25, 0)]
    for name, g0, g1, rate, slope, spread in definitions:
        row = matched_comparison(config, g0, g1, rate, slope, spread)
        row["scenario"] = name
        scenarios.append(row)
    hurdles = []
    for g0 in [0, 5, 10]:
        lo, hi = -100.0, 100.0
        if matched_comparison(config, g0, lo)["dv01_matched_excess_pnl_per_100_green"] >= 0 or matched_comparison(config, g0, hi)["dv01_matched_excess_pnl_per_100_green"] <= 0:
            raise ValueError("Entry hurdle not bracketed")
        for _ in range(80):
            mid = (lo + hi) / 2
            if matched_comparison(config, g0, mid)["dv01_matched_excess_pnl_per_100_green"] < 0:
                lo = mid
            else:
                hi = mid
        required = (lo + hi) / 2
        hurdles.append({"initial_greenium_bps": g0, "required_terminal_greenium_bps": required,
                        "additional_relative_tightening_bps": required - g0,
                        "excess_pnl_at_hurdle_per_100": matched_comparison(config, g0, required)["dv01_matched_excess_pnl_per_100_green"]})
    base = scenarios[0]
    start = date.fromisoformat(config["settlement_date"])
    curve = config["zero_curve_assumption"]
    spreads = {"green": (config["conventional_z_spread_bps"] - 5) / 10000,
               "conventional": config["conventional_z_spread_bps"] / 10000}
    residual = []
    keys = {side: key_rate_dv01(terms, start, curve, spreads[side])
            for side, terms in config["instruments"].items()}
    ratio = base["conventional_face_per_100_green_for_equal_parallel_dv01"] / 100
    for g, c in zip(keys["green"], keys["conventional"]):
        residual.append({"tenor_years": g["tenor_years"],
                         "green_dv01_per_100": g["dv01_per_100"],
                         "matched_conventional_dv01_per_100_green": ratio * c["dv01_per_100"],
                         "residual_dv01_per_100_green": g["dv01_per_100"] - ratio * c["dv01_per_100"]})
    return {"status": "CONDITIONAL_MODEL_COMPLETE_HISTORICAL_ENTRY_NEEDS_DATA",
            "research_as_of": historical_cut, "settlement_date_assumption": config["settlement_date"],
            "exit_settlement_date_assumption": config["exit_settlement_date"],
            "input_classification": "All curves, spreads, quotes in scenario pricing, funding rates, costs and unverified contract conventions are labelled assumptions",
            "quote_gate": quote_gate(quotes, historical_cut),
            "quote_packet_analysis": evaluate_quote_packet(config, quotes, historical_cut),
            "scenarios": scenarios,
            "entry_hurdles": hurdles, "key_rate_residuals": residual,
            "conventions": {"coupon_accrual": "ASSUMED Actual/Actual annual coupon reference periods",
                            "curve_discounting": "ACT/365F continuous zero rate plus flat continuous z-spread",
                            "roll_down": "Static residual-tenor curve price less time-zero implied-forward curve price at the horizon; spread held constant",
                            "rate_spread_order": "Rate/slope move first, then spread move; nonlinear decomposition is order-dependent",
                            "risk_matching": "Equal initial parallel curve DV01; residual key-rate exposure is disclosed",
                            "cash": "Coupons reinvested at assumed continuous rate; signed benchmark cash balance earns/pays assumed funding rate",
                            "cost": "Entry cost on entry dirty value and exit cost on exit dirty value; both sides explicit"}}
