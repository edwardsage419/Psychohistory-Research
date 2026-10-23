#!/usr/bin/env python3
"""R253 finite four-person sequential informational cascade with exact 9-bit sources.

Bikhchandani-Hirshleifer-Welch-type binary action stylization (not a
replication of every original model assumption): state fair, independent
conditionally private signals at q=3/4, Bayesian action history, ties
resolved by one's own signal. Countermodels separate observation,
reporting, perfect signals, imitating and common signal causal structure.
"""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path

HERE=Path(__file__).resolve().parent
FREEZE="ffb215ac35978839a3ae6db162d6447f6752ad15"
ZERO=F(0);ONE=F(1)
BITS=(0,1)
WORLDS=(
 "BAYESIAN_CASCADE_Q34","PRIVATE_ONLY_Q34","FIRST_ACTION_IMITATION_Q34",
 "BAYESIAN_CASCADE_FAIR_Q12","HARD_CODED_CASCADE_ALIAS_Q34",
 "INVERTED_SIGNALS_Q14_BAYES","PERFECT_PRIVATE_Q1",
 "STATIC_TRUE_PRIVATE_CASCADE_REPORT_ALIAS_Q34",
 "COMMON_SIGNAL_NO_SOCIAL_Q34")
EXOG=tuple(itertools.product(BITS,repeat=9))
SIGNALS=tuple(itertools.product(BITS,repeat=4))
SENSOR="STATIC_TRUE_PRIVATE_CASCADE_REPORT_ALIAS_Q34"
BAYESIAN="BAYESIAN_CASCADE_Q34"
HEURISTIC="HARD_CODED_CASCADE_ALIAS_Q34"
IMITATION="FIRST_ACTION_IMITATION_Q34"
COMMON="COMMON_SIGNAL_NO_SOCIAL_Q34"

def require(w):
    if w not in WORLDS:raise ValueError("not frozen cascade counterworld")
def quality(w):
    require(w)
    if w=="BAYESIAN_CASCADE_FAIR_Q12":return F(1,2)
    if w=="INVERTED_SIGNALS_Q14_BAYES":return F(1,4)
    if w=="PERFECT_PRIVATE_Q1":return ONE
    return F(3,4)

def draw_private(w,original):
    if len(original)!=9 or any(b not in BITS for b in original):
        raise ValueError("not nine independent original bits")
    theta=original[0]
    q=quality(w)
    private=[]
    for i in range(4):
        r=2*original[1+2*i]+original[2+2*i]
        private.append(theta if F(r)<4*q else 1-theta)
    return theta,tuple(private)

def public_actions(w,private):
    """Explicit finite behavioral generator; no statistical estimation."""
    require(w)
    s=private
    if w in ("PRIVATE_ONLY_Q34","BAYESIAN_CASCADE_FAIR_Q12"):
        return tuple(s)
    if w in (IMITATION,COMMON):return (s[0],)*4
    if w=="INVERTED_SIGNALS_Q14_BAYES":s=tuple(1-x for x in s)
    if s[0]==s[1]:return (s[0],s[1],s[0],s[0])
    return (s[0],s[1],s[2],s[3])

def source_atom(w,original):
    theta,s=draw_private(w,original)
    obs=public_actions(w,s)
    hidden=tuple(s) if w==SENSOR else obs
    do2=(1-s[0]) if w==IMITATION else (s[0] if w==COMMON else None)
    out={"world":w,"oracle_true_state_theta":theta}
    for i in range(4):
        out["oracle_original_signal_R"+str(i+1)+"1"]=original[2*i+1]
        out["oracle_original_signal_R"+str(i+1)+"2"]=original[2*i+2]
        out["oracle_private_signal_S"+str(i+1)]=s[i]
        out["observed_public_action_Y"+str(i+1)]=obs[i]
        out["oracle_true_hidden_action_H"+str(i+1)]=hidden[i]
    out["observed_first_two_agree"]=int(obs[0]==obs[1])
    out["oracle_observed_third_disagrees_private_S3"]=int(obs[2]!=s[2])
    out["oracle_do_report_Y1_flip_next_report_Y2"]=do2
    out["original_full_ninebit_source_probability"]=F(1,512)
    return out

