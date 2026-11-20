from decimal import Decimal
import pytest

from psychohistory.decision_registry import Context, default_registry
from psychohistory.decision_state import DecisionState, Objective, Option, Quantity, Weight


def method(model_id):
    return default_registry().get(model_id, "1.0.0")


def bounds(lower, upper=None):
    return Weight(lower=Decimal(lower), upper=Decimal(lower if upper is None else upper))


def score(lower, upper=None, *, unit="utility", kind="synthetic", source="人工核对样例", horizon=None):
    values = bounds(lower, upper).model_dump() if lower is not None else {}
    return Quantity(**values, unit=unit, kind=kind, source=source, horizon=horizon)


def context(a=None, b=None, **changes):
    a = a if a is not None else [score(".8"), score(".4")]
    b = b if b is not None else [score(".5"), score(".8")]
    ids = ["growth", "resources", "time"][:len(a)]
    objectives = [
        Objective(id=key, label=key, unit="utility", direction="max") for key in ids
    ]
    options = (
        Option(id="a", label="方案 A", scores=dict(zip(ids, a, strict=True))),
        Option(id="b", label="方案 B", scores=dict(zip(ids, b, strict=True))),
    )
    defaults = dict(
        decision_id="a" * 32,
        revision=1,
        question="方案 A 或方案 B 的长期权衡如何？",
        confirmed=True,
        constraints_confirmed=True,
        deadline="12个月",
        options=options,
        objectives=objectives,
        weights_confirmed=True,
        weights={"growth": bounds(".60", ".65"), "resources": bounds(".35", ".40")},
        score_basis="同一基数效用刻度，允许补偿并确认权重含义",
        score_dependence="rectangle",
        score_dependence_source="人工声明可共同达到所有分数端点",
        score_transform="identity",
        shared_offsets={},
        shared_offset_dependence="unknown",
    )
    return Context(DecisionState(**(defaults | changes)), feasible=options)


def run(model_id, ctx):
    registered = method(model_id)
    assert registered.validate(ctx) == []
    return registered.execute(ctx)


def test_comparability_audit_surfaces_unit_mismatches_and_unknown_evidence():
    result = run("comparability", context(b=[score(".5", unit="USD"), score(None, kind="unknown")]))
    assert result["status"] == "UNKNOWN"
    assert {item["objective"] for item in result["score_gaps"]} == {"growth", "resources"}
    assert all(isinstance(gap, str) for gap in result["gaps"])


def test_a_score_with_an_inconsistent_effective_horizon_makes_the_objective_unknown():
    ctx = context(b=[score(".5", horizon="3个月"), score(".8")])
    assert run("comparability", ctx)["status"] == "UNKNOWN"
    assert run("pareto", ctx)["pairs"][0]["relation"] == "UNKNOWN"
    assert method("weight_sensitivity").validate(ctx)
    assert method("c034_joint_robustness").validate(ctx)


def test_distinct_objective_horizons_allow_pareto_but_not_a_shared_utility_comparison():
    ctx = context(
        a=[score(".8", horizon="3个月"), score(".4")],
        b=[score(".5", horizon="3个月"), score(".8")],
    )
    assert run("comparability", ctx)["status"] == "COMPARABLE_BY_OBJECTIVE"
    assert run("pareto", ctx)["pairs"][0]["relation"] == "INCOMPARABLE"
    assert method("weight_sensitivity").validate(ctx)
    assert method("c034_joint_robustness").validate(ctx)


def test_pareto_preserves_tradeoffs_with_opposite_objective_directions():
    ctx = context(a=[score(".8"), score(".9")], b=[score(".5"), score(".8")])
    ctx.state.objectives[1].direction = "min"
    result = run("pareto", ctx)
    assert result["frontier"] == ["a", "b"]
    assert result["pairs"][0]["relation"] == "INCOMPARABLE"


def test_pareto_excludes_only_a_provably_dominated_feasible_option():
    ctx = context(a=[score(".8", ".9"), score(".4", ".6")], b=[score(".5", ".8"), score(".3")])
    rejected = Option(id="rejected", label="已排除", scores={})
    ctx.state.options = [*ctx.feasible, rejected]
    result = run("pareto", ctx)
    assert result["frontier"] == ["a"]
    assert result["pairs"][0]["relation"] == "A_DOMINATES"
    assert "rejected" not in str(result)


def test_pareto_keeps_overlap_unresolved_when_the_order_can_change():
    result = run("pareto", context(a=[score(".4", ".8"), score(".8")], b=[score(".5"), score(".8")]))
    assert result["status"] == "UNKNOWN"
    assert result["frontier"] == ["a", "b"]
    assert result["pairs"][0]["relation"] == "UNRESOLVED"


