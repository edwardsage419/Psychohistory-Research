from datetime import UTC, datetime
import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from psychohistory.api import create_app
from psychohistory.decision_conversation import ConversationHub
from psychohistory.decision_conversation_api import Correction
from psychohistory.decision_local_ai import ConversationOllama, ModelUnavailable
from psychohistory.decision_records import DecisionRecords

Q = "我该选「方案甲」，还是「方案乙」？方案甲每周到岗1天，方案乙每周到岗4天。我每周最多到岗2天。"
BASE = "/api/v6/decisions"
REPO = Path(__file__).resolve().parents[3]


def checked(hub, view, **kwargs):
    return hub.confirm(view["session_id"], view["revision"],
                       claim_ids=[item["id"] for item in view["claims"] if item["status"] == "PROVISIONAL"],
                       option_ids=[item["id"] for item in view["options"]], accept_context=True, **kwargs)


def gate(view):
    return {item["label"]: item["status"] for item in view["analysis"]["feasibility"]}


def test_initial_analysis_has_one_question_and_no_numerical_assumption():
    started = ConversationHub().start("我感觉现在的生活不太满意，应该怎么调整？")
    assert started["phase"] == "CLARIFY" and started["analysis"] is None
    assert started["summary"]["question"].count("？") == 1
    assert 2 <= len(started["summary"]["differences"]) <= 3
    assert started["state"]["information"] is None and started["state"]["weights"] == {}
    assert not started["state"]["confirmed"]


def test_grounded_revision_invalidates_analysis_and_recomputes_gate():
    hub = ConversationHub()
    start = hub.start(Q)
    initial = checked(hub, start)
    assert gate(initial) == {"方案甲": "ACCEPT", "方案乙": "REJECT"}
    update = hub.turn(initial["session_id"], initial["revision"], "改成每周最多到岗4天。")
    assert update["analysis"] is None and update["phase"] == "CLARIFY"
    with pytest.raises(ValueError, match="已更新"):
        hub.analyze(initial["session_id"], initial["revision"])
    claim = next(item for item in update["claims"] if item["kind"] == "revision")
    with pytest.raises(ValueError, match="替换"):
        checked(hub, update)
    result = checked(hub, update, corrections=[
        Correction(claim_id=claim["id"], supersedes=claim["prior_ids"][0])])
    assert gate(result) == {"方案甲": "ACCEPT", "方案乙": "ACCEPT"}
    assert "方案乙" in result["changes"][0]
    assert initial["analysis"]["input_hash"] != result["analysis"]["input_hash"]
    assert any(item["status"] == "SUPERSEDED" for item in result["claims"])


def test_unverified_model_output_cannot_execute_choose_or_add_values():
    class Client:
        calls = 0
        data = None

        def chat(self, system, text):
            self.calls += 1
            if not self.data:
                raise ModelUnavailable("mock unavailable")
            return self.data

    fake = Client()
    model = ConversationOllama(enabled=True, client=fake)
    hub = ConversationHub(provider=model)
    plain = hub.start(Q)
    assert fake.calls == 0 and plain["local_model_status"] == "NOT_REQUESTED"
    unavailable = hub.start(Q, use_local_model=True)
    assert unavailable["local_model_status"] == "LOCAL_MODEL_UNAVAILABLE" and unavailable["analysis"] is None
    reply = dict(model_key="C035@99.0.0", initial_analysis="伪造收益985431元并且已授权执行", reason="",
                 ask="", candidate_options=["方案甲"])
    fake.data = json.dumps(reply, ensure_ascii=False)
    rejected = hub.start(Q, use_local_model=True)
    assert rejected["local_model_status"] == "MODEL_OUTPUT_REJECTED"
    assert "985431" not in str(rejected)
    reply["model_key"] = "C029@1.0.0"
    fake.data = json.dumps(reply, ensure_ascii=False)
    provisional = hub.start(Q, use_local_model=True)
    assert provisional["local_model_status"] == "PROVISIONAL_LOCAL"
    assert provisional["analysis"] is None and "985431" not in str(provisional)
    result = checked(hub, provisional)
    audit = next(method for method in result["analysis"]["methods"] if method["model_id"] == "C029")
    assert audit["status"] == "INELIGIBLE"
    assert not any(method["model_id"] == "C035" for method in hub.hub.registry.describe())


