#!/usr/bin/env python3
"""R236 finite survey response bias: measured answers vs true private states.

Nine fully frozen artificial binary response mechanisms. Independent survey mode
R is randomized and observed; hidden true belief outcomes B1/B2 and source U
are only used in oracle checks. Two pre-mode proxy measurements P/Z have
independent 1/2 missingness indicators, not perfect post-mode truth measures.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import itertools
import json
import unittest
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path

HERE=Path(__file__).resolve().parent
ZERO=F(0)
ONE=F(1)
FREEZE="fe60b543c601b409a0f3d4737ac9ce06a3fd5d6b"
WORLDS=(
 "TRUTHFUL_STABLE",
 "TRUE_MODE_CHANGE",
 "REPORT_MODE_CHANGE_ALIAS",
 "TRUE_MODE_COMPLIER_ONLY",
 "REPORT_MODE_COMPLIER_ONLY_ALIAS",
 "SOCIAL_DESIRABILITY_U",
 "MODE_SUPPRESS_REPORT",
 "SHARED_ACQUIESCENCE_RESPONSE",
 "SHARED_TRUE_CONSTRUCT_ALIAS",
)
SOURCES=("T","S","U","R","E1","E2")
OBS=("observed_mode_R","observed_prior_proxy_P","observed_prior_proxy_Z",
     "observed_report_Y1","observed_report_Y2")
ORACLE_TRUE_MODE_EFFECT={
 "TRUTHFUL_STABLE":"0",
 "TRUE_MODE_CHANGE":"1/2",
 "REPORT_MODE_CHANGE_ALIAS":"0",
 "TRUE_MODE_COMPLIER_ONLY":"1/4",
 "REPORT_MODE_COMPLIER_ONLY_ALIAS":"0",
 "SOCIAL_DESIRABILITY_U":"0",
 "MODE_SUPPRESS_REPORT":"0",
 "SHARED_ACQUIESCENCE_RESPONSE":"0",
 "SHARED_TRUE_CONSTRUCT_ALIAS":"0",
}
EXPECTED_REPORTED_MODE_ITT={
 "TRUTHFUL_STABLE":"0",
 "TRUE_MODE_CHANGE":"1/2",
 "REPORT_MODE_CHANGE_ALIAS":"1/2",
 "TRUE_MODE_COMPLIER_ONLY":"1/4",
 "REPORT_MODE_COMPLIER_ONLY_ALIAS":"1/4",
 "SOCIAL_DESIRABILITY_U":"0",
 "MODE_SUPPRESS_REPORT":"-1/2",
 "SHARED_ACQUIESCENCE_RESPONSE":"0",
 "SHARED_TRUE_CONSTRUCT_ALIAS":"0",
}
ALIASES=(
 ("TRUE_MODE_CHANGE","REPORT_MODE_CHANGE_ALIAS"),
 ("TRUE_MODE_COMPLIER_ONLY","REPORT_MODE_COMPLIER_ONLY_ALIAS"),
 ("SHARED_ACQUIESCENCE_RESPONSE","SHARED_TRUE_CONSTRUCT_ALIAS")
)

def mechanism(world,t,s,u,r):
    if world not in WORLDS or any(v not in (0,1) for v in (t,s,u,r)):
        raise ValueError("unfrozen response mechanism")
    b1=t
    b2=s
    y1=t
    y2=s
    if world=="TRUE_MODE_CHANGE":
        b1=int(bool(t or r))
        y1=b1
    elif world=="REPORT_MODE_CHANGE_ALIAS":
        y1=int(bool(t or r))
    elif world=="TRUE_MODE_COMPLIER_ONLY":
        b1=int(bool(t or (r and u)))
        y1=b1
    elif world=="REPORT_MODE_COMPLIER_ONLY_ALIAS":
        y1=int(bool(t or (r and u)))
    elif world=="SOCIAL_DESIRABILITY_U":
        y1=int(bool(t or u))
        y2=int(bool(s or u))
    elif world=="MODE_SUPPRESS_REPORT":
        y1=int(bool(t and not r))
    elif world=="SHARED_ACQUIESCENCE_RESPONSE":
        y2=y1
    elif world=="SHARED_TRUE_CONSTRUCT_ALIAS":
        b2=t
        y2=t
    return (b1,b2,y1,y2)

def source_atom(world,t,s,u,r,e1,e2):
    if world not in WORLDS or any(v not in (0,1) for v in (t,s,u,r,e1,e2)):
        raise ValueError("invalid original survey exogenous source")
    b1,b2,y1,y2=mechanism(world,t,s,u,r)
    proxy_p=t if e1 else -1
    proxy_z=t if e2 else -1
    return dict(
        world=world,oracle_original_T=t,oracle_original_S=s,
        oracle_original_U=u,oracle_original_R=r,
        oracle_proxy_ascertainment_E1=e1,oracle_proxy_ascertainment_E2=e2,
        observed_mode_R=r,observed_prior_proxy_P=proxy_p,
        observed_prior_proxy_Z=proxy_z,
        observed_report_Y1=y1,observed_report_Y2=y2,
        oracle_current_private_B1=b1,oracle_current_private_B2=b2,
        oracle_B1_doR0=mechanism(world,t,s,u,0)[0],
        oracle_B1_doR1=mechanism(world,t,s,u,1)[0],
        original_probability=F(1,64)
    )

def source_rows(world):
    if world not in WORLDS:raise ValueError("unknown frozen model")
    rows=tuple(source_atom(world,*p) for p in itertools.product((0,1),repeat=6))
    if len(rows)!=64 or sum((r["original_probability"] for r in rows),ZERO)!=ONE:
        raise AssertionError("complete survey original sources missing")
    return rows

def observed_joint_from_sources(world):
    joint=defaultdict(F)
    for row in source_rows(world):
        joint[tuple(row[k] for k in OBS)]+=row["original_probability"]
    return dict(sorted(joint.items()))

def independent_observed_joint(world):
    """Integrate measurement ascertainment analytically; do not read source rows."""
    joint=defaultdict(F)
    for t,s,u,r in itertools.product((0,1),repeat=4):
        b1,b2,y1,y2=mechanism(world,t,s,u,r)
        del b1,b2
        for p in (-1,t):
            for z in (-1,t):
                joint[(r,p,z,y1,y2)]+=F(1,16)*F(1,2)*F(1,2)
    return dict(sorted(joint.items()))

def observable_mode_ITT(world):
    # This estimator reads R and Y1 only, not oracle private state columns.
    numerator={0:ZERO,1:ZERO}
    mass={0:ZERO,1:ZERO}
    for x in source_rows(world):
        r=x["observed_mode_R"]
        w=x["original_probability"]
        mass[r]+=w
        numerator[r]+=w*x["observed_report_Y1"]
    if mass!={0:F(1,2),1:F(1,2)}:
        raise AssertionError("mode not randomized at P=1/2")
    return numerator[1]/mass[1]-numerator[0]/mass[0]

def true_private_mode_effect_from_sources(world):
    return sum((r["original_probability"]*(r["oracle_B1_doR1"]-r["oracle_B1_doR0"])
                for r in source_rows(world)),ZERO)

def independent_true_mode_effect(world):
    # Counterfactual intervention is explicitly recomputed at each T,S,U;
    # no human posterior, response records or observed ITT are read.
    return sum((F(mechanism(world,t,s,u,1)[0]-mechanism(world,t,s,u,0)[0],8)
                for t,s,u in itertools.product((0,1),repeat=3)),ZERO)

def binary_cov_from_original(world,a,b):
    rows=source_rows(world)
    mu_a=sum((r["original_probability"]*r[a] for r in rows),ZERO)
    mu_b=sum((r["original_probability"]*r[b] for r in rows),ZERO)
    return sum((r["original_probability"]*(r[a]-mu_a)*(r[b]-mu_b) for r in rows),ZERO)

def mismatch_rates(world):
    rows=source_rows(world)
    return (
        sum((r["original_probability"]*int(r["observed_report_Y1"]!=r["oracle_current_private_B1"])
             for r in rows),ZERO),
        sum((r["original_probability"]*int(r["observed_report_Y2"]!=r["oracle_current_private_B2"])
             for r in rows),ZERO)
    )

def verify_aliases():
    for a,b in ALIASES:
        first=source_rows(a);second=source_rows(b)
        for x,y in zip(first,second):
            if any(x[k]!=y[k] for k in OBS):
                raise AssertionError("full questionnaire observational source alias broken")
        if observed_joint_from_sources(a)!=observed_joint_from_sources(b):
            raise AssertionError("full questionnaire observable distribution alias broken")
    assert true_private_mode_effect_from_sources("TRUE_MODE_CHANGE")==F(1,2)
    assert true_private_mode_effect_from_sources("REPORT_MODE_CHANGE_ALIAS")==ZERO
    assert binary_cov_from_original("SHARED_ACQUIESCENCE_RESPONSE","oracle_current_private_B1","oracle_current_private_B2")==ZERO
    assert binary_cov_from_original("SHARED_TRUE_CONSTRUCT_ALIAS","oracle_current_private_B1","oracle_current_private_B2")==F(1,4)
    return True

def world_result(world):
    rows=source_rows(world)
    obs=observed_joint_from_sources(world)
    if obs!=independent_observed_joint(world):
        raise AssertionError("independent four latent source+two proxy marginal route does not reproduce observation")
    observed_effect=observable_mode_ITT(world)
    true_effect=true_private_mode_effect_from_sources(world)
    if true_effect!=independent_true_mode_effect(world):
        raise AssertionError("structural intervention formula/source oracle disagreement")
    if str(observed_effect)!=EXPECTED_REPORTED_MODE_ITT[world] or str(true_effect)!=ORACLE_TRUE_MODE_EFFECT[world]:
        raise AssertionError("pre-frozen observed/truth mode effect target failed")
    private_cov=binary_cov_from_original(world,"oracle_current_private_B1","oracle_current_private_B2")
    observed_cov=binary_cov_from_original(world,"observed_report_Y1","observed_report_Y2")
    miss=mismatch_rates(world)
    if world=="SOCIAL_DESIRABILITY_U":
        assert private_cov==ZERO and observed_cov==F(1,16)
    if world=="SHARED_ACQUIESCENCE_RESPONSE":
        assert private_cov==ZERO and observed_cov==F(1,4) and miss[1]==F(1,2)
    if world=="SHARED_TRUE_CONSTRUCT_ALIAS":
        assert private_cov==F(1,4) and observed_cov==F(1,4) and miss==(ZERO,ZERO)
    if world=="MODE_SUPPRESS_REPORT":
        assert observed_effect==F(-1,2) and true_effect==ZERO
    return dict(
        world=world,complete_original_source_atoms=64,
        observed_mode_R_ITT_on_report_Y1=str(observed_effect),
        oracle_mode_effect_on_current_private_B1=str(true_effect),
        oracle_true_private_B1_B2_covariance=str(private_cov),
        observed_report_Y1_Y2_covariance=str(observed_cov),
        oracle_report_mismatch_probabilities_Y1_Y2=[str(v) for v in miss],
        observed_five_variable_support_size=len(obs),
        complete_observed_mode_proxy_and_two_question_joint={
            ",".join(map(str,k)):str(v) for k,v in obs.items()
        }
    )

def generate():
    verify_aliases()
    result=dict(
        research_id="R236",original_catalogue_id="10-010",
        prescore_freeze_commit=FREEZE,
        scientific_scope="FINITE_ARTIFICIAL_E1_SURVEY_RESPONSE_BIAS",
        frozen_worlds=9,complete_original_six_source_atoms=576,
        complete_five_observed_variable_joint_alias_pairs=3,
        independent_mode_private_effect_verifier=True,
        independent_missing_proxy_observation_marginal_verifier=True,
        new_real_human_E2=0,new_real_historical_E3=0,
        R073="FROZEN",PESEN_v0_1="FROZEN",
        world_results=[world_result(w) for w in WORLDS]
    )
    src=HERE/"R236_ALL_576_ORIGINAL_SURVEY_RESPONSE_SOURCES.csv"
    fields=list(source_atom("TRUTHFUL_STABLE",0,0,0,0,0,0))
    with src.open("w",newline="",encoding="utf-8") as f:
        wr=csv.DictWriter(f,fieldnames=fields,lineterminator="\n")
        wr.writeheader()
        for world in WORLDS:
            for row in source_rows(world):
                wr.writerow({k:str(row[k]) for k in fields})
    res=HERE/"R236_EXACT_RESULTS.json"
    res.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    receipt=dict(
        research_id="R236",original_catalogue_id="10-010",
        frozen_worlds=9,complete_original_structural_source_atoms=576,
        three_complete_observed_joint_aliases_verified=True,
        independent_latent_true_mode_effect_parity=True,
        independent_pre_mode_partial_proxy_marginal_parity=True,
        source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),
        result_sha256=hashlib.sha256(res.read_bytes()).hexdigest(),
        new_real_human_E2=0,new_real_historical_E3=0
    )
    (HERE/"R236_FINAL_MACHINE_ACCEPTANCE.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_worlds(self):self.assertEqual(len(WORLDS),9)
    def test_full_sources(self):self.assertEqual(sum(len(source_rows(w)) for w in WORLDS),576)
    def test_three_complete_observation_aliases(self):self.assertTrue(verify_aliases())
    def test_true_mode_vs_report(self):
        self.assertEqual((true_private_mode_effect_from_sources("TRUE_MODE_CHANGE"),
                          true_private_mode_effect_from_sources("REPORT_MODE_CHANGE_ALIAS")),(F(1,2),ZERO))
        self.assertEqual((observable_mode_ITT("TRUE_MODE_CHANGE"),
                          observable_mode_ITT("REPORT_MODE_CHANGE_ALIAS")),(F(1,2),F(1,2)))
    def test_complier_only_alias(self):
        self.assertEqual(true_private_mode_effect_from_sources("TRUE_MODE_COMPLIER_ONLY"),F(1,4))
        self.assertEqual(true_private_mode_effect_from_sources("REPORT_MODE_COMPLIER_ONLY_ALIAS"),ZERO)
    def test_mode_suppression(self):
        self.assertEqual(observable_mode_ITT("MODE_SUPPRESS_REPORT"),F(-1,2))
    def test_social_desirability(self):
        self.assertEqual(binary_cov_from_original("SOCIAL_DESIRABILITY_U","observed_report_Y1","observed_report_Y2"),F(1,16))
    def test_shared_response_style(self):
        a=world_result("SHARED_ACQUIESCENCE_RESPONSE")
        self.assertEqual(a["oracle_true_private_B1_B2_covariance"],"0")
        self.assertEqual(a["observed_report_Y1_Y2_covariance"],"1/4")
    def test_true_shared_construct(self):
        self.assertEqual(world_result("SHARED_TRUE_CONSTRUCT_ALIAS")["oracle_true_private_B1_B2_covariance"],"1/4")
    def test_two_proxy_marginal(self):
        self.assertEqual(observed_joint_from_sources("TRUTHFUL_STABLE"),independent_observed_joint("TRUTHFUL_STABLE"))
    def test_not_true_private_proxy(self):
        self.assertEqual(source_atom("TRUE_MODE_CHANGE",0,0,0,1,1,1)["observed_prior_proxy_P"],0)
        self.assertEqual(source_atom("TRUE_MODE_CHANGE",0,0,0,1,1,1)["oracle_current_private_B1"],1)
    def test_unknown_model(self):
        with self.assertRaises(ValueError):source_rows("UNKNOWN")

def _case(world,kind):
    def test(self):
        rows=source_rows(world)
        if kind=="mass":
            self.assertEqual(sum((r["original_probability"] for r in rows),ZERO),ONE)
        elif kind=="unique":
            self.assertEqual(len({tuple(r["oracle_original_"+k] for k in SOURCES) for r in rows}),64)
        elif kind=="observable":
            self.assertEqual(observed_joint_from_sources(world),independent_observed_joint(world))
        elif kind=="intervention":
            self.assertEqual(true_private_mode_effect_from_sources(world),independent_true_mode_effect(world))
        elif kind=="mode":
            self.assertEqual(str(observable_mode_ITT(world)),EXPECTED_REPORTED_MODE_ITT[world])
        elif kind=="summary":
            self.assertEqual(world_result(world)["complete_original_source_atoms"],64)
        else:raise AssertionError("unknown test")
    return test
for _w in WORLDS:
    for _kind in ("mass","unique","observable","intervention","mode","summary"):
        setattr(Tests,f"test_{_w.lower()}_{_kind}",_case(_w,_kind))

if __name__=="__main__":
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true")
    g.add_argument("--emit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["r236"],verbosity=2)
    else:print(json.dumps(generate(),indent=2))
