#!/usr/bin/env python3
"""R240 exact binary inter-coder agreement vs hidden correctness.

Nine frozen artificial annotation populations of 2^8 original exogenous
sources. Agreement reads only selected observed coder A/B. Hidden true label
T, deleted coder decisions, and source errors are accessible to oracle audits
only. Cohen kappa and pair-complete finite nominal alpha are not conflated.
"""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path

HERE=Path(__file__).resolve().parent
ZERO=F(0)
ONE=F(1)
FREEZE="23ffd77477c9eba53867692e27303ecc666a55e9"
SOURCE_NAMES=("T","U","E1","E2","E3","E4","E5","E6")
WORLDS=(
    "PERFECT_TRUTHFUL",
    "PERFECT_SYSTEMATICALLY_WRONG",
    "SHARED_SYSTEMATIC_ERROR",
    "INDEPENDENT_QUARTER_ERRORS",
    "BALANCED_INDEPENDENT_RANDOM",
    "RARE_POSITIVE_INDEPENDENT_RANDOM",
    "ASYMMETRIC_FALSE_POSITIVE",
    "SELECTIVE_MISSING_DISAGREEMENTS",
    "OPPOSING_CODERS",
)

def coder_decisions(world,values):
    if world not in WORLDS or len(values)!=8 or any(v not in (0,1) for v in values):
        raise ValueError("outside frozen binary inter-coder source support")
    t,u,e1,e2,e3,e4,e5,e6=values
    del u
    if world=="PERFECT_TRUTHFUL":
        a=b=t
    elif world=="PERFECT_SYSTEMATICALLY_WRONG":
        a=b=1-t
    elif world=="SHARED_SYSTEMATIC_ERROR":
        a=b=t^(e1&e2)
    elif world=="INDEPENDENT_QUARTER_ERRORS":
        a=t^(e1&e2);b=t^(e3&e4)
    elif world=="BALANCED_INDEPENDENT_RANDOM":
        a=e1;b=e2
    elif world=="RARE_POSITIVE_INDEPENDENT_RANDOM":
        a=e1&e2&e3;b=e4&e5&e6
    elif world=="ASYMMETRIC_FALSE_POSITIVE":
        a=t;b=t|(e1&e2)
    elif world=="SELECTIVE_MISSING_DISAGREEMENTS":
        a=t;b=t^(e1&e2)
    elif world=="OPPOSING_CODERS":
        a=t;b=1-t
    else:raise AssertionError("unknown coding world")
    selected=int(a==b) if world=="SELECTIVE_MISSING_DISAGREEMENTS" else 1
    return a,b,selected

def source_atom(world,bits):
    a,b,s=coder_decisions(world,bits)
    r={"world":world}
    for key,x in zip(SOURCE_NAMES,bits):r["oracle_original_"+key]=x
    r.update(
        oracle_gold_label_T=bits[0],
        oracle_full_coder_A=a,oracle_full_coder_B=b,
        observed_pair_available=s,
        observed_coder_A=a if s else -1,
        observed_coder_B=b if s else -1,
        original_structural_source_probability=F(1,256)
    )
    return r

def sources(world):
    if world not in WORLDS:raise ValueError("unknown world")
    rows=tuple(source_atom(world,bits) for bits in itertools.product((0,1),repeat=8))
    if len(rows)!=256 or sum((r["original_structural_source_probability"] for r in rows),ZERO)!=ONE:
        raise AssertionError("full annotation source support incomplete")
    return rows

def observed_joint(world):
    out=defaultdict(F)
    for r in sources(world):
        k=(r["observed_pair_available"],r["observed_coder_A"],r["observed_coder_B"])
        out[k]+=r["original_structural_source_probability"]
    return dict(sorted(out.items()))

def independent_observed_counts(world):
    """Direct frozen coder decision code; does NOT consult source rows or CSV."""
    out=defaultdict(int)
    for bits in itertools.product((0,1),repeat=8):
        a,b,s=coder_decisions(world,bits)
        out[(s,a if s else -1,b if s else -1)]+=1
    return dict(sorted(out.items()))

def observed_table(world):
    # Read recorded codes only for complete cases. Hidden error/gold omitted.
    rows=[r for r in sources(world) if r["observed_pair_available"]]
    tab={(a,b):sum(int(r["observed_coder_A"]==a and r["observed_coder_B"]==b)
                  for r in rows) for a in (0,1) for b in (0,1)}
    if sum(tab.values())!=len(rows) or len(rows)<2:raise AssertionError("not enough observed code units")
    return tab