@lru_cache(None)
def sources(w):
    require(w)
    rows=tuple(source_atom(w,original) for original in EXOG)
    if len(rows)!=512 or sum((r["original_full_ninebit_source_probability"] for r in rows),ZERO)!=ONE:
        raise AssertionError("incomplete ninebit original cascade source space")
    return rows

@lru_cache(None)
def observed_path_joint(w):
    d=defaultdict(F)
    for r in sources(w):
        path=tuple(r["observed_public_action_Y"+str(i)] for i in (1,2,3,4))
        d[path]+=r["original_full_ninebit_source_probability"]
    return dict(sorted(d.items()))

def theoretical_actions(w,s):
    """Closed expected action strategies from signals; no source simulator."""
    if w in ("PRIVATE_ONLY_Q34","BAYESIAN_CASCADE_FAIR_Q12"):
        return s
    if w in (IMITATION,COMMON):
        return (s[0],s[0],s[0],s[0])
    if w=="INVERTED_SIGNALS_Q14_BAYES":
        s=tuple(1-x for x in s)
    a,b,c,d=s
    return (a,b,a if a==b else c,a if a==b else d)

def theoretical_source_joint(w):
    """Independent theta x 16 signal outcomes, product likelihood."""
    require(w)
    q=quality(w)
    obs=defaultdict(F)
    correct=[ZERO]*4
    agreement=ZERO
    third_different=ZERO
    first_agree_correct=ZERO
    for theta in BITS:
        for s in SIGNALS:
            mass=F(1,2)
            for x in s:mass*=q if x==theta else ONE-q
            if mass==ZERO:continue
            a=theoretical_actions(w,s)
            obs[a]+=mass
            for i in range(4):
                if a[i]==theta:correct[i]+=mass
            if a[0]==a[1]:
                agreement+=mass
                if a[0]==theta:first_agree_correct+=mass
            if a[2]!=s[2]:third_different+=mass
    assert sum(obs.values(),ZERO)==ONE
    return dict(sorted(obs.items())),tuple(correct),agreement,third_different,first_agree_correct

def weighted_source_stats(w):
    data=sources(w)
    correct=tuple(sum((r["original_full_ninebit_source_probability"]*
                (r["observed_public_action_Y"+str(i)]==r["oracle_true_state_theta"])
                for r in data),ZERO) for i in (1,2,3,4))
    agreement=sum((r["original_full_ninebit_source_probability"]*r["observed_first_two_agree"] for r in data),ZERO)
    mismatch=sum((r["original_full_ninebit_source_probability"]*
                  r["oracle_observed_third_disagrees_private_S3"] for r in data),ZERO)
    correct_agreement=sum((r["original_full_ninebit_source_probability"]*
                  int(r["observed_first_two_agree"] and
                      r["observed_public_action_Y1"]==r["oracle_true_state_theta"])
                  for r in data),ZERO)
    return correct,agreement,mismatch,correct_agreement

