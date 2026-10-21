"""R180 exact bootstrap conditional laws and actual frequentist coverage.

30 source worlds, 7750 ordered samples of 2..4 independent four-trial clusters.
Both bootstrap conditional distributions are enumerated by two independent
algorithms and all original sampling probabilities are exact Fraction values.
Original social observations are not used. Dependencies: Python standard lib.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from functools import lru_cache
from fractions import Fraction as F
from hashlib import sha1, sha256
from itertools import product
from math import comb
from pathlib import Path
import csv
import json
import sys
import unittest
import zipfile

HERE = Path(__file__).resolve().parent
R177 = HERE.parent / "R177"
PROTO = HERE.parent.parent / "protocols/R180_CLUSTER_BOOTSTRAP_30_WORLDS_7750_SAMPLES_PRESCORE_FREEZE_2026-10-21.md"
RESULT = HERE / "R180_EXACT_RESULTS.json"
LIBRARY = HERE / "R180_ALL_CONDITIONAL_BOOTSTRAP_PMF_LIBRARY.json"
SAMPLES = HERE / "R180_ALL_7750_ORDERED_SAMPLES.csv"
ACCEPT = HERE / "R180_FINAL_MACHINE_ACCEPTANCE.json"
ARCHIVE = HERE / "R180_Exact_Bootstrap_30_Worlds_7750_Samples.zip"
R177_BLOB = "2d032513ce84141214b6b3f84df9c0ed9976a02b"
R177_RESULT_SHA256 = "57410cf2c110ce3117b7af72e4b7473cee0c3ffd013e6fb99fd43de62165a535"
CLUSTERS = (2, 3, 4)
TRUE_RATES = (F(1, 4), F(1, 2))
SOURCE_TYPES = (
    ("IID_BIN", "BIN", 0),
    ("CLUSTERED_BB_C2", "BB", 0),
    ("CLUSTERED_BB_C8", "BB", 2),
    ("INACTIVE_ZIB_Z1_8", "ZIB", 0),
    ("INACTIVE_ZIB_Z1_4", "ZIB", 1),
)
N_PER_CLUSTER = 4
Z = F(49, 25)
LOWER = F(1, 40)
UPPER = F(39, 40)


def original_source():
    py = (R177 / "r177_four_finite_count_families_exact.py").read_bytes()
    blob = sha1(b"blob " + str(len(py)).encode() + b"\x00" + py).hexdigest()
    if blob != R177_BLOB:
        raise ValueError("pinned R177 program Git blob changed")
    if sha256((R177 / "R177_EXACT_RESULTS.json").read_bytes()).hexdigest() != R177_RESULT_SHA256:
        raise ValueError("pinned R177 complete result SHA256 changed")
    if str(R177) not in sys.path:
        sys.path.insert(0, str(R177))
    from r177_four_finite_count_families_exact import formula_pmf, event_dp
    return formula_pmf, event_dp


def configurations():
    for m, p, source in product(CLUSTERS, TRUE_RATES, SOURCE_TYPES):
        yield m, p, *source


def pmf_moments(pmf):
    if sum(pmf, F(0)) != 1 or any(x < 0 for x in pmf):
        raise AssertionError("probabilities invalid")
    mean = sum((j * q for j, q in enumerate(pmf)), F(0))
    variance = sum(((F(j) - mean) ** 2 * q for j, q in enumerate(pmf)), F(0))
    return mean, variance


def iid_formula(counts):
    """Conditional IID bootstrap A: closed binomial formula."""
    m = len(counts)
    n = N_PER_CLUSTER * m
    phat = F(sum(counts), n)
    return tuple(F(comb(n, j)) * phat ** j * (1 - phat) ** (n - j)
                 for j in range(n + 1))


def iid_sequential(counts):
    """Conditional IID bootstrap B: direct one-trial count dynamic program."""
    n = len(counts) * N_PER_CLUSTER
    q = F(sum(counts), n)
    dist = {0: F(1)}
    for _ in range(n):
        updated = defaultdict(F)
        for j, weight in dist.items():
            updated[j] += weight * (1 - q)
            updated[j + 1] += weight * q
        dist = updated
    return tuple(dist.get(j, F(0)) for j in range(n + 1))


def cluster_enumeration(counts):
    """Conditional cluster bootstrap A: all ordered resampled cluster IDs."""
    m = len(counts)
    if m not in CLUSTERS:
        raise ValueError("cluster count outside frozen design")
    dist = defaultdict(int)
    for picks in product(range(m), repeat=m):
        total = sum(counts[index] for index in picks)
        dist[total] += 1
    return tuple(F(dist[k], m ** m) for k in range(m * N_PER_CLUSTER + 1))


def cluster_sequential(counts):
    """Conditional cluster bootstrap B: m stages of empirical count DP."""
    m = len(counts)
    if m not in CLUSTERS:
        raise ValueError("cluster count outside frozen design")
    dist = {0: F(1)}
    for _ in range(m):
        updated = defaultdict(F)
        for count, weight in dist.items():
            for observed in counts:
                updated[count + observed] += weight / m
        dist = updated
    return tuple(dist.get(k, F(0)) for k in range(m * N_PER_CLUSTER + 1))


def percentile_index(pmf, alpha):
    if not (F(0) < alpha < F(1)):
        raise ValueError("percentile invalid")
    accum = F(0)
    for index, val in enumerate(pmf):
        accum += val
        if accum >= alpha:
            return index
    raise AssertionError("CDF failed to reach percentile")


def variance_of_rate(pmf, sample_trials):
    _, v = pmf_moments(pmf)
    return v / sample_trials ** 2


@lru_cache(maxsize=None)
def conditional(counts):
    """Caches exact identical conditional bootstrap laws by unordered group data."""
    if counts != tuple(sorted(counts)) or len(counts) not in CLUSTERS:
        raise ValueError("expected sorted cluster-count tuple")
    if any(k not in range(5) for k in counts):
        raise ValueError("invalid four-trial cluster count")
    N = len(counts) * N_PER_CLUSTER
    p_hat = F(sum(counts), N)
    iid1 = iid_formula(counts)
    iid2 = iid_sequential(counts)
    c1 = cluster_enumeration(counts)
    c2 = cluster_sequential(counts)
    if iid1 != iid2 or c1 != c2:
        raise AssertionError("independent exhaustive bootstrap routes disagree")
    iid_v = variance_of_rate(iid1, N)
    c_v = variance_of_rate(c1, N)
    c_adj = c_v * F(len(counts), len(counts) - 1)
    iid_analytic = p_hat * (1 - p_hat) / N
    group_second = sum((k * k for k in counts), F(0)) / len(counts)
    group_mean = F(sum(counts), len(counts))
    c_analytic = (group_second - group_mean ** 2) / (len(counts) * N_PER_CLUSTER ** 2)
    if iid_v != iid_analytic or c_v != c_analytic:
        raise AssertionError("bootstrap full laws disagree with analytic variances")
    il, ih = percentile_index(iid1, LOWER), percentile_index(iid1, UPPER)
    cl, ch = percentile_index(c1, LOWER), percentile_index(c1, UPPER)
    return {
        "counts": counts, "sample_rate": p_hat,
        "iid_pmf": iid1, "cluster_pmf": c1,
        "iid_var": iid_v, "cluster_var": c_v, "corrected_cluster_var": c_adj,
        "iid_percentile": (F(il, N), F(ih, N)),
        "cluster_percentile": (F(cl, N), F(ch, N)),
    }


def coverage(p_hat, truth, variance, lower, upper):
    return (
        (p_hat - truth) ** 2 <= Z ** 2 * variance,
        lower <= truth <= upper
    )


def sample_checks(counts, truth):
    a = conditional(tuple(sorted(counts)))
    p = a["sample_rate"]
    iid_normal, iid_percentile = coverage(
        p, truth, a["iid_var"], *a["iid_percentile"]
    )
    cluster_normal, cluster_percentile = coverage(
        p, truth, a["corrected_cluster_var"], *a["cluster_percentile"]
    )
    return {
        **a,
        "iid_wald_cover": iid_normal,
        "cluster_corrected_wald_cover": cluster_normal,
        "iid_percentile_cover": iid_percentile,
        "cluster_percentile_cover": cluster_percentile,
    }


def serialize_sample(m, p, name, counts, prob, measures):
    return {
        "cluster_count_m": str(m),
        "source": name,
        "true_p": str(p),
        "ordered_group_K": ",".join(map(str, counts)),
        "true_sample_probability": str(prob),
        "observed_p_hat": str(measures["sample_rate"]),
        "iid_bootstrap_variance": str(measures["iid_var"]),
        "cluster_bootstrap_variance": str(measures["cluster_var"]),
        "cluster_finite_m_corrected_variance": str(measures["corrected_cluster_var"]),
        "iid_2p5_percentile": str(measures["iid_percentile"][0]),
        "iid_97p5_percentile": str(measures["iid_percentile"][1]),
        "cluster_2p5_percentile": str(measures["cluster_percentile"][0]),
        "cluster_97p5_percentile": str(measures["cluster_percentile"][1]),
        "iid_wald_cover": int(measures["iid_wald_cover"]),
        "cluster_corrected_wald_cover": int(measures["cluster_corrected_wald_cover"]),
        "iid_percentile_cover": int(measures["iid_percentile_cover"]),
        "cluster_percentile_cover": int(measures["cluster_percentile_cover"]),
        "conditional_bootstrap_profile": ",".join(map(str, sorted(counts))),
    }


def evaluate_world(m, p, name, family, regime, origin_pmf, saved_rows):
    mean_k, var_k = pmf_moments(origin_pmf)
    if mean_k != N_PER_CLUSTER * p:
        raise AssertionError("source marginal mean wrong")
    true_variance = var_k / (N_PER_CLUSTER ** 2 * m)
    total_mass = F(0)
    mean_hat = F(0)
    mse = F(0)
    mean_iid_var = F(0)
    mean_cluster_var = F(0)
    mean_adjusted_var = F(0)
    zeros = F(0)
    measures = {
        "iid_wald": F(0), "cluster_corrected_wald": F(0),
        "iid_percentile": F(0), "cluster_percentile": F(0)
    }
    count_rows = 0
    for ordered in product(range(N_PER_CLUSTER + 1), repeat=m):
        prob = F(1)
        for val in ordered:
            prob *= origin_pmf[val]
        checked = sample_checks(ordered, p)
        count_rows += 1
        total_mass += prob
        observed = checked["sample_rate"]
        mean_hat += prob * observed
        mse += prob * (observed - p) ** 2
        mean_iid_var += prob * checked["iid_var"]
        mean_cluster_var += prob * checked["cluster_var"]
        mean_adjusted_var += prob * checked["corrected_cluster_var"]
        zeros += prob * int(checked["cluster_var"] == 0)
        for key, condition in (
            ("iid_wald", "iid_wald_cover"),
            ("cluster_corrected_wald", "cluster_corrected_wald_cover"),
            ("iid_percentile", "iid_percentile_cover"),
            ("cluster_percentile", "cluster_percentile_cover"),
        ):
            measures[key] += prob * int(checked[condition])
        saved_rows.append(serialize_sample(m, p, name, ordered, prob, checked))
    if total_mass != 1 or mean_hat != p or mse != true_variance:
        raise AssertionError("underlying true clustered sampling law invalid")
    if mean_cluster_var != F(m - 1, m) * true_variance:
        raise AssertionError("ordinary cluster bootstrap variance is not finite-sample biased by (m-1)/m")
    if mean_adjusted_var != true_variance:
        raise AssertionError("finite-group corrected bootstrap variance not unbiased")
    if mean_iid_var != (p * (1 - p) - true_variance) / (m * N_PER_CLUSTER):
        raise AssertionError("IID bootstrap variance expected value mismatch")
    if zeros != sum((v ** m for v in origin_pmf), F(0)):
        raise AssertionError("identical-cluster degenerate bootstrap mass mismatch")
    if count_rows != (N_PER_CLUSTER + 1) ** m:
        raise AssertionError("wrong ordered sample universe")
    return {
        "m":m,"n_per_cluster":N_PER_CLUSTER,
        "true_p":str(p),"source":name,"source_family":family,
        "source_regime":regime,
        "source_count_pmf":[str(v) for v in origin_pmf],
        "ordered_dataset_count":count_rows,
        "true_sampling_variance_of_p_hat":str(true_variance),
        "true_MSE_of_p_hat":str(mse),
        "expected_iid_bootstrap_variance":str(mean_iid_var),
        "expected_cluster_bootstrap_variance":str(mean_cluster_var),
        "expected_corrected_cluster_bootstrap_variance":str(mean_adjusted_var),
        "ratio_expected_iid_bootstrap_variance_to_true_variance":str(mean_iid_var/true_variance),
        "probability_of_identical_cluster_counts_and_zero_cluster_variance":str(zeros),
        "exact_interval_frequentist_coverages":{
            k:str(val) for k,val in measures.items()
        },
        "independent_conditional_bootstrap_methods_all_agreed":True,
    }


def emit_csv(rows):
    if len(rows)!=7750:
        raise AssertionError("ordered dataset output count drifted")
    names=list(rows[0])
    with SAMPLES.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=names,lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def emit_library():
    profiles=[]
    for m in CLUSTERS:
        for counts in product(range(5),repeat=m):
            if counts != tuple(sorted(counts)):
                continue
            data=conditional(counts)
            profiles.append({
                "cluster_count_m":m,
                "sorted_observed_group_K":list(counts),
                "iid_bootstrap_total_success_PMF":[str(x) for x in data["iid_pmf"]],
                "cluster_bootstrap_total_success_PMF":[str(x) for x in data["cluster_pmf"]],
                "iid_bootstrap_rate_variance":str(data["iid_var"]),
                "cluster_bootstrap_rate_variance":str(data["cluster_var"]),
                "independent_enumeration_and_DP_fraction_equal":True,
            })
    if len(profiles)!=120:
        raise AssertionError("number of unique unordered group-count profiles drifted")
    LIBRARY.write_text(json.dumps({
        "research_id":"R180","unique_unordered_sample_profiles":len(profiles),
        "profiles":profiles,
        "full_distributions_exact_and_conditional":True
    },sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return len(profiles)


def run():
    formula, sequential = original_source()
    saved_rows=[]
    results=[]
    for m,p,name,family,regime in configurations():
        pmf=formula(family,N_PER_CLUSTER,p,regime)
        if pmf!=sequential(family,N_PER_CLUSTER,p,regime):
            raise AssertionError("source formula and individual-event algorithm differ")
        results.append(evaluate_world(m,p,name,family,regime,pmf,saved_rows))
    if len(results)!=30 or len(saved_rows)!=7750:
        raise AssertionError("not the prescored source universe")
    emit_csv(saved_rows)
    profiles=emit_library()
    selected=[r for r in results if r["m"]==4 and r["true_p"]=="1/4"]
    if len(selected)!=5:
        raise AssertionError("missing any locked main comparison")
    main={
        "research_id":"R180",
        "status":"E1_ARTIFICIAL_FULL_SAMPLE_SPACE_EXACT_BOOTSTRAP",
        "protocol":"protocols/"+PROTO.name,
        "source_R177_git_blob":R177_BLOB,
        "source_R177_results_sha256":R177_RESULT_SHA256,
        "world_count":len(results),
        "complete_ordered_sample_count":len(saved_rows),
        "unique_conditional_bootstrap_sample_profiles":profiles,
        "no_monte_carlo_random_draws":True,
        "all_conditional_bootstrap_methods_exactly_equal":True,
        "finite_m_unbiased_corrected_cluster_variance_all_worlds":True,
        "IID_and_CLUSTER_methods_have_distinct_coverage_and_resampling_laws":True,
        "preselected_m4_p_quarter_comparison":selected,
        "all_worlds":results,
        "ordered_sample_csv_sha256":sha256(SAMPLES.read_bytes()).hexdigest(),
        "conditional_full_PMF_library_sha256":sha256(LIBRARY.read_bytes()).hexdigest(),
        "human_or_historical_data_scored":False,"new_E2":0,"new_E3":0,
    }
    RESULT.write_text(json.dumps(main,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    acceptance={
        "research_id":"R180",
        "state":"CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_BOOTSTRAP",
        "world_count":30,"ordered_samples":7750,
        "full_conditional_bootstrap_profiles":120,
        "independent_IID_formula_event_DP":True,
        "independent_cluster_sequence_enumeration_DP":True,
        "corrected_cluster_variance_unbiased_in_all_worlds":True,
        "all_four_interval_coverage_rates_full_source_enumeration":True,
        "source_R177_SHA_authenticated":True,
        "result_sha256":sha256(RESULT.read_bytes()).hexdigest(),
        "ordered_sample_csv_sha256":main["ordered_sample_csv_sha256"],
        "conditional_PMF_library_sha256":main["conditional_full_PMF_library_sha256"],
        "no_real_human_or_historical_scoring":True,"new_E2":0,"new_E3":0,
    }
    ACCEPT.write_text(json.dumps(acceptance,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("R180_MACHINE_ACCEPTANCE",json.dumps(acceptance,sort_keys=True))
    print("R180_LOCKED_MAIN_COMPARISON",json.dumps(selected,sort_keys=True))
    return main


def archive():
    files=[Path(__file__).name,RESULT.name,LIBRARY.name,SAMPLES.name,ACCEPT.name]
    with zipfile.ZipFile(ARCH,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name in files:
            info=zipfile.ZipInfo(name,date_time=(2026,10,21,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o644<<16
            z.writestr(info,(HERE/name).read_bytes())
        info=zipfile.ZipInfo(PROTO.name,date_time=(2026,10,21,0,0,0))
        info.compress_type=zipfile.ZIP_DEFLATED
        info.external_attr=0o644<<16
        z.writestr(info,PROTO.read_bytes())
    print("R180_ARCHIVE_SHA256",sha256(ARCH.read_bytes()).hexdigest())


class TestExactBootstrap(unittest.TestCase):
    def test_world_count_30(self):
        self.assertEqual(len(list(configurations())),30)
    def test_all_sample_count_7750(self):
        self.assertEqual(sum(5**m for m,p,n,f,r in configurations()),7750)
    def test_exact_four_trials_per_cluster(self):
        self.assertEqual(N_PER_CLUSTER,4)
    def test_source_sha_and_dual_exact_path(self):
        a,b=original_source()
        self.assertEqual(a("BB",4,F(1,4),0),b("BB",4,F(1,4),0))
    def test_iid_full_conditional_analytic_vs_DP(self):
        for m in CLUSTERS:
            for counts in product(range(5),repeat=m):
                if counts==tuple(sorted(counts)):
                    self.assertEqual(iid_formula(counts),iid_sequential(counts))
    def test_cluster_full_conditional_ID_vs_DP(self):
        for m in CLUSTERS:
            for counts in product(range(5),repeat=m):
                if counts==tuple(sorted(counts)):
                    self.assertEqual(cluster_enumeration(counts),cluster_sequential(counts))
    def test_all_PMF_positive_and_normalized(self):
        for m in CLUSTERS:
            for counts in product(range(5),repeat=m):
                if counts==tuple(sorted(counts)):
                    r=conditional(counts)
                    self.assertEqual(sum(r["iid_pmf"]),1)
                    self.assertEqual(sum(r["cluster_pmf"]),1)
                    self.assertTrue(all(v>=0 for v in r["cluster_pmf"]))
    def test_cluster_four_trial_index_enumeration(self):
        self.assertEqual(cluster_enumeration((0,4)),(F(1,4),0,0,0,F(1,2),0,0,0,F(1,4)))
    def test_cluster_example_variance(self):
        self.assertEqual(conditional((0,4))["cluster_var"],F(1,8))
    def test_cluster_variance_finite_m_correction(self):
        self.assertEqual(conditional((0,4))["corrected_cluster_var"],F(1,4))
    def test_iid_example_variance(self):
        self.assertEqual(conditional((0,4))["iid_var"],F(1,32))
    def test_identical_counts_cluster_degeneracy(self):
        c=conditional((2,2,2))
        self.assertEqual(c["cluster_var"],0)
        self.assertGreater(c["iid_var"],0)
    def test_zero_samples_both_degenerate(self):
        c=conditional((0,0))
        self.assertEqual(c["iid_var"],0)
        self.assertEqual(c["cluster_var"],0)
    def test_identical_nontruth_cluster_coverage_false(self):
        c=sample_checks((2,2,2),F(1,4))
        self.assertFalse(c["cluster_corrected_wald_cover"])
        self.assertFalse(c["cluster_percentile_cover"])
    def test_unit_mass_for_each_real_source(self):
        a,b=original_source()
        for m,p,n,f,r in configurations():
            self.assertEqual(sum(a(f,4,p,r)),1)
            self.assertEqual(a(f,4,p,r),b(f,4,p,r))
    def test_source_mean_4p(self):
        a,_=original_source()
        for m,p,n,f,r in configurations():
            self.assertEqual(pmf_moments(a(f,4,p,r))[0],4*p)
    def test_analytical_variance_from_bootstrap_PMF(self):
        for counts in ((0,4),(1,3,4),(0,1,3,4),(2,2,2,2)):
            r=conditional(tuple(sorted(counts)))
            m=len(counts); N=m*4
            self.assertEqual(r["iid_var"],r["sample_rate"]*(1-r["sample_rate"])/N)
    def test_percentile_cdf_minimum(self):
        self.assertEqual(percentile_index((F(1,10),F(9,10)),F(1,40)),0)
        self.assertEqual(percentile_index((F(1,10),F(9,10)),F(39,40)),1)
    def test_percentile_pmf_out_of_bounds(self):
        with self.assertRaises(ValueError):
            percentile_index((F(1),),F(0))
    def test_source_cluster_expected_variance_identity_one_world(self):
        a,_=original_source()
        rows=[]
        e=evaluate_world(3,F(1,4),"IID_BIN","BIN",0,a("BIN",4,F(1,4),0),rows)
        self.assertEqual(e["true_sampling_variance_of_p_hat"],e["expected_corrected_cluster_bootstrap_variance"])
    def test_all_true_variance_finite_and_positive(self):
        a,_=original_source()
        for m,p,n,f,r in configurations():
            self.assertGreater(pmf_moments(a(f,4,p,r))[1]/(16*m),0)
    def test_invalid_cluster_tuple(self):
        with self.assertRaises(ValueError):
            conditional((0,5))
    def test_unsorted_tuples_fail_closed(self):
        with self.assertRaises(ValueError):
            conditional((3,1))
    def test_confidence_exact_integer_comparison(self):
        c=sample_checks((0,4),F(1,2))
        self.assertTrue(c["iid_wald_cover"])
        self.assertTrue(c["cluster_corrected_wald_cover"])
    def test_zero_variance_probability_positive(self):
        a,_=original_source()
        p=a("BB",4,F(1,4),0)
        self.assertGreater(sum((q**4 for q in p),F(0)),0)
    def test_repeated_original_counts_conditional_identity(self):
        self.assertEqual(conditional((0,1,3))["cluster_pmf"],
                         conditional(tuple(sorted((3,0,1))))["cluster_pmf"])
    def test_wrong_percentile_high_rejected(self):
        with self.assertRaises(ValueError):
            percentile_index((F(1),),F(1))


if __name__=="__main__":
    if sys.argv[1:]==["--test"]:
        unittest.main(argv=[sys.argv[0]],verbosity=2)
    elif sys.argv[1:]==["--run-and-archive"]:
        run();archive()
    else:
        raise SystemExit("usage: --test or --run-and-archive")
