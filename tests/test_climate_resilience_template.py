import json
import unittest
from pathlib import Path

class TestClimateResilienceCredit(unittest.TestCase):
    def test_resilience_credit_must_not_invent_investment_route(self):
        x=json.loads((Path(__file__).resolve().parents[1]/"examples/climate-resilience-credit-template.json").read_text())
        self.assertEqual(x["investment_decision"],"NOT_ASSESSED")
        self.assertEqual(x["status"],"NEEDS_DATA")
        self.assertIsNone(x["instrument"]["isin"])
        self.assertIsNone(x["instrument"]["quote_timestamp_utc"])
        self.assertTrue(all(v=="NEEDS_DATA" for v in x["separate_assessments"].values()))

if __name__=="__main__": unittest.main()