def frozen_claims():
    w=BAYESIAN
    independent=theoretical_source_joint(w)
    actual=weighted_source_stats(w)
    assert independent[0]==observed_path_joint(w)
    assert actual==independent[1:]
    correct,agree,different,right=actual
    assert correct==(F(3,4),F(3,4),F(27,32),F(27,32))
    assert agree==F(5,8)
    assert right==F(9,16)
    assert right/agree==F(9,10)
    assert different==F(3,16)
    for aliases in ((BAYESIAN,HEURISTIC,SENSOR),(IMITATION,COMMON)):
        first=observed_path_joint(aliases[0])
        for alt in aliases[1:]:
            assert observed_path_joint(alt)==first
            for bit in EXOG:
                a=source_atom(aliases[0],bit)
                b=source_atom(alt,bit)
                assert all(a["observed_public_action_Y"+str(i)]==
                           b["observed_public_action_Y"+str(i)] for i in (1,2,3,4))
    for bit in EXOG:
        imit=source_atom(IMITATION,bit);common=source_atom(COMMON,bit)
        assert imit["oracle_do_report_Y1_flip_next_report_Y2"]!=common["oracle_do_report_Y1_flip_next_report_Y2"]
        sensor=source_atom(SENSOR,bit);base=source_atom(BAYESIAN,bit)
        assert all(sensor["oracle_true_hidden_action_H"+str(i)]==
                   sensor["oracle_private_signal_S"+str(i)] for i in (1,2,3,4))
        assert all(sensor["observed_public_action_Y"+str(i)]==
                   base["observed_public_action_Y"+str(i)] for i in (1,2,3,4))
    assert weighted_source_stats("PRIVATE_ONLY_Q34")[0]==(F(3,4),)*4
    assert weighted_source_stats(IMITATION)[0]==(F(3,4),)*4
    assert weighted_source_stats("BAYESIAN_CASCADE_FAIR_Q12")[0]==(F(1,2),)*4
    assert weighted_source_stats("PERFECT_PRIVATE_Q1")[0]==(ONE,)*4
    assert weighted_source_stats("INVERTED_SIGNALS_Q14_BAYES")[0][2:]==(F(27,32),F(27,32))
    return True

def world_result(w):
    full=observed_path_joint(w)
    expected,correct,agreement,diff,right=theoretical_source_joint(w)
    actual=weighted_source_stats(w)
    if full!=expected or actual!=(correct,agreement,diff,right):
        raise AssertionError("source action law differs independent signal likelihood products")
    return dict(world=w,full_original_ninebit_source_atoms=512,
        frozen_private_signal_accuracy=str(quality(w)),
        observed_four_person_path_joint={"".join(map(str,k)):str(p) for k,p in full.items()},
        observed_path_support_count=len(full),
        observed_action_accuracy_by_agent=[str(v) for v in correct],
        observed_first_two_agreement_probability=str(agreement),
        oracle_third_action_disagrees_own_private_signal_probability=str(diff),
        observed_agreement_correct_joint_probability=str(right),
        observed_agreement_action_correct_given_first_two_agree=(
            str(right/agreement) if agreement else None),
        independent_theta_private_signal_product_law_verified=True,
        observed_vs_true_hidden_actions_different_only_in_sensor_world=(w==SENSOR),
        public_action_1_intervention_comparison_only_for_imitation_common=(w in (IMITATION,COMMON)))

