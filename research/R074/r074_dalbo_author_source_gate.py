#!/usr/bin/env python3
"""R074 original Dal Bo-Frechette source eligibility audit; no model fitting.

All human IDs, action rows and histories remain transient in-memory.
The only public output is source hash and aggregate eligibility counts.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation
import hashlib
import json
from pathlib import Path

FIELDS = ("match", "round", "date", "r", "delta", "coop", "group", "id")
SOURCE_URL = "https://gfrechette.com/data/Dal_Bo_2011a_data.txt"
SOURCE_LIMIT = 3_000_000


def number(value, label, minimum=None):
    if not value.isdigit():
        raise ValueError("INVALID_INTEGER_" + label)
    n = int(value)
    if minimum is not None and n < minimum:
        raise ValueError("OUT_OF_RANGE_" + label)
    return n


def source_rows(blob):
    if not (0 < len(blob) <= SOURCE_LIMIT):
        raise ValueError("SOURCE_BYTE_BUDGET")
    try:
        text = blob.decode("utf-8-sig")
    except UnicodeError as exc:
        raise ValueError("SOURCE_UTF8_INVALID") from exc
    lines = text.splitlines()
    headers = [i for i, line in enumerate(lines)
               if tuple(line.split()) == FIELDS]
    if len(headers) != 1 or headers[0] > 50:
        raise ValueError("SOURCE_DICTIONARY_HEADER_AMBIGUOUS")
    rows = []
    for line in lines[headers[0]+1:]:
        if not line.strip():
            continue
        f = line.split()
        if len(f) != len(FIELDS):
            raise ValueError("SOURCE_ROW_WIDTH_INVALID")
        match, rnd, date, reward, delta, coop, group, person = f
        if not date or any(x not in "0123456789." for x in date) or date.count(".") > 1:
            raise ValueError("SOURCE_SESSION_DATE_MALFORMED")
        if date.startswith(".") or date.endswith("."):
            raise ValueError("SOURCE_SESSION_DATE_MALFORMED")
        try:
            if not Decimal(date).is_finite():
                raise ValueError("SOURCE_SESSION_DATE_INVALID")
            continuation = Decimal(delta)
        except InvalidOperation as exc:
            raise ValueError("SOURCE_TREATMENT_INVALID") from exc
        if continuation not in (Decimal("0.5"), Decimal("0.75")):
            raise ValueError("SOURCE_CONTINUATION_UNEXPECTED")
        reward_n = number(reward, "R")
        if reward_n not in (32, 40, 48):
            raise ValueError("SOURCE_REWARD_UNEXPECTED")
        if coop not in ("0","1"):
            raise ValueError("SOURCE_COOP_NOT_BINARY")
        rows.append((date, reward_n, str(continuation),
                     number(match, "MATCH", 1),
                     number(rnd, "ROUND", 1), number(group, "GROUP", 1),
                     number(person, "ID", 1), int(coop)))
    if not rows:
        raise ValueError("NO_HUMAN_ROWS")
    return rows


def audit(blob):
    rows = source_rows(blob)
    seen_rows = set()
    pairs = defaultdict(list)
    persons = defaultdict(set)
    series = defaultdict(dict)
    treatment_by_session = {}
    for date, reward, delta, match, rnd, group, person, coop in rows:
        treatment = (reward, delta)
        prev = treatment_by_session.setdefault(date, treatment)
        if prev != treatment:
            raise ValueError("SESSION_MULTIPLE_TREATMENTS")
        rowkey = (date, match, rnd, person)
        if rowkey in seen_rows:
            raise ValueError("DUPLICATE_SESSION_MATCH_ROUND_PERSON")
        seen_rows.add(rowkey)
        persons[date].add(person)
        pairs[(date, match, rnd, group)].append((person, coop))
        history = series[(date, match, person)]
        history[rnd] = (group, coop)
    partner_lookup = {}
    for key, actual in pairs.items():
        if len(actual) != 2 or actual[0][0] == actual[1][0]:
            raise ValueError("MATCH_ROUND_NOT_EXACTLY_TWO_UNIQUE_HUMANS")
        date, match, rnd, group = key
        (p1,a1),(p2,a2) = actual
        partner_lookup[(date, match, rnd, p1)] = (p2, a2)
        partner_lookup[(date, match, rnd, p2)] = (p1, a1)
    rounds_three_or_later = Counter()
    human_session_series = Counter()
    period_length = []
    for (date, match, person), history in series.items():
        periods = set(history)
        if periods != set(range(1, len(periods)+1)):
            raise ValueError("NONCONTIGUOUS_PERSON_MATCH")
        group_set = {x[0] for x in history.values()}
        if len(group_set) != 1:
            raise ValueError("PAIR_GROUP_SWITCHED_WITHIN_MATCH")
        counterpart = set()
        for rd,(_,_) in history.items():
            opposite = partner_lookup.get((date,match,rd,person))
            if opposite is None:
                raise ValueError("OPPONENT_MISSING")
            counterpart.add(opposite[0])
        if len(counterpart) != 1:
            raise ValueError("OPPONENT_SWITCHED_WITHIN_MATCH")
        period_length.append(len(history))
        reward,delta = treatment_by_session[date]
        rounds_three_or_later[(reward,delta)] += max(0, len(history)-2)
        human_session_series[date] += 1
    grouped = defaultdict(set)
    rows_treatment = Counter()
    for date, reward, delta, *_ in rows:
        grouped[(reward,delta)].add(date)
        rows_treatment[(reward,delta)] += 1
    # The source's "id" is explicitly defined only within a session.
    # Do not assert cross-session real-world identities are known.
    summaries = []
    for treatment in sorted(grouped):
        sessions = len(grouped[treatment])
        scored = rounds_three_or_later[treatment]
        summaries.append({
            "reward":treatment[0],"continuation":treatment[1],
            "session_count":sessions,
            "human_action_rows":rows_treatment[treatment],
            "candidate_t3_plus_actions":scored,
            "other_same_treatment_session_trainable": sessions >= 2,
        })
    return {
        "research_id":"R074",
        "stage":"ORIGINAL_AUTHOR_SOURCE_STRUCTURE_GATE_NO_MODEL_SCORING",
        "source_url":SOURCE_URL,
        "source_sha256":hashlib.sha256(blob).hexdigest(),
        "source_bytes":len(blob),
        "source_rows":len(rows),
        "distinct_sessions":len(persons),
        "session_person_slots":sum(map(len,persons.values())),
        "human_match_series":len(series),
        "paired_match_rounds":len(pairs),
        "candidate_t3_plus_actions":sum(rounds_three_or_later.values()),
        "max_round":max(period_length),
        "min_round":min(period_length),
        "treatments":summaries,
        "source_session_field":"date; author dictionary: session date and decimal distinguishes same-day sessions",
        "cross_session_real_world_identity":"NOT_IDENTIFIED_FROM_WITHIN_SESSION_ID",
        "scoring_models_executed":False,
        "privacy":"NO_HUMAN_ROWS_OR_SESSION_IDS_IN_OUTPUT",
        "R073_E3":"OPEN_PENDING_FURTHER_SOURCE_AND_SPLIT_VALIDATION",
        "PESEN_v0.1":"FROZEN",
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--source", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    try:
        result = audit(args.source.read_bytes())
        if any(not x["other_same_treatment_session_trainable"] for x in result["treatments"]):
            result["status"] = "INSUFFICIENT_SAME_TREATMENT_SESSIONS"
            result["R073_E3"] = "BLOCKED"
        else:
            result["status"] = "ORIGINAL_SOURCE_STRUCTURE_PASS_MODEL_SCORING_NOT_RUN"
    except (OSError, UnicodeError, ValueError) as exc:
        result = {"research_id":"R074","status":"SOURCE_GATE_FAIL_CLOSED",
                  "reason": str(exc)[:95] if isinstance(exc,ValueError) else "SOURCE_IO",
                  "scoring_models_executed":False,"PESEN_v0.1":"FROZEN"}
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,sort_keys=True))
    if result["status"] != "ORIGINAL_SOURCE_STRUCTURE_PASS_MODEL_SCORING_NOT_RUN":
        raise RuntimeError("R074 source gate did not pass")


if __name__=="__main__":
    main()
