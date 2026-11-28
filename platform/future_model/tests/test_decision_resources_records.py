from datetime import UTC, datetime
from decimal import Decimal
import json
import sqlite3

import pytest

from psychohistory.decision_records import DecisionRecords
from test_decision_records import snapshot


def resource_payload(amount="85.05"):
    day = datetime.now(UTC).date().isoformat()
    return {"as_of": day, "goals": ["Fictional savings goal"],
            "cash": {"currency": "USD", "opening_balance": amount, "balance_includes_through": day},
            "options": [{"option_id": "a", "future_cost": "50.05"}]}


def test_local_resource_reuse_requires_separate_aba_safe_consent(tmp_path):
    records = DecisionRecords(tmp_path / "personal")
    epoch = records.grant()["epoch"]
    state, analysis = snapshot()
    identity = state["decision_id"]
    records.save(epoch, state, analysis, resource_state=resource_payload())
    with pytest.raises(PermissionError):
        records.resource_for_reuse(epoch, identity, "ungranted")
    with pytest.raises(PermissionError):
        records.grant_resource_reuse(epoch, identity, confirmed=False)
    first = records.grant_resource_reuse(epoch, identity, confirmed=True)["reuse_epoch"]
    shared = records.resource_for_reuse(epoch, identity, first)
    assert shared.cash.opening_balance == Decimal("85.05")
    assert shared.options == []
    records.revoke_resource_reuse(epoch, identity, first)
    assert records.get(epoch, identity)["snapshots"][0]["resource_state"]["cash"]["opening_balance"] == "85.05"
    second = records.grant_resource_reuse(epoch, identity, confirmed=True)["reuse_epoch"]
    with pytest.raises(PermissionError):
        records.resource_for_reuse(epoch, identity, first)
    assert records.resource_for_reuse(epoch, identity, second).goals == ["Fictional savings goal"]
    records.save(epoch, *snapshot(identity, 2), resource_state=resource_payload("94.10"))
    with pytest.raises(PermissionError):
        records.resource_for_reuse(epoch, identity, second)
    third = records.grant_resource_reuse(epoch, identity, confirmed=True)["reuse_epoch"]
    records.delete(epoch, identity)
    with pytest.raises(PermissionError):
        records.resource_for_reuse(epoch, identity, third)


def test_private_backup_restores_snapshot_without_reviving_reuse(tmp_path):
    root = tmp_path / "personal"
    records = DecisionRecords(root)
    epoch = records.grant()["epoch"]
    state, analysis = snapshot()
    identity = state["decision_id"]
    saved = records.save(epoch, state, analysis, resource_state=resource_payload())
    assert saved["resource_prediction"]["options"]["a"]["cash"]["margin"] == "35.00"
    with pytest.raises(ValueError):
        records.save(epoch, state, analysis, resource_state=resource_payload("94.10"))
    consent = records.grant_resource_reuse(epoch, identity, confirmed=True)
    backup = records.export(epoch)
    assert backup["backup_version"] == "1.2.0"
    assert consent["reuse_epoch"] not in backup["payload"]
    records.revoke_resource_reuse(epoch, identity, consent["reuse_epoch"])

    with sqlite3.connect(root / "records.sqlite3") as db:
        payload = json.loads(db.execute("SELECT payload FROM records").fetchone()[0])
        payload["snapshots"][0]["resource_state"]["cash"]["opening_balance"] = "500.00"
        db.execute("UPDATE records SET payload=?", (json.dumps(payload),))
    with pytest.raises(ValueError):
        records.get(epoch, identity)

    assert records.restore(epoch, backup)["eligible"] is True
    assert records.restore(epoch, backup, confirm=True)["decision_count"] == 1
    restored = records.get(epoch, identity)["snapshots"][0]
    assert restored["resource_state"] == saved["resource_state"]
    assert restored["resource_prediction"] == saved["resource_prediction"]
    with pytest.raises(PermissionError):
        records.resource_for_reuse(epoch, identity, consent["reuse_epoch"])
    records.revoke(epoch)
    with pytest.raises(ValueError):
        records.restore(records.grant()["epoch"], backup, confirm=True)


def test_feedback_replay_preserves_prediction_and_unobserved_options(tmp_path):
    records = DecisionRecords(tmp_path / "personal")
    epoch = records.grant()["epoch"]
    state, analysis = snapshot()
    identity = state["decision_id"]
    saved = records.save(epoch, state, analysis, resource_state=resource_payload())
    only_prediction = records.resource_replay(epoch, identity)
    assert only_prediction["outcome_coverage"] == {"a": "UNOBSERVED", "b": "UNOBSERVED"}

    records.action(epoch, identity, "a", datetime.now(UTC).isoformat(), 1)
    records.review(epoch, identity, "Completed at a different cost.", datetime.now(UTC).isoformat(), "real")
    replay = records.resource_replay(epoch, identity)
    assert replay["original_prediction"] == saved["resource_prediction"]
    assert replay["matches_original"] is True
    assert replay["outcome_coverage"] == {"a": "USER_REPORTED", "b": "UNOBSERVED"}
    assert replay["reviews"][0]["observation"] == "Completed at a different cost."
    assert replay["training"] == "DISABLED"


def test_feedback_from_later_revision_is_not_attributed_to_old_prediction(tmp_path):
    records = DecisionRecords(tmp_path / "personal")
    epoch = records.grant()["epoch"]
    state, analysis = snapshot()
    identity = state["decision_id"]
    original = records.save(epoch, state, analysis, resource_state=resource_payload())
    records.save(epoch, *snapshot(identity, 2), resource_state=resource_payload("95.05"))
    records.action(epoch, identity, "a", datetime.now(UTC).isoformat(), 2)
    records.review(epoch, identity, "A second-revision observation.", datetime.now(UTC).isoformat(), "real")

    earlier = records.resource_replay(epoch, identity, revision=1)
    assert earlier["original_prediction"] == original["resource_prediction"]
    assert earlier["outcome_coverage"] == {"a": "UNOBSERVED", "b": "UNOBSERVED"}
    assert earlier["reviews"] == []
