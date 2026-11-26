import pytest

from psychohistory.decision_conversation import active_claims, public_claims
from psychohistory.decision_evidence import EvidenceLedger, confirm_claim, draft_claims
from psychohistory.decision_v05 import DecisionHubV05, DecisionStateV05


def claims_for_costs(first, second):
    return [
        {"field": "cost_max", "subject": "", "value": "3000", "unit": "yuan",
         "source": "预算最多3000元", "kind": "constraint"},
        *({"field": "cost", "subject": name, "value": str(value), "unit": "yuan",
           "source": f"{name}：费用{value}元", "kind": "measurement"}
          for name, value in zip(("A", "B"), (first, second), strict=True)),
    ]


def base_state(text):
    return DecisionStateV05.model_validate(DecisionHubV05().start(text)["state"])


@pytest.mark.parametrize("reverse", [False, True])
def test_native_measurement_survives_agreeing_estimate(reverse):
    from psychohistory.decision_conversation import Conversation
    from psychohistory.decision_conversation_math import build_state

    source = "成本最多3000元。A：费用2000元。B：费用4000元。"
    base = base_state(source)
    candidates = claims_for_costs(2000, 4000)
    actual = next(item for item in candidates if item["field"] == "cost" and item["subject"] == "A")
    estimate = {**actual, "kind": "estimate", "source": "A：估计费用2000元"}
    items = [*candidates, estimate]
    if reverse:
        items.reverse()
    ledger = draft_claims(EvidenceLedger(), [
        {**item, "role": item["kind"], "kind": "estimate" if item["kind"] == "estimate" else "fact"}
        for item in items
    ])
    for entry in ledger.entries:
        ledger = confirm_claim(ledger, entry.claim_id)
    row = Conversation(session_id="worktest", base=base, domain="general", ledger=ledger)
    options = [{"id": name, "label": name, "status": "CONFIRMED"} for name in ("A", "B")]
    state = build_state(base, options, active_claims(public_claims(row)), ready=True)
    result = DecisionHubV05().analyze(state)
    assert [(item["option_id"], item["status"]) for item in result["feasibility"]] == [
        ("A", "ACCEPT"), ("B", "REJECT"),
    ]


def test_descriptive_analysis_keeps_c028_violation_separate_from_decision():
    from psychohistory.decision_conversation_math import build_state, descriptive_analysis

    source = "预算最多3000元。A：费用4000元。B：费用2000元。"
    base = base_state(source)
    options = [{"id": name, "label": name, "status": "CONFIRMED"} for name in ("A", "B")]
    claims = [{**item, "id": str(i)} for i, item in enumerate(claims_for_costs(4000, 2000))]
    state = build_state(base, options, claims, ready=False)
    assert not state.confirmed
    assert descriptive_analysis(state, context_confirmed=False) is None
    result = descriptive_analysis(state, context_confirmed=True)
    assert result["authority"] == "NONE"
    assert result["status"] == "DESCRIPTIVE_ONLY"
    assert "feasibility" not in result and "recommendation" not in result
    assert [(item["option_id"], item["constraint_id"], item["status"]) for item in result["checks"]] == [
        ("A", "talk-cost_max", "CONDITIONAL_VIOLATION"),
    ]
    assert result["checks"][0]["threshold"] == "3000"
    assert result["checks"][0]["lower"] == "4000"
    [difference] = result["differences"]
    assert (difference["higher_option_id"], difference["lower_option_id"], difference["amount"]) == (
        "A", "B", "2000",
    )
    assert difference["unit"] == "元"
