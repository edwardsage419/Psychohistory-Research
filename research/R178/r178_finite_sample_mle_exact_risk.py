"""R178 artificial finite-sample binomial maximum-likelihood audit.

Closed-form maximum p_hat=K/n versus independent rational likelihood grid.
Five actual count generators from SHA-pinned R177 supply 30 complete PMFs.
All bias, squared error, and Wald coverage are exact rational sums; heldout
log scores use two separate numeric implementations and are labeled numeric.
"""
from __future__ import annotations

from decimal import Decimal, localcontext
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha1,sha256
from pathlib import Path
from itertools import product
import json,math,sys,unittest,zipfile

HERE=Path(__file__).resolve().parent
R177=HERE.parent/"R177"
PROTO=HERE.parent.parent/"protocols/R178_MLE_30_FINITE_SAMPLE_COUNT_WORLDS_PRESCORE_FREEZE_2026-10-21.md"
OUT=HERE/"R178_EXACT_RESULTS.json"
ACCEPT=HERE/"R178_FINAL_MACHINE_ACCEPTANCE.json"
ARCH=HERE/"R178_MLE_30_Finite_Count_Sample_Worlds_Exact_Audit.zip"
ORIGINAL_SOURCE_SHA1="2d032513ce84141214b6b3f84df9c0ed9976a02b"
ORIGINAL_RESULT_SHA256="57410cf2c110ce3117b7af72e4b7473cee0c3ffd013e6fb99fd43de62165a535"
N_VALUES=(4,8,12)
P_VALUES=(F(1,4),F(1,2))
SOURCES=(
 ("IID_BIN","BIN",0),
 ("CLUSTERED_BB_C2","BB",0),
 ("CLUSTERED_BB_C8","BB",2),
 ("INACTIVE_ZIB_Z1_8","ZIB",0),
 ("INACTIVE_ZIB_Z1_4","ZIB",1),
)
WALD_MULT=F(49,25)


def git_blob(raw):
    return sha1(b"blob "+str(len(raw)).encode()+b"\x00"+raw).hexdigest()


def load_source_and_validate():
    source=R177/"r177_four_finite_count_families_exact.py"
    data=R177/"R177_EXACT_RESULTS.json"
    if git_blob(source.read_bytes())!=ORIGINAL_SOURCE_SHA1:
        raise ValueError("R177 source changed from frozen audited blob")
    if sha256(data.read_bytes()).hexdigest()!=ORIGINAL_RESULT_SHA256:
        raise ValueError("R177 full exact source result SHA256 changed")
    sys.path.insert(0,str(R177))
    from r177_four_finite_count_families_exact import formula_pmf,event_dp
    return formula_pmf,event_dp


def cases():
    for n,p,(name,family,regime) in product(N_VALUES,P_VALUES,SOURCES):
        yield n,p,name,family,regime


@lru_cache(maxsize=None)
def mle_grid_certification(n):
    """All rational likelihood grid candidates are tested for each observed K."""
    result={}
    grid=[F(j,4*n) for j in range(4*n+1)]
    for k in range(n+1):
        winner=F(k,n)
        optimum=winner**k*(1-winner)**(n-k)
        max_found=max(t**k*(1-t)**(n-k) for t in grid)
        if optimum!=max_found:
            raise AssertionError("closed-form Bernoulli MLE fails independent grid")
        result[k]=True
    return result


