from decimal import Decimal, InvalidOperation
from hashlib import sha256
from unicodedata import normalize
from collections import defaultdict
import operator

BOUNDS = {
    "cost_max": ("cost", "费用", "元", "<="),
    "income_min": ("income", "收入", "元/月", ">="),
    "hours_max": ("hours", "每周工时", "小时/周", "<="),
    "onsite_max": ("onsite", "每周到岗", "天/周", "<="),
    "move_allowed": ("move_required", "搬家要求", "逻辑值", "<="),
}
MEASURES = {
    "cost": ("费用", "元", "min", "yuan"),
    "income": ("收入", "元/月", "max", "yuan/month"),
    "hours": ("每周工时", "小时/周", "min", "hours/week"),
    "onsite": ("每周到岗", "天/周", "min", "days/week"),
    "move_required": ("搬家要求", "逻辑值", "min", ""),
}


def evidence_number(item):
    if item["field"] in {"move_allowed", "move_required"}:
        return {"yes": Decimal(1), "no": Decimal(0)}.get(item["value"])
    field = BOUNDS.get(item["field"], (item["field"],))[0]
    if item["field"] == "move_if_onsite_max":
        field = "onsite"
    expected = MEASURES.get(field)
    if not expected or item["unit"] != expected[-1]:
        return None
    try:
        number = Decimal(item["value"])
        if number.is_finite() and 0 <= number <= Decimal("100000000000") and number.as_tuple().exponent >= -8:
            return number
    except InvalidOperation:
        pass
    return None


def measure(item, unit, number):
    return {"lower": number, "upper": number, "unit": unit,
            "kind": "estimate" if item["kind"] == "estimate" else "fact", "source": item["source"]}


def sourced_key(item):
    return f"{item['field']}:{normalize('NFC', item['subject']).strip()}"


