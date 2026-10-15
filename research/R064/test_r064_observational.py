import unittest
from r064_observational import (prepare,totals,describe,score,predictions_for_subject,
                               xorshift_random,bootstrap_cis,blob_sha)

def make_rows(nsubjects=10, high=(1,0), low=(1,1)):
    rows=[]
    for i in range(nsubjects):
        for stage,(n,k) in [('high',high),('low',low)]:
            for t in range(n):
                rows.append({'participant_id':str(i), 'stakes':stage,
                             'copied':str(int(t<k)), 'accurate':'1',
                             'comprehension_check_repetitions':'1'})
    return rows

class R064Tests(unittest.TestCase):
    def test_sha_pure(self): self.assertEqual(blob_sha(b'hello'),'b6fc4c620b67d95f953a5c1c1230aaab5db5a1b0')
    def test_paired(self):
        selected,full,c=prepare(make_rows())
        self.assertEqual(len(selected),10)
        self.assertEqual(len(full),10)
        self.assertEqual(c['eligible_both_stakes'],10)
    def test_primary_sign(self):
        s,_,_=prepare(make_rows())
        self.assertEqual(describe(s)['mean_participant_high_minus_low'],-1.)
    def test_beta_prior(self):
        s,_,_=prepare(make_rows())
        self.assertAlmostEqual(predictions_for_subject(s[0],totals(s))[0],.5)
    def test_holdout_no_self_training(self):
        s,_,_=prepare(make_rows())
        t=totals(s)
        p=predictions_for_subject(s[0],t)
        self.assertEqual(len(p),3)
        self.assertAlmostEqual(p[0],.5)
    def test_loss_proper_direction(self): self.assertGreater(score(5,5,.3)[0],score(5,5,.8)[0])
    def test_brier(self): self.assertAlmostEqual(score(1,1,.8)[1],.04)
    def test_rng_repro(self):
        self.assertEqual([next(xorshift_random(123)) for _ in range(1)],
                         [next(xorshift_random(123)) for _ in range(1)])
    def test_bootstrap_point_mass(self):
        d=[{'stake':.2,'loss':-.1,'brier':0.01}]*3
        ci=bootstrap_cis(d,100,seed=7)
        self.assertAlmostEqual(ci['stake'][0],.2)
        self.assertAlmostEqual(ci['stake'][1],.2)
    def test_invalid_stake_rejected(self):
        r=make_rows();r[0]['stakes']='5'
        with self.assertRaises(ValueError):prepare(r)
    def test_invalid_copied_rejected(self):
        r=make_rows();r[0]['copied']='2'
        with self.assertRaises(ValueError):prepare(r)
    def test_under_ten_fail_closed(self):
        with self.assertRaises(ValueError):prepare(make_rows(9))
    def test_threshold_45(self):
        r=make_rows(11);r[0]['accurate']='0';r[1]['accurate']='0'
        s,_,c=prepare(r)
        self.assertEqual(c['excluded_accuracy'],1)
    def test_check_exclusion(self):
        r=make_rows(11);r[0]['comprehension_check_repetitions']='9'
        s,_,c=prepare(r)
        self.assertEqual(c['excluded_comprehension'],1)
    def test_missing_omit(self):
        r=make_rows(11);r[0]['copied']=''
        s,_,c=prepare(r)
        self.assertEqual(c['missing_by_required_field']['copied'],1)
    def test_no_causal_claim(self):
        from r064_observational import __doc__
        self.assertIn('no causal claim',__doc__)

if __name__=='__main__':unittest.main()
