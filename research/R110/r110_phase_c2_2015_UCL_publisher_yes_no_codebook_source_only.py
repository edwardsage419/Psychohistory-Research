#!/usr/bin/env python3
"""R110 C2: publisher yes/no vocabulary check, no scoring or behavior export."""
from __future__ import annotations
import argparse, collections, csv, io, json, pathlib
import r110_phase_a1_2015_PLOS_S1_verified_google_storage_original_doubleSHA_header_only as a
import r110_phase_b1_2015_PLOS_UCL_original_subject_game_round_NONBEHAVIOR_roster as b
import r110_phase_c0_2015_UCL_120actor_peer_lag_vs_equal_shrink_variance_sham_brier as c0

PASS="C2_SCHEMA_MATCHED_AUTHOR_WORDS_BOUNDED"
UNKNOWN="C2_UNMAPPED_SOURCE_TEXT_REQUIRES_CODEBOOK"
BLOCKED="C2_E0_ORIGINAL_SOURCE_BLOCKED"
CATEGORIES=("yes","no","blank","other_nonempty")

def class_word(s):
    x=s.strip(" \t\r\n\f\v").lower()
    if x=="yes":return "yes"
    if x=="no":return "no"
    if not x:return "blank"
    return "other_nonempty"

def summarize(raw):
    roster=b.audited_source_actor_game_round_roster(raw)
    if not roster["exact_paper_reported_120_people_two_games_50_each_source_structure"]:
        raise a.SourceError("R110_C2_ORIGINAL_ROSTER_MISMATCH")
    # B1 pins and audits full file SHA before C2 touches any behavior.
    counts={"own_cooperation":collections.Counter(),
            "author_prior_partner_cooperation":collections.Counter()}
    game_counts=collections.defaultdict(lambda:{"own":collections.Counter(),"peer":collections.Counter(),"rows":0})
    opt=collections.Counter()
    try:
        reader=csv.reader(io.StringIO(raw.decode("utf-8-sig"),newline=""),strict=True)
        if tuple(next(reader,None) or ())!=c0.HEAD:
            raise a.SourceError("R110_C2_PUBLISHED_18_HEADERS_DIFFER")
        n=0
        for row in reader:
            if len(row)!=18:
                raise a.SourceError("R110_C2_SOURCE_WIDTH_INVALID")
            # Strict allowed row value positions: 0,1,2,3,8,9,15,16.
            # B1 already independently audited nonbehavior (0,1,2,3,9).
            game=row[9]
            own=class_word(row[15])
            peer=class_word(row[8])
            counts["own_cooperation"][own]+=1
            counts["author_prior_partner_cooperation"][peer]+=1
            game_counts[game]["own"][own]+=1
            game_counts[game]["peer"][peer]+=1
            game_counts[game]["rows"]+=1
            mark=c0.binary(row[16])
            opt["accepted_zero" if mark==0 else "accepted_one" if mark==1 else "unmapped"]+=1
            n+=1
    except (csv.Error,UnicodeError) as ex:
        raise a.SourceError("R110_C2_SOURCE_CSV_PARSE_DENIED") from None
    if n!=12000 or len(game_counts)!=2:
        raise a.SourceError("R110_C2_ORIGINAL_SOURCE_SIZE_OR_GAME_COUNT_INVALID")
    for key in counts:
        if sum(counts[key].values())!=n:
            raise a.SourceError("R110_C2_ANONYMOUS_COLUMN_DENOMINATOR_INVALID")
    mapped=all(counts[key]["blank"]==0 and counts[key]["other_nonempty"]==0
               for key in counts)
    by_game=[]
    for game in sorted(game_counts):
        x=game_counts[game]
        by_game.append({"anonymous_game_category_slot":len(by_game)+1,
                        "source_rows":x["rows"],
                        "own_word_counts":{k:x["own"][k] for k in CATEGORIES},
                        "peer_word_counts":{k:x["peer"][k] for k in CATEGORIES}})
    return {
        "research_id":"R110","phase":"C2",
        "status":PASS if mapped else UNKNOWN,
        "source_SHA256":roster["original_whole_source_SHA256"],
        "publisher_paper_S1_prior_partner_yes_no_explicit":True,
        "source_own_cooperation_yes_no_dictionary_is_tested_hypothesis":True,
        "original_records":n,
        "original_two_game_anonymous_counts":by_game,
        "behavior_anonymous_dictionary_counts":{
            key:{cat:counts[key][cat] for cat in CATEGORIES} for key in counts
        },
        "original_prior_partner_optout_C0_numeric_classes":{
            key:opt[key] for key in ("accepted_zero","accepted_one","unmapped")
        },
        "every_cooperation_cell_matches_pre_frozen_yes_no":mapped,
        "previous_C0_gate_still_failed":True,
        "real_human_model_score_count":0,
        "raw_tokens_person_IDs_and_actions_exported":False,
        "R073_frozen":True,
        "PESEN_v0_1":"FROZEN",
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=pathlib.Path,required=True)
    args=p.parse_args()
    try:
        result=summarize(a.actual_official_source())
    except (OSError,ValueError,TypeError,UnicodeError,csv.Error) as ex:
        result={"research_id":"R110","phase":"C2","status":BLOCKED,
                "safe_failure":str(ex) if isinstance(ex,a.SourceError) else "R110_C2_REAL_SOURCE_UNVERIFIED",
                "real_human_model_score_count":0,"PESEN_v0_1":"FROZEN"}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,sort_keys=True))
    if result["status"]!=PASS:
        raise SystemExit(1)
if __name__=="__main__":
    main()
