#!/usr/bin/env python3
"""R239 finite crisp QCA source enumeration and minimal configuration covers.

Nine frozen artificial SCMs, including logically unobserved configurations,
contradictions, and observationally identical sufficiency vs intervention
effects. Source, observed and oracle views remain separate.
"""
from __future__ import annotations
import argparse, csv, hashlib, itertools, json, unittest
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path

HERE=Path(__file__).resolve().parent
FREEZE="af9ead7125b7a46a7dffc79b1f080ff6a69bc94d"
ZERO=F(0)
ONE=F(1)
BITS=(0,1)
CONFIGS=tuple(itertools.product(BITS,repeat=3))
CUBES=tuple(itertools.product((-1,0,1),repeat=3))
WORLDS=(
 "AND_AB","OR_AB","EQUIFINAL_AB_OR_NOTA_C",
 "CONTRADICTORY_A_XOR_U","LIMITED_A_AND_B","LIMITED_UNSEEN_BRANCH",
 "ALIAS_A_CAUSAL","ALIAS_U_CONFOUNDED","NEGATED_A_AND_C"
)
LIMITED_WORLDS={"LIMITED_A_AND_B","LIMITED_UNSEEN_BRANCH"}
ALIAS_WORLDS={"ALIAS_A_CAUSAL","ALIAS_U_CONFOUNDED"}

def mechanism(world,a,b,c,u):
    if world not in WORLDS:raise ValueError("unknown QCA world")
    if any(x not in BITS for x in (a,b,c,u)):raise ValueError("QCA source not binary")
    if world in ("AND_AB","LIMITED_A_AND_B"):return a & b
    if world=="OR_AB":return a | b
    if world in ("EQUIFINAL_AB_OR_NOTA_C","LIMITED_UNSEEN_BRANCH"):
        return (a & b) | ((1-a)&c)
    if world=="CONTRADICTORY_A_XOR_U":return a ^ u
    if world=="ALIAS_A_CAUSAL":return a
    if world=="ALIAS_U_CONFOUNDED":return u
    if world=="NEGATED_A_AND_C":return (1-a)&c
    raise AssertionError("missing frozen world")

def atom(world,x,b,c,u):
    if world not in WORLDS or any(z not in BITS for z in (x,b,c,u)):
        raise ValueError("invalid frozen original exogenous atom")
    a=u if world in ALIAS_WORLDS else x
    s=int(not(world in LIMITED_WORLDS and a==0 and c==1))
    y=mechanism(world,a,b,c,u)
    return dict(
        world=world,oracle_original_X=x,oracle_original_B=b,
        oracle_original_C=c,oracle_original_U=u,
        observed_A=a,observed_B=b,observed_C=c,
        observed_case_selected=s,observed_selected_Y=y if s else -1,
        oracle_actual_Y=y,
        oracle_doA0_Y=mechanism(world,0,b,c,u),
        oracle_doA1_Y=mechanism(world,1,b,c,u),
        original_source_probability=F(1,16)
    )

def sources(world):
    if world not in WORLDS:raise ValueError("unfrozen QCA world")
    out=tuple(atom(world,*v) for v in itertools.product(BITS,repeat=4))
    if len(out)!=16 or sum((r["original_source_probability"] for r in out),ZERO)!=ONE:
        raise AssertionError("full QCA source universe invalid")
    return out

def table(world):
    """Truth table on selected cases only; no oracle U or counterfactuals."""
    rows=sources(world)
    result=[]
    for config in CONFIGS:
        matched=[r for r in rows if r["observed_case_selected"] and
            tuple(r[f"observed_{k}"] for k in "ABC")==config]
        pos=sum(r["observed_selected_Y"] for r in matched)
        neg=len(matched)-pos
        assert all(r["observed_selected_Y"] in BITS for r in matched)
        consistency=F(pos,len(matched)) if matched else None
        state=("remainder" if not matched else "positive" if pos and not neg
               else "negative" if neg and not pos else "contradictory")
        result.append(dict(abc=config,selected_original_atoms=len(matched),
                           positive_original_atoms=pos,negative_original_atoms=neg,
                           consistency=consistency,state=state))
    return tuple(result)

