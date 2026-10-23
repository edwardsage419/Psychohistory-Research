#!/usr/bin/env python3
"""R261 exact finite N=2 mean-field proxy versus actual interacting 10-bit agents.

Nine frozen artificial mechanisms, 1024 complete original exogenous types
per world (2 initial binary states + 2*2 agents*2 random bits), two updates.
Independent idiosyncratic transition probabilities differ from shared
conditional shock and artificial observation/report-alias models. All
probabilities and mean-field recursions are exact rational arithmetic.
No N->infinity theorem, propagation-of-chaos evidence or human data.
"""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
HERE=Path(__file__).resolve().parent
FREEZE="32ed797483cd47496cf83a9d24d251b9aac3f15b"
ZERO=F(0);ONE=F(1)
BITS=(0,1)
EXOG=tuple(itertools.product(BITS,repeat=10))
INITIAL_COUNTS=(0,1,2)
WORLDS=(
 "FINITE_NEUTRAL_IDIOSYNCRATIC",
 "FINITE_CONVEX_SQUARE",
 "FINITE_CONCAVE_CONFORMITY",
 "FINITE_CONTRARIAN",
 "INDEPENDENT_HALF",
 "UNANIMOUS_ONLY",
 "MAJORITY_TIE_UP",
 "COMMON_NOISE_NEUTRAL",
 "OBSERVED_COMMON_NOISE_TRUE_INDEPENDENT_SENSOR")
SHARED="COMMON_NOISE_NEUTRAL"
SENSOR="OBSERVED_COMMON_NOISE_TRUE_INDEPENDENT_SENSOR"
NEUTRAL="FINITE_NEUTRAL_IDIOSYNCRATIC"
SQUARE="FINITE_CONVEX_SQUARE"
CONCAVE="FINITE_CONCAVE_CONFORMITY"
def check(w):
    if w not in WORLDS:raise ValueError("not a frozen N2 mean field world")
def update_probability(w,m):
    """Continuous [0,1] deterministic mean-field extension, frozen ex ante."""
    check(w)
    if not ZERO<=m<=ONE:raise ValueError("mean outside probability interval")
    if w in (NEUTRAL,SHARED,SENSOR):return m
    if w==SQUARE:return m*m
    if w==CONCAVE:return 2*m-m*m
    if w=="FINITE_CONTRARIAN":return ONE-m
    if w=="INDEPENDENT_HALF":return F(1,2)
    if w=="UNANIMOUS_ONLY":return ONE if m==ONE else ZERO
    if w=="MAJORITY_TIE_UP":return ONE if m>=F(1,2) else ZERO
    raise AssertionError("missing frozen q")
def from_rbits(r0,r1):
    return 2*r0+r1
def _two_draws(q,raw_pair0,raw_pair1,shared):
    r0=from_rbits(*raw_pair0)
    r1=from_rbits(*raw_pair1)
    a=int(F(r0,4)<q)
    b=int(F(r0 if shared else r1,4)<q)
    return a,b
def _epoch_bits(bits,t):
    offset=2+4*t
    return (bits[offset],bits[offset+1]),(bits[offset+2],bits[offset+3])
def source_atom(w,bits):
    check(w)
    if len(bits)!=10 or any(b not in BITS for b in bits):
        raise ValueError("must contain all ten original fair bits")
    observed=(bits[0],bits[1])
    hidden=observed
    out=dict(world=w,oracle_original_initial_agent_bit_0=bits[0],
             oracle_original_initial_agent_bit_1=bits[1],
             original_complete_tenbit_source_probability=F(1,1024),
             observed_initial_count_K0=sum(observed),
             observed_initial_empirical_mean_M0=F(sum(observed),2))
    for t in range(2):
        r0,r1=_epoch_bits(bits,t)
        for i,pair in enumerate((r0,r1)):
            out[f"oracle_original_step{t}_agent{i}_R_a"]=pair[0]
            out[f"oracle_original_step{t}_agent{i}_R_b"]=pair[1]
        obs_q=update_probability(w,F(sum(observed),2))
        hidden_q=update_probability(NEUTRAL,F(sum(hidden),2)) if w==SENSOR else obs_q
        out[f"oracle_public_generator_q_t{t}"]=obs_q
        out[f"oracle_true_hidden_generator_q_t{t}"]=hidden_q
        next_obs=_two_draws(obs_q,r0,r1,w in (SHARED,SENSOR))
        next_hidden=_two_draws(hidden_q,r0,r1,False) if w==SENSOR else next_obs
        observed=next_obs
        hidden=next_hidden
        for i in range(2):
            out[f"observed_reported_agent{i}_state_t{t+1}"]=observed[i]
            out[f"oracle_true_hidden_agent{i}_state_t{t+1}"]=hidden[i]
        out[f"observed_reported_count_K{t+1}"]=sum(observed)
        out[f"observed_reported_empirical_mean_M{t+1}"]=F(sum(observed),2)
        out[f"oracle_true_hidden_count_H{t+1}"]=sum(hidden)
    return out
