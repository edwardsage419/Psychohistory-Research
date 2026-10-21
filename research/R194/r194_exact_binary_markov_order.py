"""R194 exact first/second-order binary Markov trajectory prediction.

24 artificial worlds, 2064 source-weighted ordered training trajectory sets
and 196 order-equivalent fit profiles. Independent path-product and dynamic
generators, independent transition-count likelihoods, and double-precision
versus Decimal future NEW trajectory logloss verify finite known candidates.
No real human, social or historical sequences; R073 remains frozen.
"""
from __future__ import annotations

from collections import Counter,defaultdict
from decimal import Decimal,localcontext
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from itertools import product,combinations_with_replacement
from math import log
from pathlib import Path
import csv,json,sys,unittest,zipfile

HERE=Path(__file__).resolve().parent
PROTO=HERE.parent.parent/"protocols/R194_MARKOV_24_WORLDS_2064_TRAJECTORIES_PRESCORE_FREEZE_2026-10-21.md"
RESULT=HERE/"R194_EXACT_RESULTS.json"
ORIGINAL=HERE/"R194_ALL_2064_ORDERED_TRAINING_TRAJECTORY_SETS.csv"
FITS=HERE/"R194_ALL_196_MARKOV_FIT_PROFILES.json"
ACCEPT=HERE/"R194_FINAL_MACHINE_ACCEPTANCE.json"
ARCH=HERE/"R194_24_Exact_Markov_Trajectory_Worlds.zip"
CANDIDATES=("IID","SWITCH","PERSIST","STICKY","LAG2_SWITCH","LAG2_REPEAT")
SOURCE_SPECS={
    "IID":(1,F(1,2)),
    "SWITCH":(1,F(1,4)),
    "PERSIST":(1,F(3,4)),
    "STICKY":(1,F(7,8)),
    "LAG2_SWITCH":(2,F(1,4)),
    "LAG2_REPEAT":(2,F(3,4)),
}
LENGTHS=(3,4)
M_VALUES=(1,2)


def worlds():
    for source,length,m in product(CANDIDATES,LENGTHS,M_VALUES):
        yield source,length,m


def validate(source,length):
    if source not in CANDIDATES or length not in LENGTHS:
        raise ValueError("Markov source or trajectory length outside frozen design")


@lru_cache(maxsize=None)
def paths(length):
    if length not in LENGTHS:
        raise ValueError("unsupported path length")
    return tuple(product((0,1),repeat=length))


def conditional_next_one(source,prefix):
    if source not in SOURCE_SPECS or len(prefix)<SOURCE_SPECS[source][0]:
        raise ValueError("insufficient previous states for Markov candidate")
    order,repeat=SOURCE_SPECS[source]
    previous=prefix[-order]
    return repeat if previous==1 else 1-repeat


def last_step_probability(source,prefix,outcome):
    if outcome not in (0,1):
        raise ValueError("target state must be binary")
    p1=conditional_next_one(source,prefix)
    return p1 if outcome else 1-p1


def path_probability_direct(source,length,path):
    """A: exact forward product of first/second-order conditional steps."""
    validate(source,length)
    if len(path)!=length or any(y not in (0,1) for y in path):
        raise ValueError("source state sequence not in registered support")
    order,_=SOURCE_SPECS[source]
    mass=F(1,2)**order
    for j in range(order,length):
        mass*=last_step_probability(source,path[:j],path[j])
    return mass


@lru_cache(maxsize=None)
def trajectory_DP(source,length):
    """B: generative prefix-state expansion, not original path-product."""
    validate(source,length)
    order,repeat=SOURCE_SPECS[source]
    state={prefix:F(1,2)**order for prefix in product((0,1),repeat=order)}
    for t in range(order,length):
        new=defaultdict(F)
        for prefix,mass in state.items():
            parent=prefix[-order]
            for next_state in (0,1):
                prob=(repeat if next_state==parent else 1-repeat)
                new[prefix+(next_state,)]+=mass*prob
        state=dict(new)
    return state


