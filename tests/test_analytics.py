import unittest
from sf_agent.analytics import bond_price,bond_risk,slb_stepup_pv,greenium,allocation_coverage
from sf_agent.validation import DataError

class BondArithmetic(unittest.TestCase):
    def test_par_bond(self): self.assertAlmostEqual(bond_price(100,.05,.05,5,2),100)
    def test_discount_bond(self): self.assertLess(bond_price(100,.05,.06,5,2),100)
    def test_zero_coupon(self): self.assertAlmostEqual(bond_price(100,0,.1,2,1),100/1.1**2)
    def test_zero_yield(self): self.assertEqual(bond_price(100,.05,0,2,1),110)
    def test_negative_yield(self): self.assertGreater(bond_price(100,0,-.01,2,1),100)
    def test_irregular_schedule_rejected(self):
        with self.assertRaises(DataError): bond_price(100,.05,.05,1.2,2)
    def test_zero_period_rejected(self):
        with self.assertRaises(DataError): bond_price(100,.05,.05,1e-12,1)
    def test_frequency_boolean_rejected(self):
        with self.assertRaises(DataError): bond_price(100,.05,.05,5,True)
    def test_duration_and_convexity_finite_difference(self):
        args=dict(face=100,annual_coupon=.05,yield_to_maturity=.06,years=5,frequency=2)
        r=bond_risk(**args);h=1e-5
        pplus=bond_price(**{**args,'yield_to_maturity':.06+h});pminus=bond_price(**{**args,'yield_to_maturity':.06-h})
        self.assertAlmostEqual(r['modified_duration_years'],-(pplus-pminus)/(2*h*r['price']),places=7)
        self.assertAlmostEqual(r['convexity_years_squared'],(pplus-2*r['price']+pminus)/(h*h*r['price']),places=3)
        self.assertAlmostEqual(r['dv01_money_per_bp'],r['price']*r['modified_duration_years']*.0001)
    def test_slb_stepup(self):
        self.assertAlmostEqual(slb_stepup_pv(100,25,4,5,.05,1),.25/1.05**4+.25/1.05**5)
    def test_slb_no_step(self): self.assertEqual(slb_stepup_pv(100,0,1,2,.05,1),0)
    def test_slb_invalid_window(self):
        with self.assertRaises(DataError): slb_stepup_pv(100,25,5,4,.05,1)
    def test_greenium_sign(self): self.assertEqual(greenium(100,105),5);self.assertEqual(greenium(110,105),-5)
    def test_allocation_coverage(self): self.assertEqual(allocation_coverage(75,100),.75)
    def test_excess_allocation(self):
        with self.assertRaises(DataError): allocation_coverage(101,100)
if __name__=='__main__': unittest.main()
