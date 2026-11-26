from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from datetime import date
from decimal import Decimal

from threading import Event

from psychohistory import decision_knowledge_updates as knowledge
from psychohistory.decision_feasibility import check_constraint
from psychohistory.decision_state import Constraint, Quantity


TODAY = date(2026, 11, 25)
SOURCE = knowledge.PublicFactSource(
    id="synthetic-public-fee",
    url="https://example.invalid/public-fee.json",
    publisher="Synthetic fee publisher",
    version="fixture-v1",
    licence="Synthetic fixture",
    unit="CNY",
    max_age_days=2,
)
TEN = b'{"observed_on":"2026-11-25","value":"10.00"}'
ELEVEN = b'{"observed_on":"2026-11-25","value":"11.00"}'


def _scope():
    return knowledge.ParameterScope(
        subject="Synthetic course",
        metric="published fee",
        unit="CNY",
        horizon="One purchase",
        scenario="Published terms",
        purpose="temporary_analysis",
    )


def _qualify(cache, scope, verify=lambda observation, policy: True):
    return cache.qualify(SOURCE.id, scope, epoch="decision-v1", verify=verify, as_of=TODAY)


def _resolve(cache, ticket, scope, *, epoch="decision-v1", as_of=TODAY):
    return cache.resolve(ticket, scope, epoch=epoch, as_of=as_of)


def test_staged_public_observation_requires_separate_review_before_native_c028_can_use_it():
    cache = knowledge.PublicFactCache((SOURCE,))
    scope = _scope()
    staged = cache.stage(SOURCE.id, SOURCE.url, TEN, as_of=TODAY)
    assert staged["authority"] == "NONE"
    assert _qualify(cache, scope, verify=lambda observation, policy: False) is None
    ticket = _qualify(cache, scope, verify=lambda observation, policy: (
        observation["source"]["licence"] == "Synthetic fixture"
        and observation["observation"]["value"] == "10.00"
        and policy == scope
    ))
    assert _resolve(cache, "not-a-host-ticket", scope) is None
    parameter = _resolve(cache, ticket, scope)
    assert parameter.value == Decimal("10.00")
    limit = Constraint(id="fees", label="Fee cap", unit="CNY", operator="<=", threshold="10",
                       source="Synthetic fee limit", horizon=scope.horizon)
    value = Quantity(lower=parameter.value, upper=parameter.value, unit=scope.unit,
                     source=parameter.source_url, kind="fact", horizon=scope.horizon)
    assert check_constraint(limit, value, scope.horizon)[0] == "CERTAIN_PASS"


def test_parameter_requires_exact_scope_epoch_freshness_and_current_source_identity():
    scope = _scope()
    cache = knowledge.PublicFactCache((SOURCE,))
    cache.stage(SOURCE.id, SOURCE.url, TEN, as_of=TODAY)
    ticket = _qualify(cache, scope)

    for field in ("subject", "metric", "unit", "horizon", "scenario", "purpose"):
        assert _resolve(cache, ticket, replace(scope, **{field: "different"})) is None
    assert _resolve(cache, ticket, scope, epoch="decision-v2") is None
    assert _resolve(cache, ticket, scope, as_of=date(2026, 11, 27)).value == Decimal("10")
    assert _resolve(cache, ticket, scope, as_of=date(2026, 11, 28)) is None

    cache.set_source(replace(SOURCE, version="fixture-v2"))
    cache.stage(SOURCE.id, SOURCE.url, TEN, as_of=TODAY)
    assert _resolve(cache, ticket, scope) is None
    revised = _qualify(cache, scope)
    assert _resolve(cache, revised, scope).source_version == "fixture-v2"
    cache.withdraw(SOURCE.id)
    assert _resolve(cache, revised, scope) is None
    assert cache.stage(SOURCE.id, SOURCE.url, TEN, as_of=TODAY)["status"] == "SOURCE_NOT_ALLOWED"


def test_cache_rejects_revoked_or_superseded_receipt_even_after_aba_restore():
    scope = _scope()
    cache = knowledge.PublicFactCache((SOURCE,))
    cache.stage(SOURCE.id, SOURCE.url, TEN, as_of=TODAY)
    ticket = _qualify(cache, scope)
    cache.stage(SOURCE.id, SOURCE.url, ELEVEN, as_of=TODAY)
    cache.stage(SOURCE.id, SOURCE.url, TEN, as_of=TODAY)
    assert _resolve(cache, ticket, scope) is None

    ticket = _qualify(cache, scope)
    cache.revoke(ticket)
    assert _resolve(cache, ticket, scope) is None
    assert _resolve(cache, _qualify(cache, scope), scope).value == Decimal("10")