def exact_risks(pmf,n,p):
    if len(pmf)!=n+1 or sum(pmf,F(0))!=1:
        raise ValueError("invalid training-count distribution")
    mle_grid_certification(n)
    mle_bias=sum((weight*(F(k,n)-p) for k,weight in enumerate(pmf)),F(0))
    mle_mse=sum((weight*(F(k,n)-p)**2 for k,weight in enumerate(pmf)),F(0))
    base=p*(1-p)/n
    naive_coverage=F(0)
    for k,w in enumerate(pmf):
        hat=F(k,n)
        if (p-hat)**2 <= WALD_MULT**2*hat*(1-hat)/n:
            naive_coverage+=w
    bound_prob=pmf[0]+pmf[-1]
    if bound_prob<=0 or not 0<p<1:
        raise AssertionError("frozen infinite risk argument requires boundaries")
    lap_bias=sum((w*(F(k+1,n+2)-p) for k,w in enumerate(pmf)),F(0))
    lap_mse=sum((w*(F(k+1,n+2)-p)**2 for k,w in enumerate(pmf)),F(0))
    return {
        "mle_expected_bias":mle_bias,
        "mle_expected_squared_error":mle_mse,
        "iid_model_claimed_theoretical_mse":base,
        "true_over_naive_mle_variance_ratio":mle_mse/base,
        "wald_nominal_95_actual_coverage":naive_coverage,
        "boundary_mle_0_or_1_probability":bound_prob,
        "unsmoothed_mle_independent_test_expected_logloss":"INF",
        "laplace_bias":lap_bias,
        "laplace_expected_squared_error":lap_mse,
    }


def score_float(pmf,n,p):
    p=float(p)
    return sum(float(w)*(-p*math.log(float(F(k+1,n+2)))
                        -(1-p)*math.log(float(F(n-k+1,n+2))))
               for k,w in enumerate(pmf))


def score_decimal(pmf,n,p):
    with localcontext() as ctx:
        ctx.prec=60
        true=Decimal(p.numerator)/Decimal(p.denominator)
        total=Decimal(0)
        for k,w in enumerate(pmf):
            q=Decimal(k+1)/Decimal(n+2)
            mass=Decimal(w.numerator)/Decimal(w.denominator)
            loss=-true*q.ln()-(1-true)*(1-q).ln()
            total+=mass*loss
        return total


def expected_ratio(n,p,name,family,regime):
    if name=="IID_BIN":
        return F(1)
    if family=="BB":
        c=2 if regime==0 else 8
        return F(c+n,c+1)
    if family=="ZIB":
        z=F(1,8) if regime==0 else F(1,4)
        return F(1)+z/(1-z)*(n-1)*p/(1-p)
    raise ValueError("unknown original scenario")


