"""R190 exact 5-knot second-difference Gaussian identity-link smoother.

Ten artificial binary ±1 source worlds, 1375 exact 5-position training count
tables, four frozen smoothing penalties each. Every fitted smooth uses rational
primal 5x5 and dual 3x3 solvers. Future independently sampled squared loss
uses full-source enumeration and a separate analytic bias/variance formula.
Not a full B-spline GAM and not a binary likelihood or classification study.
"""
from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from itertools import product
from math import comb
from pathlib import Path
import csv,json,sys,unittest,zipfile

HERE=Path(__file__).resolve().parent
PROTO=HERE.parent.parent/"protocols/R190_DISCRETE_GAM_10_WORLDS_1375_TABLES_PRESCORE_FREEZE_2026-10-21.md"
RESULT=HERE/"R190_EXACT_RESULTS.json"
CSV=HERE/"R190_ALL_1375_ARTIFICIAL_SMOOTHING_TRAINING_TABLES.csv"
MATRICES=HERE/"R190_ALL_8_FRACTION_SMOOTHING_MATRICES.json"
ACCEPT=HERE/"R190_FINAL_MACHINE_ACCEPTANCE.json"
ARCH=HERE/"R190_Exact_10_Discrete_GAM_Smoothing_Worlds.zip"

N_VALUES=(1,2)
LAMBDAS=(F(0),F(1),F(4),F(16))
D=(
 (F(1),F(-2),F(1),F(0),F(0)),
 (F(0),F(1),F(-2),F(1),F(0)),
 (F(0),F(0),F(1),F(-2),F(1)),
)
SOURCES=(
 ("FLAT",(F(1,2),)*5),
 ("LINEAR",(F(1,4),F(3,8),F(1,2),F(5,8),F(3,4))),
 ("HUMP",(F(1,4),F(1,2),F(3,4),F(1,2),F(1,4))),
 ("VALLEY",(F(3,4),F(1,2),F(1,4),F(1,2),F(3,4))),
 ("ALTERNATE",(F(1,4),F(3,4),F(1,4),F(3,4),F(1,4))),
)


def worlds():
    for (name,prob),n in product(SOURCES,N_VALUES):
        yield name,prob,n


def binary_pmf_closed(n,p):
    if n not in N_VALUES or not F(0)<p<F(1):
        raise ValueError("invalid artificial training count source")
    return tuple(F(comb(n,k))*p**k*(1-p)**(n-k) for k in range(n+1))


def binary_pmf_dp(n,p):
    if n not in N_VALUES or not F(0)<p<F(1):
        raise ValueError("invalid source count")
    dist={0:F(1)}
    for _ in range(n):
        nxt=defaultdict(F)
        for k,weight in dist.items():
            nxt[k]+=weight*(1-p)
            nxt[k+1]+=weight*p
        dist=nxt
    return tuple(dist.get(k,F(0)) for k in range(n+1))


def matrix_transpose(A):
    return tuple(zip(*A))


def multiply(A,B):
    if not A or not B or len(A[0])!=len(B):
        raise ValueError("wrong multiplication shape")
    return tuple(tuple(sum((u*v for u,v in zip(row,col)),F(0))
                       for col in matrix_transpose(B)) for row in A)


def matvec(A,v):
    return tuple(sum((a*b for a,b in zip(row,v)),F(0)) for row in A)


def identity(n):
    return tuple(tuple(F(int(i==j)) for j in range(n)) for i in range(n))


def solve(A,b):
    """Fraction Gauss-Jordan, reject missing rank."""
    n=len(b)
    if n not in (3,5) or len(A)!=n or any(len(row)!=n for row in A):
        raise ValueError("invalid 3x3 or 5x5 normal equation")
    augmented=[[F(a) for a in row]+[F(b[i])] for i,row in enumerate(A)]
    for j in range(n):
        pivot=next((i for i in range(j,n) if augmented[i][j]!=0),None)
        if pivot is None:
            raise ValueError("rank deficient smoothing design")
        augmented[j],augmented[pivot]=augmented[pivot],augmented[j]
        scale=augmented[j][j]
        augmented[j]=[v/scale for v in augmented[j]]
        for i in range(n):
            if i==j:continue
            d=augmented[i][j]
            augmented[i]=[v-d*w for v,w in zip(augmented[i],augmented[j])]
    return tuple(row[-1] for row in augmented)