def joint_observable(world):
    """Observed dataset includes selection flag and -1 for missing outcomes."""
    counts=defaultdict(F)
    for r in sources(world):
        key=(r["observed_A"],r["observed_B"],r["observed_C"],
             r["observed_case_selected"],r["observed_selected_Y"])
        counts[key]+=r["original_source_probability"]
    return dict(sorted(counts.items()))

def oracle_average_doA_effect(world):
    return sum((r["original_source_probability"]*(r["oracle_doA1_Y"]-r["oracle_doA0_Y"])
                for r in sources(world)),ZERO)

def independent_doA_effect(world):
    """Independent analytical method: fresh structural Y(doA) for 8 (B,C,U)."""
    return sum((F(mechanism(world,1,b,c,u)-mechanism(world,0,b,c,u),8)
                for b,c,u in itertools.product(BITS,repeat=3)),ZERO)

def cube_contains(cube,config):
    return all(lit==-1 or lit==v for lit,v in zip(cube,config))

def cube_covered(cube):
    return frozenset(c for c in CONFIGS if cube_contains(cube,c))

def solution_score(terms):
    return (len(terms),sum(sum(x!=-1 for x in term) for term in terms),terms)

def minimal_dnf(rows,allow_remainders=False):
    positives={r["abc"] for r in rows if r["state"]=="positive"}
    negatives={r["abc"] for r in rows if r["state"] in ("negative","contradictory")}
    remainders={r["abc"] for r in rows if r["state"]=="remainder"}
    if not positives:return ()
    # All 3^3 cubes are exhaustively examined. Dynamic-program minimum cover
    # by 2^3-bit positive-support mask; no float or heuristic.
    candidates=[]
    for cube in CUBES:
        cover=cube_covered(cube)
        if cover & negatives or (not allow_remainders and cover & remainders):continue
        overlap=cover&positives
        if overlap:
            mask=sum(1<<CONFIGS.index(c) for c in overlap)
            candidates.append((cube,mask))
    target=sum(1<<CONFIGS.index(c) for c in positives)
    dp={0:()}
    for cube,mask in candidates:
        snapshot=list(dp.items())
        for prior,oldterms in snapshot:
            nextmask=prior|mask
            newterms=tuple(sorted(oldterms+(cube,)))
            if nextmask not in dp or solution_score(newterms)<solution_score(dp[nextmask]):
                dp[nextmask]=newterms
    if target not in dp:raise AssertionError("minimum conservative DNF impossible for observed positives")
    return dp[target]

def eval_dnf(terms,config):
    return int(any(cube_contains(c,config) for c in terms))

def certified_dnf(world,allow_remainders=False):
    rows=table(world)
    terms=minimal_dnf(rows,allow_remainders)
    for row in rows:
        predicted=eval_dnf(terms,row["abc"])
        if row["state"]=="positive" and predicted!=1:
            raise AssertionError("minimal DNF misses observed positive configuration")
        if row["state"] in ("negative","contradictory") and predicted:
            raise AssertionError("minimal DNF includes observed negative or contradictory cases")
        if not allow_remainders and row["state"]=="remainder" and predicted:
            raise AssertionError("conservative DNF uses unobserved remainder")
    return terms

def set_consistency(world,cube,purpose):
    if cube not in CUBES or purpose not in ("sufficiency","necessity"):
        raise ValueError("invalid QCA formula consistency request")
    rows=[r for r in sources(world) if r["observed_case_selected"]]
    if purpose=="sufficiency":
        antecedents=[r for r in rows if cube_contains(cube,tuple(r[f"observed_{k}"] for k in "ABC"))]
        return F(sum(r["observed_selected_Y"] for r in antecedents),len(antecedents)) if antecedents else None
    outcome=[r for r in rows if r["observed_selected_Y"]==1]
    return F(sum(cube_contains(cube,tuple(r[f"observed_{k}"] for k in "ABC")) for r in outcome),
             len(outcome)) if outcome else None