def test_fetch_is_opt_in_uses_only_allowlisted_url_and_retains_offline_freshness(monkeypatch):
    calls = []

    def transport(url):
        calls.append(url)
        if len(calls) == 1:
            return TEN
        raise TimeoutError("fixture offline")

    monkeypatch.setattr(knowledge, "_read_public_json", transport, raising=False)
    cache = knowledge.PublicFactCache((SOURCE,))
    assert cache.fetch(SOURCE.id, as_of=TODAY)["status"] == "NETWORK_DISABLED"
    assert cache.fetch("other", allow_network=True, as_of=TODAY)["status"] == "SOURCE_NOT_ALLOWED"
    assert calls == []
    live = cache.fetch(SOURCE.id, allow_network=True, as_of=TODAY)
    assert live["transport_identity"] == "HTTPS_RETRIEVED"
    assert live["authority"] == "NONE"
    offline = cache.fetch(SOURCE.id, allow_network=True, as_of=date(2026, 11, 28))
    assert calls == [SOURCE.url, SOURCE.url]
    assert (offline["availability"], offline["freshness"]) == ("CACHED_OFFLINE", "STALE")
    assert cache.cached(SOURCE.id, as_of=TODAY)["freshness"] == "FRESH_FOR_REVIEW"


def test_observation_older_than_current_cache_keeps_verified_current_snapshot():
    cache = knowledge.PublicFactCache((SOURCE,))
    scope = _scope()
    cache.stage(SOURCE.id, SOURCE.url, TEN, as_of=TODAY)
    ticket = _qualify(cache, scope)
    stale = b'{"observed_on":"2026-11-24","value":"90"}'
    assert cache.stage(SOURCE.id, SOURCE.url, stale, as_of=TODAY)["status"] == "OLDER_OBSERVATION"
    assert cache.cached(SOURCE.id, as_of=TODAY)["observation"]["value"] == "10.00"
    assert _resolve(cache, ticket, scope).value == Decimal("10.00")


def test_cached_local_index_rechecks_referenced_bytes_before_search_and_method_use(tmp_path):
    from pathlib import Path
    import shutil

    from psychohistory.decision_knowledge import MANIFEST_PATH, POLICY_PATH, KnowledgeIndex, discover_knowledge

    source = Path("research/decision_methods/C028_INTERVAL_HARD_CONSTRAINT_FEASIBILITY_2026-11-20.md")
    root = Path(__file__).resolve().parents[3]
    for relative in (MANIFEST_PATH, POLICY_PATH, source):
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(root / relative, target)

    index = KnowledgeIndex(tmp_path)
    query = "CERTAIN_PASS point-estimate midpoint"
    assert index.search(query)["hits"]
    before, = discover_knowledge("判断方案是否违反底线", index=index)["methods"]
    assert before["source_status"] == "MATCHED_REFERENCE_ONLY"

    (tmp_path / source).write_text("changed after the index was built", encoding="utf-8")
    result = index.search(query)
    assert result["hits"] == []
    assert result["omitted_stale_hits"] == 1
    after, = discover_knowledge("判断方案是否违反底线", index=index)["methods"]
    assert after["source_status"] == "REVIEW_REQUIRED"
    assert after["sources"][0]["current_verification"] == "CHANGED"
    assert after["sources"][0]["historical_status"] == "MATCH"
    assert index.report()["snapshot_scope"] == "INDEX_BUILD_TIME"


def test_late_failed_network_request_does_not_reuse_a_reinstalled_source_cache(monkeypatch):
    started, finish = Event(), Event()

    def transport(url):
        started.set()
        if not finish.wait(5):
            raise RuntimeError("test did not release transport")
        raise TimeoutError("simulated loss of connection")

    monkeypatch.setattr(knowledge, "_read_public_json", transport)
    cache = knowledge.PublicFactCache((SOURCE,))
    with ThreadPoolExecutor(max_workers=1) as worker:
        pending = worker.submit(cache.fetch, SOURCE.id, allow_network=True, as_of=TODAY)
        try:
            assert started.wait(5)
            cache.withdraw(SOURCE.id)
            cache.set_source(SOURCE)
            cache.stage(SOURCE.id, SOURCE.url, ELEVEN, as_of=TODAY)
        finally:
            finish.set()
        assert pending.result(timeout=5)["status"] == "SOURCE_CHANGED"
    assert cache.cached(SOURCE.id, as_of=TODAY)["observation"]["value"] == "11.00"
