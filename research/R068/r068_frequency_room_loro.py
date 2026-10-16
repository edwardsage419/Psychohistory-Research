#!/usr/bin/env python3
"""Retrospective R068 E2 four-choice room heldout conditional prediction.

Compares frequency-exponent/social and personal inertia on author's
observed PREVIOUS-ROUND peer counts, adjusted for one's own last choice.
Does not test direct payoff-biased copying or the original binary 3-model rule.
"""
from __future__ import annotations
import argparse, csv, hashlib, io, json, math
from collections import Counter, defaultdict
from pathlib import Path

from r068_toyokawa_lfs_schema import FILE_SPEC, COMMIT
from r068_toyokawa_temporal_cue_audit import (
    CUES, parse_source, maybe_int, audit_semantics,
)

PSEUDO=0.1
RHO=(0.,0.25,0.5,0.75,0.9)
THETA=(0.,0.5,1.,2.,4.)
RHO_MIX=(0.25,0.5,0.75,0.9)
THETA_MIX=(0.5,1.,2.,4.)
MIX_WEIGHT=(0.25,0.5,0.75)
FAMILIES=("uniform","inertia","frequency_exponent","inertia_frequency_mixture")
EXPECTED_SCORE=12329
EXPECTED_ROOMS=38
EXPECTED_MIXED=1


def params(family):
    if family=="uniform":return [("uniform",{})]
    if family=="inertia":
        return [(f"rho={r}",{"rho":r}) for r in RHO]
    if family=="frequency_exponent":
        return [(f"theta={t}",{"theta":t}) for t in THETA]
    if family=="inertia_frequency_mixture":
        return [(f"rho={r},theta={t},w={w}",{"rho":r,"theta":t,"weight":w})
                for r in RHO_MIX for t in THETA_MIX for w in MIX_WEIGHT]
    raise ValueError("unknown model family")


def predict_probs(family,prior,counts,p):
    if prior not in (0,1,2,3) or len(counts)!=4:
        raise ValueError("must have 4 source option slots and an observed own prior")
    if any(type(n) is not int or n<0 for n in counts):
        raise ValueError("negative or nonintegral source peer count")
    if sum(counts)<=0:
        raise ValueError("unobserved peer distribution")
    if family=="uniform":
        probs=[.25]*4
    elif family=="inertia":
        rho=p["rho"]
        if rho not in RHO:
            raise ValueError("outside prespecified inertia")
        probs=[(1-rho)/4+(rho if j==prior else 0) for j in range(4)]
    elif family=="frequency_exponent":
        t=p["theta"]
        if t not in THETA:
            raise ValueError("outside prespecified exponent")
        w=[(n+PSEUDO)**t for n in counts]
        tot=sum(w)
        probs=[v/tot for v in w]
    elif family=="inertia_frequency_mixture":
        r=p["rho"];t=p["theta"];w=p["weight"]
        if r not in RHO_MIX or t not in THETA_MIX or w not in MIX_WEIGHT:
            raise ValueError("outside frozen two-source mixture grid")
        own=predict_probs("inertia",prior,counts,{"rho":r})
        freq=predict_probs("frequency_exponent",prior,counts,{"theta":t})
        probs=[(1-w)*a+w*b for a,b in zip(own,freq)]
    else:
        raise ValueError("unknown model family")
    if (len(probs)!=4 or any(v<=0 or not math.isfinite(v) for v in probs)
        or abs(sum(probs)-1)>1e-11):
        raise ValueError("invalid categorical prediction")
    return probs


