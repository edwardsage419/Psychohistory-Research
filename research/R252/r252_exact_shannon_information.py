#!/usr/bin/env python3
"""R252 finite discrete Shannon entropy and conditional mutual information.

Complete 6-bit source universe, 64 per world x nine worlds. Shannon entropy
is represented EXACTLY as rational coefficients in basis 1, log2(prime)
without assuming irrational binary entropy at 1/4 is rational. Independent
world-specific closed joint laws verify all 3-variable PMFs.
"""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,math,unittest
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path

HERE=Path(__file__).resolve().parent
FREEZE="30815e3018c099ee362780f1b2292dc33644e27d"
Z=F(0);ONE=F(1)
BITS=(0,1)
EXOG=tuple(itertools.product(BITS,repeat=6))
WORLDS=("INDEPENDENT_BITS","DIRECT_COPY","HIDDEN_COMMON_CAUSE_ALIAS",
        "XOR_SYNERGY","ERASURE_HALF","BINARY_SYMMETRIC_QUARTER",
        "COLLIDER_AND","XOR_MASK_REPARAM","CONSTANT_REPORTER")
EXACT_LOG3_MI={"1":F(-1),"log2_3":F(3,4)}

def check(w):
    if w not in WORLDS:raise ValueError("unfrozen Shannon world")

def observe_and_do(w,bits):
    check(w)
    if len(bits)!=6 or any(b not in BITS for b in bits):
        raise ValueError("expected six independent fair exogenous bits")
    u,a,b,c,d,e=bits
    x=a
    flipped=1-a
    if w=="INDEPENDENT_BITS":y=b;z=c;do_y=b
    elif w=="DIRECT_COPY":y=x;z=c;do_y=flipped
    elif w=="HIDDEN_COMMON_CAUSE_ALIAS":y=a;z=c;do_y=a
    elif w=="XOR_SYNERGY":y=b;z=a^b;do_y=b
    elif w=="ERASURE_HALF":
        y=x if c else 2;z=c;do_y=flipped if c else 2
    elif w=="BINARY_SYMMETRIC_QUARTER":
        noise=b&c;y=x^noise;z=b;do_y=flipped^noise
    elif w=="COLLIDER_AND":y=b;z=a&b;do_y=b
    elif w=="XOR_MASK_REPARAM":y=x^b;z=b;do_y=flipped^b
    elif w=="CONSTANT_REPORTER":y=0;z=c;do_y=0
    else:raise AssertionError("case omitted")
    return (x,y,z),do_y

def source_atom(w,bits):
    xyz,do_y=observe_and_do(w,bits)
    out={"world":w}
    for name,val in zip("UABCDE",bits):out["oracle_original_"+name]=val
    for name,val in zip("XYZ",xyz):out["observed_"+name]=val
    out["oracle_counterfactual_Y_after_do_X_flip"]=do_y
    out["original_sixbit_source_probability"]=F(1,64)
    return out

@lru_cache(None)
def sources(w):
    check(w)
    s=tuple(source_atom(w,b) for b in EXOG)
    assert len(s)==64 and sum((r["original_sixbit_source_probability"] for r in s),Z)==ONE
    return s

@lru_cache(None)
def observed_joint(w):
    d=defaultdict(F)
    for r in sources(w):
        key=tuple(r["observed_"+k] for k in "XYZ")
        d[key]+=r["original_sixbit_source_probability"]
    return dict(sorted(d.items()))

def theoretical_joint(w):
    """Explicit frozen full trivariate PMF; calls no source simulator."""
    check(w)
    d={}
    if w=="INDEPENDENT_BITS":
        for x,y,z in itertools.product(BITS,repeat=3):d[(x,y,z)]=F(1,8)
    elif w in ("DIRECT_COPY","HIDDEN_COMMON_CAUSE_ALIAS"):
        for x,z in itertools.product(BITS,repeat=2):d[(x,x,z)]=F(1,4)
    elif w in ("XOR_SYNERGY","XOR_MASK_REPARAM"):
        for x,y in itertools.product(BITS,repeat=2):d[(x,y,x^y)]=F(1,4)
    elif w=="ERASURE_HALF":
        for x in BITS:
            d[(x,2,0)]=F(1,4)
            d[(x,x,1)]=F(1,4)
    elif w=="BINARY_SYMMETRIC_QUARTER":
        for x in BITS:
            d[(x,x,0)]=F(1,4)
            d[(x,x,1)]=F(1,8)
            d[(x,1-x,1)]=F(1,8)
    elif w=="COLLIDER_AND":
        for x,y in itertools.product(BITS,repeat=2):d[(x,y,x&y)]=F(1,4)
    elif w=="CONSTANT_REPORTER":
        for x,z in itertools.product(BITS,repeat=2):d[(x,0,z)]=F(1,4)
    else:raise AssertionError("frozen analytic law missing")
    assert sum(d.values(),Z)==ONE
    return dict(sorted(d.items()))