@lru_cache(None)
def sources(w):
    check(w)
    out=tuple(source_atom(w,b) for b in EXOG)
    assert len(out)==1024 and sum((r["original_complete_tenbit_source_probability"] for r in out),ZERO)==ONE
    return out
def conditional_source_count_law(w,k0,t):
    if k0 not in INITIAL_COUNTS or t not in (0,1,2):raise ValueError("out of frozen condition")
    rows=[r for r in sources(w) if r["observed_initial_count_K0"]==k0]
    assert len(rows)==(512 if k0==1 else 256)
    mass=ONE/len(rows)
    result=[]
    for k in INITIAL_COUNTS:
        col="observed_initial_count_K0" if t==0 else f"observed_reported_count_K{t}"
        result.append(sum((mass for r in rows if r[col]==k),ZERO))
    assert sum(result,ZERO)==ONE
    return tuple(result)
def independent_count_transition_matrix(w):
    """Second route: direct Bernoulli binomial/fully shared conditional count kernel."""
    check(w)
    rows=[]
    for k in INITIAL_COUNTS:
        q=update_probability(w,F(k,2))
        if w in (SHARED,SENSOR):
            row=(ONE-q,ZERO,q)
        else:
            row=((ONE-q)**2,2*q*(ONE-q),q*q)
        assert sum(row,ZERO)==ONE
        rows.append(row)
    return tuple(rows)
def theoretical_count_law(w,k0,t):
    if k0 not in INITIAL_COUNTS or t not in (0,1,2):raise ValueError("out of finite horizon")
    T=independent_count_transition_matrix(w)
    state=tuple(ONE if k==k0 else ZERO for k in INITIAL_COUNTS)
    for _ in range(t):
        state=tuple(sum((state[i]*T[i][j] for i in INITIAL_COUNTS),ZERO) for j in INITIAL_COUNTS)
    assert sum(state,ZERO)==ONE
    return state
def moments(law):
    mean=sum((p*F(k,2) for k,p in enumerate(law)),ZERO)
    var=sum((p*(F(k,2)-mean)**2 for k,p in enumerate(law)),ZERO)
    return mean,var,law[0]+law[2]
def mean_field_series(w,k0):
    m=F(k0,2)
    return (m,*(iter([update_probability(w,m)]))) if False else _mf_real(w,m)
def _mf_real(w,m):
    x1=update_probability(w,m)
    x2=update_probability(w,x1)
    return m,x1,x2
