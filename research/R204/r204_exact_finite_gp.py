#!/usr/bin/env python3
"""R204: exact finite Gaussian-process kernel selection audit with heldout latent sites.

True data sources are finite independent Rademacher latent factors and observed
noise, NOT Gaussian. Gaussian GP formulas and marginal likelihood are fixed
working-model predictors. All arithmetic involving risks uses Fraction.

python r204_exact_finite_gp.py --test
python r204_exact_finite_gp.py --emit
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import math
import unittest
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

F = Fraction
Z = F(0)
O = F(1)
SITES = (0, 1, 2, 3, 4)
T = (F(-2), F(-1), Z, O, F(2))
KERNELS = ("IID", "CONSTANT", "ALTERNATING", "LINEAR")
SPLITS = {
    "EXTRAPOLATION": ((0, 1, 2), (3, 4)),
    "INTERPOLATION": ((0, 2, 4), (1, 3)),
    "GAP": ((0, 1, 4), (2, 3)),
}
NOISES = tuple(tuple(F(z) for z in seq) for seq in itertools.product((-1, 1), repeat=3))
OUT = Path(__file__).resolve().parent


def features(kernel):
    if kernel == "IID":
        return tuple(tuple(O if i == j else Z for i in SITES) for j in SITES)
    if kernel == "CONSTANT":
        return (tuple(O for _ in SITES),)
    if kernel == "ALTERNATING":
        return (tuple(O if i % 2 == 0 else -O for i in SITES),)
    if kernel == "LINEAR":
        return (T,)
    raise ValueError("unknown kernel")


def latent_paths(kernel):
    return tuple(tuple(F(z) for z in path)
                 for path in itertools.product((-1, 1), repeat=len(features(kernel))))


def signal(kernel, latent_factors):
    phi = features(kernel)
    if len(latent_factors) != len(phi) or any(z not in (-O, O) for z in latent_factors):
        raise ValueError("wrong latent factor count or support")
    return tuple(sum((phi[j][i] * latent_factors[j] for j in range(len(phi))), Z)
                 for i in SITES)


def kernel_matrix(kernel):
    phi = features(kernel)
    return tuple(tuple(sum((f[i]*f[j] for f in phi), Z) for j in SITES)
                 for i in SITES)


def submatrix(a, rows, cols):
    return tuple(tuple(a[i][j] for j in cols) for i in rows)


def transpose(a):
    return tuple(tuple(a[i][j] for i in range(len(a))) for j in range(len(a[0])))


def mm(a, b):
    if len(a[0]) != len(b):
        raise ValueError("incompatible matrices")
    return tuple(tuple(sum((a[i][k]*b[k][j] for k in range(len(b))), Z)
                       for j in range(len(b[0]))) for i in range(len(a)))


def mv(a, x):
    return tuple(sum((a[i][j]*x[j] for j in range(len(x))), Z) for i in range(len(a)))


def sqmean(a, b):
    if len(a) != 2 or len(b) != 2:
        raise ValueError("exactly two heldout sites")
    return sum(((a[j]-b[j])**2 for j in range(2)), Z) / 2


def trace(a):
    if len(a) != len(a[0]):
        raise ValueError("square matrix required")
    return sum((a[i][i] for i in range(len(a))), Z)


def eye(n):
    return tuple(tuple(O if i==j else Z for j in range(n)) for i in range(n))


def add(a, b):
    return tuple(tuple(a[i][j]+b[i][j] for j in range(len(a[0])))
                 for i in range(len(a)))


def subtract(a, b):
    return tuple(tuple(a[i][j]-b[i][j] for j in range(len(a[0])))
                 for i in range(len(a)))


def gauss_inverse(a):
    n=len(a)
    if not a or any(len(row)!=n for row in a):
        raise ValueError("square matrix required")
    ident=eye(n)
    m=[[a[i][j] for j in range(n)]+[ident[i][j] for j in range(n)] for i in range(n)]
    for j in range(n):
        ix=next((z for z in range(j,n) if m[z][j]),None)
        if ix is None:
            raise ValueError("singular matrix")
        m[j],m[ix]=m[ix],m[j]
        d=m[j][j]
        m[j]=[v/d for v in m[j]]
        for i in range(n):
            if i!=j:
                v=m[i][j]
                m[i]=[m[i][k]-v*m[j][k] for k in range(2*n)]
    return tuple(tuple(m[i][n:]) for i in range(n))


def det3(a):
    if len(a)!=3 or any(len(r)!=3 for r in a):
        raise ValueError("det3 requires 3-by-3")
    return (a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])
           -a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])
           +a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]))


def adjugate_inverse3(a):
    det=det3(a)
    if det==0:
        raise ValueError("singular")
    cof=[]
    for i in range(3):
        line=[]
        for j in range(3):
            others=[r for r in range(3) if r!=i]
            columns=[c for c in range(3) if c!=j]
            minor=a[others[0]][columns[0]]*a[others[1]][columns[1]]-a[others[0]][columns[1]]*a[others[1]][columns[0]]
            line.append(((-1)**(i+j))*minor)
        cof.append(tuple(line))
    return tuple(tuple(transpose(cof)[i][j]/det for j in range(3)) for i in range(3))


def training_cov(kernel, train):
    k=kernel_matrix(kernel)
    return add(submatrix(k, train, train), eye(3))


def candidate_inverse(kernel, train):
    cov=training_cov(kernel,train)
    a=gauss_inverse(cov)
    b=adjugate_inverse3(cov)
    if a!=b or mm(cov,a)!=eye(3) or mm(a,cov)!=eye(3):
        raise AssertionError("independent Fraction matrix inverses differ")
    return a


def logdet_double(cov):
    d=det3(cov)
    if d<=0:
        raise AssertionError("not positive definite GP training covariance")
    ordinary=math.log(float(d))
    with localcontext() as ctx:
        ctx.prec=70
        precise=(Decimal(d.numerator)/Decimal(d.denominator)).ln()
    if abs(ordinary-float(precise))>1e-11:
        raise AssertionError("logdet double route disagreement")
    return ordinary


def gaussian_train_nll(kernel,train,y):
    cov=training_cov(kernel,train)
    inv=candidate_inverse(kernel,train)
    quad=sum((y[i]*mv(inv,y)[i] for i in range(3)),Z)
    return 0.5*(3*math.log(2*math.pi)+logdet_double(cov)+float(quad))


def choose_kernel(train,y):
    scores=[gaussian_train_nll(k,train,y) for k in KERNELS]
    best=min(scores)
    return KERNELS[next(i for i,v in enumerate(scores) if v<=best+1e-12)]


def posterior_projection(kernel,train,test):
    k=kernel_matrix(kernel)
    return mm(submatrix(k,test,train),candidate_inverse(kernel,train))


def posterior_mean(kernel,train,test,y):
    return mv(posterior_projection(kernel,train,test),y)


def gp_work_posterior_cov(kernel,train,test):
    k=kernel_matrix(kernel)
    b=posterior_projection(kernel,train,test)
    return subtract(submatrix(k,test,test),mm(b,submatrix(k,train,test)))


def exact_fixed_candidate_future_mse(true_kernel, candidate, train, test):
    true_k=kernel_matrix(true_kernel)
    b=posterior_projection(candidate,train,test)
    k_ss=submatrix(true_k,test,test)
    k_ts=submatrix(true_k,train,test)
    ctt=training_cov(true_kernel,train)
    cross=mm(b,k_ts)
    variance=mm(mm(b,ctt),transpose(b))
    analytical=(trace(k_ss)-2*trace(cross)+trace(variance))/2
    original=Z
    for latent in latent_paths(true_kernel):
        sig=signal(true_kernel,latent)
        fstar=tuple(sig[i] for i in test)
        for noise in NOISES:
            y=tuple(sig[train[i]]+noise[i] for i in range(3))
            pred=mv(b,y)
            original+=sqmean(fstar,pred) / (len(latent_paths(true_kernel))*len(NOISES))
    if analytical!=original:
        raise AssertionError("independent finite original source risk and GP moment risk differ")
    if candidate==true_kernel:
        expected=trace(gp_work_posterior_cov(candidate,train,test))/2
        if analytical!=expected:
            raise AssertionError("GP true-kernel linear prediction variance identity failed")
    return analytical


def compute():
    result_worlds=[]
    records=[]
    for split,(train,test) in SPLITS.items():
        if set(train).intersection(test) or sorted(train+test)!=list(SITES):
            raise AssertionError("illegal train heldout split")
        for source in KERNELS:
            choices={k:Z for k in KERNELS}
            expectation=Z
            fixed_risk={k:exact_fixed_candidate_future_mse(source,k,train,test)
                        for k in KERNELS}
            latent=latent_paths(source)
            source_weight=F(1,len(latent)*len(NOISES))
            for factor in latent:
                whole=signal(source,factor)
                fstar=tuple(whole[i] for i in test)
                for noise in NOISES:
                    y=tuple(whole[train[i]]+noise[i] for i in range(3))
                    chosen=choose_kernel(train,y)
                    pred=posterior_mean(chosen,train,test,y)
                    err=sqmean(fstar,pred)
                    expectation+=source_weight*err
                    choices[chosen]+=source_weight
                    records.append({
                        "split":split,
                        "true_kernel_source":source,
                        "observed_training_site_ids":"|".join(map(str,train)),
                        "heldout_test_site_ids":"|".join(map(str,test)),
                        "true_source_latent_factors":"|".join(map(str,factor)),
                        "true_observation_noise":"|".join(map(str,noise)),
                        "real_original_source_probability":str(source_weight),
                        "observed_train_y":"|".join(map(str,y)),
                        "heldout_true_latent_f":"|".join(map(str,fstar)),
                        "training_gaussian_work_nll_IID":format(gaussian_train_nll("IID",train,y),".14f"),
                        "training_gaussian_work_nll_CONSTANT":format(gaussian_train_nll("CONSTANT",train,y),".14f"),
                        "training_gaussian_work_nll_ALTERNATING":format(gaussian_train_nll("ALTERNATING",train,y),".14f"),
                        "training_gaussian_work_nll_LINEAR":format(gaussian_train_nll("LINEAR",train,y),".14f"),
                        "fitted_kernel_from_training_only":chosen,
                        "heldout_latent_predicted_mean":"|".join(map(str,pred)),
                        "heldout_latent_MSE_two_sites_exact":str(err),
                    })
            assert sum(choices.values(),Z)==1
            oracle=fixed_risk[source]
            assert oracle<=min(fixed_risk.values())
            zero_baseline=trace(submatrix(kernel_matrix(source),test,test))/2
            result_worlds.append({
                "split":split,
                "train_site_ids":list(train),
                "heldout_site_ids":list(test),
                "true_kernel":source,
                "all_ordered_original_source_records":len(latent)*len(NOISES),
                "source_probability_sum":"1",
                "selected_kernel_probability":{k:str(choices[k]) for k in KERNELS},
                "selected_true_kernel_probability":str(choices[source]),
                "selected_kernel_heldout_latent_MSE_exact":str(expectation),
                "selected_kernel_heldout_latent_MSE":round(float(expectation),12),
                "precommitted_zero_prediction_MSE_exact":str(zero_baseline),
                "true_kernel_optimal_linear_MSE_exact":str(oracle),
                "best_fixed_candidate_linear_MSE_exact":str(min(fixed_risk.values())),
            })
    assert len(result_worlds)==12 and len(records)==912
    diagnostics={
        "all_kernels_generated_by_explicit_finite_features":True,
        "IID_zero_correlation_between_disjoint_train_and_test": all(
            posterior_projection("IID",*SPLITS[split]) ==
            ((Z,Z,Z),(Z,Z,Z)) for split in SPLITS
        ),
        "true_kernels_linear_oracle_is_not_exact_discrete_Bayes_posterior":True,
        "observational_noise_variance_fixed":1,
        "source_latent_factors_real_distribution":"Rademacher ±1 independent, finite non-Gaussian",
        "working_training_marginal_likelihood":"Gaussian kernel model, misspecified for true discrete sources",
    }
    return {
        "research_id":"R204",
        "status":"ARTIFICIAL_E1_AWAIT_CI_ACCEPTANCE",
        "true_sources_and_working_candidates":list(KERNELS),
        "splits":{name:{"train":list(a),"heldout":list(b)} for name,(a,b) in SPLITS.items()},
        "full_original_observed_and_heldout_records":len(records),
        "complete_source_worlds":len(result_worlds),
        "new_real_human_E2":0,
        "new_real_historical_E3":0,
        "worlds":result_worlds,
        "diagnostics":diagnostics,
    },records


def emit():
    result,rows=compute()
    result_path=OUT/"R204_EXACT_RESULTS.json"
    csv_path=OUT/"R204_ALL_912_REAL_SOURCE_GP_TRAIN_AND_HELDOUT.csv"
    result_path.write_text(json.dumps(result,sort_keys=True,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    with csv_path.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    accepted={
        "model_id":"R204",
        "worlds":12,
        "all_original_finite_source_rows":912,
        "all_gp_matrix_inverses_two_Fraction_methods":True,
        "all_fixed_kernel_holdout_risks_two_Fraction_methods":True,
        "new_E2":0,
        "new_E3":0,
        "results_sha256":hashlib.sha256(result_path.read_bytes()).hexdigest(),
        "all_original_source_sha256":hashlib.sha256(csv_path.read_bytes()).hexdigest(),
    }
    (OUT/"R204_FINAL_MACHINE_ACCEPTANCE.json").write_text(
        json.dumps(accepted,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(accepted,indent=2))


class Tests(unittest.TestCase):
    def test_kernels_count(self):
        self.assertEqual(len(KERNELS),4)

    def test_positions_count(self):
        self.assertEqual(len(SITES),5)

    def test_splits_count(self):
        self.assertEqual(len(SPLITS),3)

    def test_splits_disjoint_full(self):
        for train,test in SPLITS.values():
            self.assertEqual(sorted(train+test),list(SITES))
            self.assertFalse(set(train)&set(test))

    def test_training_noise_count(self):
        self.assertEqual(len(NOISES),8)

    def test_iod_sources_count(self):
        self.assertEqual(len(latent_paths("IID")),32)

    def test_feature_rank_one_path_count(self):
        for k in KERNELS[1:]:
            self.assertEqual(len(latent_paths(k)),2)

    def test_original_records_total(self):
        self.assertEqual(3*(32*8+3*2*8),912)

    def test_kernel_positive_diagonal(self):
        for k in KERNELS:
            self.assertTrue(all(kernel_matrix(k)[i][i]>=0 for i in SITES))

    def test_kernel_is_symmetric(self):
        for k in KERNELS:
            self.assertEqual(kernel_matrix(k),transpose(kernel_matrix(k)))

    def test_kernel_iid_identity(self):
        self.assertEqual(kernel_matrix("IID"),eye(5))

    def test_constant_kernel(self):
        self.assertEqual(kernel_matrix("CONSTANT"),tuple((O,)*5 for _ in SITES))

    def test_alternating_negative_neighbor_cov(self):
        self.assertEqual(kernel_matrix("ALTERNATING")[0][1],-O)

    def test_linear_kernel_center_zero(self):
        self.assertTrue(all(v==0 for v in kernel_matrix("LINEAR")[2]))

    def test_true_latent_iid_covariance_by_exhaustive_paths(self):
        paths=latent_paths("IID")
        self.assertEqual(
            tuple(tuple(sum((signal("IID",z)[i]*signal("IID",z)[j] for z in paths),Z)/len(paths)
                        for j in SITES) for i in SITES),eye(5))

    def test_true_latent_lowrank_covariance_by_exhaustive_paths(self):
        for k in KERNELS[1:]:
            paths=latent_paths(k)
            recovered=tuple(tuple(sum((signal(k,z)[i]*signal(k,z)[j] for z in paths),Z)/len(paths)
                                  for j in SITES) for i in SITES)
            self.assertEqual(recovered,kernel_matrix(k))

    def test_double_inverse_consistency(self):
        for k in KERNELS:
            for train,_ in SPLITS.values():
                self.assertEqual(gauss_inverse(training_cov(k,train)),
                                 adjugate_inverse3(training_cov(k,train)))

    def test_each_covariance_positive_determinant(self):
        for k in KERNELS:
            for train,_ in SPLITS.values():
                self.assertGreater(det3(training_cov(k,train)),0)

    def test_marginal_work_score_finite(self):
        for train,_ in SPLITS.values():
            for k in KERNELS:
                self.assertTrue(math.isfinite(gaussian_train_nll(k,train,(Z,O,-O))))

    def test_fixed_kernel_forecast_two_exact_routes(self):
        for split in SPLITS.values():
            for source in KERNELS:
                for forecast in KERNELS:
                    self.assertGreaterEqual(exact_fixed_candidate_future_mse(
                        source,forecast,*split),0)

    def test_correct_kernel_optimal_linear(self):
        for train,test in SPLITS.values():
            for true in KERNELS:
                risks=[exact_fixed_candidate_future_mse(true,q,train,test) for q in KERNELS]
                self.assertEqual(risks[KERNELS.index(true)],min(risks))

    def test_iid_heldout_b_of_zero(self):
        for train,test in SPLITS.values():
            self.assertEqual(posterior_projection("IID",train,test),((Z,Z,Z),(Z,Z,Z)))

    def test_iid_true_latent_zero_prediction_risk(self):
        for train,test in SPLITS.values():
            self.assertEqual(exact_fixed_candidate_future_mse("IID","IID",train,test),O)

    def test_gp_mean_given_zero_input(self):
        train,test=SPLITS["EXTRAPOLATION"]
        for k in KERNELS:
            self.assertEqual(posterior_mean(k,train,test,(Z,Z,Z)),(Z,Z))

    def test_gp_posterior_cov_symmetry(self):
        for train,test in SPLITS.values():
            for k in KERNELS:
                self.assertEqual(gp_work_posterior_cov(k,train,test),
                                 transpose(gp_work_posterior_cov(k,train,test)))

    def test_no_future_used_in_kernel_selection(self):
        train,test=SPLITS["INTERPOLATION"]
        y=(F(1),F(-1),F(2))
        self.assertEqual(choose_kernel(train,y),choose_kernel(train,y))

    def test_reject_unknown_kernel(self):
        with self.assertRaises(ValueError):
            features("UNKNOWN")

    def test_reject_invalid_latent_factor(self):
        with self.assertRaises(ValueError):
            signal("CONSTANT",(Z,))

    def test_reject_incompatible_matrix_shapes(self):
        with self.assertRaises(ValueError):
            mm(((O,O),),((O,),))

    def test_all_original_worlds_and_sources(self):
        result,rows=compute()
        self.assertEqual((len(result["worlds"]),len(rows)),(12,912))
        self.assertTrue(all(w["source_probability_sum"]=="1" for w in result["worlds"]))

    def test_full_deterministic_replay(self):
        self.assertEqual(compute(),compute())


if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--test",action="store_true")
    parser.add_argument("--emit",action="store_true")
    a=parser.parse_args()
    if a.test:
        ok=unittest.TextTestRunner(verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
        raise SystemExit(0 if ok.wasSuccessful() else 1)
    if a.emit:
        emit()
    if not a.test and not a.emit:
        parser.print_help()
