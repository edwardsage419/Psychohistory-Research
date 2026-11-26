from types import SimpleNamespace

import pytest

from psychohistory.decision_conversation import ConversationHub
from psychohistory.decision_evidence import EvidenceLedger, confirm_claim, draft_claims
from psychohistory.decision_scenarios import BASIS_FIELD, PREFIX


PROMPT = (
    "我该选「方案甲」，还是「方案乙」？"
    "情景平常：方案甲得10分，方案乙得6分。情景变动：方案甲得0分，方案乙得7分。"
    "都比较未来30天，分差可比较，分数越高越好。"
)


def _confirm(hub, view, *, corrections=()):
    corrected = {item.claim_id for item in corrections}
    return hub.confirm(
        view["session_id"], view["revision"],
        claim_ids=[item["id"] for item in view["claims"]
                   if item["status"] == "PROVISIONAL" and item["id"] not in corrected],
        option_ids=[item["id"] for item in view["options"]],
        accept_context=True, corrections=corrections,
    )


def _turn(hub, view, text):
    return hub.turn(view["session_id"], view["revision"], text)


def _regret(view):
    return next((item for item in (view["analysis"] or {}).get("methods", [])
                 if item["model_id"] == "C029"), None)


def test_corrected_scenario_basis_requires_current_scores_for_every_previous_scenario():
    hub = ConversationHub()
    initial = _confirm(hub, hub.start(PROMPT))
    assert _regret(initial)["status"] == "EXECUTED"
    old_basis = next(item for item in initial["claims"] if item["field"] == BASIS_FIELD)

    pending = _turn(hub, initial, "都比较未来五年，分差可比较，分数越高越好。")
    replacement = next(item for item in pending["claims"]
                       if item["field"] == BASIS_FIELD and item["status"] == "PROVISIONAL")
    corrected = _confirm(hub, pending, corrections=[SimpleNamespace(
        claim_id=replacement["id"], supersedes=old_basis["id"],
    )])
    assert (_regret(corrected) or {}).get("status") != "EXECUTED"
    assert all(not scenario["utilities"] for scenario in corrected["state"]["scenarios"])

    refreshed = _confirm(hub, _turn(hub, corrected, "情景平常：方案甲得10分，方案乙得6分。"))
    assert (_regret(refreshed) or {}).get("status") != "EXECUTED"
    assert {scenario["label"] for scenario in refreshed["state"]["scenarios"]} == {"平常", "变动"}

    complete = _confirm(hub, _turn(hub, refreshed, "情景变动：方案甲得2分，方案乙得7分。"))
    assert _regret(complete)["status"] == "EXECUTED"
    assert len([item for item in complete["claims"] if item["field"].startswith(PREFIX)]) == 8


def test_equivalent_confirmed_scores_keep_both_sources_and_one_calculation_cell():
    hub = ConversationHub()
    original = _confirm(hub, hub.start(PROMPT))
    repeated = _confirm(hub, _turn(hub, original, "情景平常：方案乙得6分，方案甲得10分。"))
    assert _regret(repeated)["status"] == "EXECUTED"
    claims = [item for item in repeated["claims"]
              if item["field"] == f"{PREFIX}平常" and item["subject"] == "方案甲"]
    assert len({item["id"] for item in claims}) == 2
    assert all(item["status"] == "USER_CONFIRMED" for item in claims)
    row = next(item for item in repeated["state"]["scenarios"] if item["label"] == "平常")
    assert len(row["utilities"]) == 2

    conflict = _confirm(hub, _turn(hub, repeated, "情景平常：方案甲得11分，方案乙得6分。"))
    assert (_regret(conflict) or {}).get("status") != "EXECUTED"


def test_estimate_cannot_replace_a_hard_limit_after_an_explicit_revision():
    common = {"field": "cost_max", "subject": "", "unit": "yuan",
              "metadata": {"source_identity": "current_user", "channel": "user_self_report"}}
    hard = {**common, "kind": "fact", "role": "constraint", "value": "100", "source": "最多100元"}
    revised = {**common, "kind": "fact", "role": "revision", "value": "120", "source": "改成120元"}
    estimate = {**common, "kind": "estimate", "role": "estimate", "value": "150", "source": "可能要150元"}
    ledger = draft_claims(EvidenceLedger(), [hard, revised, estimate])
    old, revision, candidate = [entry.claim_id for entry in ledger.entries]
    ledger = confirm_claim(ledger, old)
    ledger = confirm_claim(ledger, revision, mode="correct", supersedes=old)
    with pytest.raises(ValueError, match="hard constraint"):
        confirm_claim(ledger, candidate, mode="correct", supersedes=revision)


def test_strict_hard_bound_revision_requires_an_explicit_comparator():
    common = {"field": "cost_max", "subject": "", "unit": "yuan", "kind": "fact",
              "metadata": {"source_identity": "current_user", "channel": "user_self_report"}}
    original = {**common, "role": "strict_constraint", "value": "100", "source": "费用低于100元"}
    ambiguous = {**common, "role": "revision", "value": "120", "source": "改成120元"}
    strict = {**common, "role": "revision", "value": "120", "source": "改为低于120元"}
    ledger = draft_claims(EvidenceLedger(), [original, ambiguous, strict])
    old, ambiguous_id, strict_id = [entry.claim_id for entry in ledger.entries]
    ledger = confirm_claim(ledger, old)
    with pytest.raises(ValueError, match="explicit comparison"):
        confirm_claim(ledger, ambiguous_id, mode="correct", supersedes=old)
    revised = confirm_claim(ledger, strict_id, mode="correct", supersedes=old)
    assert revised.trace()["groups"][0]["value"] == "120"


def test_first_scenario_basis_can_cover_previously_confirmed_unscoped_scores():
    hub = ConversationHub()
    initial = _confirm(hub, hub.start(PROMPT.split("都比较")[0]))
    assert (_regret(initial) or {}).get("status") != "EXECUTED"
    first_basis = _confirm(hub, _turn(hub, initial, "都比较未来30天，分差可比较，分数越高越好。"))
    assert _regret(first_basis)["status"] == "EXECUTED"
    repeated = _confirm(hub, _turn(hub, first_basis, "情景平常：方案乙得6分，方案甲得10分。"))
    assert _regret(repeated)["status"] == "EXECUTED"
