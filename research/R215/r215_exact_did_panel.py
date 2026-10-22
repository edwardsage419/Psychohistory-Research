#!/usr/bin/env python3
"""R215 exact 2x2 Difference in Differences, 12 prescored artificial worlds.

4 fixed units, 2 times, 2 treated at post only; 256 independent unit-period
noise patterns and 16 persistent-within-person noise patterns per true world.
All counterfactual baseline outcomes are artificial ORACLE AUDIT ONLY.
DiD and post-only estimates read only realized eight observed values.
"""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from fractions import Fraction as F
from pathlib import Path
Z=F(0);O=F(1);HERE=Path(__file__).resolve().parent
WORLDS=(
"VALID_CONSTANT_TWO","VALID_LEVEL_GAP","VALID_COMMON_SHOCK",
"VALID_HETEROGENEOUS","VALID_NULL","VALID_NEGATIVE",
"NONPARALLEL_TREATED_UP","NONPARALLEL_TREATED_DOWN",
"CONTROL_SPILLOVER","ANTICIPATION",
"SIMULTANEOUS_TREATED_SHOCK_NO_CAUSAL","HETEROGENEOUS_TRENDS_BALANCED",
)
SCHEMES=("CELL_INDEPENDENT","UNIT_PERSISTENT")
TREATED=(2,3);CONTROL=(0,1)
def params(world):
    if world not in WORLDS:raise ValueError("unknown frozen world")
    p={"baseline":(0,1,2,3),"trends":(1,1,1,1),"tau":(2,2),
       "q_post":0,"control_spill":0,"anticipation":0,"treated_coincident":0}
    if world=="VALID_LEVEL_GAP":p["baseline"]=(0,1,10,11)
    if world=="VALID_COMMON_SHOCK":p["q_post"]=5
    if world=="VALID_HETEROGENEOUS":p["tau"]=(1,3)
    if world=="VALID_NULL":p["tau"]=(0,0)
    if world=="VALID_NEGATIVE":p["tau"]=(-2,-2)
    if world=="NONPARALLEL_TREATED_UP":p["trends"]=(1,1,3,3)
    if world=="NONPARALLEL_TREATED_DOWN":p["trends"]=(1,1,0,0)
    if world=="CONTROL_SPILLOVER":p["control_spill"]=1
    if world=="ANTICIPATION":p["anticipation"]=1
    if world=="SIMULTANEOUS_TREATED_SHOCK_NO_CAUSAL":
        p["tau"]=(0,0);p["treated_coincident"]=2
    if world=="HETEROGENEOUS_TRENDS_BALANCED":p["trends"]=(0,2,0,2)
    return p
def latent_panel(world,eps):
    if len(eps)!=8 or any(e not in (-1,1) for e in eps):raise ValueError("eight +-1 noise values needed")
    p=params(world);base=[];observed=[]
    for i in range(4):
        for t in (0,1):
            y=F(p["baseline"][i]+p["trends"][i]*t+
                p["q_post"]*t+int(i in TREATED and t==1)*p["treated_coincident"]+eps[2*i+t])
            obs=y+int(i in TREATED and t==1)*p["tau"][i-2]
            if i in TREATED and t==0:obs+=p["anticipation"]
            if i in CONTROL and t==1:obs+=p["control_spill"]
            base.append(y);observed.append(obs)
    return tuple(base),tuple(observed)
def original_noise(scheme):
    if scheme=="CELL_INDEPENDENT":
        for bits in itertools.product((-1,1),repeat=8):
            yield bits,F(1,256),bits
    elif scheme=="UNIT_PERSISTENT":
        for bits in itertools.product((-1,1),repeat=4):
            yield tuple(v for k in bits for v in (k,k)),F(1,16),bits
    else:raise ValueError("unknown noise design")
def mean(xs):
    xs=tuple(xs)
    if not xs:raise ValueError("empty average")
    return sum(xs,Z)/len(xs)
def did(obs):
    if len(obs)!=8:raise ValueError("needs full 4x2 observed panel")
    change_t=mean([obs[2*i+1]-obs[2*i] for i in TREATED])
    change_c=mean([obs[2*i+1]-obs[2*i] for i in CONTROL])
    time_means=(mean([obs[2*i+1] for i in TREATED])-mean([obs[2*i] for i in TREATED]))-(
        mean([obs[2*i+1] for i in CONTROL])-mean([obs[2*i] for i in CONTROL]))
    if change_t-change_c!=time_means:raise AssertionError("two exact DiD paths inconsistent")
    return change_t-change_c
