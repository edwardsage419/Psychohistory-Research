"""R162 artificial attention cue copying and independent ticket enumeration.

No social measurement, people, payoff observations or actual prestige assignment.
Expected success is assigned by a synthetic externally specified correct token.
"""
from __future__ import annotations

import json
from fractions import Fraction as F

PATTERNS=((0,0,0),(1,0,0),(0,1,1),(1,1,1))
FAVORED=(0,1,2)
EXTRA_TICKETS=(0,1,3)
CORRECT_ACTIONS=(0,1)


def checked_pattern(bits):
    if not isinstance(bits,(tuple,list)) or len(bits)!=3:
        raise ValueError("exactly three demonstrator actions required")
    if any(isinstance(x,bool) or not isinstance(x,int) or x not in (0,1) for x in bits):
        raise ValueError("actions must be integer cultural 0 or 1")
    return tuple(bits)


def params(j,extra,correct):
    if isinstance(j,bool) or not isinstance(j,int) or j not in FAVORED:
        raise ValueError("favored index out of range")
    if isinstance(extra,bool) or not isinstance(extra,int) or extra not in EXTRA_TICKETS:
        raise ValueError("extra attention tickets outside frozen range")
    if isinstance(correct,bool) or not isinstance(correct,int) or correct not in CORRECT_ACTIONS:
        raise ValueError("synthetic correct action must be 0 or 1")
    return j,extra,correct


def direct_score(bits,j,extra,correct):
    bits=checked_pattern(bits)
    j,extra,correct=params(j,extra,correct)
    weights=tuple(1+extra if k==j else 1 for k in range(3))
    pA=F(sum(weights[i]*bits[i] for i in range(3)),sum(weights))
    baseline=F(sum(bits),3)
    success=pA if correct==1 else 1-pA
    neutral=baseline if correct==1 else 1-baseline
    return pA,baseline,success,neutral,success-neutral


def ticket_score(bits,j,extra,correct):
    """Explicitly enumerated attention lottery tickets, no calls to direct_score."""
    bits=checked_pattern(bits)
    j,extra,correct=params(j,extra,correct)
    tickets=[0,1,2]
    for _ in range(extra):
        tickets.append(j)
    copied=sum(1 for chosen in tickets if bits[chosen]==1)
    original=sum(1 for chosen in (0,1,2) if bits[chosen]==1)
    chance=F(copied,len(tickets))
    equal=F(original,3)
    correct_count=sum(1 for chosen in tickets if bits[chosen]==correct)
    correct_equal=sum(1 for chosen in (0,1,2) if bits[chosen]==correct)
    success=F(correct_count,len(tickets))
    reference=F(correct_equal,3)
    return chance,equal,success,reference,success-reference


def result_document():
    cases=[]
    for pi,bits in enumerate(PATTERNS):
        for ji,j in enumerate(FAVORED):
            for li,extra in enumerate(EXTRA_TICKETS):
                for ci,correct in enumerate(CORRECT_ACTIONS):
                    direct=direct_score(bits,j,extra,correct)
                    oracle=ticket_score(bits,j,extra,correct)
                    if direct!=oracle:
                        raise AssertionError("two independent Fraction attention lotteries disagree")
                    if not all(F(0)<=v<=F(1) for v in direct[:4]):
                        raise AssertionError("copying probability or success outside bounds")
                    cases.append({
                        "id":f"p{pi}_j{ji}_l{li}_c{ci}",
                        "demonstrator_actions":[int(x) for x in bits],
                        "favored_demonstrator":j,
                        "additional_attention_tickets":extra,
                        "artificial_correct_token":correct,
                        "probability_copy_A":str(direct[0]),
                        "neutral_probability_copy_A":str(direct[1]),
                        "artificial_expected_accuracy":str(direct[2]),
                        "neutral_expected_accuracy":str(direct[3]),
                        "advantage_over_neutral":str(direct[4]),
                        "two_independent_Fraction_routes_identical":True
                    })
    if len(cases)!=72 or len(set(x["id"] for x in cases))!=72:
        raise AssertionError("predeclared 72 input identities missing")
    benefit=direct_score((1,0,0),0,3,1)
    harm=direct_score((1,0,0),0,3,0)
    other=direct_score((1,0,0),1,3,1)
    if (benefit[0],benefit[-1],harm[-1],other[0])!=(F(2,3),F(1,3),F(-1,3),F(1,6)):
        raise AssertionError("frozen prestige-correctness controls mismatch")
    return {
        "research_id":"R162",
        "evidence":"E1_SYNTHETIC_ATTENTION_LOTTERY_ONLY",
        "not_original_prestige_model_or_experiment":True,
        "real_demonstrators_or_cue_observations_used":False,
        "prestige_validity_or_competence_measured":False,
        "case_count":72,
        "worlds":cases,
        "counterexamples":{
            "favored_A_at_extra3_probability_copy_A":str(benefit[0]),
            "favored_A_at_extra3_A_correct_advantage":str(benefit[-1]),
            "favored_A_at_extra3_B_correct_disadvantage":str(harm[-1]),
            "favored_B_at_extra3_probability_copy_A":str(other[0]),
            "no_bonus_cue_unidentifiable":all(
                direct_score(bits,0,0,1)==direct_score(bits,j,0,1)
                for bits in PATTERNS for j in FAVORED),
            "unanimity_cue_unidentifiable":all(
                direct_score(bits,0,l,c)==direct_score(bits,j,l,c)
                for bits in (PATTERNS[0],PATTERNS[3])
                for j in FAVORED for l in EXTRA_TICKETS for c in CORRECT_ACTIONS)
        }
    }


def main():
    print(json.dumps(result_document(),sort_keys=True,indent=2,ensure_ascii=False))


if __name__=="__main__":
    main()