def marginal(joint,indices):
    d=defaultdict(F)
    for xyz,p in joint.items():d[tuple(xyz[i] for i in indices)]+=p
    return dict(sorted(d.items()))

def factor(n):
    """Small-integer prime exponents, including prime 2."""
    if not isinstance(n,int) or n<1:raise ValueError("positive numerator only")
    out={}
    p=2
    while p*p<=n:
        while n%p==0:
            out[p]=out.get(p,0)+1
            n//=p
        p+=1
    if n>1:out[n]=out.get(n,0)+1
    return out

def canonical(expr):
    return {k:v for k,v in sorted(expr.items()) if v!=Z}
def plus(*expressions):
    out=defaultdict(F)
    for e in expressions:
        for k,v in e.items():out[k]+=v
    return canonical(out)
def minus(expr):return canonical({k:-v for k,v in expr.items()})
def entropy_symbolic(joint):
    """-sum p log2(p), p dyadic; exact rationals in prime-log basis."""
    if sum(joint.values(),Z)!=ONE:raise AssertionError("joint law not normalized")
    out=defaultdict(F)
    for p in joint.values():
        if p<=0:raise AssertionError("positive probabilities only in support")
        den=p.denominator
        if den&(den-1):raise AssertionError("non-binary denominator unsupported by exact log symbol")
        out["1"]+=p*(den.bit_length()-1)
        for prime,power in factor(p.numerator).items():
            if prime==2:out["1"]-=p*power
            else:out["log2_"+str(prime)]-=p*power
    return canonical(out)

def entropy_for(joint,inds):
    return entropy_symbolic(marginal(joint,inds))
def info_formulas(joint):
    hX=entropy_for(joint,(0,))
    hY=entropy_for(joint,(1,))
    hZ=entropy_for(joint,(2,))
    hXY=entropy_for(joint,(0,1))
    hXZ=entropy_for(joint,(0,2))
    hYZ=entropy_for(joint,(1,2))
    hXYZ=entropy_for(joint,(0,1,2))
    iXY=plus(hX,hY,minus(hXY))
    iXZ=plus(hX,hZ,minus(hXZ))
    iYZ=plus(hY,hZ,minus(hYZ))
    iXYz=plus(hXZ,hYZ,minus(hZ),minus(hXYZ))
    interaction=plus(iXY,minus(iXYz))
    tc=plus(hX,hY,hZ,minus(hXYZ))
    # A symmetry/chain-rule consistency check from independent algebraic forms.
    if iXY!=plus(hX,minus(plus(hXY,minus(hY)))):
        raise AssertionError("MI entropy identity violated")
    if iXYz!=plus(hXZ,minus(hZ),minus(plus(hXYZ,minus(hYZ)))):
        raise AssertionError("conditional MI identity violated")
    return dict(HX=hX,HY=hY,HZ=hZ,HXY=hXY,HXZ=hXZ,HYZ=hYZ,HXYZ=hXYZ,
                IXY=iXY,IXZ=iXZ,IYZ=iYZ,IXY_given_Z=iXYz,
                interaction_information=interaction,total_correlation=tc)

def sym_json(e):
    return {"exact_rational":str(e.get("1",Z)),
            "exact_log2_prime_coefficients":{
                k.removeprefix("log2_"):str(v)
                for k,v in e.items() if k!="1"},
            "numeric_approx_bits":round(float(e.get("1",Z))+
                sum(float(v)*math.log2(int(k.removeprefix("log2_"))) for k,v in e.items() if k!="1"),12)}