@pytest.mark.parametrize(
    "changes",
    [
        {"weights_confirmed": False},
        {"score_basis": None},
        {"weights": {"growth": bounds(".6", ".7"), "resources": bounds(".6", ".7")}},
        {"weights": {"growth": bounds(".6")}},
    ],
)
def test_weighted_methods_require_documented_confirmed_bounded_simplex(changes):
    ctx = context(**changes)
    assert method("weight_sensitivity").validate(ctx)
    assert method("c034_joint_robustness").validate(ctx)


def test_weight_sensitivity_reports_exact_reversal_threshold_and_weight_witnesses():
    ctx = context(weights={"growth": bounds(".3", ".7"), "resources": bounds(".3", ".7")})
    result = run("weight_sensitivity", ctx)
    pair = result["pairs"][0]
    assert (pair["lower"], pair["upper"], pair["relation"]) == ("-0.19", "0.09", "UNRESOLVED")
    assert pair["threshold"] == {"objective": "growth", "value": "4/7"}
    assert pair["minimum"]["weights"] == {"growth": "0.3", "resources": "0.7"}
    assert pair["maximum"]["weights"] == {"growth": "0.7", "resources": "0.3"}
    assert ctx.state.weights["growth"].lower == Decimal(".3")
    assert ctx.state.weights["growth"].upper == Decimal(".7")


def test_weight_sensitivity_uses_the_joint_sum_constraint_with_three_objectives():
    ctx = context(
        a=[score("1"), score("1"), score("0")],
        b=[score("0"), score("0"), score("1")],
        weights={"growth": bounds(".2", ".9"), "resources": bounds(".3", ".9"), "time": bounds(".1", ".8")},
    )
    pair = run("weight_sensitivity", ctx)["pairs"][0]
    assert (pair["lower"], pair["upper"], pair["relation"]) == ("0", "0.8", "UNRESOLVED")
    assert pair["minimum"]["weights"] == {"growth": "0.2", "resources": "0.3", "time": "0.5"}


def test_weight_sensitivity_applies_declared_clipping_to_shared_nominal_scores():
    ctx = context(
        a=[score("1.3"), score(".4")],
        b=[score(".8"), score(".5")],
        weights={"growth": bounds(".6"), "resources": bounds(".4")},
        score_dependence="shared_additive",
        score_transform="clip_01",
        shared_offsets={"growth": bounds("-.3", ".3"), "resources": bounds("-.3", ".3")},
    )
    pair = run("weight_sensitivity", ctx)["pairs"][0]
    assert (pair["lower"], pair["upper"], pair["relation"]) == ("0.08", "0.08", "A_STRICT")


@pytest.mark.parametrize(
    ("e", "lower", "upper", "relation"),
    [
        (".005", "0.01", "0.065", "A_STRICT"),
        (".01", "0", "0.075", "UNRESOLVED"),
        (".03", "-0.04", "0.115", "UNRESOLVED"),
    ],
)
def test_rectangular_joint_uncertainty_distinguishes_exact_tie_from_strict_preference(
    e, lower, upper, relation
):
    radius = Decimal(e)

    def measured(center):
        point = Decimal(center)
        return score(point - radius, point + radius)

    ctx = context(a=[measured(".8"), measured(".4")], b=[measured(".5"), measured(".8")])
    result = run("c034_joint_robustness", ctx)
    pair = result["pairs"][0]
    assert (pair["lower"], pair["upper"], pair["relation"]) == (lower, upper, relation)
    assert pair["bounds"] == "exact"
    assert pair["score_radius_threshold"] == {"preferred": "a", "strict_upper": "0.01"}
    assert pair["nominal_baseline"] == {
        "weights": {"growth": "0.625", "resources": "0.375"},
        "difference": "0.0375",
    }
    if e == ".01":
        assert pair["minimum"] == {
            "weights": {"growth": "0.6", "resources": "0.4"},
            "a_scores": {"growth": "0.79", "resources": "0.39"},
            "b_scores": {"growth": "0.51", "resources": "0.81"},
        }


def test_rectangular_joint_uncertainty_accounts_for_asymmetric_scores_and_weight_limits():
    ctx = context(
        a=[score(".80", ".85"), score(".15", ".25")],
        b=[score(".55", ".65"), score(".80", ".85")],
        weights={"growth": bounds(".50", ".65"), "resources": bounds(".40", ".50")},
    )
    pair = run("c034_joint_robustness", ctx)["pairs"][0]
    assert (pair["lower"], pair["upper"], pair["relation"]) == ("-0.275", "-0.04", "B_STRICT")
    assert pair["maximum"]["weights"] == {"growth": "0.6", "resources": "0.4"}


