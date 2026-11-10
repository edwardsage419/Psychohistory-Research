"""Independent exact joint stopping-state DP for frozen R289 S85.

No original program, source ledger or archived means/selection labels imported.
Rewards are integers in half-unit scale; fractions enter only probability mass.
"""
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
import json

NAMES=("UNIFORM","LOW_HEAVY","HIGH_HEAVY")
WEIGHTS={"UNIFORM":(1,1,1),"LOW_HEAVY":(2,1,1),"HIGH_HEAVY":(1,1,2)}
VALUES=(1,3,5)
TAGS=("duplicate","missing","weight_mutation","payoff_mutation","difference_mutation","incorrect_tie_rule")


def require(condition,reason):
    if not condition:raise ValueError(reason)


@lru_cache(maxsize=3)
def _law(name):
    require(type(name) is str and name in NAMES,"UNFROZEN_DISTRIBUTION")
    weights=WEIGHTS[name];base=sum(weights)
    states={(None,None):F(1)}
    for index in range(4):
        following=defaultdict(F)
        for state,mass in states.items():
            for offer,weight in zip(VALUES,weights):
                updated=tuple(2*offer-index if reward is None and (offer>=h or index==3) else reward
                              for reward,h in zip(state,(3,5)))
                following[updated]+=mass*F(weight,base)
        require(sum(following.values(),F(0))==1,"JOINT_DP_MASS")
        states=dict(following)
    require(all(all(type(r) is int for r in state) for state in states),"UNSTOPPED_TERMINAL_STATE")
    return tuple(states.items())


def joint_law(name):return dict(_law(name))


def reward2(source,h):
    require(type(source) is str and len(source)==4 and set(source)<={"1","3","5"} and
            type(h) is int and h in (3,5),"UNFROZEN_FIRST_PASSAGE")
    # First passage written as an index minimum, separately from state DP.
    index=min([i for i,offer in enumerate(source[:3]) if int(offer)>=h]+[3])
    return 2*int(source[index])-index


def distribution(name,m):
    require(type(m) is int and m in (1,2),"UNFROZEN_TRAIN_SIZE")
    episode=defaultdict(F)
    for pair,mass in joint_law(name).items():episode[pair[1]-pair[0]]+=mass
    totals={0:F(1)}
    for _ in range(m):
        following=defaultdict(F)
        for previous,p in totals.items():
            for delta,q in episode.items():following[previous+delta]+=p*q
        totals=dict(following)
    require(sum(totals.values(),F(0))==1,"TRAIN_DP_MASS")
    return totals


def world(name,m):
    law=joint_law(name);training=distribution(name,m)
    means=[sum((mass*F(pair[i],2) for pair,mass in law.items()),F(0)) for i in (0,1)]
    p5=sum((mass for delta,mass in training.items() if delta>0),F(0))
    tie=training.get(0,F(0));fresh=F(0)
    # Explicit product law: train selection is made before an independent
    # future episode is drawn. No per-test max and no training reward substitution.
    for delta,train_mass in training.items():
        selected=1 if delta>0 else 0
        for future,future_mass in law.items():fresh+=train_mass*future_mass*F(future[selected],2)
    best=max(means);inferior=p5 if means[0]>means[1] else 1-p5 if means[1]>means[0] else F(0)
    first=sum((F(w,sum(WEIGHTS[name]))*offer for w,offer in zip(WEIGHTS[name],VALUES)),F(0))
    return {"distribution":name,"training_episodes":m,"training_source_tuples":81**m,
            "expected_H3":str(means[0]),"expected_H5":str(means[1]),"first_only":str(first),
            "probability_select_H5":str(p5),"probability_training_tie":str(tie),
            "probability_select_inferior":str(inferior),"independent_test_expected_net":str(fresh),
            "oracle_of_two_thresholds":str(best),"regret_vs_best_fixed_threshold":str(best-fresh),
            "gain_over_first_only":str(fresh-first),"evidence":"E1_ARTIFICIAL_NONBLIND"}


@lru_cache(maxsize=1)
def _expected_json():
    worlds=[world(name,m) for name in NAMES for m in (1,2)]
    polynomial=[{"distribution":name,"m":m,"p5":world(name,m)["probability_select_H5"],
                 "tie":world(name,m)["probability_training_tie"],"support":len(distribution(name,m))}
                for name in NAMES for m in (1,2)]
    return json.dumps({"study":"R289_S85","scope":"E1_ARTIFICIAL_NONBLIND",
        "freeze_commit":"f018236900fa00368c8980db5402ce4267d59c7c",
        "original_source_git_blob":"261d821044278d05db1d15e85e20cef8aafbe5a4",
        "source_rows":243,"worlds":worlds,"independent_polynomial":polynomial,
        "mutation_tests":[{"tag":tag,"rejected":True} for tag in TAGS],
        "R073":"FROZEN","PESEN_v0_1":"FROZEN","new_E2":0,"new_E3":0,"external_replication":0})


def expected_tree():return json.loads(_expected_json())
