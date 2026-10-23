#!/usr/bin/env python3
"""R247 exact finite Galton-Watson and correlated offspring tree worlds.

One founder, seven potential binary-tree parent nodes, four observed
generations (Z0..Z3). Eight independent source bits (U+B0..B6) give 256
complete artificial source types per world, 2304 total. Independent
offspring-PGF polynomial composition audits ONLY true IID Galton-Watson
offspring worlds; shared-environment worlds explicitly do not inherit it.
"""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from fractions import Fraction as F
from functools import lru_cache
from collections import defaultdict
from pathlib import Path

HERE=Path(__file__).resolve().parent
FREEZE="2cdd09aa479b168c1072ce32f1fbea89f39c56e2"
ZERO=F(0);ONE=F(1)
BITS=(0,1)
EXOGENOUS=tuple(itertools.product(BITS,repeat=8))
GENERATIONS=(0,1,2,3)
WORLDS=(
 "IID_FAIR_0_OR_2","IID_SUBCRITICAL_0_OR_1","IID_SUPERCRITICAL_1_OR_2",
 "DETERMINISTIC_ONE","DETERMINISTIC_TWO","GLOBAL_SHARED_ENVIRONMENT",
 "GENERATION_SHARED_SHOCK","SIBLING_ANTICORRELATED_OFFSPRING",
 "STATIC_HIDDEN_TREE_SENSOR_ALIAS"
)
TRUE_IID=(
 "IID_FAIR_0_OR_2","IID_SUBCRITICAL_0_OR_1","IID_SUPERCRITICAL_1_OR_2",
 "DETERMINISTIC_ONE","DETERMINISTIC_TWO")
OBS_IID_PGF=TRUE_IID+("STATIC_HIDDEN_TREE_SENSOR_ALIAS",)

def validate_world(world):
    if world not in WORLDS:raise ValueError("unfrozen branching world")

def potential_offspring(world,bits):
    validate_world(world)
    if len(bits)!=8 or any(x not in BITS for x in bits):
        raise ValueError("expected eight frozen independent source bits")
    u=bits[0]
    b=bits[1:]
    if world in ("IID_FAIR_0_OR_2","STATIC_HIDDEN_TREE_SENSOR_ALIAS"):
        return tuple(2*x for x in b)
    if world=="IID_SUBCRITICAL_0_OR_1":return tuple(b)
    if world=="IID_SUPERCRITICAL_1_OR_2":return tuple(1+x for x in b)
    if world=="DETERMINISTIC_ONE":return (1,)*7
    if world=="DETERMINISTIC_TWO":return (2,)*7
    if world=="GLOBAL_SHARED_ENVIRONMENT":return (2*u,)*7
    if world=="GENERATION_SHARED_SHOCK":
        return (2*b[0],2*b[1],2*b[1],2*b[3],2*b[3],2*b[3],2*b[3])
    if world=="SIBLING_ANTICORRELATED_OFFSPRING":
        return (2*b[0],2*b[1],2*(1-b[1]),2*b[3],2*b[4],2*b[5],2*b[6])
    raise AssertionError("world missing")

def generate_four_generations_from_offspring(offspring):
    if len(offspring)!=7 or any(x not in (0,1,2) for x in offspring):
        raise ValueError("not a valid seven-node tree")
    active1=[j for j in (1,2) if j-1<offspring[0]]
    active2=[]
    for parent in active1:
        for k in range(offspring[parent]):
            active2.append(2*parent+1+k)
    if any(x not in (3,4,5,6) for x in active2):
        raise AssertionError("invalid potential depth2 ancestry")
    return (1,len(active1),len(active2),sum(offspring[x] for x in active2))

def observed_path_for_source(world,bits):
    offspring=potential_offspring(world,bits)
    y=generate_four_generations_from_offspring(offspring)
    hidden=(1,0,0,0) if world=="STATIC_HIDDEN_TREE_SENSOR_ALIAS" else y
    return y,hidden,offspring

def source_atom(world,bits):
    y,h,offspring=observed_path_for_source(world,bits)
    r={"world":world,"oracle_hidden_environment_U":bits[0]}
    for j in range(7):
        r["oracle_original_node_bit_B"+str(j)]=bits[j+1]
        r["oracle_potential_parent_offspring_K"+str(j)]=offspring[j]
    for gen in GENERATIONS:
        r["observed_generation_size_Y"+str(gen)]=y[gen]
        r["oracle_true_hidden_generation_H"+str(gen)]=h[gen]
    r["original_complete_source_probability"]=F(1,256)
    return r

