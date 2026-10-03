"""Keep the historical case's economic checks and stored outputs in CI."""
import importlib.util
import json
from pathlib import Path
import unittest

CASE = Path(__file__).resolve().parents[1] / "examples" / "research" / "eib-eugb-2037"
spec = importlib.util.spec_from_file_location("eib_case", CASE / "calculate.py")
model = importlib.util.module_from_spec(spec)
spec.loader.exec_module(model)


class EIBCase(unittest.TestCase):
    def test_risk_invariants_and_committed_results(self):
        # build also checks independent derivatives, zero-coupon identities,
        # maturity/principal, the stub and both payment-calendar alternatives.
        data = json.loads((CASE / "inputs.json").read_text())
        for name, expected in model.build(data).items():
            self.assertEqual((CASE / name).read_text(), expected, name)


if __name__ == "__main__":
    unittest.main()