def frozen_claims():
    for w in WORLDS:
        for k in INITIAL_COUNTS:
            for t in (0,1,2):
                if theoretical_count_law(w,k,t)!=conditional_source_count_law(w,k,t):
                    raise AssertionError(f"{w} init{k} time{t}: bit integration and independent count transition disagree")
    def get(w,t,k=1):return moments(theoretical_count_law(w,k,t))
    assert mean_field_series(NEUTRAL,1)==(F(1,2),)*3
    assert get(NEUTRAL,1)[:2]==(F(1,2),F(1,8))
    assert get(NEUTRAL,2)[:2]==(F(1,2),F(3,16))
    assert get(SHARED,1)[:2]==(F(1,2),F(1,4))
    assert get(SHARED,2)[:2]==(F(1,2),F(1,4))
    assert mean_field_series(SQUARE,1)==(F(1,2),F(1,4),F(1,16))
    assert get(SQUARE,1)[0]==F(1,4)
    assert get(SQUARE,2)[0]==F(5,32)
    assert get(SQUARE,2)[0]-mean_field_series(SQUARE,1)[2]==F(3,32)
    assert mean_field_series(CONCAVE,1)==(F(1,2),F(3,4),F(15,16))
    assert get(CONCAVE,1)[0]==F(3,4)
    assert get(CONCAVE,2)[0]==F(27,32)
    assert get(CONCAVE,2)[0]-mean_field_series(CONCAVE,1)[2]==-F(3,32)
    for bits in EXOG:
        a=source_atom(SHARED,bits)
        b=source_atom(SENSOR,bits)
        for t in (1,2):
            assert a[f"observed_reported_count_K{t}"]==b[f"observed_reported_count_K{t}"]
            assert all(a[f"observed_reported_agent{i}_state_t{t}"]==b[f"observed_reported_agent{i}_state_t{t}"] for i in (0,1))
    # Two conditionally independent agents have Bernoulli q=1/2 covariance zero,
    # both shared draws have covariance q(1-q)=1/4 for K0=1.
    assert get(NEUTRAL,1)[1]==F(1,8) and get(SHARED,1)[1]==F(1,4)
    return True
def world_result(w):
    out=[]
    for k in INITIAL_COUNTS:
        mf=mean_field_series(w,k)
        rec=dict(initial_visible_agent_count_K0=k,
                 deterministic_mean_field_m0_m1_m2=[str(x) for x in mf],
                 exact_conditional_count_PMF_each_time=[],
                 exact_finite_agent_empirical_mean_each_time=[],
                 exact_finite_agent_empirical_variance_each_time=[],
                 exact_finite_agent_full_consensus_probability_each_time=[],
                 exact_finite_minus_deterministic_mean_field_mean_each_time=[])
        for t in (0,1,2):
            law=theoretical_count_law(w,k,t)
            if law!=conditional_source_count_law(w,k,t):raise AssertionError("source vs analytic chain mismatch")
            mean,var,cons=moments(law)
            rec["exact_conditional_count_PMF_each_time"].append([str(x) for x in law])
            rec["exact_finite_agent_empirical_mean_each_time"].append(str(mean))
            rec["exact_finite_agent_empirical_variance_each_time"].append(str(var))
            rec["exact_finite_agent_full_consensus_probability_each_time"].append(str(cons))
            rec["exact_finite_minus_deterministic_mean_field_mean_each_time"].append(str(mean-mf[t]))
        out.append(rec)
    return dict(world=w,all_original_tenbit_source_atoms=1024,
        frozen_3_by_3_finite_count_transition=[
            [str(x) for x in row] for row in independent_count_transition_matrix(w)],
        conditional_same_epoch_noise_is_shared_for_public=(w in (SHARED,SENSOR)),
        hidden_agents_update_independently_if_sensor=(w==SENSOR),
        exact_n2_count_chain_vs_complete_bit_source_verified=True,
        all_three_initial_count_conditions=out)