@lru_cache(maxsize=None)
def sources(world):
    validate_world(world)
    rows=tuple(source_atom(world,b) for b in EXOGENOUS)
    if len(rows)!=256 or sum((r["original_complete_source_probability"] for r in rows),ZERO)!=ONE:
        raise AssertionError("complete eight-bit family source space missing")
    if any(r["original_complete_source_probability"]<=0 for r in rows):
        raise AssertionError("frozen positive exogenous source unexpectedly zero")
    return rows

@lru_cache(maxsize=None)
def observed_joint(world):
    d=defaultdict(F)
    for r in sources(world):
        path=tuple(r["observed_generation_size_Y"+str(g)] for g in GENERATIONS)
        d[path]+=r["original_complete_source_probability"]
    return dict(sorted(d.items()))

def generation_distribution(world,n):
    if n not in GENERATIONS:raise ValueError("not frozen 3-generation horizon")
    out=defaultdict(F)
    for path,mass in observed_joint(world).items():
        out[path[n]]+=mass
    return dict(sorted(out.items()))

def source_expected_generation(world,n):
    return sum((F(size)*p for size,p in generation_distribution(world,n).items()),ZERO)

def source_survival_probability(world,n):
    return sum((p for size,p in generation_distribution(world,n).items() if size>0),ZERO)

def offspring_pgf_coefficients(world):
    if world not in OBS_IID_PGF:raise ValueError("non-IID correlated-world PGF factorization invalid")
    if world in ("IID_FAIR_0_OR_2","STATIC_HIDDEN_TREE_SENSOR_ALIAS"):
        return (F(1,2),ZERO,F(1,2))
    if world=="IID_SUBCRITICAL_0_OR_1":return (F(1,2),F(1,2),ZERO)
    if world=="IID_SUPERCRITICAL_1_OR_2":return (ZERO,F(1,2),F(1,2))
    if world=="DETERMINISTIC_ONE":return (ZERO,ONE,ZERO)
    if world=="DETERMINISTIC_TWO":return (ZERO,ZERO,ONE)
    raise AssertionError("missing PGF")

def poly_trim(a):
    t=list(a)
    while len(t)>1 and t[-1]==ZERO:t.pop()
    return tuple(t)
def poly_add(a,b):
    n=max(len(a),len(b))
    return poly_trim(tuple((a[i] if i<len(a) else ZERO)+(b[i] if i<len(b) else ZERO) for i in range(n)))
def poly_scale(a,c):return poly_trim(tuple(c*v for v in a))
def poly_mul(a,b):
    out=[ZERO]*(len(a)+len(b)-1)
    for i,v in enumerate(a):
        for j,w in enumerate(b):out[i+j]+=v*w
    return poly_trim(out)
def pgf_generation_distribution(world,n):
    """Independent exact f composed n times; NEVER enumerate original B bits."""
    if n not in GENERATIONS:raise ValueError("outside finite generation")
    p0,p1,p2=offspring_pgf_coefficients(world)
    pol=(ZERO,ONE)  # identity s, Z0=1
    for _ in range(n):
        square=poly_mul(pol,pol)
        pol=poly_add((p0,),poly_add(poly_scale(pol,p1),poly_scale(square,p2)))
    if sum(pol,ZERO)!=ONE:raise AssertionError("PGF not normalized")
    return {i:v for i,v in enumerate(pol) if v>0}

def independent_pgf_expected_generation(world,n):
    return sum((F(k)*v for k,v in pgf_generation_distribution(world,n).items()),ZERO)

