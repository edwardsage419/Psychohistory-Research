"""Replay fixed public B11 examples through the authenticated conversation API."""
import argparse
import asyncio
from contextlib import suppress
from collections import Counter
from decimal import Decimal, InvalidOperation
import hashlib
import json
import os
import platform
from pathlib import Path
import re
import resource
from tempfile import TemporaryDirectory
from time import perf_counter

ROOT = Path(__file__).resolve().parents[3]
HUB = ROOT / "research/decision_hub"
CORPORA = (
    ("2026-11-24-language-evidence-corpus/language_corpus.json",
     "be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb"),
    ("2026-11-24-semantic-proposal-contract/corpus.json",
     "05c239f3f3b1f46235fa2464d2945c21c6c08132"),
)
HARD = {"HARD", "CONDITIONAL_HARD", "HARD_CONSEQUENCE", "constraint"}
UNKNOWN = {"UNKNOWN", "unknown", "UNAVAILABLE_EVIDENCE"}
UNCERTAIN = {"ESTIMATE", "estimate", "REPORTED_ESTIMATE", "REPORTED_POSSIBILITY",
             "REPORTED_PROMISE", "REPORTED_UNCERTAIN", "REPORTED_EXTERNAL",
             "REPORTED_UNVERIFIED", "HYPOTHESIS", "COUNTERFACTUAL_CLAIM",
             "RETROSPECTIVE_ESTIMATE"}
PERMISSION = {"AUTHORIZATION_PROPOSAL", "RECORD_INTENT", "permission_intent"}
UNIT_ALIASES = {
    "yuan": "CNY", "元": "CNY", "人民币": "CNY", "yuan/month": "CNY/month",
    "天": "day", "days": "day", "工作日": "workday", "分钟": "minute",
    "min": "minute", "小时": "hour", "次": "count",
}
PERIOD_ALIASES = {"每月": "month", "月": "month", "每年": "year", "年": "year",
                  "每周": "week", "周": "week"}
CONFIRMED = {"USER_CONFIRMED", "EXTERNALLY_VERIFIED", "CONFIRMED", "VERIFIED"}
DECISIVE = {"ACCEPT", "REJECT"}
ARABIC = re.compile(r"(?<![\w.])[+-]?[0-9]+(?:\.[0-9]+)?(?![0-9.])")


def load_corpus(path, blob):
    data = (HUB / path).read_bytes()
    if hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest() != blob:
        raise ValueError(f"Public input identity changed: {path}")
    return json.loads(data)["cases"]


def amount(value):
    if isinstance(value, bool) or value is None:
        return None
    try:
        result = Decimal(str(value))
    except InvalidOperation:
        return None
    return result if result.is_finite() else None


def unit(item):
    raw = item.get("unit")
    normalized = UNIT_ALIASES.get(raw, raw)
    period = item.get("period")
    normalized_period = PERIOD_ALIASES.get(period, period)
    if normalized and isinstance(normalized_period, str) and "/" not in normalized:
        normalized += f"/{normalized_period}"
    return normalized


def span(item, text):
    explicit = item.get("span")
    raw = item.get("source")
    if not isinstance(raw, str) or not raw:
        return None
    if isinstance(explicit, dict):
        start, end = explicit.get("start"), explicit.get("end")
        if not isinstance(start, int) or not isinstance(end, int) or not 0 <= start < end <= len(text):
            return None
        return (start, end) if text[start:end] == raw else None
    start = text.find(raw)
    if start < 0 or text.find(raw, start + 1) >= 0:
        return None
    return start, start + len(raw)


def overlaps(left, right):
    return left is not None and right is not None and max(left[0], right[0]) < min(left[1], right[1])


def contains(outer, inner):
    return outer is not None and inner is not None and outer[0] <= inner[0] <= inner[1] <= outer[1]


