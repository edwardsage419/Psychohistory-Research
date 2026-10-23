#!/usr/bin/env python3
"""R244 exact 3-step 2-state Markov processes and hidden-mixture non-Markov laws.

128 complete 7-exogenous-bit atoms per world. The observation mechanism
is separated from hidden truth; full path probabilities are independently
computed from transition-product formulas, never from empirical text.
"""
from __future__ import annotations
import csv,hashlib,json,itertools,unittest,argparse
from fractions import Fraction as F
from collections import defaultdict
from pathlib import Path

HERE=Path(__file__).resolve().parent
ZERO=F(0);ONE=F(1)
FREEZE="75ce71f7ca6281f5d14fbfe46a805cbdb3a8e6a3"
BITS=(0,1)
ALL_BITS=tuple(itertools.product(BITS,repeat=7))
ALL_PATHS=tuple((0,)+x for x in itertools.product(BITS,repeat=3))
WORLDS=(
    "IID_FAIR","PERSISTENT_3OF4","ANTIPERSISTENT_1OF4",
    "ABSORB_ONE","TIME_ALTERNATING_RATE","LATENT_RATE_MIXTURE",
    "STATIC_HIDDEN_SENSOR_ALIAS","COMPLEMENT_HIDDEN_COORDINATE_ALIAS",
    "FIXED_SWITCH_POLICY")
HOMOGENEOUS=(
    "IID_FAIR","PERSISTENT_3OF4","ANTIPERSISTENT_1OF4",
    "ABSORB_ONE","STATIC_HIDDEN_SENSOR_ALIAS","COMPLEMENT_HIDDEN_COORDINATE_ALIAS")
PERSISTENT_OBS_ALIASES=("PERSISTENT_3OF4","STATIC_HIDDEN_SENSOR_ALIAS","COMPLEMENT_HIDDEN_COORDINATE_ALIAS")

def validate(world):
    if world not in WORLDS:raise ValueError("unfrozen Markov world")

def stay_prob(world,step,state,u):
    validate(world)
    if step not in (1,2,3) or state not in BITS or u not in BITS:
        raise ValueError("invalid transition support")
    if world=="IID_FAIR":return F(1,2)
    if world in PERSISTENT_OBS_ALIASES:return F(3,4)
    if world=="ANTIPERSISTENT_1OF4":return F(1,4)
    if world=="ABSORB_ONE":return ONE if state==1 else F(1,2)
    if world=="TIME_ALTERNATING_RATE":return F(3,4) if step in (1,3) else F(1,4)
    if world=="LATENT_RATE_MIXTURE":return F(3,4) if u==0 else F(1,4)
    if world=="FIXED_SWITCH_POLICY":return ONE if u==0 else ZERO
    raise AssertionError("unspecified stochastic mechanism")

def simulate(world,bits):
    validate(world)
    if len(bits)!=7 or any(b not in BITS for b in bits):
        raise ValueError("not full seven-bit source")
    u=bits[0]
    obs=[0]
    for step in (1,2,3):
        prev=obs[-1]
        r=2*bits[2*step-1]+bits[2*step]
        s=stay_prob(world,step,prev,u)
        if s*4 not in (0,1,2,3,4):
            raise AssertionError("kernel impossible for two-bit exact quantization")
        obs.append(prev if r<4*s else 1-prev)
    if world=="STATIC_HIDDEN_SENSOR_ALIAS":hidden=(0,0,0,0)
    elif world=="COMPLEMENT_HIDDEN_COORDINATE_ALIAS":hidden=tuple(1-x for x in obs)
    else:hidden=tuple(obs)
    return tuple(obs),hidden

def source_atom(world,bits):
    obs,h=simulate(world,bits)
    r={"world":world,"oracle_source_U":bits[0]}
    for step in (1,2,3):
        r["oracle_original_R"+str(step)+"1"]=bits[2*step-1]
        r["oracle_original_R"+str(step)+"2"]=bits[2*step]
    for i in range(4):
        r["observed_y"+str(i)]=obs[i]
        r["oracle_hidden_h"+str(i)]=h[i]
    r["original_source_probability"]=F(1,128)
    return r

