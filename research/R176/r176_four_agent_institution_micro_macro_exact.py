"""R176 artificial exact four-agent institutional path-dependence model.

Two separately implemented full-state transition algorithms:
A aggregate count binomial convolution over 10 states.
B individual 4-bit all-outcome enumeration over 32 states.
Only artificial mathematical E1 results; no real history data.
"""
from __future__ import annotations

import itertools
import json
import math
import sys
import unittest
import zipfile
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from pathlib import Path

HERE=Path(__file__).resolve().parent
PROTO=HERE.parent.parent/"protocols/R176_FOUR_AGENT_INSTITUTION_96_LONGRUN_EXACT_ABM_PRESCORE_FREEZE_2026-10-21.md"
RESULT=HERE/"R176_EXACT_RESULTS.json"
ACCEPT=HERE/"R176_FINAL_MACHINE_ACCEPTANCE.json"
ARCH=HERE/"R176_96_FourAgent_Institution_MicroMacro_Exact_Worlds.zip"
MUS=(F(1,8),F(1,4))
BETAS=(F(0),F(1,4))
GAMMAS=(F(0),F(1,2))
DROPOUTS=(F(0),F(1,4))
RULES=("threshold","hysteresis")
START_K=(1,2,3)
HORIZON=12
MACRO_STATES=tuple((k,j) for k in range(5) for j in range(2))
MICRO_STATES=tuple((mask,j) for mask in range(16) for j in range(2))


def worlds():
    return itertools.product(MUS,BETAS,GAMMAS,DROPOUTS,RULES,START_K)


def change_institution(rule,k,j):
    if rule=="threshold":
        return int(k>=3)
    if rule=="hysteresis":
        return 1 if k>=3 else 0 if k<=1 else j
    raise ValueError("unknown institutional rule")


def parameters_ok(mu,beta,gamma,d,rule):
    if not all(F(0)<=v<=F(1) for v in (mu,beta,gamma,d)):
        raise ValueError("invalid parameter")
    if rule not in RULES:
        raise ValueError("invalid institution rule")


def macro_row(k,j,mu,beta,gamma,d,rule):
    """Algorithm A: binomial survivors and converts, no individual bit masks."""
    parameters_ok(mu,beta,gamma,d,rule)
    if k not in range(5) or j not in (0,1):
        raise ValueError("invalid macro state")
    q=1-(1-mu)*(1-beta)**k*(1-gamma)**j
    r=1-d/(1+j)
    out=defaultdict(F)
    for surviving in range(k+1):
        ps=F(math.comb(k,surviving))*r**surviving*(1-r)**(k-surviving)
        for newly in range(4-k+1):
            pn=F(math.comb(4-k,newly))*q**newly*(1-q)**(4-k-newly)
            kk=surviving+newly
            jj=change_institution(rule,kk,j)
            out[(kk,jj)]+=ps*pn
    return {state:prob for state,prob in out.items() if prob}


def micro_row(mask,j,mu,beta,gamma,d,rule):
    """Algorithm B: enumerate all 16 possible next 4-bit population states."""
    parameters_ok(mu,beta,gamma,d,rule)
    if mask not in range(16) or j not in (0,1):
        raise ValueError("invalid micro state")
    k=mask.bit_count()
    out=defaultdict(F)
    for target in range(16):
        prob=F(1)
        for i in range(4):
            was=(mask>>i)&1
            now=(target>>i)&1
            if was:
                p1=1-d/F(j+1)
            else:
                p1=1-(1-mu)*((1-beta)**k)*((1-gamma)**j)
            prob*= p1 if now else 1-p1
        kk=target.bit_count()
        # Separate micro update implementation rather than call aggregate function.
        if rule=="threshold":
            jj=1 if kk>=3 else 0
        elif rule=="hysteresis":
            jj=1 if kk>=3 else (0 if kk<=1 else j)
        else:
            raise ValueError("invalid rule")
        out[(target,jj)]+=prob
    return {state:prob for state,prob in out.items() if prob}


@lru_cache(maxsize=None)
def macro_table(mu,beta,gamma,d,rule):
    return {s:macro_row(*s,mu,beta,gamma,d,rule) for s in MACRO_STATES}


@lru_cache(maxsize=None)
def micro_table(mu,beta,gamma,d,rule):
    return {s:micro_row(*s,mu,beta,gamma,d,rule) for s in MICRO_STATES}


def propagate(dist,table):
    nxt=defaultdict(F)
    for state,pr in dist.items():
        for destination,p in table[state].items():
            nxt[destination]+=pr*p
    ans={s:v for s,v in nxt.items() if v}
    if sum(ans.values(),F(0))!=1:
        raise AssertionError("broken stochastic propagation")
    return ans


def aggregate(micro_dist):
    out=defaultdict(F)
    for (mask,j),p in micro_dist.items():
        out[(mask.bit_count(),j)]+=p
    return {s:p for s,p in out.items() if p}