def curvature_penalty():
    return multiply(matrix_transpose(D),D)


@lru_cache(maxsize=None)
def normal_matrix(n,lam):
    if n not in N_VALUES or lam not in LAMBDAS:
        raise ValueError("sample size or penalty outside freeze")
    penalty=curvature_penalty()
    return tuple(tuple(n*F(int(i==j))+lam*penalty[i][j] for j in range(5))
                 for i in range(5))


def primal_smooth(n,lam,ybar):
    if len(ybar)!=5:
        raise ValueError("five source locations required")
    return solve(normal_matrix(n,lam),tuple(n*y for y in ybar))


def dual_smooth(n,lam,ybar):
    """Independent 3x3 Woodbury-type formula for 5-position fitted response."""
    if n not in N_VALUES or lam not in LAMBDAS or len(ybar)!=5:
        raise ValueError("unregistered smoothing input")
    if lam==0:
        return tuple(ybar)
    dd=multiply(D,matrix_transpose(D))
    system=tuple(tuple(dd[i][j]+F(n,1)/lam*F(int(i==j))
                       for j in range(3)) for i in range(3))
    deltas=matvec(D,ybar)
    penalty_correction=solve(system,deltas)
    adjustment=matvec(matrix_transpose(D),penalty_correction)
    return tuple(y-d for y,d in zip(ybar,adjustment))


@lru_cache(maxsize=None)
def smooth_matrix(n,lam):
    if n not in N_VALUES or lam not in LAMBDAS:
        raise ValueError("invalid frozen matrix")
    columns=[]
    for j in range(5):
        source=tuple(F(int(i==j)) for i in range(5))
        columns.append(primal_smooth(n,lam,source))
    s=tuple(zip(*columns))
    for j in range(5):
        source=tuple(F(int(i==j)) for i in range(5))
        if matvec(s,source)!=dual_smooth(n,lam,source):
            raise AssertionError("smoother matrix dual basis identity fails")
    linear=tuple(F(i) for i in range(5))
    ones=(F(1),)*5
    if matvec(s,linear)!=linear or matvec(s,ones)!=ones:
        raise AssertionError("unpenalized constant and linear basis not preserved")
    return s


def fit_three_routes(n,lam,ybar):
    a=primal_smooth(n,lam,ybar)
    b=dual_smooth(n,lam,ybar)
    c=matvec(smooth_matrix(n,lam),ybar)
    if a!=b or b!=c:
        raise AssertionError("three independent smoothing paths differ")
    if lam==0 and a!=tuple(ybar):
        raise AssertionError("zero penalty must interpolate group sample means")
    return a


def source_probabilities(n,pvec):
    sources=tuple(binary_pmf_closed(n,p) for p in pvec)
    if any(a!=binary_pmf_dp(n,p) for a,p in zip(sources,pvec)):
        raise AssertionError("original two Bernoulli-count source methods differ")
    return sources


def training_mass(observed,prob):
    q=F(1)
    for k,pmf in zip(observed,prob):
        q*=pmf[k]
    return q


def true_mu_var(pvec):
    mean=tuple(2*p-F(1) for p in pvec)
    variance=tuple(4*p*(1-p) for p in pvec)
    return mean,variance


def future_mse(f,mu,variance):
    return sum((v+(m-pred)**2 for v,m,pred in zip(variance,mu,f)),F(0))/5


def analytic_future_mse(n,lam,pvec):
    """A truly independent bias/variance expression for NEW ±1 response."""
    mu,variance=true_mu_var(pvec)
    smooth=smooth_matrix(n,lam)
    predicted_mean=matvec(smooth,mu)
    return sum(
        (variance[i]+(mu[i]-predicted_mean[i])**2+
         sum((smooth[i][j]**2*variance[j]/n for j in range(5)),F(0)))
        for i in range(5)
    )/5


