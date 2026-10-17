#!/usr/bin/env python3
"""R103 B: original dyadic actor/opponent exact mutual roster without C/D action values."""
from __future__ import annotations
import argparse
from collections import Counter,defaultdict
import csv
import hashlib
import io
import json
import math
import pathlib
import re
import urllib.request

from r103_phase_a_2016_drbrain_original_md5_header_only import (
    URL,CAP,ExactOfficialRedirect,SourceError,validate_url,
    audit_firstparty_bytes_header_only
)
PINNED_SOURCE_SHA="c63b99ba7554908e54393eb9f8267a98de1a3d9bdd123a77f60f2b2122236013"
PINNED_LINES=8477
PUBLIC_GAME=re.compile(r"[A-Za-z0-9_ '/\-]{1,50}")
ID_COLUMNS=("Experiment_number","User_ID","Round_number","Opponent_ID","Game","S","T")

def positive_integer(value):
    if not isinstance(value,str) or not value.isascii() or not value.isdecimal():
        raise SourceError("R103_B_ORIGINAL_PERSON_EXPERIMENT_ROUND_NOT_POSITIVE_DECIMAL")
    n=int(value)
    if n<1 or n>10**12:
        raise SourceError("R103_B_ORIGINAL_PERSON_EXPERIMENT_ROUND_ID_OUT_OF_BOUND")
    return n

def payoff(value):
    try:
        v=float(value)
    except (TypeError,ValueError) as exc:
        raise SourceError("R103_B_ORIGINAL_GAME_PAYOFF_NOT_NUMERIC") from exc
    if not math.isfinite(v) or not -100<=v<=100:
        raise SourceError("R103_B_ORIGINAL_GAME_PAYOFF_NOT_FINITE_BOUNDED")
    return v