@lru_cache(maxsize=None)
def source_distribution(source,length):
    dp=trajectory_DP(source,length)
    full=tuple(path_probability_direct(source,length,p) for p in paths(length))
    alternate=tuple(dp.get(p,F(0)) for p in paths(length))
    if full!=alternate or sum(full,F(0))!=1 or min(full)<=0:
        raise AssertionError("independent trajectory product and state DP do not agree")
    return full


def source_single_and_pair_marginals(source,length):
    pmf=source_distribution(source,length)
    seqs=paths(length)
    singles=[]
    pairs=[]
    for pos in range(length):
        p1=sum((mass for x,mass in zip(seqs,pmf) if x[pos]==1),F(0))
        singles.append(p1)
        if p1!=F(1,2):
            raise AssertionError("symmetric artificial Markov mechanism not stationary in one-time marginals")
    for pos in range(length-1):
        joint=tuple(sum((mass for x,mass in zip(seqs,pmf)
                         if (x[pos],x[pos+1])==pair),F(0))
                    for pair in ((0,0),(0,1),(1,0),(1,1)))
        pairs.append(joint)
        if SOURCE_SPECS[source][0]==2 and joint!=(F(1,4),)*4:
            raise AssertionError("lag-two source should have pairwise independent adjacent states")
    return singles,pairs


def transition_count_likelihood(source,length,path):
    """Independent count-of-transition route, NOT trajectory product."""
    validate(source,length)
    if len(path)!=length or any(x not in (0,1) for x in path):
        raise ValueError("out-of-support count path")
    order,repeat=SOURCE_SPECS[source]
    observed_counts=Counter()
    for t in range(order,length):
        preceding=tuple(path[t-order:t])
        observed_counts[preceding+(path[t],)]+=1
    score=F(1,2)**order
    for event,count in observed_counts.items():
        prior_state=event[0]
        subsequent=event[-1]
        score*=(repeat if subsequent==prior_state else 1-repeat)**count
    if score!=path_probability_direct(source,length,path):
        raise AssertionError("independent transition-count path likelihood differs")
    return score


def dataset_likelihood_direct(path_indices,source_pmf):
    out=F(1)
    for index in path_indices:
        out*=source_pmf[index]
    return out


def dataset_likelihood_counts(path_indices,source_pmf):
    out=F(1)
    for index,count in Counter(path_indices).items():
        out*=source_pmf[index]**count
    return out


def fit_profile(length,indices):
    if (length not in LENGTHS or len(indices) not in M_VALUES
        or tuple(indices)!=tuple(sorted(indices))
        or any(v not in range(2**length) for v in indices)):
        raise ValueError("invalid original training path profile")
    likes={}
    for candidate in CANDIDATES:
        pmf=source_distribution(candidate,length)
        left=dataset_likelihood_direct(indices,pmf)
        right=dataset_likelihood_counts(indices,pmf)
        if left!=right:
            raise AssertionError("two session likelihood constructions differ")
        likes[candidate]=left
    best=max(likes.values())
    selected=next(c for c in CANDIDATES if likes[c]==best)
    return {
        "L":length,"m":len(indices),"sorted_training_paths":indices,
        "all_candidate_exact_training_likelihoods":likes,
        "best_candidate":selected,
        "all_source_transition_PMF_and_training_likelihood_paths_verified":True
    }


@lru_cache(maxsize=None)
def fit_library():
    fit={}
    for length,m in product(LENGTHS,M_VALUES):
        for indices in combinations_with_replacement(range(2**length),m):
            fit[(length,indices)]=fit_profile(length,indices)
    if len(fit)!=196:
        raise AssertionError("frozen 196 sorted path profiles missing")
    return fit