def prepared_rooms(rows_group,rows_indiv):
    semantics=audit_semantics(rows_group,rows_indiv)
    if (semantics["semantic_gate"]!="FOUR_CHOICE_PREVIOUS_TRIAL_CUES_RECOVERABLE"
        or semantics["group_distinct_anonymous_rooms"]!=39
        or semantics["group_distinct_anonymous_people"]!=184
        or semantics["group_rooms_with_multiple_risk_distribution_codes"]!=EXPECTED_MIXED
        or semantics["temporal_source_check_counts"]["at_least_one_observed_peer_choice"]!=12674):
        raise ValueError("fixed source temporal semantics changed")
    person_round={}
    room_task=defaultdict(set)
    for row in rows_group:
        person=row["amazonID"]
        rd=maybe_int(row["round"])
        if rd is None or (person,rd) in person_round:
            raise ValueError("source person-round universe changed")
        person_round[(person,rd)]=row
        room_task[row["room"]].add(row["riskDistributionId"])
    mixed={room for room,t in room_task.items() if len(t)!=1}
    rooms=defaultdict(list)
    count_pre_exclusion=0
    valid_mixed=0
    for row in rows_group:
        rd=maybe_int(row["round"])
        if rd is None or rd==1:
            continue
        prior=person_round.get((row["amazonID"],rd-1))
        if prior is None or prior["room"]!=row["room"]:
            continue
        earlier=maybe_int(prior["choice_num"])
        current=maybe_int(row["choice_num"])
        if earlier not in (0,1,2,3) or current not in (0,1,2,3):
            continue
        freq=[maybe_int(row[name]) for name in CUES]
        if any(x is None or x<0 for x in freq):
            continue
        freq[earlier]-=1
        if any(x<0 for x in freq) or sum(freq)==0:
            continue
        count_pre_exclusion+=1
        if row["room"] in mixed:
            valid_mixed+=1
            continue
        room=row["room"]
        task=row["riskDistributionId"]
        if task not in ("11","12"):
            raise ValueError("outside expected four-option experimental tasks")
        rooms[room].append((current,earlier,tuple(freq),task))
    if (count_pre_exclusion!=12674 or valid_mixed!=345 or
        sum(len(v) for v in rooms.values())!=EXPECTED_SCORE or
        len(rooms)!=EXPECTED_ROOMS):
        raise ValueError("38-room scoring and exclusion denominator drift")
    task_counts=Counter()
    for room,obs in rooms.items():
        tasks={t for _,_,_,t in obs}
        if len(tasks)!=1:
            raise ValueError("room task failed homogeneity")
        task_counts[next(iter(tasks))]+=1
    if set(task_counts)!={"11","12"}:
        raise ValueError("two experimental task types required")
    return rooms,{"source_group_rows":len(rows_group),
                  "source_group_people":184,
                  "total_rooms":39,"mixed_rooms_excluded":1,
                  "valid_pre_exclusion":count_pre_exclusion,
                  "valid_mixed_task_room_excluded":valid_mixed,
                  "eligible_heldout_rooms":len(rooms),
                  "scored_group_trial_decisions":sum(len(v) for v in rooms.values()),
                  "risk_task_room_counts":dict(sorted(task_counts.items())),
                  "four_option_cue_semantics":"previous trial peer counts excluding own earlier choice"}


def room_losses(rooms):
    cache={}
    for family in FAMILIES:
        candidates={}
        for label,p in params(family):
            by_room={}
            for room,observations in rooms.items():
                err=0.
                for choice,last,counts,task in observations:
                    probs=predict_probs(family,last,counts,p)
                    err-=math.log(probs[choice])
                by_room[room]=err/len(observations)
            candidates[label]=by_room
        cache[family]=candidates
    return cache


def choose_other_rooms(candidates,heldout):
    keys=sorted(next(iter(candidates.values())))
    train=[r for r in keys if r!=heldout]
    if len(train)!=len(keys)-1 or not train:
        raise ValueError("heldout room missing or invalid")
    ranking=[]
    for i,(label,room_err) in enumerate(candidates.items()):
        if set(room_err)!=set(keys):
            raise ValueError("candidate missing a room")
        mean=sum(room_err[r] for r in train)/len(train)
        ranking.append((mean,i,label))
    return min(ranking,key=lambda x:(x[0],x[1]))[2]