def freeze_aliases():
    for a,b in (("LIMITED_A_AND_B","LIMITED_UNSEEN_BRANCH"),
                ("ALIAS_A_CAUSAL","ALIAS_U_CONFOUNDED")):
        x=sources(a);y=sources(b)
        for l,r in zip(x,y):
            if any(l[k]!=r[k] for k in ("observed_A","observed_B","observed_C",
                    "observed_case_selected","observed_selected_Y")):
                raise AssertionError("finite QCA observational source alias broken")
        if joint_observable(a)!=joint_observable(b):
            raise AssertionError("finite QCA full observed joint not identical")
    assert oracle_average_doA_effect("ALIAS_A_CAUSAL")==ONE
    assert oracle_average_doA_effect("ALIAS_U_CONFOUNDED")==ZERO
    # Limited universes have different outcome configurations outside selection.
    xa=sources("LIMITED_A_AND_B");xb=sources("LIMITED_UNSEEN_BRANCH")
    assert any(x["oracle_actual_Y"]!=y["oracle_actual_Y"] for x,y in zip(xa,xb))
    assert all(x["oracle_actual_Y"]==y["oracle_actual_Y"] for x,y in zip(xa,xb) if x["observed_case_selected"])
    return True

def world_result(world):
    rows=table(world)
    for r in rows:
        if r["state"]=="remainder":
            assert r["selected_original_atoms"]==0 and r["consistency"] is None
    conservative=certified_dnf(world,False)
    parsimonious=certified_dnf(world,True)
    oracle=oracle_average_doA_effect(world)
    if oracle!=independent_doA_effect(world):
        raise AssertionError("direct source intervention and independent SCM effect disagree")
    if world=="CONTRADICTORY_A_XOR_U":
        assert all(r["state"]=="contradictory" and r["consistency"]==F(1,2) for r in rows)
        assert conservative==parsimonious==()
    if world in LIMITED_WORLDS:
        assert sum(r["state"]=="remainder" for r in rows)==2
    if world in ALIAS_WORLDS:
        assert set_consistency(world,(1,-1,-1),"sufficiency")==ONE
        assert set_consistency(world,(1,-1,-1),"necessity")==ONE
    return dict(
        world=world,complete_original_exogenous_atoms=16,
        original_source_mass="1",
        selected_source_atoms=sum(r["selected_original_atoms"] for r in rows),
        logical_remainder_configurations=sum(r["state"]=="remainder" for r in rows),
        contradictory_configurations=sum(r["state"]=="contradictory" for r in rows),
        complete_truth_table=[
            {**{k:(str(v) if isinstance(v,F) else v) for k,v in r.items()},
             "abc":"".join(map(str,r["abc"]))} for r in rows
        ],
        conservative_dnf_cubes=[list(x) for x in conservative],
        parsimonious_dnf_cubes=[list(x) for x in parsimonious],
        observational_sufficiency_A=str(set_consistency(world,(1,-1,-1),"sufficiency")) if set_consistency(world,(1,-1,-1),"sufficiency") is not None else None,
        observational_necessity_A=str(set_consistency(world,(1,-1,-1),"necessity")) if set_consistency(world,(1,-1,-1),"necessity") is not None else None,
        observational_sufficiency_A_and_B=str(set_consistency(world,(1,1,-1),"sufficiency")) if set_consistency(world,(1,1,-1),"sufficiency") is not None else None,
        oracle_doA1_minus_doA0_population_effect=str(oracle),
        full_observed_joint_with_explicit_selection_missingness={
            "".join(str(z) for z in k):str(v) for k,v in joint_observable(world).items()
        }
    )