def world_claims():
    base="IID_FAIR_0_OR_2";alias="STATIC_HIDDEN_TREE_SENSOR_ALIAS"
    if observed_joint(base)!=observed_joint(alias):
        raise AssertionError("sensor alias observation populations not identical")
    for bits in EXOGENOUS:
        b=observed_path_for_source(base,bits)[0]
        reported,hidden,_=observed_path_for_source(alias,bits)
        if reported!=b or hidden!=(1,0,0,0):
            raise AssertionError("sensor alias not sourcewise")
    locked={
      "IID_FAIR_0_OR_2":(ONE,F(39,128)),
      "IID_SUBCRITICAL_0_OR_1":(F(1,8),F(1,8)),
      "IID_SUPERCRITICAL_1_OR_2":(F(27,8),ONE),
      "DETERMINISTIC_ONE":(ONE,ONE),
      "DETERMINISTIC_TWO":(F(8),ONE),
      "GLOBAL_SHARED_ENVIRONMENT":(F(4),F(1,2)),
      "GENERATION_SHARED_SHOCK":(ONE,F(1,8)),
      "SIBLING_ANTICORRELATED_OFFSPRING":(ONE,F(3,8)),
      "STATIC_HIDDEN_TREE_SENSOR_ALIAS":(ONE,F(39,128))
    }
    for name,expected in locked.items():
        found=(source_expected_generation(name,3),source_survival_probability(name,3))
        if found!=expected:
            raise AssertionError(f"{name}: source exact mean/survival {found} not frozen {expected}")
    if generation_distribution(base,3).get(0)!=F(89,128):
        raise AssertionError("critical finite PGF P(Z3=0) should be 89/128")
    for world in OBS_IID_PGF:
        pgf=offspring_pgf_coefficients(world)
        mu=pgf[1]+2*pgf[2]
        for n in GENERATIONS:
            if pgf_generation_distribution(world,n)!=generation_distribution(world,n):
                raise AssertionError("independent PGF vs full tree sources differ")
            if independent_pgf_expected_generation(world,n)!=mu**n:
                raise AssertionError("IID branching mean does not follow mu^n")
    return True

def world_result(world):
    joint=observed_joint(world)
    means=tuple(source_expected_generation(world,g) for g in GENERATIONS)
    surviving=tuple(source_survival_probability(world,g) for g in GENERATIONS)
    if sum(joint.values(),ZERO)!=ONE:raise AssertionError("observed tree path normalization")
    if world in OBS_IID_PGF:
        for n in GENERATIONS:
            if pgf_generation_distribution(world,n)!=generation_distribution(world,n):
                raise AssertionError("whole tree law differs independent iid generating functions")
    else:
        if world=="GLOBAL_SHARED_ENVIRONMENT":
            assert means[3]==F(4) and surviving[3]==F(1,2)
        if world=="GENERATION_SHARED_SHOCK":
            assert means[3]==ONE and surviving[3]==F(1,8)
        if world=="SIBLING_ANTICORRELATED_OFFSPRING":
            assert means[3]==ONE and surviving[3]==F(3,8)
    return dict(
      world=world,complete_original_eight_bit_tree_source_atoms=256,
      observed_expected_generation_sizes_by_generation=[str(v) for v in means],
      observed_survival_probabilities_by_generation=[str(v) for v in surviving],
      observed_generation3_distribution={str(k):str(v) for k,v in generation_distribution(world,3).items()},
      observed_full_four_generation_family_path_joint={
          ",".join(map(str,seq)):str(p) for seq,p in joint.items()},
      true_hidden_generation3_size_by_complete_exogenous_source=[
          r["oracle_true_hidden_generation_H3"] for r in sources(world)],
      independent_classical_iid_offspring_PGF_certified=(world in OBS_IID_PGF),
      correlated_shared_parent_offspring_not_assumed_iid=(world not in OBS_IID_PGF)
    )

