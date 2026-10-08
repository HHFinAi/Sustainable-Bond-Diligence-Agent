"""Keep the historical case's economic checks and stored outputs in CI."""
import importlib.util
import json
import copy
import math
from datetime import date
from pathlib import Path
import unittest

CASE = Path(__file__).resolve().parents[1] / "examples" / "research" / "eib-eugb-2037"
spec = importlib.util.spec_from_file_location("eib_case", CASE / "calculate.py")
model = importlib.util.module_from_spec(spec)
spec.loader.exec_module(model)


class EIBCase(unittest.TestCase):
    def setUp(self):
        self.config = json.loads((CASE / "holding-period-inputs.json").read_text())
        self.hp = model.holding_period

    def test_risk_invariants_and_committed_results(self):
        # build also checks independent derivatives, zero-coupon identities,
        # maturity/principal, the stub and both payment-calendar alternatives.
        data = json.loads((CASE / "inputs.json").read_text())
        for name, expected in model.build(data).items():
            self.assertEqual((CASE / name).read_text(), expected, name)

    def test_clean_dirty_accrual_and_coupon_boundary(self):
        terms = self.config["instruments"]["green"]
        self.assertEqual(self.hp.accrual(terms, date(2025, 5, 15)), 0)
        # Independently counted actual annual period: 158 days / 365 days.
        self.assertAlmostEqual(self.hp.accrual(terms, date(2025, 10, 20)), 3.125 * 158 / 365)
        result = self.hp.matched_comparison(self.config, 5, 5)["green"]
        self.assertAlmostEqual(result["entry_clean_per_100"] + result["entry_accrued_per_100"], result["entry_dirty_per_100"])
        self.assertAlmostEqual(result["coupon_cash_per_100"], 6.25)

    def test_flat_curve_closed_form_and_spread_recovery(self):
        terms = self.config["instruments"]["green"]
        start = date(2025, 10, 20)
        curve = [{"tenor_years": 0, "zero_rate_cc": .03}, {"tenor_years": 15, "zero_rate_cc": .03}]
        flows = self.hp.cashflows(terms, start)
        expected = sum(f["total_per_100"] * math.exp(-.035 * (date.fromisoformat(f["payment_date"]) - start).days / 365) for f in flows)
        actual = self.hp.dirty_price(terms, start, curve, .005)
        self.assertAlmostEqual(actual, expected)
        self.assertAlmostEqual(self.hp.solve_spread(terms, start, curve, actual), .005)
        self.assertAlmostEqual(self.hp.dirty_price(terms, date(2027, 10, 20), curve, .005),
                               self.hp.dirty_price(terms, date(2027, 10, 20), curve, .005, forward_years=2))

    def test_full_holding_pnl_coupon_reinvestment_and_costs(self):
        row = self.hp.matched_comparison(self.config, 5, 10)["green"]
        expected_reinvestment = sum(3.125 * (math.exp(.025 * (date(2027, 10, 20) - d).days / 365) - 1) for d in [date(2026, 5, 15), date(2027, 5, 15)])
        self.assertAlmostEqual(row["coupon_reinvestment_per_100"], expected_reinvestment)
        expected = row["exit_clean_per_100"] + row["exit_accrued_per_100"] + 6.25 + expected_reinvestment - row["entry_clean_per_100"] - row["entry_accrued_per_100"] - row["entry_dirty_per_100"] * .0015 - row["exit_dirty_per_100"] * .0015
        self.assertAlmostEqual(row["net_pnl_per_100"], expected)
        self.assertAlmostEqual(sum(row["components"].values()), expected)

    def test_rate_shock_and_spread_shock_are_distinct_economically(self):
        rates = self.hp.matched_comparison(self.config, 5, 5, rate_shift=25)
        spread = self.hp.matched_comparison(self.config, 5, 5, common_spread_shift=25)
        # Same total flat discount shift gives same terminal prices, but attribution differs.
        self.assertAlmostEqual(rates["green"]["exit_dirty_per_100"], spread["green"]["exit_dirty_per_100"])
        self.assertLess(rates["green"]["components"]["rate_curve_change_per_100"], 0)
        self.assertAlmostEqual(rates["green"]["components"]["spread_change_after_rate_shift_per_100"], 0)
        self.assertAlmostEqual(spread["green"]["components"]["rate_curve_change_per_100"], 0)
        self.assertLess(spread["green"]["components"]["spread_change_after_rate_shift_per_100"], 0)

    def test_dv01_matching_identity_and_identical_instrument_control(self):
        config = copy.deepcopy(self.config)
        config["instruments"]["conventional"] = dict(config["instruments"]["green"])
        config["costs"]["conventional"] = dict(config["costs"]["green"])
        for rate, slope in [(0, 0), (100, 0), (0, 25)]:
            result = self.hp.matched_comparison(config, 0, 0, rate, slope)
            self.assertAlmostEqual(result["conventional_face_per_100_green_for_equal_parallel_dv01"], 100)
            self.assertAlmostEqual(result["benchmark_cash_balance_per_100_green"], 0)
            self.assertAlmostEqual(result["dv01_matched_excess_pnl_per_100_green"], 0)

    def test_hurdle_has_economic_sign_and_solves_net_pnl(self):
        result = self.hp.build(self.config, json.loads((CASE / "quote-request.json").read_text()), "2025-10-16")
        for hurdle in result["entry_hurdles"]:
            g0, g1 = hurdle["initial_greenium_bps"], hurdle["required_terminal_greenium_bps"]
            self.assertLess(abs(hurdle["excess_pnl_at_hurdle_per_100"]), 1e-9)
            self.assertLess(self.hp.matched_comparison(self.config, g0, g1 - 1)["dv01_matched_excess_pnl_per_100_green"], 0)
            self.assertGreater(self.hp.matched_comparison(self.config, g0, g1 + 1)["dv01_matched_excess_pnl_per_100_green"], 0)
        self.assertEqual(result["quote_gate"]["status"], "NEEDS_DATA")
        self.assertIsNone(result["quote_gate"]["entry_recommendation"])

    def test_quote_gate_rejects_hindsight_missing_sides_and_mismatch(self):
        packet = json.loads((CASE / "quote-request.json").read_text())
        packet["contract_status"] = "ISSUE_SPECIFIC_TERMS_VERIFIED"
        for quote in [packet["green"], packet["conventional"]]:
            quote.update(timestamp="2025-10-16T12:00:00+02:00", settlement_date="2025-10-20",
                         price_convention="CLEAN_PER_100", bid_clean=99, ask_clean=100,
                         bid_size_eur=1000000, ask_size_eur=1000000,
                         quote_type="EXECUTABLE_TWO_WAY", review_status="REVIEWED",
                         source_url="https://example.invalid/synthetic-test", document_locator="TEST ONLY")
        self.assertEqual(self.hp.quote_gate(packet, "2025-10-16")["status"], "QUOTE_PACKET_COMPLETE_REQUIRES_ACCOUNTABLE_REVIEW")
        changes = [{"timestamp": "2026-10-08T12:00:00+02:00"}, {"ask_clean": None},
                   {"timestamp": "2025-09-04T12:00:00+02:00"},
                   {"bid_clean": 101}, {"timestamp": "2025-10-16T12:10:00+02:00"},
                   {"settlement_date": "2025-10-21"}, {"currency": "GBP"},
                   {"timestamp": "2025-10-16T12:00:00"}, {"bid_size_eur": 0}, {"bid_clean": float("nan")}]
        for change in changes:
            bad = copy.deepcopy(packet)
            bad["green"].update(change)
            with self.subTest(change=change):
                self.assertEqual(self.hp.quote_gate(bad, "2025-10-16")["status"], "NEEDS_DATA")
        for tolerance in [0, -1, 61, 1000000, True, "60", float("nan"), float("inf")]:
            bad = copy.deepcopy(packet)
            bad["maximum_timestamp_gap_seconds"] = tolerance
            with self.subTest(tolerance=tolerance):
                self.assertEqual(self.hp.quote_gate(bad, "2025-10-16")["status"], "NEEDS_DATA")
        stale = copy.deepcopy(packet)
        for quote in [stale["green"], stale["conventional"]]:
            quote["timestamp"] = "2025-09-04T12:00:00+02:00"
        self.assertEqual(self.hp.quote_gate(stale, "2025-10-16")["status"], "NEEDS_DATA")
        # Written local date alone cannot change the fixed Paris comparison clock.
        for quote in [stale["green"], stale["conventional"]]:
            quote["timestamp"] = "2025-10-16T00:30:00+14:00"
        self.assertEqual(self.hp.quote_gate(stale, "2025-10-16")["status"], "NEEDS_DATA")
        for quote in [stale["green"], stale["conventional"]]:
            quote["timestamp"] = "2025-10-15T23:30:00+00:00"
        self.assertEqual(self.hp.quote_gate(stale, "2025-10-16")["status"], "QUOTE_PACKET_COMPLETE_REQUIRES_ACCOUNTABLE_REVIEW")

    def test_quote_analysis_preserves_bid_ask_and_no_entry_decision(self):
        packet = json.loads((CASE / "quote-request.json").read_text())
        blocked = self.hp.evaluate_quote_packet(self.config, packet, "2025-10-16")
        self.assertIsNone(blocked["pricing"])
        packet["contract_status"] = "ISSUE_SPECIFIC_TERMS_VERIFIED"
        config = copy.deepcopy(self.config)
        for terms in config["instruments"].values():
            terms["contract_status"] = "ISSUE_SPECIFIC_TERMS_VERIFIED"
        settlement = date(2025, 10, 20)
        for side, quote in [("green", packet["green"]), ("conventional", packet["conventional"])]:
            terms = self.config["instruments"][side]
            dirty = self.hp.dirty_price(terms, settlement, self.config["zero_curve_assumption"], .005)
            clean = dirty - self.hp.accrual(terms, settlement)
            quote.update(timestamp="2025-10-16T12:00:00+02:00", settlement_date="2025-10-20",
                         price_convention="CLEAN_PER_100", bid_clean=clean - .1, ask_clean=clean + .1,
                         bid_size_eur=1000000, ask_size_eur=1000000,
                         quote_type="EXECUTABLE_TWO_WAY", review_status="REVIEWED",
                         source_url="https://example.invalid/synthetic-test", document_locator="TEST ONLY")
        # Attesting the packet alone cannot silently certify the default assumed terms.
        self.assertEqual(self.hp.evaluate_quote_packet(self.config, packet, "2025-10-16")["status"], "NEEDS_DATA")
        result = self.hp.evaluate_quote_packet(config, packet, "2025-10-16")
        self.assertAlmostEqual(result["curve_adjusted_mid_greenium_bps"], 0)
        for row in result["pricing"].values():
            self.assertAlmostEqual(row["mid_z_spread_bps"], 50)
            self.assertGreater(row["bid_z_spread_bps"], row["ask_z_spread_bps"])
            self.assertAlmostEqual(row["entry_ask_minus_mid_per_100"], .1)
        self.assertIsNone(result["gate"]["entry_recommendation"])
        self.assertIsNone(result["holding_period_projection"])

    def test_reject_curve_extrapolation_and_matured_settlement(self):
        with self.assertRaises(ValueError):
            self.hp.interpolate(self.config["zero_curve_assumption"], 16)
        with self.assertRaises(ValueError):
            self.hp.accrual(self.config["instruments"]["green"], date(2037, 5, 15))


if __name__ == "__main__":
    unittest.main()
