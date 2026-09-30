"""Numerical and failure invariants for the finite teaching examples."""
import math
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from cornagents.education import cp_upper, digest, MemoryStore, ResearchBudget, DurableToy, low_rank_update

class RiskBoundTests(unittest.TestCase):
    def test_zero_error_formula(self):
        for n in [1, 100, 299, 2995]:
            self.assertAlmostEqual(cp_upper(0,n), 1-.05**(1/n), places=12)

    def test_exact_two_trials_one_error(self):
        # P(X <= 1) = 1-p^2 for n=2. Invert at alpha=.05.
        self.assertAlmostEqual(cp_upper(1,2), math.sqrt(.95), places=12)

    def test_binomial_cdf_at_bound(self):
        for k,n in [(1,10),(3,20),(7,50)]:
            p=cp_upper(k,n)
            cdf=sum(math.comb(n,i)*p**i*(1-p)**(n-i) for i in range(k+1))
            self.assertAlmostEqual(cdf,.05,places=11)

    def test_error_monotonicity(self):
        values=[cp_upper(k,20) for k in range(21)]
        self.assertTrue(all(a<=b for a,b in zip(values,values[1:])))

    def test_no_data_and_all_errors(self):
        self.assertEqual(cp_upper(0,0),1)
        self.assertEqual(cp_upper(7,7),1)

    def test_counts_reject_bool_float_and_negative(self):
        for k,n in [(True,10),(0,False),(0.,10)]:
            with self.assertRaises(TypeError):cp_upper(k,n)
        for k,n in [(-1,10),(11,10),(0,-1)]:
            with self.assertRaises(ValueError):cp_upper(k,n)

    def test_invalid_alpha(self):
        for alpha in [0,1,float('nan'),float('inf')]:
            with self.assertRaises(ValueError):cp_upper(0,10,alpha)

class RuntimeExampleTests(unittest.TestCase):
    def test_child_uses_same_budget(self):
        parent=ResearchBudget(1); child=DurableToy(parent)
        child.execute('child','payload')
        with self.assertRaises(PermissionError):parent.spend()
        self.assertEqual(parent.used,1)

    def test_direct_memory_revocation_propagates(self):
        store=MemoryStore()
        store.propose('fact','A','fact',['source'],10)
        store.propose('summary','A','summary',['fact'],10)
        store.activate('fact',True);store.activate('summary',True)
        store.revoke_source('fact')
        for key in ['fact','summary']:
            with self.assertRaises(PermissionError):store.read(key,'A',1)

    def test_low_rank_does_not_mutate_base(self):
        weights=[[1,0],[0,1]]
        updated=low_rank_update(weights,[[1],[2]],[[3,4]])
        self.assertEqual(weights,[[1,0],[0,1]])
        self.assertEqual(updated,[[4,4],[6,9]])

    def test_digest_binds_content_not_key_order(self):
        self.assertEqual(digest({'a':1,'b':2}),digest({'b':2,'a':1}))
        self.assertNotEqual(digest({'a':1}),digest({'a':2}))

if __name__=='__main__':unittest.main()