def run_world(name,pvec,n,all_records):
    law=source_probabilities(n,pvec)
    mu,variance=true_mu_var(pvec)
    mass_total=F(0)
    full_scores={lam:F(0) for lam in LAMBDAS}
    full_count=0
    for observed in product(range(n+1),repeat=5):
        mass=training_mass(observed,law)
        mass_total+=mass
        ybar=tuple(F(2*k-n,n) for k in observed)
        vals={}
        for lam in LAMBDAS:
            fit=fit_three_routes(n,lam,ybar)
            err=future_mse(fit,mu,variance)
            full_scores[lam]+=mass*err
            vals[str(lam)]={
                "fit":[str(v) for v in fit],
                "future_NEW_sample_expected_MSE":str(err),
            }
        full_count+=1
        all_records.append({
            "source":name,"n_trials_per_x":n,
            "training_count_table":",".join(map(str,observed)),
            "true_joint_training_mass":str(mass),
            "observed_five_training_mean_responses":",".join(map(str,ybar)),
            **{f"lambda_{lam}_fitted_five_response_values":",".join(vals[str(lam)]["fit"]) for lam in LAMBDAS},
            **{f"lambda_{lam}_future_NEW_sample_MSE":vals[str(lam)]["future_NEW_sample_expected_MSE"] for lam in LAMBDAS},
        })
    if mass_total!=1 or full_count!=(n+1)**5:
        raise AssertionError("complete original sample probability not one")
    analytic={lam:analytic_future_mse(n,lam,pvec) for lam in LAMBDAS}
    if full_scores!=analytic:
        raise AssertionError("full exact enumeration and independent bias/variance risk disagree")
    true_curvature=matvec(D,mu)
    return {
        "source":name,"n_trials_per_x":n,
        "source_true_p_plus_one":[str(v) for v in pvec],
        "source_true_conditional_means":[str(v) for v in mu],
        "source_true_conditional_variances":[str(v) for v in variance],
        "source_true_second_differences":[str(v) for v in true_curvature],
        "true_curve_has_zero_second_difference":all(v==0 for v in true_curvature),
        "ordered_training_tables":full_count,
        "lambda_expected_independent_NEW_response_MSE_exact":{str(lam):str(full_scores[lam]) for lam in LAMBDAS},
        "exact_enum_and_independent_analytic_bias_variance_equal":True
    }


