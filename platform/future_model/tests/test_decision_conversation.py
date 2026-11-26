from datetime import UTC, datetime
import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from psychohistory.api import create_app
from psychohistory.decision_conversation import ConversationHub
from psychohistory.decision_conversation_api import Correction
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


def test_retired_model_parameter_runs_same_local_path(monkeypatch):
    for key in ("PSYCHOHISTORY_LOCAL_AI", "PSYCHOHISTORY_LOCAL_MODEL", "OLLAMA_HOST"):
        monkeypatch.setenv(key, "1")

    def denied(*args, **kwargs):
        pytest.fail("Autonomous analysis attempted a network connection")

    monkeypatch.setattr("socket.create_connection", denied)
    monkeypatch.setattr("socket.socket.connect", denied)
    hub = ConversationHub()
    plain = hub.start(Q)
    legacy = hub.start(Q, use_local_model=True)
    assert plain["local_model_status"] == "LOCAL_AI_DISABLED"
    assert legacy["local_model_status"] == "LEGACY_REQUEST_RETIRED"
    assert legacy["local_model_receipt"]["notice"]
    assert plain["options"] == legacy["options"]
    assert gate(checked(hub, legacy)) == {"方案甲": "ACCEPT", "方案乙": "REJECT"}


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
        assert view["conversation_version"] == "0.7.0"
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


# Owner-authorized repair following A35-01 through A35-04.
def test_unsupported_conditional_limit_cannot_disappear_from_gate():
    hub = ConversationHub()
    text = ("我该选「方案甲」，还是「方案乙」？方案甲每周到岗1天，方案乙每周到岗4天。"
            "如果签约，我每周最多到岗2天。")
    started = hub.start(text)
    assert any(c["field"] == "onsite_max" and c["kind"] == "conditional"
               for c in started["claims"])
    result = checked(hub, started)
    assert result["analysis"] is None
    assert not result["state"]["constraints_confirmed"]
    assert "底线" in result["summary"]["warning"]


def test_unprojectable_monthly_budget_blocks_gate():
    from psychohistory.decision_conversation import blocking_constraints

    claim = dict(field="cost_max", kind="constraint", subject="", value="3000",
                 unit="yuan/month", source="每月预算最多3000元",
                 status="USER_CONFIRMED", confirmed_at="fixture")
    assert blocking_constraints([claim]) == [claim]
    assert not blocking_constraints([{**claim, "unit": "yuan"}])


def test_context_must_be_reconfirmed_after_substantive_turn():
    hub = ConversationHub()
    initial = checked(hub, hub.start(Q))
    revised = hub.turn(initial["session_id"], initial["revision"], "还要照顾家人。")
    assert revised["analysis"] is None
    assert not revised["state"]["constraints_confirmed"]
    retry = hub.analyze(revised["session_id"], revised["revision"])
    assert retry["analysis"] is None
    assert not retry["state"]["confirmed"]


def test_known_relocation_exception_does_not_cover_unrelated_conditional():
    from psychohistory.decision_conversation import blocking_constraints

    source = "每周到岗不超过三天就可以搬家。"
    def c(field, value, unit, kind="conditional", status="USER_CONFIRMED", text=source):
        return dict(field=field, value=value, unit=unit, kind=kind, status=status,
                    subject="", confirmed_at="fixture", source=text)
    base = [c("move_allowed", "no", "", "constraint", text="不能搬家"),
            c("move_if_onsite_max", "3", "days/week"),
            c("onsite_max", "3", "days/week", status="UNKNOWN"),
            c("move_allowed", "yes", "", status="UNKNOWN")]
    assert blocking_constraints(base) == []
    unrelated = c("onsite_max", "2", "days/week", text="如果签约，每周最多到岗2天。")
    assert blocking_constraints(base + [unrelated]) == [unrelated]
    assert blocking_constraints(base[:-1])


@pytest.mark.parametrize("clears", [0, 1, 2])
def test_pending_start_cannot_recreate_session_after_clear(clears):
    from concurrent.futures import ThreadPoolExecutor
    from threading import Event

    entered, release = Event(), Event()

    from psychohistory.decision_language import interpret

    def delayed(text, *args, **kwargs):
        if text == Q:
            entered.set()
            if not release.wait(10):
                raise RuntimeError("test parser timed out")
        return interpret(text, *args, **kwargs)

    hub = ConversationHub(parser=delayed)
    with ThreadPoolExecutor(max_workers=1) as executor:
        pending = executor.submit(hub.start, Q, use_local_model=True)
        try:
            assert entered.wait(10)
            for _ in range(clears):
                hub.clear()
            fresh = hub.start("我应该比较哪两个方案？") if clears else None
        finally:
            release.set()
        if clears:
            with pytest.raises(KeyError, match="Session invalidated"):
                pending.result(timeout=10)
            assert list(hub._sessions) == [fresh["session_id"]]
        else:
            result = pending.result(timeout=10)
            assert list(hub._sessions) == [result["session_id"]]


