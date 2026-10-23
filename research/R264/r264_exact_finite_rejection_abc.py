#!/usr/bin/env python3
"""R264: nine exact finite rejection ABC models (432 original theta/RNG atoms).
Complete simulator-source acceptance is compared with independently enumerated
Bernoulli outcome likelihoods. This is NOT Beaumont regression-adjusted ABC,
continuous-parameter calibration or evidence from population genetics.
"""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
HERE=Path(__file__).resolve().parent
FREEZE="58f17a0b73556dfb2517c4bf26da3bd82c719bd6"
ZERO=F(0);ONE=F(1)
THETA=(0,1,2)
RNG=tuple(itertools.product((0,1),repeat=4))
EPS=(0,1,2)
DISTANCES=("FULL_HAMMING","COUNT_SUM","FIRST_COMPONENT")
ASC=(F(1,4),F(1,2),F(3,4))
DESC=(F(3,4),F(1,2),F(1,4))
HALF=(F(1,2),)*3
CONFIG={
 "IID_GRADIENT":(ASC,ASC),
 "COMPLEMENTARY_GRADIENT":(ASC,DESC),
 "REVERSED_COMPLEMENT":(DESC,ASC),
 "FIRST_ONLY_INFORMATIVE":(ASC,HALF),
 "SECOND_ONLY_INFORMATIVE":(HALF,ASC),
 "NO_SIGNAL":(HALF,HALF),
 "DETERMINISTIC_ENDS":((ZERO,F(1,2),ONE),(ONE,F(1,2),ZERO)),
 "NONMONOTONE_IID":((F(1,4),F(3,4),F(1,2)),(F(1,4),F(3,4),F(1,2))),
 "FIRST_WITH_SECOND_QUARTER":(ASC,(F(1,4),)*3)
}
WORLDS=tuple(CONFIG)
OBS=(1,0)
def check(w):
    if w not in CONFIG:raise ValueError("unfrozen ABC world")
def probs(w,theta):
    check(w)
    if theta not in THETA:raise ValueError("theta not in prior")
    return CONFIG[w][0][theta],CONFIG[w][1][theta]
def simulator(w,theta,raw):
    q1,q2=probs(w,theta)
    if len(raw)!=4 or any(x not in (0,1) for x in raw):
        raise ValueError("requires four independent fair RNG bits")
    return int(F(2*raw[0]+raw[1],4)<q1),int(F(2*raw[2]+raw[3],4)<q2)
def source_atom(w,t,raw):
    q1,q2=probs(w,t);y=simulator(w,t,raw)
    row=dict(world=w,original_theta=t,
       oracle_r1_four_equally_likely_values=2*raw[0]+raw[1],
       oracle_r2_four_equally_likely_values=2*raw[2]+raw[3],
       oracle_original_conditional_probability_q1=q1,
       oracle_original_conditional_probability_q2=q2,
       observed_simulated_Y1=y[0],observed_simulated_Y2=y[1],
       frozen_observation_Y1=1,frozen_observation_Y2=0,
       original_full_theta_rng_source_probability=F(1,48))
    for i,x in enumerate(raw):row[f"oracle_original_random_bit_{i}"]=x
    return row
@lru_cache(None)
def sources(w):
    check(w)
    rows=tuple(source_atom(w,t,raw) for t in THETA for raw in RNG)
    assert len(rows)==48 and sum((r["original_full_theta_rng_source_probability"] for r in rows),ZERO)==ONE
    return rows
def distance(kind,y):
    if kind=="FULL_HAMMING":return 1-y[0]+y[1]
    if kind=="COUNT_SUM":return abs(y[0]+y[1]-1)
    if kind=="FIRST_COMPONENT":return 1-y[0]
    raise ValueError("not a frozen discrepancy")
def normalize(mass):
    denom=sum(mass,ZERO)
    if not denom:raise AssertionError("zero total acceptance impossible under frozen configurations")
    return tuple(v/denom for v in mass)
def source_rejection_ABC(w,kind,eps):
    """First route: decisions from raw simulator outputs, not likelihood."""
    if eps not in EPS:raise ValueError("not frozen epsilon")
    mass=[ZERO]*3
    for row in sources(w):
        y=row["observed_simulated_Y1"],row["observed_simulated_Y2"]
        if distance(kind,y)<=eps:
            mass[row["original_theta"]]+=row["original_full_theta_rng_source_probability"]
    return normalize(mass),sum(mass,ZERO)
def outcome_probability(q1,q2,y):
    return (q1 if y[0] else ONE-q1)*(q2 if y[1] else ONE-q2)
def analytic_ABC(w,kind,eps):
    """Independent source-free integration over 4 possible Bernoulli outcomes."""
    if eps not in EPS:raise ValueError("not frozen epsilon")
    mass=[]
    for t in THETA:
        q1,q2=probs(w,t)
        total=sum((outcome_probability(q1,q2,y)
                   for y in itertools.product((0,1),repeat=2) if distance(kind,y)<=eps),ZERO)
        mass.append(total/3)
    return normalize(mass),sum(mass,ZERO)
