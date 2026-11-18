import time
from pathlib import Path

from fastapi.testclient import TestClient

from psychohistory.api import create_app


REPO = Path(__file__).resolve().parents[3]
HEADERS = {"Authorization": "Bearer test-v2"}


def test_protocol_approval_locked_holdout_and_artifact(tmp_path):
    with TestClient(create_app(tmp_path / "data", REPO, "test-v2")) as client:
        def post(path, data=None, code=200):
            response = client.post("/api/v2/" + path, headers=HEADERS, json=data or {})
            assert response.status_code == code, response.text
            return response.json()

        assert client.get("/api/v2/sources").status_code == 401
        source = post("sources", {"research_id": "R123"})
        protocol = post("protocols", {"seed": 813, "source_id": source["source_id"],
                                      "model_id": "r123-degroot", "model_version": "1.0.0"})
        pid = protocol["protocol_id"]
        post("experiments", {"protocol_id": pid}, 422)
        post(f"protocols/{pid}/approve")
        run = post("experiments", {"protocol_id": pid})
        assert post("experiments", {"protocol_id": pid})["id"] == run["id"]
        post(f"experiments/{run['id']}/cancel")
        retry = post(f"experiments/{run['id']}/retry")
        assert retry["id"] != run["id"]
        post(f"experiments/{retry['id']}/approve")
        for _ in range(200):
            current = client.get(f"/api/v2/experiments/{retry['id']}", headers=HEADERS).json()
            if current["status"] not in {"PENDING", "APPROVED", "RUNNING"}:
                break
            time.sleep(.05)
        assert current["status"] == "COMPLETED", current
        artifact = client.get(f"/api/v2/experiments/{retry['id']}/result", headers=HEADERS).json()
        assert artifact["artifact_sha256"] == current["result_hash"]
        assert set(artifact["result"]["metrics"]) == {"r123-degroot", "train-prevalence"}
        assert artifact["result"]["protocol_id"] == pid
        assert post("experiments", {"protocol_id": pid})["id"] == retry["id"]
        assert post(f"experiments/{retry['id']}/retry")["id"] == retry["id"]
        assert client.get("/api/v1/runs", headers=HEADERS).json() == []


def test_candidate_duplicates_and_worker_refuses_changed_code_identity(tmp_path):
    from psychohistory.sources import MAIN_COMMIT
    from psychohistory.service import Service

    with TestClient(create_app(tmp_path / "candidate", REPO, "test-v2")) as client:
        candidate = client.post("/api/v2/sources", headers=HEADERS,
                                json={"research_id": "R123", "commit": MAIN_COMMIT}).json()
        assert candidate["origin"] == "CANDIDATE"
        duplicate = client.post("/api/v2/sources", headers=HEADERS,
                                json={"research_id": "R123", "commit": MAIN_COMMIT}).json()
        assert candidate["source_id"] == duplicate["source_id"]
        assert "DUPLICATE_SOURCE_ID" in duplicate["warnings"]
        assert len(client.get("/api/v2/sources", headers=HEADERS).json()) == 1
        denied = client.post("/api/v2/protocols", headers=HEADERS,
                             json={"seed": 92, "source_id": candidate["source_id"],
                                   "model_id": "r123-degroot", "model_version": "1.0.0"})
        assert denied.status_code == 403

    service = Service(tmp_path / "code", REPO, dispatch=False)
    try:
        workflow = service.workflow
        source = workflow.register_source("R123")
        protocol = workflow.create_protocol(source["source_id"], 82, "r123-degroot", "1.0.0")
        identity = protocol["protocol_id"]
        workflow.approve_protocol(identity)
        run = workflow.submit(service.scheduler, identity)
        identifier = run["id"]
        service.store.update_run(identifier, code_sha256="0" * 64)
        service.scheduler.approve(identifier)
        service.scheduler.execute_approved(identifier)
        outcome = service.scheduler.wait(identifier)
        assert outcome["status"] == "BLOCKED"
        assert "identity changed" in outcome["error"]
        assert outcome["result_hash"] is None
        assert any("blocked execution" in entry for entry in outcome["logs"])
        retry = workflow.retry(service.scheduler, identifier)
        assert retry["id"] != identifier
        assert retry["retry_of"] == identifier
        assert service.store.get_run(identifier) == outcome
    finally:
        service.close()


def test_consumed_holdout_survives_late_failure_and_restart(tmp_path, monkeypatch):
    from psychohistory.service import Service

    root = tmp_path / "late-failure"
    service = Service(root, REPO, dispatch=False)
    try:
        source = service.workflow.register_source("R123")
        protocol = service.workflow.create_protocol(source["source_id"], 56, "r123-degroot", "1.0.0")
        identity = protocol["protocol_id"]
        service.workflow.approve_protocol(identity)
        run_id = service.workflow.submit(service.scheduler, identity)["id"]

        def fail_after_scoring(result):
            raise OSError("injected persistence failure after scoring")

        monkeypatch.setattr(service.store, "put", fail_after_scoring)
        service.scheduler.approve(run_id)
        service.scheduler.execute_approved(run_id)
        outcome = service.scheduler.wait(run_id)
        assert outcome["status"] == "FAILED"
        assert "persistence failure" in outcome["error"]
        assert outcome["result_hash"] is None
    finally:
        service.close()

    with TestClient(create_app(root, REPO, "test-v2")) as client:
        retry = client.post(f"/api/v2/experiments/{run_id}/retry", headers=HEADERS, json={})
        assert retry.status_code == 422
        assert "holdout" in retry.json()["detail"].lower()
        assert len(client.get("/api/v2/experiments", headers=HEADERS).json()) == 1
        for endpoint in ("", "/result"):
            assert client.get(f"/api/v1/runs/{run_id}{endpoint}", headers=HEADERS).status_code == 404
        for action in ("approve", "cancel"):
            assert client.post(f"/api/v1/runs/{run_id}/{action}", headers=HEADERS, json={}).status_code == 404


def test_incomplete_comparison_result_cannot_pass_validation():
    import pytest
    from psychohistory.prediction import protocol_spec
    from psychohistory.v02_execution import validate_result

    config = {"protocol_id": "p", "source_id": "s", "spec": protocol_spec(1)}
    run = {"config": config, "code_sha256": "c"}
    incomplete = {"input": config, "protocol_id": "p", "source_id": "s", "code_sha256": "c"}
    with pytest.raises(ValueError, match="Incomplete comparison"):
        validate_result(run, incomplete)
