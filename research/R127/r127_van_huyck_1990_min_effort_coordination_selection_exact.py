#!/usr/bin/env python3
"""R127 primary 1990 minimum effort AER and separate 2x2 synthetic risk game.

Van Huyck, Battalio, Beil (1990), AER 80(1):234-248, original pdf:
https://econweb.ucsd.edu/~jandreoni/Econ264/papers/Van%20Huyck%20et%20al%20AER%201990.pdf
Original pp235 Eq(1), 238 Payoff Table A, pp239-242 original Table2.
Cooper et al 1990 AER 80:218-233 only published abstract inspected.
Harsanyi & Selten 1988 original monograph NOT directly inspected; 2x2
risk dominance product rule verified via later explicit theory reference.
Synthetic risk matrices here are NOT original experimental treatments.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
import json


class CoordinationAuditError(ValueError):
    pass


A=F(1,5)
B=F(1,10)
EXPERIMENT_A_OFFSET=F(3,5)
SOURCE_TABLE2={
    1:{"n":16,"period1":(8,3,2,1,1,1,0),"period10":(1,0,0,0,1,1,13)},
    2:{"n":16,"period1":(4,1,3,4,1,3,0),"period10":(1,0,1,0,0,1,13)},
    3:{"n":14,"period1":(4,2,5,3,0,0,0),"period10":(2,0,0,1,0,2,9)},
    4:{"n":15,"period1":(6,0,8,1,0,0,0),"period10":(0,0,0,0,0,2,13)},
    5:{"n":16,"period1":(2,1,9,3,1,0,0),"period10":(0,0,0,1,1,3,11)},
    6:{"n":16,"period1":(5,2,5,2,1,0,1),"period10":(3,0,0,0,0,5,8)},
    7:{"n":14,"period1":(4,1,2,4,1,1,1),"period10":(1,0,0,0,0,3,10)},
}


def efforts(v):
    if type(v) not in (tuple,list) or not 2<=len(v)<=16:
        raise CoordinationAuditError("R127_EXPLICIT_GROUP_SIZE_2_TO_16")
    if any(type(x) is not int or not 1<=x<=7 for x in v):
        raise CoordinationAuditError("R127_EXACT_EFFORT_INTEGER_1_TO_7")
    return tuple(v)


def game_minimum(v):
    return min(efforts(v))


def payoff_vector(v, experimental=True):
    """Original AER 1990 p235 Eq1, with original p238 A $0.60 offset."""
    e=efforts(v)
    if type(experimental) is not bool:
        raise CoordinationAuditError("R127_EXPERIMENTAL_OFFSET_BOOLEAN_REQUIRED")
    minimum=min(e)
    offset=EXPERIMENT_A_OFFSET if experimental else F(0)
    return tuple(offset+A*minimum-B*x for x in e)


def independent_payoff_from_others(own, other_efforts, experimental=True):
    """Independent single-agent formula from MIN OTHER, no group payoff call."""
    if type(own) is not int or not 1<=own<=7:
        raise CoordinationAuditError("R127_OWN_EFFORT_RANGE")
    if type(other_efforts) not in (tuple,list) or not 1<=len(other_efforts)<=15:
        raise CoordinationAuditError("R127_OTHER_EFFORTS_REQUIRED")
    if any(type(x) is not int or not 1<=x<=7 for x in other_efforts):
        raise CoordinationAuditError("R127_OTHER_EFFORT_INVALID")
    if type(experimental) is not bool:
        raise CoordinationAuditError("R127_EXPERIMENTAL_FLAG")
    q=min(other_efforts)
    return (EXPERIMENT_A_OFFSET if experimental else F(0))+A*min(own,q)-B*own


def strict_best_effort_against_others(other_efforts):
    """For 0 < b < a, unique best response = min(other agents' efforts)."""
    if type(other_efforts) not in (tuple,list) or not 1<=len(other_efforts)<=15:
        raise CoordinationAuditError("R127_BEST_RESPONSE_NEEDS_OTHERS")
    if any(type(x) is not int or not 1<=x<=7 for x in other_efforts):
        raise CoordinationAuditError("R127_OTHER_EFFORT_INVALID")
    q=min(other_efforts)
    scores=[independent_payoff_from_others(i,other_efforts) for i in range(1,8)]
    top=max(scores)
    maximizers=tuple(i for i,z in enumerate(scores,1) if z==top)
    if maximizers!=(q,):
        raise CoordinationAuditError("R127_ORIGINAL_EQUATION_UNIQUE_BEST_RESPONSE_FAILED")
    return q


def strict_pure_nash_minimum_effort(v):
    e=efforts(v)
    return all(strict_best_effort_against_others(e[:i]+e[i+1:])==x
               for i,x in enumerate(e))


def min_effort_security_and_payoff_rank():
    all_eq=[]
    securities=[]
    for choice in range(1,8):
        same=payoff_vector((choice,)*2)[0]
        all_eq.append(same)
        security=independent_payoff_from_others(choice,(1,))
        securities.append(security)
    return {
        "all_equal_profiles_are_strict_Nash":all(
            strict_pure_nash_minimum_effort((i,)*3) for i in range(1,8)),
        "equal_equilibrium_payoffs":[str(x) for x in all_eq],
        "own_choices_1_to7_worst_case_payoffs":[str(x) for x in securities],
        "unique_maximin_security_effort":securities.index(max(securities))+1,
        "source_payoff_dominant_effort":7,
        "source_payoff_A_all7":str(all_eq[-1]),
        "source_payoff_A_all1":str(all_eq[0]),
    }


def original_payoff_table_A():
    """Full source 1990 p238 Payoff Table A legal triangular cells.

    Row own effort e in 1..7, column group minimum m<=e.
    Invalid m>e is marked absent, not populated with imaginary payoffs.
    """
    return {str(e):{
        str(m):(str(EXPERIMENT_A_OFFSET+A*m-B*e) if m<=e else None)
        for m in range(1,8)
    } for e in range(1,8)}


def published_1990_table2_verification():
    """Independently sum PRINTED counts; no invented person transitions."""
    total=0
    first7=0
    first1=0
    final1=0
    last_minimum_by_experiment={}
    first_minimum_by_experiment={}
    for ex in range(1,8):
        data=SOURCE_TABLE2[ex]
        n=data["n"]
        first=data["period1"]
        last=data["period10"]
        if len(first)!=7 or len(last)!=7 or any(type(x) is not int or x<0 for x in first+last):
            raise CoordinationAuditError("R127_PRIMARY_TABLE2_MALFORMED_COUNTS")
        if sum(first)!=n or sum(last)!=n:
            raise CoordinationAuditError("R127_SOURCE_TABLE2_SESSION_COUNT_NOT_CLOSED")
        total+=n
        first7+=first[0]
        first1+=first[-1]
        final1+=last[-1]
        first_minimum_by_experiment[str(ex)]=min(
            effort for j,effort in enumerate(range(7,0,-1)) if first[j]>0)
        last_minimum_by_experiment[str(ex)]=min(
            effort for j,effort in enumerate(range(7,0,-1)) if last[j]>0)
    if (total,first7,first1,final1)!=(107,33,2,77):
        raise CoordinationAuditError("R127_PRIMARY_TABLE2_PRINTED_COUNTS_DO_NOT_AGREE")
    return {
        "published_original_article":"Van Huyck et al AER 1990 pp239-242 Table2 Treatment A",
        "experiment_sizes":[SOURCE_TABLE2[i]["n"] for i in range(1,8)],
        "source_reported_human_participants_not_reanalyzed":total,
        "original_published_aggregate_first_period_choice_7":first7,
        "original_published_aggregate_first_period_choice_1":first1,
        "original_published_aggregate_final_period_choice_1":final1,
        "period1_group_minimums":first_minimum_by_experiment,
        "period10_group_minimums":last_minimum_by_experiment,
        "published_text_period10_choice_1_percent_rounded":72,
        "published_text_period1_choice_7_percent_rounded":31,
        "individual_level_transition_matrix_identified_from_printed_counts":False,
        "new_real_human_E2_prediction_scores":0,
        "only_period1_and_period10_tables_entered":True,
    }


def exhaustive_original_min_effort_payoff_audit():
    """7^n all effort profiles (n2..4), n*7 candidate personal deviations.

    Independent best-reply and per-person published Eq1 exact values checked
    at EVERY 75,117 mathematically valid deviation-payoff comparison.
    """
    counts={}
    deviation_total=0
    eqs={}
    for n in range(2,5):
        n_profiles=0
        strict_eq=0
        for v in product(range(1,8),repeat=n):
            actual=payoff_vector(v)
            expected_min=min(v)
            for i,own in enumerate(v):
                others=v[:i]+v[i+1:]
                if actual[i]!=independent_payoff_from_others(own,others):
                    raise CoordinationAuditError("R127_PAYOFF_INDEPENDENT_EXACT_DISAGREEMENT")
                q=min(others)
                for trial in range(1,8):
                    next_vec=v[:i]+(trial,)+v[i+1:]
                    eq_path=payoff_vector(next_vec)[i]
                    independent=independent_payoff_from_others(trial,others)
                    analytic=EXPERIMENT_A_OFFSET+A*min(trial,q)-B*trial
                    if eq_path!=independent or eq_path!=analytic:
                        raise CoordinationAuditError("R127_INDEPENDENT_PAYOFF_ROUNDTRIP_FAILED")
                    if trial==q and any(
                        independent_payoff_from_others(other,others)>=independent
                        for other in range(1,8) if other!=q):
                        raise CoordinationAuditError("R127_SOURCE_UNIQUE_BEST_REPLY_FAILED")
                    deviation_total+=1
                if actual[i]!=EXPERIMENT_A_OFFSET+A*expected_min-B*own:
                    raise CoordinationAuditError("R127_PUBLISHED_EQ1_WRONG")
            expected_eq=(len(set(v))==1)
            if strict_pure_nash_minimum_effort(v)!=expected_eq:
                raise CoordinationAuditError("R127_NASH_SET_NOT_ALL_EQUAL_ONLY")
            if expected_eq:
                strict_eq+=1
            n_profiles+=1
        if n_profiles!=7**n or strict_eq!=7:
            raise CoordinationAuditError("R127_SMALL_GAME_EXHAUSTION_COUNT_DRIFT")
        counts[str(n)]=n_profiles
        eqs[str(n)]=strict_eq
    if deviation_total!=75117 or sum(counts.values())!=2793:
        raise CoordinationAuditError("R127_FULL_MIN_EFFORT_DEVIATIONS_NOT_COMPLETE")
    return {
        "exact_profiles_by_group_size":counts,
        "strict_diagonal_Nash_by_group_size":eqs,
        "all_original_payoff_profiles":sum(counts.values()),
        "all_exact_individual_candidate_deviations":deviation_total,
        "real_person_level_observations":0,
    }


def validate_symmetric_game(a,b,c,d):
    """Symmetric row payoff matrix [[a,b],[c,d]], each exact Fraction.

    Cell row A col B=(b,c); row B col A=(c,b). Symmetry DOES NOT
    mean all row payoff cells b=c!
    """
    vals=(a,b,c,d)
    if any(type(x) is not F for x in vals):
        raise CoordinationAuditError("R127_SYMMETRIC_GAME_EXACT_FRACTIONS_ONLY")
    return vals


def bimatrix_payoffs(a,b,c,d):
    a,b,c,d=validate_symmetric_game(a,b,c,d)
    return (((a,a),(b,c)),((c,b),(d,d)))


def pure_nash_profiles(a,b,c,d):
    matrix=bimatrix_payoffs(a,b,c,d)
    equilibria=[]
    for i in range(2):
        for j in range(2):
            row_payoff,col_payoff=matrix[i][j]
            if row_payoff>=matrix[1-i][j][0] and col_payoff>=matrix[i][1-j][1]:
                equilibria.append((i,j))
    return tuple(equilibria)


def strict_diagonal_coordination(a,b,c,d):
    a,b,c,d=validate_symmetric_game(a,b,c,d)
    return a>c and d>b


def payoff_risk_selection(a,b,c,d):
    """Two-person TWO STRICT diagonal pure Nash equilibria only.

    Risk product for (A,A)=(a-c)^2 and (B,B)=(d-b)^2
    on symmetric 2x2. This is NOT multi-player min-effort risk dominance.
    """
    a,b,c,d=validate_symmetric_game(a,b,c,d)
    if not strict_diagonal_coordination(a,b,c,d):
        raise CoordinationAuditError("R127_TWO_STRICT_COORDINATION_EQUILIBRIA_REQUIRED")
    if pure_nash_profiles(a,b,c,d)!=((0,0),(1,1)):
        raise CoordinationAuditError("R127_ONLY_TWO_DIAGONAL_PURE_EQUILIBRIA_EXPECTED")
    aa=a-c
    bb=d-b
    aa_prod=aa*aa
    bb_prod=bb*bb
    risk="A" if aa_prod>bb_prod else "B" if aa_prod<bb_prod else "TIE"
    payoff="A" if a>d else "B" if a<d else "TIE"
    belief_threshold=bb/(aa+bb)
    if not 0<belief_threshold<1:
        raise CoordinationAuditError("R127_INNER_MIXED_THRESHOLD_MISSING")
    return {
        "pure_nash_profiles":((0,0),(1,1)),
        "A_deviation_loss":aa,"B_deviation_loss":bb,
        "A_loss_product":aa_prod,"B_loss_product":bb_prod,
        "risk_dominant":risk,"payoff_dominant":payoff,
        "belief_opponent_A_indifference":belief_threshold,
    }


def independent_expected_payoff_differences(a,b,c,d,q):
    """Calculate both strategy EXPECTED PAYOFFS directly from payoff matrix."""
    a,b,c,d=validate_symmetric_game(a,b,c,d)
    if type(q) is not F or not 0<=q<=1:
        raise CoordinationAuditError("R127_BELIEF_EXACT_PROBABILITY_0_TO_1")
    cells=bimatrix_payoffs(a,b,c,d)
    uA=q*cells[0][0][0]+(1-q)*cells[0][1][0]
    uB=q*cells[1][0][0]+(1-q)*cells[1][1][0]
    return {"expected_A":uA,"expected_B":uB,"best":"A" if uA>uB else "B" if uB>uA else "TIE"}


def frozen_two_person_examples():
    conflict=(F(5),F(0),F(4),F(4))
    risk_tie=(F(4),F(0),F(2),F(2))
    c=payoff_risk_selection(*conflict)
    t=payoff_risk_selection(*risk_tie)
    return {
        "project_synthetic_conflict_payoff_matrix": [
            [[str(v) for v in cell] for cell in row] for row in bimatrix_payoffs(*conflict)
        ],
        "conflict_payoff_dominant":c["payoff_dominant"],
        "conflict_risk_dominant":c["risk_dominant"],
        "conflict_payoff_AA":"5","conflict_payoff_BB":"4",
        "conflict_deviation_AA":str(c["A_deviation_loss"]),
        "conflict_deviation_BB":str(c["B_deviation_loss"]),
        "conflict_loss_products":[str(c["A_loss_product"]),str(c["B_loss_product"])],
        "conflict_belief_opponent_A_indifference":str(c["belief_opponent_A_indifference"]),
        "conflict_when_belief_A_three_quarters":independent_expected_payoff_differences(*conflict,F(3,4))["best"],
        "conflict_when_belief_A_nine_tenths":independent_expected_payoff_differences(*conflict,F(9,10))["best"],
        "equal_risk_products":tuple(str(v) for v in (t["A_loss_product"],t["B_loss_product"])),
        "equal_risk_selection":t["risk_dominant"],
        "equal_risk_payoff_dominant":t["payoff_dominant"],
        "not_the_Van_Huyck_1990_n_agent_original_game":True,
    }


def exhaustive_two_player_symmetric_payoff_grid():
    """All integer a,b,c,d in 0..5 as Fraction, strict dual Nash only.

    This is a FINITE SYNTHETIC logical audit, not real experiment actions.
    """
    total=0
    strict_games=0
    disagreements=0
    ties=0
    for a,b,c,d in product(range(6),repeat=4):
        total+=1
        vals=tuple(F(v) for v in (a,b,c,d))
        eqs=pure_nash_profiles(*vals)
        if not (a>c and d>b):
            continue
        if eqs!=((0,0),(1,1)):
            raise CoordinationAuditError("R127_COHERENCE_NASH_EXHAUSTION_FAIL")
        s=payoff_risk_selection(*vals)
        strict_games+=1
        if s["risk_dominant"]=="TIE":
            ties+=1
        if s["risk_dominant"]!="TIE" and s["payoff_dominant"]!="TIE" and s["risk_dominant"]!=s["payoff_dominant"]:
            disagreements+=1
        threshold=s["belief_opponent_A_indifference"]
        at=independent_expected_payoff_differences(*vals,threshold)
        if at["best"]!="TIE":
            raise CoordinationAuditError("R127_2X2_THRESHOLD_NOT_INDIFFERENT")
        qlo=threshold/2
        qhi=(threshold+F(1))/2
        if independent_expected_payoff_differences(*vals,qlo)["best"]!="B":
            raise CoordinationAuditError("R127_2X2_BELOW_THRESHOLD_BR_FAIL")
        if independent_expected_payoff_differences(*vals,qhi)["best"]!="A":
            raise CoordinationAuditError("R127_2X2_ABOVE_THRESHOLD_BR_FAIL")
        if pure_nash_profiles(*(v+F(5) for v in vals))!=eqs:
            raise CoordinationAuditError("R127_COMMON_PAYOFF_OFFSET_CHANGES_NASH")
        plus=payoff_risk_selection(*(v+F(5) for v in vals))
        scale=payoff_risk_selection(*(v*F(3,2) for v in vals))
        if (plus["risk_dominant"],scale["risk_dominant"])!=(s["risk_dominant"],)*2:
            raise CoordinationAuditError("R127_POSITIVE_AFFINE_RISK_SELECTION_INCONSISTENT")
    if total!=1296 or strict_games<=0 or disagreements<=0 or ties<=0:
        raise CoordinationAuditError("R127_TWO_BY_TWO_EXHAUSTION_NOT_COMPLETE")
    return {
        "all_two_by_two_symmetric_integer_payoff_games":total,
        "two_strict_diagonal_Nash_games":strict_games,
        "payoff_vs_risk_strict_conflict_games":disagreements,
        "two_equilibria_risk_tie_games":ties,
        "belief_threshold_and_positive_affine_invariance_checks":True,
        "synthetic_not_original_cooper_1990_person_data":True,
    }


def phase_receipt():
    return {
        "research_id":"R127","catalogue_id":"05-003",
        "original_1990_AER_primary_fulltext":"https://econweb.ucsd.edu/~jandreoni/Econ264/papers/Van%20Huyck%20et%20al%20AER%201990.pdf",
        "original_AER_source_print_pages_reviewed":[234,235,236,237,238,239,240,241,242,245],
        "source_1990_payoff_table_A":original_payoff_table_A(),
        "original_source_selection_result":min_effort_security_and_payoff_rank(),
        "source_published_1990_human_Treatment_A_aggregates_only":published_1990_table2_verification(),
        "project_min_effort_all_profiles":exhaustive_original_min_effort_payoff_audit(),
        "project_synthetic_2x2_equilibrium_selection":frozen_two_person_examples(),
        "project_synthetic_2x2_full_small_payoff_grid":exhaustive_two_player_symmetric_payoff_grid(),
        "original_Cooper1990_full_experimental_tables_reanalyzed":False,
        "original_Harsanyi_Selten1988_full_monograph_directly_read":False,
        "new_person_level_human_E2_predictions_scored":0,
        "R073":"FROZEN","PESEN_v0_1":"FROZEN",
    }


if __name__=="__main__":
    print(json.dumps(phase_receipt(),sort_keys=True,indent=2))