def sources(world):
    validate(world)
    rows=tuple(source_atom(world,b) for b in ALL_BITS)
    if len(rows)!=128 or sum((r["original_source_probability"] for r in rows),ZERO)!=ONE:
        raise AssertionError("complete structural Markov source mass broken")
    return rows

def observed_path_joint(world):
    d=defaultdict(F)
    for r in sources(world):
        obs=tuple(r["observed_y"+str(i)] for i in range(4))
        d[obs]+=r["original_source_probability"]
    return dict(sorted(d.items()))

def kernel_prob(world,step,current,next_state,u):
    s=stay_prob(world,step,current,u)
    return s if current==next_state else ONE-s

def independent_path_probability(world,path):
    validate(world)
    if path not in ALL_PATHS:raise ValueError("not an accessible four-time binary path")
    if world in ("LATENT_RATE_MIXTURE","FIXED_SWITCH_POLICY"):
        return sum((F(1,2)*_kernel_product(world,path,u) for u in BITS),ZERO)
    return _kernel_product(world,path,0)

def _kernel_product(world,path,u):
    mass=ONE
    for i in (1,2,3):
        mass*=kernel_prob(world,i,path[i-1],path[i],u)
    return mass

def independent_path_joint(world):
    return {p:independent_path_probability(world,p) for p in ALL_PATHS
            if independent_path_probability(world,p)>0}

def conditional(world,criteria,event_index=3,event_value=1):
    """From actual observed full path PMF; no latent U or transition parameters."""
    j=observed_path_joint(world)
    den=sum((p for seq,p in j.items() if all(seq[k]==v for k,v in criteria.items())),ZERO)
    if den==ZERO:return None
    num=sum((p for seq,p in j.items()
             if all(seq[k]==v for k,v in criteria.items()) and seq[event_index]==event_value),ZERO)
    return num/den

def markov_defect(world):
    """Finite time 3 Markov conditional-independence defect on positive support."""
    largest=ZERO
    for y1 in BITS:
        for y2 in BITS:
            with_history=conditional(world,{1:y1,2:y2})
            without_history=conditional(world,{2:y2})
            if with_history is None:continue
            if without_history is None:raise AssertionError("incoherent positive support")
            largest=max(largest,abs(with_history-without_history))
    return largest

def homogenous_matrix(world):
    if world not in HOMOGENEOUS:raise ValueError("not assumed time-homogeneous Markov observable")
    return tuple(tuple(kernel_prob(world,1,a,b,0) for b in BITS) for a in BITS)

def matrix_mul(a,b):
    return tuple(tuple(sum((a[i][k]*b[k][j] for k in BITS),ZERO) for j in BITS)
                 for i in BITS)
def markov_ck(world):
    """Independent transition-product Chapman–Kolmogorov source check."""
    p=homogenous_matrix(world)
    p2=matrix_mul(p,p)
    p3=matrix_mul(p2,p)
    j=observed_path_joint(world)
    for n,kernel in ((1,p),(2,p2),(3,p3)):
        for state in BITS:
            observed=sum((v for path,v in j.items() if path[n]==state),ZERO)
            if observed!=kernel[0][state]:
                raise AssertionError("finite observed marginals fail CK power at step "+str(n))
    return True

