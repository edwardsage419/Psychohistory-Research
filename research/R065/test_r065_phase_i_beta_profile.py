"""R065 Phase I tests: author-source softmax and analytic beta fit."""
import math
import unittest
from r065_phase_i_beta_profile import (
    AUTHOR, BLOCK, counts_for, combine, subtract, nll, fit_beta, lopo,
    profile, summary_from_aggregate)


def trial(day, typ, chosen, available=(0,1)):
    return {'day':day,'type':typ,'chosen':chosen,'available':list(available)}

class BetaProfileTests(unittest.TestCase):
    def test_reduction_exact_to_trial_likelihood(self):
        seq=[trial(1,'observe',0),trial(2,'play',0),trial(3,'play',1),trial(4,'play',2,(1,2))]
        c=counts_for(seq,())
        self.assertEqual(c,{'match':1,'mismatch':1,'uniform':1,'play':3})
        from r065_phase_h_model3_reset import predict
        for beta in [0,.5,1,2,3,5,10,20,30]:
            self.assertAlmostEqual(nll(c,beta),sum(x['nll'] for x in predict(seq,(),beta)),places=10)

    def test_reset_on_day89(self):
        seq=[trial(88,'observe',0),trial(89,'play',0)]
        self.assertEqual(counts_for(seq,AUTHOR)['uniform'],1)
        self.assertEqual(counts_for(seq,BLOCK)['match'],1)

    def test_closed_form_mle(self):
        c={'match':18,'mismatch':12,'uniform':8,'play':38}
        self.assertAlmostEqual(fit_beta(c)['beta'],math.log(1.5),places=5)

    def test_excess_mismatch_beta_zero(self):
        c={'match':2,'mismatch':7,'uniform':3,'play':12}
        self.assertEqual(fit_beta(c)['beta'],0)

    def test_only_match_beta_max(self):
        c={'match':4,'mismatch':0,'uniform':3,'play':7}
        self.assertEqual(fit_beta(c)['beta'],30.)

    def test_only_uniform_has_arbitrary_beta_flat(self):
        c={'match':0,'mismatch':0,'uniform':5,'play':5}
        r=fit_beta(c)
        self.assertAlmostEqual(nll(c,0),nll(c,30),places=12)
        # A uniform-only sample cannot identify beta; never interpret the chosen beta as estimated evidence.

    def test_invalid_counts_fail_closed(self):
        for c in [{'match':1,'mismatch':-1,'uniform':1,'play':1},
                  {'match':1,'mismatch':1,'uniform':1,'play':2},
                  {'match':1,'mismatch':1,'uniform':1,'play':3.},
                  {'match':0,'mismatch':0,'uniform':0,'play':0}]:
            with self.subTest(c=c),self.assertRaises(ValueError):nll(c,5)

    def test_invalid_beta(self):
        c={'match':1,'mismatch':1,'uniform':0,'play':2}
        for beta in [-1,31,float('nan'),float('inf')]:
            with self.subTest(beta=beta),self.assertRaises(ValueError):nll(c,beta)

    def test_lopo_excludes_complete_subject(self):
        a={'match':8,'mismatch':0,'uniform':0,'play':8}
        b={'match':0,'mismatch':8,'uniform':0,'play':8}
        v=lopo([a,b]);self.assertEqual(v['folds'],2)
        # Each training fold perfectly predicts the opposite heldout behavior.
        self.assertAlmostEqual(v['mean_nll'],(nll(a,0)+nll(b,30))/16,places=7)

    def test_correct_aggregate_arithmetic(self):
        example={'study':'R065_PHASE_I','subjects':10,'models':{
            'author':{'reset_days':list(AUTHOR),'counts':{'match':182,'mismatch':120,'uniform':240,'play':542}},
            'block':{'reset_days':list(BLOCK),'counts':{'match':188,'mismatch':135,'uniform':219,'play':542}}}}
        s=summary_from_aggregate(example)
        self.assertAlmostEqual(s['models']['author']['pooled_fit']['beta'],.41651494,places=5)
        self.assertAlmostEqual(s['models']['block']['pooled_fit']['beta'],.33116718,places=5)
        self.assertAlmostEqual(s['models']['author']['beta_grid'][5]['mean_nll'],1.4176814699609261,places=11)
        self.assertAlmostEqual(s['models']['block']['beta_grid'][5]['mean_nll'],1.5294617860236366,places=11)

    def test_reject_bad_source_model_mapping(self):
        x={'study':'R065_PHASE_I','subjects':10,'models':{'author':{'reset_days':[89],'counts':{'match':1,'mismatch':1,'uniform':0,'play':2}}}}
        with self.assertRaisesRegex(ValueError,'reset days'):summary_from_aggregate(x)

    def test_train_minus_holdout(self):
        a={'match':18,'mismatch':10,'uniform':8,'play':36}
        b={'match':2,'mismatch':3,'uniform':1,'play':6}
        self.assertEqual(subtract(a,b),{'match':16,'mismatch':7,'uniform':7,'play':30})

if __name__=='__main__':unittest.main()