def observed_agreement(world):
    tab=observed_table(world)
    n=sum(tab.values())
    po=F(tab[0,0]+tab[1,1],n)
    pA0=F(tab[0,0]+tab[0,1],n);pA1=ONE-pA0
    pB0=F(tab[0,0]+tab[1,0],n);pB1=ONE-pB0
    pe=pA0*pB0+pA1*pB1
    if pe==ONE:raise AssertionError("frozen Cohen kappa denominator zero")
    kappa=(po-pe)/(ONE-pe)
    # Finite nominal Krippendorff alpha, pair-complete observations only.
    # Expected disagreement draws 2 labels without replacement among 2*n
    # finite coder responses; is intentionally not the Cohen-kappa baseline.
    m0=2*tab[0,0]+tab[0,1]+tab[1,0]
    m1=2*tab[1,1]+tab[0,1]+tab[1,0]
    assert m0+m1==2*n
    do=F(tab[0,1]+tab[1,0],n)
    de=F(2*m0*m1,2*n*(2*n-1))
    if de==0:raise AssertionError("frozen nominal alpha chance denominator zero")
    alpha=ONE-do/de
    return dict(
        selected_source_units=n,observed_pair_agreement=po,
        expected_independent_marginal_agreement=pe,
        cohens_kappa=kappa,
        nominal_krippendorff_alpha_pair_complete=alpha,
        nominal_alpha_observed_disagreement=do,
        nominal_alpha_finite_without_replacement_expected_disagreement=de,
        observed_coder_A_positive_marginal=pA1,
        observed_coder_B_positive_marginal=pB1
    )

def independent_agreement(world):
    """Second route uses frozen structural decision function, not source rows."""
    t=independent_observed_counts(world)
    tab={(a,b):t.get((1,a,b),0) for a in (0,1) for b in (0,1)}
    n=sum(tab.values())
    po=F(tab[0,0]+tab[1,1],n)
    pe=F(tab[0,0]+tab[0,1],n)*F(tab[0,0]+tab[1,0],n)+F(tab[1,0]+tab[1,1],n)*F(tab[0,1]+tab[1,1],n)
    return (n,po,pe,(po-pe)/(ONE-pe))

def oracle_accuracy(world):
    # Explicitly depends on artificial gold T and ALL 256 original sources,
    # including those deleted from actually observed coder pair records.
    data=sources(world)
    return (
        sum((r["original_structural_source_probability"]*int(r["oracle_full_coder_A"]==r["oracle_gold_label_T"]) for r in data),ZERO),
        sum((r["original_structural_source_probability"]*int(r["oracle_full_coder_B"]==r["oracle_gold_label_T"]) for r in data),ZERO)
    )

def oracle_full_pair_agreement(world):
    return sum((r["original_structural_source_probability"]*int(r["oracle_full_coder_A"]==r["oracle_full_coder_B"])
                for r in sources(world)),ZERO)

def full_observed_alias_check():
    one=observed_joint("PERFECT_TRUTHFUL")
    if one!=observed_joint("PERFECT_SYSTEMATICALLY_WRONG") or one!=observed_joint("SHARED_SYSTEMATIC_ERROR"):
        raise AssertionError("shared labels do not generate full observed pair alias")
    expected=[(ONE,ONE),(ZERO,ZERO),(F(3,4),F(3,4))]
    measured=[oracle_accuracy(w) for w in ("PERFECT_TRUTHFUL","PERFECT_SYSTEMATICALLY_WRONG","SHARED_SYSTEMATIC_ERROR")]
    if expected!=measured:raise AssertionError("hidden true accuracies no longer differ")
    return True

