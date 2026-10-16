"""Phase J deterministic author-eligibility and result-boundary tests. Synthetic only."""
import copy
import unittest
from r065_phase_j_screened_replay import select_eligible, verify_manifest, validate_against_archived

DAYS=(4,21,38,55,72,89,106,123)

def fixture(hi=12,lo=12):
    rows=[]
    for n in range(hi+lo):
        first_high=n<hi
        for j,d in enumerate(DAYS):
            stake='high' if first_high==(j%2==0) else 'low'
            rows.append({'participant_id':f'P{n:03d}', 'accurate':'1',
                         'comprehension_check_repetitions':'0','critical':'1',
                         'day':str(d),'stakes':stake,
                         'counterbalance':'1' if first_high else '0'})
    return rows

class ScreenedSelectionTests(unittest.TestCase):
    def test_fixed_balanced_selection(self):
        out=select_eligible(fixture(),each=12,strict=False)
        self.assertEqual(len(out['first_high']),12)
        self.assertEqual(len(out['first_low']),12)
        self.assertEqual(len(set(out['first_high']+out['first_low'])),24)

    def test_quantile_select_deterministic(self):
        x=select_eligible(fixture(24,24),each=12,strict=False)
        self.assertEqual(x['first_high'][0],'P001')
        self.assertEqual(x['first_high'][-1],'P023')

    def test_selection_invariant_to_row_order(self):
        a=fixture()
        self.assertEqual(select_eligible(a,strict=False),select_eligible(a[::-1],strict=False))

    def test_ineligible_accuracy_exclusion(self):
        a=fixture()
        for row in a:
            if row['participant_id']=='P000':row['accurate']='0'
        with self.assertRaisesRegex(ValueError,'too few eligible'):
            select_eligible(a,strict=False)

    def test_ineligible_repetition_exclusion(self):
        a=fixture()
        for row in a:
            if row['participant_id']=='P012':row['comprehension_check_repetitions']='3'
        with self.assertRaisesRegex(ValueError,'too few eligible'):
            select_eligible(a,strict=False)

    def test_bad_critical_day_rejected(self):
        a=fixture();a[0]['day']='90'
        with self.assertRaisesRegex(ValueError,'diagnostic schedule'):
            select_eligible(a,strict=False)

    def test_bad_counterbalance_rejected(self):
        a=fixture();a[0]['counterbalance']='0'
        with self.assertRaisesRegex(ValueError,'counterbalance'):
            select_eligible(a,strict=False)

    def test_bad_participant_id_rejected(self):
        a=fixture();a[0]['participant_id']='非匿名'
        with self.assertRaisesRegex(ValueError,'non-ASCII'):
            select_eligible(a,strict=False)

    def test_manifest_rejects_bad_sha(self):
        m={'stage':'R065_PHASE_J','selected_subjects':24,'selected_first_high':12,
           'selected_first_low':12,'pinned_raw_git_blobs_in_group_order':['0'*40]*23+['wrong']}
        with self.assertRaisesRegex(ValueError,'blob list'): verify_manifest(m)

    def test_archive_comparison_fail_closed(self):
        now={'subjects':24,'first_high':12,'first_low':12,'models':{
             k:{'counts':{'play':42},'beta_optimal':.4,'in_sample_mean_nll':.6,
                'fixed_beta5_mean_nll':1.5,'looo_mean_nll':.7}
             for k in ('author','boundary')}}
        old={'selected_subjects':24,'models':copy.deepcopy(now['models'])}
        validate_against_archived(now,old)
        old['models']['author']['counts']['play']=43
        with self.assertRaisesRegex(ValueError,'sufficient counts'):validate_against_archived(now,old)

if __name__=='__main__':unittest.main()
