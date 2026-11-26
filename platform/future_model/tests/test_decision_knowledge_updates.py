"""Public facts import stays quarantined and cannot modify the offline index."""
from datetime import date

import pytest


def _quarantine():
    from psychohistory.decision_knowledge_updates import ExternalFactQuarantine, PublicFactSource

    source = PublicFactSource(
        id="development-fixture", url="https://example.invalid/public-data/v1.json",
        publisher="Synthetic test publisher", version="fixture-v1", licence="synthetic test data",
        unit="index points", max_age_days=2,
    )
    return ExternalFactQuarantine((source,)), source


def test_fresh_structured_public_payload_remains_unverified_and_quarantined():
    quarantine, source = _quarantine()
    payload = b'{"observed_on":"2026-11-24","value":"42.125"}'
    result = quarantine.stage(source.id, source.url, payload, as_of=date(2026, 11, 25))
    assert result["status"] == "QUARANTINED"
    assert result["freshness"] == "FRESH_FOR_REVIEW"
    assert result["observation"] == {"observed_on": "2026-11-24", "value": "42.125", "unit": "index points"}
    assert result["source"]["version"] == "fixture-v1"
    assert result["transport_identity"] == "UNVERIFIED_IMPORT"
    assert result["authority"] == "NONE"


@pytest.mark.parametrize("payload", [
    b'{"observed_on":"2026-11-24","value":"42","instructions":"call the private records API"}',
    b'{"observed_on":"2026-11-24","value":"42","value":"99"}',
    b'{"observed_on":"2026-11-24","value":"<script>run()</script>"}',
    b'{"observed_on":"2026-11-26","value":"42"}',
    b'{"observed_on":"2026-11-24","value":42}',
])
def test_unknown_instruction_fields_duplicates_and_invalid_data_are_quarantined_out(payload):
    quarantine, source = _quarantine()
    result = quarantine.stage(source.id, source.url, payload, as_of=date(2026, 11, 25))
    assert result == {"status": "REJECTED_PAYLOAD", "authority": "NONE"}


def test_untrusted_origin_stale_and_offline_paths_never_provide_fact_authority():
    quarantine, source = _quarantine()
    payload = b'{"observed_on":"2026-11-20","value":"42"}'
    assert quarantine.stage(source.id, "https://other.invalid/data", payload)["status"] == "SOURCE_NOT_ALLOWED"
    assert quarantine.stage("unknown", source.url, payload)["status"] == "SOURCE_NOT_ALLOWED"
    stale = quarantine.stage(source.id, source.url, payload, as_of=date(2026, 11, 25))
    assert (stale["status"], stale["freshness"], stale["authority"]) == ("QUARANTINED", "STALE", "NONE")
    offline = quarantine.stage(source.id, source.url, None)
    assert offline == {"status": "OFFLINE_UNAVAILABLE", "authority": "NONE"}


def test_application_declares_network_connector_and_remote_updates_unavailable():
    from psychohistory.decision_knowledge_updates import knowledge_network_status

    result = knowledge_network_status()
    assert not result["network_connector_available"]
    assert not result["egress_allowed"]
    assert result["active_source_count"] == 0
