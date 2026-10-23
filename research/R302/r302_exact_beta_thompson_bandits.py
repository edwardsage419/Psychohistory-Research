#!/usr/bin/env python3
"""R302 exact Beta-Bernoulli two-armed Thompson choice probabilities (artificial E1)."""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,math,unittest
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parent
FREEZE="b3c92f9f013e795a0db4622dc48613f82eb38bca"
COUNTS=(0,1,2)
ARMS=("A","B")
WORLDS=tuple(itertools.product(COUNTS,repeat=4))
SOURCE_NAME="R302_ALL_162_ORIGINAL_BETA_BANDIT_ARM_SOURCES.csv"
RESULT_NAME="R302_EXACT_BANDIT_THOMPSON_RESULTS.json"
RECEIPT_NAME="R302_MACHINE_RECEIPT.json"
Z,O=F(0),F(1)

def beta(a,b):
    if a<=0 or b<=0:raise ValueError("beta parameters positive")
    return F(math.factorial(a-1)*math.factorial(b-1),math.factorial(a+b-1))

def superior(a,b,c,d):
    # A Beta(a,b) random probability > independent B Beta(c,d).
    total=Z
    n=c+d-1
    for j in range(c,n+1):
        total+=math.comb(n,j)*beta(a+j,b+n-j)/beta(a,b)
    return total

def stats(s,f):
    if s not in COUNTS or f not in COUNTS:raise ValueError("unfrozen count")
    a,b=s+1,f+1
    return {"posterior_a":a,"posterior_b":b,"posterior_mean":F(a,a+b),
        "posterior_variance":F(a*b,(a+b)**2*(a+b+1))}

def world_id(counts):
    sa,fa,sb,fb=counts
    return f"A_success={sa}|A_failure={fa}|B_success={sb}|B_failure={fb}"

def evaluate(counts):
    if counts not in WORLDS:raise ValueError("unfrozen count world")
    sa,fa,sb,fb=counts
    A,B=stats(sa,fa),stats(sb,fb)
    prob=superior(A["posterior_a"],A["posterior_b"],
                  B["posterior_a"],B["posterior_b"])
    if not Z<=prob<=O:raise AssertionError("invalid Thompson choice probability")
    return {"A":A,"B":B,
       "greedy_action":"A" if A["posterior_mean"]>=B["posterior_mean"] else "B",
       "thompson_prob_A":prob,"thompson_prob_B":O-prob}

def source(counts,arm):
    if arm not in ARMS:raise ValueError("unsupported arm")
    sa,fa,sb,fb=counts
    vals=evaluate(counts)
    st=vals[arm]
    return {"world":world_id(counts),"A_successes":sa,"A_failures":fa,
       "B_successes":sb,"B_failures":fb,"arm":arm,
       "arm_successes":sa if arm=="A" else sb,
       "arm_failures":fa if arm=="A" else fb,
       **st,
       "posterior_greedy_choice":vals["greedy_action"],
       "thompson_choice_probability":vals["thompson_prob_"+arm],
       "other_arm_thompson_probability":vals["thompson_prob_"+("B" if arm=="A" else "A")]}

def sources():return tuple(source(w,arm) for w in WORLDS for arm in ARMS)

def verify():
    assert len(WORLDS)==81 and len(sources())==162
    assert len({(x["world"],x["arm"]) for x in sources()})==162
    for w in WORLDS:
        v=evaluate(w)
        assert v["thompson_prob_A"]+v["thompson_prob_B"]==O
        assert Z<v["thompson_prob_A"]<O and Z<v["thompson_prob_B"]<O
        reverse=(w[2],w[3],w[0],w[1])
        assert evaluate(reverse)["thompson_prob_A"]==O-v["thompson_prob_A"]
        for arm in ARMS:
            x=source(w,arm)
            assert x["posterior_mean"]==F(x["posterior_a"],x["posterior_a"]+x["posterior_b"])
            assert x["posterior_variance"]==F(x["posterior_a"]*x["posterior_b"],
             (x["posterior_a"]+x["posterior_b"])**2*(x["posterior_a"]+x["posterior_b"]+1))
            assert x["thompson_choice_probability"]+x["other_arm_thompson_probability"]==O
        if w[:2]==w[2:]:assert v["thompson_prob_A"]==F(1,2) and v["greedy_action"]=="A"
    assert evaluate((0,0,0,0))["thompson_prob_A"]==F(1,2)
    assert evaluate((1,0,0,0))["thompson_prob_A"]==F(2,3)
    assert evaluate((2,0,0,2))["thompson_prob_A"]==F(19,20)
    assert stats(0,0)["posterior_variance"]==F(1,12)
    assert stats(2,2)["posterior_variance"]==F(1,28)
    assert evaluate((2,2,0,0))["thompson_prob_A"]==F(1,2)
    return True