def frozen_claims():
    expected={
     "INDEPENDENT_BITS":(Z,Z,ONE,ONE,ONE),
     "DIRECT_COPY":(ONE,ONE,ONE,ONE,ONE),
     "HIDDEN_COMMON_CAUSE_ALIAS":(ONE,ONE,ONE,ONE,ONE),
     "XOR_SYNERGY":(Z,ONE,ONE,ONE,ONE),
     "ERASURE_HALF":(F(1,2),F(1,2),ONE,F(3,2),ONE),
     "BINARY_SYMMETRIC_QUARTER":(EXACT_LOG3_MI,F(1,2),ONE,ONE,ONE),
     "COLLIDER_AND":(Z,EXACT_LOG3_MI,ONE,ONE,Z),
     "XOR_MASK_REPARAM":(Z,ONE,ONE,ONE,ONE),
     "CONSTANT_REPORTER":(Z,Z,ONE,Z,ONE)
    }
    for w,(I,IC,HX,HY,HZ) in expected.items():
        law=observed_joint(w)
        if law!=theoretical_joint(w):raise AssertionError("source vs independently specified distribution")
        q=info_formulas(law)
        def expr(x):return x if isinstance(x,dict) else ({"1":x} if x else {})
        for name,x in (("IXY",I),("IXY_given_Z",IC),("HX",HX),("HY",HY),("HZ",HZ)):
            if q[name]!=expr(x):
                raise AssertionError(f"{w} {name} exact symbol mismatch: {q[name]} vs {expr(x)}")
    assert 3**3>2**4 # 3/4 log2 3 > 1, so the nonrational MI is positive.
    copy="DIRECT_COPY";hidden="HIDDEN_COMMON_CAUSE_ALIAS"
    for bit in EXOG:
        o1,do1=observe_and_do(copy,bit)
        o2,do2=observe_and_do(hidden,bit)
        assert o1==o2
        assert do1==1-bit[1]
        assert do2==bit[1]
        assert do1!=do2
    assert observed_joint("XOR_SYNERGY")==observed_joint("XOR_MASK_REPARAM")
    assert info_formulas(observed_joint("XOR_SYNERGY"))["interaction_information"]=={"1":F(-1)}
    assert info_formulas(observed_joint("COLLIDER_AND"))["interaction_information"]==minus(EXACT_LOG3_MI)
    return True

def world_result(w):
    j=observed_joint(w)
    assert j==theoretical_joint(w)
    m=info_formulas(j)
    return dict(world=w,all_complete_original_sixbit_atoms=64,
        observed_complete_XYZ_joint={",".join(map(str,k)):str(v) for k,v in j.items()},
        observed_support_size=len(j),
        exact_information_measures={k:sym_json(e) for k,e in m.items()},
        original_oracle_do_flip_Y_by_source=[
            r["oracle_counterfactual_Y_after_do_X_flip"] for r in sources(w)],
        full_source_and_independent_analytic_PMF_equal=True,
        exact_symbolic_prime_log_entropy_algebra=True)
