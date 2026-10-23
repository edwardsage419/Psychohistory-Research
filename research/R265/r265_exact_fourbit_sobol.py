#!/usr/bin/env python3
"""R265: exhaustive Sobol variance decomposition for nine finite four-bit worlds.

144 complete original 4bit sources. One route is the orthogonal Walsh basis
over independent Rademacher inputs. The second uses independent conditional
expectations and subset Möbius inversion, not the Walsh coefficients.
No Monte Carlo estimator, uncertain correlated inputs, human/historical data.
"""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
HERE=Path(__file__).resolve().parent
FREEZE="3236f95d7773c63f54fdfd521d060d9ef606b1ad"
ZERO=F(0);ONE=F(1)
INPUTS=tuple(itertools.product((0,1),repeat=4))
NONEMPTY=tuple(range(1,16))
WORLDS=(
 "ADDITIVE_WEIGHTED_123",
 "ADDITIVE_EQUAL_FOUR",
 "PURE_PAIR_PARITY",
 "PURE_TRIPLE_PARITY",
 "PURE_FOUR_PARITY",
 "AND_PAIR",
 "AND_FOUR",
 "SHIFT_SCALED_PAIR_PARITY",
 "INTERACTION_PLUS_ADDITIVE")
def check(w):
    if w not in WORLDS:raise ValueError("not a frozen Sobol world")
def output(w,x):
    check(w)
    if len(x)!=4 or any(v not in (0,1) for v in x):raise ValueError("requires four fair bits")
    a,b,c,d=x
    if w=="ADDITIVE_WEIGHTED_123":return F(a+2*b+3*c)
    if w=="ADDITIVE_EQUAL_FOUR":return F(a+b+c+d)
    if w=="PURE_PAIR_PARITY":return F(a^b)
    if w=="PURE_TRIPLE_PARITY":return F(a^b^c)
    if w=="PURE_FOUR_PARITY":return F(a^b^c^d)
    if w=="AND_PAIR":return F(a*b)
    if w=="AND_FOUR":return F(a*b*c*d)
    if w=="SHIFT_SCALED_PAIR_PARITY":return F(7+3*(a^b))
    if w=="INTERACTION_PLUS_ADDITIVE":return F((a^b)+c+2*d)
    raise AssertionError("unhandled frozen world")
def source_atom(w,x):
    y=output(w,x)
    row=dict(world=w,original_frozen_fourbit_output_Y=y,
       original_output_squared_Y2=y*y,original_complete_fourbit_design_probability=F(1,16))
    for i,v in enumerate(x):row[f"oracle_original_independent_input_X{i+1}"]=v
    return row
@lru_cache(None)
def sources(w):
    check(w)
    rows=tuple(source_atom(w,x) for x in INPUTS)
    assert len(rows)==16 and sum((z["original_complete_fourbit_design_probability"] for z in rows),ZERO)==ONE
    return rows
def bit_selected(mask):
    return tuple(i for i in range(4) if mask&(1<<i))
def direct_mean_variance(w):
    vals=[z["original_frozen_fourbit_output_Y"] for z in sources(w)]
    mu=sum(vals,ZERO)/16
    variance=sum(((v-mu)**2 for v in vals),ZERO)/16
    if variance<=ZERO:raise AssertionError("Sobol division by zero frozen world")
    return mu,variance
def walsh_fourier_components(w):
    """First exact route: orthogonal +/-1 Fourier basis on all sixteen sources."""
    rows=sources(w)
    ans={}
    for mask in NONEMPTY:
        coeff=ZERO
        for z in rows:
            prod=ONE
            for i in bit_selected(mask):
                prod*=2*z[f"oracle_original_independent_input_X{i+1}"]-1
            coeff+=z["original_complete_fourbit_design_probability"]*z["original_frozen_fourbit_output_Y"]*prod
        ans[mask]=coeff*coeff
    return ans
def independent_conditional_mobius(w):
    """Second route: E[Y|X_S] and Möbius inversion; never call Walsh routine."""
    f={x:output(w,x) for x in INPUTS}
    totalmean=sum(f.values(),ZERO)/16
    conditional_variance={0:ZERO}
    for mask in NONEMPTY:
        chosen=bit_selected(mask)
        grouped={}
        for x,v in f.items():
            key=tuple(x[i] for i in chosen)
            grouped.setdefault(key,[]).append(v)
        conditional_means=[sum(values,ZERO)/len(values) for values in grouped.values()]
        assert len(conditional_means)==(1<<len(chosen))
        conditional_variance[mask]=sum(((v-totalmean)**2 for v in conditional_means),ZERO)/len(conditional_means)
    pieces={}
    for mask in sorted(NONEMPTY,key=lambda m:(m.bit_count(),m)):
        pieces[mask]=conditional_variance[mask]-sum((v for subset,v in pieces.items() if subset&mask==subset),ZERO)
        assert pieces[mask]>=ZERO
    return pieces,conditional_variance