@lru_cache(maxsize=None)
def independent_future_last_step_loss(source,selected,length):
    """Predict final state in entirely NEW trajectory, after seeing its prefix."""
    seqs=paths(length)
    true=source_distribution(source,length)
    float_loss=0.0
    decimal_loss=Decimal(0)
    brier=F(0)
    for obs,mass in zip(seqs,true):
        p_correct=last_step_probability(selected,obs[:-1],obs[-1])
        p1=conditional_next_one(selected,obs[:-1])
        float_loss-=float(mass)*log(float(p_correct))
        with localcontext() as ctx:
            ctx.prec=60
            decimal_loss-=((Decimal(mass.numerator)/Decimal(mass.denominator))*
                           (Decimal(p_correct.numerator)/Decimal(p_correct.denominator)).ln())
        brier+=mass*((1-p1)**2 if obs[-1] else p1**2)
    if abs(float_loss-float(decimal_loss))>1e-12:
        raise AssertionError("new session logloss math and Decimal do not agree")
    # Truly independent conditional next-step Brier uses only prefix distribution.
    prefix_prob=defaultdict(F)
    for obs,mass in zip(seqs,true):
        prefix_prob[obs[:-1]]+=mass
    brier_cond=F(0)
    for prefix,mass in prefix_prob.items():
        truth_p=conditional_next_one(source,prefix)
        predicted_p=conditional_next_one(selected,prefix)
        brier_cond+=mass*(truth_p*(1-predicted_p)**2+(1-truth_p)*predicted_p**2)
    if brier!=brier_cond:
        raise AssertionError("full trajectory vs independent conditional next-step Brier differ")
    return float_loss,decimal_loss,brier


def run_world(source,length,m,all_records):
    truth=source_distribution(source,length)
    single,pairs=source_single_and_pair_marginals(source,length)
    selection={c:F(0) for c in CANDIDATES}
    training_total=F(0)
    score=0.0
    score_high=Decimal(0)
    brier=F(0)
    samples=0
    for indices in product(range(2**length),repeat=m):
        sample_prob=dataset_likelihood_direct(indices,truth)
        fit=fit_library()[(length,tuple(sorted(indices)))]
        chosen=fit["best_candidate"]
        test=float(independent_future_last_step_loss(source,chosen,length)[0])
        decimal=independent_future_last_step_loss(source,chosen,length)[1]
        loss_brier=independent_future_last_step_loss(source,chosen,length)[2]
        selection[chosen]+=sample_prob
        training_total+=sample_prob
        score+=float(sample_prob)*test
        score_high+=(Decimal(sample_prob.numerator)/Decimal(sample_prob.denominator))*decimal
        brier+=sample_prob*loss_brier
        samples+=1
        all_records.append({
            "source_Markov_mechanism":source,"trajectory_length_L":length,
            "independent_training_trajectories_m":m,
            "ordered_training_trajectory_indices":",".join(map(str,indices)),
            "ordered_training_binary_paths":";".join("".join(map(str,paths(length)[i])) for i in indices),
            "true_training_joint_probability":str(sample_prob),
            "sorted_training_fit_profile":",".join(map(str,sorted(indices))),
            **{f"candidate_likelihood_{c}":str(fit["all_candidate_exact_training_likelihoods"][c]) for c in CANDIDATES},
            "chosen_model":chosen,
            "heldout_NEW_trajectory_final_step_logloss":format(test,".16g"),
            "heldout_NEW_trajectory_final_step_Brier":str(loss_brier)
        })
    if samples!=(2**length)**m or training_total!=1 or sum(selection.values(),F(0))!=1:
        raise AssertionError("full true training session probability not one")
    if abs(score-float(score_high))>1e-12:
        raise AssertionError("full world expected new trajectory numeric scores disagree")
    return {
        "source":source,"source_order":SOURCE_SPECS[source][0],
        "source_repeat_probability":str(SOURCE_SPECS[source][1]),
        "L":length,"m":m,"complete_ordered_training_datasets":samples,
        "one_time_marginals_P_state_1":[str(v) for v in single],
        "adjacent_time_pair_probabilities_00_01_10_11":[[str(q) for q in v] for v in pairs],
        "train_selected_candidate_probabilities":{k:str(v) for k,v in selection.items()},
        "train_select_true_source_probability":str(selection[source]),
        "independent_new_trajectory_last_state_expected_logloss":format(score,".16g"),
        "independent_new_trajectory_last_state_expected_Brier":str(brier),
        "all_full_original_sessions_and_double_scored_new_paths":True
    }