def test_cancel_pending_start_by_id_even_when_end_arrives_first():
    from concurrent.futures import ThreadPoolExecutor
    from threading import Event

    from psychohistory.decision_language import interpret

    entered, release = Event(), Event()
    session_id = "1" * 32

    def delayed(text):
        entered.set()
        assert release.wait(10)
        return interpret(text)

    hub = ConversationHub(parser=delayed)
    with ThreadPoolExecutor(max_workers=1) as executor:
        pending = executor.submit(hub.start, Q, session_id=session_id)
        try:
            assert entered.wait(10)
            hub.end(session_id)
        finally:
            release.set()
        with pytest.raises(KeyError, match="Session invalidated"):
            pending.result(timeout=10)
    with pytest.raises(KeyError, match="Session invalidated"):
        hub.start(Q, session_id=session_id)


def test_v7_receipt_revisions_and_purpose_are_bound_to_current_session():
    hub = ConversationHub()
    initial = hub.start(Q)
    checked_view = checked(hub, initial)
    assert checked_view["result"]["session_id"] == initial["session_id"]
    assert checked_view["result"]["revision"] == checked_view["revision"]
    assert checked_view["result"]["purpose"] == "temporary_analysis"
    assert checked_view["result"]["layers"]["calculation"]["status"] == "COMPUTED"
    assert checked_view["result"]["layers"]["semantic"]["sha256"] == initial["result"]["layers"]["semantic"]["sha256"]
    twin = checked(hub, hub.start(Q))
    assert twin["result"]["receipt_sha256"] != checked_view["result"]["receipt_sha256"]
    with pytest.raises(ValueError):
        hub.analyze(initial["session_id"], initial["revision"])


def test_plain_scenario_scores_reach_native_regret_without_probabilities():
    question = ("我该选「方案甲」，还是「方案乙」？"
                "情景平常：方案甲得10分，方案乙得6分。"
                "情景变动：方案甲得0分，方案乙得7分。都比较未来30天，分差可比较，分数越高越好。")
    hub = ConversationHub()
    initial = hub.start(question)
    assert initial["analysis"] is None and not initial["state"]["scenarios"]
    view = checked(hub, initial)
    assert len(view["state"]["scenarios"]) == 2
    assert all(item["probability"] is None for item in view["state"]["scenarios"])
    method = next(method for method in view["analysis"]["methods"] if method["model_id"] == "C029")
    by_label = {item["label"]: item["id"] for item in view["options"]}
    assert method["status"] == "EXECUTED"
    assert method["result"]["leaders"] == [by_label["方案乙"]]


def test_confirmed_resource_revision_drives_native_gate():
    from datetime import date

    from psychohistory.decision_resources import ResourceState

    hub = ConversationHub()
    initial = checked(hub, hub.start("我该选「方案甲」，还是「方案乙」？"))
    by_label = {item["label"]: item["id"] for item in initial["options"]}
    today = date.today().isoformat()
    pending = {"as_of": today, "cash": {"currency": "CNY", "opening_balance": "800",
                                        "balance_includes_through": today, "source": "虚构现金快照",
                                        "events": [
                                            {"id": "paid", "kind": "actual_expense", "date": today, "amount": 400, "source": "虚构已付"},
                                            {"id": "refund", "kind": "estimated_refund", "date": today, "amount": 500, "refund_of": "paid", "source": "虚构预计"},
                                        ]},
               "options": [{"option_id": by_label["方案甲"], "future_cost": 900},
                           {"option_id": by_label["方案乙"], "future_cost": 600}]}
    checked_cash = hub.update_resources(initial["session_id"], initial["revision"],
                                        resources=ResourceState.model_validate(pending), confirmed=True)
    assert gate(checked_cash) == {"方案甲": "REJECT", "方案乙": "ACCEPT"}
    assert checked_cash["resources"]["result"]["cash"]["balance"] == "800.00"
    with pytest.raises(ValueError, match="已更新"):
        hub.select(initial["session_id"], initial["revision"], by_label["方案甲"], confirmed=True)
    pending["cash"]["opening_balance"] = "1000"
    amended = hub.update_resources(initial["session_id"], checked_cash["revision"],
                                   resources=ResourceState.model_validate(pending), confirmed=True)
    assert gate(amended) == {"方案甲": "ACCEPT", "方案乙": "ACCEPT"}
    assert amended["result"]["receipt_sha256"] != checked_cash["result"]["receipt_sha256"]