def generate():
    world_claims()
    result=dict(
       research_id="R247",original_catalogue_id="11-007",
       prescore_freeze_commit=FREEZE,
       scientific_scope="FINITE_ARTIFICIAL_E1_GALTON_WATSON_OFFSPRING_INDEPENDENCE_AND_CORRELATED_FAMILY_SHOCKS",
       frozen_worlds=9,complete_eight_bit_original_tree_source_atoms=2304,
       four_generation_horizon_including_founder=4,
       independent_classical_PGF_for_true_iid_generating_worlds=True,
       independent_classical_PGF_for_observation_only_sensor_alias=True,
       forbidden_to_apply_iid_PGF_to_correlated_offspring_worlds=True,
       new_real_human_E2=0,new_real_historical_E3=0,
       R073="FROZEN",PESEN_v0_1="FROZEN",
       world_results=[world_result(w) for w in WORLDS]
    )
    src=HERE/"R247_ALL_2304_ORIGINAL_BINARY_TREE_FAMILY_SOURCES.csv"
    fields=list(sources("IID_FAIR_0_OR_2")[0])
    with src.open("w",encoding="utf-8",newline="") as f:
        wr=csv.DictWriter(f,fieldnames=fields,lineterminator="\n")
        wr.writeheader()
        for name in WORLDS:
            for r in sources(name):wr.writerow({k:str(r[k]) for k in fields})
    res=HERE/"R247_EXACT_RESULTS.json"
    res.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    receipt=dict(
       research_id="R247",original_catalogue_id="11-007",
       frozen_worlds=9,complete_original_eight_bit_family_atoms=2304,
       finite_critical_generation3_survival="39/128",
       actual_correlated_vs_iid_offspring_predictions_separated=True,
       full_tree_source_vs_iid_polynomial_PGF_parity=True,
       sourcewise_hidden_static_tree_observation_alias=True,
       source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),
       results_sha256=hashlib.sha256(res.read_bytes()).hexdigest(),
       new_real_human_E2=0,new_real_historical_E3=0)
    (HERE/"R247_FINAL_MACHINE_ACCEPTANCE.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_nine_worlds(self):self.assertEqual(len(WORLDS),9)
    def test_all_2304(self):self.assertEqual(sum(len(sources(w)) for w in WORLDS),2304)
    def test_all_frozen_mean_survival(self):self.assertTrue(world_claims())
    def test_critical_3generation_survival(self):
        self.assertEqual(source_survival_probability("IID_FAIR_0_OR_2",3),F(39,128))
    def test_iid_offspring_mean_power(self):
        self.assertEqual(independent_pgf_expected_generation("IID_SUPERCRITICAL_1_OR_2",3),F(27,8))
    def test_global_environment_not_independent(self):
        self.assertEqual(source_expected_generation("GLOBAL_SHARED_ENVIRONMENT",3),F(4))
    def test_generation_shock_same_mean_different_survival(self):
        self.assertEqual(source_expected_generation("GENERATION_SHARED_SHOCK",3),ONE)
        self.assertEqual(source_survival_probability("GENERATION_SHARED_SHOCK",3),F(1,8))
    def test_anticorrelation_survival(self):
        self.assertEqual(source_survival_probability("SIBLING_ANTICORRELATED_OFFSPRING",3),F(3,8))
    def test_true_hidden_static(self):
        self.assertTrue(all(r["oracle_true_hidden_generation_H3"]==0 for r in sources("STATIC_HIDDEN_TREE_SENSOR_ALIAS")))
    def test_gw_pgf_not_allowed_for_correlated(self):
        with self.assertRaises(ValueError):pgf_generation_distribution("GLOBAL_SHARED_ENVIRONMENT",3)
    def test_static_alias_sourcewise(self):
        self.assertEqual(observed_joint("IID_FAIR_0_OR_2"),observed_joint("STATIC_HIDDEN_TREE_SENSOR_ALIAS"))
    def test_8_max_generation(self):
        self.assertEqual(max(generation_distribution("DETERMINISTIC_TWO",3)),8)

def _case(world,kind):
    def t(self):
        data=sources(world)
        if kind=="mass":
            self.assertEqual(sum((r["original_complete_source_probability"] for r in data),ZERO),ONE)
        elif kind=="unique":
            keys=("oracle_hidden_environment_U",)+tuple("oracle_original_node_bit_B"+str(j) for j in range(7))
            self.assertEqual(len({tuple(r[k] for k in keys) for r in data}),256)
        elif kind=="positive":
            self.assertTrue(all(r["original_complete_source_probability"]>0 for r in data))
        elif kind=="observed_joint":
            self.assertEqual(sum(observed_joint(world).values(),ZERO),ONE)
        elif kind=="source_generations":
            for r in data:
                self.assertEqual(r["observed_generation_size_Y0"],1)
                self.assertTrue(all(0<=r["observed_generation_size_Y"+str(g)]<=2**g for g in GENERATIONS))
        elif kind=="critical_formula":
            if world in OBS_IID_PGF:
                for g in GENERATIONS:
                    self.assertEqual(generation_distribution(world,g),pgf_generation_distribution(world,g))
        elif kind=="hidden_stat":
            self.assertGreaterEqual(source_survival_probability(world,3),ZERO)
            self.assertLessEqual(source_survival_probability(world,3),ONE)
        elif kind=="report":
            self.assertEqual(world_result(world)["complete_original_eight_bit_tree_source_atoms"],256)
        else:raise AssertionError("not frozen test")
    return t
for _w in WORLDS:
    for _kind in ("mass","unique","positive","observed_joint","source_generations",
                  "critical_formula","hidden_stat","report"):
        setattr(Tests,"test_"+_w.lower()+"_"+_kind,_case(_w,_kind))

if __name__=="__main__":
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true")
    g.add_argument("--emit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["r247"],verbosity=2)
    else:print(json.dumps(generate(),indent=2))