def serialize_fits(fits):
    return [{
        "L":length,"m":len(ind),"sorted_trajectory_index_profile":list(ind),
        "selected":fit["best_candidate"],
        "all_candidate_training_Fraction_likelihoods":{
            k:str(v) for k,v in fit["all_candidate_exact_training_likelihoods"].items()},
        "independent_full_path_and_transition_count_algorithms":True
    } for (length,ind),fit in sorted(fits.items())]


def run():
    all_records=[]
    worlds_out=[run_world(*spec,all_records) for spec in worlds()]
    if len(worlds_out)!=24 or len(all_records)!=2064:
        raise AssertionError("full Markov source count not as frozen")
    for source in CANDIDATES:
        for length in LENGTHS:
            source_single_and_pair_marginals(source,length)
            for trajectory in paths(length):
                transition_count_likelihood(source,length,trajectory)
    for length in LENGTHS:
        for source in ("LAG2_REPEAT","LAG2_SWITCH"):
            p=independent_future_last_step_loss(source,"IID",length)
            q=independent_future_last_step_loss(source,source,length)
            if p[2]!=F(1,4) or q[2]!=F(3,16) or not q[0]<p[0]:
                raise AssertionError("frozen lag-two memory vs one-step iid risk contrast failed")
    fits=serialize_fits(fit_library())
    with ORIGINAL.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(all_records[0]),lineterminator="\n")
        writer.writeheader();writer.writerows(all_records)
    FITS.write_text(json.dumps({"research_id":"R194","unique_trajectory_fit_profiles":len(fits),
                                "full_fitted_profiles":fits},sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    fixed=[w for w in worlds_out if w["source"] in ("IID","LAG2_REPEAT","LAG2_SWITCH") and w["L"]==3]
    out={
        "research_id":"R194",
        "stage":"E1_ARTIFICIAL_EXACT_FIRST_VS_SECOND_ORDER_MARKOV_CHAINS",
        "worlds":24,"full_ordered_original_training_sets":2064,
        "unique_fitted_trajectory_profiles":196,
        "all_complete_source_distributions_path_product_vs_prefix_state_DP_exact":True,
        "all_independent_transition_count_and_path_likelihood_exact":True,
        "all_one_time_marginals_stationary_and_equal_one_half":True,
        "two_lag_sources_all_adjacent_pairs_independent_fair":True,
        "IID_one_step_predictor_Brier_lag_two_source":"1/4",
        "true_second_order_predictor_Brier_lag_two_source":"3/16",
        "math_vs_Decimal_heldout_new_session_conditional_logloss_all_verified":True,
        "independent_conditional_and_full_trajectory_Brier_routes_exact":True,
        "prelocked_independent_vs_lag_two_sources":fixed,
        "all_worlds":worlds_out,
        "training_CSV_sha256":sha256(ORIGINAL.read_bytes()).hexdigest(),
        "full_fit_library_sha256":sha256(FITS.read_bytes()).hexdigest(),
        "real_human_or_historical_data":False,"new_E2":0,"new_E3":0
    }
    RESULT.write_text(json.dumps(out,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    acceptance={
        "research_id":"R194","status":"CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_MARKOV_CHAIN_ORDER",
        "worlds":24,"ordered_original_train_sets":2064,"complete_fit_profiles":196,
        "two_independent_full_trajectory_PMF_algorithms_exact":True,
        "transition_count_and_sequential_likelihoods_exact":True,
        "stationary_state_and_adjacent_pair_alias_verified":True,
        "lag_two_source_IID_vs_true_conditional_Brier_valid":True,
        "true_independent_NEW_session_last_state_score_double_verified":True,
        "result_sha256":sha256(RESULT.read_bytes()).hexdigest(),
        "original_CSV_sha256":out["training_CSV_sha256"],
        "complete_profile_library_sha256":out["full_fit_library_sha256"],
        "real_human_or_historical_data":False,"new_E2":0,"new_E3":0
    }
    ACCEPT.write_text(json.dumps(acceptance,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("R194_ACCEPTANCE",json.dumps(acceptance,sort_keys=True))
    print("R194_LOCKED_MEMORY_VS_IID",json.dumps(fixed,sort_keys=True))
    return out


def archive():
    names=[Path(__file__).name,RESULT.name,ORIGINAL.name,FITS.name,ACCEPT.name]
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
    print("R194_ARCHIVE_SHA256",sha256(ARCH.read_bytes()).hexdigest())


class TestMarkovChainOrder(unittest.TestCase):
    def test_24_frozen_worlds(self):
        self.assertEqual(len(list(worlds())),24)
    def test_2064_all_training_session_sets(self):
        self.assertEqual(sum((2**L)**m for src,L,m in worlds()),2064)
    def test_196_unique_training_profiles(self):
        self.assertEqual(len(fit_library()),196)
    def test_six_candidates(self):
        self.assertEqual(len(CANDIDATES),6)
    def test_four_first_order_two_second_order(self):
        self.assertEqual(sum(1 for c in CANDIDATES if SOURCE_SPECS[c][0]==1),4)
        self.assertEqual(sum(1 for c in CANDIDATES if SOURCE_SPECS[c][0]==2),2)
    def test_all_source_full_PMF_path_vs_DP(self):
        for s in CANDIDATES:
            for L in LENGTHS:
                a=source_distribution(s,L)
                self.assertEqual(a,tuple(trajectory_DP(s,L)[p] for p in paths(L)))
    def test_all_source_PMF_positive_and_sum_one(self):
        for s in CANDIDATES:
            for L in LENGTHS:
                x=source_distribution(s,L)
                self.assertEqual(sum(x,F(0)),1)
                self.assertTrue(all(z>0 for z in x))
    def test_independent_path_transition_counter_parity(self):
        for s in CANDIDATES:
            for L in LENGTHS:
                for p in paths(L):
                    self.assertEqual(path_probability_direct(s,L,p),
                                     transition_count_likelihood(s,L,p))
    def test_all_one_time_marginals_half(self):
        for s in CANDIDATES:
            for L in LENGTHS:
                single,pair=source_single_and_pair_marginals(s,L)
                self.assertTrue(all(v==F(1,2) for v in single))
    def test_lag_two_adjacent_all_pairs_uniform(self):
        for s in ("LAG2_SWITCH","LAG2_REPEAT"):
            for L in LENGTHS:
                _,pair=source_single_and_pair_marginals(s,L)
                self.assertTrue(all(z==(F(1,4),)*4 for z in pair))
    def test_true_IID_all_adjacent_pairs_uniform(self):
        for L in LENGTHS:
            _,pair=source_single_and_pair_marginals("IID",L)
            self.assertTrue(all(z==(F(1,4),)*4 for z in pair))
    def test_markov_persist_adjacent_not_uniform(self):
        _,pair=source_single_and_pair_marginals("PERSIST",3)
        self.assertNotEqual(pair[0],(F(1,4),)*4)
    def test_lag_two_full_triplet_differs_from_IID(self):
        for src in ("LAG2_SWITCH","LAG2_REPEAT"):
            self.assertNotEqual(source_distribution(src,3),source_distribution("IID",3))
    def test_IID_conditional_state_one_half(self):
        for p in paths(3):
            self.assertEqual(conditional_next_one("IID",p[:2]),F(1,2))
    def test_lag2_repeat_uses_state_two_steps_back(self):
        self.assertEqual(conditional_next_one("LAG2_REPEAT",(1,0)),F(3,4))
        self.assertEqual(conditional_next_one("LAG2_REPEAT",(0,1)),F(1,4))
    def test_lag2_switch_reverse_probability(self):
        self.assertEqual(conditional_next_one("LAG2_SWITCH",(1,0)),F(1,4))
        self.assertEqual(conditional_next_one("LAG2_SWITCH",(0,1)),F(3,4))
    def test_true_lag2_brier_three_sixteenths(self):
        for L in LENGTHS:
            self.assertEqual(independent_future_last_step_loss("LAG2_REPEAT","LAG2_REPEAT",L)[2],F(3,16))
    def test_wrong_IID_lag2_brier_one_quarter(self):
        for L in LENGTHS:
            self.assertEqual(independent_future_last_step_loss("LAG2_REPEAT","IID",L)[2],F(1,4))
    def test_lag2_true_model_heldout_loss_lower(self):
        for src in ("LAG2_REPEAT","LAG2_SWITCH"):
            for L in LENGTHS:
                self.assertLess(independent_future_last_step_loss(src,src,L)[0],
                                independent_future_last_step_loss(src,"IID",L)[0])
    def test_double_precision_all_source_candidate_combinations(self):
        for source in CANDIDATES:
            for candidate in CANDIDATES:
                for L in LENGTHS:
                    a,b,c=independent_future_last_step_loss(source,candidate,L)
                    self.assertAlmostEqual(a,float(b),places=12)
    def test_independent_Brier_path_vs_prefix_aggregation(self):
        for source in CANDIDATES:
            for candidate in CANDIDATES:
                for L in LENGTHS:
                    independent_future_last_step_loss(source,candidate,L)
    def test_training_likelihood_product_vs_histogram(self):
        for L,m in product(LENGTHS,M_VALUES):
            for seq in product(range(2**L),repeat=m):
                for c in CANDIDATES:
                    pmf=source_distribution(c,L)
                    self.assertEqual(dataset_likelihood_direct(seq,pmf),
                                     dataset_likelihood_counts(seq,pmf))
    def test_full_training_source_probability_one(self):
        for source,L,m in worlds():
            pmf=source_distribution(source,L)
            self.assertEqual(sum((dataset_likelihood_direct(x,pmf)
                                  for x in product(range(2**L),repeat=m)),F(0)),1)
    def test_unique_profiles_all_candidates_fit(self):
        for fit in fit_library().values():
            self.assertIn(fit["best_candidate"],CANDIDATES)
            self.assertTrue(all(v>0 for v in fit["all_candidate_exact_training_likelihoods"].values()))
    def test_sequence_order_invariance(self):
        x=fit_library()[(3,(1,5))]
        self.assertEqual(x["best_candidate"],fit_profile(3,(1,5))["best_candidate"])
    def test_bad_source_rejected(self):
        with self.assertRaises(ValueError):
            source_distribution("NOT_SOURCE",3)
    def test_bad_length_rejected(self):
        with self.assertRaises(ValueError):
            source_distribution("IID",2)
    def test_nonbinary_path_rejected(self):
        with self.assertRaises(ValueError):
            path_probability_direct("IID",3,(0,2,0))
    def test_insufficient_second_order_prefix_rejected(self):
        with self.assertRaises(ValueError):
            conditional_next_one("LAG2_REPEAT",(1,))
    def test_bad_last_state_rejected(self):
        with self.assertRaises(ValueError):
            last_step_probability("IID",(0,1),2)
    def test_invalid_unsorted_training_profile_rejected(self):
        with self.assertRaises(ValueError):
            fit_profile(3,(5,1))
    def test_invalid_too_many_training_sessions_rejected(self):
        with self.assertRaises(ValueError):
            fit_profile(3,(0,0,0))
    def test_state_transition_not_linked_across_sessions(self):
        pmf=source_distribution("PERSIST",3)
        # Two independent complete sessions: never add a cross-session edge.
        self.assertEqual(dataset_likelihood_direct((0,7),pmf),pmf[0]*pmf[7])
        self.assertEqual(dataset_likelihood_counts((0,7),pmf),pmf[0]*pmf[7])


if __name__=="__main__":
    if sys.argv[1:]==["--test"]:
        unittest.main(argv=[sys.argv[0]],verbosity=2)
    elif sys.argv[1:]==["--run-and-archive"]:
        run();archive()
    else:
        raise SystemExit("Use --test or --run-and-archive")
