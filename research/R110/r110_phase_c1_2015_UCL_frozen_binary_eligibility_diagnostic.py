#!/usr/bin/env python3
"""R110 C1 source-only anonymous exclusion audit, frozen 2026-10-19.

No forecasts, model scoring, raw tokens, or raw actor identifiers are exported.
The failed C0 prescore gate remains immutable.
"""
from __future__ import annotations

import argparse
import collections
import csv
import io
import json
import pathlib

import r110_phase_a1_2015_PLOS_S1_verified_google_storage_original_doubleSHA_header_only as a
import r110_phase_b1_2015_PLOS_UCL_original_subject_game_round_NONBEHAVIOR_roster as b
import r110_phase_c0_2015_UCL_120actor_peer_lag_vs_equal_shrink_variance_sham_brier as c0

SUCCESS="C1_DIAGNOSTIC_COMPLETE_C0_GATE_STILL_FAIL"
DISCREPANCY="C1_IMPLEMENTATION_DISCREPANCY"
FAILURE="C1_E0_SOURCE_BLOCKED"
SHAPE_FIELDS=(0,1,2,3,8,9,15,16)

REASONS=(
    "first_round_each_actor_game",
    "no_exact_previous_actor_game_period",
    "invalid_or_missing_current_binary_action",
    "invalid_or_missing_previous_own_binary_action",
    "invalid_or_missing_author_previous_peer_signal",
    "prior_partner_optout_or_unknown",
    "source_actor_game_condition_changed",
    "external_prior_same_condition_pool_below_two",
    "sham_donor_source_stratum_under_two",
)
TOKEN_CLASSES=("accepted_zero","accepted_one","blank","other_numeric","other_nonempty")
BEHAVIOR_COLS={
    "own_current_cooperated":15,
    "author_prior_partner_signal":8,
    "prior_partner_optout_flag":16,
}

def token_class(value):
    """Labels only; the original token is never returned or printed."""
    if c0.binary(value)==0:
        return "accepted_zero"
    if c0.binary(value)==1:
        return "accepted_one"
    if not value.strip():
        return "blank"
    try:
        float(value)
    except (ValueError, OverflowError):
        return "other_nonempty"
    return "other_numeric"

def format_counts(counter, names):
    return {name:int(counter.get(name,0)) for name in names}

