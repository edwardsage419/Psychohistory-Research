#!/usr/bin/env python3
"""R115 independent joint-path E1 audit. Original functions used only for comparison."""
from fractions import Fraction as F
from pathlib import Path
import importlib.util
import hashlib
import json

H, Z, O = F(1,2), F(0), F(1)

def signal(s,v,p):
    return p if s == v else O-p

def action_one(m,s,p):
    yes=m[1]*signal(s,1,p)
    no=m[0]*signal(s,0,p)
    return O if yes>no else Z if yes<no else H

def enumerate_joint(n,p):
    paths={():{0:H,1:H}}
    for _ in range(n):
        nxt={}
        for history,m in paths.items():
            for a in (0,1):
                weights={}
                for v in (0,1):
                    likelihood=Z
                    for s in (0,1):
                        one=action_one(m,s,p)
                        likelihood+=signal(s,v,p)*(one if a else O-one)
                    weights[v]=m[v]*likelihood
                if weights[0]+weights[1]>Z:
                    nxt[history+(a,)]=weights
        paths=nxt
        assert sum((sum(m.values(),Z) for m in paths.values()),Z)==O
    return paths

def post(m):
    return m[1]/(m[0]+m[1])

def cascade(m,p):
    a=[action_one(m,s,p) for s in (0,1)]
    return 1 if a==[O,O] else 0 if a==[Z,Z] else None

def masses_by_cascade(paths,p):
    out={0:Z,1:Z,None:Z}
    for m in paths.values():
        out[cascade(m,p)]+=m[0]+m[1]
    return {"up_cascade":out[1],"down_cascade":out[0],"no_cascade":out[None]}

def source(root):
    path=root/"research/R115/r115_bhw_1992_informational_action_cascade_exact.py"
    if not path.is_file():
        raise FileNotFoundError("ORIGINAL_R115_SOURCE_MISSING")
    receipt_path=root/"research/R115/R115_PHASE_A_BHW_1992_EXACT_FRACTION_SYNTHETIC_EQ1_CI_ACCEPTANCE.json"
    receipt=json.loads(receipt_path.read_text(encoding="utf-8"))
    expected=receipt["underlying_study_source_SHA256"]
    for filename,expected_sha in expected.items():
        source_file=root/"research/R115"/filename
        actual=hashlib.sha256(source_file.read_bytes()).hexdigest()
        if actual!=expected_sha:
            raise AssertionError("ORIGINAL_SOURCE_SHA256_MISMATCH "+filename)
    spec=importlib.util.spec_from_file_location("r115_original_comparison_only",path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def compare(paths,p,mod):
    count=0
    for h,m in paths.items():
        if post(m)!=mod.trace_public_actions(h,p)[0][-1]:
            raise AssertionError("PUBLIC_POSTERIOR_MISMATCH "+str((p,h)))
        count+=1
        for v in (0,1):
            if m[v]/H!=mod.history_likelihood_given_state(h,v,p):
                raise AssertionError("CONDITIONAL_PATH_MISMATCH "+str((p,h,v)))
            count+=1
        if cascade(m,p)!=mod.cascade_action(post(m),p):
            raise AssertionError("CASCADE_CLASS_MISMATCH "+str((p,h)))
        count+=1
    return count

def run(root):
    mod=source(root)
    comparisons=0
    paths_checked=0
    cases=[]
    for p in (F(3,5),F(7,10),F(4,5)):
        for n in (2,4,6):
            paths=enumerate_joint(n,p)
            comparisons+=compare(paths,p,mod)
            paths_checked+=len(paths)
            got=masses_by_cascade(paths,p)
            no=(p*(O-p))**(n//2)
            expected={"up_cascade":(O-no)/2,"down_cascade":(O-no)/2,"no_cascade":no}
            if got!=expected:
                raise AssertionError("ORIGINAL_PAPER_EQ1_MISMATCH "+str((p,n)))
            if got!=mod.ex_ante_cascade_masses_after_n(n,p):
                raise AssertionError("ORIGINAL_IMPLEMENTATION_CASCADE_MISMATCH")
            comparisons+=6
            cases.append({"precision":str(p),"n":n,"feasible_paths":len(paths),"no_cascade":str(no)})
    p=F(7,10)
    two=enumerate_joint(2,p)
    three=enumerate_joint(3,p)
    if post(two[(1,1)])!=F(119,158):
        raise AssertionError("POSTERIOR_AFTER_TWO")
    if post(three[(1,1,1)])!=F(119,158):
        raise AssertionError("THIRD_ACTION_ZERO_INFORMATION")
    if two[(1,1)][0]/H!=F(39,200):
        raise AssertionError("WRONG_UP_CASCADE_GIVEN_V0")
    if p*p/(p*p+(O-p)**2)!=F(49,58):
        raise AssertionError("NAIVE_DOUBLE_COUNTING_NEGATIVE_BASELINE")
    comparisons+=4
    tampered={h:dict(m) for h,m in two.items()}
    first=next(iter(two))
    tampered[first][1]+=F(1,1000)
    rejected_mass=False
    try:
        compare(tampered,p,mod)
    except AssertionError:
        rejected_mass=True
    rejected_post=(post(two[first])+F(1,1000)!=mod.trace_public_actions(first,p)[0][-1])
    if not rejected_mass or not rejected_post:
        raise AssertionError("TAMPER_NEGATIVE_CONTROL_NOT_REJECTED")
    return {"research_id":"R115","catalogue_id":"03-006",
            "grade":"PASS_BOUNDED_INTERNAL_INDEPENDENT_METHOD_E1",
            "method":"joint_state_action_path_probability_enumeration",
            "original_source_receipt_sha256_verified":3,
            "cases":cases,"case_count":len(cases),"feasible_path_comparisons":paths_checked,
            "exact_assertions":comparisons,"tamper_controls_rejected":2,
            "p70_public_posterior_after_two":"119/158",
            "p70_public_posterior_after_three":"119/158",
            "p70_wrong_up_cascade_given_V0":"39/200",
            "human_E2_new":0,"historical_E3_new":0,
            "external_independent_replication":False,"R073":"FROZEN","PESEN_v0_1":"FROZEN"}

if __name__=="__main__":
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument("--repo-root",type=Path,default=Path(__file__).resolve().parents[2])
    args=parser.parse_args()
    print(json.dumps(run(args.repo_root),indent=2,sort_keys=True))
