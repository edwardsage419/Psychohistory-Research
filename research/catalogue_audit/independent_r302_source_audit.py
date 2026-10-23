#!/usr/bin/env python3
"""Independent exact Thompson posterior P(A>B) via alternating beta-CDF integral; no model imports."""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,math,unittest
from fractions import Fraction as Q
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]/"research/R302"
SOURCE=ROOT/"R302_ALL_162_ORIGINAL_BETA_BANDIT_ARM_SOURCES.csv"
RESULT=ROOT/"R302_EXACT_BANDIT_THOMPSON_RESULTS.json"
RECEIPT=ROOT/"R302_MACHINE_RECEIPT.json"
COUNTS=(0,1,2)
WORLDS=list(itertools.product(COUNTS,repeat=4))
ARMS=("A","B")
ZERO,ONE=Q(0),Q(1)

def obj(path):return json.loads(path.read_text(encoding="utf-8"))
def read():
    with SOURCE.open(newline="",encoding="utf-8") as f:return list(csv.DictReader(f))
def bfun(a,b):return Q(math.factorial(a-1)*math.factorial(b-1),math.factorial(a+b-1))

def independent_integral(sA,fA,sB,fB):
    # A~Beta(a,b), B~Beta(c,d): integrate f_A(x)*CDF_B(x) dx.
    # F_B(x)=sum (-1)^k binom(d-1,k) x^(c+k) / ((c+k)*Beta(c,d))
    a,b,c,d=sA+1,fA+1,sB+1,fB+1
    probability=ZERO
    for k in range(d):
        term=Q((-1)**k*math.comb(d-1,k))*bfun(a+c+k,b)
        term/=((c+k)*bfun(a,b)*bfun(c,d))
        probability+=term
    return probability

def expected(counts):
    sa,fa,sb,fb=counts
    arms={}
    for arm,s,f in (("A",sa,fa),("B",sb,fb)):
        a,b=1+s,1+f
        arms[arm]={"posterior_a":a,"posterior_b":b,
                   "posterior_mean":Q(a,a+b),
                   "posterior_variance":Q(a*b,(a+b)**2*(a+b+1))}
    thompsonA=independent_integral(*counts)
    return arms,"A" if arms["A"]["posterior_mean"]>=arms["B"]["posterior_mean"] else "B",{
      "A":thompsonA,"B":ONE-thompsonA}

def ident(counts):
    a,b,c,d=counts
    return f"A_success={a}|A_failure={b}|B_success={c}|B_failure={d}"

def verify(original,result):
    if len(original)!=162 or result["synthetic_count_worlds"]!=81 or result["original_labeled_source_rows"]!=162:
        raise AssertionError("incomplete source universe")
    if len(result["worlds"])!=81:raise AssertionError("missing complete world outputs")
    allkeys=set((counts,arm) for counts in WORLDS for arm in ARMS)
    seen={}
    for r in original:
        try:
            counts=tuple(int(r[k]) for k in ("A_successes","A_failures","B_successes","B_failures"))
            arm=r["arm"]
        except (KeyError,ValueError) as err:raise AssertionError("corrupt counts") from err
        key=(counts,arm)
        if key not in allkeys or key in seen:raise AssertionError("duplicate/unfrozen count world")
        if r["world"]!=ident(counts):raise AssertionError("false source ID")
        post,greedy,p=expected(counts)
        s=counts[0] if arm=="A" else counts[2]
        f=counts[1] if arm=="A" else counts[3]
        if int(r["arm_successes"])!=s or int(r["arm_failures"])!=f:
            raise AssertionError("arm original counts tampered")
        for k in ("posterior_a","posterior_b","posterior_mean","posterior_variance"):
            if Q(r[k])!=post[arm][k]:raise AssertionError("source posterior tampered: "+k)
        if r["posterior_greedy_choice"]!=greedy:raise AssertionError("greedy wrong")
        if Q(r["thompson_choice_probability"])!=p[arm]:raise AssertionError("TS probability wrong")
        other="A" if arm=="B" else "B"
        if Q(r["other_arm_thompson_probability"])!=p[other]:raise AssertionError("other arm probability wrong")
        if not ZERO<p[arm]<ONE:raise AssertionError("unexpected certain posterior draw")
        seen[key]=r
    if set(seen)!=allkeys:raise AssertionError("incomplete set")
    for i,counts in enumerate(WORLDS):
        v=result["worlds"][i]
        post,greedy,p=expected(counts)
        if v["world"]!=ident(counts) or v["success_failure_counts"]!=list(counts):raise AssertionError("world identity wrong")
        if v["arm_A_posterior"]!={k:str(val) for k,val in post["A"].items()}:raise AssertionError("A posterior JSON")
        if v["arm_B_posterior"]!={k:str(val) for k,val in post["B"].items()}:raise AssertionError("B posterior JSON")
        if v["greedy_posterior_mean_choice"]!=greedy:raise AssertionError("greedy JSON")
        if v["thompson_P_choose_A"]!=str(p["A"]) or v["thompson_P_choose_B"]!=str(p["B"]):
            raise AssertionError("Thompson probability JSON")
        if v["fully_labeled_original_arm_sources"]!=2:raise AssertionError("source row per world wrong")
        swapped=(counts[2],counts[3],counts[0],counts[1])
        if p["A"]+expected(swapped)[2]["A"]!=ONE:raise AssertionError("arm exchange symmetry broken")
    expect={"unobserved_A_selection":"1/2","A_one_success_B_unobserved":"2/3",
      "A_two_success_B_two_failure":"19/20",
      "A_B_identical_Beta3_3":"1/2","uniform_Beta1_1_variance":"1/12","Beta3_3_variance":"1/28"}
    if result["reference_exact_cases"]!=expect:raise AssertionError("frozen analytic cases corrupted")
    return {"independent_thompson_alternate_beta_integral":"PASS",
      "complete_original_arm_sources":162,"artificial_evidence_worlds":81,
      "unobserved_TS_exploration_probability":"1/2","real_human_E2":0,
      "real_animal_E2":0,"historical_E3":0}