def run():
    all_records=[]
    worlds_out=[run_world(name,p,n,all_records) for name,p,n in worlds()]
    if len(worlds_out)!=10 or len(all_records)!=1375:
        raise AssertionError("frozen 10-world 1375-table universe changed")
    with CSV.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(all_records[0]),lineterminator="\n")
        writer.writeheader()
        writer.writerows(all_records)
    matrices=[]
    for n,lam in product(N_VALUES,LAMBDAS):
        s=smooth_matrix(n,lam)
        matrices.append({
            "n":n,"lambda":str(lam),
            "exact_5x5_smoothing_matrix":[[str(x) for x in row] for row in s],
            "all_primal_dual_and_mapping_routes_agree":True,
            "unpenalized_linear_and_constant_trends_unchanged":True
        })
    MATRICES.write_text(json.dumps({
        "research_id":"R190","matrix_count":len(matrices),"matrices":matrices
    },sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    anchors=[v for v in worlds_out if v["n_trials_per_x"]==1 and v["source"] in ("FLAT","ALTERNATE","LINEAR","HUMP")]
    if len(anchors)!=4 or not next(v for v in anchors if v["source"]=="FLAT")["true_curve_has_zero_second_difference"] or next(v for v in anchors if v["source"]=="ALTERNATE")["true_curve_has_zero_second_difference"]:
        raise AssertionError("locked flat vs alternating truth identification failed")
    results={
        "research_id":"R190","status":"E1_ARTIFICIAL_IDENTITY_LINK_FIVE_POSITION_SMOOTH",
        "world_count":10,"complete_training_count_tables":1375,
        "exact_primal_dual_and_linear_operator_fits":1375*4,
        "smoothing_matrix_count":8,"lambda_grid":[str(v) for v in LAMBDAS],
        "all_source_closed_binomial_and_event_DP_agree":True,
        "all_future_risk_original_sample_enumeration_and_bias_variance_equal":True,
        "all_full_Fraction_primal_dual_and_S_matrix_equal":True,
        "fixed_n1_flat_vs_nonlinear_truth":anchors,
        "worlds":worlds_out,
        "all_original_train_CSV_sha256":sha256(CSV.read_bytes()).hexdigest(),
        "all_smoother_matrices_sha256":sha256(MATRICES.read_bytes()).hexdigest(),
        "actual_human_or_historical_data":False,"new_E2":0,"new_E3":0
    }
    RESULT.write_text(json.dumps(results,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    accept={
        "research_id":"R190","status":"CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_DISCRETE_GAM",
        "worlds":10,"complete_count_training_tables":1375,
        "exact_smoothing_coefficients":5500,"unique_smoother_matrices":8,
        "original_Bernoulli_source_PMF_two_methods_equal":True,
        "five_by_five_primal_three_by_three_dual_and_S_mapping_equal":True,
        "heldout_new_response_squared_loss_full_enum_and_analytic_exact":True,
        "fixed_flat_vs_alternate_bias_variance_cases_retained":True,
        "result_sha256":sha256(RESULT.read_bytes()).hexdigest(),
        "original_source_CSV_sha256":results["all_original_train_CSV_sha256"],
        "smoothing_matrix_library_sha256":results["all_smoother_matrices_sha256"],
        "actual_human_or_historical_data":False,"new_E2":0,"new_E3":0
    }
    ACCEPT.write_text(json.dumps(accept,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("R190_MACHINE_ACCEPTANCE",json.dumps(accept,sort_keys=True))
    print("R190_LOCKED_FLAT_VS_NONLINEAR",json.dumps(anchors,sort_keys=True))
    return results


def archive():
    names=[Path(__file__).name,RESULT.name,CSV.name,MATRICES.name,ACCEPT.name]
    with zipfile.ZipFile(ARCH,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name in names:
            info=zipfile.ZipInfo(name,date_time=(2026,10,21,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o644<<16
            z.writestr(info,(HERE/name).read_bytes())
        info=zipfile.ZipInfo(PROTO.name,date_time=(2026,10,21,0,0,0))
        info.compress_type=zipfile.ZIP_DEFLATED
        info.external_attr=0o644<<16
        z.writestr(info,PROTO.read_bytes())
    print("R190_ARCHIVE_SHA256",sha256(ARCH.read_bytes()).hexdigest())


class TestFiniteGAMSmoothing(unittest.TestCase):
    def test_ten_worlds(self):
        self.assertEqual(len(list(worlds())),10)
    def test_1375_original_training_tables(self):
        self.assertEqual(sum((n+1)**5 for name,p,n in worlds()),1375)
    def test_five_locations(self):
        self.assertTrue(all(len(p)==5 for name,p in SOURCES))
    def test_four_locked_penalties(self):
        self.assertEqual(LAMBDAS,(0,1,4,16))
    def test_three_second_difference_rows(self):
        self.assertEqual(len(D),3)
    def test_second_diff_flat_zero(self):
        self.assertEqual(matvec(D,(F(1),)*5),(F(0),)*3)
    def test_second_diff_linear_zero(self):
        self.assertEqual(matvec(D,tuple(F(i) for i in range(5))),(F(0),)*3)
    def test_alternating_curvature_nonzero(self):
        mu,_=true_mu_var(SOURCES[-1][1])
        self.assertTrue(any(v!=0 for v in matvec(D,mu)))
    def test_all_true_binomial_pmf_closed_vs_dp(self):
        for name,p,n in worlds():
            for q in p:
                self.assertEqual(binary_pmf_closed(n,q),binary_pmf_dp(n,q))
    def test_all_origin_probability_normalized(self):
        for name,p,n in worlds():
            laws=source_probabilities(n,p)
            self.assertEqual(sum((training_mass(k,laws) for k in product(range(n+1),repeat=5)),F(0)),1)
    def test_smoothing_matrix_exact_all(self):
        for n,lam in product(N_VALUES,LAMBDAS):
            s=smooth_matrix(n,lam)
            self.assertEqual(len(s),5)
            self.assertTrue(all(len(row)==5 for row in s))
    def test_lambda_zero_identity_mapping(self):
        for n in N_VALUES:
            self.assertEqual(smooth_matrix(n,F(0)),identity(5))
    def test_primal_dual_all_training_profiles(self):
        for name,p,n in worlds():
            for counts in product(range(n+1),repeat=5):
                y=tuple(F(2*k-n,n) for k in counts)
                for lam in LAMBDAS:
                    self.assertEqual(primal_smooth(n,lam,y),dual_smooth(n,lam,y))
    def test_full_three_paths_all_training_profiles(self):
        for name,p,n in worlds():
            for counts in product(range(n+1),repeat=5):
                y=tuple(F(2*k-n,n) for k in counts)
                for lam in LAMBDAS:
                    fit_three_routes(n,lam,y)
    def test_flat_source_no_true_smoothing_bias(self):
        mu,_=true_mu_var(SOURCES[0][1])
        for n,lam in product(N_VALUES,LAMBDAS):
            self.assertEqual(matvec(smooth_matrix(n,lam),mu),mu)
    def test_linear_source_no_true_smoothing_bias(self):
        mu,_=true_mu_var(SOURCES[1][1])
        for n,lam in product(N_VALUES,LAMBDAS):
            self.assertEqual(matvec(smooth_matrix(n,lam),mu),mu)
    def test_alternate_true_smoothing_bias_positive(self):
        mu,_=true_mu_var(SOURCES[-1][1])
        for n in N_VALUES:
            for lam in LAMBDAS[1:]:
                self.assertNotEqual(matvec(smooth_matrix(n,lam),mu),mu)
    def test_all_world_exact_bias_variance_with_full_enumeration(self):
        for name,p,n in worlds():
            laws=source_probabilities(n,p)
            mu,v=true_mu_var(p)
            for lam in LAMBDAS:
                total=sum((
                    training_mass(k,laws)*future_mse(
                        fit_three_routes(n,lam,tuple(F(2*x-n,n) for x in k)),mu,v)
                    for k in product(range(n+1),repeat=5)
                ),F(0))
                self.assertEqual(total,analytic_future_mse(n,lam,p))
    def test_lambda_zero_future_risk_known(self):
        for name,p,n in worlds():
            mu,v=true_mu_var(p)
            self.assertEqual(analytic_future_mse(n,F(0),p),sum(v,F(0))/5*(1+F(1,n)))
    def test_higher_penalty_reduces_curvature_single_profile(self):
        v=(F(1),F(-1),F(1),F(-1),F(1))
        def curvature(x):
            return sum((q*q for q in matvec(D,x)),F(0))
        self.assertLess(curvature(primal_smooth(1,F(16),v)),curvature(primal_smooth(1,F(0),v)))
    def test_penalty_matrix_symmetry(self):
        m=curvature_penalty()
        self.assertEqual(m,matrix_transpose(m))
    def test_penalty_matrix_zero_on_linear(self):
        self.assertEqual(matvec(curvature_penalty(),tuple(F(i) for i in range(5))),(F(0),)*5)
    def test_original_synthetic_binary_variance(self):
        mu,v=true_mu_var((F(1,4),)*5)
        self.assertEqual(mu,(F(-1,2),)*5)
        self.assertEqual(v,(F(3,4),)*5)
    def test_invalid_source_n(self):
        with self.assertRaises(ValueError):
            binary_pmf_closed(3,F(1,2))
    def test_invalid_source_p(self):
        with self.assertRaises(ValueError):
            binary_pmf_dp(1,F(0))
    def test_invalid_lambda(self):
        with self.assertRaises(ValueError):
            smooth_matrix(2,F(3))
    def test_invalid_smoothing_input(self):
        with self.assertRaises(ValueError):
            primal_smooth(1,F(1),(F(1),))
    def test_singular_normal_rejected(self):
        with self.assertRaises(ValueError):
            solve(((1,0,0),(0,1,0),(0,0,0)),(1,1,1))
    def test_eight_precise_matrices(self):
        self.assertEqual(len([smooth_matrix(n,lam) for n,lam in product(N_VALUES,LAMBDAS)]),8)
    def test_future_MSE_nonnegative(self):
        mu,v=true_mu_var(SOURCES[2][1])
        self.assertGreaterEqual(future_mse(mu,mu,v),0)


if __name__=="__main__":
    if sys.argv[1:]==["--test"]:
        unittest.main(argv=[sys.argv[0]],verbosity=2)
    elif sys.argv[1:]==["--run-and-archive"]:
        run();archive()
    else:
        raise SystemExit("Usage --test or --run-and-archive")
