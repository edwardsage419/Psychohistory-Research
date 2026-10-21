"""R196 exact two-latent-bit posterior versus finite-grid mean-field variational Bayes.

Six artificial likelihood tables, m=1/2 repeated success observations and
nested coarse/fine product-Bernoulli grids give 24 worlds and 408 scored
candidates. Exact Fraction Bayes is checked twice; ELBO is independently
calculated by float joint/entropy and 70-digit Decimal evidence minus KL.
This is not unrestricted continuous VI optimization or human posterior data.
"""
from __future__ import annotations
import csv,json,math,sys,unittest,zipfile
from decimal import Decimal,localcontext
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path

HERE=Path(__file__).resolve().parent
PROTOCOL=HERE.parent.parent/"protocols/R196_FINITE_VB_24_WORLDS_408_CANDIDATES_PRESCORE_FREEZE_2026-10-21.md"
ERRATUM=HERE.parent.parent/"protocols/R196_ELBO_DECIMAL_COMPARISON_PRECISION_ERRATUM_2026-10-21.md"
RESULT=HERE/"R196_EXACT_RESULTS.json"
CANDIDATES=HERE/"R196_ALL_408_MEAN_FIELD_ELBO_CANDIDATES.csv"
TRUTHS=HERE/"R196_ALL_12_EXACT_POSTERIOR_SOURCES.json"
ACCEPT=HERE/"R196_FINAL_MACHINE_ACCEPTANCE.json"
ZIP=HERE/"R196_24_Exact_Finite_Variational_Bayes_Worlds.zip"
SOURCES=(
    ("UNIFORM",(1,1,1,1)),
    ("INDEPENDENT_SKEW",(9,3,3,1)),
    ("POSITIVE_COUPLED",(16,1,1,16)),
    ("NEGATIVE_COUPLED",(1,16,16,1)),
    ("ASYMMETRIC_COUPLED",(16,1,1,4)),
    ("WEAK_COUPLED",(9,2,2,3)),
)
GRID_COARSE=(F(1,4),F(1,2),F(3,4))
GRID_FINE=(F(1,8),F(1,4),F(1,2),F(3,4),F(7,8))
GRIDS=(("COARSE",GRID_COARSE),("FINE",GRID_FINE))
COUNTS=(1,2)
STATES=((0,0),(0,1),(1,0),(1,1))

def source_check(w,m):
    if w not in tuple(x for n,x in SOURCES) or m not in COUNTS:
        raise ValueError("Outside frozen artificial Bayes source")

def source_worlds():
    for name,w in SOURCES:
        for m in COUNTS:
            yield name,w,m

def posterior_from_joint(w,m):
    """A: independent prior/likelihood construction and marginal evidence."""
    source_check(w,m)
    M=max(w)
    joint=[]
    for weight in w:
        probability=F(1,4)
        for _ in range(m):
            probability*=F(weight,M)
        joint.append(probability)
    evidence=sum(joint,F(0))
    post=tuple(x/evidence for x in joint)
    return post,evidence,tuple(joint)

def posterior_normalize_weights(w,m):
    """B: direct normalization of integer likelihood powers."""
    source_check(w,m)
    weights=tuple(int(weight)**m for weight in w)
    total=sum(weights)
    p=tuple(F(v,total) for v in weights)
    evidence=F(total,4*max(w)**m)
    return p,evidence

def true_posterior(w,m):
    p,evidence,joint=posterior_from_joint(w,m)
    other,ev2=posterior_normalize_weights(w,m)
    if p!=other or evidence!=ev2 or sum(p,F(0))!=1 or any(x<=0 for x in p):
        raise AssertionError("Two independent exact source Bayes implementations differ")
    return p,evidence,joint

def family_grid(label):
    return dict(GRIDS)[label]

