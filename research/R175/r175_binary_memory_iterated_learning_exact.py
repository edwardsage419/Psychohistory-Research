"""R175: exact artificial serial reproduction of two-state cultural memory.

Original finite-model study inspired by Griffiths/Kalish 2007 and Xu/Griffiths
2010. It is not a reproduction of their original human observations.
Two independent Fraction transition constructions are deliberately retained.
"""
from __future__ import annotations

import csv
import itertools
import json
import math
import sys
import unittest
import zipfile
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path

HERE=Path(__file__).resolve().parent
PROTOCOL=HERE.parent.parent/"protocols/R175_INTERGENERATIONAL_BINARY_MEMORY_72_WORLDS_PRESCORE_FREEZE_2026-10-21.md"
RESULT=HERE/"R175_EXACT_RESULTS.json"
ACCEPTANCE=HERE/"R175_FINAL_MACHINE_ACCEPTANCE.json"
ARCHIVE=HERE/"R175_Intergenerational_72_Binary_Memory_Worlds_Exact.zip"

PRIORS=(Q(1,4),Q(1,2),Q(3,4))
NOISES=(Q(1,4),Q(1,3))
SAMPLE_SIZES=(1,3)
RULES=("posterior_sample","posterior_MAP")
STARTS=("point0","point1","prior")
HORIZON=8


def row_a(pi,eps,n,rule,parent):
    """Method A: group independent signals into binomial sufficient statistics."""
    if rule not in RULES or parent not in (0,1):
        raise ValueError("invalid learner or prior state")
    if not (0<pi<1 and 0<eps<Q(1,2) and n>0):
        raise ValueError("invalid process parameter")
    adopted=Q(0)
    for ones in range(n+1):
        l1=(1-eps)**ones * eps**(n-ones)
        l0=eps**ones * (1-eps)**(n-ones)
        likelihood=l1 if parent==1 else l0
        p_y=Q(math.comb(n,ones))*likelihood
        p1=pi*l1/(pi*l1+(1-pi)*l0)
        report=p1 if rule=="posterior_sample" else Q(int(p1>Q(1,2)))
        adopted+=p_y*report
    return (1-adopted,adopted)


def matrix_a(pi,eps,n,rule):
    return (row_a(pi,eps,n,rule,0),row_a(pi,eps,n,rule,1))


def row_b(pi,eps,n,rule,parent):
    """Method B: enumerate sequences and observation likelihood explicitly.

    Does not share row_a, binomial counts or the posterior computation code.
    """
    total_ones=Q(0)
    for message in itertools.product((0,1),repeat=n):
        parent_likelihood=Q(1)
        hypothesis_likelihood=[Q(1),Q(1)]
        for bit in message:
            parent_likelihood*= (1-eps) if bit==parent else eps
            for state in (0,1):
                hypothesis_likelihood[state]*= (1-eps) if bit==state else eps
        a=pi*hypothesis_likelihood[1]
        b=(1-pi)*hypothesis_likelihood[0]
        if rule=="posterior_sample":
            change=a/(a+b)
        elif rule=="posterior_MAP":
            change=Q(1) if a>b else Q(0)
        else:
            raise ValueError("unknown rule")
        total_ones+=parent_likelihood*change
    return (Q(1)-total_ones,total_ones)


def matrix_b(pi,eps,n,rule):
    return (row_b(pi,eps,n,rule,0),row_b(pi,eps,n,rule,1))


def start_state(pi,start):
    if start=="point0":
        return (Q(1),Q(0))
    if start=="point1":
        return (Q(0),Q(1))
    if start=="prior":
        return (1-pi,pi)
    raise ValueError("unknown start")


def propagate(mat,starting,horizon=HORIZON):
    if horizon<0:
        raise ValueError("negative horizon")
    out=[starting]
    for _ in range(horizon):
        prev=out[-1]
        nextp=(
            prev[0]*mat[0][0]+prev[1]*mat[1][0],
            prev[0]*mat[0][1]+prev[1]*mat[1][1],
        )
        if any(not(0<=p<=1) for p in nextp) or sum(nextp)!=1:
            raise AssertionError("invalid state distribution")
        out.append(nextp)
    return out


def worlds():
    for pi,eps,n,rule,start in itertools.product(
            PRIORS,NOISES,SAMPLE_SIZES,RULES,STARTS):
        yield pi,eps,n,rule,start


def fraction_matrix(mat):
    return [[str(v) for v in row] for row in mat]