def post_only(obs):
    if len(obs)!=8:raise ValueError("needs panel")
    return mean([obs[2*i+1] for i in TREATED])-mean([obs[2*i+1] for i in CONTROL])
def att(world):return mean(params(world)["tau"])
def analytical_did_center(world):
    # Using fixed source-free outcome generation; audit only.
    p=params(world)
    return att(world)+mean(p["trends"][i] for i in TREATED)-mean(p["trends"][i] for i in CONTROL)+(
        p["treated_coincident"]-p["control_spill"]-p["anticipation"])
def analytical_post_center(world):
    p=params(world)
    return (att(world)+mean(p["baseline"][i]+p["trends"][i] for i in TREATED)
       -mean(p["baseline"][i]+p["trends"][i] for i in CONTROL)
       +p["treated_coincident"]-p["control_spill"])
def compute():
    allrows=[];worlds=[];noise_observation_pairs={}
    for world in WORLDS:
        for scheme in SCHEMES:
            raw=[];mass=Z
            for eps,weight,bits in original_noise(scheme):
                baseline,obs=latent_panel(world,eps)
                dh=did(obs);po=post_only(obs);true=att(world)
                mass+=weight
                row={
                    "world":world,"noise_scheme":scheme,
                    "original_noise_seed_bits":"|".join(map(str,bits)),
                    "realized_unit_period_noise_8":"|".join(map(str,eps)),
                    "source_true_probability_exact":str(weight),
                    "oracle_no_target_policy_potential_panel_8_FOR_AUDIT_ONLY":"|".join(map(str,baseline)),
                    "actually_observed_four_units_two_periods_8":"|".join(map(str,obs)),
                    "true_post_treated_average_policy_direct_effect_exact":str(true),
                    "observable_DiD_estimate_exact":str(dh),
                    "observable_post_only_estimate_exact":str(po),
                    "DiD_squared_error_from_true_ATT_exact":str((dh-true)**2),
                    "post_only_squared_error_from_true_ATT_exact":str((po-true)**2),
                }
                raw.append((weight,dh,po,row))
                allrows.append(row)
            if mass!=O:raise AssertionError("complete noise sources not normalized")
            expected_did=sum((w*v for w,v,p,r in raw),Z)
            expected_post=sum((w*p for w,v,p,r in raw),Z)
            if expected_did!=analytical_did_center(world) or expected_post!=analytical_post_center(world):
                raise AssertionError("source enumeration and independently derived noiseless centers differ")
            var_did=sum((w*(v-expected_did)**2 for w,v,p,r in raw),Z)
            var_post=sum((w*(p-expected_post)**2 for w,v,p,r in raw),Z)
            correct_did_var=F(2) if scheme=="CELL_INDEPENDENT" else Z
            if var_did!=correct_did_var or var_post!=O:
                raise AssertionError("independent noise coefficient variance fails")
            tau=att(world)
            mse_did=sum((w*(v-tau)**2 for w,v,p,r in raw),Z)
            mse_post=sum((w*(p-tau)**2 for w,v,p,r in raw),Z)
            if mse_did!=(expected_did-tau)**2+var_did or mse_post!=(expected_post-tau)**2+var_post:
                raise AssertionError("two independent exact bias^2 plus variance MSE routes differ")
            worlds.append({
                "world":world,"noise_scheme":scheme,"original_source_count":len(raw),
                "original_source_probability_sum_exact":"1",
                "source_true_post_ATT_exact":str(tau),
                "DiD_observed_estimator_expected_exact":str(expected_did),
                "DiD_bias_vs_ATT_exact":str(expected_did-tau),
                "DiD_exact_noise_variance":str(var_did),
                "DiD_source_MSE_exact":str(mse_did),
                "DiD_independent_analytic_MSE_exact":str((expected_did-tau)**2+var_did),
                "post_only_expected_exact":str(expected_post),
                "post_only_bias_exact":str(expected_post-tau),
                "post_only_exact_noise_variance":str(var_post),
                "post_only_source_MSE_exact":str(mse_post),
                "parallel_untreated_group_mean_trends":
                    mean(params(world)["trends"][i] for i in TREATED)==
                    mean(params(world)["trends"][i] for i in CONTROL),
                "no_policy_anticipation":params(world)["anticipation"]==0,
                "no_control_spillover":params(world)["control_spill"]==0,
                "no_treated_coincident_shock":params(world)["treated_coincident"]==0,
            })
            if world in ("VALID_CONSTANT_TWO","SIMULTANEOUS_TREATED_SHOCK_NO_CAUSAL"):
                noise_observation_pairs[(world,scheme)]=tuple(
                    (r["original_noise_seed_bits"],r["actually_observed_four_units_two_periods_8"])
                    for w,v,p,r in raw)
    for scheme in SCHEMES:
        if noise_observation_pairs[("VALID_CONSTANT_TWO",scheme)]!=noise_observation_pairs[("SIMULTANEOUS_TREATED_SHOCK_NO_CAUSAL",scheme)]:
            raise AssertionError("precommitted identical observed panels for different true ATT fail")
    if len(allrows)!=3264 or len(worlds)!=24:raise AssertionError("original source count missing")
    return {
        "research_id":"R215","catalogue_id":"09-006",
        "status":"ARTIFICIAL_E1_AWAIT_CI_ACCEPTANCE",
        "four_fixed_panel_units":4,"pre_and_post_periods":2,
        "source_true_worlds":12,"noise_schemes":list(SCHEMES),
        "full_world_noise_source_conditions":24,"full_original_noise_panel_sources":3264,
        "two_independent_observable_DiD_routes_exact":True,
        "two_independent_fraction_MSE_routes_exact":True,
        "observationally_equivalent_complete_panel_worlds_with_distinct_true_ATT":
            ["VALID_CONSTANT_TWO","SIMULTANEOUS_TREATED_SHOCK_NO_CAUSAL"],
        "worlds":worlds,
        "new_real_human_E2":0,"new_real_historical_E3":0,
        "scope":"two-period four-person artificial panel, no 3+ pretrends or asymptotic clustered inference"
    },allrows
