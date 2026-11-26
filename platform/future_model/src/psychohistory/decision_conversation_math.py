"""Translate confirmed conversational facts to the existing v0.5 math contract."""
from decimal import Decimal, InvalidOperation
from hashlib import sha256
from unicodedata import normalize

from .decision_feasibility import GATE_ID, METHOD as FEASIBILITY_METHOD, check_constraint, inconsistent_measurements, metric_key
from .decision_language import interpret
from .decision_semantics import comparison, monetary_scope
from .decision_v05 import DecisionStateV05

BOUNDS = {
    "cost_max": ("cost", "费用", "元", "<="),
    "cost_min": ("cost", "费用", "元", ">="),
    "income_min": ("income", "收入", "元/月", ">="),
    "income_max": ("income", "收入", "元/月", "<="),
    "hours_max": ("hours", "每周工时", "小时/周", "<="),
    "hours_min": ("hours", "每周工时", "小时/周", ">="),
    "onsite_max": ("onsite", "每周到岗", "天/周", "<="),
    "onsite_min": ("onsite", "每周到岗", "天/周", ">="),
    "move_allowed": ("move_required", "搬家要求", "逻辑值", "<="),
    "rent_parking_max": ("rent_parking", "房租和停车费合计", "元/月", "<="),
    "night_shift_max": ("night_shift_required", "当前实际排班含夜班", "是否包含", "<="),
}
MEASURES = {
    "cost": ("费用", "元", "min", "yuan"),
    "income": ("收入", "元/月", "max", "yuan/month"),
    "hours": ("每周工时", "小时/周", "min", "hours/week"),
    "onsite": ("每周到岗", "天/周", "min", "days/week"),
    "move_required": ("搬家要求", "逻辑值", "min", ""),
}
TYPED = {"rent_monthly": "yuan/month", "parking_monthly": "yuan/month", "rent_parking": "yuan/month",
         "night_shift_required": "presence"}
JOINT_FORMULA_VERSION = "cny-monthly-rent-parking/1"
NIGHT_HORIZON = "当前实际排班"
JOINT_HORIZON = "每月"


def evidence_number(item):
    if item["field"] in {"move_allowed", "move_required"}:
        return {"yes": Decimal(1), "no": Decimal(0)}.get(item["value"])
    field = BOUNDS.get(item["field"], (item["field"],))[0]
    if item["field"] == "move_if_onsite_max":
        field = "onsite"
    expected = TYPED.get(field) or MEASURES.get(field, (None,))[-1]
    if expected is None or item["unit"] != expected:
        return None
    if field in {"rent_monthly", "parking_monthly", "rent_parking", "income", "cost"} and monetary_scope(
        item["source"], monthly=field in {"rent_monthly", "parking_monthly", "rent_parking"}
    ):
        return None
    if field == "night_shift_required" and item["field"] == field:
        return {"yes": Decimal(1), "no": Decimal(0)}.get(item["value"])
    try:
        number = Decimal(item["value"])
        if number.is_finite() and 0 <= number <= Decimal("100000000000") and number.as_tuple().exponent >= -8:
            return number
    except InvalidOperation:
        pass
    return None


def _is_estimate(item):
    return item["kind"] == "estimate" or item.get("evidence_kind") == "estimate"


def measure(item, unit, number):
    return {"lower": number, "upper": number, "unit": unit,
            "kind": "estimate" if _is_estimate(item) else "fact", "source": item["source"]}


def sourced_key(item):
    return f"{item['field']}:{normalize('NFC', item['subject']).strip()}"


def _current_evidence(item, name):
    if not item or _is_estimate(item) or item["kind"] in {"conditional", "previous"}:
        return None
    number = evidence_number(item)
    if number is None:
        return None
    keys = ("field", "subject", "value", "unit", "source")
    for candidate in interpret(item["source"], known_options=[name])["claims"]:
        if all(item[key] == candidate[key] for key in keys) and candidate["kind"] in {"measurement", "revision"}:
            return number
    return None


def _joint_measurement(active, name, unit):
    rent = active.get(f"rent_monthly:{name}")
    parking = active.get(f"parking_monthly:{name}")
    rent_value = _current_evidence(rent, name)
    parking_value = _current_evidence(parking, name)
    if rent_value is None or parking_value is None:
        return None
    total = rent_value + parking_value
    source = f"{JOINT_FORMULA_VERSION} 房租 + 停车费；{rent['source']}；{parking['source']}"
    # The gate's source has a fixed length. Do not truncate a dependency.
    if len(source) > 400:
        return None
    return {"lower": total, "upper": total, "unit": unit, "kind": "fact",
            "source": source, "horizon": JOINT_HORIZON}


def _scope(item):
    metadata = item.get("metadata") or {}
    return (item["unit"], *(metadata.get(field) or "" for field in ("observed_at", "population", "scope")))


def _active_evidence(claims):
    active = {}
    for item in claims:
        key = sourced_key(item)
        prior = active.get(key)
        if prior and item["field"] in BOUNDS and _operator(prior) in {"<", ">"}:
            continue
        if (prior and _is_estimate(item) and not _is_estimate(prior)
                and prior["kind"] in {"fact", "measurement", "revision"}
                and _scope(prior) == _scope(item)
                and evidence_number(prior) is not None
                and evidence_number(prior) == evidence_number(item)):
            # Both entries survived the trusted ledger's scope and conflict validation.
            continue
        active[key] = item
    return active


