#!/usr/bin/env python3
"""R110 B1: only NONBEHAVIOR subject, game, round and player/partner types.

All actor IDs and condition tokens are transient and never published.
No original cooperation, punishment, opt-out or demographic cells accessed.
"""
from __future__ import annotations
import argparse,collections,csv,io,json,pathlib,re
import r110_phase_a1_2015_PLOS_S1_verified_google_storage_original_doubleSHA_header_only as a
import r110_phase_b0_2015_PLOS_original_12000_CSV_row_width_and_18_public_headers_only as b

PINNED_SHA="ea70b0f3d98075f9d3e4401becfcdec8f6bdb5cae00c4dad63a697f9b61d7b5f"
ORIGINAL_ROWS=12000
FIELDS=("Subject ID","Round","Game type","Player type","Partner type")
ID_RE=re.compile(r"[A-Za-z0-9_.-]{1,40}",flags=re.ASCII)
TYPE_RE=re.compile(r"[A-Za-z0-9_ .()/-]{1,80}",flags=re.ASCII)
ROUND_RE=re.compile(r"[0-9]{1,4}",flags=re.ASCII)

def audited_source_actor_game_round_roster(raw):
    base=b.original_public_source_headers_and_widths(raw)
    if (base["original_source_SHA256"]!=PINNED_SHA or
        base["original_logical_CSV_data_rows"]!=ORIGINAL_ROWS or
        not base["all_source_rows_12000x18_structurally"]):
        raise a.SourceError("R110_B1_AUTHENTIC_ORIGINAL_SOURCE_12000x18_NOT_PINNED")
    head=base["author_original_public_field_names_only"]
    if not all(field in head for field in FIELDS):
        raise a.SourceError("R110_B1_REQUIRED_NONBEHAVIOR_SOURCE_FIELDS_NOT_PRESENT")
    idx={name:head.index(name) for name in FIELDS}
    persons=collections.Counter()
    games_by_person=collections.defaultdict(set)
    events=collections.defaultdict(list)
    type_universe={"Game type":set(),"Player type":set(),"Partner type":set()}
    types_by_actor_game=collections.defaultdict(set)
    all_rounds=set()
    processed=0
    try:
        r=csv.reader(io.StringIO(raw.decode("utf-8-sig"),newline=""),strict=True)
        next(r)
        for row in r:
            if len(row)!=18:
                raise a.SourceError("R110_B1_TRUE_ORIGINAL_SOURCE_ROW_WIDTH_CHANGED")
            # WHITELIST: Only exactly five frozen NONBEHAVIOR body fields.
            sid=row[idx["Subject ID"]]
            raw_round=row[idx["Round"]]
            game=row[idx["Game type"]]
            focal_type=row[idx["Player type"]]
            partner_type=row[idx["Partner type"]]
            if not ID_RE.fullmatch(sid):
                raise a.SourceError("R110_B1_SOURCE_PSEUDONYMOUS_SUBJECT_ID_INVALID")
            if any(TYPE_RE.fullmatch(v) is None for v in (game,focal_type,partner_type)):
                raise a.SourceError("R110_B1_ORIGINAL_NONBEHAVIOR_CONDITION_CODE_INVALID")
            if not ROUND_RE.fullmatch(raw_round):
                raise a.SourceError("R110_B1_ORIGINAL_NONBEHAVIOR_ROUND_CODE_INVALID")
            t=int(raw_round)
            if not 1<=t<=1000:
                raise a.SourceError("R110_B1_SOURCE_ROUND_NOT_1_TO_1000")
            processed+=1
            persons[sid]+=1
            games_by_person[sid].add(game)
            events[(sid,game)].append(t)
            types_by_actor_game[(sid,game)].add((focal_type,partner_type))
            for key,value in (("Game type",game),("Player type",focal_type),("Partner type",partner_type)):
                type_universe[key].add(value)
            all_rounds.add(t)
    except (UnicodeError,csv.Error,StopIteration) as e:
        raise a.SourceError("R110_B1_ORIGINAL_PLOS_ROSTER_NONBEHAVIOR_PARSE_INVALID") from e
    if processed!=ORIGINAL_ROWS:
        raise a.SourceError("R110_B1_SOURCE_PSEUDONYMOUS_ACTOR_ROW_UNIVERSE_NOT_12000")
    all_actor_game_sizes=collections.Counter(len(v) for v in events.values())
    all_actor_sizes=collections.Counter(persons.values())
    actor_game_50_exact=sum(len(v)==50 and set(v)==set(range(1,51)) for v in events.values())
    duplicated=sum(len(v)-len(set(v)) for v in events.values())
    games_per_actor=collections.Counter(len(s) for s in games_by_person.values())
    stable_types=sum(len(v)==1 for v in types_by_actor_game.values())
    exact_possible=(len(persons)==120 and len(events)==240
                    and all_actor_game_sizes=={50:240} and
                    actor_game_50_exact==240 and duplicated==0
                    and games_per_actor=={2:120})
    return {
        "research_id":"R110","phase":"B1",
        "status":"R110_B1_REAL_2015_UCL_SOURCE_NONBEHAVIOR_ACTOR_GAME_ROUND_ROSTER_E1",
        "source_publisher_DOI":"10.1371/journal.pone.0117183.s001",
        "original_whole_source_SHA256":PINNED_SHA,
        "original_human_candidate_rows_from_true_original":processed,
        "source_distinct_pseudonymous_Subject_ID_codes":len(persons),
        "source_anonymous_rows_per_subject_histogram":dict(sorted((str(k),v) for k,v in all_actor_sizes.items())),
        "source_anonymous_game_type_count_per_subject_histogram":dict(sorted((str(k),v) for k,v in games_per_actor.items())),
        "source_distinct_Subject_ID_by_Game_type_groups":len(events),
        "source_anonymous_rows_per_subject_game_histogram":dict(sorted((str(k),v) for k,v in all_actor_game_sizes.items())),
        "source_actor_game_groups_exactly_50_ordinal_rounds_1_to_50":actor_game_50_exact,
        "source_duplicate_subject_game_round_keys":duplicated,
        "source_round_min":min(all_rounds),
        "source_round_max":max(all_rounds),
        "source_round_distinct_count":len(all_rounds),
        "source_anonymous_distinct_game_type_code_count":len(type_universe["Game type"]),
        "source_anonymous_distinct_player_type_code_count":len(type_universe["Player type"]),
        "source_anonymous_distinct_partner_type_code_count":len(type_universe["Partner type"]),
        "source_actor_game_groups_player_and_partner_type_stable":stable_types,
        "exact_paper_reported_120_people_two_games_50_each_source_structure":exact_possible,
        "original_true_lab_session_key_present_in_published_CSV":False,
        "original_actual_counterpart_Subject_ID_key_present_in_published_CSV":False,
        "original_subject_ID_or_nonbehavior_condition_values_transiently_read":True,
        "original_cooperation_punishment_optout_demographic_or_partner_coop_prev_cells_read":False,
        "original_private_actor_ID_game_tokens_or_raw_action_values_exported":False,
        "real_human_next_action_model_scores":0,
        "PESEN_v0_1":"FROZEN",
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=pathlib.Path,required=True)
    args=p.parse_args()
    try:r=audited_source_actor_game_round_roster(a.actual_official_source())
    except (OSError,ValueError,TypeError,UnicodeError,csv.Error) as e:
        r={"research_id":"R110","phase":"B1",
           "status":"R110_B1_REAL_SOURCE_NONBEHAVIOR_IDENTITY_FAIL_CLOSED",
           "safe_failure":str(e) if isinstance(e,a.SourceError) else "R110_B1_REAL_SOURCE_ACTOR_GAME_ROUND_UNVERIFIED",
           "real_human_next_action_model_scores":0,"PESEN_v0_1":"FROZEN"}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(r,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(r,sort_keys=True))
    if r["status"]!="R110_B1_REAL_2015_UCL_SOURCE_NONBEHAVIOR_ACTOR_GAME_ROUND_ROSTER_E1":
        raise SystemExit(1)
if __name__=="__main__":main()
