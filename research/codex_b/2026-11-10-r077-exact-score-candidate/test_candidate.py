"""Synthetic only: catches rounding, tolerance and source/target mixing repairs."""
from pathlib import Path
from copy import deepcopy
from fractions import Fraction as F
from itertools import product
import json
import sys
import unittest
from candidate import score_exact_brier,original
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'research/codex_b/2026-11-10-r077-exact-paired-ties'))
from case import legacy_fit,target_cases
sys.path.insert(0,str(ROOT/'research/codex_b/2026-11-10-r077-score-leakage'))
from score_oracle import expected_scores,validate_scores

PAIR='M3_JOINT_LAST_VS_M1_OWN_LAST'

def from_bins(bins):
    indices=((0,),(1,),(0,1),(0,1,2,3))
    tables={}
    for model,ix in zip(original.MODEL_NAMES[1:5],indices):
        table={}
        for state,(c,n) in bins.items():
            key=tuple(state[i] for i in ix);a,b=table.get(key,(0,0))
            table[key]=(a+c,b+n)
        tables[model]=table
    c=sum(x[0] for x in bins.values());n=sum(x[1] for x in bins.values())
    return {'train_only_prevalence':c/n,'train_target_count':n,'source_sessions':2,'state_counts':tables}

def tiny_case():
    n=2**65
    fit=from_bins({(a,b,0,0):(n//8+(1 if (a,b)==(1,1) else -1 if (a,b)==(1,0) else 0),n//4)
                   for a,b in product((0,1),repeat=2)})
    sessions={f'SYNTHETIC_{tr}':{'treatment':tr,'events':[(1,1,0,0,0)]} for tr in (0,1)}
    return fit,sessions,F(1,n//4+20)+F(1,(n//4+20)**2)

class CandidateTests(unittest.TestCase):
    def test_exact_tie_in_all35_orders(self):
        for positions,sessions in target_cases():
            with self.subTest(positions=positions):
                pair=score_exact_brier(legacy_fit(),sessions)['scores']['paired_differences']['M3_JOINT_LAST_VS_M1_OWN_LAST']
                self.assertEqual((pair['sessions_better'],pair['sessions_equal'],pair['sessions_worse']),(0,2,0))
                self.assertEqual(pair['Brier_delta_all_original_sessions_equal'],0.0)

    def test_integer_tie_certificate_and_order_invariance(self):
        from case import integer_witness
        certificates=[]
        for _,sessions in target_cases():
            integers=integer_witness([e[4] for e in next(iter(sessions.values()))['events']])
            self.assertEqual(integers['integer_squared_sums'],{'candidate':343,'reference':343})
            cert=score_exact_brier(legacy_fit(),sessions)['exact_Brier'];certificates.append(cert)
            for model in ('M1_OWN_LAST','M3_JOINT_LAST'):
                self.assertEqual(cert['models'][model]['all_original_sessions_equal_Brier'],'1/4')
            self.assertEqual(cert['paired_differences'][PAIR]['Brier_delta_all_original_sessions_equal'],'0')
        self.assertTrue(all(c==certificates[0] for c in certificates))

    def test_tiny_genuine_direction_not_rounded_or_toleranced(self):
        fit,sessions,delta=tiny_case()
        self.assertEqual(original.score_with_frozen_source(fit,sessions)['paired_differences'][PAIR]['sessions_equal'],2)
        out=score_exact_brier(fit,sessions)
        self.assertEqual(out['scores']['paired_differences'][PAIR]['sessions_worse'],2)
        self.assertEqual(F(out['exact_Brier']['paired_differences'][PAIR]['Brier_delta_all_original_sessions_equal']),delta)

    def test_complete_scores_against_existing_independent_oracle(self):
        fit=legacy_fit()
        sessions={f'SYNTHETIC_{tr}':{'treatment':tr,'events':[(*state,y) for state in product((0,1),repeat=4) for y in (0,1)]}
                  for tr in (0,1)}
        self.assertGreater(validate_scores(score_exact_brier(fit,sessions)['scores'],expected_scores(fit,sessions)),100)

    def test_log_loss_and_metadata_pass_through_unchanged(self):
        _,sessions=next(target_cases());fit=legacy_fit()
        old=original.score_with_frozen_source(fit,sessions);new=score_exact_brier(fit,sessions)['scores']
        self.assertEqual(set(new),set(old))
        for model in original.MODEL_NAMES:
            self.assertEqual(new['models'][model]['all_original_sessions_equal_log_loss'],old['models'][model]['all_original_sessions_equal_log_loss'])
            for tr in ('0','1'):
                self.assertEqual(new['models'][model]['per_treatment_original_session_equal'][tr]['log_loss'],old['models'][model]['per_treatment_original_session_equal'][tr]['log_loss'])
        for key in set(old)-{'models','paired_differences'}:self.assertEqual(new[key],old[key])

    def test_session_weights_not_event_weights(self):
        sessions={f'SYNTHETIC_{tr}':{'treatment':tr,'events':[(1,1,0,0,tr)]} for tr in (0,1)}
        a=score_exact_brier(legacy_fit(),sessions)
        sessions['SYNTHETIC_1']['events']*=37
        b=score_exact_brier(legacy_fit(),sessions)
        self.assertEqual(a['exact_Brier'],b['exact_Brier'])
        self.assertEqual(a['exact_Brier']['models']['M5_TFT_NOISY']['all_original_sessions_equal_Brier'],'181/400')

    def test_exact_source_ratio_and_unseen_state(self):
        fit=from_bins({(0,0,0,0):(1,3)})
        sessions={f'SYNTHETIC_{tr}':{'treatment':tr,'events':[(1,1,1,1,0)]} for tr in (0,1)}
        cert=score_exact_brier(fit,sessions)['exact_Brier']
        self.assertEqual(cert['source_prevalence'],'1/3')
        for model in original.MODEL_NAMES[:5]:
            self.assertEqual(cert['models'][model]['all_original_sessions_equal_Brier'],'1/9')

    def test_no_target_fit_mutation_or_label_feedback(self):
        fit=legacy_fit();_,sessions=next(target_cases());before=deepcopy((fit,sessions))
        score_exact_brier(fit,sessions)
        self.assertEqual((fit,sessions),before)
        for info in sessions.values():info['events']=[e[:4]+(1-e[4],) for e in info['events']]
        validate_scores(score_exact_brier(fit,sessions)['scores'],expected_scores(fit,sessions))
        self.assertEqual(fit,before[0])

    def test_source_inconsistency_rejected(self):
        _,sessions=next(target_cases())
        for name in ('prevalence','marginal','count','missing'):
            fit=legacy_fit()
            if name=='prevalence':fit['train_only_prevalence']=.6
            elif name=='count':fit['train_target_count']=31
            elif name=='missing':del fit['state_counts']['M2_OPPONENT_LAST']
            else:fit['state_counts']['M1_OWN_LAST'][(1,)]=(9,16)
            with self.subTest(name=name),self.assertRaises(ValueError):score_exact_brier(fit,sessions)

    def test_wrong_source_types_and_degenerate_counts_rejected(self):
        _,sessions=next(target_cases())
        for value in (True,float('nan'),float('inf'),'0.5',F(1,2)):
            fit=legacy_fit();fit['train_only_prevalence']=value
            with self.subTest(value=str(value)),self.assertRaises(ValueError):score_exact_brier(fit,sessions)
        for counts in ((True,8),(0,8.0),(-1,8),(9,8),(0,0)):
            fit=legacy_fit();fit['state_counts']['M4_JOINT_TWO_LAGS'][(1,1,0,0)]=counts
            with self.subTest(counts=counts),self.assertRaises(ValueError):score_exact_brier(fit,sessions)

    def test_invalid_targets_and_missing_treatments_rejected(self):
        _,good=next(target_cases())
        bad=[{}, {'SYNTHETIC_0':good['ARTIFICIAL_SESSION_0']}]
        for value in (True,2):
            s=deepcopy(good);s['ARTIFICIAL_SESSION_0']['treatment']=value;bad.append(s)
        for event in ((1,1,0,0,True),(1,1,0,0,2),(1,1,0,0)):
            s=deepcopy(good);s['ARTIFICIAL_SESSION_0']['events']=[event];bad.append(s)
        s=deepcopy(good);s['ARTIFICIAL_SESSION_0']['events']=[];bad.append(s)
        for sessions in bad:
            with self.subTest(sessions=sessions),self.assertRaises(ValueError):score_exact_brier(legacy_fit(),sessions)

    def test_certificate_json_has_no_target_identifiers_or_rows(self):
        _,sessions=next(target_cases());result=score_exact_brier(legacy_fit(),sessions)
        text=json.dumps(result,allow_nan=False)
        self.assertNotIn('ARTIFICIAL_SESSION',text);self.assertNotIn('events',result['exact_Brier'])
        self.assertEqual(len(result['scores']['models']),7);self.assertEqual(len(result['scores']['paired_differences']),6)

if __name__=='__main__':unittest.main(verbosity=2)
