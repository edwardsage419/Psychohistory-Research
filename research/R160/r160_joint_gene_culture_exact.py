"""R160 project-authored G/C frequency coupling, exact Fraction and enumeration.

Artificial neutral labels G0/G1 and C0/C1: NO genetic inference about people.
These are NOT Feldman/Laland or Zhivotovsky original full equations.
"""
from __future__ import annotations

import json
from fractions import Fraction as F
from itertools import product

INITIAL_TABLES = (
    (F(1,4),F(1,4),F(1,4),F(1,4)),
    (F(3,8),F(1,8),F(1,8),F(3,8)),
    (F(1,8),F(3,8),F(3,8),F(1,8)),
    (F(1,2),F(0),F(1,2),F(0)),
    (F(0),F(1,2),F(0),F(1,2)),
)
SELECTION = (F(0), F(1,2))
IMITATION = (F(0), F(1,2), F(1))
HORIZONTAL = (F(0), F(1,4))
HORIZON = 4


def unit(x: object, label: str) -> F:
    if isinstance(x, bool) or not isinstance(x,(int,F)):
        raise ValueError(f"{label}: int or Fraction required")
    x=F(x)
    if not 0 <= x <= 1:
        raise ValueError(f"{label}: outside unit interval")
    return x


def checked_table(values) -> tuple[F,F,F,F]:
    if not isinstance(values, (tuple,list)) or len(values)!=4:
        raise ValueError("joint table needs exactly four (00,01,10,11) entries")
    cells=tuple(unit(x,"joint table cell") for x in values)
    if sum(cells,F(0)) != F(1):
        raise ValueError("joint distribution must sum exactly to one")
    return cells


def checked_params(s,h,u):
    return unit(s,"interaction selection"),unit(h,"conformism"),unit(u,"horizontal fraction")


def marginals(cells):
    p00,p01,p10,p11=checked_table(cells)
    g=p10+p11
    c=p01+p11
    d=p11-g*c
    return g,c,d


def majority_polynomial(p):
    p=unit(p,"culture rate")
    return 3*p*p-2*p*p*p


def step_direct(cells,s,h,u):
    """Project-defined: selection of 11, then culture replacement by population q."""
    p00,p01,p10,p11=checked_table(cells)
    s,h,u=checked_params(s,h,u)
    z=F(1)+s*p11
    a00,a01,a10,a11=(p00/z,p01/z,p10/z,(1+s)*p11/z)
    c=a01+a11
    q=(1-h)*c+h*majority_polynomial(c)
    g0=a00+a01
    g1=a10+a11
    next00=(1-u)*a00+u*g0*(1-q)
    next01=(1-u)*a01+u*g0*q
    next10=(1-u)*a10+u*g1*(1-q)
    next11=(1-u)*a11+u*g1*q
    return checked_table((next00,next01,next10,next11))


def step_enumerated(cells,s,h,u):
    """Independent 4-class weighted enumeration with 8 demonstration configurations."""
    original=checked_table(cells)
    s,h,u=checked_params(s,h,u)
    weighted={}
    normalizer=F(0)
    for gene in (0,1):
        for cultural in (0,1):
            mass=original[2*gene+cultural]
            fitness=F(1)+(s if gene==1 and cultural==1 else F(0))
            weighted[(gene,cultural)]=mass*fitness
            normalizer+=mass*fitness
    selected={key:value/normalizer for key,value in weighted.items()}
    v=selected[(0,1)]+selected[(1,1)]
    majority=F(0)
    for three in product((0,1),repeat=3):
        ones=sum(three)
        if ones>=2:
            majority+=v**ones*(1-v)**(3-ones)
    copied=(1-h)*v+h*majority
    output={}
    for g in (0,1):
        gene_total=selected[(g,0)]+selected[(g,1)]
        for c in (0,1):
            probability=copied if c==1 else F(1)-copied
            output[(g,c)]=(1-u)*selected[(g,c)]+u*gene_total*probability
    return checked_table(tuple(output[(g,c)] for g in (0,1) for c in (0,1)))