def world_result(world):
    joint=observed_joint(world)
    independently=independent_observed_counts(world)
    expected_joint={k:F(v,256) for k,v in independently.items()}
    if joint!=expected_joint:raise AssertionError("full observed source joint and independent truth function differ")
    stats=observed_agreement(world)
    nn,po,pe,kappa=independent_agreement(world)
    if (nn,po,pe,kappa)!=(stats["selected_source_units"],stats["observed_pair_agreement"],
                         stats["expected_independent_marginal_agreement"],stats["cohens_kappa"]):
        raise AssertionError("source-based agreement and independent outcome count route disagree")
    true_agree=oracle_full_pair_agreement(world)
    acc=oracle_accuracy(world)
    if world in ("PERFECT_TRUTHFUL","PERFECT_SYSTEMATICALLY_WRONG","SHARED_SYSTEMATIC_ERROR"):
        assert po==ONE and kappa==ONE and stats["nominal_krippendorff_alpha_pair_complete"]==ONE
    if world=="INDEPENDENT_QUARTER_ERRORS":
        assert po==F(5,8) and kappa==F(1,4) and acc==(F(3,4),F(3,4))
    if world=="BALANCED_INDEPENDENT_RANDOM":
        assert po==F(1,2) and pe==F(1,2) and kappa==ZERO
    if world=="RARE_POSITIVE_INDEPENDENT_RANDOM":
        assert po==pe==F(25,32) and kappa==ZERO
    if world=="ASYMMETRIC_FALSE_POSITIVE":
        assert po==F(7,8) and kappa==F(3,4) and acc==(ONE,F(7,8))
    if world=="SELECTIVE_MISSING_DISAGREEMENTS":
        assert nn==192 and po==ONE and kappa==ONE and true_agree==F(3,4)
        assert acc==(ONE,F(3,4))
    if world=="OPPOSING_CODERS":
        assert po==ZERO and pe==F(1,2) and kappa==-ONE
    return dict(
        world=world,full_original_exogenous_sources=256,
        complete_original_source_mass="1",
        proportion_with_observed_complete_coder_pair=str(F(nn,256)),
        observed_pair_table_2x2={f"{a}{b}":observed_table(world)[a,b] for a in (0,1) for b in (0,1)},
        observed_population_agreement_metrics={k:str(v) for k,v in stats.items()},
        oracle_accuracy_to_hidden_gold_T=[str(v) for v in acc],
        oracle_all_original_sources_coder_pair_agreement=str(true_agree),
        full_observed_selection_and_coder_joint={"".join(map(str,k)):str(v) for k,v in joint.items()}
    )

