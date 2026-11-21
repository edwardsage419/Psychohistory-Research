"""Opt-in local language model safety and deterministic engine boundaries."""
import json

import pytest

from psychohistory.decision_local_ai import (
    ALLOWED_MODELS, LocalDecisionAI, OllamaClient,
)
from psychohistory.decision_v05 import DecisionHubV05


def response(model_key, **overrides):
    record = {
        "model_key": model_key,
        "initial_analysis": "可先检查硬约束，数值仍待确认。",
        "reason": "本问题涉及用户确认的阈值。",
        "ask": "每项数据的来源可靠吗？",
        "candidate_options": [],
    }
    record.update(overrides)
    return json.dumps(record, ensure_ascii=False)


class FakeClient:
    def __init__(self, answer):
        self.answer = answer
        self.calls = []

    def chat(self, system, question):
        self.calls.append((system, question))
        return self.answer


def test_disabled_cannot_send_private_question_to_model():
    client = FakeClient(response("NONE"))
    bridge = LocalDecisionAI(client=client, enabled=False)
    assert bridge.propose("是否要搬家？")["status"] == "LOCAL_AI_DISABLED"
    assert client.calls == []


def test_registered_method_proposal_is_unconfirmed_and_does_not_compute():
    hub = DecisionHubV05()
    key = "c028_interval_feasibility@1.0.0"
    client = FakeClient(response(key))
    bridge = LocalDecisionAI(client=client, enabled=True, hub=hub)
    result = bridge.propose("我房租不能超过4000元，如何判断？")
    assert result["status"] == "NEEDS_CONFIRMATION"
    assert result["calculated"] is False
    assert result["proposal"]["model_key"] == key
    assert result["draft_state"]["confirmed"] is False
    assert "c028_interval_feasibility" in client.calls[0][0]


@pytest.mark.parametrize("bad", [
    response("invented_model@1.0.0"),
    response("NONE", candidate_options=["新增的房屋方案"]),
    response("NONE", initial_analysis="x" * 401),
    response("NONE") + " garbage",
    response("NONE").replace('"model_key": "NONE",', '"model_key": "NONE", "model_key": "NONE",'),
])
def test_invalid_model_or_untrusted_output_fails_closed(bad):
    bridge = LocalDecisionAI(client=FakeClient(bad), enabled=True)
    assert bridge.propose("我只有两个选择，想比较风险。 ")["status"] == "MODEL_OUTPUT_REJECTED"


def test_query_size_boundary_and_model_allowlist():
    client = FakeClient(response("NONE"))
    bridge = LocalDecisionAI(client=client, enabled=True)
    assert bridge.propose("问题" * 3001)["status"] == "INVALID_QUERY"
    assert client.calls == []
    with pytest.raises(ValueError):
        OllamaClient("remote-cloud-model")
    assert "psychohistory:v0" in ALLOWED_MODELS


def test_no_calculation_before_explicit_confirmation():
    bridge = LocalDecisionAI(client=FakeClient(response("NONE")), enabled=True)
    state = bridge.hub.start("我该怎么选？")["state"]
    key = "c028_interval_feasibility@1.0.0"
    assert bridge.analyze_confirmed(state, key, confirmed_by_user=False)["status"] == "USER_CONFIRMATION_REQUIRED"
    assert bridge.analyze_confirmed(state, key, confirmed_by_user=True)["status"] == "USER_CONFIRMATION_REQUIRED"
    state["confirmed"] = True
    state["constraints_confirmed"] = True
    assert bridge.analyze_confirmed(state, "invented@1.0.0", confirmed_by_user=True)["status"] == "INVALID_METHOD"


def test_confirmed_synthetic_input_uses_real_v05_feasibility_engine():
    key = "c028_interval_feasibility@1.0.0"
    state = {
        "decision_id": "a" * 32,
        "revision": 1,
        "question": "合成测试：方案甲租金4000元，方案乙4100元，底线4000元。",
        "confirmed": True,
        "constraints_confirmed": True,
        "deadline": "无固定期限",
        "objectives": [{"id": "rent", "label": "月租", "unit": "CNY", "direction": "min"}],
        "constraints": [{"id": "limit", "label": "预算上限", "unit": "CNY", "operator": "<=",
                         "threshold": "4000", "source": "仅供合成测试"}],
        "options": [
            {"id": "a", "label": "方案甲", "measurements": {"limit": {
                "lower": "4000", "upper": "4000", "unit": "CNY",
                "kind": "synthetic", "source": "仅供合成测试"}}},
            {"id": "b", "label": "方案乙", "measurements": {"limit": {
                "lower": "4100", "upper": "4100", "unit": "CNY",
                "kind": "synthetic", "source": "仅供合成测试"}}},
        ],
    }
    bridge = LocalDecisionAI(enabled=True, client=FakeClient(response(key)))
    result = bridge.analyze_confirmed(state, key, confirmed_by_user=True)
    assert result["calculated"] is True
    method = result["selected_method"]
    assert method["status"] == "EXECUTED"
    rows = method["result"]["feasibility"]
    assert [(row["option_id"], row["status"]) for row in rows] == [
        ("a", "ACCEPT"), ("b", "REJECT")
    ]
    assert result["source"] == "DecisionHubV05_deterministic"


def test_unknown_or_missing_information_does_not_claim_calculation():
    bridge = LocalDecisionAI(client=FakeClient(response("NONE")), enabled=True)
    result = bridge.propose("我最近没有方向，也没有可选行动。")
    assert result["status"] == "NEEDS_CONFIRMATION"
    assert result["candidate_method"] is None
    assert result["calculated"] is False