def diagnose(raw, *, enforce_real=True):
    # B1 authenticates the full file, the 120x2x50 roster and the pinned SHA.
    roster=b.audited_source_actor_game_round_roster(raw)
    if enforce_real and not roster["exact_paper_reported_120_people_two_games_50_each_source_structure"]:
        raise a.SourceError("R110_C1_ORIGINAL_ID_GAME_ROUND_ROSTER_INVALID")
    if roster["original_whole_source_SHA256"]!=b.PINNED_SHA:
        raise a.SourceError("R110_C1_ORIGINAL_WHOLE_SOURCE_SHA_MISMATCH")
    try:
        reader=csv.reader(io.StringIO(raw.decode("utf-8-sig"),newline=""),strict=True)
        header=next(reader,None)
        if tuple(header or ())!=c0.HEAD:
            raise a.SourceError("R110_C1_PINNED_ORIGINAL_PUBLIC_FIELD_HEADERS_CHANGED")
        obs={}
        values_by_prev=collections.defaultdict(dict)
        field_counts={name:collections.Counter() for name in BEHAVIOR_COLS}
        game_set=set()
        for row in reader:
            if len(row)!=len(c0.HEAD):
                raise a.SourceError("R110_C1_ORIGINAL_CSV_ROW_WIDTH_INVALID")
            # Only eight whitelisted columns below, no demographic, punitive or payoff reads.
            t=int(row[0]); sid=row[1];game=row[9]; condition=(game,row[2],row[3])
            y=c0.binary(row[15]);peer=c0.binary(row[8]); opt=c0.binary(row[16])
            for name,idx in BEHAVIOR_COLS.items():
                field_counts[name][token_class(row[idx])]+=1
            key=(sid,game,t)
            if key in obs:
                raise a.SourceError("R110_C1_DUPLICATE_PERSON_GAME_ROUND")
            obs[key]=(sid,game,condition,t,y,peer,opt)
            values_by_prev[(condition,t)][sid]=y
            game_set.add(game)
    except (UnicodeError,csv.Error,ValueError,TypeError) as exc:
        if isinstance(exc,a.SourceError):
            raise
        raise a.SourceError("R110_C1_ORIGINAL_SAFE_CSV_PARSE_FAILED") from None

    if len(obs)!=12000 or len(game_set)!=2:
        raise a.SourceError("R110_C1_REAL_ORIGINAL_12000_TWO_GAME_UNIVERSE_INVALID")
    missing=collections.Counter()
    per_game=collections.defaultdict(lambda:{"total":0,"eligible":0})
    candidate=[]
    for sid,game,t in sorted(obs):
        item=obs[(sid,game,t)]
        sid,game,condition,t,y,peer,opt=item
        per_game[game]["total"]+=1
        reason=None
        if t==1:
            reason=REASONS[0]
        else:
            previous=obs.get((sid,game,t-1))
            if previous is None:
                reason=REASONS[1]
            elif y is None:
                reason=REASONS[2]
            elif previous[4] is None:
                reason=REASONS[3]
            elif peer is None:
                reason=REASONS[4]
            elif opt!=0:
                reason=REASONS[5]
            elif condition!=previous[2]:
                reason=REASONS[6]
            else:
                pool=[v for other,v in values_by_prev[(condition,t-1)].items()
                      if other!=sid and v is not None]
                if len(pool)<2:
                    reason=REASONS[7]
        if reason:
            missing[reason]+=1
        else:
            candidate.append((sid,game,condition,t))
    strata=collections.defaultdict(list)
    for sid,game,condition,t in candidate:
        strata[(condition,t)].append((sid,game))
    eligible_actors=set()
    eligible_games=set()
    qualified=0
    for group in strata.values():
        if len(group)<2:
            missing[REASONS[8]]+=len(group)
        else:
            for sid,game in group:
                qualified+=1
                eligible_actors.add(sid)
                eligible_games.add(game)
                per_game[game]["eligible"]+=1

    if sum(missing.values())+qualified!=len(obs):
        raise a.SourceError("R110_C1_EXCLUSIVE_EXCLUSION_ACCOUNTING_NOT_CLOSED")
    if sum(x["total"] for x in per_game.values())!=len(obs) or sum(x["eligible"] for x in per_game.values())!=qualified:
        raise a.SourceError("R110_C1_GAME_DENOMINATOR_ACCOUNTING_NOT_CLOSED")
    game_out=[]
    for game in sorted(per_game):
        group=per_game[game]
        game_out.append({"anonymous_game_category_slot":len(game_out)+1,
                         "source_rows":group["total"],
                         "eligible_targets":group["eligible"],
                         "excluded_rows":group["total"]-group["eligible"]})
    # Never score or call the C0 evaluator: C0 failed before a score could be released.
    c0_gate_pass=(qualified>=c0.MIN_TARGETS and len(eligible_actors)>=c0.MIN_ACTORS
                  and len(eligible_games)>=2)
    return {
        "research_id":"R110", "phase":"C1",
        "status":DISCREPANCY if c0_gate_pass else SUCCESS,
        "original_source_SHA256":roster["original_whole_source_SHA256"],
        "original_source_rows":len(obs),
        "anonymized_original_game_categories":len(game_set),
        "total_valid_C0_identical_targets":qualified,
        "source_actors_with_valid_targets":len(eligible_actors),
        "game_categories_with_valid_targets":len(eligible_games),
        "frozen_C0_evidence_gate_pass_in_C1_diagnostic":c0_gate_pass,
        "C0_original_failure_unchanged":"R110_C0_PRE_FROZEN_REAL_800_TARGET_40_ACTOR_2_GAME_GATE_FAIL",
        "mutually_exclusive_reasons":format_counts(missing,REASONS),
        "behavior_field_anonymous_token_class_counts":{
            name:format_counts(field_counts[name],TOKEN_CLASSES) for name in BEHAVIOR_COLS
        },
        "game_level_anonymous_denominators":game_out,
        "denominator_closed":True,
        "raw_tokens_actor_identifiers_and_person_actions_exported":False,
        "new_human_prediction_scores":0,
        "R073_frozen":True,
        "PESEN_v0_1":"FROZEN",
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",type=pathlib.Path,required=True)
    args=ap.parse_args()
    try:
        outcome=diagnose(a.actual_official_source())
    except (OSError,ValueError,TypeError,csv.Error,UnicodeError) as exc:
        # Full errors from parsing/HTTP must not echo source tokens or addresses.
        message=str(exc) if isinstance(exc,a.SourceError) else "R110_C1_REAL_SOURCE_FAILED_SAFELY"
        outcome={"research_id":"R110","phase":"C1","status":FAILURE,
                 "safe_failure":message,"new_human_prediction_scores":0,
                 "PESEN_v0_1":"FROZEN"}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(outcome,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(outcome,sort_keys=True))
    if outcome["status"]!=SUCCESS:
        raise SystemExit(1)

if __name__=="__main__":
    main()
