#!/usr/bin/env python3
"""R129 Chicken / Hawk-Dove primary-source boundary and exact theory audit.

FIRSTHAND original: Maynard Smith & Price (1973), Nature 246:15-18,
DOI 10.1038/246015a0, original simulation Table 1 p16 FIVE strategies
and one-decimal mean payoffs. These are NOT the simplified V,C model below.
Original source PDF: https://public.ek-cer.hu/~szabo/EGT20/library/maynard_n73.pdf
The original 15 pairings x 2000 pseudorandom contests are NOT resimulated.
Project's symmetric 2x2 V,C game, coupling and flip noise are mathematical
toy models, NOT original reported human or animal individual observations.
"""
from __future__ import annotations

from fractions import Fraction as F
from itertools import product
import json


class ChickenDomainError(ValueError):
    pass


ORIGINAL_1973_STRATEGIES=(
    "Mouse","Hawk","Bully","Retaliator","Prober-Retaliator"
)
ORIGINAL_1973_SIMULATED_ROUNDED_TABLE=(
    (F("29.0"),F("19.5"),F("19.5"),F("29.0"),F("17.2")),
    (F("80.0"),F("-19.5"),F("74.6"),F("-18.1"),F("-18.9")),
    (F("80.0"),F("4.9"),F("41.5"),F("11.9"),F("11.2")),
    (F("29.0"),F("-22.3"),F("57.1"),F("29.0"),F("23.1")),
    (F("56.7"),F("-20.1"),F("59.4"),F("26.9"),F("21.9")),
)


def original_published_table_audit():
    """Only cite/compare published one-decimal values; not original RNG."""
    a=ORIGINAL_1973_SIMULATED_ROUNDED_TABLE
    if len(a)!=5 or any(len(row)!=5 for row in a):
        raise ChickenDomainError("R129_ORIGINAL_TABLE1_NOT_5_BY_5")
    if any(type(v) is not F or 10*v!=int(10*v) for row in a for v in row):
        raise ChickenDomainError("R129_SOURCE_PRINTED_ONE_DECIMAL_PAYOFF_INVALID")
    best={}
    pure_symmetric=[]
    for j,opponent in enumerate(ORIGINAL_1973_STRATEGIES):
        mx=max(row[j] for row in a)
        best[opponent]=[ORIGINAL_1973_STRATEGIES[i] for i in range(5)
                        if a[i][j]==mx]
        if a[j][j]==mx:
            pure_symmetric.append(opponent)
    if pure_symmetric!=["Retaliator"]:
        raise ChickenDomainError("R129_ROUNDED_TABLE_NASH_AUDIT_DRIFT")
    mouse=0; r=3
    second_order_unresolvable=(a[mouse][r]==a[r][r]
                                and a[r][mouse]==a[mouse][mouse])
    return {
        "published_row_and_column_strategy_order":list(ORIGINAL_1973_STRATEGIES),
        "source_printed_payoff_matrix":[[str(v) for v in row] for row in a],
        "published_table_payoff_cells":25,
        "original_simulated_unordered_strategy_pairs":15,
        "source_reported_stochastic_contests_per_pair":2000,
        "source_simulated_contests_replayed_by_R129":0,
        "best_replies_to_published_rounded_columns":best,
        "pure_symmetric_Nash_from_rounded_table":pure_symmetric,
        "Retaliator_vs_Retaliator":"29",
        "Mouse_vs_Retaliator":"29",
        "Retaliator_vs_Mouse":"29",
        "Mouse_vs_Mouse":"29",
        "strict_second_order_ESS_Retaliator_proven_from_rounded_table":
            not second_order_unresolvable,
        "author_1973_claimed_Retaliator_ESS_but_rounded_table_cannot_verify_strict_refinement":
            second_order_unresolvable,
        "real_human_or_animal_individual_raw_observations_reanalyzed":0,
    }


def _parameters(value,cost):
    if type(value) is not F or type(cost) is not F:
        raise ChickenDomainError("R129_V_C_EXACT_FRACTION_REQUIRED")
    if not (F(0)<value<cost):
        raise ChickenDomainError("R129_STRICT_0_LESS_V_LESS_C_REQUIRED")
    return value,cost


