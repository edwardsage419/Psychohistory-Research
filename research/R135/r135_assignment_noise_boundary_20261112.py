#!/usr/bin/env python3
"""R135 exploratory post-freeze E1 audit: complete reputation erasure.

Ohtsuki & Iwasa (2004), JTB 231:107-120, Eq. 3-10.
Assumes the paper's indirect-observation, infinite-population, shared binary
reputation model. No parameters or outcomes from the 2026-10-20 frozen R135
study are changed. Python standard library only.
"""
from fractions import Fraction as F
from itertools import product
import hashlib
import json
import unittest

B, C = F(2), F(1)
MU_E, MU_A = F(1, 50), F(1, 2)
HALF = F(1, 2)


def bits(num, width):
    return tuple((num >> j) & 1 for j in range(width - 1, -1, -1))


def cell_weights(donor_good, recipient_good):
    return (donor_good * recipient_good,
            donor_good * (1 - recipient_good),
            (1 - donor_good) * recipient_good,
            (1 - donor_good) * (1 - recipient_good))


def intended_help(action_bits, donor_good, recipient_good):
    """Direct independent four-cell expansion of published Eq. (5)-(7)."""
    return sum((F(bit) * weight for bit, weight in
                zip(action_bits, cell_weights(donor_good, recipient_good))), F(0))


def assignment_expectation(norm_bits, action_bits, own_good, opp_good,
                           me=MU_E, ma=MU_A):
    """Eight norm bits are ordered 11C,11D,10C,10D,01C,01D,00C,00D.

    Eq. (3), using conditional intended action and executed defection noise.
    """
    assert len(norm_bits) == 8 and len(action_bits) == 4
    total = F(0)
    for k, weight in enumerate(cell_weights(own_good, opp_good)):
        dc, dd = norm_bits[2 * k], norm_bits[2 * k + 1]
        action_is_c = action_bits[k]
        correct = F(dc if action_is_c else dd)
        executed_c = F(dc) if action_is_c else F(dd)
        # Me flips intended C to D; intended D always executes D.
        intended_transition = ((1 - me) * executed_c + me * F(dd)) if action_is_c else F(dd)
        total += weight * (ma + (1 - 2 * ma) * intended_transition)
    return total


def direct_payoffs(resident, mutant, hr=HALF, hm=HALF, b=B, c=C):
    """Literal source Eq. (5)-(9), with intentional rather than executed help.
    Since execution failures are uniform, actual-payoff comparisons scale by
    the same positive (1-me) and have identical ESS order.
    """
    theta_rr = intended_help(resident, hr, hr)
    theta_rm = intended_help(resident, hr, hm)
    theta_mr = intended_help(mutant, hm, hr)
    return (b * theta_rr - c * theta_rr, b * theta_rm - c * theta_mr)


def mirror_norm(d):
    """Good/Bad swap in all roles and output, retaining C/D action meanings."""
    out = []
    for state in range(4):
        counterpart = 3 - state  # 11<->00 and 10<->01
        out += [1 - d[2*counterpart], 1 - d[2*counterpart+1]]
    return tuple(out)


def mirror_action(p):
    return tuple(p[3-i] for i in range(4))


def uniform_exclusion_margin(ma, b=B, c=C):
    """Lower bound on AllD's payoff advantage against any p!=AllD.

    For ma in (0,1/2], stationary reputations in [ma,1-ma], so
    |h_res - h_AllD| <= 1-2ma. Resident donation rate >= ma^2.
    Recipient-label sensitivity of help is <= 1, hence the difference
    in benefits is <= b(1-2ma). AllD's payoff gain is at least
    c ma^2 - b(1-2ma) (intentional payoff units).
    """
    assert F(0) < ma <= HALF
    return c * ma * ma - b * (1 - 2 * ma)