def audit():
    r,j=obj(RECEIPT),obj(RESULT)
    freeze="b3c92f9f013e795a0db4622dc48613f82eb38bca"
    if r["freeze_commit"]!=freeze or j["freeze_commit"]!=freeze:raise AssertionError("missing prospective freeze")
    if j["original_catalogue_id"]!="02-016" or j["research_id"]!="R302":raise AssertionError("wrong model")
    if any(j[k]!=0 for k in ("real_human_E2_added","real_animal_E2_added","historical_E3_added")):
        raise AssertionError("synthetic data promoted to human/animal")
    if j["actual_arm_reward_generating_rates_known"] is not False or j["actual_bandit_actions_simulated"] is not False or j["UCB1_finite_time_regret_theorem_reproduced"] is not False:
        raise AssertionError("actual reward/real regret falsely claimed")
    if r["source_rows"]!=162 or r["new_real_E2"]!=0 or r["new_historical_E3"]!=0:
        raise AssertionError("receipt metadata wrong")
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest()!=r["source_sha256"]:raise AssertionError("original source SHA")
    if hashlib.sha256(RESULT.read_bytes()).hexdigest()!=r["results_sha256"]:raise AssertionError("original result SHA")
    return {**verify(read(),j),"source_sha256":r["source_sha256"],"results_sha256":r["results_sha256"]}

class Tests(unittest.TestCase):
    def test_full(self):self.assertEqual(audit()["complete_original_arm_sources"],162)
    def test_worlds(self):self.assertEqual(len(WORLDS),81)
    def test_uniform(self):self.assertEqual(independent_integral(0,0,0,0),Q(1,2))
    def test_one(self):self.assertEqual(independent_integral(1,0,0,0),Q(2,3))
    def test_opposed(self):self.assertEqual(independent_integral(2,0,0,2),Q(19,20))
    def test_label_swap(self):self.assertEqual(independent_integral(0,2,2,0),Q(1,20))
    def test_same_shapes(self):self.assertEqual(independent_integral(2,2,2,2),Q(1,2))
    def test_missing_row(self):
        with self.assertRaises(AssertionError):verify(read()[:-1],obj(RESULT))
    def test_duplicate_row(self):
        d=read();d[1]=dict(d[0])
        with self.assertRaises(AssertionError):verify(d,obj(RESULT))
    def test_bad_count(self):
        d=read();d[1]=dict(d[1]);d[1]["A_successes"]="3"
        with self.assertRaises(AssertionError):verify(d,obj(RESULT))
    def test_bad_mean(self):
        d=read();d[1]=dict(d[1]);d[1]["posterior_mean"]="8"
        with self.assertRaises(AssertionError):verify(d,obj(RESULT))
    def test_bad_prob(self):
        d=read();d[1]=dict(d[1]);d[1]["thompson_choice_probability"]="1"
        with self.assertRaises(AssertionError):verify(d,obj(RESULT))
    def test_bad_greedy(self):
        d=read();d[1]=dict(d[1]);d[1]["posterior_greedy_choice"]="C"
        with self.assertRaises(AssertionError):verify(d,obj(RESULT))
    def test_wrong_result(self):
        x=obj(RESULT);x["worlds"][0]["thompson_P_choose_A"]="2"
        with self.assertRaises(AssertionError):verify(read(),x)
    def test_bad_reference(self):
        x=obj(RESULT);x["reference_exact_cases"]["unobserved_A_selection"]="0"
        with self.assertRaises(AssertionError):verify(read(),x)
    def test_sha_tamper(self):self.assertNotEqual(hashlib.sha256(SOURCE.read_bytes()+b"fake").hexdigest(),obj(RECEIPT)["source_sha256"])
    def test_no_real_regret(self):self.assertFalse(obj(RESULT)["actual_bandit_actions_simulated"])

if __name__=="__main__":
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true");g.add_argument("--audit",action="store_true")
    args=p.parse_args()
    if args.test:unittest.main(argv=["R302 independent"],verbosity=1)
    else:print(json.dumps(audit(),ensure_ascii=False,indent=2))
