#!/usr/bin/env python3
"""R289 artificial four-offer bounded search and stopping, 486 original sources.

A hindsight full-information maximum is marked nondeployable; no human data.
"""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parent
FREEZE="27fa695d5e0c612fd77fb3a3fc5af26a543c0a27"
Z,O=F(0),F(1);VALUES=(1,3,5)
DGP={
 "UNIFORM":(F(1,3),F(1,3),F(1,3)),
 "LOW_HEAVY":(F(1,2),F(1,4),F(1,4)),
 "HIGH_HEAVY":(F(1,4),F(1,4),F(1,2))}
THRESHOLDS=(3,5)
WORLD=tuple((name,t) for name in DGP for t in THRESHOLDS)
SOURCES=tuple(itertools.product(VALUES,repeat=4))
COST=F(1,2)
def validate(name,t):
    if (name,t) not in WORLD:raise ValueError("unfrozen offer distribution or aspiration")
def prob(name,offers):
    if name not in DGP:raise ValueError("unknown")
    if tuple(offers) not in SOURCES:raise ValueError("must be four ordered offers from {1,3,5}")
    ps=dict(zip(VALUES,DGP[name]))
    p=O
    for x in offers:p*=ps[x]
    return p
def decision(offers,threshold):
    if threshold not in THRESHOLDS:raise ValueError("unfrozen aspiration")
    if tuple(offers) not in SOURCES:raise ValueError("wrong source")
    stop=4
    for i,value in enumerate(offers,1):
        if value>=threshold:
            stop=i;break
    chosen=offers[stop-1]
    achieved=int(chosen>=threshold)
    net=F(chosen)-COST*(stop-1)
    return stop,chosen,achieved,net
def row(name,t,offers):
    validate(name,t)
    stop,choice,achieved,net=decision(offers,t)
    return dict(world=name+"_"+str(t),distribution=name,aspiration=t,
      complete_ordered_four_offer_source="".join(str(x) for x in offers),
      complete_source_probability=prob(name,offers),
      stopped_at_offer_index=stop,observed_offer_count=stop,
      aspiration_met=int(bool(achieved)),
      chosen_payoff=choice,search_cost=COST*(stop-1),net_payoff=net,
      first_offer_only_payoff=offers[0],
      infeasible_full_future_information_maximum_payoff=max(offers))
def source_rows(name,t):
    validate(name,t)
    for offers in SOURCES:yield row(name,t,offers)
def source_moments(name,t):
    rs=tuple(source_rows(name,t))
    assert len(rs)==81 and sum((z["complete_source_probability"] for z in rs),Z)==O
    fields=("net_payoff","observed_offer_count","first_offer_only_payoff",
       "infeasible_full_future_information_maximum_payoff")
    e=[sum((z["complete_source_probability"]*z[field] for z in rs),Z) for field in fields]
    unmet=sum((z["complete_source_probability"]*(1-z["aspiration_met"]) for z in rs),Z)
    return (*e,unmet)
def analytic(name,t):
    validate(name,t)
    ps=dict(zip(VALUES,DGP[name]))
    q=sum((ps[x] for x in VALUES if x<t),Z)
    hitpay=sum((ps[x]*x for x in VALUES if x>=t),Z)
    mu=sum((ps[x]*x for x in VALUES),Z)
    inspected=O+q+q*q+q*q*q
    collected=hitpay*(O+q+q*q)+q**3*mu
    net=collected-COST*(inspected-O)
    p1=ps[1];p3=ps[3]
    oracle=O+2*(O-p1**4)+2*(O-(p1+p3)**4)
    return net,inspected,mu,oracle,q**4
def claims():
    assert len(SOURCES)==81 and len(WORLD)==6
    for name,t in WORLD:
        assert source_moments(name,t)==analytic(name,t)
        net,n,first,oracle,unmet=analytic(name,t)
        assert oracle>=first
        assert Z<=unmet<=O and O<=n<=4
    assert decision((1,1,1,1),5)==(4,1,0,F(-1,2))
    assert decision((5,1,1,1),5)==(1,5,1,F(5))
    return True