def gold_claims(turn):
    if "claims" in turn:
        return [{**claim, "source": claim["span"]} for claim in turn["claims"]]
    return [{**claim, "source": claim["quote"], "kind": claim["role"]}
            for claim in turn["proposal"]["claims"]]


def compact(item):
    return {key: item[key] for key in (
        "kind", "field", "value", "unit", "period", "operator", "subject", "condition",
        "status", "reason", "source", "span", "reading", "ratio", "authority", "hard",
        "evidence_kind", "supersedes", "prior_ids",
    ) if key in item}


def semantically_hard(item):
    return item.get("hard") is True or item.get("kind") in {"constraint", "strict_constraint"}


def coverage_row(gold, text, claims, obligations, explicit_unknowns, lexical):
    target = span(gold, text)
    if target is None:
        raise ValueError(f"Ambiguous frozen annotation {gold['source']!r}")
    claim_matches = [item for item in claims if contains(span(item, text), target)]
    # UNKNOWN obligations often cover a larger clause. Overlap is measured separately from exact spans.
    obligation_matches = [item for item in obligations if overlaps(span(item, text), target)]
    unknowns = [item for item in explicit_unknowns if overlaps(span(item, text), target)]
    numeric = {}
    for key in ("value", "lo", "hi"):
        wanted = gold.get(key)
        if not isinstance(wanted, (int, float)) or isinstance(wanted, bool):
            continue
        lex = [item for item in lexical if contains(target, span(item, text))]
        matching_lexical = [item for item in lex if amount(wanted) in
                            {amount(item.get("value")), amount(item.get("ratio"))}]
        matching_ledger = [
            item for item in claim_matches
            if item.get("field") == gold.get("field") and amount(item.get("value")) == amount(wanted)
        ] if gold.get("field") else []
        numeric[key] = {
            "expected": wanted,
            "ascii_baseline": any(Decimal(match[0]) == amount(wanted) for match in ARABIC.finditer(gold["source"])),
            "lexical_values": [compact(item) for item in lex],
            "lexical_value_match": bool(matching_lexical),
            "lexical_typed_match": (any(unit(item) == gold["unit"] for item in matching_lexical)
                                    if gold.get("unit") else None),
            "native_field_value_match": bool(matching_ledger),
            "native_typed_match": (any(unit(item) == gold["unit"] for item in matching_ledger)
                                   if gold.get("unit") else None),
        }
    hard_anchors = [item for item in (*claim_matches, *obligation_matches) if semantically_hard(item)]
    conditional = gold.get("condition")
    comparison = gold.get("op") if gold.get("op") in {"<", "<=", "==", ">=", ">"} else None
    edit = gold.get("operation", gold.get("op"))
    # Narrow, source-bearing dimension checks. Missing annotations and unsupported fields stay visible.
    return {
        "source": gold["source"], "class": gold["kind"], "field": gold.get("field"),
        "actor": gold.get("actor"), "condition": conditional, "comparison": comparison,
        "revision_operation": edit if edit in {"replace", "retract"} else None,
        "annotation_unit": gold.get("unit"), "matched_claim_count": len(claim_matches),
        "matched_obligation_count": len(obligation_matches), "matched_unknown_count": len(unknowns),
        "matched_hard_count": len(hard_anchors),
        "specific_unknown_retained": bool(unknowns or any(
            item.get("kind") == "unknown" or item.get("status") == "UNKNOWN" for item in claim_matches
        )),
        "condition_retained": (any(item.get("condition") == conditional for item in
                                   (*claim_matches, *obligation_matches)) if conditional else None),
        "comparison_retained": (any(item.get("operator") == comparison for item in
                                    (*claim_matches, *obligation_matches)) if comparison else None),
        "other_subject_retained": (any(item.get("subject") for item in (*claim_matches, *obligation_matches))
                                   if gold.get("actor") == "other" else None),
        "revision_link_present": (any(item.get("supersedes") or item.get("prior_ids") for item in claim_matches)
                                  if edit in {"replace", "retract"} else None),
        "false_certainty": (any(item.get("status") in CONFIRMED and item.get("evidence_kind") == "fact"
                                for item in claim_matches) if gold["kind"] in UNKNOWN | UNCERTAIN else None),
        "provisional_fact_label_on_uncertainty": (
            any(item.get("evidence_kind") == "fact" and item.get("status") == "PROVISIONAL"
                for item in claim_matches) if gold["kind"] in UNKNOWN | UNCERTAIN else None
        ),
        "numeric": numeric,
    }


