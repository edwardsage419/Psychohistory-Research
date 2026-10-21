"""R186 source-authenticated finite zero-inflation inference and identifiability.

Exact rational ZIB versus Binomial grid likelihoods on all 40 artificial worlds
and 1860 ordered training count arrays. Original R177 count PMFs are verified
by two distinct sources. All heldout cross entropy uses an independent new
group count, with math.log and Decimal.ln cross-validation. No E2/E3 data.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from decimal import Decimal, localcontext
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha1,sha256
from itertools import product,combinations_with_replacement
from math import comb,factorial,log
from pathlib import Path
import csv,json,sys,unittest,zipfile

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/"R177"
PROTO=HERE.parent.parent/"protocols/R186_ZERO_INFLATED_40_WORLDS_1860_SAMPLES_PRESCORE_FREEZE_2026-10-21.md"
OUT=HERE/"R186_EXACT_RESULTS.json"
SAMPLES=HERE/"R186_ALL_1860_ORDERED_TRAINING_SAMPLES.csv"
PROFILES=HERE/"R186_ALL_66_FIT_PROFILES.json"
ACCEPT=HERE/"R186_FINAL_MACHINE_ACCEPTANCE.json"
ARCH=HERE/"R186_Zero_Inflation_40_Worlds_Exact_Archive.zip"
R177_BLOB="2d032513ce84141214b6b3f84df9c0ed9976a02b"
R177_RESULTS="57410cf2c110ce3117b7af72e4b7473cee0c3ffd013e6fb99fd43de62165a535"

N_VALUES=(2,4)
M_VALUES=(2,3)
P_VALUES=(F(1,4),F(1,2))
SOURCES=(
 ("IID_BIN","BIN",0,None),
 ("CLUSTERED_BB_C2","BB",0,None),
 ("CLUSTERED_BB_C8","BB",2,None),
 ("INACTIVE_ZIB_Z1_8","ZIB",0,F(1,8)),
 ("INACTIVE_ZIB_Z1_4","ZIB",1,F(1,4)),
)
Z_VALUES=(F(0),F(1,8),F(1,4),F(3,8),F(1,2))
Q_VALUES=tuple(F(j,12) for j in range(1,12))


def original_source():
    raw=(SOURCE/"r177_four_finite_count_families_exact.py").read_bytes()
    gitsha=sha1(b"blob "+str(len(raw)).encode()+b"\x00"+raw).hexdigest()
    if gitsha!=R177_BLOB:
        raise ValueError("R177 original Python source Git blob changed")
    if sha256((SOURCE/"R177_EXACT_RESULTS.json").read_bytes()).hexdigest()!=R177_RESULTS:
        raise ValueError("R177 original complete results SHA256 changed")
    if str(SOURCE) not in sys.path:
        sys.path.insert(0,str(SOURCE))
    from r177_four_finite_count_families_exact import formula_pmf,event_dp
    return formula_pmf,event_dp


def worlds():
    for n,m,p,source_spec in product(N_VALUES,M_VALUES,P_VALUES,SOURCES):
        name,family,regime,structural=source_spec
        yield n,m,p,name,family,regime,structural


def zib_formula(n,z,q):
    """Exact closed binomial mixture probability, including zero base mass."""
    if n not in N_VALUES or z not in Z_VALUES or q not in Q_VALUES:
        raise ValueError("candidate outside frozen zero-inflation grid")
    return tuple((z if k==0 else F(0))+
                 (1-z)*F(comb(n,k))*q**k*(1-q)**(n-k) for k in range(n+1))


def zib_event_dp(n,z,q):
    """Independent count-state sequential Bernoulli trials plus zero mixture."""
    if n not in N_VALUES or z not in Z_VALUES or q not in Q_VALUES:
        raise ValueError("candidate outside frozen zero-inflation grid")
    dist={0:F(1)}
    for _ in range(n):
        nxt=defaultdict(F)
        for count,weight in dist.items():
            nxt[count]+=(1-q)*weight
            nxt[count+1]+=q*weight
        dist=nxt
    return tuple((z if k==0 else F(0))+
                 (1-z)*dist.get(k,F(0)) for k in range(n+1))


@lru_cache(maxsize=None)
def candidate_law(n,z,q):
    direct=zib_formula(n,z,q)
    dynamic=zib_event_dp(n,z,q)
    if direct!=dynamic or sum(direct,F(0))!=1 or min(direct)<=0:
        raise AssertionError("candidate ZIB PMF mismatch or invalid")
    return direct


def iid_law(n,q):
    return candidate_law(n,F(0),q)


def likelihood_direct(observed,prob):
    likelihood=F(1)
    for k in observed:
        likelihood*=prob[k]
    return likelihood


def likelihood_histogram(observed,prob):
    likelihood=F(1)
    for k,count in Counter(observed).items():
        likelihood*=prob[k]**count
    return likelihood


def fit_profile(n,profile):
    """Strict deterministic finite grid likelihood fits and fit certificates."""
    if n not in N_VALUES or len(profile) not in M_VALUES:
        raise ValueError("unregistered profile size")
    if tuple(sorted(profile))!=tuple(profile) or any(k not in range(n+1) for k in profile):
        raise ValueError("count profile out of support or unsorted")
    iid_best=None
    zib_best=None
    for q in Q_VALUES:
        law=iid_law(n,q)
        a=likelihood_direct(profile,law)
        b=likelihood_histogram(profile,law)
        if a!=b:
            raise AssertionError("individual likelihood and histogram differs")
        if iid_best is None or a>iid_best[0]:
            iid_best=(a,q,law)
    # Candidate order is fixed z first, q second; ties retain first candidate.
    for z in Z_VALUES:
        for q in Q_VALUES:
            law=candidate_law(n,z,q)
            a=likelihood_direct(profile,law)
            b=likelihood_histogram(profile,law)
            if a!=b:
                raise AssertionError("ZIB candidate likelihood direct and histogram differ")
            if zib_best is None or a>zib_best[0]:
                zib_best=(a,z,q,law)
    il,iq,im=iid_best
    zl,zz,zq,zm=zib_best
    if zl<il or likelihood_direct(profile,zm)!=zl:
        raise AssertionError("nested ZIB likelihood must contain BIN")
    posterior_0=zz/zm[0]
    if not F(0)<=posterior_0<=F(1):
        raise AssertionError("posterior structural zero attribution invalid")
    return {
        "n":n,"m":len(profile),"profile":profile,
        "iid_grid_q":iq,
        "zib_grid_z":zz,"zib_grid_q":zq,
        "iid_training_max_likelihood":il,
        "zib_training_max_likelihood":zl,
        "zib_training_likelihood_improvement_nonnegative":True,
        "iid_fitted_full_PMF":im,"zib_fitted_full_PMF":zm,
        "zib_working_posterior_structural_given_zero":posterior_0,
        "independent_fraction_likelihood_and_two_PMF_routes_equal":True,
    }


@lru_cache(maxsize=None)
def fit_library():
    out={}
    for n,m in product(N_VALUES,M_VALUES):
        for profile in combinations_with_replacement(range(n+1),m):
            out[(n,profile)]=fit_profile(n,profile)
    if len(out)!=66:
        raise AssertionError("prescored 66 unordered conditional profile count drifted")
    return out


def cross_entropy_float(source_pmf,fitted_pmf):
    if len(source_pmf)!=len(fitted_pmf):
        raise ValueError("support sizes differ")
    return -sum(float(p)*log(float(q)) for p,q in zip(source_pmf,fitted_pmf))


def cross_entropy_decimal(source_pmf,fitted_pmf):
    if len(source_pmf)!=len(fitted_pmf):
        raise ValueError("support sizes differ")
    with localcontext() as ctx:
        ctx.prec=60
        return -sum((Decimal(p.numerator)/Decimal(p.denominator))*
                    (Decimal(q.numerator)/Decimal(q.denominator)).ln()
                    for p,q in zip(source_pmf,fitted_pmf))


def original_order_multiplicity(profile):
    den=1
    for count in Counter(profile).values():
        den*=factorial(count)
    return factorial(len(profile))//den


def fit_record_for_csv(fit):
    return {
        "selected_iid_q":str(fit["iid_grid_q"]),
        "selected_zib_z":str(fit["zib_grid_z"]),
        "selected_zib_q":str(fit["zib_grid_q"]),
        "iid_max_training_likelihood":str(fit["iid_training_max_likelihood"]),
        "zib_max_training_likelihood":str(fit["zib_training_max_likelihood"]),
        "model_implied_structural_posterior_given_zero":str(
            fit["zib_working_posterior_structural_given_zero"]),
    }


def evaluate_world(n,m,p,name,family,regime,structural,source_pmf,fit_cache,all_rows):
    total_mass=F(0)
    positive_z=F(0)
    model_structural_given_zero=F(0)
    iid_risk=0.0
    zib_risk=0.0
    iid_decimal=Decimal(0)
    zib_decimal=Decimal(0)
    strictly_better_training=F(0)
    sample_count=0
    # Training is m separate independent group counts. The fresh heldout group
    # also follows the same source PMF and is independent of the training.
    for observed in product(range(n+1),repeat=m):
        mass=F(1)
        for k in observed:
            mass*=source_pmf[k]
        fit=fit_cache[(n,tuple(sorted(observed)))]
        loss_i=cross_entropy_float(source_pmf,fit["iid_fitted_full_PMF"])
        loss_z=cross_entropy_float(source_pmf,fit["zib_fitted_full_PMF"])
        dec_i=cross_entropy_decimal(source_pmf,fit["iid_fitted_full_PMF"])
        dec_z=cross_entropy_decimal(source_pmf,fit["zib_fitted_full_PMF"])
        if abs(loss_i-float(dec_i))>1e-12 or abs(loss_z-float(dec_z))>1e-12:
            raise AssertionError("independent float versus decimal heldout cross entropy diverged")
        total_mass+=mass
        sample_count+=1
        iid_risk+=float(mass)*loss_i
        zib_risk+=float(mass)*loss_z
        decimal_mass=Decimal(mass.numerator)/Decimal(mass.denominator)
        iid_decimal+=decimal_mass*dec_i
        zib_decimal+=decimal_mass*dec_z
        positive_z+=mass*int(fit["zib_grid_z"]>0)
        model_structural_given_zero+=mass*fit["zib_working_posterior_structural_given_zero"]
        strictly_better_training+=mass*int(fit["zib_training_max_likelihood"]>fit["iid_training_max_likelihood"])
        all_rows.append({
            "model_source":name,
            "source_family":family,"source_regime":regime,
            "n":n,"m":m,"true_marginal_p":str(p),
            "ordered_training_K":",".join(map(str,observed)),
            "true_training_probability":str(mass),
            "sorted_conditional_profile":",".join(map(str,sorted(observed))),
            **fit_record_for_csv(fit),
            "heldout_iid_expected_logloss":format(loss_i,".16g"),
            "heldout_zib_expected_logloss":format(loss_z,".16g"),
        })
    if total_mass!=1 or sample_count!=(n+1)**m:
        raise AssertionError("artificial complete sample source probability not one")
    if abs(iid_risk-float(iid_decimal))>1e-12 or abs(zib_risk-float(zib_decimal))>1e-12:
        raise AssertionError("full expected heldout loss independent implementation mismatch")
    truth_structural=F(0) if structural is None else structural/source_pmf[0]
    if not F(0)<=truth_structural<=1:
        raise AssertionError("source structural posterior outside probability bounds")
    return {
        "n":n,"m":m,"true_marginal_p":str(p),
        "source":name,"source_family":family,"source_regime":regime,
        "source_full_count_PMF":[str(v) for v in source_pmf],
        "complete_ordered_training_samples":sample_count,
        "expected_independent_heldout_BIN_logloss":format(iid_risk,".16g"),
        "expected_independent_heldout_ZIB_logloss":format(zib_risk,".16g"),
        "ZIB_minus_BIN_independent_heldout_loss":format(zib_risk-iid_risk,".16g"),
        "probability_ZIB_fit_selects_nonzero_structural_z":str(positive_z),
        "probability_ZIB_training_likelihood_strictly_above_BIN":str(strictly_better_training),
        "expected_fitted_model_structural_posterior_given_new_observed_zero":str(model_structural_given_zero),
        "actual_source_structural_posterior_given_new_observed_zero":str(truth_structural),
        "independent_full_sample_and_decimal_score_consistency":True,
    }


def serialize_fit_library(fit_cache):
    entries=[]
    for key,fit in sorted(fit_cache.items()):
        n,profile=key
        entries.append({
            "n":n,"m":len(profile),"sorted_count_profile":list(profile),
            "ordered_profile_multiplicity":original_order_multiplicity(profile),
            **fit_record_for_csv(fit),
            "fitted_iid_full_PMF":[str(q) for q in fit["iid_fitted_full_PMF"]],
            "fitted_zib_full_PMF":[str(q) for q in fit["zib_fitted_full_PMF"]],
            "exact_two_likelihood_and_two_probability_methods_agree":True,
        })
    return {"research_id":"R186","profiles":entries,"unique_unordered_profiles":len(entries),
            "candidate_z":[str(v) for v in Z_VALUES],
            "candidate_q":[str(v) for v in Q_VALUES]}


def run():
    formula,dp=original_source()
    fits=fit_library()
    all_rows=[]
    world_out=[]
    for n,m,p,name,family,regime,structural in worlds():
        source_pmf=formula(family,n,p,regime)
        if source_pmf!=dp(family,n,p,regime):
            raise AssertionError("R177 frozen generative models disagree")
        world_out.append(evaluate_world(n,m,p,name,family,regime,structural,
                                        source_pmf,fits,all_rows))
    if len(world_out)!=40 or len(all_rows)!=1860:
        raise AssertionError("prescored world or complete ordered sample count drifted")
    aliases=[w for w in world_out if w["n"]==2 and w["true_marginal_p"]=="1/2"
             and w["source"] in ("CLUSTERED_BB_C2","INACTIVE_ZIB_Z1_4")]
    if len(aliases)!=4:
        raise AssertionError("two true mechanisms across two m must be present")
    by={(w["m"],w["source"]):w for w in aliases}
    for m in M_VALUES:
        bb=by[m,"CLUSTERED_BB_C2"]
        zi=by[m,"INACTIVE_ZIB_Z1_4"]
        if bb["source_full_count_PMF"]!=zi["source_full_count_PMF"] or bb["source_full_count_PMF"]!=["1/3"]*3:
            raise AssertionError("source observational alias full PMF no longer identical")
        for key in (
            "expected_independent_heldout_BIN_logloss",
            "expected_independent_heldout_ZIB_logloss",
            "ZIB_minus_BIN_independent_heldout_loss",
            "probability_ZIB_fit_selects_nonzero_structural_z",
            "expected_fitted_model_structural_posterior_given_new_observed_zero"):
            if bb[key]!=zi[key]:
                raise AssertionError("observationally identical sources got different inference")
        if bb["actual_source_structural_posterior_given_new_observed_zero"]!="0" or zi["actual_source_structural_posterior_given_new_observed_zero"]!="3/4":
            raise AssertionError("genuinely distinct latent zero mechanisms not retained")
    fields=list(all_rows[0])
    with SAMPLES.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=fields,lineterminator="\n")
        writer.writeheader()
        writer.writerows(all_rows)
    library=serialize_fit_library(fits)
    PROFILES.write_text(json.dumps(library,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    main={
        "research_id":"R186",
        "stage":"E1_ARTIFICIAL_COMPLETE_FINITE_SAMPLE_ZERO_INFLATION_GRID",
        "protocol":"protocols/"+PROTO.name,
        "R177_original_git_blob":R177_BLOB,
        "R177_original_complete_results_sha256":R177_RESULTS,
        "worlds":40,"complete_ordered_training_datasets":1860,
        "unique_fit_profiles":66,
        "training_ZIB_is_strictly_nested_in_BIN_for_same_Q_grid":True,
        "all_source_R177_and_fitted_ZIB_independent_PMF_parity":True,
        "all_independent_numeric_future_scores_agreed":True,
        "BB_C2_and_ZIB_z_quarter_n2_full_observation_alias":True,
        "alias_source_comparisons_both_m":aliases,
        "all_worlds":world_out,
        "original_training_CSV_sha256":sha256(SAMPLES.read_bytes()).hexdigest(),
        "full_fit_profile_library_sha256":sha256(PROFILES.read_bytes()).hexdigest(),
        "no_real_human_or_historical_data_scored":True,
        "new_E2":0,"new_E3":0,
    }
    OUT.write_text(json.dumps(main,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    accept={
        "research_id":"R186","state":"CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_ZERO_INFLATION",
        "worlds":40,"original_ordered_samples":1860,
        "unique_exact_profile_fits":66,
        "authentic_R177_source_SHA_and_pmf_verified":True,
        "independent_ZIB_formula_and_trial_DP_all_candidates_equal":True,
        "both_exact_likelihood_product_and_count_histogram_routes_equal":True,
        "all_heldout_cross_entropy_math_and_decimal_routes_agree":True,
        "complete_R177_BB_vs_ZIB_count_alias_and_hidden_zero_truth_disagreement":True,
        "result_sha256":sha256(OUT.read_bytes()).hexdigest(),
        "ordered_training_CSV_sha256":main["original_training_CSV_sha256"],
        "profile_library_sha256":main["full_fit_profile_library_sha256"],
        "new_E2":0,"new_E3":0,"real_human_or_historical_data":False,
    }
    ACCEPT.write_text(json.dumps(accept,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("R186_ACCEPTANCE",json.dumps(accept,sort_keys=True))
    print("R186_FULL_IDENTIFIABILITY_ALIAS",json.dumps(aliases,sort_keys=True))
    return main


def archive():
    filenames=[Path(__file__).name,OUT.name,SAMPLES.name,PROFILES.name,ACCEPT.name]
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
    print("R186_ARCHIVE_SHA256",sha256(ARCH.read_bytes()).hexdigest())


class TestZeroInflation(unittest.TestCase):
    def test_40_worlds(self):
        self.assertEqual(len(list(worlds())),40)
    def test_1860_ordered_datasets(self):
        self.assertEqual(sum((n+1)**m for n,m,*rest in worlds()),1860)
    def test_66_sorted_fitted_profiles(self):
        self.assertEqual(len(fit_library()),66)
    def test_55_nested_candidates_per_n(self):
        self.assertEqual(len(Z_VALUES)*len(Q_VALUES),55)
    def test_source_SHA_and_independent_count_methods(self):
        a,b=original_source()
        self.assertEqual(a("BB",2,F(1,2),0),b("BB",2,F(1,2),0))
    def test_all_full_source_PMF_two_routes(self):
        a,b=original_source()
        for n,m,p,name,f,reg,z in worlds():
            self.assertEqual(a(f,n,p,reg),b(f,n,p,reg))
    def test_all_ZIB_full_PMF_formula_event_parity(self):
        for n in N_VALUES:
            for z,q in product(Z_VALUES,Q_VALUES):
                self.assertEqual(zib_formula(n,z,q),zib_event_dp(n,z,q))
    def test_all_nested_binomial_nonstruc(self):
        for n in N_VALUES:
            for q in Q_VALUES:
                self.assertEqual(iid_law(n,q),zib_formula(n,F(0),q))
    def test_all_candidates_strictly_positive(self):
        for n in N_VALUES:
            for z,q in product(Z_VALUES,Q_VALUES):
                self.assertTrue(all(v>0 for v in candidate_law(n,z,q)))
    def test_fitted_likelihood_histogram_direct_equal(self):
        for (n,profile),fit in fit_library().items():
            self.assertEqual(likelihood_direct(profile,fit["iid_fitted_full_PMF"]),
                             likelihood_histogram(profile,fit["iid_fitted_full_PMF"]))
            self.assertEqual(likelihood_direct(profile,fit["zib_fitted_full_PMF"]),
                             likelihood_histogram(profile,fit["zib_fitted_full_PMF"]))
    def test_full_nested_likelihood_bound(self):
        for fit in fit_library().values():
            self.assertGreaterEqual(fit["zib_training_max_likelihood"],
                                    fit["iid_training_max_likelihood"])
    def test_profile_multiplicity_total_ordered(self):
        for n,m in product(N_VALUES,M_VALUES):
            count=sum(original_order_multiplicity(profile)
                      for profile in combinations_with_replacement(range(n+1),m))
            self.assertEqual(count,(n+1)**m)
    def test_actual_training_source_probability_one(self):
        a,b=original_source()
        for n,m,p,name,f,reg,z in worlds():
            pmf=a(f,n,p,reg)
            self.assertEqual(sum((self._joint(q,pmf) for q in product(range(n+1),repeat=m)),F(0)),1)
    @staticmethod
    def _joint(observed,pmf):
        val=F(1)
        for k in observed:
            val*=pmf[k]
        return val
    def test_fixed_alias_full_PMF(self):
        a,b=original_source()
        self.assertEqual(a("BB",2,F(1,2),0),(F(1,3),)*3)
        self.assertEqual(a("ZIB",2,F(1,2),1),(F(1,3),)*3)
    def test_true_alias_latent_attribution_differs(self):
        a,b=original_source()
        q=a("ZIB",2,F(1,2),1)
        self.assertEqual(F(1,4)/q[0],F(3,4))
    def test_all_fitted_zero_posterior_in_unit(self):
        for fit in fit_library().values():
            self.assertTrue(0<=fit["zib_working_posterior_structural_given_zero"]<=1)
    def test_training_z_selection_can_be_nonzero_without_true_z(self):
        a,b=original_source()
        pmf=a("BB",2,F(1,2),0)
        total=F(0)
        for x in product(range(3),repeat=2):
            if fit_library()[(2,tuple(sorted(x)))]["zib_grid_z"]>0:
                total+=self._joint(x,pmf)
        self.assertGreater(total,0)
    def test_all_source_fit_loss_float_decimal_two_routes(self):
        a,b=original_source()
        for n,m,p,name,f,reg,z in worlds():
            true=a(f,n,p,reg)
            for profile in combinations_with_replacement(range(n+1),m):
                fit=fit_library()[(n,profile)]
                for key in ("iid_fitted_full_PMF","zib_fitted_full_PMF"):
                    self.assertAlmostEqual(cross_entropy_float(true,fit[key]),
                                           float(cross_entropy_decimal(true,fit[key])),places=12)
    def test_zero_inflated_candidate_hand(self):
        self.assertEqual(zib_formula(2,F(1,4),F(2,3)),(F(1,3),)*3)
    def test_same_source_not_observable_identified(self):
        a,b=original_source()
        pmf1=a("BB",2,F(1,2),0)
        pmf2=a("ZIB",2,F(1,2),1)
        for observed in product(range(3),repeat=3):
            self.assertEqual(self._joint(observed,pmf1),self._joint(observed,pmf2))
    def test_invalid_candidate_q_fail_closed(self):
        with self.assertRaises(ValueError):
            zib_formula(2,F(1,4),F(1,20))
    def test_invalid_candidate_z_fail_closed(self):
        with self.assertRaises(ValueError):
            zib_event_dp(2,F(1,16),F(1,2))
    def test_invalid_n_fail_closed(self):
        with self.assertRaises(ValueError):
            zib_formula(3,F(0),F(1,2))
    def test_invalid_unsorted_fit_fail_closed(self):
        with self.assertRaises(ValueError):
            fit_profile(2,(2,0))
    def test_invalid_likelihood_support_fail_closed(self):
        with self.assertRaises(IndexError):
            likelihood_direct((5,), (F(1),))
    def test_decimal_predictive_loss_strictly_finite(self):
        f=fit_library()[(2,(0,0))]
        self.assertGreater(cross_entropy_float((F(1,3),)*3,f["zib_fitted_full_PMF"]),0)
    def test_known_independent_binomial_hand_probability(self):
        self.assertEqual(zib_formula(2,F(0),F(1,2)),(F(1,4),F(1,2),F(1,4)))
    def test_source_alias_ordered_train_m2_m3(self):
        a,b=original_source()
        for m in M_VALUES:
            source1=a("BB",2,F(1,2),0)
            source2=a("ZIB",2,F(1,2),1)
            self.assertEqual(sum((self._joint(x,source1) for x in product(range(3),repeat=m)),F(0)),
                             sum((self._joint(x,source2) for x in product(range(3),repeat=m)),F(0)))
    def test_zero_predictive_loss_all_valid(self):
        f=fit_library()[(4,(0,0,0))]
        self.assertTrue(all(v>0 for v in f["zib_fitted_full_PMF"]))


if __name__=="__main__":
    if sys.argv[1:]==["--test"]:
        unittest.main(argv=[sys.argv[0]],verbosity=2)
    elif sys.argv[1:]==["--run-and-archive"]:
        run();archive()
    else:
        raise SystemExit("Use --test or --run-and-archive")