def count_marginal(row):
    p=defaultdict(F)
    for (k,j),v in row.items():
        p[k]+=v
    return dict(p)


def expectation(row):
    return sum((k*p for (k,j),p in row.items()),F(0))


def institute_frequency(row):
    return sum((p for (k,j),p in row.items() if j==1),F(0))


def build_world(mu,beta,gamma,d,rule,k0):
    macro={ (k0,0):F(1) }
    micro={ ((1<<k0)-1,0):F(1) }
    mt=macro_table(mu,beta,gamma,d,rule)
    it=micro_table(mu,beta,gamma,d,rule)
    path=[]
    for t in range(HORIZON+1):
        if macro!=aggregate(micro):
            raise AssertionError("micro to macro aggregation mismatch")
        path.append({
            "t":t,
            "P_k_J":[str(macro.get(s,F(0))) for s in MACRO_STATES],
            "expected_adopters":str(expectation(macro)),
            "prob_institution_active":str(institute_frequency(macro)),
        })
        if t<HORIZON:
            macro=propagate(macro,mt)
            micro=propagate(micro,it)
    return path


def nonidentification():
    mu,beta,gamma,d=F(1,8),F(1,4),F(1,2),F(1,4)
    r0=macro_row(2,0,mu,beta,gamma,d,"hysteresis")
    r1=macro_row(2,1,mu,beta,gamma,d,"hysteresis")
    e0,e1=expectation(r0),expectation(r1)
    if e0!=F(161,64) or e1!=F(417,128):
        raise AssertionError("prescored positive control no longer matches explicit algebra")
    a=count_marginal(macro_row(2,0,F(1,8),F(1,4),F(0),F(0),"hysteresis"))
    b=count_marginal(macro_row(2,1,F(1,8),F(1,4),F(0),F(0),"hysteresis"))
    if a!=b:
        raise AssertionError("institution independent negative control did not match")
    return {
        "positive_control_mu":"1/8","positive_control_beta":"1/4",
        "positive_control_gamma":"1/2","positive_control_dropout":"1/4",
        "same_count":2,"institution_0_expected_next_count":str(e0),
        "institution_1_expected_next_count":str(e1),
        "difference":str(e1-e0),
        "negative_control_gamma_0_dropout_0_same_next_count_distribution":True,
        "institution_hysteresis_k2_keeps_previous_status":True,
    }