class Replay:
    def __init__(self, client, prefix):
        self.client = client
        self.prefix = prefix
        self.samples = []
        self.calls = Counter()

    async def request(self, op, body):
        start = perf_counter()
        self.calls[op] += 1
        response = await self.client.post(f"{self.prefix}/{op}", json=body)
        if op in {"start", "turn"}:
            self.samples.append((perf_counter() - start) * 1000)
        if response.status_code != 200:
            raise RuntimeError(f"{op} HTTP {response.status_code}: {response.text}")
        return response.json()


def bind(view):
    return {"session_id": view["session_id"], "revision": view["revision"]}


async def evaluate_case(api, episode):
    view = None
    seen_claims = set()
    seen_options = set()
    rows = []
    for index, turn in enumerate(episode["turns"], start=1):
        text = turn["text"]
        if view is None:
            view = await api.request("start", {"question": text, "use_local_model": False})
        else:
            view = await api.request("turn", {**bind(view), "text": text, "use_local_model": False})
        fresh_claims = [item for item in view["claims"] if item["id"] not in seen_claims]
        fresh_options = [item for item in view["options"] if item["id"] not in seen_options]
        seen_claims.update(item["id"] for item in view["claims"])
        seen_options.update(item["id"] for item in view["options"])
        semantics = view.get("semantic", {}).get("turns", [])
        semantic = semantics[-1] if semantics else {}
        obligations = semantic.get("obligations", [])
        unknowns = semantic.get("unknowns", [])
        quantities = [item for item in semantic.get("candidates", []) if item.get("kind") == "quantity"]
        comparison = [coverage_row(gold, text, fresh_claims, obligations, unknowns, quantities)
                      for gold in gold_claims(turn)]
        analysis = view.get("analysis") or {}
        knowledge = view.get("knowledge") or {}
        search = knowledge.get("search", {})
        gating = [item["status"] for item in analysis.get("feasibility", [])]
        question = view.get("summary", {}).get("question") or ""
        rows.append({
            "id": f"{episode['id']}.{index}", "domain": episode["domain"], "text": text,
            "reference_response": turn.get("expected"), "reference_prohibitions": turn.get("forbid", []),
            "phase": view["phase"], "question": question, "question_marks": question.count("？") + question.count("?"),
            "analysis_published": bool(analysis), "gate_statuses": gating,
            "methods_executed": [item.get("model_id")
                                 for item in analysis.get("methods", []) if item.get("status") == "EXECUTED"],
            "new_claims": [compact(item) for item in fresh_claims],
            "new_options": [item["label"] for item in fresh_options],
            "ungrounded_claims": [item["source"] for item in fresh_claims if span(item, text) is None],
            "invalid_semantic_spans": [item.get("source") for item in
                                       (*quantities, *obligations, *unknowns) if span(item, text) is None],
            "unauthorized_dialogue": bool(view.get("selected_option_id") or view.get("selected_plan")
                                          or view.get("state", {}).get("confirmed")),
            "semantic_version": semantic.get("version"),
            "knowledge_status": search.get("status"),
            "knowledge_hit_count": len(search.get("hits", [])),
            "knowledge_authority": knowledge.get("authority"),
            "annotations": comparison,
        })
    await api.request("end", {"session_id": view["session_id"]})
    return rows