def generate():
    freeze_aliases()
    items=[world_result(w) for w in WORLDS]
    results=dict(research_id="R239",original_catalogue_id="10-013",
        prescore_freeze_commit=FREEZE,scientific_scope="FINITE_ARTIFICIAL_E1_CRISP_QCA_CONFIGURATION_AND_IDENTIFICATION",
        frozen_worlds=9,original_exogenous_source_atoms=144,
        full_observed_alias_pairs=[
            ["LIMITED_A_AND_B","LIMITED_UNSEEN_BRANCH"],
            ["ALIAS_A_CAUSAL","ALIAS_U_CONFOUNDED"]
        ],independent_do_intervention_truth_verified=True,
        conservative_vs_parsimonious_unobserved_remainder_separated=True,
        new_real_human_E2=0,new_real_historical_E3=0,
        R073="FROZEN",PESEN_v0_1="FROZEN",
        world_results=items)
    out=HERE/"R239_ALL_144_ORIGINAL_CONFIGURATION_CAUSAL_SOURCES.csv"
    fields=list(sources("AND_AB")[0])
    with out.open("w",newline="",encoding="utf-8") as f:
        wr=csv.DictWriter(f,fieldnames=fields,lineterminator="\n")
        wr.writeheader()
        for world in WORLDS:
            for r in sources(world):wr.writerow({k:str(r[k]) for k in fields})
    path=HERE/"R239_EXACT_RESULTS.json"
    path.write_text(json.dumps(results,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    rec=dict(research_id="R239",original_catalogue_id="10-013",
        frozen_worlds=9,all_complete_source_atoms=144,
        complete_truth_table_all_eight_conditions_per_world=True,
        conservative_and_parsimonious_cube_certificates=True,
        full_observation_alias_pairs_verified=2,
        source_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),
        results_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
        new_real_human_E2=0,new_real_historical_E3=0)
    (HERE/"R239_FINAL_MACHINE_ACCEPTANCE.json").write_text(json.dumps(rec,indent=2)+"\n",encoding="utf-8")
    return rec

class Tests(unittest.TestCase):
    def test_world_count(self):self.assertEqual(len(WORLDS),9)
    def test_full_source_count(self):self.assertEqual(sum(len(sources(w)) for w in WORLDS),144)
    def test_full_source_aliases(self):self.assertTrue(freeze_aliases())
    def test_and_minimization(self):
        self.assertEqual(minimal_dnf(table("AND_AB")),((-1,1,1),) if False else ((1,1,-1),))
    def test_or_minimization(self):
        self.assertEqual(minimal_dnf(table("OR_AB")),((-1,1,-1),(1,-1,-1)))
    def test_equifinality(self):
        self.assertEqual(minimal_dnf(table("EQUIFINAL_AB_OR_NOTA_C")),((-1,1,1),(0,-1,1),(1,1,-1)) if False else ((0,-1,1),(1,1,-1)))
    def test_all_configurations_contradictory(self):
        self.assertTrue(all(r["consistency"]==F(1,2) for r in table("CONTRADICTORY_A_XOR_U")))
    def test_limiting_remainder(self):
        self.assertEqual(sum(r["state"]=="remainder" for r in table("LIMITED_A_AND_B")),2)
    def test_causes_not_from_sufficiency(self):
        self.assertEqual(oracle_average_doA_effect("ALIAS_A_CAUSAL"),ONE)
        self.assertEqual(oracle_average_doA_effect("ALIAS_U_CONFOUNDED"),ZERO)
    def test_missing_not_negative(self):
        self.assertTrue(all(r["negative_original_atoms"]==0 and r["positive_original_atoms"]==0
                            for r in table("LIMITED_UNSEEN_BRANCH") if r["state"]=="remainder"))
    def test_dnf_matches_world(self):
        for w in WORLDS:
            certified_dnf(w,False);certified_dnf(w,True)
    def test_negation_world(self):
        self.assertEqual(minimal_dnf(table("NEGATED_A_AND_C")),((0,-1,1),))
    def test_unknown(self):
        with self.assertRaises(ValueError):sources("invalid")

def _case(world,kind):
    def t(self):
        rows=sources(world)
        if kind=="mass":
            self.assertEqual(sum((r["original_source_probability"] for r in rows),ZERO),ONE)
        elif kind=="source_unique":
            self.assertEqual(len({(r["oracle_original_X"],r["oracle_original_B"],r["oracle_original_C"],r["oracle_original_U"]) for r in rows}),16)
        elif kind=="table_eight":
            self.assertEqual(len(table(world)),8)
        elif kind=="table_count":
            self.assertEqual(sum(r["selected_original_atoms"] for r in table(world)),sum(r["observed_case_selected"] for r in rows))
        elif kind=="truth":
            self.assertEqual(oracle_average_doA_effect(world),independent_doA_effect(world))
        elif kind=="dnf":
            certified_dnf(world,False);certified_dnf(world,True)
        elif kind=="joint":
            self.assertEqual(sum(joint_observable(world).values(),ZERO),ONE)
        elif kind=="report":
            self.assertEqual(world_result(world)["complete_original_exogenous_atoms"],16)
        else:raise AssertionError("unknown test")
    return t
for _w in WORLDS:
    for _kind in ("mass","source_unique","table_eight","table_count","truth","dnf","joint","report"):
        setattr(Tests,"test_"+_w.lower()+"_"+_kind,_case(_w,_kind))

if __name__=="__main__":
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true")
    g.add_argument("--emit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["r239"],verbosity=2)
    else:print(json.dumps(generate(),indent=2))