def run():
    params=list(worlds())
    if len(params)!=96:
        raise AssertionError("wrong prescored parameter universe")
    controls=nonidentification()
    rows=[]
    for mu,beta,gamma,d,rule,k0 in params:
        path=build_world(mu,beta,gamma,d,rule,k0)
        rows.append({
            "mu":str(mu),"beta":str(beta),"gamma":str(gamma),
            "dropout":str(d),"rule":rule,"initial_k":k0,
            "time_series":path,
            "micro_32_state_equals_macro_10_state_all_t":True,
        })
    out={
        "research_id":"R176",
        "stage":"ARTIFICIAL_EXACT_MICRO_MACRO_LONGRUN_ABM_E1",
        "protocol":"protocols/"+PROTO.name,
        "full_micro_states":32,"aggregate_states":10,
        "worlds":len(rows),"periods":HORIZON+1,
        "aggregate_probability_cells":len(rows)*(HORIZON+1)*10,
        "parameter_grid":{
            "mu":[str(v) for v in MUS],"beta":[str(v) for v in BETAS],
            "gamma":[str(v) for v in GAMMAS],"dropout":[str(v) for v in DROPOUTS],
            "institution_rules":list(RULES),"initial_adopters":list(START_K),
        },
        "macro_state_order":[f"{k},{j}" for k,j in MACRO_STATES],
        "rows":rows,"hidden_institution_checks":controls,
        "all_independent_micro_macro_exact":True,
        "real_human_or_historical_data_scored":False,
        "new_E2":0,"new_E3":0,
    }
    RESULT.write_text(json.dumps(out,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    acceptance={
        "research_id":"R176","state":"E1_ARTIFICIAL_EXACT_FINITE_ABM_CLOSED_BOUNDED",
        "worlds":96,"periods":13,"macro_states":10,
        "exact_aggregate_probability_cells":12480,
        "micro_states":32,"all_micro_macro_exact":True,
        "hidden_institution_positive_control_diff":controls["difference"],
        "negative_control_same_population_transition":True,
        "real_history_evidence":False,"new_E2":0,"new_E3":0,
        "exact_results_sha256":sha256(RESULT.read_bytes()).hexdigest(),
    }
    ACCEPT.write_text(json.dumps(acceptance,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("R176_MACHINE_ACCEPTANCE",json.dumps(acceptance,sort_keys=True))
    return acceptance


def archive():
    names=[Path(__file__).name,RESULT.name,ACCEPT.name]
    with zipfile.ZipFile(ARCH,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for n in names:
            info=zipfile.ZipInfo(n,date_time=(2026,10,21,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o644<<16
            z.writestr(info,(HERE/n).read_bytes())
        info=zipfile.ZipInfo(PROTO.name,date_time=(2026,10,21,0,0,0))
        info.compress_type=zipfile.ZIP_DEFLATED
        info.external_attr=0o644<<16
        z.writestr(info,PROTO.read_bytes())
    print("R176_ARCHIVE_SHA256",sha256(ARCH.read_bytes()).hexdigest())


class TestFourAgentInstitution(unittest.TestCase):
    def test_world_grid(self):
        self.assertEqual(len(list(worlds())),96)
    def test_state_dimensions(self):
        self.assertEqual((len(MACRO_STATES),len(MICRO_STATES)),(10,32))
    def test_empty_population_can_innovate(self):
        self.assertTrue(any(k>0 for k,j in macro_row(0,0,F(1,8),F(0),F(0),F(0),"threshold")))
    def test_zero_adoption_preserves_zero(self):
        self.assertEqual(macro_row(0,0,F(0),F(0),F(0),F(0),"threshold"),{(0,0):F(1)})
    def test_full_population_can_decay(self):
        r=macro_row(4,0,F(1,8),F(0),F(0),F(1,4),"threshold")
        self.assertTrue(any(k<4 for k,j in r))
    def test_full_population_stays_if_zero_dropout(self):
        self.assertEqual(macro_row(4,1,F(1,8),F(0),F(0),F(0),"threshold"),{(4,1):F(1)})
    def test_threshold_k2_resets_institution(self):
        self.assertEqual(change_institution("threshold",2,1),0)
    def test_hysteresis_k2_keeps_institution(self):
        self.assertEqual(change_institution("hysteresis",2,1),1)
    def test_hysteresis_k1_turns_off(self):
        self.assertEqual(change_institution("hysteresis",1,1),0)
    def test_hysteresis_k3_turns_on(self):
        self.assertEqual(change_institution("hysteresis",3,0),1)
    def test_bad_institution_fails(self):
        with self.assertRaises(ValueError):change_institution("other",2,1)
    def test_bad_parameter_fails(self):
        with self.assertRaises(ValueError):
            macro_row(2,0,F(-1),F(1,4),F(0),F(0),"threshold")
    def test_aggregate_independent_one_step(self):
        for mu,beta,gamma,d,rule in itertools.product(
                MUS,BETAS,GAMMAS,DROPOUTS,RULES):
            for k in range(5):
                for j in (0,1):
                    r=macro_row(k,j,mu,beta,gamma,d,rule)
                    s=micro_row((1<<k)-1,j,mu,beta,gamma,d,rule)
                    self.assertEqual(r,aggregate(s))
    def test_full_matrices_normalized(self):
        for mu,beta,gamma,d,rule in itertools.product(
                MUS,BETAS,GAMMAS,DROPOUTS,RULES):
            self.assertTrue(all(sum(x.values(),F(0))==1
                                for x in macro_table(mu,beta,gamma,d,rule).values()))
            self.assertTrue(all(sum(x.values(),F(0))==1
                                for x in micro_table(mu,beta,gamma,d,rule).values()))
    def test_positive_hidden_state_analytic(self):
        self.assertEqual(nonidentification()["difference"],"95/128")
    def test_zero_gamma_dropout_negative_control(self):
        self.assertTrue(nonidentification()["negative_control_gamma_0_dropout_0_same_next_count_distribution"])
    def test_population_label_permutation_invariant(self):
        for mask in (3,5,6,9,10,12):
            one=aggregate(micro_row(mask,0,F(1,8),F(1,4),F(1,2),F(1,4),"hysteresis"))
            two=macro_row(2,0,F(1,8),F(1,4),F(1,2),F(1,4),"hysteresis")
            self.assertEqual(one,two)
    def test_full_trajectory_length_and_prob(self):
        r=build_world(F(1,8),F(1,4),F(1,2),F(1,4),"hysteresis",2)
        self.assertEqual(len(r),13)
        self.assertTrue(all(sum(F(x) for x in t["P_k_J"])==1 for t in r))
    def test_initial_institution_zero(self):
        r=build_world(F(1,8),F(0),F(0),F(0),"threshold",3)
        self.assertEqual(r[0]["prob_institution_active"],"0")
    def test_individual_transition_all_nonnegative(self):
        x=micro_table(F(1,4),F(1,4),F(1,2),F(1,4),"threshold")
        self.assertTrue(all(all(0<=p<=1 for p in row.values()) for row in x.values()))


if __name__=="__main__":
    if sys.argv[1:]==["--test"]:
        unittest.main(argv=[sys.argv[0]],verbosity=2)
    elif sys.argv[1:]==["--run"]:
        run()
        archive()
    else:
        raise SystemExit("Use --test or --run")
