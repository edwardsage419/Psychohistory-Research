#!/usr/bin/env python3
"""R126 finite VCM vs costly punishment mathematical audit, not raw human E2.

Firsthand Fehr & Gaechter 2000 AER 90(4) pp 980-994
DOI 10.1257/aer.90.4.980; MIT-held original printed pp 981-985.
Eq(1) MPCR 0.4, endowment 20, n=4; Eq(2) punishment percentage cap.
Table 2 exact NONLINEAR punishment cost, Table 3 published Stranger means.
Do NOT conflate with R105 2024 commons extraction E2 experiment.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
import json


class PGGAuditError(ValueError):
    pass


N=4
ENDOWMENT=20
ALPHA=F(2,5)
PUNISHMENT_COST=(0,1,2,4,6,9,12,16,20,25,30)
TABLE3_PRINTED_SESSIONS={
    1:(F(27,10),F(109,10),F(13,10),F(98,10)),
    2:(F(4),F(129,10),F(23,10),F(143,10)),
    3:(F(9,2),F(107,10),F(2),F(131,10)),
}
TABLE3_PRINTED_MEAN=(F(37,10),F(115,10),F(19,10),F(123,10))


def _contributions(g):
    if type(g) not in (tuple,list) or len(g)!=N:
        raise PGGAuditError("R126_FOUR_EXPLICIT_CONTRIBUTIONS_REQUIRED")
    if any(type(v) is not int or not 0<=v<=ENDOWMENT for v in g):
        raise PGGAuditError("R126_INTEGER_TOKEN_CONTRIBUTION_0_TO_20_REQUIRED")
    return tuple(g)


def _punishment(points):
    if type(points) not in (tuple,list) or len(points)!=N:
        raise PGGAuditError("R126_FOUR_BY_FOUR_POINT_MATRIX_REQUIRED")
    rows=[]
    for i,row in enumerate(points):
        if type(row) not in (tuple,list) or len(row)!=N:
            raise PGGAuditError("R126_FOUR_BY_FOUR_POINT_MATRIX_REQUIRED")
        if any(type(v) is not int or not 0<=v<=10 for v in row):
            raise PGGAuditError("R126_INTEGRAL_SENT_PUNISHMENT_0_TO_10")
        if row[i]!=0:
            raise PGGAuditError("R126_SELF_PUNISHMENT_FORBIDDEN")
        rows.append(tuple(row))
    return tuple(rows)


def stage1_payoff(g):
    """Verbatim first-stage AER p982 Eq(1), individual."""
    v=_contributions(g)
    common=ALPHA*sum(v)
    return tuple(F(ENDOWMENT-gi)+common for gi in v)


def independent_stage1_group_surplus(g):
    """Algebraically independent of summing the individual-payoff function."""
    v=_contributions(g)
    return F(N*ENDOWMENT)+(N*ALPHA-F(1))*sum(v)


def independent_marginal_incentives():
    return {
        "one_extra_token_private_gain":ALPHA-1,
        "one_extra_token_total_group_gain":N*ALPHA-1,
        "single_round_selfish_best_contribution":0,
        "first_stage_social_optimum_each_contribution":ENDOWMENT,
        "finite_ten_round_pure_money_common_knowledge_SPNE_contribution":0,
        "finite_ten_round_pure_money_common_knowledge_SPNE_sent_punishment":0,
    }


def punishment_cost(k):
    if type(k) is not int or not 0<=k<=10:
        raise PGGAuditError("R126_TABLE2_COST_INPUT_0_TO_10_INT")
    return F(PUNISHMENT_COST[k])


def effective_received_points(points):
    rows=_punishment(points)
    return tuple(min(10,sum(rows[sender][receiver] for sender in range(N)))
                 for receiver in range(N))


def punishment_payoff(g,points):
    """Exactly source p982 Eq(2), per-target 10% first-payoff cap at ten points."""
    first=stage1_payoff(g)
    rows=_punishment(points)
    received=effective_received_points(rows)
    result=[]
    for i in range(N):
        sent_cost=sum((punishment_cost(rows[i][j]) for j in range(N) if j!=i),F(0))
        result.append(first[i]*(F(1)-F(received[i],10))-sent_cost)
    return tuple(result)


def independent_punishment_group_surplus(g,points):
    """Separate first stage aggregate minus first-payoff losses minus costs.

    Do not call punishment_payoff (the first independent check).
    """
    v=_contributions(g)
    rows=_punishment(points)
    total=independent_stage1_group_surplus(v)
    common=ALPHA*sum(v)
    for target in range(N):
        received=min(10,sum(rows[sender][target] for sender in range(N) if sender!=target))
        base=F(ENDOWMENT-v[target])+common
        total-=base*F(received,10)
    for sender in range(N):
        for receiver in range(N):
            if sender!=receiver:
                total-=F(PUNISHMENT_COST[rows[sender][receiver]])
    return total


def zero_punishment():
    return ((0,0,0,0),)*N


def project_frozen_exact_cases():
    g=(20,20,20,0)
    pts=((0,0,0,1),(0,0,0,2),(0,0,0,0),(0,0,0,0))
    saturated=((0,0,0,6),(0,0,0,7),(0,0,0,10),(0,0,0,0))
    first=stage1_payoff(g)
    punished=punishment_payoff(g,pts)
    cap=punishment_payoff(g,saturated)
    return {
        "all_zero_each_stage1":tuple(str(v) for v in stage1_payoff((0,)*4)),
        "all_zero_stage1_group":str(independent_stage1_group_surplus((0,)*4)),
        "all_twenty_each_stage1":tuple(str(v) for v in stage1_payoff((20,)*4)),
        "all_twenty_stage1_group":str(independent_stage1_group_surplus((20,)*4)),
        "three_twenty_one_zero_stage1":tuple(str(v) for v in first),
        "three_twenty_one_zero_group_stage1":str(independent_stage1_group_surplus(g)),
        "one_and_two_points_sent_stage2_net":tuple(str(v) for v in punished),
        "one_and_two_points_sent_stage2_group":str(independent_punishment_group_surplus(g,pts)),
        "saturated_6_7_10_points_received_total":sum(saturated[i][3] for i in range(N)),
        "saturated_effective_received":effective_received_points(saturated)[3],
        "saturated_sender_costs_total":str(sum((punishment_cost(k) for k in (6,7,10)),F(0))),
        "saturated_target_payoff":str(cap[3]),
        "saturated_group_net_surplus":str(independent_punishment_group_surplus(g,saturated)),
        "private_single_token_marginal":str(ALPHA-1),
        "group_single_token_marginal":str(N*ALPHA-1),
        "punishment_technology_not_fixed_three_to_one":True,
    }


def printed_table3_audit():
    """Printed page985 Table3 values, not person-level behavior or new E2."""
    session_deltas={}
    session_means=[]
    for s in (1,2,3):
        no,yes,last_no,last_yes=TABLE3_PRINTED_SESSIONS[s]
        session_deltas[str(s)]={
            "overall_punishment_minus_no":str(yes-no),
            "final_punishment_minus_no":str(last_yes-last_no),
        }
        session_means.append(TABLE3_PRINTED_SESSIONS[s])
    displayed_session_unweighted=tuple(
        sum((rows[j] for rows in session_means),F(0))/3 for j in range(4)
    )
    if not all(TABLE3_PRINTED_SESSIONS[s][1]>TABLE3_PRINTED_SESSIONS[s][0]
               for s in (1,2,3)):
        raise PGGAuditError("R126_PRIMARY_TABLE3_NOT_HIGHER_IN_ALL_SESSIONS")
    if not all(TABLE3_PRINTED_SESSIONS[s][3]>TABLE3_PRINTED_SESSIONS[s][2]
               for s in (1,2,3)):
        raise PGGAuditError("R126_PRIMARY_TABLE3_NOT_HIGHER_IN_FINAL_ROUND")
    return {
        "source":"Fehr & Gaechter 2000 original AER p985 Table 3 Stranger",
        "individual_level_E2_scores":0,
        "table_sessions_printed_1_decimal":{
            str(s):[str(x) for x in TABLE3_PRINTED_SESSIONS[s]] for s in (1,2,3)
        },
        "source_published_Mean_row":tuple(str(x) for x in TABLE3_PRINTED_MEAN),
        "independent_equal_session_average_of_PRINTED_rows":tuple(
            str(v) for v in displayed_session_unweighted),
        "last_punishment_published_Mean_minus_equal_average_PRINTED_rows":str(
            TABLE3_PRINTED_MEAN[3]-displayed_session_unweighted[3]),
        "last_punishment_printed_row_mean_discrepancy_unresolved":True,
        "session_stranger_differences_from_source_printed_means":session_deltas,
        "published_overall_punishment_contribution_fraction_endowment":str(
            TABLE3_PRINTED_MEAN[1]/ENDOWMENT),
        "published_overall_no_punishment_contribution_fraction_endowment":str(
            TABLE3_PRINTED_MEAN[0]/ENDOWMENT),
        "source_human_subjects_reported_by_authors_not_loaded_as_microdata":112,
        "original_10_round_conditions":True,
        "not_a_reproduction_of_original_Wilcoxon_p_value":True,
    }


def exhaustive_mathematical_incentives():
    """625 project-generated profiles; 4*21 deviations -> 52500 checks.

    No real-world participants, no E2. No punishment here: contribution stage
    is a separate exact subgame. Pure-money SPNE requires a separate assumption.
    """
    profiles=0
    deviations=0
    for original in product((0,5,10,15,20),repeat=N):
        base=stage1_payoff(original)
        if sum(base,F(0))!=independent_stage1_group_surplus(original):
            raise PGGAuditError("R126_GROUP_SURPLUS_INDEPENDENT_ALGORITHMS_DISAGREE")
        for i in range(N):
            others=sum(original)-original[i]
            # Analytic optimal choice is g_i=0 given others' frozen choices.
            best=F(ENDOWMENT)+ALPHA*others
            for gi in range(ENDOWMENT+1):
                temp=list(original)
                temp[i]=gi
                direct=stage1_payoff(temp)[i]
                by_margin=best+(ALPHA-F(1))*gi
                if direct!=by_margin or direct>best:
                    raise PGGAuditError("R126_DEVIATION_VS_ANALYTIC_STAGE1_MISMATCH")
                if gi and not direct<best:
                    raise PGGAuditError("R126_ZERO_NOT_STRICT_BEST_REPLY")
                deviations+=1
        profiles+=1
    if profiles!=625 or deviations!=52500:
        raise PGGAuditError("R126_EXHAUSTIVE_MATH_COVERAGE_WRONG")
    return {"purely_mathematical_contribution_profiles":profiles,
            "player_specific_0_to20_deviation_checks":deviations,
            "all_profitable_individual_deviations_from_zero":0,
            "actual_original_person_records_read":0}


def published_model_receipt():
    return {
        "research_id":"R126","catalogue_id":"05-002",
        "source_original_AER2000_DOI":"10.1257/aer.90.4.980",
        "source_printed_pages_visually_reviewed":[981,982,983,984,985],
        "source_table2_costs":list(PUNISHMENT_COST),
        "source_eq1_eq2_project_exact_fixtures":project_frozen_exact_cases(),
        "source_table3_published_aggregates_and_math":printed_table3_audit(),
        "synthetic_exhaustive":exhaustive_mathematical_incentives(),
        "different_source_than_R105_2024_CPR_Zenodo":True,
        "new_real_person_predictive_E2_scores":0,
        "R073":"FROZEN","PESEN_v0_1":"FROZEN",
    }


if __name__=="__main__":
    print(json.dumps(published_model_receipt(),sort_keys=True,indent=2))