def exact_full_bayes(w):
    return normalize([outcome_probability(*probs(w,t),OBS) for t in THETA])
def tv(a,b):return sum((abs(x-y) for x,y in zip(a,b)),ZERO)/2
def count_distribution(w,t):
    p,q=probs(w,t)
    return ((ONE-p)*(ONE-q),p*(ONE-q)+(ONE-p)*q,p*q)
def summary(w):
    exact=exact_full_bayes(w)
    scenarios={}
    for kind in DISTANCES:
        scenarios[kind]={}
        for eps in EPS:
            got,rate=source_rejection_ABC(w,kind,eps)
            derived,d_rate=analytic_ABC(w,kind,eps)
            assert got==derived and rate==d_rate
            scenarios[kind][str(eps)]=dict(
                exact_acceptance_probability=str(rate),
                posterior_theta0_theta1_theta2=[str(x) for x in got],
                posterior_total_variation_against_exact_full_observation=str(tv(got,exact)),
                independent_analytic_Bernoulli_outcome_acceptance_verified=True)
    return dict(world=w,all_original_theta_rng_source_atoms=48,
        frozen_q1_by_theta=[str(x) for x in CONFIG[w][0]],
        frozen_q2_by_theta=[str(x) for x in CONFIG[w][1]],
        frozen_actual_observation_Y1_Y2=[1,0],
        exact_full_data_Bayes_posterior_theta0_theta1_theta2=[str(v) for v in exact],
        nine_rejection_ABC_discrepancy_epsilon_certificates=scenarios,
        full_source_vs_Bernoulli_exact_likelihood_all_four_possible_Y_verified=True)
def locked_claims():
    for w in WORLDS:
        exact=exact_full_bayes(w)
        for kind in DISTANCES:
            for eps in EPS:
                a=source_rejection_ABC(w,kind,eps)
                assert a==analytic_ABC(w,kind,eps)
                if eps==2 or (kind in ("COUNT_SUM","FIRST_COMPONENT") and eps==1):
                    assert a[0]==(F(1,3),)*3
        assert source_rejection_ABC(w,"FULL_HAMMING",0)[0]==exact
    x="COMPLEMENTARY_GRADIENT";y="REVERSED_COMPLEMENT"
    assert exact_full_bayes(x)==(F(1,14),F(2,7),F(9,14))
    assert exact_full_bayes(y)==(F(9,14),F(2,7),F(1,14))
    assert all(count_distribution(x,t)==count_distribution(y,t) for t in THETA)
    assert source_rejection_ABC(x,"COUNT_SUM",0)[0]==(F(5,14),F(2,7),F(5,14))
    assert source_rejection_ABC(y,"COUNT_SUM",0)[0]==(F(5,14),F(2,7),F(5,14))
    assert exact_full_bayes("IID_GRADIENT")== (F(3,10),F(2,5),F(3,10))
    assert source_rejection_ABC("IID_GRADIENT","COUNT_SUM",0)[0]==exact_full_bayes("IID_GRADIENT")
    assert source_rejection_ABC("FIRST_ONLY_INFORMATIVE","FIRST_COMPONENT",0)[0]==exact_full_bayes("FIRST_ONLY_INFORMATIVE")
    assert source_rejection_ABC("SECOND_ONLY_INFORMATIVE","FIRST_COMPONENT",0)[0]==(F(1,3),)*3
    assert exact_full_bayes("SECOND_ONLY_INFORMATIVE")!=(F(1,3),)*3
    for kind in DISTANCES:
        for eps in EPS:assert source_rejection_ABC("NO_SIGNAL",kind,eps)[0]==(F(1,3),)*3
    assert exact_full_bayes("DETERMINISTIC_ENDS")==(ZERO,F(1,5),F(4,5))
    return True
