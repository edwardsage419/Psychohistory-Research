from dataclasses import replace

import pytest


def test_reviewed_local_parser_can_upgrade_and_rollback_without_changing_native_projection():
    from psychohistory.decision_conversation import ConversationHub
    from psychohistory.decision_parser_registry import ParserRegistry, ParserSpec

    def first(raw):
        return [{"source": raw.text[:1], "start": 0, "end": 1, "kind": "symbol"}]

    def second(raw):
        return [{"source": raw.text[1:3], "start": 1, "end": 3, "kind": "word"}]

    spec = ParserSpec("plain_example", "1.0.0", "Unicode code point example", ("tokens",))
    registry = ParserRegistry()
    registry.register(spec, first)
    registry.register(replace(spec, version="2.0.0"), second)
    question = "🙂我想比较方案甲和方案乙"
    plain = ConversationHub().start(question, current=True)
    registry.enable(spec.key)
    tested = ConversationHub(candidate_parsers=registry).start(question, current=True)
    turn = tested["semantic"]["turns"][0]
    assert tested["claims"] == plain["claims"]
    assert turn["alternative_parses"][0]["authority"] == "NONE"
    assert turn["alternative_parses"][0]["candidates"][0]["source"] == "🙂"
    assert turn["raw_turn"]["session_instance"] == tested["session_instance"]
    registry.enable("plain_example@2.0.0")
    upgraded = ConversationHub(candidate_parsers=registry).start(question, current=True)
    assert upgraded["semantic"]["turns"][0]["alternative_parses"][-1]["candidates"][0]["source"] == "我想"
    registry.disable(spec.key)
    registry.disable("plain_example@2.0.0")
    registry.enable(spec.key)
    rolled_back = ConversationHub(candidate_parsers=registry).start(question, current=True)
    assert [item["key"] for item in rolled_back["semantic"]["turns"][0]["alternative_parses"]] == [spec.key]


def test_invalid_alternative_anchor_cannot_be_used_as_a_claim():
    from psychohistory.decision_conversation import ConversationHub
    from psychohistory.decision_parser_registry import ParserRegistry, ParserSpec

    registry = ParserRegistry()
    spec = ParserSpec("example", "1.0.0", "Fixture", ("tokens",))
    registry.register(spec, lambda raw: [{"source": "伪造", "start": 0, "end": 2, "kind": "token"}])
    registry.enable(spec.key)
    response = ConversationHub(candidate_parsers=registry).start("🙂看来不行", current=True)
    [reading] = response["semantic"]["turns"][0]["alternative_parses"]
    assert reading["status"] == "INVALID_OUTPUT"
    assert not reading["candidates"]
    assert response["analysis"] is None


def test_new_math_method_dispatches_in_an_isolated_native_registry():
    from decimal import Decimal
    from psychohistory.decision_registry import Context, Method, default_registry
    from psychohistory.decision_v05 import DecisionHubV05, DecisionStateV05

    baseline = default_registry()
    isolated = default_registry()

    def validate(context):
        return [] if len(context.state.question) else ["question missing"]

    def execute(context):
        return {"constant": str(Decimal("0.1") + Decimal("0.2"))}

    method = Method("example_sum", "1.0.0", "Isolated exact sum", "synthetic fixture", "none", "sum",
                    "dimensionless", "decimal", "none", "test fixture", "no decision authority",
                    "independent 3/10", "constant 0", validate, execute)
    isolated.register(method)
    assert method.key not in {existing.key for existing in baseline.methods()}
    state = DecisionStateV05.model_validate(DecisionHubV05().start("虚构方案")["state"])
    registered = next(entry for entry in isolated.execution_order() if entry.key == method.key)
    context = Context(state=state)
    assert registered.validate(context) == []
    assert registered.execute(context) == {"constant": "0.3"}
    assert method.key not in {item.key for item in default_registry().methods()}


def test_explicit_active_manifest_switches_native_execution_and_can_roll_back():
    from dataclasses import replace

    from psychohistory.decision_feasibility import METHOD as gate
    from psychohistory.decision_registry import DecisionRegistry, Method
    from psychohistory.decision_v05 import DecisionHubV05

    lab = DecisionRegistry()
    lab.register(gate)
    method = Method("synthetic_add", "1.0.0", "Fixture sum", "synthetic", "none", "sum", "count",
                    "explicit fixture", "none", "test", "none", "independent integer sum", "zero",
                    lambda context: [], lambda context: {"summary": "1", "sum": 1}, depends_on=(gate.key,))
    new = replace(method, version="2.0.0", execute=lambda context: {"summary": "2", "sum": 2})
    dependent = replace(method, model_id="synthetic_dependent", depends_on=(new.key,))
    for entry in (method, new, dependent):
        lab.register(entry)

    base = [(entry.model_id, entry.version, entry.source_baseline) for entry in (gate, dependent)]

    def run(entry):
        manifest = (*base, (entry.model_id, entry.version, entry.source_baseline))
        hub = DecisionHubV05(registry=lab.for_release(manifest))
        state = hub.start("合成比较")["state"]
        state.update(confirmed=True, constraints_confirmed=True, deadline="本月",
                     objectives=[{"id": "benefit", "label": "收益", "unit": "分", "direction": "max"}],
                     options=[{"id": "left", "label": "甲"}, {"id": "right", "label": "乙"}])
        result = hub.analyze(state)
        return {row["model_id"]: row for row in result["methods"]}

    first = run(method)
    assert first["synthetic_add"]["result"]["sum"] == 1
    assert first["synthetic_dependent"]["status"] == "INELIGIBLE"
    upgraded = run(new)
    assert upgraded["synthetic_add"]["result"]["sum"] == 2
    assert upgraded["synthetic_dependent"]["status"] == "EXECUTED"
    assert run(method) == first
    with pytest.raises(ValueError, match="source"):
        lab.for_release((*base, (method.model_id, method.version, "0" * 40)))
    with pytest.raises(ValueError, match="gate"):
        lab.for_release(base[1:])
