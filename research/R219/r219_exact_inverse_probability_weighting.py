#!/usr/bin/env python3
"""R219 exact inverse probability weighting on all six artificial 8-unit worlds.

Complete independent assignment histories (5*2**8+1 = 1281). Finite
Horvitz-Thompson HT and Hájek self-normalized estimates, exact Fraction
Bernoulli assignment score and independent variance/mean analytic checks.

PUBLIC policy uses known X-stratum propensities only (NOT fitted).
Oracle has true individual assignment p which may depend on hidden U.
Positivity failure is an honest undefined causal IPW status, not zero.
No human studies and no new heldout people.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import unittest
from fractions import Fraction as F
from pathlib import Path

ZERO=F(0)
ONE=F(1)
N=8
XS=(0,0,0,0,1,1,1,1)
US=(0,0,1,1,0,0,1,1)
WORLDS=("CORRECT_X","HIDDEN_U_BOTH","HIDDEN_U_ASSIGNMENT_ONLY",
        "WEAK_OVERLAP","HETEROGENEOUS_TAU_X","POSITIVITY_FAILURE")
METHODS=("PUBLIC_HT_X","PRIVILEGED_TRUE_HT","WRONG_CONSTANT_HT","CLIPPED_PUBLIC_HT")
HERE=Path(__file__).resolve().parent

def world_definition(world):
    if world not in WORLDS:
        raise ValueError("not a frozen world")
    e0,e1=(F(1,16),F(15,16)) if world=="WEAK_OVERLAP" else (
        (ZERO,ONE) if world=="POSITIVITY_FAILURE" else (F(1,4),F(3,4)))
    public=tuple(e0 if x==0 else e1 for x in XS)
    if world in ("HIDDEN_U_BOTH","HIDDEN_U_ASSIGNMENT_ONLY"):
        true=tuple((F(1,8)+F(u,4)) if x==0 else (F(5,8)+F(u,4))
                   for x,u in zip(XS,US))
    else:
        true=public
    y0=tuple(F(2*x+(2*u if world=="HIDDEN_U_BOTH" else 0)) for x,u in zip(XS,US))
    y1=tuple(y0[i]+(F(4*XS[i]) if world=="HETEROGENEOUS_TAU_X" else F(2))
             for i in range(N))
    if sum(y1[i]-y0[i] for i in range(N))/N!=F(2):
        raise AssertionError("frozen ATE2 violated")
    return {"world":world,"true_p":true,"public_eX":public,"y0":y0,"y1":y1,
            "ate":F(2),"finite_positive":all(ZERO<q<ONE for q in true)
               and all(ZERO<q<ONE for q in public)}

def assignment(bits):
    if bits<0 or bits>=1<<N:
        raise ValueError("assignment bitmask not in finite 8-person universe")
    return tuple(int(bits&(1<<i)!=0) for i in range(N))

def true_assignment_probability(true_p,z):
    if len(true_p)!=N or len(z)!=N:
        raise ValueError("eight units")
    score=ONE
    for q,treated in zip(true_p,z):
        score*=q if treated else (ONE-q)
    return score

def observed_y(y0,y1,z):
    if any(len(x)!=N for x in (y0,y1,z)):
        raise ValueError("eight units")
    return tuple(y1[i] if z[i] else y0[i] for i in range(N))

def valid_weight_proposal(q):
    return len(q)==N and all(ZERO<v<ONE for v in q)

def ht(y,z,q):
    if len(y)!=N or len(z)!=N or not valid_weight_proposal(q):
        raise ValueError("no HT weights if nonpositive probability")
    return sum(((y[i]/q[i]) if z[i] else (-y[i]/(ONE-q[i]))
                for i in range(N)),ZERO)/N

def clamp_public(q):
    return tuple(min(F(3,4),max(F(1,4),x)) for x in q)

def policy_probabilities(world):
    w=world_definition(world)
    if not w["finite_positive"]:
        return None
    return {
        "PUBLIC_HT_X":w["public_eX"],
        "PRIVILEGED_TRUE_HT":w["true_p"],
        "WRONG_CONSTANT_HT":(F(1,2),)*N,
        "CLIPPED_PUBLIC_HT":clamp_public(w["public_eX"]),
    }

def oracle_analytic_ht_moments(y0,y1,true_p,q):
    """INDEPENDENT Bernoulli-moment calculation, no Z enumeration."""
    if not valid_weight_proposal(true_p) or not valid_weight_proposal(q):
        raise ValueError("no valid population HT moments")
    expected=sum((
        true_p[i]*y1[i]/q[i] - (ONE-true_p[i])*y0[i]/(ONE-q[i])
        for i in range(N)),ZERO)/N
    variance=sum((
        true_p[i]*(ONE-true_p[i]) *
        (y1[i]/q[i]+y0[i]/(ONE-q[i]))**2
        for i in range(N)),ZERO)/(N*N)
    return expected,variance

def naive(y,z):
    t=[y[i] for i in range(N) if z[i]]
    c=[y[i] for i in range(N) if not z[i]]
    return sum(t,ZERO)/len(t)-sum(c,ZERO)/len(c) if t and c else None

def ess(weights):
    if not weights:
        return None
    denom=sum((w*w for w in weights),ZERO)
    if denom<=0:
        raise AssertionError("positive weight squares")
    return sum(weights,ZERO)**2/denom

def hajek(y,z,q):
    if not valid_weight_proposal(q):
        raise ValueError("no Hajek weights if nonpositive probability")
    w1=tuple(ONE/q[i] for i in range(N) if z[i])
    w0=tuple(ONE/(ONE-q[i]) for i in range(N) if not z[i])
    if not w1 or not w0:
        return None
    sum1,sum0=sum(w1,ZERO),sum(w0,ZERO)
    mean1=sum((y[i]/q[i] for i in range(N) if z[i]),ZERO)/sum1
    mean0=sum((y[i]/(ONE-q[i]) for i in range(N) if not z[i]),ZERO)/sum0
    return {"effect":mean1-mean0,"w_treated_sum":sum1,"w_control_sum":sum0,
            "ess_treated":ess(w1),"ess_control":ess(w0),
            "max_observed_inverse_weight":max(w1+w0)}

def conditional_source_moments(records,field):
    """Finite probability distribution on defined assignment events only."""
    mass=sum((r["source_probability"] for r in records if r[field] is not None),ZERO)
    if mass<=0:
        return {"defined_mass":ZERO,"conditional_mean":None,"conditional_var":None}
    mean=sum((r["source_probability"]*r[field] for r in records
              if r[field] is not None),ZERO)/mass
    var=sum((r["source_probability"]*(r[field]-mean)**2 for r in records
             if r[field] is not None),ZERO)/mass
    return {"defined_mass":mass,"conditional_mean":mean,"conditional_var":var}

def compute():
    source_rows=[]
    worlds=[]
    for world in WORLDS:
        w=world_definition(world)
        policy=policy_probabilities(world)
        candidates=range(256)
        events=[]
        for bits in candidates:
            z=assignment(bits)
            prob=true_assignment_probability(w["true_p"],z)
            if prob==0:
                continue
            y=observed_y(w["y0"],w["y1"],z)
            if policy is None:
                ht_results={method:None for method in METHODS}
                h_public=h_oracle=None
                naive_val=naive(y,z)
            else:
                ht_results={method:ht(y,z,q) for method,q in policy.items()}
                h_public=hajek(y,z,policy["PUBLIC_HT_X"])
                h_oracle=hajek(y,z,policy["PRIVILEGED_TRUE_HT"])
                naive_val=naive(y,z)
            event={"bits":bits,"z":z,"y":y,"source_probability":prob,
                   "ht":ht_results,"h_public":h_public,"h_oracle":h_oracle,
                   "naive":naive_val}
            events.append(event)
            rec={
                "world":world,
                "true_full_assignment_bitmask":bits,
                "original_source_probability_exact":str(prob),
                "all_eight_Z":"|".join(map(str,z)),
                "all_eight_actual_observed_Y":"|".join(map(str,y)),
                "oracle_all_eight_true_individual_propensity_NOT_ESTIMATOR_INPUT":
                    "|".join(map(str,w["true_p"])),
                "public_observed_X_propensity":"|".join(map(str,w["public_eX"])),
                "auditor_all_eight_Y0_NOT_ESTIMATOR_INPUT":"|".join(map(str,w["y0"])),
                "auditor_all_eight_Y1_NOT_ESTIMATOR_INPUT":"|".join(map(str,w["y1"])),
                "finite_true_ATE_ORACLE_ONLY":"2",
                "IPW_identification_status":"DEFINED_WITH_POSITIVITY" if policy else
                     "UNIDENTIFIED_NO_POSITIVITY",
                "PUBLIC_HT_X_exact":str(ht_results["PUBLIC_HT_X"]) if policy else "",
                "PRIVILEGED_TRUE_HT_ORACLE_ONLY_exact":
                    str(ht_results["PRIVILEGED_TRUE_HT"]) if policy else "",
                "WRONG_CONSTANT_HT_EXPLICIT_WRONG_MODEL_exact":
                    str(ht_results["WRONG_CONSTANT_HT"]) if policy else "",
                "CLIPPED_PUBLIC_HT_exact":str(ht_results["CLIPPED_PUBLIC_HT"]) if policy else "",
                "PUBLIC_HAJEK_X_exact":str(h_public["effect"]) if h_public else "",
                "PRIVILEGED_HAJEK_ORACLE_ONLY_exact":str(h_oracle["effect"]) if h_oracle else "",
                "PUBLIC_HAJEK_defined":int(h_public is not None),
                "PUBLIC_HAJEK_treated_weight_sum_exact":
                    str(h_public["w_treated_sum"]) if h_public else "",
                "PUBLIC_HAJEK_control_weight_sum_exact":
                    str(h_public["w_control_sum"]) if h_public else "",
                "PUBLIC_HAJEK_treated_effective_sample_size_exact":
                    str(h_public["ess_treated"]) if h_public else "",
                "PUBLIC_HAJEK_control_effective_sample_size_exact":
                    str(h_public["ess_control"]) if h_public else "",
                "PUBLIC_HAJEK_max_actual_weight":
                    str(h_public["max_observed_inverse_weight"]) if h_public else "",
                "NAIVE_mean_difference_exact":str(naive_val) if naive_val is not None else "",
                "NAIVE_defined":int(naive_val is not None),
            }
            source_rows.append(rec)
        mass=sum((e["source_probability"] for e in events),ZERO)
        if mass!=ONE:
            raise AssertionError("incomplete independent Bernoulli true source")
        expected_count=1 if world=="POSITIVITY_FAILURE" else 256
        if len(events)!=expected_count:
            raise AssertionError("did not enumerate all positive-probability assignment sources")
        result={
            "world":world,"original_full_treatment_assignment_sources":len(events),
            "true_source_probability_mass_exact":"1",
            "true_ATE_exact":str(w["ate"]),
            "public_X0_propensity_exact":str(w["public_eX"][0]),
            "public_X1_propensity_exact":str(w["public_eX"][4]),
            "hidden_U_affects_true_selection":world in (
                "HIDDEN_U_BOTH","HIDDEN_U_ASSIGNMENT_ONLY"),
            "hidden_U_affects_potential_Y0":world=="HIDDEN_U_BOTH",
            "true_individual_propensities_ORACLE_ONLY":"|".join(map(str,w["true_p"])),
            "has_full_public_X_positivity":bool(policy),
            "IPW_status":"DEFINED_WITH_POSITIVITY" if policy else "UNIDENTIFIED_NO_POSITIVITY",
        }
        if not policy:
            for method in METHODS:
                result[method+"_expected_value_exact"]=None
                result[method+"_randomization_variance_exact"]=None
                result[method+"_bias_exact"]=None
            result["PUBLIC_HAJEK_defined_source_probability_exact"]=None
            result["PUBLIC_HAJEK_conditional_expected_value_exact"]=None
            result["PUBLIC_HAJEK_conditional_variance_exact"]=None
            result["PRIVILEGED_HAJEK_defined_source_probability_exact"]=None
            result["PRIVILEGED_HAJEK_conditional_expected_value_exact"]=None
            result["PRIVILEGED_HAJEK_conditional_variance_exact"]=None
        else:
            for method,q in policy.items():
                empirical_mean=sum((e["source_probability"]*e["ht"][method]
                                    for e in events),ZERO)
                empirical_var=sum((e["source_probability"]*
                    (e["ht"][method]-empirical_mean)**2 for e in events),ZERO)
                analytic_mean,analytic_var=oracle_analytic_ht_moments(
                    w["y0"],w["y1"],w["true_p"],q)
                if (empirical_mean,empirical_var)!=(analytic_mean,analytic_var):
                    raise AssertionError("1281 original assignments vs independent Bernoulli analytic HT moments")
                result[method+"_expected_value_exact"]=str(empirical_mean)
                result[method+"_randomization_variance_exact"]=str(empirical_var)
                result[method+"_bias_exact"]=str(empirical_mean-w["ate"])
            for label,field in (("PUBLIC_HAJEK","h_public"),
                                ("PRIVILEGED_HAJEK","h_oracle")):
                m=conditional_source_moments([
                    {"source_probability":e["source_probability"],
                     "effect":e[field]["effect"] if e[field] else None}
                    for e in events],"effect")
                result[label+"_defined_source_probability_exact"]=str(m["defined_mass"])
                result[label+"_conditional_expected_value_exact"]=str(m["conditional_mean"])
                result[label+"_conditional_variance_exact"]=str(m["conditional_var"])
            result["PUBLIC_max_possible_inverse_weight_exact"]=str(
                max(max(ONE/q,ONE/(ONE-q)) for q in policy["PUBLIC_HT_X"]))
            result["CLIPPED_max_possible_inverse_weight_exact"]=str(
                max(max(ONE/q,ONE/(ONE-q)) for q in policy["CLIPPED_PUBLIC_HT"]))
        naive_stats=conditional_source_moments([
            {"source_probability":e["source_probability"],"estimate":e["naive"]}
            for e in events],"estimate")
        result["NAIVE_defined_probability_exact"]=str(naive_stats["defined_mass"])
        result["NAIVE_conditional_expectation_exact"]=str(naive_stats["conditional_mean"])
        result["NAIVE_conditional_variance_exact"]=str(naive_stats["conditional_var"])
        worlds.append(result)
    if len(source_rows)!=1281 or len(worlds)!=6:
        raise AssertionError("full precommitted source universe not saved")
    d={w["world"]:w for w in worlds}
    if d["POSITIVITY_FAILURE"]["PUBLIC_HT_X_expected_value_exact"] is not None:
        raise AssertionError("positivity failure must NOT publish numeric causal HT result")
    for key in ("CORRECT_X","HIDDEN_U_ASSIGNMENT_ONLY","WEAK_OVERLAP",
                "HETEROGENEOUS_TAU_X"):
        if d[key]["PUBLIC_HT_X_expected_value_exact"]!="2":
            raise AssertionError("true X-based weighting did not restore finite ATE")
    if d["HIDDEN_U_BOTH"]["PUBLIC_HT_X_expected_value_exact"]=="2":
        raise AssertionError("hidden confounding counterexample lost")
    for w in worlds:
        if w["IPW_status"]=="DEFINED_WITH_POSITIVITY":
            if w["PRIVILEGED_TRUE_HT_expected_value_exact"]!="2":
                raise AssertionError("correct oracle individual HT not mean unbiased")
    return {
        "research_id":"R219",
        "original_239_catalogue_id":"09-010",
        "status":"ARTIFICIAL_E1_AWAIT_CI_ACCEPTANCE",
        "artificial_units":8,
        "complete_assignment_source_rows":len(source_rows),
        "true_worlds":len(worlds),
        "independent_Bernoulli_assignment_sources_not_new_real_people":True,
        "public_X_propensities_preknown_not_fitted":True,
        "individual_true_p_used_only_by_privileged_oracle":True,
        "hidden_U_not_read_by_public_estimators":True,
        "all_original_source_probabilities_exact":True,
        "two_fraction_moment_verification_routes":True,
        "HAJEK_only_conditional_on_both_nonempty_treatment_arms":True,
        "positivity_failure_numeric_estimates_refused":True,
        "all_true_finite_population_ATE":"2",
        "worlds":worlds,
        "new_real_human_E2":0,"new_real_historical_E3":0,
        "limits":"Exact synthetic eight-unit independent Bernoulli treatment distributions with public propensities pre-known, not fitted or measured; no human causal effect identified."
    },source_rows

def emit():
    results,rows=compute()
    paths={"results":HERE/"R219_EXACT_RESULTS.json",
           "sources":HERE/"R219_ALL_1281_ORIGINAL_TREATMENT_ASSIGNMENT_SOURCES.csv"}
    paths["results"].write_text(
        json.dumps(results,sort_keys=True,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    with paths["sources"].open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    machine={
        "model_id":"R219","original_catalogue_id":"09-010",
        "six_artificial_worlds":6,
        "complete_original_assignment_source_rows":1281,
        "complete_source_means_variances_match_independent_Bernoulli_formulas":True,
        "positive_assumption_failure_causal_output_null":True,
        "human_E2":0,"historical_E3":0,
        **{k+"_sha256":hashlib.sha256(path.read_bytes()).hexdigest()
           for k,path in paths.items()}
    }
    (HERE/"R219_FINAL_MACHINE_ACCEPTANCE.json").write_text(
        json.dumps(machine,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(machine,indent=2))

class Tests(unittest.TestCase):
    def test_n_eight(self): self.assertEqual(N,8)
    def test_six_worlds(self): self.assertEqual(len(WORLDS),6)
    def test_x_strata_sizes(self): self.assertEqual((XS.count(0),XS.count(1)),(4,4))
    def test_u_each_x_stratum_balanced(self):
        self.assertEqual(sum(US[:4]),2)
        self.assertEqual(sum(US[4:]),2)
    def test_all_true_ate_two(self):
        for name in WORLDS:
            self.assertEqual(world_definition(name)["ate"],F(2))
    def test_all_256_assignment_vectors(self):
        self.assertEqual(len({assignment(i) for i in range(256)}),256)
    def test_assignment_zero_bits(self):
        self.assertEqual(assignment(0),(0,)*8)
    def test_assignment_full_bits(self):
        self.assertEqual(assignment(255),(1,)*8)
    def test_hidden_both_p_within_x(self):
        v=world_definition("HIDDEN_U_BOTH")["true_p"]
        self.assertEqual((v[0],v[2],v[4],v[6]),(F(1,8),F(3,8),F(5,8),F(7,8)))
    def test_hidden_assignment_only_y0_not_u(self):
        self.assertEqual(world_definition("HIDDEN_U_ASSIGNMENT_ONLY")["y0"],
                         tuple(F(2*x) for x in XS))
    def test_hidden_both_y0_depends_u(self):
        w=world_definition("HIDDEN_U_BOTH")
        self.assertEqual((w["y0"][0],w["y0"][2]),(ZERO,F(2)))
    def test_public_hidden_strata_propensities(self):
        w=world_definition("HIDDEN_U_BOTH")
        self.assertEqual((w["public_eX"][0],w["public_eX"][4]),(F(1,4),F(3,4)))
    def test_weak_overlap_max_weight_16(self):
        q=world_definition("WEAK_OVERLAP")["public_eX"]
        self.assertEqual(max(max(ONE/x,ONE/(ONE-x)) for x in q),F(16))
    def test_clipped_max_weight_4(self):
        q=clamp_public(world_definition("WEAK_OVERLAP")["public_eX"])
        self.assertEqual(max(max(ONE/x,ONE/(ONE-x)) for x in q),F(4))
    def test_no_positivity_prob_exact_one_deterministic(self):
        w=world_definition("POSITIVITY_FAILURE")
        self.assertFalse(w["finite_positive"])
        self.assertEqual(true_assignment_probability(w["true_p"],assignment(240)),ONE)
        self.assertEqual(sum(true_assignment_probability(w["true_p"],assignment(i))>0
                             for i in range(256)),1)
    def test_no_positivity_weights_are_rejected(self):
        self.assertIsNone(policy_probabilities("POSITIVITY_FAILURE"))
    def test_full_assignment_mass_every_world(self):
        for name in WORLDS:
            p=world_definition(name)["true_p"]
            self.assertEqual(sum((true_assignment_probability(p,assignment(i))
                                  for i in range(256)),ZERO),ONE)
    def test_true_assignment_probability_nonnegative(self):
        w=world_definition("HIDDEN_U_BOTH")
        self.assertTrue(all(true_assignment_probability(w["true_p"],assignment(i))>0
                            for i in range(256)))
    def test_analytic_oracle_mean_two(self):
        w=world_definition("HIDDEN_U_BOTH")
        mean,var=oracle_analytic_ht_moments(w["y0"],w["y1"],w["true_p"],w["true_p"])
        self.assertEqual(mean,F(2))
        self.assertGreaterEqual(var,ZERO)
    def test_analytic_public_hidden_mean_not_two(self):
        w=world_definition("HIDDEN_U_BOTH")
        self.assertNotEqual(oracle_analytic_ht_moments(w["y0"],w["y1"],
                            w["true_p"],w["public_eX"])[0],F(2))
    def test_public_hidden_assignment_only_unbiased(self):
        w=world_definition("HIDDEN_U_ASSIGNMENT_ONLY")
        self.assertEqual(oracle_analytic_ht_moments(w["y0"],w["y1"],
                         w["true_p"],w["public_eX"])[0],F(2))
    def test_public_heterogeneous_effect_ATE_two(self):
        w=world_definition("HETEROGENEOUS_TAU_X")
        self.assertEqual(oracle_analytic_ht_moments(w["y0"],w["y1"],
                         w["true_p"],w["public_eX"])[0],F(2))
    def test_observed_only_uses_z(self):
        y0=(ZERO,)*8
        y1=(ONE,)*8
        z=assignment(85)
        self.assertEqual(observed_y(y0,y1,z),tuple(F(v) for v in z))
    def test_HT_no_weights_without_positivity(self):
        with self.assertRaises(ValueError):
            ht((ONE,)*8,(0,)*8,(ZERO,)*8)
    def test_HT_empty_treatments_is_defined(self):
        q=(F(1,2),)*8
        self.assertEqual(ht((ONE,)*8,(0,)*8,q),F(-2))
    def test_HT_full_treatments_is_defined(self):
        q=(F(1,2),)*8
        self.assertEqual(ht((ONE,)*8,(1,)*8,q),F(2))
    def test_Hajek_empty_treated_is_undefined(self):
        self.assertIsNone(hajek((ONE,)*8,(0,)*8,(F(1,2),)*8))
    def test_Hajek_empty_control_is_undefined(self):
        self.assertIsNone(hajek((ONE,)*8,(1,)*8,(F(1,2),)*8))
    def test_naive_empty_arm_is_undefined(self):
        self.assertIsNone(naive((ONE,)*8,(1,)*8))
    def test_naive_two_arms_defined(self):
        self.assertEqual(naive((ZERO,ZERO,ZERO,ZERO,ONE,ONE,ONE,ONE),
                               (0,0,0,0,1,1,1,1)),ONE)
    def test_Hajek_constant_outcomes_same_zero(self):
        z=assignment(85)
        self.assertEqual(hajek((F(2),)*8,z,(F(1,2),)*8)["effect"],ZERO)
    def test_ESS_identical_weights_equals_n(self):
        self.assertEqual(ess((ONE,)*3),F(3))
    def test_ESS_weight_unequal_under_n(self):
        self.assertLess(ess((ONE,F(4))),F(2))
    def test_conditional_moments_not_unconditional(self):
        records=[{"source_probability":F(1,4),"v":ZERO},
                 {"source_probability":F(3,4),"v":None}]
        m=conditional_source_moments(records,"v")
        self.assertEqual(m["defined_mass"],F(1,4))
        self.assertEqual(m["conditional_mean"],ZERO)
    def test_valid_ht_population_no_reference_to_z(self):
        w=world_definition("CORRECT_X")
        a=oracle_analytic_ht_moments(w["y0"],w["y1"],w["true_p"],w["public_eX"])
        self.assertEqual(a[0],F(2))
    def test_bad_bits_rejected(self):
        with self.assertRaises(ValueError):
            assignment(256)
    def test_bad_world_rejected(self):
        with self.assertRaises(ValueError):
            world_definition("UNLISTED")
    def test_all_worlds_1281_rows_and_double_means(self):
        d,rows=compute()
        self.assertEqual((len(d["worlds"]),len(rows)),(6,1281))
        by={w["world"]:w for w in d["worlds"]}
        self.assertIsNone(by["POSITIVITY_FAILURE"]["PUBLIC_HT_X_expected_value_exact"])
        self.assertEqual(by["CORRECT_X"]["PUBLIC_HT_X_expected_value_exact"],"2")
        self.assertNotEqual(by["HIDDEN_U_BOTH"]["PUBLIC_HT_X_expected_value_exact"],"2")
    def test_all_worlds_replay_deterministic(self):
        self.assertEqual(compute(),compute())

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--test",action="store_true")
    ap.add_argument("--emit",action="store_true")
    args=ap.parse_args()
    if args.test:
        r=unittest.TextTestRunner(verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
        raise SystemExit(0 if r.wasSuccessful() else 1)
    if args.emit:
        emit()
    if not args.test and not args.emit:
        ap.print_help()
