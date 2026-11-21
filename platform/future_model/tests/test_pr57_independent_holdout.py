"""PR #57: independently authored engineering holdout against evidence promotion.

These fictional inputs are not derived from the Codex development fixtures.
Original numerical reference is a separate Fraction-based joint-event enumeration.
A passing run establishes engineering behavior, not empirical scientific validity.
"""
from fractions import Fraction as F

from psychohistory.decision_registry import Context
from psychohistory.decision_state import Option, Quantity, Scenario
from psychohistory.decision_v05 import DecisionStateV05
from psychohistory.decision_voi import InformationInput, METHODS


def _probability(numerator, denominator=10, *, kind="fact", source="fictional self-report"):
    value = F(numerator, denominator)
    return {"lower": str(value), "upper": str(value), "kind": kind, "source": source}


def _quantity(amount, *, kind, source="fictional self-report"):
    return Quantity(lower=str(amount), upper=str(amount), unit="common utility",
                    horizon="common horizon", kind=kind, source=source)


def _context(kind="fact", receipt=None, *, cost="0.3", only_one=False):
    actions = (Option(id="safe", label="Safe"), Option(id="risky", label="Risky"))
    outcomes = (
        Scenario(id="wet", label="Wet", kind=kind, source="fictional self-report",
                 utilities={"safe": _quantity(4, kind=kind), "risky": _quantity(9, kind=kind)}),
        Scenario(id="dry", label="Dry", kind=kind, source="fictional self-report",
                 utilities={"safe": _quantity(4, kind=kind), "risky": _quantity(-1, kind=kind)}),
    )
    info = InformationInput(
        signals=[{"id": "alert", "label": "Alert"}, {"id": "clear", "label": "Clear"}],
        prior={"wet": _probability(3, kind=kind), "dry": _probability(7, kind=kind)},
        likelihoods={
            "wet": {"alert": _probability(8, kind=kind), "clear": _probability(2, kind=kind)},
            "dry": {"alert": _probability(2, kind=kind), "clear": _probability(8, kind=kind)},
        },
        cost=_quantity(cost, kind=kind), unrestricted_actions=True,
        action_source="fictional action scope", timing_basis="simultaneous and no delay",
        verification_source=receipt,
    )
    state = DecisionStateV05(
        decision_id="e" * 32, revision=1, question="Fictional choice with uncertain signal",
        deadline="common horizon", options=list(actions), scenarios=list(outcomes),
        scenario_basis="fixed common cardinal utility", information=info,
    )
    return Context(state, actions[:1] if only_one else actions)


def _run(ctx):
    method = next(m for m in METHODS if m.model_id == "voi_point")
    assert method.validate(ctx) == []
    return method.execute(ctx)


def _independent_event_enumeration(cost):
    prior = {"wet": F(3, 10), "dry": F(7, 10)}
    likelihood = {"wet": {"alert": F(4, 5), "clear": F(1, 5)},
                  "dry": {"alert": F(1, 5), "clear": F(4, 5)}}
    utility = {"safe": {"wet": F(4), "dry": F(4)},
               "risky": {"wet": F(9), "dry": F(-1)}}
    baseline = max(sum(prior[s] * utility[a][s] for s in prior)
                   for a in utility)
    informed = sum(max(sum(prior[s] * likelihood[s][z] * utility[a][s]
                           for s in prior) for a in utility)
                   for z in ("alert", "clear"))
    return baseline, informed, informed - baseline - F(cost)


def test_holdout_unseen_joint_event_arithmetic():
    baseline, informed, net = _independent_event_enumeration("0.3")
    assert (baseline, informed, net) == (F(4), F(9, 2), F(1, 5))
    actual = _run(_context(kind="synthetic"))
    assert F(actual["baseline_value"]) == baseline
    assert F(actual["information_value"]) == informed
    assert F(actual["net_value"]) == net
    assert actual["evidence_status"] == "SYNTHETIC"


def test_holdout_fabricated_url_cannot_upgrade_claim_to_verified():
    result = _run(_context(receipt="https://example.invalid/independent-audit-passed"))
    assert result["evidence_status"] == "USER_ATTESTED"
    assert "没有独立核实" in result["summary"]
    assert "VERIFIED" not in result["summary"]


def test_holdout_user_receipt_absent_keeps_conditional_status():
    assert _run(_context(receipt=None))["evidence_status"] == "CONDITIONAL"


def test_holdout_pretend_external_receipt_does_not_override_synthetic():
    assert _run(_context(kind="synthetic", receipt="claimed independent audit"))["evidence_status"] == "SYNTHETIC"


def test_holdout_assumption_is_not_verified_by_user_receipt():
    ctx = _context(receipt="user has checked values")
    ctx.state.information.cost.kind = "assumption"
    assert _run(ctx)["evidence_status"] == "CONDITIONAL"


def test_holdout_blank_receipt_cannot_upgrade_claim():
    ctx = _context(receipt="user has checked values")
    ctx.state.information.verification_source = "    "
    assert _run(ctx)["evidence_status"] == "CONDITIONAL"


def test_holdout_invalid_source_is_rejected_even_with_receipt():
    ctx = _context(receipt="user has checked values")
    ctx.state.information.cost.source = ""
    method = next(m for m in METHODS if m.model_id == "voi_point")
    assert method.validate(ctx)


def test_holdout_net_value_cost_threshold_and_no_action_inference():
    assert _run(_context(kind="synthetic", cost="0.5"))["decision"] == "TIE"
    negative = _run(_context(kind="synthetic", cost="0.8"))
    assert negative["decision"] == "NEGATIVE"
    assert F(negative["net_value"]) == F(-3, 10)
    restricted = _run(_context(kind="synthetic", only_one=True))
    assert F(restricted["net_value"]) == F(-3, 10)
    assert restricted["evsi"] == "0"


def test_holdout_relabeling_signals_preserves_expected_value():
    ctx = _context(kind="synthetic")
    ctx.state.information.signals.reverse()
    result = _run(ctx)
    assert F(result["net_value"]) == F(1, 5)
    assert result["baseline_actions"] == ["safe"]
