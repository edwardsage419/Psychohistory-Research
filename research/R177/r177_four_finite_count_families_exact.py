"""R177 exact finite count probability families: original synthetic E1 benchmark.

The four source processes distinguish trial independence, positive dependence,
sampling without replacement, and latent structural inactivity.
Method A uses closed-form PMFs. Method B performs sequential-state dynamic
programming on primitive event probabilities. No observed social data.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from math import comb
from pathlib import Path
import json
import sys
import unittest
import zipfile

HERE=Path(__file__).resolve().parent
PROTO=HERE.parent.parent/"protocols/R177_FOUR_FINITE_COUNT_DISTRIBUTION_FAMILIES_108_WORLDS_PRESCORE_FREEZE_2026-10-21.md"
OUT=HERE/"R177_EXACT_RESULTS.json"
ACCEPT=HERE/"R177_FINAL_MACHINE_ACCEPTANCE.json"
ARCH=HERE/"R177_Four_Count_Distribution_Families_108_Exact_Worlds.zip"

N_VALUES=(4,8,12)
P_VALUES=(F(1,8),F(1,4),F(1,2))
REGIMES=(0,1,2)
FAMILIES=("BIN","BB","HG","ZIB")
CONCENTRATIONS=(2,4,8)
POPULATIONS=(24,48,72)
ZERO_PROBS=(F(1,8),F(1,4),F(1,3))


def configurations():
    for family,n,p,regime in product(FAMILIES,N_VALUES,P_VALUES,REGIMES):
        yield family,n,p,regime


def extra(family,regime):
    if regime not in REGIMES:
        raise ValueError("regime outside freeze")
    if family=="BIN":
        return {}
    if family=="BB":
        return {"concentration":CONCENTRATIONS[regime]}
    if family=="HG":
        return {"population":POPULATIONS[regime]}
    if family=="ZIB":
        return {"structural_zero":ZERO_PROBS[regime]}
    raise ValueError("unknown family")


def validate(family,n,p,regime):
    if family not in FAMILIES or n<1 or not 0<p<1 or regime not in REGIMES:
        raise ValueError("invalid source parameters")
    opt=extra(family,regime)
    if family=="HG" and (n>opt["population"] or (p*opt["population"]).denominator!=1):
        raise ValueError("invalid finite population composition")
    if family=="ZIB" and not 0<p/(1-opt["structural_zero"])<1:
        raise ValueError("invalid adjusted trial success rate")


def rising(x,k):
    val=F(1)
    for i in range(k):
        val*=x+i
    return val


def formula_pmf(family,n,p,regime):
    """Algorithm A: four distinct normalized probability mass formulas."""
    validate(family,n,p,regime)
    opt=extra(family,regime)
    if family=="BIN":
        return tuple(F(comb(n,k))*p**k*(1-p)**(n-k) for k in range(n+1))
    if family=="BB":
        c=opt["concentration"]
        a=p*c
        b=(1-p)*c
        return tuple(F(comb(n,k))*rising(a,k)*rising(b,n-k)/rising(c,n)
                     for k in range(n+1))
    if family=="HG":
        N=opt["population"]
        K=int(N*p)
        return tuple(F(comb(K,k)*comb(N-K,n-k),comb(N,n))
                     if 0<=k<=K and 0<=n-k<=N-K else F(0)
                     for k in range(n+1))
    if family=="ZIB":
        z=opt["structural_zero"]
        q=p/(1-z)
        return tuple((z if k==0 else 0)+(1-z)*F(comb(n,k))*q**k*(1-q)**(n-k)
                     for k in range(n+1))
    raise AssertionError("impossible family")


def event_dp(family,n,p,regime):
    """Algorithm B: sequential elementary trials in count-state dynamic program.

    No closed-form coefficients or rising factorial PMF are used here.
    For BB, each draw adjusts the urn after seeing the preceding successes.
    For HG, each draw physically removes a member from the population.
    """
    validate(family,n,p,regime)
    opt=extra(family,regime)
    c=opt.get("concentration",None)
    N=opt.get("population",None)
    K=int(N*p) if N is not None else None
    z=opt.get("structural_zero",F(0))
    q_fixed=p/(1-z) if family=="ZIB" else p
    dist={0:F(1)}
    for step in range(n):
        nxt=defaultdict(F)
        for success,weight in dist.items():
            if family=="BB":
                q=(p*c+success)/(c+step)
            elif family=="HG":
                q=F(K-success,N-step)
            else:
                q=q_fixed
            nxt[success]+=weight*(1-q)
            nxt[success+1]+=weight*q
        dist=nxt
    if family=="ZIB":
        # Latent inactive class puts all its weight at zero.
        return tuple((z if k==0 else F(0))+(1-z)*dist.get(k,F(0))
                     for k in range(n+1))
    return tuple(dist.get(k,F(0)) for k in range(n+1))


def moments(pmf):
    mean=sum((k*v for k,v in enumerate(pmf)),F(0))
    variance=sum(((F(k)-mean)**2*v for k,v in enumerate(pmf)),F(0))
    return mean,variance,pmf[0]


def theory_variance(family,n,p,regime):
    base=n*p*(1-p)
    opt=extra(family,regime)
    if family=="BIN":
        return base
    if family=="BB":
        c=opt["concentration"]
        return base*F(c+n,c+1)
    if family=="HG":
        N=opt["population"]
        return base*F(N-n,N-1)
    if family=="ZIB":
        z=opt["structural_zero"]
        return base+z/(1-z)*n*(n-1)*p**2
    raise ValueError("unknown family")


def synthetic_alias():
    """Frozen n=2 complete observational equivalence counterexample."""
    # BB(c=2, alpha=beta=1) PMF computed without relying on grid mapping.
    bb=tuple(F(comb(2,k))*rising(1,k)*rising(1,2-k)/rising(2,2)
             for k in range(3))
    z=F(1,4)
    q=F(2,3)
    zib=tuple((z if k==0 else F(0))+(1-z)*F(comb(2,k))*q**k*(1-q)**(2-k)
              for k in range(3))
    urn={0:F(1)}
    for j in range(2):
        new=defaultdict(F)
        for k,weight in urn.items():
            chance=F(1+k,2+j)
            new[k]+=weight*(1-chance)
            new[k+1]+=weight*chance
        urn=new
    bb_urn=tuple(urn.get(k,F(0)) for k in range(3))
    active={0:F(1)}
    for j in range(2):
        new=defaultdict(F)
        for k,weight in active.items():
            new[k]+=weight*(1-q)
            new[k+1]+=weight*q
        active=new
    zib_events=tuple((z if k==0 else F(0))+(1-z)*active.get(k,F(0))
                     for k in range(3))
    if bb!=zib or bb!=bb_urn or zib!=zib_events or bb!=(F(1,3),)*3:
        raise AssertionError("counterexample failed independent two-route identity")
    mean,var,_=moments(bb)
    return {
        "count_support":[0,1,2],
        "BB_c2_alpha1_beta1_pmf":[str(v) for v in bb],
        "ZIB_z_quarter_q_two_thirds_pmf":[str(v) for v in zib],
        "mean":str(mean),"variance":str(var),
        "same_entire_distribution_in_both_implementations":True,
        "mechanisms_distinct":True,
        "real_human_identification_claim":False
    }


def run():
    worlds=[]
    groups=defaultdict(dict)
    for family,n,p,regime in configurations():
        a=formula_pmf(family,n,p,regime)
        b=event_dp(family,n,p,regime)
        if a!=b:
            raise AssertionError(f"exact PMF route mismatch for {family,n,p,regime}")
        if any(v<0 for v in a) or sum(a,F(0))!=1:
            raise AssertionError("probability vector invalid")
        mean,var,p0=moments(a)
        if mean!=n*p or var!=theory_variance(family,n,p,regime):
            raise AssertionError("first and second moments fail analytic formula")
        groups[(n,p,regime)][family]=(mean,var,p0,a)
        details={k:str(v) for k,v in extra(family,regime).items()}
        worlds.append({
            "family":family,"n":n,"p":str(p),"regime":regime,
            "extra":details,
            "count_support":list(range(n+1)),
            "full_PMF":[str(z) for z in a],
            "mean":str(mean),"variance":str(var),"p_zero":str(p0),
            "independent_formula_and_sequential_event_algorithms_exact":True
        })
    assert len(worlds)==108 and sum(len(w["full_PMF"]) for w in worlds)==972
    for (n,p,regime),family in groups.items():
        vb=family["BIN"][1]
        pb=family["BIN"][2]
        if not family["HG"][1] < vb < family["BB"][1]:
            raise AssertionError("variance ordering incompatible with finite dependence")
        if not family["ZIB"][1] > vb:
            raise AssertionError("inactivity mixture failed overdispersion")
        if not family["HG"][2] < pb < family["BB"][2]:
            raise AssertionError("zero mass inequality for sampling mechanisms")
        if not family["ZIB"][2] > pb:
            raise AssertionError("structural zero model did not exceed baseline P0")
    for n,p in product(N_VALUES,P_VALUES):
        base=[formula_pmf("BIN",n,p,r) for r in REGIMES]
        if not(base[0]==base[1]==base[2]):
            raise AssertionError("redundant BIN regime changed probability")
    alias=synthetic_alias()
    selected=[]
    for f in FAMILIES:
        row=next(w for w in worlds
                 if w["family"]==f and w["n"]==8
                 and w["p"]=="1/4" and w["regime"]==0)
        selected.append({"family":f,"mean":row["mean"],"variance":row["variance"],
                         "p_zero":row["p_zero"],"extra":row["extra"]})
    out={
        "research_id":"R177",
        "stage":"E1_ARTIFICIAL_EXACT_FINITE_DISTRIBUTION_FAMILIES",
        "protocol":"protocols/"+PROTO.name,
        "families":list(FAMILIES),"worlds":108,"distinct_parameter_worlds":90,
        "full_PMF_probability_cells":972,
        "complete_support_count_vectors":108,
        "all_means_matched_to_n_p":True,
        "two_independent_exact_methods_equal":True,
        "signed_variance_ordering_for_all_27_parameter_crossings":{
            "hypergeometric_less_than_binomial":True,
            "beta_binomial_greater_than_binomial":True,
            "zero_inflated_greater_than_binomial":True,
        },
        "selected_illustration_n8_p_quarter_regime0":selected,
        "two_different_mechanisms_identical_full_count_PMF":alias,
        "world_data":worlds,
        "real_social_events_or_historical_data":False,
        "new_E2":0,"new_E3":0,
    }
    OUT.write_text(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    acceptance={
        "research_id":"R177","status":"CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_FINITE_PMF",
        "family_count":4,"worlds":108,"distinct_parameter_worlds":90,
        "full_probability_cells":972,
        "independent_methods_exact_match":True,
        "mean_equivalence_all_family_worlds":True,
        "variance_and_zero_mass_orderings_all":True,
        "n2_BB_and_ZIB_full_count_distribution_equivalence":True,
        "real_human_or_historical_data_tested":False,
        "new_E2":0,"new_E3":0,
        "exact_results_sha256":sha256(OUT.read_bytes()).hexdigest(),
    }
    ACCEPT.write_text(json.dumps(acceptance,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("R177_MACHINE_ACCEPTANCE",json.dumps(acceptance,sort_keys=True))
    print("R177_LOCKED_ILLUSTRATION",json.dumps(selected,sort_keys=True))
    return out


def archive():
    names=[Path(__file__).name,OUT.name,ACCEPT.name]
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
    print("R177_ARCHIVE_SHA256",sha256(ARCH.read_bytes()).hexdigest())


class TestCountFamilies(unittest.TestCase):
    def test_grid_108(self):
        self.assertEqual(len(list(configurations())),108)
    def test_all_n_support(self):
        for f,n,p,r in configurations():
            self.assertEqual(len(formula_pmf(f,n,p,r)),n+1)
    def test_all_pmf_normalized(self):
        for f,n,p,r in configurations():
            self.assertEqual(sum(formula_pmf(f,n,p,r),F(0)),1)
    def test_all_nonnegative(self):
        for f,n,p,r in configurations():
            self.assertTrue(all(v>=0 for v in formula_pmf(f,n,p,r)))
    def test_two_independent_algorithms_every_world(self):
        for f,n,p,r in configurations():
            self.assertEqual(formula_pmf(f,n,p,r),event_dp(f,n,p,r))
    def test_equal_means(self):
        for f,n,p,r in configurations():
            self.assertEqual(moments(event_dp(f,n,p,r))[0],n*p)
    def test_correct_analytic_variances(self):
        for f,n,p,r in configurations():
            self.assertEqual(moments(formula_pmf(f,n,p,r))[1],
                             theory_variance(f,n,p,r))
    def test_variance_orderings(self):
        for n,p,r in product(N_VALUES,P_VALUES,REGIMES):
            b=theory_variance("BIN",n,p,r)
            self.assertLess(theory_variance("HG",n,p,r),b)
            self.assertGreater(theory_variance("BB",n,p,r),b)
            self.assertGreater(theory_variance("ZIB",n,p,r),b)
    def test_zero_mass_orderings(self):
        for n,p,r in product(N_VALUES,P_VALUES,REGIMES):
            b=formula_pmf("BIN",n,p,r)[0]
            self.assertLess(formula_pmf("HG",n,p,r)[0],b)
            self.assertGreater(formula_pmf("BB",n,p,r)[0],b)
            self.assertGreater(formula_pmf("ZIB",n,p,r)[0],b)
    def test_bin_redundant_regime(self):
        for n,p in product(N_VALUES,P_VALUES):
            self.assertEqual(len({formula_pmf("BIN",n,p,r) for r in REGIMES}),1)
    def test_bb_urn_reinforcement(self):
        self.assertEqual(event_dp("BB",4,F(1,2),0),formula_pmf("BB",4,F(1,2),0))
    def test_hypergeom_finite_population(self):
        self.assertEqual(sum(event_dp("HG",12,F(1,2),0)),1)
    def test_adjusted_zero_inflated_probability(self):
        self.assertEqual(F(1,2)/(1-F(1,3)),F(3,4))
    def test_full_observational_alias(self):
        self.assertEqual(synthetic_alias()["BB_c2_alpha1_beta1_pmf"],
                         ["1/3","1/3","1/3"])
    def test_full_alias_matches_second_family(self):
        a=synthetic_alias()
        self.assertEqual(a["BB_c2_alpha1_beta1_pmf"],a["ZIB_z_quarter_q_two_thirds_pmf"])
    def test_alias_second_moment(self):
        self.assertEqual(synthetic_alias()["variance"],"2/3")
    def test_binomial_hand_calculation(self):
        self.assertEqual(formula_pmf("BIN",4,F(1,2),0),
                         tuple(F(x,16) for x in (1,4,6,4,1)))
    def test_hypergeom_boundary_k_invalid_combinatorics_zero(self):
        p=formula_pmf("HG",12,F(1,8),0)
        self.assertTrue(all(p[k]==0 for k in range(4,13)))
    def test_hg_zero_prob_greater_than_zero(self):
        self.assertGreater(event_dp("HG",12,F(1,2),0)[0],0)
    def test_zero_mass_mixture_formula(self):
        z=F(1,4)
        q=F(1,4)/(1-z)
        self.assertEqual(formula_pmf("ZIB",4,F(1,4),1)[0],z+(1-z)*(1-q)**4)
    def test_reject_bad_regime(self):
        with self.assertRaises(ValueError):
            formula_pmf("BIN",4,F(1,2),3)
    def test_reject_out_of_bounds_p(self):
        with self.assertRaises(ValueError):
            formula_pmf("BIN",4,F(0),0)
    def test_reject_unknown_family(self):
        with self.assertRaises(ValueError):
            formula_pmf("UNKNOWN",4,F(1,2),0)
    def test_reject_population_smaller_than_sample(self):
        with self.assertRaises(ValueError):
            formula_pmf("HG",25,F(1,4),0)
    def test_total_cells_972(self):
        self.assertEqual(sum(n+1 for f,n,p,r in configurations()),972)
    def test_rising_factorial(self):
        self.assertEqual(rising(F(1,2),3),F(15,8))


if __name__=="__main__":
    if sys.argv[1:]==["--test"]:
        unittest.main(argv=[sys.argv[0]],verbosity=2)
    elif sys.argv[1:]==["--run-and-archive"]:
        run()
        archive()
    else:
        raise SystemExit("Use --test or --run-and-archive")
