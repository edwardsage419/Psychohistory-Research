import pytest
from fastapi.testclient import TestClient

from psychohistory.api import create_app
from psychohistory.decision_conversation import ConversationHub
from psychohistory.decision_language import interpret


QUESTION = "房租和停车费合计每月最多3000元。A：每月房租2600元，停车费每月500元。B：每月房租2600元，停车费每月300元。"


def test_v08_requires_current_server_instance_at_every_session_route(tmp_path):
    token = "local-test-token"
    with TestClient(create_app(tmp_path, tmp_path, token=token), headers={"Authorization": f"Bearer {token}"}) as client:
        prefix = "/api/v8/decisions/"
        nonce = "a" * 32
        started = client.post(prefix + "start", json={"question": QUESTION, "cancel_nonce": nonce})
        assert started.status_code == 200, started.text
        view = started.json()
        assert view["conversation_version"] == "0.8.0"
        assert view["session_id"] != nonce
        assert view["cancel_nonce"] == nonce
        session = {"session_id": view["session_id"], "revision": view["revision"]}
        key = {"session_instance": view["session_instance"]}
        assert view["result"]["session_instance"] == view["session_instance"]
        assert isinstance(view["result"]["authority_generation"], int)
        assert client.post(prefix + "analyze", json=session).status_code == 422
        assert client.post(prefix + "end", json={**session, "session_instance": "b" * 32}).status_code == 404
        assert client.post("/api/v7/decisions/analyze", json=session).status_code == 404
        assert client.post("/api/v7/decisions/end", json={"session_id": session["session_id"]}).status_code == 404
        assert client.post(prefix + "cancel-start", json={"cancel_nonce": nonce}).status_code == 200
        advanced = client.post(prefix + "analyze", json={**session, **key})
        assert advanced.status_code == 200, advanced.text
        assert client.post(prefix + "end", json={**session, **key}).status_code == 422
        session["revision"] += 1
        assert client.post(prefix + "end", json={**session, **key}).status_code == 200
        assert client.post(prefix + "analyze", json={**session, **key}).status_code == 404


def test_legacy_client_reservation_does_not_become_a_reusable_session_identity(monkeypatch):
    import psychohistory.decision_conversation as host

    clock = [0]
    monkeypatch.setattr(host, "monotonic", lambda: clock[0])
    hub = ConversationHub()
    label = "c" * 32
    old = hub.start(QUESTION, session_id=label)
    clock[0] += host.SESSION_TTL + 1
    assert old["session_id"] == label  # v7 clients require this echo.
    with pytest.raises(KeyError):
        hub.start(QUESTION, session_id=label)
    new = hub.start(QUESTION, session_id="d" * 32)
    assert old["session_id"] != new["session_id"]
    hub.end(old["session_id"])
    current = hub.analyze(new["session_id"], new["revision"])
    assert current["revision"] == 2


def test_session_that_expires_during_parse_cannot_publish_into_a_restarted_conversation(monkeypatch):
    import psychohistory.decision_conversation as host

    clock = [0]
    started_again = []
    label = "e" * 32

    def parse(text, **kwargs):
        if text == "另一个说法":
            clock[0] += host.SESSION_TTL + 1
            started_again.append(hub.start(QUESTION, session_id="f" * 32))
        return interpret(text, **kwargs)

    monkeypatch.setattr(host, "monotonic", lambda: clock[0])
    hub = ConversationHub(parser=parse)
    first = hub.start(QUESTION, session_id=label)
    with pytest.raises(KeyError):
        hub.turn(first["session_id"], first["revision"], "另一个说法")
    fresh, = started_again
    assert first["session_id"] != fresh["session_id"]
    assert hub.analyze(fresh["session_id"], fresh["revision"])["revision"] == 2


def test_dismissed_exact_proposal_can_be_reoffered_but_stays_pending():
    hub = ConversationHub()
    text = "每周最多到岗4天。"
    first = hub.start(text)
    bound = next(claim for claim in first["claims"] if claim["field"] == "onsite_max")
    dismissed = hub.confirm(first["session_id"], first["revision"], dismiss_claim_ids=[bound["id"]])
    assert dismissed["analysis"] is None
    next_view = hub.turn(dismissed["session_id"], dismissed["revision"], text)
    same_bound = [claim for claim in next_view["claims"] if claim["field"] == "onsite_max"]
    assert [claim["status"] for claim in same_bound] == ["DISMISSED", "PROVISIONAL"]
    assert next_view["analysis"] is None


