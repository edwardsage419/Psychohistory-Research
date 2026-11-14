"""New R077 boundaries only; original35 permutations are not repeated."""
import unittest
from copy import deepcopy
import math
from integer_certificate import probability,source_counts,_probability,text,integer_scores,MODELS
from fixtures import candidate,original,donor_fixture,one_event_targets,count_shaped_targets,small_identity_fixture

class ReadinessTests(unittest.TestCase):
    def test_hand_source_probability_identity(self):
        source=[(0,0,0,0,1)]+[(0,0,0,0,0)]*8
        for model in range(5):
            with self.subTest(model=model):
                self.assertEqual(probability(source,model,(0,0,0,0,0)),(1,9))
        self.assertEqual(probability(source,5,(0,0,0,0,0)),(1,20))
        self.assertEqual(probability(source,6,(0,0,0,0,0)),(19,20))

    def test_original_donor_interface_matches_independent_history_counts(self):
        for kind in ('identity','varied'):
            fit,source,shape=donor_fixture(kind)
            with self.subTest(kind=kind):
                self.assertEqual((shape['sessions'],shape['humans'],shape['individual_scorable_outcomes']),(12,188,18424))
                self.assertEqual((fit['source_sessions'],fit['train_target_count']),(12,18424))
                C,N,tables=source_counts(source)
                self.assertEqual(fit['train_only_prevalence'],C/N)
                for model,width,table in zip(MODELS[1:5],(1,1,2,4),tables):
                    for code,counts in enumerate(table):
                        state=tuple((code>>i)&1 for i in reversed(range(width)))
                        self.assertEqual(tuple(counts),fit['state_counts'][model].get(state,(0,0)))
                if kind=='identity':self.assertEqual((C,N),(5,18424))

    def test_all_histories_seven_probabilities_and_label_invariance(self):
        for kind in ('identity','varied'):
            fit,source,_=donor_fixture(kind);compiled=source_counts(source)
            p0=candidate.source_prevalence(fit)
            for code in range(16):
                state=tuple((code>>i)&1 for i in (3,2,1,0))
                for model in range(7):
                    for y in (0,1):
                        event=state+(y,)
                        with self.subTest(kind=kind,state=state,model=model,y=y):
                            self.assertEqual(str(candidate.exact_prediction(MODELS[model],event,fit,p0)),text(_probability(compiled,model,event)))

    def test_integer_whole_scores_match_candidate_at_frozen_dimensions(self):
        full=count_shaped_targets()
        self.assertEqual(len(full),15);self.assertEqual(sum(len(x['events']) for x in full.values()),1040)
        self.assertEqual([sum(x['treatment']==tr for x in full.values()) for tr in (0,1)],[7,8])
        small={k:deepcopy(full[k]) for k in ('ARTIFICIAL_TARGET_00','ARTIFICIAL_TARGET_01','ARTIFICIAL_TARGET_07','ARTIFICIAL_TARGET_08','ARTIFICIAL_TARGET_14')}
        for kind in ('identity','varied'):
            fit,source,_=donor_fixture(kind)
            for label,sessions in (('15/1040 count-shaped',full),('unequal five sessions',small)):
                with self.subTest(kind=kind,target=label):
                    self.assertEqual(candidate.score_exact_brier(fit,sessions)['exact_Brier'],integer_scores(source,sessions)['exact_Brier'])

    def test_single_event_identity_old_false_worse_and_false_better(self):
        cases=[(*small_identity_fixture(),(0,0,2)),(*donor_fixture('identity')[:2],(2,0,0))]
        key=MODELS[1]+'_VS_'+MODELS[0]
        for fit,source,expected_old in cases:
            sessions=one_event_targets()
            old=original.score_with_frozen_source(fit,sessions)['paired_differences'][key]
            new=candidate.score_exact_brier(fit,sessions)
            expected=integer_scores(source,sessions)['exact_Brier']
            self.assertEqual(tuple(old[k] for k in ('sessions_better','sessions_equal','sessions_worse')),expected_old)
            self.assertEqual(new['exact_Brier'],expected)
            self.assertEqual(tuple(new['scores']['paired_differences'][key][k] for k in ('sessions_better','sessions_equal','sessions_worse')),(0,2,0))
            p=original.predict(MODELS[0],(0,0,0,0,0),fit);q=original.predict(MODELS[1],(0,0,0,0,0),fit)
            self.assertNotEqual(p,q)
            self.assertNotEqual(math.fsum([original.brier(0,p)]),math.fsum([original.brier(0,q)]))

    def test_independent_session_and_event_reversal(self):
        fit,source,_=donor_fixture('varied');sessions=count_shaped_targets()
        reference=integer_scores(source,sessions)['exact_Brier']
        reversed_events=deepcopy(sessions)
        for v in reversed_events.values():v['events'].reverse()
        self.assertEqual(candidate.score_exact_brier(fit,reversed_events)['exact_Brier'],reference)
        reversed_sessions=dict(reversed(list(sessions.items())))
        self.assertEqual(candidate.score_exact_brier(fit,reversed_sessions)['exact_Brier'],reference)

    def test_invalid_integer_inputs_rejected(self):
        fit,source=small_identity_fixture()
        for bad in ([],[(0,0,0,0,True)],[(0,0,0,0,2)]):
            with self.subTest(bad=bad),self.assertRaises(ValueError):integer_scores(bad,one_event_targets())
        with self.assertRaises(ValueError):integer_scores(source,{})

if __name__=='__main__':unittest.main(verbosity=2)