def emit():
    claims()
    src=ROOT/"R289_ALL_486_ORIGINAL_SEQUENTIAL_OFFER_SOURCES.csv"
    cols=("world","distribution","aspiration","complete_ordered_four_offer_source",
      "complete_source_probability","stopped_at_offer_index","observed_offer_count",
      "aspiration_met","chosen_payoff","search_cost","net_payoff",
      "first_offer_only_payoff","infeasible_full_future_information_maximum_payoff")
    with src.open("w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=cols,lineterminator="\n");writer.writeheader()
        for name,t in WORLD:
            for z in source_rows(name,t):writer.writerow({k:str(z[k]) for k in cols})
    result=dict(research_id="R289",catalogue_original_id="01-004",freeze_commit=FREEZE,
      scientific_scope="BOUNDED_ARTIFICIAL_E1_SEQ_SEARCH_SATISFICING_NOT_REAL_SIMON_BEHAVIORAL_EVIDENCE",
      six_artificial_worlds=6,original_source_types=486,nondeployable_oracle_explicit=True,
      E2_human=0,E3_historical=0,R073="FROZEN",PESEN_v0_1="FROZEN",
      worlds=[dict(distribution=name,aspiration=t,complete_source_types=81,
        expected_net_payoff=str(source_moments(name,t)[0]),
        expected_observed_offers=str(source_moments(name,t)[1]),
        first_offer_baseline_mean=str(source_moments(name,t)[2]),
        nondeployable_perfect_foresight_max_mean=str(source_moments(name,t)[3]),
        probability_aspiration_never_met=str(source_moments(name,t)[4]),
        independent_analytic_agreement=True) for name,t in WORLD])
    path=ROOT/"R289_EXACT_SATISFICING_RESULTS.json"
    path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    receipt=dict(research_id="R289",freeze_commit=FREEZE,complete_original_sources=486,
      source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),
      results_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),new_human_E2=0,new_historical_E3=0)
    (ROOT/"R289_MACHINE_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n")
    return receipt
class Tests(unittest.TestCase):
    def test_claims(self):self.assertTrue(claims())
    def test_worlds(self):self.assertEqual(len(WORLD),6)
    def test_sources(self):self.assertEqual(len(SOURCES),81)
    def test_early_achieve(self):self.assertEqual(decision((5,1,1,1),5)[0],1)
    def test_force_stop(self):self.assertEqual(decision((1,1,1,1),5)[2],0)
    def test_last_achieve(self):self.assertEqual(decision((1,1,1,5),5)[0],4)
    def test_threshold3(self):self.assertEqual(decision((1,3,5,1),3)[0],2)
    def test_cost(self):self.assertEqual(decision((1,1,1,1),5)[3],F(-1,2))
    def test_bad_threshold(self):
        with self.assertRaises(ValueError):decision((1,3,5,1),4)
    def test_bad_offer(self):
        with self.assertRaises(ValueError):decision((1,2,3,5),3)
def make(name,t,k):
    def fn(self):
        rs=tuple(source_rows(name,t))
        if k=="length":self.assertEqual(len(rs),81)
        elif k=="mass":self.assertEqual(sum((x["complete_source_probability"] for x in rs),Z),O)
        elif k=="unique":self.assertEqual(len({x["complete_ordered_four_offer_source"] for x in rs}),81)
        elif k=="analytic":self.assertEqual(source_moments(name,t),analytic(name,t))
        elif k=="positive":self.assertTrue(all(x["complete_source_probability"]>0 for x in rs))
        elif k=="net":
            for x in rs:self.assertEqual(x["net_payoff"],F(x["chosen_payoff"])-x["search_cost"])
        elif k=="source":
            for x in rs:self.assertEqual(x["complete_source_probability"],prob(name,tuple(map(int,x["complete_ordered_four_offer_source"]))))
        elif k=="first":self.assertEqual(source_moments(name,t)[2],sum((DGP[name][i]*VALUES[i] for i in range(3)),Z))
        elif k=="forced":
            for x in rs:
                if x["aspiration_met"]==0:self.assertEqual(x["observed_offer_count"],4)
        elif k=="oracle":
            for x in rs:self.assertGreaterEqual(x["infeasible_full_future_information_maximum_payoff"],x["chosen_payoff"])
        else:raise AssertionError(k)
    return fn
for name,t in WORLD:
    for k in ("length","mass","unique","analytic","positive","net","source","first","forced","oracle"):
        setattr(Tests,"test_"+name.lower()+"_"+str(t)+"_"+k,make(name,t,k))
if __name__=="__main__":
    a=argparse.ArgumentParser()
    g=a.add_mutually_exclusive_group(required=True);g.add_argument("--test",action="store_true");g.add_argument("--emit",action="store_true")
    cmd=a.parse_args()
    if cmd.test:unittest.main(argv=["r289"],verbosity=1)
    else:print(json.dumps(emit(),indent=2))