def test_perfect_center_scores_cannot_fix_a_weight_interval_that_straddles_the_threshold():
    ctx = context(weights={"growth": bounds(".55", ".65"), "resources": bounds(".35", ".45")})
    pair = run("c034_joint_robustness", ctx)["pairs"][0]
    assert (pair["lower"], pair["upper"]) == ("-0.015", "0.055")
    assert pair["information_gap"] == "WEIGHT_CAN_REVERSE_AT_CENTER_SCORES"


@pytest.mark.parametrize(
    "changes",
    [
        {"score_dependence": "unknown"},
        {"score_dependence_source": None},
        {"score_transform": "unknown"},
        {"score_dependence": "shared_additive"},
    ],
)
def test_c034_does_not_infer_dependence_transformation_or_missing_shared_offsets(changes):
    assert method("c034_joint_robustness").validate(context(**changes))


def test_c034_preserves_unknown_score_bounds():
    incomplete = score(".8")
    incomplete.upper = None
    assert method("c034_joint_robustness").validate(context(a=[incomplete, score(".4")]))


def test_shared_unclipped_offsets_cancel_even_with_unknown_cross_objective_dependence():
    ctx = context(
        score_dependence="shared_additive",
        shared_offsets={"growth": bounds("-.3", ".3"), "resources": bounds("-.3", ".3")},
    )
    pair = run("c034_joint_robustness", ctx)["pairs"][0]
    assert (pair["lower"], pair["upper"], pair["relation"]) == ("0.02", "0.055", "A_STRICT")
    assert pair["bounds"] == "exact"
    assert "offsets" not in pair["minimum"]


def test_shared_clipping_builds_the_c034_reversal_witness_when_offsets_form_a_product():
    ctx = context(
        score_dependence="shared_additive",
        score_transform="clip_01",
        shared_offsets={"growth": bounds("-.3", ".3"), "resources": bounds("-.3", ".3")},
        shared_offset_dependence="rectangle",
    )
    pair = run("c034_joint_robustness", ctx)["pairs"][0]
    assert (pair["lower"], pair["upper"], pair["relation"]) == ("-0.04", "0.09", "UNRESOLVED")
    assert pair["minimum"]["weights"]["growth"] == "0.6"
    assert pair["minimum"]["offsets"] == {"growth": "0.3", "resources": "-0.3"}
    assert pair["minimum"]["a_scores"] == {"growth": "1", "resources": "0.1"}
    assert pair["minimum"]["b_scores"] == {"growth": "0.8", "resources": "0.5"}


def test_shared_clipping_searches_interior_breakpoints():
    ctx = context(
        a=[score(".75"), score(".4")],
        b=[score(".25"), score(".8")],
        weights={"growth": bounds(".6"), "resources": bounds(".4")},
        score_dependence="shared_additive",
        score_transform="clip_01",
        shared_offsets={"growth": bounds("-.9", ".9"), "resources": bounds("0")},
        shared_offset_dependence="rectangle",
    )
    pair = run("c034_joint_robustness", ctx)["pairs"][0]
    assert (pair["lower"], pair["upper"]) == ("-0.16", "0.14")
    assert pair["maximum"]["offsets"]["growth"] == "-0.25"


def test_shared_clipping_with_unknown_offset_dependence_does_not_claim_feasible_witnesses():
    ctx = context(
        score_dependence="shared_additive",
        score_transform="clip_01",
        shared_offsets={"growth": bounds("-.3", ".3"), "resources": bounds("-.3", ".3")},
    )
    result = run("c034_joint_robustness", ctx)
    pair = result["pairs"][0]
    assert result["status"] == "UNKNOWN"
    assert (pair["lower"], pair["upper"], pair["relation"]) == ("-0.04", "0.09", "UNKNOWN")
    assert pair["bounds"] == "outer"
    assert "minimum" not in pair
    assert "maximum" not in pair
    assert result["gaps"]


def test_a_positive_clipping_outer_bound_still_proves_strict_preference():
    ctx = context(
        score_dependence="shared_additive",
        score_transform="clip_01",
        shared_offsets={"growth": bounds("-.05", ".05"), "resources": bounds("-.05", ".05")},
    )
    result = run("c034_joint_robustness", ctx)
    pair = result["pairs"][0]
    assert result["leaders"] == ["a"]
    assert (pair["lower"], pair["upper"], pair["relation"], pair["bounds"]) == ("0.02", "0.055", "A_STRICT", "outer")
    assert "minimum" not in pair
