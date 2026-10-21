"""R181 six-cluster Fisher randomization versus invalid event-level permutation.

Source populations are the source-pinned artificial R177 count laws. There are
210 unordered six-cluster count profiles, 20 actual treatment allocations,
and 10 independent data-generating worlds, producing 42000 exact records.
Full group and individual permutation laws each have two independent routes.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as F
from hashlib import sha1, sha256
from itertools import combinations, combinations_with_replacement
from math import comb, factorial
from pathlib import Path
import csv
import json
import sys
import unittest
import zipfile

HERE=Path(__file__).resolve().parent
R177=HERE.parent/"R177"
PROTO=HERE.parent.parent/"protocols/R181_EXACT_SIX_CLUSTER_RANDOMIZATION_42000_PROFILES_PRESCORE_FREEZE_2026-10-21.md"
OUT=HERE/"R181_EXACT_RESULTS.json"
LIB=HERE/"R181_ALL_210_RANDOMIZATION_PROFILES.json"
CSV=HERE/"R181_ALL_42000_SOURCE_WEIGHTED_ASSIGNMENTS.csv"
ACCEPT=HERE/"R181_FINAL_MACHINE_ACCEPTANCE.json"
ARCHIVE=HERE/"R181_Six_Cluster_Exact_Randomization_42000_Assignments.zip"
R177_SOURCE_BLOB="2d032513ce84141214b6b3f84df9c0ed9976a02b"
R177_RESULT_SHA256="57410cf2c110ce3117b7af72e4b7473cee0c3ffd013e6fb99fd43de62165a535"
N_GROUPS=6
EVENTS_PER_GROUP=4
TREAT_GROUPS=3
EVENT_SLOTS=24
TREAT_EVENT_SLOTS=12
ASSIGNMENTS=tuple(combinations(range(N_GROUPS),TREAT_GROUPS))
PROFILES=tuple(combinations_with_replacement(range(EVENTS_PER_GROUP+1),N_GROUPS))
ALPHAS=(F(1,10),F(1,5))
TRUTH_P=(F(1,4),F(1,2))
SOURCES=(
    ("IID_BIN","BIN",0),
    ("CLUSTERED_BB_C2","BB",0),
    ("CLUSTERED_BB_C8","BB",2),
    ("INACTIVE_ZIB_Z1_8","ZIB",0),
    ("INACTIVE_ZIB_Z1_4","ZIB",1),
)


def original_source():
    raw=(R177/"r177_four_finite_count_families_exact.py").read_bytes()
    blob=sha1(b"blob "+str(len(raw)).encode()+b"\x00"+raw).hexdigest()
    if blob!=R177_SOURCE_BLOB:
        raise ValueError("pinned R177 source implementation identity changed")
    if sha256((R177/"R177_EXACT_RESULTS.json").read_bytes()).hexdigest()!=R177_RESULT_SHA256:
        raise ValueError("pinned source output full SHA changed")
    if str(R177) not in sys.path:
        sys.path.insert(0,str(R177))
    from r177_four_finite_count_families_exact import formula_pmf,event_dp
    return formula_pmf,event_dp


def worlds():
    for p in TRUTH_P:
        for name,family,regime in SOURCES:
            yield p,name,family,regime


def group_perm_enum(profile):
    """A: enumerate 20 true three-group assignments under the sharp null."""
    if len(profile)!=N_GROUPS:
        raise ValueError("invalid group count")
    counts=Counter(sum(profile[i] for i in choice) for choice in ASSIGNMENTS)
    total=N_GROUPS*EVENTS_PER_GROUP
    out=tuple(F(counts.get(t,0),len(ASSIGNMENTS)) for t in range(total+1))
    return out


def group_perm_dp(profile):
    """B: without-replacement selection count DP over actual clusters."""
    if len(profile)!=N_GROUPS:
        raise ValueError("invalid group count")
    dp={(0,0):1}
    for amount in profile:
        nxt=defaultdict(int)
        for (chosen,total),count in dp.items():
            nxt[(chosen,total)]+=count
            if chosen<TREAT_GROUPS:
                nxt[(chosen+1,total+amount)]+=count
        dp=nxt
    return tuple(F(dp.get((TREAT_GROUPS,t),0),comb(N_GROUPS,TREAT_GROUPS))
                 for t in range(EVENT_SLOTS+1))


def individual_perm_hypergeom(total_success):
    """C: incorrect treatment randomization over 24 event opportunities."""
    if total_success not in range(EVENT_SLOTS+1):
        raise ValueError("event total invalid")
    den=comb(EVENT_SLOTS,TREAT_EVENT_SLOTS)
    return tuple(F(comb(total_success,t)*comb(EVENT_SLOTS-total_success,TREAT_EVENT_SLOTS-t),den)
                 if 0<=t<=total_success and 0<=TREAT_EVENT_SLOTS-t<=EVENT_SLOTS-total_success
                 else F(0) for t in range(TREAT_EVENT_SLOTS+1))


def individual_perm_draw_dp(total_success):
    """D: actual trial-by-trial hypergeometric urn without replacement."""
    if total_success not in range(EVENT_SLOTS+1):
        raise ValueError("event total invalid")
    dist={0:F(1)}
    for drawn in range(TREAT_EVENT_SLOTS):
        nxt=defaultdict(F)
        remaining=EVENT_SLOTS-drawn
        for success,weight in dist.items():
            chance=F(total_success-success,remaining)
            nxt[success]+=weight*(1-chance)
            nxt[success+1]+=weight*chance
        dist=nxt
    return tuple(dist.get(t,F(0)) for t in range(TREAT_EVENT_SLOTS+1))


def sharp_two_sided_p(total_success,observed_t,distribution):
    target=abs(2*observed_t-total_success)
    return sum((mass for t,mass in enumerate(distribution)
                if abs(2*t-total_success)>=target),F(0))


def profile_multiplier(profile):
    if len(profile)!=N_GROUPS or tuple(sorted(profile))!=tuple(profile):
        raise ValueError("expect sorted six-group count multiset")
    sizes=Counter(profile).values()
    den=1
    for count in sizes:
        den*=factorial(count)
    return factorial(N_GROUPS)//den


def profile_mass(profile,source_pmf):
    p=F(profile_multiplier(profile))
    for k in profile:
        p*=source_pmf[k]
    return p


def library_of_profiles():
    if len(ASSIGNMENTS)!=20 or len(PROFILES)!=210:
        raise AssertionError("source universe changed")
    library={}
    for profile in PROFILES:
        S=sum(profile)
        grp=group_perm_enum(profile)
        alt=group_perm_dp(profile)
        ev=individual_perm_hypergeom(S)
        ev2=individual_perm_draw_dp(S)
        if grp!=alt or ev!=ev2 or sum(grp,F(0))!=1 or sum(ev,F(0))!=1:
            raise AssertionError("exact independent randomization laws diverge")
        outcomes=[]
        for choice in ASSIGNMENTS:
            T=sum(profile[i] for i in choice)
            pc=sharp_two_sided_p(S,T,grp)
            pe=sharp_two_sided_p(S,T,ev)
            if not (0<pc<=1 and 0<pe<=1):
                raise AssertionError("randomization p outside (0,1]")
            outcomes.append({
                "treated_cluster_indices":",".join(map(str,choice)),
                "treated_event_count":T,
                "absolute_double_count_contrast":abs(2*T-S),
                "cluster_exact_two_sided_p":str(pc),
                "invalid_event_level_two_sided_p":str(pe),
                "cluster_reject_alpha_0p1":int(pc<=ALPHAS[0]),
                "cluster_reject_alpha_0p2":int(pc<=ALPHAS[1]),
                "invalid_event_reject_alpha_0p1":int(pe<=ALPHAS[0]),
                "invalid_event_reject_alpha_0p2":int(pe<=ALPHAS[1]),
            })
        for alpha in ALPHAS:
            conditional=F(sum(int(F(z["cluster_exact_two_sided_p"])<=alpha) for z in outcomes),
                          len(outcomes))
            if conditional>alpha:
                raise AssertionError("valid sharp-null group Fisher test exceeded nominal level")
        library[profile]={
            "sorted_group_counts":list(profile),
            "group_permutation_count":len(ASSIGNMENTS),
            "source_ordering_multiplicity":profile_multiplier(profile),
            "group_treated_success_PMF":[str(z) for z in grp],
            "invalid_event_treated_success_PMF":[str(z) for z in ev],
            "all_20_true_cluster_assignments":outcomes,
            "full_two_independent_null_algorithms_agreed":True,
        }
    return library


def evaluate_source(p,name,family,regime,source_pmf,library,rows):
    if sum(source_pmf,F(0))!=1:
        raise AssertionError("broken source probability")
    total_mass=F(0)
    null_dist=Counter()
    p_cluster_marginal=F(0)
    p_event_marginal=F(0)
    rejection={"cluster_alpha_0p1":F(0),"cluster_alpha_0p2":F(0),
               "invalid_event_alpha_0p1":F(0),"invalid_event_alpha_0p2":F(0)}
    n=0
    for profile in PROFILES:
        mass=profile_mass(profile,source_pmf)
        total_mass+=mass
        entry=library[profile]
        for allocation in entry["all_20_true_cluster_assignments"]:
            n+=1
            weight=mass/F(len(ASSIGNMENTS))
            pc=F(allocation["cluster_exact_two_sided_p"])
            pe=F(allocation["invalid_event_level_two_sided_p"])
            p_cluster_marginal+=weight*pc
            p_event_marginal+=weight*pe
            null_dist["all_profiles"]+=weight
            for k,key in (
                ("cluster_alpha_0p1","cluster_reject_alpha_0p1"),
                ("cluster_alpha_0p2","cluster_reject_alpha_0p2"),
                ("invalid_event_alpha_0p1","invalid_event_reject_alpha_0p1"),
                ("invalid_event_alpha_0p2","invalid_event_reject_alpha_0p2"),
            ):
                rejection[k]+=weight*allocation[key]
            rows.append({
                "model":name,
                "true_p":str(p),
                "sorted_group_counts":",".join(map(str,profile)),
                "profile_ordering_multiplicity":entry["source_ordering_multiplicity"],
                "true_profile_probability":str(mass),
                "true_profile_and_assignment_probability":str(weight),
                **allocation
            })
    if total_mass!=1 or null_dist["all_profiles"]!=1 or n!=len(PROFILES)*len(ASSIGNMENTS):
        raise AssertionError("source sample space does not normalize")
    if rejection["cluster_alpha_0p1"]>ALPHAS[0] or rejection["cluster_alpha_0p2"]>ALPHAS[1]:
        raise AssertionError("actual group randomization is not sharp-null valid")
    return {
        "true_p":str(p),
        "source":name,
        "R177_family":family,
        "R177_regime":regime,
        "group_count":N_GROUPS,
        "independent_groups":True,
        "actual_treated_groups":TREAT_GROUPS,
        "invalid_imaginary_individually_randomized_events":TREAT_EVENT_SLOTS,
        "unique_unordered_group_count_profiles":len(PROFILES),
        "actual_assignment_per_profile":len(ASSIGNMENTS),
        "ordered_underlying_count_samples":5**N_GROUPS,
        "scenario_analysis_rows":n,
        "source_count_pmf":[str(z) for z in source_pmf],
        "true_frequentist_false_positive_probabilities":{
            k:str(v) for k,v in rejection.items()
        },
        "mean_true_randomization_pvalue":str(p_cluster_marginal),
        "mean_invalid_event_permutation_pvalue":str(p_event_marginal),
        "group_sharp_null_test_verified_exact":True,
    }


def archive():
    files=[Path(__file__).name,OUT.name,LIB.name,CSV.name,ACCEPT.name]
    with zipfile.ZipFile(ARCHIVE,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name in files:
            info=zipfile.ZipInfo(name,date_time=(2026,10,21,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o644<<16
            z.writestr(info,(HERE/name).read_bytes())
        info=zipfile.ZipInfo(PROTO.name,date_time=(2026,10,21,0,0,0))
        info.compress_type=zipfile.ZIP_DEFLATED
        info.external_attr=0o644<<16
        z.writestr(info,PROTO.read_bytes())
    print("R181_ARCHIVE_SHA256",sha256(ARCHIVE.read_bytes()).hexdigest())


def run():
    formula,events=original_source()
    lib=library_of_profiles()
    rows=[]
    worlds_out=[]
    for p,name,family,regime in worlds():
        law=formula(family,EVENTS_PER_GROUP,p,regime)
        if law!=events(family,EVENTS_PER_GROUP,p,regime):
            raise AssertionError("pinned original group count source fails second method")
        if sum((profile_mass(profile,law) for profile in PROFILES),F(0))!=1:
            raise AssertionError("multinomial source profile weights do not normalize")
        worlds_out.append(evaluate_source(p,name,family,regime,law,lib,rows))
    if len(worlds_out)!=10 or len(rows)!=42000:
        raise AssertionError("missing frozen source scenarios or randomized observations")
    headers=list(rows[0])
    with CSV.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=headers,lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    library_result={
        "research_id":"R181",
        "profiles":list(lib.values()),
        "source_neutral_profiles":len(lib),
        "independent_cluster_and_event_null_probability_paths_verified":True,
        "exact_group_sharp_null_all_profile_conditional_levels_valid":True
    }
    LIB.write_text(json.dumps(library_result,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    anchor=lib[(0,0,0,0,4,4)]
    main={
        "research_id":"R181",
        "status":"E1_ARTIFICIAL_EXACT_SHARP_NULL_GROUP_RANDOMIZATION",
        "protocol":"protocols/"+PROTO.name,
        "R177_pinned_git_blob":R177_SOURCE_BLOB,
        "R177_pinned_results_sha256":R177_RESULT_SHA256,
        "source_worlds":10,
        "unordered_profiles_per_world":210,
        "actual_assignments_per_profile":20,
        "total_source_weighted_assignment_rows":42000,
        "balanced_group_permutation_and_individual_hypergeom_both_dual_verified":True,
        "zero_effect_sharp_null_all_worlds":True,
        "fixed_profile_000044":anchor,
        "true_level_alpha":[str(a) for a in ALPHAS],
        "all_source_worlds":worlds_out,
        "ordered_assignment_csv_sha256":sha256(CSV.read_bytes()).hexdigest(),
        "full_profile_library_sha256":sha256(LIB.read_bytes()).hexdigest(),
        "human_or_real_historical_data_scored":False,
        "new_E2":0,"new_E3":0
    }
    OUT.write_text(json.dumps(main,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    accepted={
        "research_id":"R181",
        "status":"CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_RANDOMIZATION",
        "worlds":10,"unordered_count_profiles":210,
        "actual_assignment_choices":20,"weighted_analysis_rows":42000,
        "original_ordered_group_count_universe_per_world":15625,
        "source_R177_SHA_authenticated":True,
        "independent_full_permutation_distributions_both_methods":True,
        "correct_randomization_conditional_and_unconditional_null_level_bounded":True,
        "invalid_individual_assignment_distribution_distinguished":True,
        "result_sha256":sha256(OUT.read_bytes()).hexdigest(),
        "sample_csv_sha256":main["ordered_assignment_csv_sha256"],
        "profile_library_sha256":main["full_profile_library_sha256"],
        "new_E2":0,"new_E3":0,
    }
    ACCEPT.write_text(json.dumps(accepted,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("R181_MACHINE_ACCEPTANCE",json.dumps(accepted,sort_keys=True))
    print("R181_ALL_NULL_FALSE_REJECTION",json.dumps(worlds_out,sort_keys=True))
    return main


class TestExactClusterRandomization(unittest.TestCase):
    def test_ten_worlds(self):
        self.assertEqual(len(list(worlds())),10)
    def test_treatment_assignment_count(self):
        self.assertEqual(len(ASSIGNMENTS),20)
    def test_group_profiles_count(self):
        self.assertEqual(len(PROFILES),210)
    def test_total_analysis_rows(self):
        self.assertEqual(len(PROFILES)*len(ASSIGNMENTS)*len(list(worlds())),42000)
    def test_ordered_source_group_universe(self):
        self.assertEqual((EVENTS_PER_GROUP+1)**N_GROUPS,15625)
    def test_source_pin(self):
        a,b=original_source()
        self.assertEqual(a("BB",4,F(1,4),0),b("BB",4,F(1,4),0))
    def test_all_twenty_sharp_assignment_exact_PMF(self):
        for profile in PROFILES:
            self.assertEqual(group_perm_enum(profile),group_perm_dp(profile))
    def test_all_individual_hypergeom_laws_exact(self):
        for S in range(25):
            self.assertEqual(individual_perm_hypergeom(S),individual_perm_draw_dp(S))
    def test_cluster_permutation_probability_one(self):
        for profile in PROFILES:
            self.assertEqual(sum(group_perm_enum(profile),F(0)),1)
    def test_individual_probability_one(self):
        for S in range(25):
            self.assertEqual(sum(individual_perm_draw_dp(S),F(0)),1)
    def test_fixed_profile_level_000044(self):
        pro=(0,0,0,0,4,4)
        group=group_perm_enum(pro)
        self.assertEqual(group[0],F(1,5))
        self.assertEqual(group[4],F(3,5))
        self.assertEqual(group[8],F(1,5))
    def test_fixed_profile_extreme_p_cluster(self):
        pro=(0,0,0,0,4,4)
        self.assertEqual(sharp_two_sided_p(8,8,group_perm_enum(pro)),F(2,5))
    def test_fixed_profile_extreme_p_naive_much_smaller(self):
        pro=(0,0,0,0,4,4)
        self.assertLess(sharp_two_sided_p(8,8,individual_perm_hypergeom(8)),F(1,10))
    def test_20_balanced_assignments_each_complement(self):
        al=set(ASSIGNMENTS)
        self.assertTrue(all(tuple(i for i in range(6) if i not in c) in al for c in al))
    def test_all_true_group_conditional_type1(self):
        lib=library_of_profiles()
        for entry in lib.values():
            for alpha,index in ((F(1,10),"cluster_reject_alpha_0p1"),(F(1,5),"cluster_reject_alpha_0p2")):
                rate=F(sum(o[index] for o in entry["all_20_true_cluster_assignments"]),20)
                self.assertLessEqual(rate,alpha)
    def test_profile_multiset_multiplicity(self):
        self.assertEqual(profile_multiplier((0,0,0,0,4,4)),15)
        self.assertEqual(profile_multiplier((1,2,3,4,4,4)),120)
    def test_all_profiles_source_probability_sums_one(self):
        formula,_=original_source()
        for p,name,family,regime in worlds():
            law=formula(family,4,p,regime)
            self.assertEqual(sum((profile_mass(pro,law) for pro in PROFILES),F(0)),1)
    def test_profile_probability_nonnegative(self):
        f,_=original_source()
        pmf=f("BB",4,F(1,4),0)
        self.assertGreater(profile_mass((0,0,0,0,4,4),pmf),0)
    def test_randomized_equal_cluster_results_no_rejection(self):
        pro=(2,2,2,2,2,2)
        self.assertEqual(sharp_two_sided_p(12,6,group_perm_enum(pro)),1)
    def test_randomization_truth_unit_unchanged(self):
        pro=(0,1,1,2,3,4)
        s=sum(pro)
        for a in ASSIGNMENTS:
            t=sum(pro[i] for i in a)
            self.assertEqual(t+(s-t),s)
    def test_invalid_profile_length(self):
        with self.assertRaises(ValueError):
            group_perm_dp((0,1))
    def test_invalid_total_success(self):
        with self.assertRaises(ValueError):
            individual_perm_hypergeom(-1)
    def test_invalid_profile_order(self):
        with self.assertRaises(ValueError):
            profile_multiplier((4,0,0,0,0,0))
    def test_all_source_PMF_dual_methods(self):
        a,b=original_source()
        for p,name,family,regime in worlds():
            self.assertEqual(a(family,4,p,regime),b(family,4,p,regime))
    def test_two_sided_p_complement_symmetry(self):
        pro=(0,0,1,2,3,4)
        pmf=group_perm_dp(pro)
        total=sum(pro)
        for t in range(total+1):
            if total-t>=0:
                self.assertEqual(sharp_two_sided_p(total,t,pmf),
                                 sharp_two_sided_p(total,total-t,pmf))
    def test_group_and_individual_permutation_not_identical(self):
        pro=(0,0,0,0,4,4)
        self.assertNotEqual(group_perm_dp(pro),individual_perm_hypergeom(8))
    def test_tied_scores_all_included(self):
        pro=(0,0,0,0,4,4)
        self.assertEqual(sharp_two_sided_p(8,4,group_perm_dp(pro)),1)
    def test_actual_permutation_not_nonzero_effect_estimation(self):
        self.assertEqual(TREAT_GROUPS,3)


if __name__=="__main__":
    if sys.argv[1:]==["--test"]:
        unittest.main(argv=[sys.argv[0]],verbosity=2)
    elif sys.argv[1:]==["--run-and-archive"]:
        run();archive()
    else:
        raise SystemExit("use --test or --run-and-archive")