def emit():
    result,rows=compute()
    path=HERE/"R215_EXACT_RESULTS.json"
    csvpath=HERE/"R215_ALL_3264_ORIGINAL_PANEL_NOISE_SOURCES.csv"
    path.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    with csvpath.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    a={
        "research_id":"R215","actual_catalogue_id":"09-006",
        "complete_source_worlds":12,"noise_modes":2,"full_original_noise_panel_sources":3264,
        "true_same_observation_different_ATT_counterexample":True,
        "source_and_closed_form_mse_exact":True,
        "new_E2":0,"new_E3":0,
        "result_sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
        "full_source_sha256":hashlib.sha256(csvpath.read_bytes()).hexdigest(),
    }
    (HERE/"R215_FINAL_MACHINE_ACCEPTANCE.json").write_text(
        json.dumps(a,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(a,indent=2))
class Tests(unittest.TestCase):
    def test_worlds12(self):self.assertEqual(len(WORLDS),12)
    def test_noise_modes2(self):self.assertEqual(len(SCHEMES),2)
    def test_source_count_independent(self):self.assertEqual(len(list(original_noise("CELL_INDEPENDENT"))),256)
    def test_source_count_persistent(self):self.assertEqual(len(list(original_noise("UNIT_PERSISTENT"))),16)
    def test_full_source_formula(self):self.assertEqual(12*(256+16),3264)
    def test_noise_norm_independent(self):self.assertEqual(sum((w for e,w,b in original_noise("CELL_INDEPENDENT")),Z),O)
    def test_noise_norm_persistent(self):self.assertEqual(sum((w for e,w,b in original_noise("UNIT_PERSISTENT")),Z),O)
    def test_noise_persistent_by_unit(self):
        self.assertTrue(all(all(e[2*i]==e[2*i+1] for i in range(4))
                            for e,w,b in original_noise("UNIT_PERSISTENT")))
    def test_effect_valid_two(self):self.assertEqual(att("VALID_CONSTANT_TWO"),F(2))
    def test_effect_heterogeneous_two(self):self.assertEqual(att("VALID_HETEROGENEOUS"),F(2))
    def test_effect_null(self):self.assertEqual(att("VALID_NULL"),Z)
    def test_effect_negative(self):self.assertEqual(att("VALID_NEGATIVE"),F(-2))
    def test_effect_nonpolicy_shock_zero(self):self.assertEqual(att("SIMULTANEOUS_TREATED_SHOCK_NO_CAUSAL"),Z)
    def test_level_gap_did_two(self):self.assertEqual(analytical_did_center("VALID_LEVEL_GAP"),F(2))
    def test_common_shock_did_two(self):self.assertEqual(analytical_did_center("VALID_COMMON_SHOCK"),F(2))
    def test_treated_up_did_four(self):self.assertEqual(analytical_did_center("NONPARALLEL_TREATED_UP"),F(4))
    def test_treated_down_did_one(self):self.assertEqual(analytical_did_center("NONPARALLEL_TREATED_DOWN"),O)
    def test_spillover_did_one(self):self.assertEqual(analytical_did_center("CONTROL_SPILLOVER"),O)
    def test_anticipation_did_one(self):self.assertEqual(analytical_did_center("ANTICIPATION"),O)
    def test_coincident_shock_did_two_not_true_effect(self):
        self.assertEqual(analytical_did_center("SIMULTANEOUS_TREATED_SHOCK_NO_CAUSAL"),F(2))
        self.assertEqual(att("SIMULTANEOUS_TREATED_SHOCK_NO_CAUSAL"),Z)
    def test_balanced_heterogeneous_trends_did_two(self):
        self.assertEqual(analytical_did_center("HETEROGENEOUS_TRENDS_BALANCED"),F(2))
    def test_observation_equivalence_noiseless(self):
        e=(1,)*8
        self.assertEqual(latent_panel("VALID_CONSTANT_TWO",e)[1],
                         latent_panel("SIMULTANEOUS_TREATED_SHOCK_NO_CAUSAL",e)[1])
    def test_observation_equivalence_every_noise_source(self):
        for scheme in SCHEMES:
            for eps,w,bits in original_noise(scheme):
                self.assertEqual(latent_panel("VALID_CONSTANT_TWO",eps)[1],
                                 latent_panel("SIMULTANEOUS_TREATED_SHOCK_NO_CAUSAL",eps)[1])
    def test_diff_in_means_did_two_routes(self):
        for world in WORLDS:
            obs=latent_panel(world,(1,)*8)[1]
            self.assertEqual(did(obs),analytical_did_center(world))
    def test_did_invariant_to_time_constant_baseline(self):
        self.assertEqual(analytical_did_center("VALID_CONSTANT_TWO"),analytical_did_center("VALID_LEVEL_GAP"))
    def test_all_original_source_expectations(self):
        for world in WORLDS:
            for scheme in SCHEMES:
                data=[(w,did(latent_panel(world,eps)[1]),post_only(latent_panel(world,eps)[1]))
                      for eps,w,bits in original_noise(scheme)]
                self.assertEqual(sum((w*v for w,v,p in data),Z),analytical_did_center(world))
                self.assertEqual(sum((w*p for w,v,p in data),Z),analytical_post_center(world))
    def test_noise_variance_analytic_two(self):
        e=[did(latent_panel("VALID_CONSTANT_TWO",eps)[1]) for eps,w,bits in original_noise("CELL_INDEPENDENT")]
        mu=mean(e)
        self.assertEqual(mean([(v-mu)**2 for v in e]),F(2))
    def test_noise_variance_persistent_zero(self):
        e=[did(latent_panel("VALID_CONSTANT_TWO",eps)[1]) for eps,w,bits in original_noise("UNIT_PERSISTENT")]
        self.assertEqual(max(e),min(e))
    def test_post_only_noise_variance_independent_one(self):
        a=[post_only(latent_panel("VALID_CONSTANT_TWO",eps)[1]) for eps,w,bits in original_noise("CELL_INDEPENDENT")]
        mu=mean(a)
        self.assertEqual(mean([(v-mu)**2 for v in a]),O)
    def test_post_only_noise_variance_persistent_one(self):
        a=[post_only(latent_panel("VALID_CONSTANT_TWO",eps)[1]) for eps,w,bits in original_noise("UNIT_PERSISTENT")]
        mu=mean(a)
        self.assertEqual(mean([(v-mu)**2 for v in a]),O)
    def test_invalid_world_rejected(self):
        with self.assertRaises(ValueError):params("INVALID")
    def test_invalid_noise_rejected(self):
        with self.assertRaises(ValueError):list(original_noise("BAD"))
    def test_invalid_panel_rejected(self):
        with self.assertRaises(ValueError):did((0,))
    def test_full_world_count(self):
        r,rows=compute()
        self.assertEqual(len(r["worlds"]),24)
        self.assertEqual(len(rows),3264)
        self.assertEqual(r["new_real_human_E2"],0)
    def test_full_deterministic_replay(self):self.assertEqual(compute(),compute())
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--test",action="store_true");p.add_argument("--emit",action="store_true")
    a=p.parse_args()
    if a.test:
        result=unittest.TextTestRunner(verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
        raise SystemExit(0 if result.wasSuccessful() else 1)
    if a.emit:emit()
    if not a.test and not a.emit:p.print_help()