def score_rooms(rooms,cache):
    if len(rooms)!=EXPECTED_ROOMS:
        raise ValueError("fixed 38 room universe required")
    out={}
    for family in FAMILIES:
        options=cache[family]
        aggregate=[]
        chosen=Counter()
        for room in sorted(rooms):
            label=choose_other_rooms(options,room)
            chosen[label]+=1
            loss=options[label][room]
            task=rooms[room][0][-1]
            aggregate.append((task,loss,len(rooms[room])))
        if len(aggregate)!=EXPECTED_ROOMS or sum(x[2] for x in aggregate)!=EXPECTED_SCORE:
            raise ValueError("source heldout scoring universe drift")
        out[family]={
            "heldout_room_count":len(aggregate),
            "scored_trial_decisions":sum(x[2] for x in aggregate),
            "primary_room_equal_NLL_nats":sum(x[1] for x in aggregate)/len(aggregate),
            "secondary_trial_weighted_NLL_nats":sum(x[1]*x[2] for x in aggregate)/EXPECTED_SCORE,
            "task_11_room_equal_NLL_nats":sum(x[1] for x in aggregate if x[0]=="11")/sum(x[0]=="11" for x in aggregate),
            "task_12_room_equal_NLL_nats":sum(x[1] for x in aggregate if x[0]=="12")/sum(x[0]=="12" for x in aggregate),
            "heldout_training_selected_parameters":dict(sorted(chosen.items())),
            "individual_trial_or_room_outcomes_exported":False,
        }
    return out


def evaluate(folder:Path):
    src={name:(folder/name).read_bytes() for name in FILE_SPEC}
    group=parse_source("allBehaviour1022_group.csv",src["allBehaviour1022_group.csv"])
    indiv=parse_source("allBehaviour1022_indiv.csv",src["allBehaviour1022_indiv.csv"])
    rooms,counts=prepared_rooms(group,indiv)
    losses=room_losses(rooms)
    result=score_rooms(rooms,losses)
    return {
        "research_id":"R068","stage":"E2_TOYOKAWA_38_ROOM_FREQUENCY_HELDOUT",
        "status":"SOURCE_PINNED_38_ROOM_HELDOUT_COMPLETE",
        "protocol":"protocols/R068_E2_38_ROOM_FREQUENCY_HOLDOUT_2026-10-16.md",
        "upstream":"WataruToyokawa/ToyokawaGaissmaier2021",
        "upstream_commit":COMMIT,
        "source_LFS_sha256":{k:v["sha256"] for k,v in FILE_SPEC.items()},
        "source_counts":counts,
        "class_scores":result,
        "target":"one-step conditional 4-option human choice from PREVIOUS-trial peer frequencies and own previous choice",
        "score":"room-equal heldout categorical logloss nats; smaller is better",
        "source_provenance":"original author repo human experimental data E2",
        "original_hierarchical_RL_cmdstanr":"NOT_REPRODUCED",
        "E1_three_demonstrator_binary_mechanism":"NOT_DIRECTLY_IDENTIFIED_BY_THIS_DATA",
        "success_payoff_social_demonstrator_model":"NOT_OBSERVABLE_FROM_PEER_FREQUENCY_ONLY",
        "causal_learning_mechanism":"NOT_ESTABLISHED",
        "independent_external_E3":"OPEN",
        "raw_participant_data_exported":False,
        "pesen_v01":"FROZEN",
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--source-dir",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()
    try:
        result=evaluate(args.source_dir)
    except (ValueError,OSError,UnicodeError,csv.Error) as e:
        result={"research_id":"R068","stage":"E2_TOYOKAWA_38_ROOM_FREQUENCY_HELDOUT",
                "status":"FAIL_CLOSED",
                "reason_type":type(e).__name__,
                "reason":str(e)[:140],
                "raw_participant_data_exported":False,
                "pesen_v01":"FROZEN"}
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":result["status"],"source_counts":result.get("source_counts"),
                      "room_NLL":{m:record["primary_room_equal_NLL_nats"]
                         for m,record in result.get("class_scores",{}).items()},
                      "selected":{m:record["heldout_training_selected_parameters"]
                         for m,record in result.get("class_scores",{}).items()}},sort_keys=True))
    if result["status"]!="SOURCE_PINNED_38_ROOM_HELDOUT_COMPLETE":
        raise RuntimeError("R068 real room heldout evaluation failed")


if __name__=="__main__":
    main()