def stats(rows):
    all_claims = [item for row in rows for item in row["annotations"]]
    nums = [num for item in all_claims for num in item["numeric"].values()]
    hard = [item for item in all_claims if item["class"] in HARD]
    explicit_unknowns = [item for item in all_claims if item["class"] in UNKNOWN]
    return {
        "episodes": len({row["id"].split(".")[0] for row in rows}),
        "turns": len(rows), "annotations": len(all_claims),
        "turns_with_new_ledger_claims": sum(bool(row["new_claims"]) for row in rows),
        "turns_with_unconfirmed_analysis": sum(row["analysis_published"] for row in rows),
        "turns_without_confirmation_or_selection": sum(not row["unauthorized_dialogue"] for row in rows),
        "new_ledger_candidates": sum(len(row["new_claims"]) for row in rows),
        "invalid_semantic_spans": sum(len(row["invalid_semantic_spans"]) for row in rows),
        "ungrounded_or_ambiguous_ledger_anchors": sum(len(row["ungrounded_claims"]) for row in rows),
        "annotation_ledger_anchor_coverage": sum(item["matched_claim_count"] > 0 for item in all_claims),
        "annotation_obligation_overlap": sum(item["matched_obligation_count"] > 0 for item in all_claims),
        "hard_annotations": len(hard),
        "hard_anchor_coverage": sum(item["matched_hard_count"] > 0 for item in hard),
        "explicit_unknown_annotations": len(explicit_unknowns),
        "specific_unknown_annotations": sum(item["specific_unknown_retained"] for item in explicit_unknowns),
        "false_confirmed_certainty_matches": sum(item["false_certainty"] is True for item in all_claims),
        "provisional_fact_labels_on_uncertainty": sum(
            item["provisional_fact_label_on_uncertainty"] is True for item in all_claims
        ),
        "turns_with_unprompted_gate": sum(bool(DECISIVE.intersection(row["gate_statuses"])) for row in rows),
        "turns_with_local_knowledge_hits": sum(bool(row["knowledge_hit_count"]) for row in rows),
        "knowledge_status_counts": dict(Counter(row["knowledge_status"] or "ABSENT" for row in rows)),
        "turns_with_retrieval_authority": sum(row["knowledge_authority"] not in {None, "NONE"} for row in rows),
        "question_mark_counts": dict(sorted(Counter(row["question_marks"] for row in rows).items())),
        "numeric_obligations": len(nums),
        "ascii_baseline_value_matches": sum(num["ascii_baseline"] for num in nums),
        "lexical_value_matches": sum(num["lexical_value_match"] for num in nums),
        "numerics_with_annotated_units": sum(num["lexical_typed_match"] is not None for num in nums),
        "lexical_value_and_unit_matches": sum(num["lexical_typed_match"] is True for num in nums),
        "native_field_value_matches": sum(num["native_field_value_match"] for num in nums),
        "native_field_value_and_unit_matches": sum(num["native_typed_match"] is True for num in nums),
        **{
            f"{key}_outcomes": dict(Counter(
                "retained" if item[key] else "missing"
                for item in all_claims if item[key] is not None
            )) for key in ("condition_retained", "comparison_retained", "other_subject_retained",
                           "revision_link_present")
        },
    }