def emit():
    frozen_claims()
    result=dict(research_id="R261",original_catalogue_id="11-021",
       prescore_freeze_commit=FREEZE,
       scientific_scope="FINITE_ARTIFICIAL_E1_TWO_AGENT_TWO_STEP_MEAN_FIELD_VS_FINITE_COUNT_MARKOV",
       frozen_worlds=9,all_original_tenbit_complete_source_atoms=9216,
       no_N_tends_infinity_theorem_or_propagation_of_chaos_proven=True,
       convex_square_k0_one_exact_finite_minus_MF_at_t2="3/32",
       concave_k0_one_exact_finite_minus_MF_at_t2="-3/32",
       independent_neutral_k0_one_variance_t1="1/8",
       independent_neutral_k0_one_variance_t2="3/16",
       common_noise_neutral_k0_one_variance_t1_t2="1/4",
       sensor_sourcewise_observed_alias_with_common_noise=True,
       new_real_human_E2=0,new_real_historical_E3=0,
       R073="FROZEN",PESEN_v0_1="FROZEN",
       world_results=[world_result(w) for w in WORLDS])
    out=HERE/"R261_ALL_9216_ORIGINAL_TENBIT_MEAN_FIELD_AGENT_SOURCES.csv"
    keys=list(sources(WORLDS[0])[0])
    with out.open("w",encoding="utf-8",newline="") as f:
        wr=csv.DictWriter(f,fieldnames=keys,lineterminator="\n");wr.writeheader()
        for w in WORLDS:
            for row in sources(w):wr.writerow({k:str(row[k]) for k in keys})
    jp=HERE/"R261_EXACT_RESULTS.json"
    jp.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    receipt=dict(research_id="R261",original_catalogue_id="11-021",frozen_worlds=9,
       all_original_tenbit_agent_source_atoms=9216,
       direct_finite_bit_source_vs_independent_count_markov_matrix=True,
       Jensen_n2_nonlinear_conditional_mean_discrepancy_verified=True,
       shared_noise_conditional_variance_inflation_verified=True,
       sensor_fake_observation_alias_vs_true_independent_agents=True,
       source_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),
       results_sha256=hashlib.sha256(jp.read_bytes()).hexdigest(),
       new_real_human_E2=0,new_real_historical_E3=0)
    (HERE/"R261_FINAL_MACHINE_ACCEPTANCE.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt
class Tests(unittest.TestCase):
    def test_world_count(self):self.assertEqual(len(WORLDS),9)
    def test_9216(self):self.assertEqual(sum(len(sources(w)) for w in WORLDS),9216)
    def test_claims(self):self.assertTrue(frozen_claims())
    def test_neutral_noise_variance(self):self.assertEqual(moments(theoretical_count_law(NEUTRAL,1,2))[1],F(3,16))
    def test_common_noise_variance(self):self.assertEqual(moments(theoretical_count_law(SHARED,1,2))[1],F(1,4))
    def test_square_Jensen(self):self.assertEqual(moments(theoretical_count_law(SQUARE,1,2))[0],F(5,32))
    def test_concave_Jensen(self):self.assertEqual(moments(theoretical_count_law(CONCAVE,1,2))[0],F(27,32))
    def test_count_law_normalized(self):
        self.assertEqual(sum(theoretical_count_law(SQUARE,1,2),ZERO),ONE)
    def test_observed_sourcewise_alias(self):
        for bits in EXOG:
            a=source_atom(SHARED,bits);b=source_atom(SENSOR,bits)
            self.assertEqual(a["observed_reported_count_K2"],b["observed_reported_count_K2"])
    def test_bad_world(self):
        with self.assertRaises(ValueError):sources("INVALID")
def _case(w,k):
    def t(self):
        src=sources(w)
        if k=="mass":self.assertEqual(sum((r["original_complete_tenbit_source_probability"] for r in src),ZERO),ONE)
        elif k=="unique":
            keys=["oracle_original_initial_agent_bit_0","oracle_original_initial_agent_bit_1"]+[
                f"oracle_original_step{t}_agent{i}_R_{b}" for t in (0,1) for i in (0,1) for b in ("a","b")]
            self.assertEqual(len({tuple(r[key] for key in keys) for r in src}),1024)
        elif k=="positive":self.assertTrue(all(r["original_complete_tenbit_source_probability"]==F(1,1024) for r in src))
        elif k=="law":
            for init in INITIAL_COUNTS:
                for time in (0,1,2):
                    self.assertEqual(conditional_source_count_law(w,init,time),theoretical_count_law(w,init,time))
        elif k=="states":
            self.assertTrue(all(all(r[f"observed_reported_count_K{time}"] in (0,1,2) for time in (1,2)) for r in src))
        elif k=="q":
            for r in src:
                for time in (0,1):self.assertTrue(0<=r[f"oracle_public_generator_q_t{time}"]<=1)
        elif k=="mf":
            for init in INITIAL_COUNTS:
                self.assertEqual(len(mean_field_series(w,init)),3)
        elif k=="report":self.assertEqual(world_result(w)["all_original_tenbit_source_atoms"],1024)
        else:raise AssertionError("bad frozen test")
    return t
for w in WORLDS:
    for k in ("mass","unique","positive","law","states","q","mf","report"):
        setattr(Tests,"test_"+w.lower()+"_"+k,_case(w,k))
if __name__=="__main__":
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true");g.add_argument("--emit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["r261"],verbosity=2)
    else:print(json.dumps(emit(),indent=2))
