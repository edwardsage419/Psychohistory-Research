import asyncio

from psychohistory.decision_extensions import AdapterPermit, AdapterSpec, request_candidates


class SyntheticAdapter:
    def __init__(self, *, free=True, delay=0, answer=None):
        self.spec = AdapterSpec(identity="fixture", version="1.0", capability="evidence", mode="external",
                                privacy_scope="fictional excerpt", free_confirmed=free,
                                maximum_input_bytes=48, timeout_ms=10)
        self.delay = delay
        self.answer = answer
        self.calls = 0

    async def propose(self, query):
        self.calls += 1
        await asyncio.sleep(self.delay)
        return self.answer


def test_evidence_adapter_permission_and_result_validation():
    proposal = {"field": "evidence", "value": "候选来源", "source": "虚构目录"}
    adapter = SyntheticAdapter(answer=[proposal])
    permit = AdapterPermit("evidence", "fixture", True, "fictional query", "1.0")
    assert asyncio.run(request_candidates(None, "evidence", "fictional query", permit))["status"] == "USER_SOURCE_REQUIRED"
    assert asyncio.run(request_candidates(adapter, "evidence", "unapproved query", permit))["status"] == "PERMISSION_REQUIRED"
    assert asyncio.run(request_candidates(adapter, "evidence", "fictional query",
                                          AdapterPermit("evidence", "fixture", True, "fictional query", "2.0"))
                       )["status"] == "PERMISSION_REQUIRED"
    assert adapter.calls == 0
    reply = asyncio.run(request_candidates(adapter, "evidence", "fictional query", permit))
    assert reply["status"] == "NEEDS_CONFIRMATION"
    assert reply["provider_id"] == "fixture"
    assert reply["proposals"][0]["source"] == proposal["source"]
    adapter.answer = [{"field": "execute", "value": "do something", "source": "fictional"}]
    assert asyncio.run(request_candidates(adapter, "evidence", "fictional query", permit))["status"] == "INVALID_RESULT"


def test_adapter_timeout_and_unconfirmed_cost_do_not_supply_evidence():
    permit = AdapterPermit("evidence", "fixture", True, "fictional query", "1.0")
    paid = SyntheticAdapter(free=False)
    assert asyncio.run(request_candidates(paid, "evidence", "fictional query", permit))["status"] == "PERMISSION_REQUIRED"
    assert not paid.calls
    slow = SyntheticAdapter(delay=0.1)
    assert asyncio.run(request_candidates(slow, "evidence", "fictional query", permit))["status"] == "TIMEOUT"


def test_v05_hub_receives_proposals_without_changing_the_active_question():
    from psychohistory.decision_v05 import DecisionHubV05

    query = "public fictional facts"
    adapter = SyntheticAdapter(answer=[{"field": "evidence", "value": "虚构档案", "source": "公开样例"}])
    hub = DecisionHubV05(adapters={"evidence": adapter})
    state = hub.start("我该现在改变安排，还是下周再决定？")["state"]
    reply = asyncio.run(hub.propose("evidence", query, AdapterPermit("evidence", "fixture", True, query, "1.0")))
    assert reply["status"] == "NEEDS_CONFIRMATION"
    assert state["evidence"] == [] and not state["confirmed"]