OPTION_QUESTION = "我该选「方案甲」，还是「方案乙」？"
ONSITE_1_4 = "方案甲每周到岗1天，方案乙每周到岗4天。"
TRIALS = (
    {
        "id": "onsite-hard-calculation", "text": OPTION_QUESTION + ONSITE_1_4 + "我每周最多到岗2天。",
        "oracle": "1 ≤ 2 and 4 > 2 days/week",
        "expected": {"方案甲": "ACCEPT", "方案乙": "REJECT"},
    },
    {
        "id": "onsite-comparison-calculation", "text": OPTION_QUESTION + ONSITE_1_4 + "我每周最多到岗4天。",
        "oracle": "Both pass 4 days/week; 1 < 4 on the shared minimize objective",
        "expected": {"方案甲": "ACCEPT", "方案乙": "ACCEPT"}, "frontier": ["方案甲"],
    },
    {
        "id": "L01-explicit-joint-budget",
        "text": (OPTION_QUESTION + "房租加停车每月最多4000元。方案甲房租每月3600元，"
                 "方案甲停车每月400元。方案乙房租每月3600元，方案乙停车每月450元。"),
        "oracle": "3600 + 400 = 4000 ≤ 4000; 3600 + 450 = 4050 > 4000 CNY/month.",
        "expected": {"方案甲": "ACCEPT", "方案乙": "REJECT"},
        "projected_measurement": "talk-rent_parking_max",
        "reference_values": {"方案甲": 4000, "方案乙": 4050},
    },
    {
        "id": "R55-currency-mismatch",
        "text": OPTION_QUESTION + "方案甲费用2000美元，方案乙费用3500元。我的预算最多3000元。",
        "oracle": "No exchange rate; 2000 USD cannot be compared to 3000 CNY. 3500 > 3000 CNY.",
        "unknown": ["方案甲"], "optional_reject": ["方案乙"], "source_anchor": "2000美元",
    },
    {
        "id": "R55-period-mismatch",
        "text": OPTION_QUESTION + "方案甲每天费用200元，方案乙每月费用3500元。我每月预算最多3000元。",
        "oracle": "No billable day count; 200 CNY/day cannot be compared to 3000 CNY/month.",
        "unknown": ["方案甲"], "optional_reject": ["方案乙"], "source_anchor": "每天费用200元",
    },
    {
        "id": "R56-negated-direction",
        "text": OPTION_QUESTION + "方案甲每周工时20小时，方案乙每周工时40小时。我每周工时不能少于30小时。",
        "oracle": "Cannot be less than means ≥; 20 < 30 and 40 ≥ 30 hours/week.",
        "expected": {"方案甲": "REJECT", "方案乙": "ACCEPT"}, "source_anchor": "不能少于30小时",
    },
    {
        "id": "R57-third-party-limit",
        "text": OPTION_QUESTION + ONSITE_1_4 + "我每周最多到岗4天。我朋友的预算最多3000元。",
        "oracle": "The friend's financial bound is not the speaker's constraint; both pass the speaker's bound.",
        "expected": {"方案甲": "ACCEPT", "方案乙": "ACCEPT"}, "source_anchor": "我朋友的预算最多3000元",
    },
    {
        "id": "L02-night-shifts-missing-evidence",
        "text": OPTION_QUESTION + ONSITE_1_4 + "我每周最多到岗2天。只要夜班我就不去。",
        "oracle": "No shift evidence; 甲 cannot pass all bottom lines. 乙 independently violates the onsite bound.",
        "unknown": ["方案甲"], "optional_reject": ["方案乙"], "source_anchor": "只要夜班我就不去",
    },
    {
        "id": "S02-walking-distance-unknown",
        "text": OPTION_QUESTION + ONSITE_1_4 + "我每周最多到岗4天。任何一套都必须离车站步行十五分钟以内。",
        "oracle": "No option has door-to-station walking time, so neither can pass this hard constraint.",
        "unknown": ["方案甲", "方案乙"], "source_anchor": "必须离车站步行十五分钟以内",
    },
)