def emit():
    locked_claims()
    data=dict(research_id="R264",original_catalogue_id="11-024",
       prescore_freeze_commit=FREEZE,
       scientific_scope="FINITE_ARTIFICIAL_E1_DISCRETE_REJECTION_ABC_VERSUS_EXACT_FULL_BAYES",
       frozen_worlds=9,all_complete_original_theta_simulation_source_atoms=432,
       finite_equal_prior_theta_categories=3,
       all_four_bits_random_uniform_under_each_theta=True,
       abc_acceptance_is_simulation_only_not_explicit_likelihood=True,
       analytic_bernoulli_likelihood_is_separate_exact_benchmark=True,
       epsilon_0_full_Hamming_is_full_exact_Bayes_for_all_worlds=True,
       epsilon_2_all_discrepancies_recover_uninformative_prior=True,
       count_summary_observation_alias_in_complement_vs_reverse=True,
       no_local_linear_Beaumont_regression_or_real_genetics_inference=True,
       new_real_human_E2=0,new_real_historical_E3=0,R073="FROZEN",PESEN_v0_1="FROZEN",
       world_results=[summary(w) for w in WORLDS])
    out=HERE/"R264_ALL_432_ORIGINAL_THETA_SIMULATOR_SOURCE_ATOMS.csv"
    keys=list(sources(WORLDS[0])[0])
    with out.open("w",newline="",encoding="utf-8") as f:
        wr=csv.DictWriter(f,fieldnames=keys,lineterminator="\n");wr.writeheader()
        for w in WORLDS:
            for z in sources(w):wr.writerow({k:str(z[k]) for k in keys})
    jp=HERE/"R264_EXACT_RESULTS.json"
    jp.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    rec=dict(research_id="R264",original_catalogue_id="11-024",
       frozen_worlds=9,complete_original_theta_rng_source_atoms=432,
       all_81_ABC_source_and_analytic_posterior_comparisons_verified=True,
       summary_insufficiency_alias_theta_position_reversal=True,
       exact_full_observation_epsilon_zero_recovers_Bayes=True,
       epsilon_loose_posterior_reverts_to_prior=True,
       source_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),
       results_sha256=hashlib.sha256(jp.read_bytes()).hexdigest(),
       new_real_human_E2=0,new_real_historical_E3=0)
    (HERE/"R264_FINAL_MACHINE_ACCEPTANCE.json").write_text(json.dumps(rec,indent=2)+"\n",encoding="utf-8")
    return rec
class Tests(unittest.TestCase):
    def test_nine(self):self.assertEqual(len(WORLDS),9)
    def test_432(self):self.assertEqual(sum(len(sources(w)) for w in WORLDS),432)
    def test_frozen(self):self.assertTrue(locked_claims())
    def test_full(self):self.assertEqual(exact_full_bayes("COMPLEMENTARY_GRADIENT"),(F(1,14),F(2,7),F(9,14)))
    def test_reverse(self):self.assertEqual(exact_full_bayes("REVERSED_COMPLEMENT"),(F(9,14),F(2,7),F(1,14)))
    def test_count_alias(self):self.assertEqual(source_rejection_ABC("COMPLEMENTARY_GRADIENT","COUNT_SUM",0)[0],source_rejection_ABC("REVERSED_COMPLEMENT","COUNT_SUM",0)[0])
    def test_sufficient_count(self):self.assertEqual(source_rejection_ABC("IID_GRADIENT","COUNT_SUM",0)[0],exact_full_bayes("IID_GRADIENT"))
    def test_sufficient_first(self):self.assertEqual(source_rejection_ABC("FIRST_ONLY_INFORMATIVE","FIRST_COMPONENT",0)[0],exact_full_bayes("FIRST_ONLY_INFORMATIVE"))
    def test_flat(self):self.assertEqual(exact_full_bayes("NO_SIGNAL"),(F(1,3),)*3)
    def test_invalid(self):
        with self.assertRaises(ValueError):sources("UNFROZEN")
def _case(w,k):
    def t(self):
        src=sources(w)
        if k=="mass":self.assertEqual(sum((r["original_full_theta_rng_source_probability"] for r in src),ZERO),ONE)
        elif k=="unique":
            fields=["original_theta"]+[f"oracle_original_random_bit_{i}" for i in range(4)]
            self.assertEqual(len({tuple(z[v] for v in fields) for z in src}),48)
        elif k=="positive":self.assertTrue(all(z["original_full_theta_rng_source_probability"]==F(1,48) for z in src))
        elif k=="bits":
            for z in src:
                raw=tuple(z[f"oracle_original_random_bit_{i}"] for i in range(4))
                self.assertEqual((z["observed_simulated_Y1"],z["observed_simulated_Y2"]),simulator(w,z["original_theta"],raw))
        elif k=="posterior":
            for kind in DISTANCES:
                for eps in EPS:self.assertEqual(source_rejection_ABC(w,kind,eps),analytic_ABC(w,kind,eps))
        elif k=="exact":self.assertEqual(source_rejection_ABC(w,"FULL_HAMMING",0)[0],exact_full_bayes(w))
        elif k=="normalized":
            for kind in DISTANCES:
                for eps in EPS:self.assertEqual(sum(source_rejection_ABC(w,kind,eps)[0],ZERO),ONE)
        elif k=="report":self.assertEqual(summary(w)["all_original_theta_rng_source_atoms"],48)
        else:raise AssertionError("bad frozen test")
    return t
for w in WORLDS:
    for k in ("mass","unique","positive","bits","posterior","exact","normalized","report"):
        setattr(Tests,"test_"+w.lower()+"_"+k,_case(w,k))
if __name__=="__main__":
    a=argparse.ArgumentParser();g=a.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true");g.add_argument("--emit",action="store_true")
    x=a.parse_args()
    if x.test:unittest.main(argv=["r264"],verbosity=2)
    else:print(json.dumps(emit(),indent=2))