def _operator(item):
    default = BOUNDS[item["field"]][-1]
    explicit = comparison(item["source"])
    if explicit in {"<", ">", "<=", ">="} and explicit[0] == default[0]:
        return explicit
    return default[0] if item["kind"] == "strict_constraint" else default


def build_state(base, options, claims, *, ready, overrides=None):
    """Only eligible ledger entries are supplied. Statements remain user-sourced."""
    present = [item for item in options if item["status"] == "CONFIRMED"]
    keys = {item["id"] for item in present}
    names = {normalize("NFC", item["label"]).strip(): item["id"] for item in present}
    active = _active_evidence(claims)
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
        if item is None or _is_estimate(item) or item["kind"] == "previous":
            continue
        number = evidence_number(item)
        if number is None or (field == "move_allowed" and number == 1):
            continue
        key = f"talk-{field}"
        cutoff_source = item["source"]
        if field == "move_allowed" and exception_limit is not None:
            label = "需要搬家且不符合到岗例外"
            cutoff_source = f"{cutoff_source}；{exception['source']}"
        operator = _operator(item)
        constraints[key] = {"id": key, "label": label, "unit": unit, "operator": operator,
                            "threshold": number, "source": cutoff_source[:400]}
        if field == "rent_parking_max":
            constraints[key]["horizon"] = JOINT_HORIZON
        elif field == "night_shift_max":
            constraints[key]["horizon"] = NIGHT_HORIZON
        for name, opt_id in names.items():
            if field == "rent_parking_max":
                if result := _joint_measurement(active, name, unit):
                    by_option[opt_id]["measurements"][key] = result
                continue
            value = active.get(f"{measurement}:{name}")
            measured = _current_evidence(value, name) if field == "night_shift_max" else (
                evidence_number(value) if value else None
            )
            if measured is None or _is_estimate(value):
                continue
            result = measure(value, unit, measured)
            if field == "night_shift_max":
                result["horizon"] = NIGHT_HORIZON
            if field == "move_allowed" and exception_limit is not None and measured == 1:
                attendance = active.get(f"onsite:{name}")
                attendance_number = evidence_number(attendance) if attendance else None
                if attendance_number is None or _is_estimate(attendance):
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
        kind = "estimate" if _is_estimate(item) else "fact"
        label = f"{item['subject']} {item['value']} {item['unit']}".strip()[:400]
        evidence.append({"id": identifier, "label": label, "kind": kind, "source": item["source"][:400],
                         "verification": "user_confirmed", "scope": "用户确认原文。外部情况待核实。"})
    initial["evidence"] = evidence
    if initial["information"]:
        initial["information"]["verification_source"] = None
    return DecisionStateV05.model_validate(initial)


def descriptive_analysis(state, *, context_confirmed: bool):
    """Publish isolated grounded calculations without feasibility or decision authority."""
    if not context_confirmed:
        return None

    checks = []
    for option in state.options:
        inconsistent = inconsistent_measurements(state, option)
        for constraint in state.constraints:
            measurement = option.measurements.get(constraint.id)
            if (not constraint.id.startswith("talk-") or measurement is None or measurement.kind != "fact"
                    or metric_key(constraint, state.deadline) in inconsistent):
                continue
            status, _ = check_constraint(constraint, measurement, state.deadline)
            if status != "CERTAIN_FAIL":
                continue
            checks.append({
                "option_id": option.id, "option_label": option.label, "constraint_id": constraint.id,
                "constraint_label": constraint.label, "status": "CONDITIONAL_VIOLATION",
                "method": GATE_ID, "method_version": FEASIBILITY_METHOD.version,
                "unit": constraint.unit, "horizon": constraint.horizon or state.deadline,
                "operator": constraint.operator, "threshold": format(constraint.threshold, "f"),
                "lower": format(measurement.lower, "f"), "upper": format(measurement.upper, "f"),
                "dependencies": [constraint.source, measurement.source],
            })

    differences = []
    if len(state.options) == 2:
        left, right = state.options
        for objective in state.objectives:
            if not objective.id.startswith("talk-"):
                continue
            a, b = left.scores.get(objective.id), right.scores.get(objective.id)
            if (not a or not b or a.lower is None or b.lower is None or a.lower != a.upper
                    or b.lower != b.upper or a.lower == b.lower or not a.source.strip() or not b.source.strip()
                    or a.unit != objective.unit or b.unit != objective.unit
                    or (a.horizon or state.deadline) != (b.horizon or state.deadline)
                    or a.kind != "fact" or b.kind != "fact"):
                continue
            high, low = (left, right) if a.lower > b.lower else (right, left)
            differences.append({
                "objective_id": objective.id, "label": objective.label,
                "higher_option_id": high.id, "higher_option_label": high.label,
                "lower_option_id": low.id, "lower_option_label": low.label,
                "amount": format(abs(a.lower - b.lower), "f"),
                "unit": objective.unit, "horizon": a.horizon or state.deadline,
                "dependencies": [a.source, b.source],
            })

    if not checks and not differences:
        return None
    return {"version": "1.0.0", "authority": "NONE", "status": "DESCRIPTIVE_ONLY",
            "checks": checks, "differences": differences}
