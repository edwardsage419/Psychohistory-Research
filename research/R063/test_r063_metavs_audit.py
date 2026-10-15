import unittest
import math
from r063_metavs_audit import Parameters, simulate, illustrative_trace


def P(choice=0, state=1, reward=1):
    return {'kind':'private','state':state,'choice':choice,'reward':reward}


def D(choice=0, state=1):
    return {'kind':'demo','state':state,'choice':choice}


class MechanismTests(unittest.TestCase):
    def setUp(self):
        self.p=Parameters(alpha_private=0.2, alpha_social_or_meta=0.03)

    def test_initial_meta_demos_have_no_effect(self):
        r=simulate([D(),D(),D()],self.p,'metaVS')
        self.assertEqual(r['trace'][-1]['new_q'],[0.,0.])
        self.assertEqual(r['trace'][-1]['effective_social_rate'],0.)

    def test_fixed_updates_before_any_private_trial(self):
        r=simulate([D()],self.p,'VS2')
        self.assertAlmostEqual(r['trace'][0]['new_q'][0],0.03)
        self.assertAlmostEqual(r['trace'][0]['new_q'][1],-0.03)

    def test_private_choice_unlocks_meta_rate(self):
        r=simulate([P(),D()],self.p,'metaVS')
        self.assertAlmostEqual(r['trace'][1]['effective_social_rate'],.03)

    def test_meta_param_is_not_current_learning_rate(self):
        r=simulate([P(),D(),D()],self.p,'metaVS')
        self.assertAlmostEqual(r['trace'][2]['effective_social_rate'],0.0591)
        self.assertNotAlmostEqual(r['trace'][2]['effective_social_rate'],0.03)

    def test_one_concordant_demonstration_matches_fixed_rate_only_here(self):
        a=simulate([P(),D()],self.p,'metaVS')
        b=simulate([P(),D()],self.p,'VS2')
        self.assertEqual(a['trace'][-1]['new_q'],b['trace'][-1]['new_q'])

    def test_second_concordant_demonstration_diverges(self):
        a=simulate([P(),D(),D()],self.p,'metaVS')
        b=simulate([P(),D(),D()],self.p,'VS2')
        self.assertGreater(a['trace'][-1]['new_q'][0],b['trace'][-1]['new_q'][0])

    def test_concordant_closed_form(self):
        r=illustrative_trace()
        self.assertAlmostEqual(r['meta_final_rate'],1-.97**20,places=12)

    def test_discordant_first_demo_no_learning(self):
        r=simulate([P(),D(1)],self.p,'metaVS')
        self.assertEqual(r['trace'][1]['target'],0)
        self.assertEqual(r['trace'][1]['effective_social_rate'],0)
        self.assertEqual(r['trace'][1]['new_q'],r['trace'][1]['old_q'])

    def test_rate_decay_after_concordant_then_discordant(self):
        r=simulate([P(),D(),D(1)],self.p,'metaVS')
        self.assertAlmostEqual(r['trace'][2]['effective_social_rate'],.03*.97)

    def test_separate_state_gate(self):
        r=simulate([P(state=1),D(state=2)],self.p,'metaVS')
        self.assertEqual(r['trace'][-1]['effective_social_rate'],0.)

    def test_private_initial_loss_is_log_two(self):
        r=simulate([P()],self.p,'metaVS')
        self.assertAlmostEqual(r['trace'][0]['private_loss_before_reward'],math.log(2))

    def test_no_current_reward_leakage(self):
        a=simulate([P(reward=1)],self.p,'metaVS')
        b=simulate([P(reward=-1)],self.p,'metaVS')
        self.assertEqual(a['trace'][0]['private_loss_before_reward'],b['trace'][0]['private_loss_before_reward'])
        self.assertNotEqual(a['trace'][0]['new_q'],b['trace'][0]['new_q'])

    def test_changed_past_reward_changes_next_probability(self):
        a=simulate([P(reward=1),P()],self.p,'metaVS')
        b=simulate([P(reward=-1),P()],self.p,'metaVS')
        self.assertNotEqual(a['trace'][1]['private_loss_before_reward'],b['trace'][1]['private_loss_before_reward'])

    def test_perseveration_only_affects_private_choice_probability(self):
        base=Parameters(beta=2,alpha_private=.2,alpha_social_or_meta=.03,perseveration=0)
        changed=Parameters(beta=2,alpha_private=.2,alpha_social_or_meta=.03,perseveration=.5)
        events=[P(),P()]
        a=simulate(events,base,'metaVS')
        b=simulate(events,changed,'metaVS')
        self.assertNotEqual(a['trace'][-1]['private_loss_before_reward'],b['trace'][-1]['private_loss_before_reward'])
        self.assertEqual(a['trace'][-1]['new_q'],b['trace'][-1]['new_q'])

    def test_tie_break_first_action(self):
        p=Parameters(alpha_private=0,alpha_social_or_meta=.5)
        a=simulate([P(choice=1),D(choice=0)],p,'metaVS')
        self.assertEqual(a['trace'][-1]['target'],1)
        b=simulate([P(choice=1),D(choice=1)],p,'metaVS')
        self.assertEqual(b['trace'][-1]['target'],0)

    def test_alpha_equal_one_rate_bounds(self):
        p=Parameters(alpha_social_or_meta=1)
        r=simulate([P(),D(),D()],p,'metaVS')
        self.assertEqual(r['trace'][-1]['effective_social_rate'],1.)

    def test_alpha_zero_equals_fixed_zero(self):
        p=Parameters(alpha_social_or_meta=0)
        events=[P(),D(),D(1),P()]
        self.assertEqual([t['new_q'] for t in simulate(events,p,'metaVS')['trace']], [t['new_q'] for t in simulate(events,p,'VS2')['trace']])

    def test_rate_bounded_for_valid_update_values(self):
        for eta in (0,.001,.1,.5,1):
            p=Parameters(alpha_social_or_meta=eta)
            e=[P()]+[D(i%2) for i in range(30)]
            r=simulate(e,p,'metaVS')
            self.assertTrue(all(0<=t['effective_social_rate']<=1 for t in r['trace']))

    def test_reward_for_demo_is_rejected(self):
        with self.assertRaises(ValueError):
            simulate([{'kind':'demo','state':1,'choice':0,'reward':1}],self.p)

    def test_reordered_future_demo_cannot_change_first_private(self):
        a=simulate([P(),D(),D(1)],self.p,'metaVS')
        b=simulate([P(),D(1),D()],self.p,'metaVS')
        self.assertEqual(a['trace'][0]['private_loss_before_reward'],b['trace'][0]['private_loss_before_reward'])


    def test_symmetric_q_sum_is_zero_for_all_events(self):
        events=[P(),D(),D(1),P(choice=1,reward=1),D(1),P(reward=-1)]
        for family in ('VS2','metaVS'):
            trace=simulate(events,self.p,family)['trace']
            for t in trace:
                self.assertAlmostEqual(sum(t['new_q']),0,places=12)

    def test_no_direct_skill_metadata_in_model(self):
        # Code only accesses state, kind, choice, reward. Labels are inert.
        a=[P(),{**D(), 'demonstrator_skill':'high'}]
        b=[P(),{**D(), 'demonstrator_skill':'low'}]
        self.assertEqual(simulate(a,self.p)['trace'], simulate(b,self.p)['trace'])

    def test_session_reset_when_new_call(self):
        # MATLAB model initializes Q/alpha_sape once per function invocation.
        a=simulate([P(),D()],self.p,'metaVS')
        b=simulate([D()],self.p,'metaVS')
        self.assertGreater(a['trace'][1]['effective_social_rate'],0.)
        self.assertEqual(b['trace'][0]['effective_social_rate'],0.)

if __name__ == '__main__':
    unittest.main(verbosity=2)