def sensitivity(w):
    mu,V=direct_mean_variance(w)
    chunks=walsh_fourier_components(w)
    independent,cond=independent_conditional_mobius(w)
    if chunks!=independent or sum(chunks.values(),ZERO)!=V:
        raise AssertionError(f"{w}: orthogonal Sobol vs conditional Möbius exact decomposition mismatch")
    first=[chunks[1<<i]/V for i in range(4)]
    total=[sum((v for mask,v in chunks.items() if mask&(1<<i)),ZERO)/V for i in range(4)]
    complementary=[ONE-cond[15^(1<<i)]/V for i in range(4)]
    assert total==complementary
    assert all(0<=f<=t<=1 for f,t in zip(first,total))
    return dict(world=w,original_complete_fourbit_source_atoms=16,
       exact_mean_Y=str(mu),exact_variance_Y=str(V),
       complete_nonempty_subset_variance_components={str(k):str(chunks[k]) for k in NONEMPTY},
       complete_nonempty_subset_Sobol_indices={str(k):str(chunks[k]/V) for k in NONEMPTY},
       first_order_S1_S2_S3_S4=[str(z) for z in first],
       total_effect_ST1_ST2_ST3_ST4=[str(z) for z in total],
       independent_conditional_expectation_Mobius_decomposition_verified=True,
       source_variance_equals_sum_all_15_interaction_components=True,
       all_four_total_indices_equal_complement_conditional_formula=True)
def locked_claims():
    for w in WORLDS:sensitivity(w)
    a=sensitivity("ADDITIVE_WEIGHTED_123")
    assert a["exact_variance_Y"]=="7/2"
    assert a["first_order_S1_S2_S3_S4"]==["1/14","2/7","9/14","0"]
    assert a["first_order_S1_S2_S3_S4"]==a["total_effect_ST1_ST2_ST3_ST4"]
    a=sensitivity("ADDITIVE_EQUAL_FOUR")
    assert a["first_order_S1_S2_S3_S4"]==a["total_effect_ST1_ST2_ST3_ST4"]==["1/4"]*4
    for world,key,variance in [("PURE_PAIR_PARITY","3","1/4"),
                               ("PURE_TRIPLE_PARITY","7","1/4"),
                               ("PURE_FOUR_PARITY","15","1/4"),
                               ("SHIFT_SCALED_PAIR_PARITY","3","9/4")]:
        z=sensitivity(world)
        assert z["exact_variance_Y"]==variance
        assert z["complete_nonempty_subset_Sobol_indices"][key]=="1"
        assert all(v=="0" for k,v in z["complete_nonempty_subset_Sobol_indices"].items() if k!=key)
    a=sensitivity("AND_PAIR")
    assert a["exact_variance_Y"]=="3/16"
    assert [a["complete_nonempty_subset_Sobol_indices"][k] for k in ("1","2","3")]==["1/3"]*3
    assert a["total_effect_ST1_ST2_ST3_ST4"]==["2/3","2/3","0","0"]
    a=sensitivity("AND_FOUR")
    assert a["exact_variance_Y"]=="15/256"
    assert all(v=="1/15" for v in a["complete_nonempty_subset_Sobol_indices"].values())
    assert a["first_order_S1_S2_S3_S4"]==["1/15"]*4
    assert a["total_effect_ST1_ST2_ST3_ST4"]==["8/15"]*4
    a=sensitivity("INTERACTION_PLUS_ADDITIVE")
    assert a["exact_variance_Y"]=="3/2"
    assert a["first_order_S1_S2_S3_S4"]==["0","0","1/6","2/3"]
    assert a["total_effect_ST1_ST2_ST3_ST4"]==["1/6","1/6","1/6","2/3"]
    assert a["complete_nonempty_subset_Sobol_indices"]["3"]=="1/6"
    return True