def run():
    f1,f2=load_source_and_validate()
    records=[]
    for n,p,name,family,regime in cases():
        pmf_a=f1(family,n,p,regime)
        pmf_b=f2(family,n,p,regime)
        if pmf_a!=pmf_b:
            raise AssertionError("R177 two verified generators disagree")
        risk=exact_risks(pmf_a,n,p)
        if risk["mle_expected_bias"]!=0:
            raise AssertionError("fixed generator should match marginal mean p")
        ratio=expected_ratio(n,p,name,family,regime)
        if risk["true_over_naive_mle_variance_ratio"]!=ratio:
            raise AssertionError("analytic cluster variance ratio did not match MLE MSE")
        floated=score_float(pmf_a,n,p)
        decimal=score_decimal(pmf_a,n,p)
        if not math.isfinite(floated) or abs(floated-float(decimal))>1e-12:
            raise AssertionError("independent finite forecast loss computations differ")
        raw={k:str(v) if isinstance(v,F) else v for k,v in risk.items()}
        raw.update({
            "sample_size":n,"true_marginal_p":str(p),
            "training_mechanism":name,"source_R177_family":family,
            "source_R177_regime":regime,
            "full_training_count_pmf":[str(x) for x in pmf_a],
            "laplace_expected_independent_test_logloss":format(floated,".16g"),
            "independent_decimal_logloss":str(decimal),
            "r177_closed_form_and_trial_dp_exact_parity":True,
            "mle_rational_grid_maximization_certificate":True,
        })
        records.append(raw)
    if len(records)!=30 or sum(len(x["full_training_count_pmf"]) for x in records)!=270:
        raise AssertionError("source population does not match prescore freeze")
    selected=[r for r in records if r["sample_size"]==8 and r["true_marginal_p"]=="1/4"]
    if len(selected)!=5:
        raise AssertionError("fixed model illustration incomplete")
    out={
        "research_id":"R178",
        "stage":"E1_ARTIFICIAL_EXACT_FINITE_SAMPLE_MLE_RISK",
        "protocol":"protocols/"+PROTO.name,
        "r177_original_python_git_blob":ORIGINAL_SOURCE_SHA1,
        "r177_exact_input_sha256":ORIGINAL_RESULT_SHA256,
        "world_count":len(records),"full_count_probability_cells":270,
        "source_distributions":len(SOURCES),
        "all_MLEs_exactly_unbiased_for_marginal_p":True,
        "all_full_distributions_independently_verified":True,
        "all_30_positive_probability_MLE_boundary_infinite_expected_test_logloss":True,
        "fixed_n8_p_quarter_comparison":selected,
        "source_worlds":records,
        "real_human_or_history_tested":False,"new_E2":0,"new_E3":0,
    }
    OUT.write_text(json.dumps(out,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    acceptance={
       "research_id":"R178","state":"CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_FINITE_MLE",
       "scenario_count":30,"full_count_probability_cells":270,
       "r177_source_verified":True,
       "all_mle_analytical_and_grid_maxima_verified":True,
       "all_exact_unbiased_and_risk_ratios_verified":True,
       "all_exact_wald_coverage":True,
       "all_MLE_expected_oos_logloss_infinite":True,
       "all_laplace_numeric_log_scores_independent_double_check":True,
       "real_data_scored":False,"new_E2":0,"new_E3":0,
       "result_sha256":sha256(OUT.read_bytes()).hexdigest(),
    }
    ACCEPT.write_text(json.dumps(acceptance,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("R178_MACHINE_ACCEPTANCE",json.dumps(acceptance,sort_keys=True))
    print("R178_LOCKED_COMPARISON",json.dumps(selected,sort_keys=True))
    return out


def archive():
    filenames=[Path(__file__).name,OUT.name,ACCEPT.name]
    with zipfile.ZipFile(ARCH,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name in filenames:
            info=zipfile.ZipInfo(name,date_time=(2026,10,21,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o644<<16
            z.writestr(info,(HERE/name).read_bytes())
        info=zipfile.ZipInfo(PROTO.name,date_time=(2026,10,21,0,0,0))
        info.compress_type=zipfile.ZIP_DEFLATED
        info.external_attr=0o644<<16
        z.writestr(info,PROTO.read_bytes())
    print("R178_ARCHIVE_SHA256",sha256(ARCH.read_bytes()).hexdigest())


class TestArtificialMLE(unittest.TestCase):
    def test_world_grid_30(self):
        self.assertEqual(len(list(cases())),30)
    def test_support_total_270(self):
        self.assertEqual(sum(n+1 for n,p,name,f,r in cases()),270)
    def test_model_count_5(self):
        self.assertEqual(len(SOURCES),5)
    def test_analytical_mle_rational_grid_all_n(self):
        for n in N_VALUES:
            self.assertTrue(all(mle_grid_certification(n).values()))
    def test_boundary_mle_zero(self):
        self.assertEqual(F(0,8),0)
    def test_boundary_mle_one(self):
        self.assertEqual(F(8,8),1)
    def test_r177_sha_validation_and_parity(self):
        a,b=load_source_and_validate()
        self.assertEqual(a("BB",4,F(1,4),0),b("BB",4,F(1,4),0))
    def test_independent_training_distribution_all(self):
        a,b=load_source_and_validate()
        for n,p,name,f,r in cases():
            self.assertEqual(a(f,n,p,r),b(f,n,p,r))
    def test_all_bias_zero(self):
        a,b=load_source_and_validate()
        for n,p,name,f,r in cases():
            self.assertEqual(exact_risks(a(f,n,p,r),n,p)["mle_expected_bias"],0)
    def test_all_true_variance_ratios(self):
        a,_=load_source_and_validate()
        for n,p,name,f,r in cases():
            self.assertEqual(exact_risks(a(f,n,p,r),n,p)["true_over_naive_mle_variance_ratio"],
                             expected_ratio(n,p,name,f,r))
    def test_iid_variance_calibrated(self):
        a,_=load_source_and_validate()
        for n,p in product(N_VALUES,P_VALUES):
            self.assertEqual(exact_risks(a("BIN",n,p,0),n,p)["true_over_naive_mle_variance_ratio"],1)
    def test_cluster_overdispersion(self):
        a,_=load_source_and_validate()
        for n,p in product(N_VALUES,P_VALUES):
            self.assertGreater(exact_risks(a("BB",n,p,0),n,p)["true_over_naive_mle_variance_ratio"],1)
    def test_structural_zero_overdispersion(self):
        a,_=load_source_and_validate()
        for n,p in product(N_VALUES,P_VALUES):
            self.assertGreater(exact_risks(a("ZIB",n,p,0),n,p)["true_over_naive_mle_variance_ratio"],1)
    def test_all_mle_boundaries_positive(self):
        a,_=load_source_and_validate()
        for n,p,name,f,r in cases():
            self.assertGreater(exact_risks(a(f,n,p,r),n,p)["boundary_mle_0_or_1_probability"],0)
    def test_wald_coverage_exact_rational(self):
        a,_=load_source_and_validate()
        for n,p,name,f,r in cases():
            coverage=exact_risks(a(f,n,p,r),n,p)["wald_nominal_95_actual_coverage"]
            self.assertIsInstance(coverage,F)
            self.assertGreaterEqual(coverage,0)
            self.assertLessEqual(coverage,1)
    def test_boundary_wald_degeneracy(self):
        self.assertFalse((F(1,4)-0)**2 <= WALD_MULT**2*0)
    def test_laplace_positive_at_boundary(self):
        for n in N_VALUES:
            self.assertGreater(F(1,n+2),0)
            self.assertLess(F(n+1,n+2),1)
    def test_laplace_numeric_score_paths_all(self):
        a,_=load_source_and_validate()
        for n,p,name,f,r in cases():
            pmf=a(f,n,p,r)
            self.assertAlmostEqual(score_float(pmf,n,p),float(score_decimal(pmf,n,p)),places=12)
    def test_laplace_mse_exact(self):
        a,_=load_source_and_validate()
        r=exact_risks(a("BIN",4,F(1,2),0),4,F(1,2))
        self.assertIsInstance(r["laplace_expected_squared_error"],F)
    def test_mle_can_have_better_mse_than_laplace(self):
        # At the symmetric midpoint, smoothing can improve risk; no global claim.
        a,_=load_source_and_validate()
        r=exact_risks(a("BIN",8,F(1,2),0),8,F(1,2))
        self.assertNotEqual(r["laplace_expected_squared_error"],r["mle_expected_squared_error"])
    def test_fixed_external_true_probability(self):
        p=F(1,4)
        self.assertEqual(F(3,12),p)
    def test_source_unchanged_expected_blob(self):
        raw=(R177/"r177_four_finite_count_families_exact.py").read_bytes()
        self.assertEqual(git_blob(raw),ORIGINAL_SOURCE_SHA1)
    def test_invalid_training_pmf_fails(self):
        with self.assertRaises(ValueError):
            exact_risks([F(1),F(1)],1,F(1,2))
    def test_wald_multipler_exact(self):
        self.assertEqual(WALD_MULT,F(49,25))
    def test_full_scenario_source_names_unique(self):
        self.assertEqual(len({x[0] for x in SOURCES}),5)


if __name__=="__main__":
    if sys.argv[1:]==["--test"]:
        unittest.main(argv=[sys.argv[0]],verbosity=2)
    elif sys.argv[1:]==["--run-and-archive"]:
        run()
        archive()
    else:
        raise SystemExit("Use --test or --run-and-archive")