def emit():
    frozen_claims()
    d=dict(research_id="R252",original_catalogue_id="11-012",
       prescore_freeze_commit=FREEZE,
       scientific_scope="FINITE_ARTIFICIAL_E1_SHANNON_ENTROPY_EXACT_PRIME_LOG_COEFFICIENTS_NOT_CAUSAL_IDENTIFICATION",
       frozen_worlds=9,all_complete_original_sixbit_source_atoms=576,
       strictly_exact_information_measures_prime_log_basis=True,
       bsc_and_collider_information_exact="3/4*log2(3)-1",
       bsc_collider_mi_positive_because_3_cubed_greater_than_2_to_fourth=True,
       sourcewise_observation_alias_with_intervention_distinction=[
           "DIRECT_COPY","HIDDEN_COMMON_CAUSE_ALIAS"],
       full_observation_distribution_alias_with_reparam=[
           "XOR_SYNERGY","XOR_MASK_REPARAM"],
       new_real_human_E2=0,new_real_historical_E3=0,
       R073="FROZEN",PESEN_v0_1="FROZEN",
       world_results=[world_result(w) for w in WORLDS])
    path=HERE/"R252_ALL_576_ORIGINAL_SIXBIT_INFORMATION_SOURCES.csv"
    keys=list(sources(WORLDS[0])[0])
    with path.open("w",encoding="utf-8",newline="") as f:
        wr=csv.DictWriter(f,fieldnames=keys,lineterminator="\n")
        wr.writeheader()
        for w in WORLDS:
            for r in sources(w):wr.writerow({k:str(r[k]) for k in keys})
    result=HERE/"R252_EXACT_RESULTS.json"
    result.write_text(json.dumps(d,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    rec=dict(research_id="R252",original_catalogue_id="11-012",frozen_worlds=9,
       complete_original_sixbit_atom_types=576,
       symbolically_exact_prime_log_entropy_coefficients=True,
       sourcewise_alias_different_do_X_causal_oracle=True,
       independent_world_specific_joint_probability_closed_forms=True,
       source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
       results_sha256=hashlib.sha256(result.read_bytes()).hexdigest(),
       new_real_human_E2=0,new_real_historical_E3=0)
    (HERE/"R252_FINAL_MACHINE_ACCEPTANCE.json").write_text(json.dumps(rec,indent=2)+"\n",encoding="utf-8")
    return rec

class Tests(unittest.TestCase):
    def test_nine(self):self.assertEqual(len(WORLDS),9)
    def test_576_original_bits(self):self.assertEqual(sum(len(sources(w)) for w in WORLDS),576)
    def test_frozen_information_and_aliases(self):self.assertTrue(frozen_claims())
    def test_prime_factorization(self):self.assertEqual(factor(24),{2:3,3:1})
    def test_exact_non_rational(self):self.assertEqual(EXACT_LOG3_MI,{"1":F(-1),"log2_3":F(3,4)})
    def test_bsc_information(self):
        self.assertEqual(info_formulas(observed_joint("BINARY_SYMMETRIC_QUARTER"))["IXY"],EXACT_LOG3_MI)
    def test_collider_conditional_information(self):
        self.assertEqual(info_formulas(observed_joint("COLLIDER_AND"))["IXY_given_Z"],EXACT_LOG3_MI)
    def test_erasure(self):
        a=info_formulas(observed_joint("ERASURE_HALF"))
        self.assertEqual(a["HY"],{"1":F(3,2)})
        self.assertEqual(a["IXY"],{"1":F(1,2)})
    def test_xor_synergy(self):
        a=info_formulas(observed_joint("XOR_SYNERGY"))
        self.assertEqual(a["IXY"],{})
        self.assertEqual(a["IXY_given_Z"],{"1":ONE})
    def test_direct_hidden_same_observation(self):
        self.assertEqual(observed_joint("DIRECT_COPY"),observed_joint("HIDDEN_COMMON_CAUSE_ALIAS"))
    def test_binary_entropy_fair(self):
        self.assertEqual(entropy_symbolic({(0,):F(1,2),(1,):F(1,2)}),{"1":ONE})
    def test_constant_entropy_zero(self):
        self.assertEqual(entropy_symbolic({(0,):ONE}),{})
    def test_not_frozen(self):
        with self.assertRaises(ValueError):sources("NOT_A_WORLD")

def _case(w,kind):
    def t(self):
        src=sources(w)
        if kind=="mass":self.assertEqual(sum((r["original_sixbit_source_probability"] for r in src),Z),ONE)
        elif kind=="unique":
            keys=["oracle_original_"+x for x in "UABCDE"]
            self.assertEqual(len({tuple(r[k] for k in keys) for r in src}),64)
        elif kind=="positive":self.assertTrue(all(r["original_sixbit_source_probability"]==F(1,64) for r in src))
        elif kind=="independent":self.assertEqual(observed_joint(w),theoretical_joint(w))
        elif kind=="entropy":
            m=info_formulas(observed_joint(w))
            self.assertTrue("IXY" in m and "IXY_given_Z" in m)
            self.assertEqual(m["IXY"],plus(m["HX"],m["HY"],minus(m["HXY"])))
        elif kind=="conditional":
            m=info_formulas(observed_joint(w))
            self.assertEqual(m["IXY_given_Z"],
                             plus(m["HXZ"],m["HYZ"],minus(m["HZ"]),minus(m["HXYZ"])))
        elif kind=="bits":
            self.assertTrue(all(r["observed_X"] in BITS and r["observed_Z"] in BITS for r in src))
        elif kind=="result":
            self.assertEqual(world_result(w)["all_complete_original_sixbit_atoms"],64)
        else:raise AssertionError("not frozen")
    return t
for w in WORLDS:
    for kind in ("mass","unique","positive","independent","entropy","conditional","bits","result"):
        setattr(Tests,"test_"+w.lower()+"_"+kind,_case(w,kind))
if __name__=="__main__":
    p=argparse.ArgumentParser();group=p.add_mutually_exclusive_group(required=True)
    group.add_argument("--test",action="store_true");group.add_argument("--emit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["r252"],verbosity=2)
    else:print(json.dumps(emit(),indent=2))
