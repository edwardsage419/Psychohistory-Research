#!/usr/bin/env python3
"""R226: finite exact homophily, latent causes, randomized messages and peer effects.

Eight frozen artificial SCMs, sixteen independent exogenous atom types per
world. Observed peer coefficients use only (E,A0,B0,B1), while the true
do(A0) causal effect uses separately retained artificial oracle outcomes.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import itertools
import unittest
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path

HERE=Path(__file__).resolve().parent
ZERO=F(0)
ONE=F(1)
WORLDS=(
 "PEER_COPY",
 "SHARED_LATENT_SHOCK",
 "HOMOPHILY_ONLY",
 "HOMOPHILY_WITH_COPY",
 "RANDOMIZED_PEER_COPY",
 "RANDOMIZED_NO_COPY",
 "RANDOMIZED_SIGNAL_ON_HOMOPHILY_NETWORK",
 "ANTI_PEER_COPY",
)
RANDOMIZED=("RANDOMIZED_PEER_COPY","RANDOMIZED_NO_COPY",
            "RANDOMIZED_SIGNAL_ON_HOMOPHILY_NETWORK")
HOMOPHILY=("HOMOPHILY_ONLY","HOMOPHILY_WITH_COPY",
           "RANDOMIZED_SIGNAL_ON_HOMOPHILY_NETWORK")
FROZEN_COMMIT="e86adecc5745ba5b7bafb6eda5511838418df00a"

def link(world,u,v):
    if world not in WORLDS or u not in (0,1) or v not in (0,1):
        raise ValueError("invalid frozen link source")
    return int(u==v) if world in HOMOPHILY else 1

def sender(world,u,r):
    if world not in WORLDS or u not in (0,1) or r not in (0,1):
        raise ValueError("invalid frozen sender source")
    return r if world in RANDOMIZED else u

def receiver_next(world,u,v,a,e):
    if world not in WORLDS or any(k not in (0,1) for k in (u,v,a,e)):
        raise ValueError("invalid structural receiver state")
    if world in ("PEER_COPY","RANDOMIZED_PEER_COPY"): return a
    if world in ("SHARED_LATENT_SHOCK","RANDOMIZED_NO_COPY"): return u
    if world=="HOMOPHILY_ONLY": return v
    if world in ("HOMOPHILY_WITH_COPY","RANDOMIZED_SIGNAL_ON_HOMOPHILY_NETWORK"):
        return a if e else v
    if world=="ANTI_PEER_COPY": return 1-a
    raise AssertionError("unfrozen world")

def source_atom(world,u,v,r,q):
    if world not in WORLDS or any(k not in (0,1) for k in (u,v,r,q)):
        raise ValueError("out-of-support exogenous source")
    e=link(world,u,v)
    a=sender(world,u,r)
    b1=receiver_next(world,u,v,a,e)
    return dict(world=world,oracle_U=u,oracle_V=v,external_random_R=r,
                independent_background_Q=q,
                observed_edge_E=e,observed_sender_A0=a,
                observed_receiver_B0=v,observed_receiver_B1=b1,
                oracle_B1_doA0=receiver_next(world,u,v,0,e),
                oracle_B1_doA1=receiver_next(world,u,v,1,e),
                original_probability=F(1,16))

def full_sources(world):
    if world not in WORLDS: raise ValueError("unknown frozen model")
    data=tuple(source_atom(world,*s) for s in itertools.product((0,1),repeat=4))
    assert len(data)==16
    assert sum((row["original_probability"] for row in data),ZERO)==ONE
    return data

def observation_signature(rows):
    # No oracle, latent source, or intervention outcome is read here.
    joint=defaultdict(F)
    for row in rows:
        key=tuple(row["observed_"+k] for k in (
            "edge_E","sender_A0","receiver_B0","receiver_B1"))
        joint[key]+=row["original_probability"]
    if sum(joint.values(),ZERO)!=ONE: raise AssertionError("missing observed mass")
    return dict(sorted(joint.items()))

def analytic_observation_signature(world):
    # Independent marginal law: integrate out the unused Q at the outset.
    # Enumerate only 2^3 U,V,R states, each with mass 1/8.
    result=defaultdict(F)
    for u,v,r in itertools.product((0,1),repeat=3):
        e=link(world,u,v)
        a=sender(world,u,r)
        b=receiver_next(world,u,v,a,e)
        result[(e,a,v,b)]+=F(1,8)
    return dict(sorted(result.items()))

def observed_peer_contrast(rows):
    numer=defaultdict(F)
    denom=defaultdict(F)
    adjacent=ZERO
    discordant=ZERO
    for row in rows:
        p=row["original_probability"]
        if row["observed_edge_E"]:
            adjacent+=p
            a=row["observed_sender_A0"]
            numer[a]+=p*row["observed_receiver_B1"]
            denom[a]+=p
            if row["observed_sender_A0"]!=row["observed_receiver_B0"]:
                discordant+=p
    if adjacent==0 or denom[0]==0 or denom[1]==0:
        raise AssertionError("frozen connected comparison unsupported")
    return dict(connected_probability=adjacent,
                conditional_discordance_probability=discordant/adjacent,
                observed_connected_peer_contrast=numer[1]/denom[1]-numer[0]/denom[0])

def oracle_peer_contrast(rows):
    p_connected=ZERO
    total=ZERO
    conditional_numerator=ZERO
    for row in rows:
        p=row["original_probability"]
        diff=row["oracle_B1_doA1"]-row["oracle_B1_doA0"]
        total+=p*diff
        if row["observed_edge_E"]:
            p_connected+=p
            conditional_numerator+=p*diff
    assert p_connected>0
    return dict(true_population_peer_effect=total,
                true_connected_peer_effect=conditional_numerator/p_connected)

def independent_oracle_formula(world):
    if world in ("PEER_COPY","RANDOMIZED_PEER_COPY"): return ONE,ONE
    if world in ("SHARED_LATENT_SHOCK","HOMOPHILY_ONLY","RANDOMIZED_NO_COPY"):
        return ZERO,ZERO
    if world in ("HOMOPHILY_WITH_COPY","RANDOMIZED_SIGNAL_ON_HOMOPHILY_NETWORK"):
        return F(1,2),ONE
    if world=="ANTI_PEER_COPY": return -ONE,-ONE
    raise ValueError("unfrozen theory")

def world_results(world):
    data=full_sources(world)
    source_joint=observation_signature(data)
    analytic_joint=analytic_observation_signature(world)
    if source_joint!=analytic_joint: raise AssertionError("marginal Q integration changes observed data")
    obs=observed_peer_contrast(data)
    true=oracle_peer_contrast(data)
    if (true["true_population_peer_effect"],true["true_connected_peer_effect"]) != independent_oracle_formula(world):
        raise AssertionError("independent structural intervention formula mismatch")
    return dict(world=world,
                original_exogenous_atoms=16,
                full_source_probability_sum="1",
                observed_edge_probability=str(obs["connected_probability"]),
                observed_discordance_probability_given_edge=str(obs["conditional_discordance_probability"]),
                observed_peer_difference_given_edge=str(obs["observed_connected_peer_contrast"]),
                oracle_true_population_doA_peer_effect=str(true["true_population_peer_effect"]),
                oracle_true_connected_doA_peer_effect=str(true["true_connected_peer_effect"]),
                observable_joint_support_cells=len(source_joint),
                observation_signature={
                    "".join(map(str,k)):str(v) for k,v in source_joint.items()
                },
                artificial_sender_signal_independent_of_U_V=world in RANDOMIZED)

def generate():
    out_worlds=[world_results(w) for w in WORLDS]
    exact={w:observation_signature(full_sources(w)) for w in WORLDS}
    assert exact["PEER_COPY"]==exact["SHARED_LATENT_SHOCK"]
    assert exact["HOMOPHILY_ONLY"]==exact["HOMOPHILY_WITH_COPY"]
    assert independent_oracle_formula("PEER_COPY")!=(independent_oracle_formula("SHARED_LATENT_SHOCK"))
    assert independent_oracle_formula("HOMOPHILY_ONLY")!=(independent_oracle_formula("HOMOPHILY_WITH_COPY"))
    result=dict(research_id="R226",original_catalogue_id="09-017",
                scientific_scope="FINITE_ARTIFICIAL_E1_ONLY",
                prescore_protocol_commit=FROZEN_COMMIT,
                frozen_worlds=8,full_original_source_atoms=128,
                original_sources_each_world=16,
                all_exact_observable_alias_pairs_verified=True,
                new_human_E2=0,new_historical_E3=0,
                R073="FROZEN",PESEN_v0_1="FROZEN",world_results=out_worlds)
    src=HERE/"R226_ALL_128_ORIGINAL_SELECTION_INFLUENCE_ATOMS.csv"
    headers=list(source_atom("PEER_COPY",0,0,0,0))
    with src.open("w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=headers,lineterminator="\n")
        writer.writeheader()
        for w in WORLDS:
            for row in full_sources(w):
                writer.writerow({key:str(row[key]) for key in headers})
    a=HERE/"R226_EXACT_RESULTS.json"
    a.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    receipt=dict(research_id="R226",catalogue_id="09-017",frozen_worlds=8,
                 full_original_source_atoms=128,
                 independent_eight_state_observed_marginal_parity=True,
                 independent_oracle_structural_parity=True,
                 observed_alias_pairs=2,
                 source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),
                 result_sha256=hashlib.sha256(a.read_bytes()).hexdigest(),
                 new_real_human_E2=0,new_real_historical_E3=0)
    (HERE/"R226_FINAL_MACHINE_ACCEPTANCE.json").write_text(
        json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_eight_worlds(self): self.assertEqual(len(WORLDS),8)
    def test_total_source_count(self): self.assertEqual(sum(len(full_sources(w)) for w in WORLDS),128)
    def test_alias_common(self):
        self.assertEqual(observation_signature(full_sources("PEER_COPY")),
                         observation_signature(full_sources("SHARED_LATENT_SHOCK")))
    def test_alias_homophily(self):
        self.assertEqual(observation_signature(full_sources("HOMOPHILY_ONLY")),
                         observation_signature(full_sources("HOMOPHILY_WITH_COPY")))
    def test_alias_causes_differ(self):
        self.assertEqual(independent_oracle_formula("PEER_COPY"),(ONE,ONE))
        self.assertEqual(independent_oracle_formula("SHARED_LATENT_SHOCK"),(ZERO,ZERO))
    def test_homophily_cause_differ(self):
        self.assertEqual(independent_oracle_formula("HOMOPHILY_ONLY"),(ZERO,ZERO))
        self.assertEqual(independent_oracle_formula("HOMOPHILY_WITH_COPY"),(F(1,2),ONE))
    def test_homophily_no_discordance(self):
        for w in ("HOMOPHILY_ONLY","HOMOPHILY_WITH_COPY"):
            self.assertEqual(world_results(w)["observed_discordance_probability_given_edge"],"0")
            self.assertEqual(world_results(w)["observed_peer_difference_given_edge"],"1")
    def test_random_activated_discordance(self):
        w=world_results("RANDOMIZED_SIGNAL_ON_HOMOPHILY_NETWORK")
        self.assertEqual(w["observed_discordance_probability_given_edge"],"1/2")
        self.assertEqual(w["observed_peer_difference_given_edge"],"1")
    def test_random_null(self):
        w=world_results("RANDOMIZED_NO_COPY")
        self.assertEqual(w["observed_peer_difference_given_edge"],"0")
        self.assertEqual(w["oracle_true_population_doA_peer_effect"],"0")
    def test_anti_peer_copy(self):
        w=world_results("ANTI_PEER_COPY")
        self.assertEqual(w["observed_peer_difference_given_edge"],"-1")
        self.assertEqual(w["oracle_true_population_doA_peer_effect"],"-1")
    def test_source_truth_consistency(self):
        for w in WORLDS:
            for row in full_sources(w):
                expected=(row["oracle_B1_doA1"] if row["observed_sender_A0"] else row["oracle_B1_doA0"])
                self.assertEqual(row["observed_receiver_B1"],expected)
    def test_invalid_link(self):
        with self.assertRaises(ValueError): link("UNKNOWN",0,0)
    def test_invalid_source(self):
        with self.assertRaises(ValueError): source_atom("PEER_COPY",0,0,0,2)

def _case(world,what):
    def test(self):
        source=full_sources(world)
        if what=="mass":
            self.assertEqual(sum((x["original_probability"] for x in source),ZERO),ONE)
        elif what=="unique":
            self.assertEqual(len({(x["oracle_U"],x["oracle_V"],x["external_random_R"],
                                   x["independent_background_Q"]) for x in source}),16)
        elif what=="observed":
            self.assertEqual(observation_signature(source),analytic_observation_signature(world))
        elif what=="oracle":
            d=oracle_peer_contrast(source)
            self.assertEqual((d["true_population_peer_effect"],d["true_connected_peer_effect"]),
                             independent_oracle_formula(world))
        elif what=="edge":
            k=observed_peer_contrast(source)
            self.assertGreater(k["connected_probability"],0)
        elif what=="report":
            self.assertEqual(world_results(world)["original_exogenous_atoms"],16)
        else: raise AssertionError("unfrozen test")
    return test
for _w in WORLDS:
    for _kind in ("mass","unique","observed","oracle","edge","report"):
        setattr(Tests,"test_"+_w.lower()+"_"+_kind,_case(_w,_kind))

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--test",action="store_true")
    group.add_argument("--emit",action="store_true")
    args=parser.parse_args()
    if args.test: unittest.main(argv=["r226"],verbosity=2)
    else: print(json.dumps(generate(),ensure_ascii=False,indent=2))