def observational_alias_certificates():
    original=observed_path_joint("PERSISTENT_3OF4")
    for w in PERSISTENT_OBS_ALIASES[1:]:
        if observed_path_joint(w)!=original:raise AssertionError("persistent observation alias broken")
        for bits in ALL_BITS:
            if simulate(w,bits)[0]!=simulate("PERSISTENT_3OF4",bits)[0]:
                raise AssertionError("same source complete observed pathway differs")
    mix="LATENT_RATE_MIXTURE"
    assert conditional(mix,{1:0,2:0},event_value=0)==F(7,10)
    assert conditional(mix,{1:1,2:0},event_value=0)==F(3,10)
    assert conditional(mix,{2:0},event_value=0)==F(1,2)
    assert markov_defect(mix)==F(1,5)
    fixed="FIXED_SWITCH_POLICY"
    assert conditional(fixed,{1:0,2:0},event_value=0)==ONE
    assert conditional(fixed,{1:1,2:0},event_value=0)==ZERO
    assert markov_defect(fixed)==F(1,2)
    assert conditional(fixed,{0:0},event_index=1,event_value=0)==F(1,2)
    assert conditional("IID_FAIR",{0:0},event_index=1,event_value=0)==F(1,2)
    assert conditional("TIME_ALTERNATING_RATE",{0:0},event_index=1,event_value=0)==F(3,4)
    assert conditional("TIME_ALTERNATING_RATE",{1:0},event_index=2,event_value=0)==F(1,4)
    for w in WORLDS:
        if (markov_defect(w)==ZERO)!=(w not in (mix,fixed)):
            raise AssertionError("frozen finite Markov/non-Markov classifications violated")
    return True

def world_result(world):
    j=observed_path_joint(world)
    expected=independent_path_joint(world)
    if j!=expected:raise AssertionError("full 4-point joint and independent transition product disagree")
    if world in HOMOGENEOUS:markov_ck(world)
    marginals=[sum((prob for p,prob in j.items() if p[n]==1),ZERO) for n in range(4)]
    return dict(
        world=world,complete_original_seven_bit_exogenous_atoms=128,
        observed_path_support_size=len(j),
        observed_probability_state1_by_step=[str(v) for v in marginals],
        observed_time3_conditional_markov_defect=str(markov_defect(world)),
        observed_p_Y3zero_given_Y2zero_Y1zero=(
            str(conditional(world,{1:0,2:0},event_value=0))
            if conditional(world,{1:0,2:0},event_value=0) is not None else None),
        observed_p_Y3zero_given_Y2zero_Y1one=(
            str(conditional(world,{1:1,2:0},event_value=0))
            if conditional(world,{1:1,2:0},event_value=0) is not None else None),
        observed_p_Y3zero_given_Y2zero=(
            str(conditional(world,{2:0},event_value=0))
            if conditional(world,{2:0},event_value=0) is not None else None),
        complete_observed_four_time_state_joint={
            "".join(map(str,p)):str(v) for p,v in j.items()},
        independent_transition_product_full_path_parity=True,
        homogenous_observed_CK_matrix_powers_verified=(world in HOMOGENEOUS),
        oracle_real_hidden_h4_by_source=[str(r["oracle_hidden_h3"]) for r in sources(world)]
    )

