from datetime import UTC, datetime
import json
import os
from pathlib import Path
import subprocess
import sys

from fastapi.testclient import TestClient

from psychohistory.api import create_app
from psychohistory.decision_service import personal_data_root

REPO = Path(__file__).resolve().parents[3]
V4, V5 = "/api/v4/decisions", "/api/v5/decisions"
HEADERS = {"Authorization": "Bearer fictional-v05-test-token"}


def complete(state):
    state.update(confirmed=True, constraints_confirmed=True, deadline="一周内",
                 objectives=[dict(id="a-goal", label="练习质量", unit="分", direction="max")],
                 options=[dict(id="a", label="保留安排"), dict(id="b", label="更换安排")])
    return state


def test_api_uses_same_ledger_but_preserves_workflow_and_action_boundaries(tmp_path):
    research = tmp_path / "research"
    marker = "Fictional v05 question and private false field"
    with TestClient(create_app(research, REPO, "fictional-v05-test-token")) as client:
        def invoke(url, data, expected=200, headers=HEADERS):
            response = client.post(url, json=data, headers=headers)
            assert response.status_code == expected, response.text
            return response.json()

        assert client.get(V5 + "/models").status_code == 401
        invoke(V5 + "/start", {"question": marker}, 403, {**HEADERS, "Origin": "https://example.invalid"})
        invalid = invoke(V5 + "/start", {"question": marker, marker: True}, 422)
        assert marker not in json.dumps(invalid)
        initial = invoke(V5 + "/start", {"question": marker})
        assert initial["plan"]["items"] and initial["execution"]["available"] is False
        state = complete(initial["state"])
        state.update(intended_option_id="b", plan_note="仅记录未来的选择计划")
        assert not personal_data_root(research).exists()
        denied_execution = client.post(V5 + "/execute", json={"decision_id": state["decision_id"]}, headers=HEADERS)
        assert denied_execution.status_code in {404, 405}
        invoke(V5 + "/save", {"state": state, "epoch": "ungranted"}, 403)
        assert not personal_data_root(research).exists()
        auth = {"epoch": invoke(V4 + "/consent", {})["epoch"]}
        state["preferences"] = {"values": [{"label": "练习", "value": "优先持续性"}],
                                "applicability": "虚构学习选择", "provenance": "用户确认"}
        saved = invoke(V5 + "/save", {**auth, "state": state})
        assert saved["analysis"]["hub_version"] == "0.5.0"
        assert saved["state"]["intended_option_id"] == "b"
        key = {**auth, "decision_id": state["decision_id"]}
        assert invoke(V5 + "/record", key)["action"] is None
        action = {**key, "revision": 1, "option_id": "a", "occurred_at": datetime.now(UTC).isoformat()}
        invoke(V4 + "/action", action, 422)
        assert invoke(V5 + "/action", action)["coverage"]["b"] == "UNOBSERVED"
        review = invoke(V5 + "/review", {**key, "observed_at": datetime.now(UTC).isoformat(),
                                        "observation": "虚构结果", "kind": "synthetic",
                                        "hindsight": {"evidence": "后来加入的信息",
                                                      "current_preferences": state["preferences"]}})
        assert review["hindsight"]["evidence"] == "后来加入的信息"
        invoke(V5 + "/adopt-preferences", {**key, "review_index": 1, "confirmed": False}, 422)
        adopted = invoke(V5 + "/adopt-preferences", {**key, "review_index": 1, "confirmed": True})
        assert invoke(V5 + "/preferences", auth)[0]["version_id"] == adopted["version_id"]
        next_state = invoke(V5 + "/start", {"question": "Different fictional question"})["state"]
        assert next_state["preferences"] is None and next_state["weights"] == {}
        assert invoke(V5 + "/record", key)["snapshots"][0] == saved


def test_cli_v05_start_analyze_and_versioned_catalog(tmp_path):
    base = [sys.executable, "-m", "psychohistory.cli", "--data", str(tmp_path / "research")]
    environment = {**os.environ, "PYTHONPATH": str(REPO / "platform/future_model/src")}

    def call(workflow, operation, payload=None):
        result = subprocess.run([*base, workflow, operation], input=json.dumps(payload) if payload else "",
                                text=True, capture_output=True, env=environment, timeout=20)
        assert result.returncode == 0, result.stderr
        return json.loads(result.stdout)

    started = call("decision-v05", "start", {"question": "我该参加虚构培训，还是保留资金？"})
    result = call("decision-v05", "analyze", {"state": started["state"]})
    assert result["status"] == "CLARIFY" and result["plan"]["items"]
    v4 = {item["model_id"] for item in call("decision", "models")}
    v5 = {item["model_id"] for item in call("decision-v05", "models")}
    assert v4 < v5