def emit():
    locked_claims()
    result=dict(research_id="R265",original_catalogue_id="11-025",
       prescore_freeze_commit=FREEZE,
       scientific_scope="FINITE_ARTIFICIAL_E1_EXACT_FOUR_INDEPENDENT_BINARY_SOBOL_ANOVA",
       frozen_worlds=9,complete_original_fourbit_source_atoms=144,
       variance_decomposition_subset_count_per_world=15,
       original_independent_Bernoulli_input_probability="1/16 per 4bit configuration",
       analytical_walsh_fourier_vs_conditional_Mobius_all_15_components_exact=True,
       high_order_parity_all_first_order_zero_but_total_order_one=True,
       correlated_input_generalization_not_established=True,
       no_sampling_Saltelli_estimator_variance_or_human_parameter_distribution_established=True,
       new_real_human_E2=0,new_real_historical_E3=0,R073="FROZEN",PESEN_v0_1="FROZEN",
       world_results=[sensitivity(w) for w in WORLDS])
    out=HERE/"R265_ALL_144_ORIGINAL_FOURBIT_SOBOL_INPUT_SOURCES.csv"
    keys=list(sources(WORLDS[0])[0])
    with out.open("w",newline="",encoding="utf-8") as f:
        wr=csv.DictWriter(f,fieldnames=keys,lineterminator="\n");wr.writeheader()
        for w in WORLDS:
            for z in sources(w):wr.writerow({k:str(z[k]) for k in keys})
    jp=HERE/"R265_EXACT_RESULTS.json"
    jp.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    receipt=dict(research_id="R265",original_catalogue_id="11-025",
       frozen_worlds=9,all_complete_original_fourbit_source_atoms=144,
       all_135_independent_Sobol_subset_variance_comparisons_verified=True,
       zero_first_vs_unit_total_for_pure_fourway_interaction=True,
       scale_shift_invariant_pair_parity_indices=True,
       source_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),
       results_sha256=hashlib.sha256(jp.read_bytes()).hexdigest(),
       new_real_human_E2=0,new_real_historical_E3=0)
    (HERE/"R265_FINAL_MACHINE_ACCEPTANCE.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt
class Tests(unittest.TestCase):
    def test_nine(self):self.assertEqual(len(WORLDS),9)
    def test_144(self):self.assertEqual(sum(len(sources(w)) for w in WORLDS),144)
    def test_lock(self):self.assertTrue(locked_claims())
    def test_additive_weighted(self):self.assertEqual(sensitivity("ADDITIVE_WEIGHTED_123")["exact_variance_Y"],"7/2")
    def test_four_parity(self):self.assertEqual(sensitivity("PURE_FOUR_PARITY")["total_effect_ST1_ST2_ST3_ST4"],["1"]*4)
    def test_four_And(self):self.assertEqual(sensitivity("AND_FOUR")["first_order_S1_S2_S3_S4"],["1/15"]*4)
    def test_zero_first_nonzero_total(self):self.assertEqual(sensitivity("PURE_PAIR_PARITY")["first_order_S1_S2_S3_S4"],["0"]*4)
    def test_summed_variance(self):
        for w in WORLDS:
            z=sensitivity(w)
            self.assertEqual(sum((F(v) for v in z["complete_nonempty_subset_variance_components"].values()),ZERO),F(z["exact_variance_Y"]))
    def test_mask(self):self.assertEqual(bit_selected(3),(0,1))
    def test_invalid(self):
        with self.assertRaises(ValueError):sources("NOT_FROZEN")
def _case(w,k):
    def t(self):
        src=sources(w)
        if k=="mass":self.assertEqual(sum((z["original_complete_fourbit_design_probability"] for z in src),ZERO),ONE)
        elif k=="unique":
            fields=[f"oracle_original_independent_input_X{i}" for i in range(1,5)]
            self.assertEqual(len({tuple(z[k] for k in fields) for z in src}),16)
        elif k=="positive":self.assertTrue(all(z["original_complete_fourbit_design_probability"]==F(1,16) for z in src))
        elif k=="source":
            for z in src:
                x=tuple(z[f"oracle_original_independent_input_X{i}"] for i in range(1,5))
                self.assertEqual(z["original_frozen_fourbit_output_Y"],output(w,x))
        elif k=="square":
            for z in src:self.assertEqual(z["original_output_squared_Y2"],z["original_frozen_fourbit_output_Y"]**2)
        elif k=="mobius":self.assertEqual(walsh_fourier_components(w),independent_conditional_mobius(w)[0])
        elif k=="normal":
            z=sensitivity(w)
            self.assertEqual(sum((F(v) for v in z["complete_nonempty_subset_Sobol_indices"].values()),ZERO),ONE)
        elif k=="report":self.assertEqual(sensitivity(w)["original_complete_fourbit_source_atoms"],16)
        else:raise AssertionError("bad frozen test")
    return t
for w in WORLDS:
    for k in ("mass","unique","positive","source","square","mobius","normal","report"):
        setattr(Tests,"test_"+w.lower()+"_"+k,_case(w,k))
if __name__=="__main__":
    ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true");g.add_argument("--emit",action="store_true")
    a=ap.parse_args()
    if a.test:unittest.main(argv=["r265"],verbosity=2)
    else:print(json.dumps(emit(),indent=2))