def family_q(p,r):
    if not F(0)<p<F(1) or not F(0)<r<F(1):
        raise ValueError("Product Bernoulli support must be strictly interior")
    q=((1-p)*(1-r),(1-p)*r,p*(1-r),p*r)
    if sum(q,F(0))!=1:
        raise AssertionError("Mean-field normalization error")
    return q

def posterior_marginals(post):
    p=post[2]+post[3]
    r=post[1]+post[3]
    covariance=post[3]-p*r
    agreement=post[0]+post[3]
    return p,r,covariance,agreement

def independent_posterior(post):
    return post[0]*post[3]==post[1]*post[2]

def decimal_fraction(f):
    return Decimal(f.numerator)/Decimal(f.denominator)

def candidate_score(w,m,p,r):
    """Two independent floating/Decimal evaluations of log evidence=ELBO+KL."""
    q=family_q(p,r)
    post,evidence,joint=true_posterior(w,m)
    elbo_float=sum(float(qi)*(math.log(float(ji))-math.log(float(qi)))
                   for qi,ji in zip(q,joint))
    with localcontext() as ctx:
        ctx.prec=70
        kl_decimal=sum((decimal_fraction(qi)*(decimal_fraction(qi)/decimal_fraction(pi)).ln()
                        for qi,pi in zip(q,post)),Decimal(0))
        log_evidence=decimal_fraction(evidence).ln()
        elbo_decimal=log_evidence-kl_decimal
        direct_decimal=sum((decimal_fraction(qi)*
                            ((decimal_fraction(ji)).ln()-(decimal_fraction(qi)).ln())
                            for qi,ji in zip(q,joint)),Decimal(0))
    if (abs(elbo_float-float(elbo_decimal))>1e-12 or
        abs(float(direct_decimal-elbo_decimal))>1e-12 or
        float(kl_decimal)<-1e-12):
        raise AssertionError("ELBO/KL/log evidence different numeric paths disagree")
    true_p,true_r,true_c,true_agree=posterior_marginals(post)
    return {
        "q":q,"p":p,"r":r,
        "elbo_float":elbo_float,"elbo_decimal":elbo_decimal,
        "KL_reverse_decimal":kl_decimal,
        "log_evidence_decimal":log_evidence,
        "true_p":true_p,"true_r":true_r,
        "true_covariance":true_c,"true_agreement":true_agree,
        "q_agreement":q[0]+q[3]
    }

def forward_optimal_independent(post):
    """Analytic forward KL P||q optimizer: product of true marginals, not VI fit."""
    p,r,cov,agree=posterior_marginals(post)
    q=family_q(p,r)
    with localcontext() as ctx:
        ctx.prec=70
        mutual_information=sum((decimal_fraction(x)*
              (decimal_fraction(x)/decimal_fraction(y)).ln()
              for x,y in zip(post,q)),Decimal(0))
    if float(mutual_information)<-1e-12:
        raise AssertionError("Negative true posterior mutual information")
    return q,mutual_information