def build_state(base, options, claims, *, ready, overrides=None):
    """Only eligible ledger entries are supplied. Statements remain user-sourced."""
    present = [item for item in options if item["status"] == "CONFIRMED"]
    keys = {item["id"] for item in present}
    names = {normalize("NFC", item["label"]).strip(): item["id"] for item in present}
    active = {sourced_key(item): item for item in claims}
    initial = (overrides or base).model_dump(mode="python")
    initial.update(question=base.question, decision_id=base.decision_id, revision=base.revision,
                   understanding_receipt=base.understanding_receipt)
    raw_options = {item["id"]: item for item in initial["options"]}
    by_option = {
        opt["id"]: {"id": opt["id"], "label": opt["label"], "measurements": {}, "scores": {},
                    **raw_options.get(opt["id"], {})} for opt in present
    }
    for opt in present:
        by_option[opt["id"]]["label"] = opt["label"]
    constraints = {item["id"]: item for item in initial["constraints"]}
    objectives = {item["id"]: item for item in initial["objectives"]}
    # Conversation-defined keys are reserved from the advanced editor.
    constraints = {key: value for key, value in constraints.items() if not key.startswith("talk-")}
    objectives = {key: value for key, value in objectives.items() if not key.startswith("talk-")}
    for opt in by_option.values():
        for group in ("measurements", "scores"):
            opt[group] = {key: val for key, val in opt[group].items() if not key.startswith("talk-")}

    exception = active.get("move_if_onsite_max:")
    exception_limit = evidence_number(exception) if exception else None
    for field, (measurement, label, unit, operator) in BOUNDS.items():
        item = active.get(f"{field}:")
        if item is None or item["kind"] in {"estimate", "previous"}:
            continue
        number = evidence_number(item)
        if number is None or (field == "move_allowed" and number == 1):
            continue
        key = f"talk-{field}"
        cutoff_source = item["source"]
        if field == "move_allowed" and exception_limit is not None:
            label = "需要搬家且不符合到岗例外"
            cutoff_source = f"{cutoff_source}；{exception['source']}"
        if item["kind"] == "strict_constraint":
            operator = ">" if operator == ">=" else "<"
        constraints[key] = {"id": key, "label": label, "unit": unit, "operator": operator,
                            "threshold": number, "source": cutoff_source[:400]}
        for name, opt_id in names.items():
            value = active.get(f"{measurement}:{name}")
            measured = evidence_number(value) if value else None
            if measured is None or value["kind"] == "estimate":
                continue
            result = measure(value, unit, measured)
            if field == "move_allowed" and exception_limit is not None and measured == 1:
                attendance = active.get(f"onsite:{name}")
                attendance_number = evidence_number(attendance) if attendance else None
                if attendance_number is None or attendance["kind"] == "estimate":
                    continue
                result = measure(value, unit, Decimal(attendance_number > exception_limit))
                result["source"] = f"{value['source']}；{attendance['source']}；{exception['source']}"[:400]
            by_option[opt_id]["measurements"][key] = result

    for field, (label, unit, direction, _) in MEASURES.items():
        if field == "move_required":
            continue
        key = f"talk-{field}"
        for name, opt_id in names.items():
            item = active.get(f"{field}:{name}")
            number = evidence_number(item) if item else None
            if number is not None:
                objectives[key] = {"id": key, "label": label, "unit": unit, "direction": direction}
                by_option[opt_id]["scores"][key] = measure(item, unit, number)
    goal = active.get("goal:")
    if not objectives and ready:
        label = goal["value"] if goal else "比较目前可行的选择"
        objectives["talk-goal"] = {"id": "talk-goal", "label": label[:400], "unit": "待确认", "direction": "max"}

    deadline = active.get("deadline:")
    initial["deadline"] = deadline["value"][:400] if deadline else initial["deadline"] or ("仅比较当前条件" if ready else None)
    initial["intent"] = goal["value"][:400] if goal else initial["intent"]
    initial["options"] = list(by_option.values())
    initial["constraints"] = list(constraints.values())
    initial["objectives"] = list(objectives.values())
    initial["confirmed"] = ready
    initial["constraints_confirmed"] = ready
    for item in initial["scenarios"]:
        item["utilities"] = {key: v for key, v in item["utilities"].items() if key in keys}
    for field in ("weights", "shared_offsets"):
        initial[field] = {k: v for k, v in initial[field].items() if k in objectives}
    if initial["reference_option_id"] not in keys:
        initial["reference_option_id"] = None
    initial["intended_option_id"] = None
    initial["plan_note"] = None
    for opt in initial["options"]:
        opt["measurements"] = {k: v for k, v in opt["measurements"].items() if k in constraints}
        opt["scores"] = {k: v for k, v in opt["scores"].items() if k in objectives}
    evidence = [item for item in initial["evidence"] if not item["id"].startswith("talk-")][:12]
    for item in claims[-28:]:
        identifier = "talk-" + sha256(item["id"].encode()).hexdigest()[:22]
        kind = "estimate" if item["kind"] == "estimate" else "fact"
        label = f"{item['subject']} {item['value']} {item['unit']}".strip()[:400]
        evidence.append({"id": identifier, "label": label, "kind": kind, "source": item["source"][:400],
                         "verification": "user_confirmed", "scope": "用户确认原文。外部情况待核实。"})
    initial["evidence"] = evidence
    if initial["information"]:
        initial["information"]["verification_source"] = None
    return DecisionStateV05.model_validate(initial)


def public_claims(row):
    trace = row.ledger.trace()
    statuses = {key: group["status"] for group in trace["groups"] for key in group["active_claim_ids"]}
    previous = {i: group["active_claim_ids"] for group in trace["groups"] for i in group["provisional_claim_ids"]}
    claims = []
    for entry in trace["entries"]:
        claim_id = entry["claim_id"]
        record = entry["claim"].copy()
        record["evidence_kind"] = record["kind"]
        record["kind"] = record.pop("role") or record["kind"]
        state = "DISMISSED" if claim_id in row.dismissed else entry["status"]
        if state == "USER_CONFIRMED" and statuses.get(claim_id) in {"CONFLICT", "INCOMPARABLE", "UNKNOWN"}:
            state = statuses[claim_id]
        claims.append({"id": claim_id, **record, "status": state, "prior_ids": previous.get(claim_id, []),
                       "supersedes": entry["supersedes"], "recorded_at": entry["recorded_at"],
                       "confirmed_at": entry["confirmed_at"]})
    return claims