def direct_history(cells,s,h,u,horizon=HORIZON):
    if isinstance(horizon,bool) or not isinstance(horizon,int) or horizon<0:
        raise ValueError("invalid time horizon")
    initial=checked_table(cells)
    checked_params(s,h,u)
    out=[initial]
    for _ in range(horizon):
        out.append(step_direct(out[-1],s,h,u))
    return tuple(out)


def independent_history(cells,s,h,u,horizon=HORIZON):
    if isinstance(horizon,bool) or not isinstance(horizon,int) or horizon<0:
        raise ValueError("invalid time horizon")
    initial=checked_table(cells)
    checked_params(s,h,u)
    out=[initial]
    for _ in range(horizon):
        out.append(step_enumerated(out[-1],s,h,u))
    return tuple(out)


def result_document():
    worlds=[]
    for ii,initial in enumerate(INITIAL_TABLES):
        for si,s in enumerate(SELECTION):
            for hi,h in enumerate(IMITATION):
                for ui,u in enumerate(HORIZONTAL):
                    direct=direct_history(initial,s,h,u)
                    separate=independent_history(initial,s,h,u)
                    if direct!=separate:
                        raise AssertionError("exact direct and enumerated trajectories differ")
                    ledger=[]
                    for t,table in enumerate(direct):
                        gene,culture,association=marginals(table)
                        ledger.append({
                            "t":t,
                            "joint_00_01_10_11":[str(x) for x in table],
                            "G1_fraction":str(gene),
                            "C1_fraction":str(culture),
                            "gene_culture_association_D":str(association)
                        })
                    worlds.append({
                        "id":f"i{ii}_s{si}_h{hi}_u{ui}",
                        "s":str(s),"h":str(h),"u":str(u),
                        "two_independent_exact_methods_equal":True,
                        "points":ledger,
                    })
    if len(worlds)!=60 or len({x["id"] for x in worlds})!=60:
        raise AssertionError("frozen scenario identity violation")
    positive=step_direct(INITIAL_TABLES[1],F(1,2),0,0)
    negative=step_direct(INITIAL_TABLES[2],F(1,2),0,0)
    pos_g,_,_=marginals(positive)
    neg_g,_,_=marginals(negative)
    if pos_g!=F(11,19) or neg_g!=F(9,17):
        raise AssertionError("prespecified association contrast not met")
    return {
        "research_id":"R160",
        "evidence_level":"E1_SYNTHETIC_TWO_BINARY_TRAIT_ALGEBRA_ONLY",
        "original_gene_culture_equations_recreated":False,
        "real_genetic_or_cultural_data_used":False,
        "human_population_predictions":False,
        "main_worlds":60,"timestamps_per_world":5,
        "initial_distributions": [[str(x) for x in row] for row in INITIAL_TABLES],
        "worlds":worlds,
        "frozen_controls":{
            "same_marginals_opposite_association_before_selection": ["1/8","-1/8"],
            "genetic_G1_after_selection_positive_association":str(pos_g),
            "genetic_G1_after_selection_negative_association":str(neg_g),
            "s_zero_I1_u_quarter_D_at_t1":str(marginals(direct_history(INITIAL_TABLES[1],0,1,F(1,4))[1])[2]),
            "s_zero_I2_u_quarter_D_at_t1":str(marginals(direct_history(INITIAL_TABLES[2],0,1,F(1,4))[1])[2]),
            "no_C1_origin_stays_absent":all(marginals(x)[1]==0 for x in direct_history(INITIAL_TABLES[3],F(1,2),1,F(1,4))),
            "all_C1_origin_stays_unity":all(marginals(x)[1]==1 for x in direct_history(INITIAL_TABLES[4],F(1,2),1,F(1,4)))
        },
    }


def main():
    print(json.dumps(result_document(),sort_keys=True,indent=2,ensure_ascii=False))


if __name__=="__main__":
    main()