async def evaluate_pressure(api, trial):
    before = await api.request("start", {"question": trial["text"], "use_local_model": False})
    selections = [item["id"] for item in before["options"] if item["label"] in {"方案甲", "方案乙"}]
    if len(selections) != 2:
        raise ValueError(f"Focused pressure trial lacks both genuine options: {trial['id']}")
    confirmed = await api.request("confirm", {
        **bind(before), "claim_ids": [item["id"] for item in before["claims"]
                                    if item["status"] == "PROVISIONAL"],
        "option_ids": selections, "accept_context": True,
    })
    analysis = confirmed.get("analysis") or {}
    gate = {item["label"]: item["status"] for item in analysis.get("feasibility", [])}
    methods = {item["model_id"]: item["result"] for item in analysis.get("methods", [])
               if item["status"] == "EXECUTED"}
    label = {item["id"]: item["label"] for item in confirmed["options"]}
    frontier = [
        label.get(key, key) for item in methods.values() for key in item.get("frontier", [])
    ]
    outcomes = {}
    for name, expected in trial.get("expected", {}).items():
        actual = gate.get(name, "UNRESOLVED")
        if actual != expected:
            outcomes[name] = "FALSE_ACCEPT" if actual == "ACCEPT" else (
                "FALSE_REJECT" if actual == "REJECT" else "UNRESOLVED_SUPPORTED_REFERENCE"
            )
        else:
            outcomes[name] = "CORRECT"
    for name in trial.get("unknown", []):
        actual = gate.get(name, "UNRESOLVED")
        outcomes[name] = f"FALSE_{actual}" if actual in DECISIVE else "CORRECT_UNKNOWN"
    for name in trial.get("optional_reject", []):
        outcomes[name] = ("FALSE_ACCEPT" if gate.get(name) == "ACCEPT" else
                          "CORRECT_REJECT" if gate.get(name) == "REJECT" else "CONSERVATIVE_UNKNOWN")
    if "frontier" in trial:
        outcomes["frontier"] = "CORRECT" if frontier == trial["frontier"] else "FRONTIER_MISMATCH"
    measurements = {}
    if "projected_measurement" in trial:
        for option in confirmed["state"]["options"]:
            metric = option["measurements"].get(trial["projected_measurement"])
            if metric:
                measurements[option["label"]] = {key: metric.get(key) for key in ("lower", "upper", "unit", "source")}
    absolute_errors = {}
    for name, expected in trial.get("reference_values", {}).items():
        measured = measurements.get(name)
        if not measured:
            absolute_errors[name] = None
            continue
        errors = [abs(amount(measured[bound]) - amount(expected)) for bound in ("lower", "upper")]
        absolute_errors[name] = str(max(errors))
        if max(errors) != 0:
            outcomes[f"{name}_numeric"] = "NUMERIC_MISMATCH"
    await api.request("end", {"session_id": confirmed["session_id"]})
    return {
        **trial, "gate": gate, "outcomes": outcomes, "frontier_labels": frontier,
        "max_absolute_errors": absolute_errors,
        "analysis_published": bool(analysis), "executed_methods": list(methods), "measurements": measurements,
        "initial_summary": before.get("summary"), "confirmed_summary": confirmed.get("summary"),
        "gates": [{k: item[k] for k in ("label", "status", "checks") if k in item}
                  for item in analysis.get("feasibility", [])],
        "confirmation_claims": [compact(item) for item in confirmed["claims"]],
        "remaining_blockers": [compact(item) for item in
                              confirmed.get("semantic", {}).get("blocking_obligations", [])],
        "source_anchor_present": (any(trial["source_anchor"] in item.get("source", "")
                                       for item in [*confirmed["claims"], *confirmed.get("semantic", {})
                                                    .get("blocking_obligations", [])])
                                 if "source_anchor" in trial else None),
    }


def count_exact_old_action_proxy(interpret, cases):
    out = Counter()
    hard_fields = {"cost_max", "income_min", "onsite_max", "hours_max", "move_allowed", "move_if_onsite_max"}
    for episode in cases:
        for turn in episode["turns"]:
            gold = Counter(item["quote"] for item in turn["proposal"]["claims"]
                           if (item["role"], item["op"], item["actor"], item["modality"], item["time"])
                           == ("action", "add", "self", "proposed", "future"))
            limits = [item["quote"] for item in turn["proposal"]["claims"] if item["role"] == "constraint"]
            reading = interpret(turn["text"])
            choices = Counter(reading["options"])
            out.update(turns=1, actionTP=sum((gold & choices).values()), actionFP=sum((choices - gold).values()),
                       actionFN=sum((gold - choices).values()), actionExact=gold == choices,
                       goldConstraints=len(limits), candidateClaims=len(reading["claims"]),
                       emptyClaims=not reading["claims"], emptyBoth=not reading["claims"] and not choices,
                       anyClaimAnchor=sum(any(quote in item["source"] for item in reading["claims"])
                                          for quote in limits),
                       hardFieldAnchor=sum(any(quote in item["source"] and item["field"] in hard_fields
                                               for item in reading["claims"]) for quote in limits))
    return dict(out)


