from datetime import UTC, datetime
import json
import os
from pathlib import Path
import subprocess
import sys

from fastapi.testclient import TestClient

from psychohistory.api import create_app
from psychohistory.decision_service import personal_data_root
from test_decision_hub import decision

REPO = Path(__file__).resolve().parents[3]
URL = "/api/v4/decisions"
HEADERS = {"Authorization": "Bearer fictitious-local-secret"}


def test_api_local_boundary_and_no_persistence_without_permission(tmp_path):
    root = tmp_path / "science"
    marker = "FICTITIOUS do not echo invalid input"
    with TestClient(create_app(root, REPO, "fictitious-local-secret")) as client:
        assert client.get(URL + "/models").status_code == 401
        assert client.post(URL + "/start", headers={**HEADERS, "Origin": "https://example.invalid"},
                           json={"question": marker}).status_code == 403
        broken = client.post(URL + "/analyze", headers=HEADERS, json={"state": {"question": marker}})
        assert broken.status_code == 422 and marker not in broken.text
        start = client.post(URL + "/start", headers=HEADERS, json={"question": marker})
        assert start.status_code == 200 and start.headers["cache-control"] == "no-store"
        assert start.json()["state"]["question"] == marker
        assert client.post(URL + "/analyze", headers=HEADERS, json={"state": decision()}).status_code == 200
        assert client.post(URL + "/save", headers=HEADERS,
                           json={"epoch": "fictitious-token", "state": decision()}).status_code == 403
        assert client.get(URL + "/consent", headers=HEADERS).json()["authorized"] is False
        assert not personal_data_root(root).exists()


def test_api_consent_revisions_review_withdrawal_and_research_backup(tmp_path):
    root = tmp_path / "science"
    personal_marker = "FICTITIOUS career marker 5e96"
    state = decision()
    state["question"] = personal_marker
    archive = tmp_path / "research-backup"
    with TestClient(create_app(root, REPO, "fictitious-local-secret")) as client:
        def post(path, payload):
            return client.post(URL + "/" + path, headers=HEADERS, json=payload)

        grant = post("consent", {}).json()
        auth = {"epoch": grant["epoch"]}
        key = {**auth, "decision_id": state["decision_id"]}
        assert grant["authorized"]
        assert post("save", {**auth, "state": state, "analysis": {"leaders": ["b"]}}).status_code == 422
        first = post("save", {**auth, "state": state})
        assert first.status_code == 200, first.text
        assert first.json()["analysis"]["feasibility"][1]["status"] == "REJECT"
        state["revision"] = 2
        state["constraints"][0]["threshold"] = "9"
        second = post("save", {**auth, "state": state})
        assert second.status_code == 200, second.text
        assert second.json()["analysis"]["input_hash"] != first.json()["analysis"]["input_hash"]
        action = {**key, "option_id": "a", "occurred_at": datetime.now(UTC).isoformat()}
        assert post("action", {**action, "revision": 1}).status_code == 422
        assert post("action", {**action, "revision": 2}).status_code == 200
        assert post("review", {**key, "observation": "虚构回访", "observed_at": datetime.now(UTC).isoformat(),
                               "kind": "synthetic"}).status_code == 200
        record = post("record", key).json()
        assert [snapshot["revision"] for snapshot in record["snapshots"]] == [1, 2]
        assert record["action"]["coverage"]["b"] == "UNOBSERVED"
        assert record["reviews"][0]["option_id"] == "a"
        exported = post("export", auth).json()
        assert personal_marker in json.dumps(exported)
        assert auth["epoch"] not in json.dumps(exported)
        assert personal_marker not in client.get("/api/v1/runs", headers=HEADERS).text
        client.app.state.service.scheduler.backup(archive)
        files = [path for path in archive.rglob("*") if path.is_file()]
        assert files and all(personal_marker.encode() not in path.read_bytes() for path in files)
        assert post("revoke", auth).json()["authorized"] is False
        assert post("record", key).status_code == 403
        auth = {"epoch": post("consent", {}).json()["epoch"]}
        assert not post("restore", {**auth, "backup": exported, "confirm": False}).json()["eligible"]
        assert post("restore", {**auth, "backup": exported, "confirm": True}).status_code == 422
        assert post("history", auth).json() == []


def test_cli_uses_the_same_analysis_and_record_contract(tmp_path):
    root = tmp_path / "science"
    base = [sys.executable, "-m", "psychohistory.cli", "--data", str(root), "decision"]
    env = {**os.environ, "PYTHONPATH": str(REPO / "platform/future_model/src")}

    def run(action, data=None, code=0):
        result = subprocess.run(base + [action], input=json.dumps(data) if data is not None else "",
                                capture_output=True, text=True, env=env, timeout=15)
        assert result.returncode == code, result.stderr
        return json.loads(result.stdout if code == 0 else result.stderr)

    raw = "我该留在虚构工作甲，还是接受虚构工作乙？"
    started = run("start", {"question": raw})
    assert started["state"]["question"] == raw
    assert run("analyze", {"state": started["state"]})["status"] == "CLARIFY"
    assert run("status")["authorized"] is False
    assert not personal_data_root(root).exists()
    state = decision()
    outcome = run("analyze", {"state": state})
    grant = run("grant")
    snapshot = run("save", {"state": state, "epoch": grant["epoch"]})
    assert snapshot["analysis"] == outcome
    assert run("history", {"epoch": grant["epoch"]})[0]["decision_id"] == state["decision_id"]
    assert not run("revoke", {"epoch": grant["epoch"]})["authorized"]
    assert run("history", {"epoch": grant["epoch"]}, code=1)["status"] == "FAILED"