def generate():
    full_observed_alias_check()
    worlds=[world_result(w) for w in WORLDS]
    result=dict(
        research_id="R240",original_catalogue_id="10-014",
        prescore_freeze_commit=FREEZE,
        scientific_scope="FINITE_ARTIFICIAL_E1_INTER_CODER_RELIABILITY_AND_ACCURACY",
        frozen_worlds=9,full_original_source_atoms=2304,
        complete_observation_alias_accuracy_triple=[
            "PERFECT_TRUTHFUL","PERFECT_SYSTEMATICALLY_WRONG","SHARED_SYSTEMATIC_ERROR"
        ],
        exact_finite_pair_complete_alpha_not_conflated_with_kappa=True,
        nonrandom_missingness_flag_explicit=True,
        independent_source_vs_decision_table_parity=True,
        new_real_human_E2=0,new_real_historical_E3=0,
        R073="FROZEN",PESEN_v0_1="FROZEN",
        world_results=worlds
    )
    csvfile=HERE/"R240_ALL_2304_ORIGINAL_TWO_CODER_ANNOTATION_ATOMS.csv"
    fields=list(sources("PERFECT_TRUTHFUL")[0])
    with csvfile.open("w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=fields,lineterminator="\n")
        writer.writeheader()
        for w in WORLDS:
            for r in sources(w):writer.writerow({k:str(r[k]) for k in fields})
    jsonfile=HERE/"R240_EXACT_RESULTS.json"
    jsonfile.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    machine=dict(
        research_id="R240",original_catalogue_id="10-014",
        frozen_worlds=9,original_source_atoms=2304,
        complete_observed_pair_alias_vs_accuracy_verified=True,
        exact_kappa_and_finite_pair_complete_alpha=True,
        independent_2by2_source_vs_structural_function_verification=True,
        source_sha256=hashlib.sha256(csvfile.read_bytes()).hexdigest(),
        results_sha256=hashlib.sha256(jsonfile.read_bytes()).hexdigest(),
        new_real_human_E2=0,new_real_historical_E3=0
    )
    (HERE/"R240_FINAL_MACHINE_ACCEPTANCE.json").write_text(json.dumps(machine,indent=2)+"\n",encoding="utf-8")
    return machine

class Tests(unittest.TestCase):
    def test_worlds(self):self.assertEqual(len(WORLDS),9)
    def test_2304_sources(self):self.assertEqual(sum(len(sources(w)) for w in WORLDS),2304)
    def test_observational_alias_triple(self):self.assertTrue(full_observed_alias_check())
    def test_hidden_accuracy_can_be_zero(self):
        self.assertEqual(oracle_accuracy("PERFECT_SYSTEMATICALLY_WRONG"),(ZERO,ZERO))
        self.assertEqual(observed_agreement("PERFECT_SYSTEMATICALLY_WRONG")["cohens_kappa"],ONE)
    def test_shared_error_all_agree(self):
        self.assertEqual(oracle_accuracy("SHARED_SYSTEMATIC_ERROR"),(F(3,4),F(3,4)))
        self.assertEqual(observed_agreement("SHARED_SYSTEMATIC_ERROR")["cohens_kappa"],ONE)
    def test_independent_error(self):
        self.assertEqual(observed_agreement("INDEPENDENT_QUARTER_ERRORS")["cohens_kappa"],F(1,4))
    def test_prevalence_paradox(self):
        a=observed_agreement("BALANCED_INDEPENDENT_RANDOM")
        b=observed_agreement("RARE_POSITIVE_INDEPENDENT_RANDOM")
        self.assertGreater(b["observed_pair_agreement"],a["observed_pair_agreement"])
        self.assertEqual(a["cohens_kappa"],b["cohens_kappa"])
        self.assertEqual(a["cohens_kappa"],ZERO)
    def test_missingness_bias(self):
        s=world_result("SELECTIVE_MISSING_DISAGREEMENTS")
        self.assertEqual(s["proportion_with_observed_complete_coder_pair"],"3/4")
        self.assertEqual(s["observed_population_agreement_metrics"]["cohens_kappa"],"1")
        self.assertEqual(s["oracle_all_original_sources_coder_pair_agreement"],"3/4")
    def test_asymmetry(self):
        a=observed_agreement("ASYMMETRIC_FALSE_POSITIVE")
        self.assertEqual(a["cohens_kappa"],F(3,4))
        self.assertNotEqual(a["observed_coder_A_positive_marginal"],a["observed_coder_B_positive_marginal"])
    def test_opposition(self):
        self.assertEqual(observed_agreement("OPPOSING_CODERS")["cohens_kappa"],-ONE)
    def test_nominal_alpha_finite(self):
        a=observed_agreement("BALANCED_INDEPENDENT_RANDOM")
        self.assertNotEqual(a["nominal_krippendorff_alpha_pair_complete"],a["cohens_kappa"])
    def test_bad_world(self):
        with self.assertRaises(ValueError):sources("UNKNOWN")

def _case(world,kind):
    def t(self):
        data=sources(world)
        if kind=="mass":
            self.assertEqual(sum((r["original_structural_source_probability"] for r in data),ZERO),ONE)
        elif kind=="unique":
            self.assertEqual(len({tuple(r["oracle_original_"+k] for k in SOURCE_NAMES) for r in data}),256)
        elif kind=="joint":
            self.assertEqual(observed_joint(world),{k:F(v,256) for k,v in independent_observed_counts(world).items()})
        elif kind=="selected":
            self.assertEqual(observed_agreement(world)["selected_source_units"],sum(x["observed_pair_available"] for x in data))
        elif kind=="kappa":
            n,po,pe,k=independent_agreement(world)
            a=observed_agreement(world)
            self.assertEqual((n,po,pe,k),(a["selected_source_units"],a["observed_pair_agreement"],
                                        a["expected_independent_marginal_agreement"],a["cohens_kappa"]))
        elif kind=="alpha":
            self.assertGreater(observed_agreement(world)["nominal_alpha_finite_without_replacement_expected_disagreement"],ZERO)
        elif kind=="oracle":
            self.assertTrue(all(ZERO<=v<=ONE for v in oracle_accuracy(world)))
        elif kind=="result":
            self.assertEqual(world_result(world)["full_original_exogenous_sources"],256)
        else:raise AssertionError("unknown test")
    return t

for _w in WORLDS:
    for _kind in ("mass","unique","joint","selected","kappa","alpha","oracle","result"):
        setattr(Tests,f"test_{_w.lower()}_{_kind}",_case(_w,_kind))

if __name__=="__main__":
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true")
    g.add_argument("--emit",action="store_true")
    z=p.parse_args()
    if z.test:unittest.main(argv=["r240"],verbosity=2)
    else:print(json.dumps(generate(),indent=2))