def _q(q):
    if type(q) is not F or not F(0)<=q<=F(1):
        raise ChickenDomainError("R129_EXACT_PROBABILITY_0_TO_1_REQUIRED")
    return q


def _action(x):
    if type(x) is not str or x not in ("H","D"):
        raise ChickenDomainError("R129_ACTION_H_OR_D_REQUIRED")
    return x


def row_payoff_for_pair(value,cost,own,other):
    """Simplified project V,C anti-coordination -- NOT the 1973 5x5 table."""
    v,c=_parameters(value,cost)
    own=_action(own);other=_action(other)
    if own=="H" and other=="H":
        return (v-c)/2
    if own=="H" and other=="D":
        return v
    if own=="D" and other=="H":
        return F(0)
    return v/2


def two_person_payoffs(value,cost,row,col):
    """Symmetric role permutation, without calling pair payoff twice."""
    v,c=_parameters(value,cost)
    row=_action(row);col=_action(col)
    if row=="H" and col=="H":
        return ((v-c)/2,(v-c)/2)
    if row=="H" and col=="D":
        return (v,F(0))
    if row=="D" and col=="H":
        return (F(0),v)
    return (v/2,v/2)


def independently_enumerated_pure_nash(value,cost):
    v,c=_parameters(value,cost)
    out=[]
    for own,opp in product(("H","D"),repeat=2):
        row,col=two_person_payoffs(v,c,own,opp)
        other_own="D" if own=="H" else "H"
        other_opp="D" if opp=="H" else "H"
        row_dev=two_person_payoffs(v,c,other_own,opp)[0]
        col_dev=two_person_payoffs(v,c,own,other_opp)[1]
        if row>=row_dev and col>=col_dev:
            out.append((own,opp))
    return tuple(out)


def expected_from_independent_opponent(value,cost,q):
    """Explicit four pure payoffs, no risk or mixing formulas invoked."""
    v,c=_parameters(value,cost);p=_q(q)
    H=p*row_payoff_for_pair(v,c,"H","H")+(1-p)*row_payoff_for_pair(v,c,"H","D")
    D=p*row_payoff_for_pair(v,c,"D","H")+(1-p)*row_payoff_for_pair(v,c,"D","D")
    return {
        "hawk":H,"dove":D,"difference":H-D,
        "best":"H" if H>D else "D" if D>H else "TIE",
    }


def independent_analytic_expected_difference(value,cost,q):
    v,c=_parameters(value,cost);p=_q(q)
    return (v-c*p)/2


def mixed_nash_solution(value,cost):
    v,c=_parameters(value,cost)
    q=v/c
    payoffs=expected_from_independent_opponent(v,c,q)
    if payoffs["difference"]!=0:
        raise ChickenDomainError("R129_INTERIOR_MIXED_NASH_NOT_INDIFFERENT")
    return {
        "hawk_marginal":q,
        "both_hawk_under_independent_mixing":q*q,
        "each_player_expected_payoff":payoffs["hawk"],
        "two_players_total_expected":2*payoffs["hawk"],
    }


def _joint(law):
    if type(law) not in (tuple,list) or len(law)!=4:
        raise ChickenDomainError("R129_FOUR_EXPLICIT_ORDERED_JOINT_OUTCOMES_REQUIRED")
    a=tuple(_q(x) for x in law)
    if sum(a,F(0))!=1:
        raise ChickenDomainError("R129_JOINT_MASS_NOT_ONE")
    return a


def joint_marginals(law):
    hh,hd,dh,dd=_joint(law)
    return (hh+hd,hh+dh)


def independent_expected_welfare(value,cost,law):
    """Weighted outcomes using direct 2-person payoff code."""
    v,c=_parameters(value,cost)
    masses=_joint(law)
    outcomes=(("H","H"),("H","D"),("D","H"),("D","D"))
    e0=F(0);e1=F(0)
    for mass,(a,b) in zip(masses,outcomes):
        x,y=two_person_payoffs(v,c,a,b)
        e0+=mass*x
        e1+=mass*y
    return {
        "hawk_marginals":joint_marginals(masses),
        "collision_both_hawk":masses[0],
        "row_expected":e0,
        "col_expected":e1,
        "total_expected":e0+e1,
    }


