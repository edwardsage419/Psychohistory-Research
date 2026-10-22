#!/usr/bin/env python3
"""R220 doubly robust AIPW: all 1537 finite artificial assignment histories.

Eight artificial units, X observed, U hidden. Seven worlds include a
2-by-2 correct/misspecified propensity and outcome model factorial, hidden
U jointly affecting treatment and Y, rare overlap and zero positivity.

AIPW public uses ONLY precommitted q(X), m0(X), m1(X), realized treatment Z,
and realized Y. True individual p and both counterfactuals are AUDIT ONLY.
No fitting/learning, empirical standard errors or real-world causal claim.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import unittest
from fractions import Fraction as F
from pathlib import Path

Z=F(0)
ONE=F(1)
N=8
X=(0,0,0,0,1,1,1,1)
U=(0,0,1,1,0,0,1,1)
WORLDS=(
    "BOTH_CORRECT","PROP_CORRECT_OUTCOME_WRONG",
    "PROP_WRONG_OUTCOME_CORRECT","BOTH_WRONG",
    "HIDDEN_U_BOTH","WEAK_OVERLAP","NO_POSITIVITY",
)
PUBLIC=("PUBLIC_AIPW","PUBLIC_HT","PUBLIC_OUTCOME_ONLY")
PRIV=("PRIVILEGED_TRUE_P_AIPW","PRIVILEGED_TRUE_Y_AIPW")
METHODS=PUBLIC+PRIV
HERE=Path(__file__).resolve().parent

def world_definition(name):
    if name not in WORLDS:
        raise ValueError("not a frozen R220 world")
    y0=tuple(F(2*x+2*u) for x,u in zip(X,U))
    y1=tuple(v+2 for v in y0)
    if name=="NO_POSITIVITY":
        p=tuple(Z if x==0 else ONE for x in X)
    elif name=="WEAK_OVERLAP":
        p=tuple(F(1,16) if x==0 else F(15,16) for x in X)
    elif name=="HIDDEN_U_BOTH":
        p=tuple(F(1,8)+F(u,4) if x==0 else F(5,8)+F(u,4)
                for x,u in zip(X,U))
    else:
        p=tuple(F(1,4) if x==0 else F(3,4) for x in X)
    if name in ("PROP_WRONG_OUTCOME_CORRECT","BOTH_WRONG"):
        q=(F(1,2),)*N
    elif name=="HIDDEN_U_BOTH":
        q=tuple(F(1,4) if x==0 else F(3,4) for x in X)
    else:
        q=p
    outcome_correct = name in (
        "BOTH_CORRECT","PROP_WRONG_OUTCOME_CORRECT",
        "HIDDEN_U_BOTH","NO_POSITIVITY",
    )
    if outcome_correct:
        m0=tuple(F(2*x+1) for x in X)
        m1=tuple(v+2 for v in m0)
    else:
        m0=(Z,)*N
        m1=(ONE,)*N
    if sum((y1[i]-y0[i] for i in range(N)),Z)/N!=F(2):
        raise AssertionError("all seven true finite ATE must equal two")
    return {
        "name":name,"p":p,"q":q,"y0":y0,"y1":y1,"m0":m0,"m1":m1,
        "true_ATE":F(2),
        "q_claim_correct_for_each_individual":q==p,
        "m_claim_correct_conditional_X_stratum":outcome_correct,
        "hidden_U_affects_treatment":name=="HIDDEN_U_BOTH",
        "positivity":all(Z<v<ONE for v in p) and all(Z<v<ONE for v in q),
    }

def treat_vector(bits):
    if type(bits) is not int or not 0<=bits<256:
        raise ValueError("eight Bernoulli bits only")
    return tuple(int(bool(bits&(1<<i))) for i in range(N))

def source_probability(p,t):
    if len(p)!=N or len(t)!=N:
        raise ValueError("need all eight source units")
    weight=ONE
    for pi,ti in zip(p,t):
        weight*=pi if ti else (ONE-pi)
    return weight

def actual_y(w,t):
    return tuple(w["y1"][i] if t[i] else w["y0"][i] for i in range(N))

def valid_q(q):
    return len(q)==N and all(Z<v<ONE for v in q)

def aipw(y,t,q,m0,m1):
    """Observed-data augmented HT: never reads truth counterfactuals."""
    if len(y)!=N or len(t)!=N or any(len(v)!=N for v in (q,m0,m1)) or not valid_q(q):
        raise ValueError("no AIPW without positive weights and 8 observations")
    return sum((m1[i]-m0[i]+
                (y[i]-m1[i])/q[i] if t[i] else
                m1[i]-m0[i]-(y[i]-m0[i])/(ONE-q[i])
               for i in range(N)),Z)/N

def ht(y,t,q):
    if len(y)!=N or len(t)!=N or not valid_q(q):
        raise ValueError("no HT without positivity")
    return sum((y[i]/q[i] if t[i] else -y[i]/(ONE-q[i])
                for i in range(N)),Z)/N

def outcome_only(m0,m1):
    return sum((m1[i]-m0[i] for i in range(N)),Z)/N

def independent_aipw_moments(w,q,m0,m1):
    """Full analytic Bernoulli moments: NO assignment enumeration."""
    if not valid_q(q) or not valid_q(w["p"]):
        raise ValueError("true and assumed assignment probability must be interior")
    p=w["p"]; y0=w["y0"]; y1=w["y1"]
    mean=sum((
        m1[i]-m0[i]+
        p[i]*(y1[i]-m1[i])/q[i]-
        (ONE-p[i])*(y0[i]-m0[i])/(ONE-q[i])
        for i in range(N)),Z)/N
    var=sum((
        p[i]*(ONE-p[i])*(
            (y1[i]-m1[i])/q[i]+(y0[i]-m0[i])/(ONE-q[i])
        )**2
        for i in range(N)),Z)/(N*N)
    return mean,var

def independent_ht_moments(w,q):
    if not valid_q(q) or not valid_q(w["p"]):
        raise ValueError("true and working propensity must have positivity")
    p=w["p"]; y0=w["y0"]; y1=w["y1"]
    mean=sum((p[i]*y1[i]/q[i]-(ONE-p[i])*y0[i]/(ONE-q[i])
              for i in range(N)),Z)/N
    var=sum((p[i]*(ONE-p[i])*(y1[i]/q[i]+y0[i]/(ONE-q[i]))**2
             for i in range(N)),Z)/(N*N)
    return mean,var

def methods_for_assignment(w,t):
    if not w["positivity"]:
        return {m:None for m in METHODS}
    y=actual_y(w,t)
    return {
        "PUBLIC_AIPW":aipw(y,t,w["q"],w["m0"],w["m1"]),
        "PUBLIC_HT":ht(y,t,w["q"]),
        "PUBLIC_OUTCOME_ONLY":outcome_only(w["m0"],w["m1"]),
        "PRIVILEGED_TRUE_P_AIPW":aipw(y,t,w["p"],w["m0"],w["m1"]),
        "PRIVILEGED_TRUE_Y_AIPW":aipw(y,t,w["q"],w["y0"],w["y1"]),
    }

def analytic_method_moments(w,m):
    if not w["positivity"]:
        return None
    if m=="PUBLIC_AIPW":
        return independent_aipw_moments(w,w["q"],w["m0"],w["m1"])
    if m=="PUBLIC_HT":
        return independent_ht_moments(w,w["q"])
    if m=="PUBLIC_OUTCOME_ONLY":
        return outcome_only(w["m0"],w["m1"]),Z
    if m=="PRIVILEGED_TRUE_P_AIPW":
        return independent_aipw_moments(w,w["p"],w["m0"],w["m1"])
    if m=="PRIVILEGED_TRUE_Y_AIPW":
        return independent_aipw_moments(w,w["q"],w["y0"],w["y1"])
    raise ValueError("unknown fixed AIPW audit method")

def compute():
    all_source_rows=[]
    full_worlds=[]
    for world in WORLDS:
        w=world_definition(world)
        samples=[]
        for bits in range(256):
            t=treat_vector(bits)
            p=source_probability(w["p"],t)
            if p==0:
                continue
            o=actual_y(w,t)
            methods=methods_for_assignment(w,t)
            samples.append((p,methods))
            row={
                "world":world,"original_assignment_bitmask":bits,
                "actual_eight_treatment_assignment":"|".join(map(str,t)),
                "actual_observed_eight_outcomes":"|".join(map(str,o)),
                "original_source_probability_exact":str(p),
                "observed_eight_X":"|".join(map(str,X)),
                "hidden_U_AUDIT_ONLY":"|".join(map(str,U)),
                "true_individual_treatment_propensities_AUDIT_ONLY":
                    "|".join(map(str,w["p"])),
                "public_q_propensity_model_precommitted":"|".join(map(str,w["q"])),
                "public_m0_precommitted":"|".join(map(str,w["m0"])),
                "public_m1_precommitted":"|".join(map(str,w["m1"])),
                "true_eight_Y0_COUNTERFACTUAL_AUDIT_ONLY":"|".join(map(str,w["y0"])),
                "true_eight_Y1_COUNTERFACTUAL_AUDIT_ONLY":"|".join(map(str,w["y1"])),
                "oracle_true_finite_ATE":"2",
                "causal_AIPW_identification_status":"DEFINED_WITH_POSITIVITY" if w["positivity"]
                       else "UNIDENTIFIED_NO_POSITIVITY",
            }
            for m in METHODS:
                row[m+"_exact"]="" if methods[m] is None else str(methods[m])
                row[m+"_true_ATE_squared_error_exact"]="" if methods[m] is None else (
                    str((methods[m]-w["true_ATE"])**2))
            all_source_rows.append(row)
        mass=sum((p for p,v in samples),Z)
        if mass!=ONE:
            raise AssertionError("frozen world sources not normalized")
        if len(samples)!=(256 if w["positivity"] else 1):
            raise AssertionError("not all positive-probability source paths")
        summary={
            "world":world,"full_original_assignment_histories":len(samples),
            "full_original_source_probability_mass":"1",
            "true_ATE_exact":"2",
            "actual_true_propensity_eight_AUDIT_ONLY":"|".join(map(str,w["p"])),
            "public_q_eight":"|".join(map(str,w["q"])),
            "public_m0_eight":"|".join(map(str,w["m0"])),
            "public_m1_eight":"|".join(map(str,w["m1"])),
            "propensity_exact_individual_correct":w["q_claim_correct_for_each_individual"],
            "outcome_model_correct_finite_X_stratum_mean":
                w["m_claim_correct_conditional_X_stratum"],
            "hidden_U_affects_true_treatment":w["hidden_U_affects_treatment"],
            "has_full_positivity":w["positivity"],
            "causal_AIPW_status":"DEFINED_WITH_POSITIVITY" if w["positivity"]
                   else "UNIDENTIFIED_NO_POSITIVITY",
        }
        for m in METHODS:
            if not w["positivity"]:
                summary[m+"_expected_value_exact"]=None
                summary[m+"_variance_exact"]=None
                summary[m+"_bias_exact"]=None
                summary[m+"_MSE_exact"]=None
                continue
            mean=sum((p*v[m] for p,v in samples),Z)
            var=sum((p*(v[m]-mean)**2 for p,v in samples),Z)
            mse=sum((p*(v[m]-w["true_ATE"])**2 for p,v in samples),Z)
            analytic_mean,analytic_var=analytic_method_moments(w,m)
            if (mean,var)!=(analytic_mean,analytic_var):
                raise AssertionError("complete 256 original Bernoulli sources vs independent analytic AIPW routes differ")
            if mse!=var+(mean-w["true_ATE"])**2:
                raise AssertionError("source true-Ate MSE vs bias²+variance identity failed")
            summary[m+"_expected_value_exact"]=str(mean)
            summary[m+"_variance_exact"]=str(var)
            summary[m+"_bias_exact"]=str(mean-w["true_ATE"])
            summary[m+"_MSE_exact"]=str(mse)
        full_worlds.append(summary)
    if len(all_source_rows)!=1537 or len(full_worlds)!=7:
        raise AssertionError("full seven world source enumeration violated")
    d={x["world"]:x for x in full_worlds}
    if any(d[x]["PUBLIC_AIPW_expected_value_exact"]!="2" for x in (
        "BOTH_CORRECT","PROP_CORRECT_OUTCOME_WRONG",
        "PROP_WRONG_OUTCOME_CORRECT","WEAK_OVERLAP")):
        raise AssertionError("finite double robustness source demonstration fails")
    if d["BOTH_WRONG"]["PUBLIC_AIPW_expected_value_exact"]=="2":
        raise AssertionError("both-wrong source not differentiating misspecification")
    if d["HIDDEN_U_BOTH"]["PUBLIC_AIPW_expected_value_exact"]=="2":
        raise AssertionError("exchangeability failure should be visible")
    for w in full_worlds:
        if w["has_full_positivity"]:
            if (w["PRIVILEGED_TRUE_P_AIPW_expected_value_exact"],
                w["PRIVILEGED_TRUE_Y_AIPW_expected_value_exact"])!=("2","2"):
                raise AssertionError("oracle controls not source-valid")
            if w["PRIVILEGED_TRUE_Y_AIPW_variance_exact"]!="0":
                raise AssertionError("oracle both counterfactuals must annihilate residuals")
    return {
        "research_id":"R220",
        "original_catalogue_id":"09-011",
        "status":"ARTIFICIAL_E1_AWAIT_CI_ACCEPTANCE",
        "number_of_artificial_units":N,
        "number_of_artificial_worlds":7,
        "full_original_assignment_source_rows":len(all_source_rows),
        "true_ATE_all_worlds":"2",
        "precommitted_propensity_and_outcome_models_not_estimated":True,
        "observable_X_only_public_estimators":True,
        "true_individual_p_and_potential_outcomes_ORACLE_ONLY":True,
        "full_source_and_independent_analytic_Fraction_moments_equal":True,
        "complete_true_source_probability_each_world_one":True,
        "nonpositive_support_returns_causal_null":True,
        "true_human_E2":0,"true_historical_E3":0,
        "worlds":full_worlds,
        "limits":"Artificial 8-unit 7-world Bernoulli source enumeration; correct X-stratum outcome mean is known in advance, no sample fitting, no cross-fitting, no human causal effect.",
    },all_source_rows

def emit():
    results,raw=compute()
    paths={
        "results":HERE/"R220_EXACT_RESULTS.json",
        "source":HERE/"R220_ALL_1537_ORIGINAL_AIPW_ASSIGNMENT_SOURCES.csv",
    }
    paths["results"].write_text(
        json.dumps(results,sort_keys=True,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    with paths["source"].open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(raw[0]))
        writer.writeheader()
        writer.writerows(raw)
    receipt={
        "model_id":"R220","original_catalogue_id":"09-011",
        "seven_true_artificial_worlds":7,
        "complete_original_treatment_assignments":1537,
        "two_independent_Fraction_AIPW_moment_routes_agree":True,
        "zero_propensity_assumption_failure_returns_null":True,
        "human_E2":0,"historical_E3":0,
        **{name+"_sha256":hashlib.sha256(path.read_bytes()).hexdigest()
           for name,path in paths.items()},
    }
    (HERE/"R220_FINAL_MACHINE_ACCEPTANCE.json").write_text(
        json.dumps(receipt,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(receipt,indent=2))

class Tests(unittest.TestCase):
    def test_eight_units(self): self.assertEqual(N,8)
    def test_seven_worlds(self): self.assertEqual(len(WORLDS),7)
    def test_X_four_per_stratum(self): self.assertEqual(X.count(0),4)
    def test_U_balanced_per_X(self): self.assertEqual(sum(U[:4]),2)
    def test_true_ATE_two_all(self):
        self.assertTrue(all(world_definition(w)["true_ATE"]==F(2) for w in WORLDS))
    def test_full_1537_original_source_count(self): self.assertEqual(6*256+1,1537)
    def test_public_model_is_stratum_mean(self):
        w=world_definition("BOTH_CORRECT")
        for x in (0,1):
            ids=[i for i in range(8) if X[i]==x]
            self.assertEqual(sum(w["y0"][i] for i in ids)/4,w["m0"][ids[0]])
            self.assertEqual(sum(w["y1"][i] for i in ids)/4,w["m1"][ids[0]])
    def test_correct_propensity_q_matches_true(self):
        self.assertEqual(world_definition("BOTH_CORRECT")["p"],
                         world_definition("BOTH_CORRECT")["q"])
    def test_wrong_propensity_q_half(self):
        self.assertEqual(world_definition("PROP_WRONG_OUTCOME_CORRECT")["q"],
                         (F(1,2),)*8)
    def test_wrong_outcome_model_m0_zero_m1_one(self):
        w=world_definition("PROP_CORRECT_OUTCOME_WRONG")
        self.assertEqual((w["m0"],w["m1"]),( (Z,)*8,(ONE,)*8))
    def test_hidden_true_p_varies_U(self):
        w=world_definition("HIDDEN_U_BOTH")
        self.assertEqual((w["p"][0],w["p"][2],w["p"][4],w["p"][6]),
                         (F(1,8),F(3,8),F(5,8),F(7,8)))
    def test_hidden_public_q_coarse(self):
        w=world_definition("HIDDEN_U_BOTH")
        self.assertEqual((w["q"][0],w["q"][4]),(F(1,4),F(3,4)))
    def test_weak_probability_true_extreme(self):
        w=world_definition("WEAK_OVERLAP")
        self.assertEqual((w["p"][0],w["p"][4]),(F(1,16),F(15,16)))
    def test_no_positivity_one_true_assignment(self):
        w=world_definition("NO_POSITIVITY")
        self.assertFalse(w["positivity"])
        self.assertEqual(source_probability(w["p"],treat_vector(240)),ONE)
    def test_zero_pos_has_no_public_estimator(self):
        w=world_definition("NO_POSITIVITY")
        self.assertEqual(methods_for_assignment(w,treat_vector(240)),
                         {m:None for m in METHODS})
    def test_true_assignment_256_support(self):
        w=world_definition("BOTH_CORRECT")
        self.assertEqual(sum(source_probability(w["p"],treat_vector(i))>0
                             for i in range(256)),256)
    def test_true_source_masses_one_each_world(self):
        for name in WORLDS:
            w=world_definition(name)
            self.assertEqual(sum((source_probability(w["p"],treat_vector(i))
                                  for i in range(256)),Z),ONE)
    def test_observed_equals_realized_potential(self):
        w=world_definition("BOTH_CORRECT")
        for mask in (0,1,17,85,240,255):
            t=treat_vector(mask)
            y=actual_y(w,t)
            self.assertTrue(all(y[i]==w["y1"][i] if t[i] else y[i]==w["y0"][i]
                                for i in range(N)))
    def test_AIPW_per_person_with_true_Y_oracle_returns_ATE_each_assignment(self):
        w=world_definition("BOTH_WRONG")
        for mask in (0,1,85,128,240,255):
            t=treat_vector(mask);y=actual_y(w,t)
            self.assertEqual(aipw(y,t,w["q"],w["y0"],w["y1"]),F(2))
    def test_true_p_makes_AIPW_correct_even_wrong_m(self):
        w=world_definition("PROP_CORRECT_OUTCOME_WRONG")
        self.assertEqual(independent_aipw_moments(w,w["p"],w["m0"],w["m1"])[0],F(2))
    def test_outcome_stratum_true_m_residuals_sum_zero(self):
        w=world_definition("PROP_WRONG_OUTCOME_CORRECT")
        for x in (0,1):
            self.assertEqual(sum((w["y0"][i]-w["m0"][i] for i in range(N) if X[i]==x),Z),Z)
    def test_correct_outcome_wrong_q_public_AIPW_mean_two(self):
        w=world_definition("PROP_WRONG_OUTCOME_CORRECT")
        self.assertEqual(independent_aipw_moments(w,w["q"],w["m0"],w["m1"])[0],F(2))
    def test_both_wrong_public_AIPW_biased(self):
        w=world_definition("BOTH_WRONG")
        self.assertNotEqual(independent_aipw_moments(w,w["q"],w["m0"],w["m1"])[0],F(2))
    def test_hidden_U_both_public_AIPW_biased(self):
        w=world_definition("HIDDEN_U_BOTH")
        self.assertNotEqual(independent_aipw_moments(w,w["q"],w["m0"],w["m1"])[0],F(2))
    def test_weak_overlap_public_AIPW_mean_two(self):
        w=world_definition("WEAK_OVERLAP")
        self.assertEqual(independent_aipw_moments(w,w["q"],w["m0"],w["m1"])[0],F(2))
    def test_regression_only_wrong_model_one(self):
        w=world_definition("PROP_CORRECT_OUTCOME_WRONG")
        self.assertEqual(outcome_only(w["m0"],w["m1"]),ONE)
    def test_regression_only_true_model_two(self):
        w=world_definition("PROP_WRONG_OUTCOME_CORRECT")
        self.assertEqual(outcome_only(w["m0"],w["m1"]),F(2))
    def test_public_HT_correct_propensity_true_ATE(self):
        w=world_definition("PROP_CORRECT_OUTCOME_WRONG")
        self.assertEqual(independent_ht_moments(w,w["q"])[0],F(2))
    def test_public_HT_wrong_propensity_bias(self):
        w=world_definition("PROP_WRONG_OUTCOME_CORRECT")
        self.assertNotEqual(independent_ht_moments(w,w["q"])[0],F(2))
    def test_analytic_AIPW_var_nonnegative_all_interior(self):
        for name in WORLDS[:-1]:
            w=world_definition(name)
            self.assertGreaterEqual(independent_aipw_moments(w,w["q"],w["m0"],w["m1"])[1],Z)
    def test_true_Y_oracle_AIPW_variance_zero(self):
        for name in WORLDS[:-1]:
            w=world_definition(name)
            self.assertEqual(independent_aipw_moments(w,w["q"],w["y0"],w["y1"]),(F(2),Z))
    def test_empty_Y_handling(self):
        with self.assertRaises(ValueError):
            aipw((),(0,)*8,(F(1,2),)*8,(Z,)*8,(ONE,)*8)
    def test_invalid_q_zero_rejected(self):
        with self.assertRaises(ValueError):
            aipw((ONE,)*8,(0,)*8,(Z,)*8,(Z,)*8,(ONE,)*8)
    def test_invalid_true_p_for_analytic_rejected(self):
        w=world_definition("NO_POSITIVITY")
        with self.assertRaises(ValueError):
            independent_aipw_moments(w,(F(1,2),)*8,w["m0"],w["m1"])
    def test_invalid_world_rejected(self):
        with self.assertRaises(ValueError):
            world_definition("UNREGISTERED")
    def test_invalid_bitmask_rejected(self):
        with self.assertRaises(ValueError):
            treat_vector(256)
    def test_all_1537_original_sources_and_double_checks(self):
        r,rows=compute()
        self.assertEqual((len(r["worlds"]),len(rows)),(7,1537))
        self.assertEqual(r["true_human_E2"],0)
        w={s["world"]:s for s in r["worlds"]}
        self.assertIsNone(w["NO_POSITIVITY"]["PUBLIC_AIPW_expected_value_exact"])
    def test_deterministic_repeat(self):
        self.assertEqual(compute(),compute())

if __name__=="__main__":
    pa=argparse.ArgumentParser()
    pa.add_argument("--test",action="store_true")
    pa.add_argument("--emit",action="store_true")
    args=pa.parse_args()
    if args.test:
        result=unittest.TextTestRunner(verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
        raise SystemExit(0 if result.wasSuccessful() else 1)
    if args.emit:
        emit()
    if not (args.test or args.emit):
        pa.print_help()