async def periodic_wake():
    # The managed offline sandbox rejects socket writes used to wake asyncio across threads.
    # A timer dispatches the normal HTTP middleware and handlers with no network access.
    while True:
        await asyncio.sleep(0.001)


async def run_api(prefix, corpora):
    from httpx import ASGITransport, AsyncClient
    from psychohistory.api import create_app

    token = "private-public-development-replay"
    with TemporaryDirectory(prefix="psychohistory-v07-public-") as temp:
        app = create_app(Path(temp), ROOT, token=token)
        # The decision routes do not depend on the separate research experiment worker.
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost",
                               headers={"Authorization": f"Bearer {token}"}) as client:
            wake = asyncio.create_task(periodic_wake())
            try:
                api = Replay(client, prefix)
                rows = [
                    row for corpus in corpora for episode in corpus
                    for row in await evaluate_case(api, episode)
                ]
                samples = list(api.samples)
                pressure = [await evaluate_pressure(api, trial) for trial in TRIALS]
                knowledge = None
                if any(row["knowledge_status"] for row in rows):
                    response = await client.get(f"{prefix}/knowledge/report")
                    response.raise_for_status()
                    knowledge = {key: response.json()[key] for key in ("status", "counts", "authority")}
            finally:
                wake.cancel()
                with suppress(asyncio.CancelledError):
                    await wake
    return rows, samples, pressure, api.calls, knowledge


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prefix", default="/api/v7/decisions")
    parser.add_argument("--label", required=True)
    parser.add_argument("--output", type=Path, required=True)
    options = parser.parse_args()
    os.environ["PSYCHOHISTORY_LOCAL_AI"] = "0"
    import psychohistory
    from psychohistory.decision_language import interpret

    corpora = [load_corpus(path, blob) for path, blob in CORPORA]
    rows, samples, pressure, calls, knowledge = asyncio.run(run_api(options.prefix, corpora))
    summary = stats(rows)
    if (summary["episodes"], summary["turns"], summary["annotations"], summary["numeric_obligations"]) != (
        32, 64, 167, 28
    ):
        raise ValueError("Frozen public development denominators changed")
    latencies = sorted(samples)
    result = {
        "corpora": dict(CORPORA), "arm": options.label, "api": options.prefix,
        "sample_type": "PUBLIC_SYNTHETIC_DEVELOPMENT_ONLY",
        "environment": {
            "python": platform.python_version(), "system": platform.system(),
            "machine": platform.machine(), "http_transport": "IN_PROCESS_ASGI",
            "loaded_source_sha256": {
                path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                for path in sorted(Path(psychohistory.__file__).parent.glob("decision*.py"))
            },
        },
        "summary": summary, "legacy_cold_action_proxy": count_exact_old_action_proxy(interpret, corpora[1]),
        "resource_measurements": {
            "raw_request_median_ms": round((latencies[31] + latencies[32]) / 2, 3),
            "raw_request_max_ms": round(latencies[-1], 3),
            "max_process_rss_linux_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        },
        "confirmation_pressure": pressure,
        "confirmation_outcomes": dict(sorted(Counter(outcome for trial in pressure
                                                      for outcome in trial["outcomes"].values()).items())),
        "production_index": knowledge, "api_requests": dict(calls), "turns": rows,
    }
    options.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(json.dumps(result["confirmation_outcomes"], ensure_ascii=False))


if __name__ == "__main__":
    main()