def audit():
    raw_strict = 0
    directed = 0
    direct_vs_count = 0
    stationary_checks = 0
    near_ties = 0
    strict_by_strategy = [0]*16
    worst_allD_win = None
    norms = [bits(d,8) for d in range(256)]
    strategies = [bits(p,4) for p in range(16)]
    fixed_norms = sum(mirror_norm(d)==d for d in norms)
    fixed_pairs = sum(mirror_norm(d)==d for d in norms) * sum(mirror_action(p)==p for p in strategies)
    for norm in norms:
        assert mirror_norm(mirror_norm(norm)) == norm
        for p_num, resident in enumerate(strategies):
            # At ma=1/2 every update map is exactly 1/2 regardless
            # of original label, recipient label or eight-bit norm.
            for h_old, h_peer in product((F(0), HALF, F(1)), repeat=2):
                assert assignment_expectation(norm, resident, h_old, h_peer) == HALF
                stationary_checks += 1
            all_win = True
            for m_num, mutant in enumerate(strategies):
                if p_num == m_num:
                    continue
                wr, wm = direct_payoffs(resident, mutant)
                expected_gap = C * F(sum(mutant)-sum(resident), 4)
                if wr-wm != expected_gap:
                    raise AssertionError((norm, p_num, m_num, wr, wm, expected_gap))
                direct_vs_count += 1
                directed += 1
                all_win &= wr > wm
                if wr == wm:
                    near_ties += 1
                if p_num == 0:
                    worst_allD_win = (wr-wm if worst_allD_win is None else min(worst_allD_win,wr-wm))
            if all_win:
                raw_strict += 1
                strict_by_strategy[p_num] += 1

    # Independent utility arithmetic at ma=1/2, directly from number of C bits:
    # resident (b-c)*K/4, mutant (b*K/4-c*K_mut/4).
    for p_num, resident in enumerate(strategies):
        for m_num, mutant in enumerate(strategies):
            wr, wm = direct_payoffs(resident,mutant)
            k, km = F(sum(resident),4),F(sum(mutant),4)
            assert wr == (B-C)*k
            assert wm == B*k-C*km

    # Compare exact closed-form sufficient condition without claiming necessity.
    margins={str(v):str(uniform_exclusion_margin(v)) for v in
             (F(2,5),F(11,25),F(9,20),F(23,50),F(49,100),HALF)}
    return {
        "study":"R135 post-freeze signal-erasure and universal noncooperation bound",
        "source":"Ohtsuki & Iwasa (2004) DOI 10.1016/j.jtbi.2004.06.005 Eq.3-10",
        "evidence":"internal exact mathematical E1; no new observational E2/E3",
        "parameters":{"b":"2","c":"1","mu_e":"1/50","mu_a":"1/2"},
        "checked_norms":len(norms),
        "checked_residents":len(norms)*len(strategies),
        "checked_directed_invasions":directed,
        "exact_eq3_transition_erasure_checks":stationary_checks,
        "exact_eq5_to_eq9_vs_algebra_checks":direct_vs_count,
        "raw_strict_ESS_pairs":raw_strict,
        "strict_ESS_by_strategy_ascending_binary_id":strict_by_strategy,
        "zero_payoff_gap_mutant_comparisons":near_ties,
        "min_strict_AllD_win_intended_payoff":str(worst_allD_win),
        "mirror_involution_fixed_norms":fixed_norms,
        "mirror_involution_fixed_total_pairs":fixed_pairs,
        "mirror_orbits_all_4096_pairs":(4096+fixed_pairs)//2,
        "mirror_ESS_orbits_at_half_assignment_error":(256+fixed_norms)//2,
        "uniform_sufficient_bound":"c*mu_a^2 > b*(1-2*mu_a)",
        "bound_margins_cma2_minus_b1minus2ma":margins,
        "b2_c1_exact_bound_threshold":"sqrt(6)-2",
        "notes":[
            "At mu_a=1/2 the H-score of every resident and mutant converges to 1/2.",
            "For any b>0,c>0 and mu_e<1, only AllD can be a strict ESS.",
            "For b=2,c=1, the sufficient universal exclusion bound is positive for mu_a>sqrt(6)-2; it may be conservative.",
            "The original 2026-10-20 mu_a=.02 frozen R135 results are untouched.",
        ]
    }


class Tests(unittest.TestCase):
    def test_random_reputation_erases_all_norms(self):
        for normid in range(256):
            n=bits(normid,8)
            for strategy in range(16):
                p=bits(strategy,4)
                for own in (F(0),F(1,3),HALF,F(4,5),F(1)):
                    for opp in (F(0),F(2,3),F(1)):
                        self.assertEqual(assignment_expectation(n,p,own,opp), HALF)

    def test_mutant_pairwise_analytic_source_eqs(self):
        for p in range(16):
            for m in range(16):
                resident,mutant=bits(p,4),bits(m,4)
                wr,wm=direct_payoffs(resident,mutant)
                self.assertEqual(wr-wm,F(sum(mutant)-sum(resident),4))

    def test_all_4096_x_15_exact_comparisons(self):
        result=audit()
        self.assertEqual(result["checked_directed_invasions"],61440)
        self.assertEqual(result["raw_strict_ESS_pairs"],256)
        self.assertEqual(result["strict_ESS_by_strategy_ascending_binary_id"],[256]+[0]*15)

    def test_mirror_orbits_burnside(self):
        d=[bits(x,8) for x in range(256)]
        p=[bits(x,4) for x in range(16)]
        self.assertEqual(sum(mirror_norm(x)==x for x in d),16)
        self.assertEqual(sum(mirror_action(x)==x for x in p),4)
        self.assertEqual((4096+16*4)//2,2080)
        self.assertEqual((256+16)//2,136)

    def test_uniform_analytic_sufficient_bound(self):
        self.assertLess(uniform_exclusion_margin(F(11,25)),0)
        self.assertEqual(uniform_exclusion_margin(F(9,20)),F(1,400))
        self.assertGreater(uniform_exclusion_margin(F(23,50)),0)
        self.assertEqual(uniform_exclusion_margin(HALF),F(1,4))

    def test_invalid_zero_cost_not_included(self):
        self.assertEqual(uniform_exclusion_margin(HALF,c=F(0)),0)

    def test_two_assignment_values_other_than_half(self):
        # A norm that always assigns good shows erasure is special to ma=1/2.
        norm=(1,)*8
        p=(1,0,1,0)
        self.assertEqual(assignment_expectation(norm,p,HALF,HALF,ma=F(1,50)),F(49,50))
        self.assertEqual(assignment_expectation((0,)*8,p,HALF,HALF,ma=F(1,50)),F(1,50))


if __name__=="__main__":
    import sys
    if "--test" in sys.argv:
        unittest.main(argv=[sys.argv[0]],verbosity=2)
    else:
        print(json.dumps(audit(),indent=2,ensure_ascii=False,sort_keys=True))