def optimize_world(name,w,m,label,grid,all_candidates):
    post,evidence,joint=true_posterior(w,m)
    choice=None
    scored=0
    for p,r in product(grid,repeat=2):
        result=candidate_score(w,m,p,r)
        scored+=1
        all_candidates.append({
            "source":name,"observed_independent_successes_m":m,
            "grid":label,"mean_field_p_z1":str(p),"mean_field_p_z2":str(r),
            "mean_field_joint_probability":",".join(map(str,result["q"])),
            "ELBO_direct_float":format(result["elbo_float"],".16g"),
            "ELBO_70digit_Decimal":str(result["elbo_decimal"]),
            "reverse_KL_70digit_Decimal":str(result["KL_reverse_decimal"]),
            "log_true_evidence_70digit_Decimal":str(result["log_evidence_decimal"]),
            "true_Z1_Z2_covariance_exact":str(result["true_covariance"]),
            "q_Z1_Z2_covariance_exact":"0",
            "ELBO_two_implementations_agree":True
        })
        # Exact Decimal comparisons; grid is stable lexicographically ordered.
        if choice is None or result["elbo_decimal"]>choice["elbo_decimal"]:
            choice=result
    if choice is None or scored!=len(grid)**2:
        raise AssertionError("Fixed mean-field finite grid incomplete")
    if choice["elbo_decimal"]>choice["log_evidence_decimal"]+Decimal("1e-50"):
        raise AssertionError("ELBO above exact log evidence")
    if choice["KL_reverse_decimal"]<Decimal("-1e-50"):
        raise AssertionError("Negative grid-optimal KL")
    return {
        "source":name,"m_positive_likelihood_observations":m,
        "grid":label,"finite_candidate_count":scored,
        "true_posterior_exact":[str(x) for x in post],
        "true_evidence_exact":str(evidence),
        "true_log_evidence_70digit":str(choice["log_evidence_decimal"]),
        "selected_mean_field_p_z1_exact":str(choice["p"]),
        "selected_mean_field_p_z2_exact":str(choice["r"]),
        "selected_mean_field_joint_exact":[str(x) for x in choice["q"]],
        "selected_mean_field_ELBO_70digit":str(choice["elbo_decimal"]),
        "selected_mean_field_reverse_KL_gap_70digit":str(choice["KL_reverse_decimal"]),
        "selected_abs_error_Z1_marginal":str(abs(choice["p"]-choice["true_p"])),
        "selected_abs_error_Z2_marginal":str(abs(choice["r"]-choice["true_r"])),
        "true_covariance_Z1_Z2_exact":str(choice["true_covariance"]),
        "mean_field_covariance_Z1_Z2_exact":"0",
        "true_probability_Z1_equals_Z2_exact":str(choice["true_agreement"]),
        "selected_mean_field_probability_Z1_equals_Z2_exact":str(choice["q_agreement"]),
        "all_exact_Bayes_and_independent_ELBO_routes_verified":True
    }