def active_claims(claims):
    return [item for item in claims if item["status"] in {"USER_CONFIRMED", "EXTERNALLY_VERIFIED"}
            and item["kind"] != "previous"
            and (item["kind"] != "conditional" or item["field"] == "move_if_onsite_max")]


class Projector:
    def _project(self, row):
        claims = public_claims(row)
        blocking = [c for c in claims if c["field"] in set(BOUNDS) | {"move_if_onsite_max"}
                    and c["kind"] not in {"previous", "estimate"}
                    and (c["kind"] != "conditional" or c["field"] == "move_if_onsite_max")
                    and c["status"] in {"PROVISIONAL", "CONFLICT", "INCOMPARABLE", "UNKNOWN"}]
        ready = row.context_confirmed and not row.coupled and not blocking and sum(
            opt["status"] == "CONFIRMED" for opt in row.options.values()) >= 2
        chosen = row.base.model_copy(update={"revision": row.saved_revision + 1})
        projected = build_state(chosen, row.options.values(), active_claims(claims), ready=ready,
                                overrides=row.overrides)
        if row.selected_plan:
            projected = projected.model_copy(update={"intended_option_id": row.selected_option_id,
                                                    "plan_note": row.selected_plan["trigger"]})
        return projected


GATE_ID = "c028_interval_feasibility"
OPERATORS = {">=": operator.ge, ">": operator.gt, "<=": operator.le, "<": operator.lt}


def check_constraint(constraint, value, deadline):
    if not constraint.source.strip():
        return "UNKNOWN", "请补充硬约束阈值的依据。"
    if value is None or value.kind == "unknown" or value.lower is None or value.upper is None:
        return "UNKNOWN", "请补充有依据的上下界。"
    if not value.source.strip():
        return "UNKNOWN", "请补充区间来源。"
    if value.unit.strip() != constraint.unit.strip():
        return "UNKNOWN", "区间单位与硬约束单位冲突。"
    if (value.horizon or deadline) != (constraint.horizon or deadline):
        return "UNKNOWN", "区间与硬约束的时间范围冲突。"
    meets = OPERATORS[constraint.operator]
    worst, best = (value.lower, value.upper) if constraint.operator.startswith(">") else (value.upper, value.lower)
    if meets(worst, constraint.threshold):
        return "CERTAIN_PASS", "整个闭区间满足阈值。"
    if not meets(best, constraint.threshold):
        return "CERTAIN_FAIL", "整个闭区间违反阈值。"
    return "POSSIBLE", "区间同时包含满足与违反阈值的值。"


def metric_key(constraint, deadline):
    return (constraint.label.strip(), constraint.unit.strip(), constraint.horizon or deadline)


def inconsistent_measurements(state, option):
    metrics = defaultdict(list)
    for constraint in state.constraints:
        value = option.measurements.get(constraint.id)
        status, _ = check_constraint(constraint, value, state.deadline)
        if status != "UNKNOWN":
            metrics[metric_key(constraint, state.deadline)].append(value)
    return {
        key for key, values in metrics.items()
        if max(value.lower for value in values) > min(value.upper for value in values)
    }


def evaluate(context):
    state = context.state
    feasibility = []
    for option in state.options:
        checks = []
        inconsistent = inconsistent_measurements(state, option)
        for constraint in state.constraints:
            value = option.measurements.get(constraint.id)
            status, reason = check_constraint(constraint, value, state.deadline)
            if metric_key(constraint, state.deadline) in inconsistent:
                status, reason = "UNKNOWN", "同指标、同单位及时间范围的区间互相冲突。"
            checks.append(dict(constraint_id=constraint.id, status=status, reason=reason))
        if any(check["status"] == "CERTAIN_FAIL" for check in checks):
            status = "REJECT"
        elif all(check["status"] == "CERTAIN_PASS" for check in checks):
            status = "ACCEPT"
        else:
            status = "UNRESOLVED"
        feasibility.append(dict(option_id=option.id, label=option.label, status=status, checks=checks))
    return {
        "summary": "依据用户确认的底线逐项筛查。只对 ACCEPT 方案执行后续比较。",
        "tables": [{"title": "硬约束筛查", "columns": ["方案", "判定"],
                    "rows": [[item["label"], item["status"]] for item in feasibility]}],
        "charts": [],
        "feasibility": feasibility,
    }