def test_partial_result_is_bound_and_never_eligible_for_selection_or_save():
    hub = ConversationHub()
    start = hub.start("预算最多3000元。A：费用4000元。B：费用2000元。我不能确定是否必须搬家。", current=True)
    key = {"session_instance": start["session_instance"]}
    current = hub.confirm(
        start["session_id"], start["revision"],
        claim_ids=[item["id"] for item in start["claims"] if item["status"] == "PROVISIONAL"],
        option_ids=[item["id"] for item in start["options"]],
        accept_context=True, **key,
    )
    assert current["analysis"] is None
    assert current["phase"] == "CLARIFY"
    partial = current["partial_analysis"]
    assert partial["authority"] == "NONE"
    assert partial["session_instance"] == current["session_instance"]
    assert partial["revision"] == current["revision"]
    assert partial["dependency_sha256"] == current["result"]["layers"]["preparation"]["sha256"]
    assert current["result"]["layers"]["calculation"]["status"] == "NOT_RUN"
    assert current["result"]["layers"]["partial_calculation"]["status"] == "DESCRIPTIVE_ONLY"
    with pytest.raises(ValueError, match="已经通过筛查"):
        hub.select(current["session_id"], current["revision"], current["options"][0]["id"],
                   confirmed=True, **key)
    updated = hub.turn(current["session_id"], current["revision"], "重新核对这些资料。", **key)
    assert updated["partial_analysis"] is None


def test_v08_privacy_revocation_ends_the_live_authority_epoch(tmp_path):
    token = "local-test-token"
    with TestClient(create_app(tmp_path, tmp_path, token=token), headers={"Authorization": f"Bearer {token}"}) as client:
        status = client.get("/api/v5/decisions/consent").json()
        granted = client.post("/api/v5/decisions/consent", json={})
        assert granted.status_code == 200, granted.text
        assert status["authorized"] is False
        route = "/api/v8/decisions/"
        old = client.post(route + "start", json={"question": QUESTION}).json()
        body = {key: old[key] for key in ("session_id", "session_instance", "revision")}
        revoked = client.post("/api/v5/decisions/revoke", json={"epoch": granted.json()["epoch"]})
        assert revoked.status_code == 200, revoked.text
        assert client.post(route + "analyze", json=body).status_code == 404
        new = client.post(route + "start", json={"question": QUESTION}).json()
        assert new["result"]["authority_generation"] > old["result"]["authority_generation"]


def test_v08_capabilities_match_cli_contract(tmp_path):
    from psychohistory.decision_conversation_api import current_capabilities

    token = "local-test-token"
    with TestClient(create_app(tmp_path, tmp_path, token=token), headers={"Authorization": f"Bearer {token}"}) as client:
        published = client.get("/api/v8/decisions/capabilities").json()
    assert published == current_capabilities(ConversationHub())
    assert published["conversation_contract"]["session_instance"] == "REQUIRED"
    assert published["conversation_contract"]["feedback"] == "ISOLATED_DEVELOPMENT_ONLY"


def test_legacy_id_cannot_be_reused_after_restart(tmp_path):
    from psychohistory.decision_conversation_api import create_conversation_root

    root = tmp_path / "workspace"
    nonce = "d" * 32
    first = create_conversation_root(root)
    assert first.start(QUESTION, session_id=nonce)["session_id"] == nonce
    first.end(nonce)
    restarted = create_conversation_root(root)
    with pytest.raises(KeyError):
        restarted.start(QUESTION, session_id=nonce)
    assert restarted.records.status() == {"authorized": False, "epoch": None}


def test_discard_accepts_last_delivered_revision_of_only_the_same_instance(tmp_path):
    token = "local-test-token"
    with TestClient(create_app(tmp_path, tmp_path, token=token), headers={"Authorization": f"Bearer {token}"}) as client:
        route = "/api/v8/decisions/"
        first = client.post(route + "start", json={"question": QUESTION}).json()
        stale = {key: first[key] for key in ("session_id", "session_instance", "revision")}
        assert client.post(route + "analyze", json=stale).status_code == 200
        other = client.post(route + "start", json={"question": QUESTION}).json()
        assert client.post(route + "discard", json={**stale, "session_instance": other["session_instance"]}).status_code == 404
        assert client.post(route + "end", json=stale).status_code == 422
        assert client.post(route + "discard", json=stale).status_code == 200
        assert client.post(route + "analyze", json={**stale, "revision": first["revision"] + 1}).status_code == 404