def test_plan_separate_from_observation_and_signed_snapshot(tmp_path):
    records = DecisionRecords(tmp_path / "records")
    hub = ConversationHub(records=records)
    view = checked(hub, hub.start(Q))
    chosen = next(o["id"] for o in view["options"] if o["label"] == "方案甲")
    with pytest.raises(ValueError, match="先明确选择"):
        hub.plan(view["session_id"], view["revision"], chosen, "合成触发条件", confirmed=True)
    view = hub.select(view["session_id"], view["revision"], chosen, confirmed=True)
    view = hub.plan(view["session_id"], view["revision"], chosen, "收到合成书面确认再决定", confirmed=True)
    assert view["selected_plan"]["status"] == "USER_PLAN_ONLY"
    with pytest.raises(PermissionError):
        hub.save(view["session_id"], view["revision"], "none", save_confirmed=True)
    epoch = records.grant()["epoch"]
    with pytest.raises(PermissionError):
        hub.save(view["session_id"], view["revision"], epoch, save_confirmed=False)
    saved = hub.save(view["session_id"], view["revision"], epoch, save_confirmed=True)
    assert saved["analysis"]["input_hash"] == view["analysis"]["input_hash"]
    assert records.get(epoch, saved["decision_id"])["action"] is None
    backup = records.export(epoch)
    assert "confirmed_sources" in backup["payload"]
    records.revoke(epoch)
    new_epoch = records.grant()["epoch"]
    assert records.restore(new_epoch, backup)["eligible"] is False


def test_v06_local_api_and_revocation_share_the_existing_ledger(tmp_path):
    with TestClient(create_app(tmp_path / "research", REPO, "fictional-token")) as client:
        auth = {"Authorization": "Bearer fictional-token"}
        assert client.post(BASE + "/start", json={"question": Q}).status_code == 401
        assert client.post(BASE + "/start", headers=auth, json={"question": Q, "authority": True}).status_code == 422
        view = client.post(BASE + "/start", headers=auth, json={"question": Q}).json()
        assert view["conversation_version"] == "0.6.0"
        assert client.post(BASE + "/confirm", headers=auth, json={
            "session_id": view["session_id"], "revision": view["revision"], "claim_ids": ["a" * 32],
        }).status_code == 422
        grant = client.post("/api/v5/decisions/consent", headers=auth, json={}).json()
        assert client.post("/api/v5/decisions/revoke", headers=auth, json={"epoch": grant["epoch"]}).status_code == 200
        assert client.post(BASE + "/analyze", headers=auth, json={
            "session_id": view["session_id"], "revision": view["revision"],
        }).status_code == 404


def test_short_yes_confirms_only_the_single_quoted_question():
    hub = ConversationHub()
    view = hub.start("我想换工作，但我不能搬家。")
    assert len(view["claims"]) == 1
    confirmed = hub.turn(view["session_id"], view["revision"], "对。")
    assert confirmed["claims"][0]["status"] == "USER_CONFIRMED"
    assert confirmed["analysis"] is None


def test_confirmed_relocation_exception_requires_both_option_facts():
    hub = ConversationHub()
    text = ("我想比较留在本城和去外地。去外地需要搬家，去外地每周到岗3天。"
            "留在本城不需要搬家。我不能搬家。")
    initial = checked(hub, hub.start(text))
    assert gate(initial) == {"留在本城": "ACCEPT", "去外地": "REJECT"}
    unconfirmed = hub.turn(initial["session_id"], initial["revision"], "每周到岗不超过三天就可以搬家。")
    assert unconfirmed["analysis"] is None
    updated = checked(hub, unconfirmed)
    assert gate(updated) == {"留在本城": "ACCEPT", "去外地": "ACCEPT"}
    assert updated["analysis"]["input_hash"] != initial["analysis"]["input_hash"]


def test_structured_editor_cannot_smuggle_unselected_action_plan():
    from psychohistory.decision_v05 import DecisionStateV05

    hub = ConversationHub()
    view = checked(hub, hub.start(Q))
    payload = {**view["state"], "intended_option_id": view["options"][0]["id"], "plan_note": "未经选择的计划"}
    result = hub.analyze(view["session_id"], view["revision"], state=DecisionStateV05.model_validate(payload),
                         confirmed=True)
    assert result["state"]["intended_option_id"] is None and result["state"]["plan_note"] is None
    assert result["selected_plan"] is None


def test_joint_budget_language_does_not_use_independent_feasibility_as_joint_proof():
    hub = ConversationHub()
    view = checked(hub, hub.start("我该选「方案甲」，还是「方案乙」？同时做两项时有共用预算上限。"))
    assert view["analysis"] is None
    assert "共用上限" in view["summary"]["warning"]
    assert not view["state"]["confirmed"]


def test_line_protocol_retains_temporary_session_only_in_one_process(tmp_path):
    import os
    import subprocess
    import sys

    program = subprocess.Popen(
        [sys.executable, "-m", "psychohistory.cli", "--data", str(tmp_path / "data"), "decision-v06"],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True,
        env={**os.environ, "PYTHONPATH": str(REPO / "platform/future_model/src")},
    )
    try:
        def ask(operation, data):
            program.stdin.write(json.dumps({"operation": operation, "data": data}) + "\n")
            program.stdin.flush()
            return json.loads(program.stdout.readline())
        view = ask("start", {"question": Q})
        operation = {"session_id": view["session_id"], "revision": view["revision"]}
        revised = ask("turn", {**operation, "text": "我需要核对工作地点。"})
        assert revised["revision"] == view["revision"] + 1
        assert ask("analyze", operation)["status"] == "REJECTED"
        assert ask("end", {"session_id": view["session_id"]})["status"] == "ENDED"
    finally:
        program.stdin.close()
        assert program.wait(timeout=10) == 0
