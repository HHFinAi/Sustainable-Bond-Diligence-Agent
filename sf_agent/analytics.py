"""Regular, fixed-rate, option-free bond helpers; no yield-curve or OAS model."""
from __future__ import annotations
import math
from .maths import COMMON_OPERATIONS, checked, fraction, number, operation, positive, require

BOND_UNITS = {"face": "$money", "annual_coupon": "decimal", "yield_to_maturity": "decimal", "years": "years", "frequency": "payments_per_year"}

def terms(face, annual_coupon, yield_to_maturity, years, frequency):
    face = positive(face, "face")
    coupon = checked(annual_coupon, "annual_coupon", 0, 1)
    require(type(frequency) is int and frequency in (1, 2, 4, 12), "frequency must be 1, 2, 4, or 12")
    years = positive(years, "years")
    periods = years * frequency
    require(abs(periods - round(periods)) < 1e-9 and 1 <= round(periods) <= 600, "regular schedule required; 1..600 whole periods")
    rate = number(yield_to_maturity, "yield_to_maturity") / frequency
    require(rate > -1, "yield must exceed -frequency")
    return face, face * coupon / frequency, rate, int(round(periods)), frequency

@operation(BOND_UNITS, "$money")
def bond_price(face: float, annual_coupon: float, yield_to_maturity: float, years: float, frequency: int) -> float:
    """Coupon-date full price; accrued interest is zero at the assumed valuation date."""
    par, coupon, rate, n, _ = terms(face, annual_coupon, yield_to_maturity, years, frequency)
    try:
        price = sum(coupon / (1 + rate) ** t for t in range(1, n + 1)) + par / (1 + rate) ** n
    except (OverflowError, ZeroDivisionError) as exc:
        from .validation import DataError
        raise DataError("discount factors outside supported range") from exc
    return number(price, "price")

@operation(BOND_UNITS, "bond_risk_metrics")
def bond_risk(face: float, annual_coupon: float, yield_to_maturity: float, years: float, frequency: int) -> dict:
    par, coupon, rate, n, freq = terms(face, annual_coupon, yield_to_maturity, years, frequency)
    price = bond_price(face, annual_coupon, yield_to_maturity, years, frequency)
    pvs = [(t, (coupon + (par if t == n else 0)) / (1 + rate) ** t) for t in range(1, n + 1)]
    macaulay = sum(t / freq * pv for t, pv in pvs) / price
    modified = macaulay / (1 + rate)
    convexity = sum(t * (t + 1) * pv for t, pv in pvs) / (price * freq**2 * (1 + rate)**2)
    return {"price": price, "modified_duration_years": modified, "convexity_years_squared": convexity,
            "dv01_money_per_bp": price * modified * 0.0001}

@operation({"face": "$money", "step_up_bps": "basis_points", "first_payment_period": "period_index", "last_payment_period": "period_index", "annual_discount": "decimal", "frequency": "payments_per_year"}, "$money")
def slb_stepup_pv(face: float, step_up_bps: float, first_payment_period: int, last_payment_period: int,
                  annual_discount: float, frequency: int) -> float:
    """PV of extra coupons IF the contractual step-up triggers; not expected value."""
    par = positive(face, "face")
    step = checked(step_up_bps, "step_up_bps", 0)
    require(type(frequency) is int and frequency in (1, 2, 4, 12), "unsupported frequency")
    require(type(first_payment_period) is int and type(last_payment_period) is int, "periods must be integers")
    require(1 <= first_payment_period <= last_payment_period <= 600, "invalid step-up period range")
    rate = number(annual_discount, "annual_discount") / frequency
    require(rate > -1, "invalid discount rate")
    return number(sum(par * step / 10000 / frequency / (1 + rate) ** t
                      for t in range(first_payment_period, last_payment_period + 1)), "step-up PV")

@operation({"labelled_spread_bps": "basis_points", "matched_conventional_spread_bps": "basis_points"}, "basis_points")
def greenium(labelled_spread_bps: float, matched_conventional_spread_bps: float) -> float:
    """Positive value = labelled bond's tighter spread. Comparability is external."""
    return number(matched_conventional_spread_bps, "conventional spread") - number(labelled_spread_bps, "labelled spread")

@operation({"eligible_allocated": "$money", "net_proceeds": "$money"}, "decimal_fraction")
def allocation_coverage(eligible_allocated: float, net_proceeds: float) -> float:
    allocated = checked(eligible_allocated, "eligible_allocated", 0)
    proceeds = positive(net_proceeds, "net_proceeds")
    require(allocated <= proceeds, "allocated amount exceeds proceeds; reconcile double counting and currency first")
    return allocated / proceeds

OPERATIONS = dict(COMMON_OPERATIONS)
OPERATIONS.update({f.__name__: f for f in (bond_price, bond_risk, slb_stepup_pv, greenium, allocation_coverage)})