def generate():
    observational_alias_certificates()
    result=dict(research_id="R244",original_catalogue_id="11-004",
        prescore_freeze_commit=FREEZE,
        scientific_scope="FINITE_ARTIFICIAL_E1_BINARY_MARKOV_VS_HIDDEN_MIXTURE",
        frozen_worlds=9,complete_seven_bit_original_path_atoms=1152,
        finite_time_conditional_Markov_property_tested=True,
        time_inhomogeneous_markov_distinguished_from_hidden_mixture=True,
        full_observed_sourcewise_aliases=list(PERSISTENT_OBS_ALIASES),
        new_real_human_E2=0,new_real_historical_E3=0,
        R073="FROZEN",PESEN_v0_1="FROZEN",
        world_results=[world_result(w) for w in WORLDS])
    out=HERE/"R244_ALL_1152_ORIGINAL_BINARY_MARKOV_SOURCE_PATHS.csv"
    fields=list(sources("IID_FAIR")[0])
    with out.open("w",encoding="utf-8",newline="") as f:
        wr=csv.DictWriter(f,fieldnames=fields,lineterminator="\n");wr.writeheader()
        for w in WORLDS:
            for row in sources(w):wr.writerow({k:str(row[k]) for k in fields})
    res=HERE/"R244_EXACT_RESULTS.json"
    res.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    receipt=dict(research_id="R244",original_catalogue_id="11-004",
        frozen_worlds=9,original_complete_seven_bit_path_atoms=1152,
        all_full_path_probability_equal_independent_transition_products=True,
        homogeneous_CK_where_applicable=True,
        hidden_mixture_conditional_markov_counterexample=True,
        source_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),
        results_sha256=hashlib.sha256(res.read_bytes()).hexdigest(),
        new_real_human_E2=0,new_real_historical_E3=0)
    (HERE/"R244_FINAL_MACHINE_ACCEPTANCE.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_all_worlds(self):self.assertEqual(len(WORLDS),9)
    def test_full_1152(self):self.assertEqual(sum(len(sources(w)) for w in WORLDS),1152)
    def test_observed_alias_and_hidden_mixture(self):self.assertTrue(observational_alias_certificates())
    def test_late_history_mixture(self):
        w="LATENT_RATE_MIXTURE"
        self.assertEqual(conditional(w,{1:0,2:0},event_value=0),F(7,10))
        self.assertEqual(conditional(w,{1:1,2:0},event_value=0),F(3,10))
    def test_fixed_policy_non_markov(self):
        self.assertEqual(markov_defect("FIXED_SWITCH_POLICY"),F(1,2))
    def test_time_varying_is_still_markov(self):
        self.assertEqual(markov_defect("TIME_ALTERNATING_RATE"),ZERO)
    def test_all_CK_homogeneous(self):
        for w in HOMOGENEOUS:self.assertTrue(markov_ck(w))
    def test_constant_sensor_alias(self):
        self.assertTrue(all(r["oracle_hidden_h3"]==0 for r in sources("STATIC_HIDDEN_SENSOR_ALIAS")))
        self.assertEqual(observed_path_joint("STATIC_HIDDEN_SENSOR_ALIAS"),
                         observed_path_joint("PERSISTENT_3OF4"))
    def test_absorbing_one(self):
        self.assertEqual(kernel_prob("ABSORB_ONE",1,1,1,0),ONE)
        self.assertEqual(kernel_prob("ABSORB_ONE",1,1,0,0),ZERO)
    def test_invalid(self):
        with self.assertRaises(ValueError):sources("UNKNOWN")
    def test_full_path_support(self):
        self.assertEqual(len(observed_path_joint("IID_FAIR")),8)

def _case(world,kind):
    def t(self):
        rows=sources(world)
        if kind=="mass":
            self.assertEqual(sum((r["original_source_probability"] for r in rows),ZERO),ONE)
        elif kind=="unique":
            self.assertEqual(len({tuple(r[k] for k in ("oracle_source_U",
                          "oracle_original_R11","oracle_original_R12",
                          "oracle_original_R21","oracle_original_R22",
                          "oracle_original_R31","oracle_original_R32")) for r in rows}),128)
        elif kind=="positive":
            self.assertTrue(all(r["original_source_probability"]>0 for r in rows))
        elif kind=="joint":
            self.assertEqual(observed_path_joint(world),independent_path_joint(world))
        elif kind=="normalization":
            self.assertEqual(sum(observed_path_joint(world).values(),ZERO),ONE)
        elif kind=="supported_condition":
            self.assertGreaterEqual(markov_defect(world),ZERO)
        elif kind=="oracle":
            self.assertEqual(len({(r["observed_y0"],r["observed_y1"],
                                   r["observed_y2"],r["observed_y3"]) for r in rows}),
                             len(observed_path_joint(world)))
        elif kind=="report":
            self.assertEqual(world_result(world)["complete_original_seven_bit_exogenous_atoms"],128)
        else:raise AssertionError("unknown test")
    return t
for _w in WORLDS:
    for _kind in ("mass","unique","positive","joint","normalization","supported_condition","oracle","report"):
        setattr(Tests,"test_"+_w.lower()+"_"+_kind,_case(_w,_kind))

if __name__=="__main__":
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true")
    g.add_argument("--emit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["r244"],verbosity=2)
    else:print(json.dumps(generate(),indent=2))