def emit():
    verify()
    cols=("world","A_successes","A_failures","B_successes","B_failures","arm",
      "arm_successes","arm_failures","posterior_a","posterior_b","posterior_mean",
      "posterior_variance","posterior_greedy_choice","thompson_choice_probability",
      "other_arm_thompson_probability")
    path=ROOT/SOURCE_NAME
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=cols,lineterminator="\n");w.writeheader()
        for x in sources():w.writerow({k:str(x[k]) for k in cols})
    world_results=[]
    for w in WORLDS:
        v=evaluate(w)
        world_results.append({"world":world_id(w),"success_failure_counts":list(w),
          "arm_A_posterior":{k:str(value) for k,value in v["A"].items()},
          "arm_B_posterior":{k:str(value) for k,value in v["B"].items()},
          "greedy_posterior_mean_choice":v["greedy_action"],
          "thompson_P_choose_A":str(v["thompson_prob_A"]),
          "thompson_P_choose_B":str(v["thompson_prob_B"]),
          "fully_labeled_original_arm_sources":2})
    result={"research_id":"R302","original_catalogue_id":"02-016","freeze_commit":FREEZE,
      "scope":"E1_FINITE_ARTIFICIAL_POSTERIOR_SUPERIORITY_AND_THOMPSON_ACTION_PROBABILITIES_NO_REWARDS_OR_REGRET",
      "synthetic_count_worlds":81,"original_labeled_source_rows":162,
      "real_human_E2_added":0,"real_animal_E2_added":0,"historical_E3_added":0,
      "actual_arm_reward_generating_rates_known":False,
      "actual_bandit_actions_simulated":False,
      "UCB1_finite_time_regret_theorem_reproduced":False,
      "R073":"FROZEN","PESEN_v0_1":"FROZEN",
      "worlds":world_results,
      "reference_exact_cases":{"unobserved_A_selection":"1/2",
         "A_one_success_B_unobserved":"2/3",
         "A_two_success_B_two_failure":"19/20",
         "A_B_identical_Beta3_3":"1/2",
         "uniform_Beta1_1_variance":"1/12",
         "Beta3_3_variance":"1/28"}}
    rp=ROOT/RESULT_NAME
    rp.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    receipt={"research_id":"R302","freeze_commit":FREEZE,"source_rows":162,
       "source_sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
       "results_sha256":hashlib.sha256(rp.read_bytes()).hexdigest(),
       "new_real_E2":0,"new_historical_E3":0}
    (ROOT/RECEIPT_NAME).write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_full(self):self.assertTrue(verify())
    def test_worlds(self):self.assertEqual(len(WORLDS),81)
    def test_sources(self):self.assertEqual(len(sources()),162)
    def test_uniform(self):self.assertEqual(evaluate((0,0,0,0))["thompson_prob_A"],F(1,2))
    def test_one_success(self):self.assertEqual(evaluate((1,0,0,0))["thompson_prob_A"],F(2,3))
    def test_two_opposing(self):self.assertEqual(evaluate((2,0,0,2))["thompson_prob_A"],F(19,20))
    def test_uniform_variance(self):self.assertEqual(stats(0,0)["posterior_variance"],F(1,12))
    def test_concentrated_variance(self):self.assertEqual(stats(2,2)["posterior_variance"],F(1,28))
    def test_equal_means(self):self.assertEqual(evaluate((2,2,0,0))["thompson_prob_A"],F(1,2))
    def test_bad_count(self):
        with self.assertRaises(ValueError):stats(3,0)
    def test_bad_arm(self):
        with self.assertRaises(ValueError):source((0,0,0,0),"C")
    def test_bad_shape(self):
        with self.assertRaises(ValueError):beta(0,1)

def generated(w,arm,kind):
    def check(self):
        s=source(w,arm)
        v=evaluate(w)
        if kind=="mean":self.assertEqual(s["posterior_mean"],v[arm]["posterior_mean"])
        elif kind=="variance":self.assertEqual(s["posterior_variance"],v[arm]["posterior_variance"])
        elif kind=="thompson":self.assertEqual(s["thompson_choice_probability"],v["thompson_prob_"+arm])
        elif kind=="sum":self.assertEqual(s["thompson_choice_probability"]+s["other_arm_thompson_probability"],O)
        else:raise AssertionError(kind)
    return check
for i,w in enumerate(WORLDS):
    for arm in ARMS:
        for kind in ("mean","variance","thompson","sum"):
            setattr(Tests,f"test_world{i}_{arm}_{kind}",generated(w,arm,kind))

if __name__=="__main__":
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true");g.add_argument("--emit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["R302"],verbosity=1)
    else:print(json.dumps(emit(),indent=2))