def analytic_group_welfare_from_collision(value,cost,law):
    """Independent algebra: total = V - C*Pr(H,H)."""
    v,c=_parameters(value,cost)
    hh,hd,dh,dd=_joint(law)
    return v-c*hh


def frozen_same_marginals_joint_conflict_examples():
    """Marginal each Hawk exactly 1/3, but collision probability varies."""
    v=F(2);c=F(6)
    cases={
        "independent":(F(1,9),F(2,9),F(2,9),F(4,9)),
        "anti_correlated_role_allocation":(F(0),F(1,3),F(1,3),F(1,3)),
        "perfect_positive_correlation":(F(1,3),F(0),F(0),F(2,3)),
    }
    out={}
    for name,law in cases.items():
        x=independent_expected_welfare(v,c,law)
        if x["hawk_marginals"]!=(F(1,3),F(1,3)):
            raise ChickenDomainError("R129_SAME_HAWK_MARGINALS_NOT_SATISFIED")
        if x["total_expected"]!=analytic_group_welfare_from_collision(v,c,law):
            raise ChickenDomainError("R129_INDEPENDENT_WELFARE_ALGEBRA_DIVERGED")
        out[name]={
            "joint_outcomes_HH_HD_DH_DD":[str(i) for i in law],
            "marginal_each_hawk":"1/3",
            "collision_probability":str(x["collision_both_hawk"]),
            "row_expected":str(x["row_expected"]),
            "column_expected":str(x["col_expected"]),
            "joint_total_expected":str(x["total_expected"]),
        }
    if [out[x]["collision_probability"] for x in cases]!=["1/9","0","1/3"]:
        raise ChickenDomainError("R129_FROZEN_CORRELATED_COLLISION_RATES_INCORRECT")
    return {
        "project_frozen_value":"2","project_frozen_cost":"6",
        "same_individual_hawk_marginal":"1/3",
        "joint_hawk_dependence_models":out,
        "these_joint_laws_are_not_all_claimed_correlated_equilibria":True,
        "real_human_conflict_probability_observed":False,
    }


def flip_noise_distribution(epsilon):
    """From assigned role H,D; each independently flips with prob epsilon."""
    e=_q(epsilon)
    return ((1-e)*e,(1-e)**2,e**2,e*(1-e))


def flip_noise_direct_enumeration(epsilon):
    """Independent event enumeration, not a call to analytic law."""
    e=_q(epsilon)
    observed={}
    for f0,f1 in product((False,True),repeat=2):
        mass=(e if f0 else F(1)-e)*(e if f1 else F(1)-e)
        action0="D" if f0 else "H"
        action1="H" if f1 else "D"
        observed[action0+action1]=mass
    return tuple(observed[x] for x in ("HH","HD","DH","DD"))