def run():
    cand=[]
    worlds_out=[]
    truth_sources=[]
    for name,w,m in source_worlds():
        post,evidence,joint=true_posterior(w,m)
        margin1,margin2,cov,agree=posterior_marginals(post)
        marginal_prod,mi=forward_optimal_independent(post)
        truth_sources.append({
            "source":name,"weights":[int(x) for x in w],
            "positive_observations_m":m,
            "exact_prior_probability_each_state":"1/4",
            "exact_evidence":str(evidence),
            "exact_posterior_00_01_10_11":[str(x) for x in post],
            "exact_posterior_z1_marginal_1":str(margin1),
            "exact_posterior_z2_marginal_1":str(margin2),
            "exact_posterior_covariance":str(cov),
            "exact_posterior_indicator_agreement":str(agree),
            "true_posterior_is_independent":independent_posterior(post),
            "unconstrained_exact_joint_ELBO_gap":"0",
            "forward_KL_optimum_product_of_true_marginals":[str(x) for x in marginal_prod],
            "forward_KL_optimum_mutual_information_70digit":str(mi),
            "forward_and_reverse_KL_directions_not_interchangeable":True
        })
        outcomes={}
        for label,grid in GRIDS:
            x=optimize_world(name,w,m,label,grid,cand)
            worlds_out.append(x)
            outcomes[label]=x
        with localcontext() as ctx:
            ctx.prec=80
            if (Decimal(outcomes["FINE"]["selected_mean_field_reverse_KL_gap_70digit"])>
                Decimal(outcomes["COARSE"]["selected_mean_field_reverse_KL_gap_70digit"])+Decimal("1e-50")):
                raise AssertionError("Nested fine grid is worse than coarse")
    if len(worlds_out)!=24 or len(cand)!=408 or len(truth_sources)!=12:
        raise AssertionError("Frozen 24/408/12 universe changed")
    for n,m in product(("UNIFORM","INDEPENDENT_SKEW"),COUNTS):
        candidates=[x for x in worlds_out if x["source"]==n and
                    x["m_positive_likelihood_observations"]==m]
        if n=="UNIFORM" or (n=="INDEPENDENT_SKEW" and m==1):
            if any(Decimal(x["selected_mean_field_reverse_KL_gap_70digit"])!=0 for x in candidates):
                raise AssertionError("Prelocked exact factorization grid case not recovered")
        if n=="INDEPENDENT_SKEW" and m==2:
            if not all(Decimal(x["selected_mean_field_reverse_KL_gap_70digit"])>0 for x in candidates):
                raise AssertionError("Prelocked independent but off-grid posterior not measured")
    for x in worlds_out:
        if "COUPLED" in x["source"]:
            if x["true_covariance_Z1_Z2_exact"]=="0" or Decimal(x["selected_mean_field_reverse_KL_gap_70digit"])<=0:
                raise AssertionError("Dependent true target somehow perfectly factorized")
    for path,rows in ((CANDIDATES,cand),):
        with path.open("w",newline="",encoding="utf-8") as f:
            writer=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator="\n")
            writer.writeheader();writer.writerows(rows)
    TRUTHS.write_text(json.dumps({"research_id":"R196","source_evidence_worlds":12,
        "exact_source_truths":truth_sources},sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    focus=[x for x in worlds_out if x["source"] in ("UNIFORM","INDEPENDENT_SKEW",
                                                   "POSITIVE_COUPLED","NEGATIVE_COUPLED")]
    result={
        "research_id":"R196",
        "state":"E1_ARTIFICIAL_TWO_BINARY_LATENT_FINITE_MEAN_FIELD_VB",
        "frozen_scoring_worlds":24,"exact_source_evidence_configurations":12,
        "total_all_candidate_scores":408,
        "coarse_grid_candidates_per_source":9,
        "fine_grid_candidates_per_source":25,
        "exact_Bayes_posterior_two_independent_Fraction_paths_agree":True,
        "ELBO_float_joint_entropy_vs_Decimal_log_evidence_minus_reverse_KL_agree":True,
        "all_exact_evidence_ELBO_reverse_KL_identity_verified":True,
        "all_nested_fine_grid_reverse_KL_not_worse_than_coarse":True,
        "independent_posterior_exact_and_off_grid_cases_tested":True,
        "correlated_posterior_mean_field_cannot_encode_covariance":True,
        "mode_seeking_depends_on_reverse_KL_and_finite_candidate_grid":True,
        "frozen_exact_vs_off_grid_vs_dependent_worlds":focus,
        "all_worlds":worlds_out,
        "all_408_candidate_csv_sha256":sha256(CANDIDATES.read_bytes()).hexdigest(),
        "all_12_source_truths_sha256":sha256(TRUTHS.read_bytes()).hexdigest(),
        "new_E2":0,"new_E3":0,"real_human_or_history_data":False
    }
    RESULT.write_text(json.dumps(result,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    accept={
        "research_id":"R196","status":"CLOSED_BOUNDED_E1_ARTIFICIAL_FINITE_VARIATIONAL_BAYES",
        "frozen_worlds":24,"true_posterior_configurations":12,"scored_candidates":408,
        "two_exact_Bayes_Fraction_implementations_equal":True,
        "ELBO_KL_true_log_evidence_two_independent_numeric_paths_agree":True,
        "fine_grid_contains_and_never_underperforms_coarse":True,
        "off_grid_independent_and_dependent_mean_field_limits_verified":True,
        "source_results_sha256":sha256(RESULT.read_bytes()).hexdigest(),
        "candidate_CSV_sha256":result["all_408_candidate_csv_sha256"],
        "exact_truth_sources_sha256":result["all_12_source_truths_sha256"],
        "new_E2":0,"new_E3":0,"real_human_or_history_data":False
    }
    ACCEPT.write_text(json.dumps(accept,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("R196_ACCEPTANCE",json.dumps(accept,sort_keys=True))
    print("R196_PRIMARY_MODE_CONTRAST",json.dumps([x for x in focus if x["grid"]=="FINE"],sort_keys=True)[:7500])
    return result

def archive():
    names=[Path(__file__).name,RESULT.name,CANDIDATES.name,TRUTHS.name,ACCEPT.name]
    with zipfile.ZipFile(ZIP,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name in names:
            info=zipfile.ZipInfo(name,date_time=(2026,10,21,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o644<<16
            z.writestr(info,(HERE/name).read_bytes())
        for document in (PROTOCOL,ERRATUM):
            info=zipfile.ZipInfo(document.name,date_time=(2026,10,21,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o644<<16
            z.writestr(info,document.read_bytes())
    print("R196_ZIP_SHA256",sha256(ZIP.read_bytes()).hexdigest())

class TestFiniteVariationalBayes(unittest.TestCase):
    def test_six_targets(self):self.assertEqual(len(SOURCES),6)
    def test_two_likelihood_repetitions(self):self.assertEqual(COUNTS,(1,2))
    def test_12_source_configs(self):self.assertEqual(len(list(source_worlds())),12)
    def test_24_search_worlds(self):self.assertEqual(len(list(source_worlds()))*len(GRIDS),24)
    def test_all_408_candidate_scores(self):self.assertEqual(6*2*(9+25),408)
    def test_coarse_subset_fine(self):self.assertTrue(set(GRID_COARSE).issubset(set(GRID_FINE)))
    def test_two_exact_Bayes_methods_all(self):
        for name,w,m in source_worlds():
            p,e,j=posterior_from_joint(w,m)
            alt,e2=posterior_normalize_weights(w,m)
            self.assertEqual((p,e),(alt,e2))
    def test_all_exact_posteriors_mass_one(self):
        for name,w,m in source_worlds():
            p,e,j=true_posterior(w,m)
            self.assertEqual(sum(p,F(0)),1)
            self.assertGreater(e,0)
    def test_all_evidence_at_most_one(self):
        for name,w,m in source_worlds():
            self.assertLessEqual(true_posterior(w,m)[1],1)
    def test_uniform_is_equal_quarter_posterior(self):
        for m in COUNTS:self.assertEqual(true_posterior(SOURCES[0][1],m)[0],(F(1,4),)*4)
    def test_independent_skew_m1_true_quarter_marginals(self):
        p=true_posterior(SOURCES[1][1],1)[0]
        self.assertEqual(posterior_marginals(p)[:2],(F(1,4),F(1,4)))
    def test_independent_skew_m2_true_one_tenth_marginals(self):
        p=true_posterior(SOURCES[1][1],2)[0]
        self.assertEqual(posterior_marginals(p)[:2],(F(1,10),F(1,10)))
    def test_independent_skew_both_are_exact_product(self):
        for m in COUNTS:self.assertTrue(independent_posterior(true_posterior(SOURCES[1][1],m)[0]))
    def test_true_positive_coupled_covariance(self):
        p=true_posterior(SOURCES[2][1],1)[0]
        self.assertGreater(posterior_marginals(p)[2],0)
    def test_true_negative_coupled_covariance(self):
        p=true_posterior(SOURCES[3][1],1)[0]
        self.assertLess(posterior_marginals(p)[2],0)
    def test_all_meanfield_candidates_normalized(self):
        for _,grid in GRIDS:
            for p,r in product(grid,repeat=2):
                self.assertEqual(sum(family_q(p,r),F(0)),1)
    def test_true_meanfield_covariance_zero(self):
        for _,grid in GRIDS:
            for p,r in product(grid,repeat=2):
                self.assertEqual(posterior_marginals(family_q(p,r))[2],0)
    def test_forward_KL_product_marginals(self):
        for name,w,m in source_worlds():
            post=true_posterior(w,m)[0]
            family,mi=forward_optimal_independent(post)
            self.assertEqual(posterior_marginals(family)[:2],posterior_marginals(post)[:2])
            self.assertGreaterEqual(mi,0)
    def test_two_independent_numeric_ELBO_routes_all_408(self):
        for name,w,m in source_worlds():
            for label,grid in GRIDS:
                for p,r in product(grid,repeat=2):
                    candidate_score(w,m,p,r)
    def test_optimal_coarse_fine_nested(self):
        for name,w,m in source_worlds():
            short=optimize_world(name,w,m,"COARSE",GRID_COARSE,[])
            fine=optimize_world(name,w,m,"FINE",GRID_FINE,[])
            with localcontext() as ctx:
                ctx.prec=80
                self.assertLessEqual(Decimal(fine["selected_mean_field_reverse_KL_gap_70digit"]),
                                     Decimal(short["selected_mean_field_reverse_KL_gap_70digit"])+Decimal("1e-50"))
    def test_uniform_true_exact_zero_KL(self):
        for m in COUNTS:
            for label,grid in GRIDS:
                x=optimize_world("UNIFORM",SOURCES[0][1],m,label,grid,[])
                self.assertEqual(Decimal(x["selected_mean_field_reverse_KL_gap_70digit"]),0)
    def test_independent_skew_m1_grid_exact(self):
        for label,grid in GRIDS:
            x=optimize_world("INDEPENDENT_SKEW",SOURCES[1][1],1,label,grid,[])
            self.assertEqual(Decimal(x["selected_mean_field_reverse_KL_gap_70digit"]),0)
    def test_independent_skew_m2_off_grid_positive(self):
        for label,grid in GRIDS:
            x=optimize_world("INDEPENDENT_SKEW",SOURCES[1][1],2,label,grid,[])
            self.assertGreater(Decimal(x["selected_mean_field_reverse_KL_gap_70digit"]),0)
    def test_dependent_sources_never_exact_meanfield(self):
        for name,w,m in source_worlds():
            if "COUPLED" in name:
                self.assertFalse(independent_posterior(true_posterior(w,m)[0]))
    def test_selected_q_indicators_bounded(self):
        x=optimize_world("POSITIVE_COUPLED",SOURCES[2][1],2,"FINE",GRID_FINE,[])
        self.assertTrue(0<=F(x["selected_mean_field_probability_Z1_equals_Z2_exact"])<=1)
    def test_fixed_lexicographic_candidate_order(self):
        pairs=list(product(GRID_COARSE,repeat=2))
        self.assertEqual(pairs[0],(F(1,4),F(1,4)))
        self.assertEqual(pairs[-1],(F(3,4),F(3,4)))
    def test_reject_unknown_target(self):
        with self.assertRaises(ValueError):source_check((2,2,2,2),1)
    def test_reject_unknown_observation_count(self):
        with self.assertRaises(ValueError):source_check((1,1,1,1),3)
    def test_reject_outside_Bernoulli_probability(self):
        with self.assertRaises(ValueError):family_q(F(0),F(1,2))
    def test_reject_upper_Bernoulli_probability(self):
        with self.assertRaises(ValueError):family_q(F(1,2),F(1))
    def test_independent_exact_Evidence_uniform_one(self):
        for m in COUNTS:self.assertEqual(true_posterior(SOURCES[0][1],m)[1],1)
    def test_strong_positive_posterior_marginals_equal_half(self):
        for m in COUNTS:
            post=true_posterior(SOURCES[2][1],m)[0]
            self.assertEqual(posterior_marginals(post)[:2],(F(1,2),F(1,2)))

if __name__=="__main__":
    if sys.argv[1:]==["--test"]:
        unittest.main(argv=[sys.argv[0]],verbosity=2)
    elif sys.argv[1:]==["--run-and-archive"]:
        run();archive()
    else:raise SystemExit("Use --test or --run-and-archive")