def identity_only(raw):
    source=audit_firstparty_bytes_header_only(raw)
    if source["original_project_computed_SHA256"]!=PINNED_SOURCE_SHA or source["source_physical_data_lines_without_parsing"]!=PINNED_LINES:
        raise SourceError("R103_B_ORIGINAL_SOURCE_SHA_OR_LINES_DIFFER")
    reader=csv.DictReader(io.StringIO(raw.decode("utf-8-sig"),newline=""),strict=True)
    allrows={}
    self_pointing_rows=set()
    games=Counter()
    payoff_rules=set()
    experiment_users=defaultdict(set)
    experiment_rounds=defaultdict(set)
    user_experiments=defaultdict(set)
    per_person_rounds=defaultdict(set)
    observed=0
    for row in reader:
        observed+=1
        if observed>PINNED_LINES or None in row or any(row.get(k) is None for k in ID_COLUMNS):
            raise SourceError("R103_B_ORIGINAL_CSV_ROW_STRUCTURE_INVALID")
        # IMPORTANT: never dereference Action or Opponent_Action source cells.
        experiment=positive_integer(row["Experiment_number"])
        actor=positive_integer(row["User_ID"])
        t=positive_integer(row["Round_number"])
        opponent=positive_integer(row["Opponent_ID"])
        self_pointing=(actor==opponent)
        game=row["Game"]
        if not isinstance(game,str) or PUBLIC_GAME.fullmatch(game) is None:
            raise SourceError("R103_B_ORIGINAL_GAME_CODE_UNSAFE")
        S=payoff(row["S"])
        T=payoff(row["T"])
        key=(experiment,actor,t)
        if key in allrows:
            raise SourceError("R103_B_DUPLICATE_ORIGINAL_PERSON_ROUND")
        allrows[key]=opponent
        if self_pointing:
            self_pointing_rows.add(key)
        experiment_users[experiment].add(actor)
        experiment_rounds[experiment].add(t)
        user_experiments[actor].add(experiment)
        per_person_rounds[(experiment,actor)].add(t)
        games[game]+=1
        payoff_rules.add((S,T,game))
    if observed!=PINNED_LINES:
        raise SourceError("R103_B_ORIGINAL_SOURCE_ROW_COUNT_CHANGED")
    reciprocal=0
    missing=0
    nonreciprocal=0
    per_experiment=defaultdict(Counter)
    for (experiment,actor,t),opponent in allrows.items():
        if (experiment,actor,t) in self_pointing_rows:
            per_experiment[experiment]["self_pointing_source_actor_rounds"]+=1
            continue
        opp=allrows.get((experiment,opponent,t))
        if opp is None:
            missing+=1
            per_experiment[experiment]["missing_opponent_row"]+=1
        elif opp!=actor or (experiment,opponent,t) in self_pointing_rows:
            nonreciprocal+=1
            per_experiment[experiment]["opponent_nonreciprocal"]+=1
        else:
            reciprocal+=1
            per_experiment[experiment]["reciprocal_actor_rounds"]+=1
    if reciprocal%2:
        raise SourceError("R103_B_RECIPROCAL_ACTOR_ROUNDS_MUST_BE_EVEN")
    experiment_count=len(experiment_users)
    eligible_experiments=sum(per_experiment[e]["reciprocal_actor_rounds"]>0 for e in experiment_users)
    criteria=(reciprocal/observed>=0.95 and eligible_experiments>=30 and
              experiment_count>=30)
    output=[]
    for slot,ex in enumerate(sorted(experiment_users),1):
        output.append({
            "anonymous_original_experiment_slot":slot,
            "distinct_original_actor_codes":len(experiment_users[ex]),
            "distinct_original_round_numbers":len(experiment_rounds[ex]),
            "reciprocal_actor_rounds":per_experiment[ex]["reciprocal_actor_rounds"],
            "missing_opponent_source_row_count":per_experiment[ex]["missing_opponent_row"],
            "nonreciprocal_opponent_source_row_count":per_experiment[ex]["opponent_nonreciprocal"],
            "self_pointing_source_actor_rounds":per_experiment[ex]["self_pointing_source_actor_rounds"],
        })
    return {
        "research_id":"R103","phase":"B",
        "status":("R103_B_ORIGINAL_DYADIC_SOURCE_RECIPROCITY_ELIGIBLE" if criteria else
                  "R103_B_BOUNDED_ORIGINAL_DYADIC_RECIPROCITY_INELIGIBLE"),
        "official_original_full_SHA256":PINNED_SOURCE_SHA,
        "original_actor_round_rows":observed,
        "original_experiment_number_count":experiment_count,
        "original_unique_global_actor_code_count":len(user_experiments),
        "person_code_reuse_across_experiments_count":sum(len(xs)-1 for xs in user_experiments.values() if len(xs)>1),
        "original_session_person_identity_count":len(per_person_rounds),
        "actor_rounds_with_exact_reciprocal_opponent":reciprocal,
        "unique_source_reciprocal_pair_rounds":reciprocal//2,
        "source_actor_rounds_with_missing_opponent":missing,
        "source_actor_rounds_with_nonreciprocal_opponent":nonreciprocal,
        "source_actor_rounds_self_pointing_opponent":len(self_pointing_rows),
        "reciprocal_actor_round_fraction":reciprocal/observed,
        "source_experiments_with_reciprocal_pairs":eligible_experiments,
        "original_experiment_size_histogram":dict(sorted(Counter(map(len,experiment_users.values())).items())),
        "original_experiment_rounds_histogram":dict(sorted(Counter(map(len,experiment_rounds.values())).items())),
        "source_distinct_game_code_counts":dict(sorted(games.items())),
        "source_distinct_game_payoff_rule_count":len(payoff_rules),
        "source_original_experiment_anonymous_summaries":output,
        "eligible_for_prescoring_after_B":criteria,
        "actual_original_actions_or_opponent_actions_dereferenced":False,
        "original_raw_person_opponent_experiment_IDs_exported":False,
        "actual_human_model_scores":0,
        "PESEN_v0_1":"FROZEN",
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=pathlib.Path,required=True)
    args=p.parse_args()
    try:
        validate_url(URL)
        req=urllib.request.Request(URL,headers={"User-Agent":"Psychohistory-R103-B-Original-Only-Dyad-Source-Roster/1.0"})
        with urllib.request.build_opener(ExactOfficialRedirect()).open(req,timeout=55) as response:
            validate_url(response.geturl())
            b=response.read(CAP+1)
        result=identity_only(b)
    except (ValueError,TypeError,OSError,KeyError,UnicodeError,csv.Error) as exc:
        result={
            "research_id":"R103","phase":"B",
            "status":"R103_B_SOURCE_ROSTER_FAIL_CLOSED",
            "safe_failure":str(exc) if isinstance(exc,SourceError) else "R103_B_SOURCE_ORIGINAL_IDENTITY_UNVERIFIED",
            "actual_human_model_scores":0,"PESEN_v0_1":"FROZEN",
        }
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,sort_keys=True))
    if result["status"]!="R103_B_ORIGINAL_DYADIC_SOURCE_RECIPROCITY_ELIGIBLE":
        raise SystemExit(1)

if __name__=="__main__":
    main()