def emit():
    frozen_claims()
    data=dict(research_id="R253",original_catalogue_id="11-013",
        prescore_freeze_commit=FREEZE,
        scientific_scope="FINITE_ARTIFICIAL_E1_FOUR_AGENT_BINARY_INFORMATION_CASCADE_AND_OBSERVATIONAL_CAUSAL_ALIASES",
        frozen_worlds=9,full_original_ninebit_source_atoms=4608,
        frozen_bayesian_cascade_event_probability="5/8",
        frozen_bayesian_agreement_conditional_accuracy="9/10",
        frozen_agent3_and4_unconditional_accuracy="27/32",
        frozen_agent3_own_private_signal_conflict_rate="3/16",
        cognitive_strategy_vs_hardcoded_observation_sourcewise_alias=[
          BAYESIAN,HEURISTIC,SENSOR],
        imitation_vs_shared_signal_observation_sourcewise_alias=[IMITATION,COMMON],
        no_real_human_bayesian_cognition_identified=True,
        new_real_human_E2=0,new_real_historical_E3=0,
        R073="FROZEN",PESEN_v0_1="FROZEN",
        world_results=[world_result(w) for w in WORLDS])
    out=HERE/"R253_ALL_4608_ORIGINAL_FOUR_AGENT_SIGNAL_SOURCES.csv"
    fields=list(sources(WORLDS[0])[0])
    with out.open("w",encoding="utf-8",newline="") as f:
        wr=csv.DictWriter(f,fieldnames=fields,lineterminator="\n")
        wr.writeheader()
        for w in WORLDS:
            for r in sources(w):wr.writerow({k:str(r[k]) for k in fields})
    result=HERE/"R253_EXACT_RESULTS.json"
    result.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    receipt=dict(research_id="R253",original_catalogue_id="11-013",
        frozen_worlds=9,full_original_ninebit_atoms=4608,
        source_vs_independent_theta_signal_likelihood_exact=True,
        four_agent_bayesian_cascade_statistics_precisely_certified=True,
        observational_heuristic_and_static_report_aliases_verified=True,
        imitation_vs_common_signal_different_intervention_oracles=True,
        source_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),
        results_sha256=hashlib.sha256(result.read_bytes()).hexdigest(),
        new_real_human_E2=0,new_real_historical_E3=0)
    (HERE/"R253_FINAL_MACHINE_ACCEPTANCE.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_nine_worlds(self):self.assertEqual(len(WORLDS),9)
    def test_original_4608(self):self.assertEqual(sum(len(sources(w)) for w in WORLDS),4608)
    def test_all_frozen_posteriors_and_aliases(self):self.assertTrue(frozen_claims())
    def test_cascade_probability(self):self.assertEqual(weighted_source_stats(BAYESIAN)[1],F(5,8))
    def test_correct_when_agree(self):
        stats=weighted_source_stats(BAYESIAN)
        self.assertEqual(stats[3]/stats[1],F(9,10))
    def test_third_accuracy(self):self.assertEqual(weighted_source_stats(BAYESIAN)[0][2],F(27,32))
    def test_third_different_private(self):self.assertEqual(weighted_source_stats(BAYESIAN)[2],F(3,16))
    def test_no_social(self):self.assertEqual(weighted_source_stats("PRIVATE_ONLY_Q34")[0][3],F(3,4))
    def test_perfect_signal(self):self.assertEqual(weighted_source_stats("PERFECT_PRIVATE_Q1")[0],(ONE,)*4)
    def test_fair_signal(self):self.assertEqual(weighted_source_stats("BAYESIAN_CASCADE_FAIR_Q12")[0],(F(1,2),)*4)
    def test_imitation_shared_sourcewise(self):self.assertEqual(observed_path_joint(IMITATION),observed_path_joint(COMMON))
    def test_hidden_report(self):self.assertEqual(observed_path_joint(BAYESIAN),observed_path_joint(SENSOR))
    def test_unknown(self):
        with self.assertRaises(ValueError):sources("UNFROZEN_CASCADE")

def _case(w,kind):
    def t(self):
        src=sources(w)
        if kind=="mass":self.assertEqual(sum((r["original_full_ninebit_source_probability"] for r in src),ZERO),ONE)
        elif kind=="unique":
            keys=["oracle_true_state_theta"]+["oracle_original_signal_R"+str(i)+s for i in (1,2,3,4) for s in ("1","2")]
            self.assertEqual(len({tuple(r[k] for k in keys) for r in src}),512)
        elif kind=="positive":self.assertTrue(all(r["original_full_ninebit_source_probability"]==F(1,512) for r in src))
        elif kind=="joint":self.assertEqual(observed_path_joint(w),theoretical_source_joint(w)[0])
        elif kind=="normalization":self.assertEqual(sum(observed_path_joint(w).values(),ZERO),ONE)
        elif kind=="expected_accuracy":self.assertEqual(weighted_source_stats(w)[0],theoretical_source_joint(w)[1])
        elif kind=="expected_agreement":self.assertEqual(weighted_source_stats(w)[1],theoretical_source_joint(w)[2])
        elif kind=="result":self.assertEqual(world_result(w)["full_original_ninebit_source_atoms"],512)
        else:raise AssertionError("unfrozen test")
    return t
for w in WORLDS:
    for kind in ("mass","unique","positive","joint","normalization","expected_accuracy","expected_agreement","result"):
        setattr(Tests,"test_"+w.lower()+"_"+kind,_case(w,kind))
if __name__=="__main__":
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true");g.add_argument("--emit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["r253"],verbosity=2)
    else:print(json.dumps(emit(),indent=2))