def run():
    combos=list(itertools.product(PRIORS,NOISES,SAMPLE_SIZES,RULES))
    world_rows=[]
    matrix_rows=[]
    violations=[]
    for pi,eps,n,rule in combos:
        a=matrix_a(pi,eps,n,rule)
        b=matrix_b(pi,eps,n,rule)
        if a!=b:
            raise AssertionError("independent mathematical implementations disagree")
        for row in a:
            assert sum(row)==1 and all(0<=x<=1 for x in row)
        lam=a[1][1]-a[0][1]
        prior_after=propagate(a,start_state(pi,"prior"))[1][1]
        invariant=prior_after==pi
        if rule=="posterior_sample" and not invariant:
            raise AssertionError("Bayesian posterior sampling must preserve its prior")
        if rule=="posterior_MAP" and not invariant:
            violations.append({"pi":str(pi),"epsilon":str(eps),"n":n,
                               "prior_after_one_generation":str(prior_after)})
        matrix_rows.append({
            "pi":str(pi),"epsilon":str(eps),"n":n,"rule":rule,
            "T_old_to_new":fraction_matrix(a),
            "eigen_memory_persistence":str(lam),
            "prior_stationary":invariant,
            "prior_after_one_generation":str(prior_after)
        })
        trajectories={}
        for start in STARTS:
            initial=start_state(pi,start)
            path_a=propagate(a,initial)
            path_b=propagate(b,initial)
            if path_a!=path_b:
                raise AssertionError("independent multigeneration trajectories disagree")
            trajectories[start]=path_a
            world_rows.append({
                "pi":str(pi),"epsilon":str(eps),"n":n,
                "rule":rule,"start":start,
                "p_H0_and_H1_t0_to_t8":[[str(p0),str(p1)] for p0,p1 in path_a],
                "independent_fraction_methods_equal":True,
            })
        deltas=[trajectories["point1"][t][1]-trajectories["point0"][t][1]
                for t in range(HORIZON+1)]
        if deltas!=[lam**t for t in range(HORIZON+1)]:
            raise AssertionError("two-state exact ancestry dependence identity failed")
        matrix_rows[-1]["conditional_ancestry_difference_t0_to_t8"]=[str(x) for x in deltas]
    if len(world_rows)!=72 or len(matrix_rows)!=24:
        raise AssertionError("frozen grid mismatch")

    comparison={}
    for n in SAMPLE_SIZES:
        row=next(r for r in matrix_rows
                 if r["pi"]=="1/2" and r["epsilon"]=="1/4"
                 and r["n"]==n and r["rule"]=="posterior_sample")
        comparison[str(n)]={
            "stationary_marginal":row["prior_stationary"],
            "D4":row["conditional_ancestry_difference_t0_to_t8"][4],
            "matrix":row["T_old_to_new"]
        }
    if comparison["1"]["D4"]==comparison["3"]["D4"]:
        raise AssertionError("locked comparison must retain a provenance distinction")
    if len(violations)==0:
        raise AssertionError("MAP prior nonstationarity negative control failed")

    result={
        "research_id":"R175",
        "status":"ORIGINAL_FINITE_BINARY_MEMORY_E1_ARTIFICIAL_ONLY",
        "frozen_protocol":str(PROTOCOL.relative_to(HERE.parent.parent)),
        "priors":[str(q) for q in PRIORS],"noises":[str(q) for q in NOISES],
        "n_training_reports":list(SAMPLE_SIZES),
        "rules":list(RULES),"initial_conditions":list(STARTS),
        "world_count":len(world_rows),"unique_transitions":len(matrix_rows),
        "generations_per_world":HORIZON+1,
        "full_probability_cells":len(world_rows)*(HORIZON+1)*2,
        "matrices":matrix_rows,"worlds":world_rows,
        "matched_stationary_marginal_but_different_ancestral_retention":comparison,
        "MAP_prior_nonstationary_parameter_sets":violations,
        "MAP_prior_nonstationary_count":len(violations),
        "independent_method_results_exact":True,
        "real_human_data_or_history_scored":False,
        "new_E2":0,"new_E3":0
    }
    RESULT.write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    acceptance={
        "research_id":"R175","status":"E1_ARTIFICIAL_EXACT_BOUNDED_CLOSED",
        "worlds":72,"matrices":24,"generations":9,"full_state_cells":1296,
        "independent_fraction_transition_and_path_parity":True,
        "posterior_sampling_prior_invariant_for_all_parameters":True,
        "same_stationary_marginal_distinct_ancestry_examples":comparison,
        "MAP_nonstationary_matrix_count":len(violations),
        "original_paper_full_model_reproduced":False,
        "human_intergenerational_evidence":False,
        "new_E2":0,"new_E3":0,
        "exact_results_sha256":sha256(RESULT.read_bytes()).hexdigest(),
    }
    ACCEPTANCE.write_text(json.dumps(acceptance,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("R175_MACHINE_ACCEPTANCE",json.dumps(acceptance,sort_keys=True))
    return acceptance


def archive():
    names=["r175_binary_memory_iterated_learning_exact.py",RESULT.name,ACCEPTANCE.name]
    with zipfile.ZipFile(ARCHIVE,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as zipped:
        for name in names:
            info=zipfile.ZipInfo(name,(2026,10,21,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o644<<16
            zipped.writestr(info,(HERE/name).read_bytes())
        p=zipfile.ZipInfo(PROTOCOL.name,(2026,10,21,0,0,0))
        p.compress_type=zipfile.ZIP_DEFLATED
        p.external_attr=0o644<<16
        zipped.writestr(p,PROTOCOL.read_bytes())
    print("R175_ARCHIVE_SHA256",sha256(ARCHIVE.read_bytes()).hexdigest())


class TestBinaryMemory(unittest.TestCase):
    def test_number_of_worlds(self):
        self.assertEqual(len(list(worlds())),72)
    def test_two_unique_rules(self):
        self.assertEqual(len(RULES),2)
    def test_start_point0(self):
        self.assertEqual(start_state(Q(1,4),"point0"),(1,0))
    def test_start_point1(self):
        self.assertEqual(start_state(Q(1,4),"point1"),(0,1))
    def test_start_prior(self):
        self.assertEqual(start_state(Q(1,4),"prior"),(Q(3,4),Q(1,4)))
    def test_invalid_start_fails(self):
        with self.assertRaises(ValueError):
            start_state(Q(1,2),"unknown")
    def test_n1_posterior_sample_manual(self):
        # For symmetric prior and epsilon=1/4, parent 0 -> child 1 is 3/8.
        self.assertEqual(row_a(Q(1,2),Q(1,4),1,"posterior_sample",0)[1],Q(3,8))
    def test_n1_map_manual(self):
        self.assertEqual(row_a(Q(1,2),Q(1,4),1,"posterior_MAP",0)[1],Q(1,4))
    def test_map_tie_always_zero(self):
        self.assertEqual(row_a(Q(1,4),Q(1,4),1,"posterior_MAP",0)[1],0)
    def test_n1_analytical_vs_bit_sequences(self):
        for pi in PRIORS:
            for eps in NOISES:
                for rule in RULES:
                    self.assertEqual(matrix_a(pi,eps,1,rule),matrix_b(pi,eps,1,rule))
    def test_n3_analytical_vs_bit_sequences(self):
        for pi in PRIORS:
            for eps in NOISES:
                for rule in RULES:
                    self.assertEqual(matrix_a(pi,eps,3,rule),matrix_b(pi,eps,3,rule))
    def test_stationary_sample_all(self):
        for pi,eps,n in itertools.product(PRIORS,NOISES,SAMPLE_SIZES):
            m=matrix_a(pi,eps,n,"posterior_sample")
            self.assertEqual(propagate(m,start_state(pi,"prior"))[-1][1],pi)
    def test_map_nonstationary_known(self):
        m=matrix_a(Q(1,4),Q(1,3),1,"posterior_MAP")
        self.assertNotEqual(propagate(m,start_state(Q(1,4),"prior"))[1][1],Q(1,4))
    def test_trajectory_length(self):
        m=matrix_a(Q(1,2),Q(1,4),3,"posterior_sample")
        self.assertEqual(len(propagate(m,(1,0))),9)
    def test_analytic_ancestry_decay(self):
        for pi,eps,n,rule,_ in worlds():
            m=matrix_a(pi,eps,n,rule)
            lam=m[1][1]-m[0][1]
            a=propagate(m,(1,0))
            b=propagate(m,(0,1))
            self.assertEqual([b[t][1]-a[t][1] for t in range(9)],
                             [lam**t for t in range(9)])
    def test_rejected_invalid_noise(self):
        with self.assertRaises(ValueError):
            row_a(Q(1,2),Q(1,2),1,"posterior_sample",0)
    def test_rejected_invalid_rule(self):
        with self.assertRaises(ValueError):
            row_b(Q(1,2),Q(1,4),3,"unknown",0)
    def test_negative_horizon(self):
        with self.assertRaises(ValueError):
            propagate(((1,0),(0,1)),(1,0),-1)
    def test_probability_normalized_for_every_world(self):
        for pi,eps,n,rule,start in worlds():
            matrix=matrix_b(pi,eps,n,rule)
            for state in propagate(matrix,start_state(pi,start)):
                self.assertEqual(sum(state),1)
                self.assertTrue(all(0<=x<=1 for x in state))
    def test_prior_alone_cannot_prove_ancestral_retention(self):
        m1=matrix_a(Q(1,2),Q(1,4),1,"posterior_sample")
        m3=matrix_a(Q(1,2),Q(1,4),3,"posterior_sample")
        self.assertEqual(propagate(m1,(Q(1,2),Q(1,2))),
                         propagate(m3,(Q(1,2),Q(1,2))))
        self.assertNotEqual(propagate(m1,(0,1))[4],propagate(m3,(0,1))[4])


if __name__=="__main__":
    if sys.argv[1:]==["--test"]:
        unittest.main(argv=[sys.argv[0]],verbosity=2)
    elif sys.argv[1:]==["--run"]:
        run()
        archive()
    else:
        raise SystemExit("Expected --test or --run")