def strict_grid_anti_coordination_audit():
    """51 exact V,C cases; 13 opponent H belief points per game=663."""
    game_count=0
    belief_comparisons=0
    baseline_examples=[]
    for v in range(1,7):
        for c in range(v+1,13):
            value,cost=F(v),F(c)
            if independently_enumerated_pure_nash(value,cost)!=(("H","D"),("D","H")):
                raise ChickenDomainError("R129_NOT_TWO_ASYMMETRIC_PURE_NASH")
            qstar=mixed_nash_solution(value,cost)
            if qstar["hawk_marginal"]!=value/cost:
                raise ChickenDomainError("R129_MIXED_NASH_THRESHOLD_NOT_V_OVER_C")
            if expected_from_independent_opponent(value,cost,qstar["hawk_marginal"])["best"]!="TIE":
                raise ChickenDomainError("R129_MIXING_NASH_FAIL")
            for k in range(13):
                q=F(k,12)
                calc=expected_from_independent_opponent(value,cost,q)
                diff=independent_analytic_expected_difference(value,cost,q)
                expected="H" if diff>0 else "D" if diff<0 else "TIE"
                if calc["difference"]!=diff or calc["best"]!=expected:
                    raise ChickenDomainError("R129_EXPECTED_PAYOFF_ANALYTIC_DIFFERENCE_FAIL")
                belief_comparisons+=1
            if (v,c) in ((2,6),(2,12)):
                baseline_examples.append({
                    "V":v,"C":c,
                    "mixed_hawk_probability":str(qstar["hawk_marginal"]),
                    "independent_mixed_both_escalate":str(qstar["both_hawk_under_independent_mixing"])
                })
            game_count+=1
    if game_count!=51 or belief_comparisons!=663:
        raise ChickenDomainError("R129_VC_Q_FULL_GRID_NOT_COMPLETE")
    return {
        "exact_value_cost_games":game_count,
        "exact_opponent_belief_and_payoff_cross_checks":belief_comparisons,
        "pure_Nash_in_every_game":[["H","D"],["D","H"]],
        "representative_cost_sensitivity":baseline_examples,
        "not_empirical_danger_or_cost_estimates":True,
    }


def role_flip_noise_audit():
    verified=0
    max_coll=F(-1)
    coll_max_at=None
    cases={}
    for k in range(13):
        epsilon=F(k,12)
        expected=flip_noise_distribution(epsilon)
        enumerated=flip_noise_direct_enumeration(epsilon)
        if expected!=enumerated or sum(expected,F(0))!=1:
            raise ChickenDomainError("R129_FLIP_NOISE_TWO_ALGORITHMS_DIVERGED")
        if expected[0]>max_coll:
            max_coll=expected[0];coll_max_at=epsilon
        if epsilon in (F(0),F(1,2),F(1)):
            cases[str(epsilon)]={
                "distribution_HH_HD_DH_DD":[str(z) for z in expected],
                "both_hawk_probability":str(expected[0])
            }
        verified+=1
    if verified!=13 or max_coll!=F(1,4) or coll_max_at!=F(1,2):
        raise ChickenDomainError("R129_FLIP_NOISE_COLLISION_EXTREMA_NOT_MATCHED")
    return {
        "exact_flip_probabilities_checked":verified,
        "full_2x2_flip_events_each":4,
        "max_collisions_probability":"1/4",
        "max_collisions_at_independent_flip":"1/2",
        "source_role_initially_H_D":True,
        "special_cases":cases,
        "original_1973_stochastic_simulation_replayed":False,
    }


def frozen_chicken_math():
    v=F(2);c=F(6)
    pure=independently_enumerated_pure_nash(v,c)
    mixed=mixed_nash_solution(v,c)
    return {
        "project_row_payoffs":[[str(row_payoff_for_pair(v,c,x,y)) for y in ("H","D")]
                               for x in ("H","D")],
        "two_asymmetric_strict_pure_Nash":[list(x) for x in pure],
        "project_mixed_hawk_probability":str(mixed["hawk_marginal"]),
        "project_independent_both_hawk":str(mixed["both_hawk_under_independent_mixing"]),
        "project_each_player_mixed_expected":str(mixed["each_player_expected_payoff"]),
        "project_two_player_total_mixed_expected":str(mixed["two_players_total_expected"]),
        "joint_conflict_risk_same_marginals":frozen_same_marginals_joint_conflict_examples(),
        "error_in_assigned_roles":role_flip_noise_audit(),
        "full_theory_cost_and_belief_grid":strict_grid_anti_coordination_audit()
    }


def phase_receipt():
    return {
        "study":"R129","catalogue_id":"05-005",
        "primary_1973_Nature_published_simulation_table":original_published_table_audit(),
        "project_exact_2x2_conflict_games":frozen_chicken_math(),
        "human_microdata_E2_new_prediction_scores":0,
        "R073":"FROZEN","PESEN_v0_1":"FROZEN"
    }


if __name__=="__main__":
    print(json.dumps(phase_receipt(),sort_keys=True,indent=2))
