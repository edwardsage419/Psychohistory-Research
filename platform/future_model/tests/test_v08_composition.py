from pathlib import Path
from subprocess import run

import pytest


KEY = b"synthetic verification key only 32+ bytes!"


def scope(*, exhaustive=True, revision=2, worlds=("quiet", "busy", "late", "unknown")):
    from psychohistory.decision_composition import CompositionScope

    return CompositionScope(
        session_instance="synthetic-session", authorization_epoch="test-epoch", evidence_epoch="evidence-1",
        revision=revision, domain_id="cash-and-start", domain_version="1",
        unit="CNY cents per week", horizon="three weeks",
        exhaustive=exhaustive, worlds=worlds,
    )


def port(domain, kind, rows, source="fixture@1"):
    from psychohistory.decision_composition import GroupedPort, ValueGroup

    return GroupedPort(
        scope=domain, kind=kind, method_version="fixture@1.0",
        source_versions=(source,),
        groups=tuple(ValueGroup(value=value, worlds=worlds) for value, worlds in rows),
    )


def test_join_resume_keeps_missing_worlds_and_never_crosses_labels():
    from psychohistory.decision_composition import advance_join, prepare_join

    domain = scope()
    threshold = port(domain, "threshold", [(100, ("quiet",)), (200, ("busy", "unknown")),
                                           (None, ("late",))])
    gains = port(domain, "gain", [(90, ("quiet",)), (200, ("busy",)), (500, ("late",))])
    plan = prepare_join(domain, threshold, gains)
    paused = advance_join(plan, domain, 0, signing_key=KEY)
    assert paused["conclusion"] == "UNKNOWN_GLOBAL"
    assert paused["not_calculated"] == ["quiet", "busy", "late"]
    assert paused["missing_evidence"] == ["unknown"]
    assert paused["pass_count_bounds"] == [0, 4]
    partial = advance_join(plan, domain, 2, signing_key=KEY, checkpoint=paused["checkpoint"],
                           stop_on_mixed=True)
    assert partial["conclusion"] == "CONDITIONAL_MIXED"
    assert partial["pass"] == ["busy"]
    assert partial["fail"] == ["quiet"]
    assert partial["not_calculated"] == ["late"]
    assert partial["pass_count_bounds"] == [1, 3]
    complete = advance_join(plan, domain, 2, signing_key=KEY, checkpoint=partial["checkpoint"])
    assert complete["fail"] == ["quiet", "late"]
    assert complete["missing_evidence"] == ["unknown"]
    assert complete["not_calculated"] == []
    assert complete["pass_count_bounds"] == [1, 2]
    assert complete["fail_count_bounds"] == [2, 3]
    assert complete["authority"] == "NONE"
    assert complete["checkpoint"] is None


def test_cursor_tampering_source_revision_and_authorization_fail_closed():
    from psychohistory.decision_composition import advance_join, prepare_join

    domain = scope()
    threshold = port(domain, "threshold", [(100, ("quiet", "busy"))])
    gains = port(domain, "gain", [(100, ("quiet",)), (150, ("busy",))])
    plan = prepare_join(domain, threshold, gains)
    partial = advance_join(plan, domain, 1, signing_key=KEY)
    assert partial["conclusion"] == "UNKNOWN_GLOBAL"
    checkpoint = partial["checkpoint"]
    changed_source = prepare_join(domain, threshold, gains.model_copy(update={"source_versions": ("gain@2",)}))
    for other_plan, current, supplied, key in (
        (plan, domain, {**checkpoint, "cursor": checkpoint["cursor"] + 1}, KEY),
        (plan, domain, checkpoint, b"other synthetic verification key!!"),
        (changed_source, domain, checkpoint, KEY),
        (plan, scope(revision=3), checkpoint, KEY),
        (plan, domain.model_copy(update={"authorization_epoch": "new-epoch"}), checkpoint, KEY),
        (plan, domain.model_copy(update={"evidence_epoch": "evidence-2"}), checkpoint, KEY),
        (plan, domain.model_copy(update={"session_instance": "other-session"}), checkpoint, KEY),
    ):
        with pytest.raises(ValueError):
            advance_join(other_plan, current, 1, signing_key=key, checkpoint=supplied)
    with pytest.raises(ValueError):
        advance_join(plan, domain, True, signing_key=KEY)


def test_untrusted_empty_or_overlapping_joint_support_cannot_publish():
    from psychohistory.decision_composition import advance_join, prepare_join

    domain = scope(exhaustive=False)
    plan = prepare_join(domain, port(domain, "threshold", [(1, ("quiet",))]),
                        port(domain, "gain", [(1, ("quiet",))]))
    assert advance_join(plan, domain, 4, signing_key=KEY) == {
        "version": "1.0.0", "authority": "NONE", "conclusion": "UNKNOWN_COVERAGE",
    }
    empty = scope(worlds=())
    plan = prepare_join(empty, port(empty, "threshold", []), port(empty, "gain", []))
    assert advance_join(plan, empty, 4, signing_key=KEY)["conclusion"] == "CONFLICT"
    domain = scope()
    with pytest.raises(ValueError):
        prepare_join(domain, port(domain, "threshold", [(1, ("quiet",)), (2, ("quiet",))]),
                     port(domain, "gain", [(1, ("quiet",))]))
    with pytest.raises(ValueError):
        prepare_join(domain, port(domain, "threshold", [(1, ("quiet",))]),
                     port(domain, "gain", [(None, ("quiet",))]))
    with pytest.raises(ValueError):
        prepare_join(domain, port(scope(revision=3), "threshold", [(1, ("quiet",))]),
                     port(domain, "gain", [(1, ("quiet",))]))


def test_competing_model_keeps_possible_but_uncomputed_explanation():
    from psychohistory.decision_composition import Hypothesis, ModelResult, compare_hypotheses

    domain = scope(worlds=("quiet", "busy"))
    alpha = Hypothesis(method_version="alpha@1", scope=domain, source_versions=("alpha-source@1",),
                       results=(ModelResult(world="quiet", winners=("stay",)),
                                ModelResult(world="busy", winners=("move",))))
    beta = Hypothesis(method_version="beta@1", scope=domain, source_versions=("beta-source@1",),
                      results=(ModelResult(world="quiet", winners=("stay", "move")),
                               ModelResult(world="busy", winners=None)))
    result = compare_hypotheses(domain, ("stay", "move"), (alpha, beta))
    assert result["conclusion"] == "PARTIAL_COVERAGE"
    assert result["rows"] == [{"world": "quiet", "models": ["alpha@1", "beta@1"],
                               "common": ["stay"], "possible": ["stay", "move"]}]
    assert result["missing"] == {"busy": ["beta@1"]}
    assert result["common"] is None and result["possible"] is None
    beta = beta.model_copy(update={"results": beta.results[:1]})
    result = compare_hypotheses(domain, ("stay", "move"), (alpha, beta))
    assert result["conclusion"] == "CONDITIONAL_NO_COMMON"
    assert result["common"] == [] and result["possible"] == ["stay", "move"]
    assert result["authority"] == "NONE"


def test_isolated_replay_uses_open_python_entry_and_matches_fixed_oracle():
    import json
    import sys

    path = Path(__file__).resolve().parents[1] / "scripts" / "v08_composition_replay.py"
    result = run([sys.executable, str(path)], capture_output=True, text=True, check=True)
    report = json.loads(result.stdout)
    assert report == {"authority": "NONE", "joint_cases": 1024, "hypothesis_cases": 225}


def test_composition_metadata_is_discoverable_only_as_isolated_research():
    from psychohistory.decision_candidates import default_candidate_registry
    from psychohistory.decision_v05 import v05_registry

    candidates = default_candidate_registry()
    executable = {method.key for method in v05_registry().methods()}
    for key in ("conditional_model_coverage@1.0.0", "joint_threshold_composition@1.0.0"):
        row = candidates.describe(key)
        assert (row["admission"], row["authority"]) == ("NOT_ADMITTED", "NONE")
        assert row["replay"].endswith("v08_composition_replay.py")
        assert key not in executable


def test_checkpoint_support_beyond_javascript_integer_range_is_lossless():
    import json

    from psychohistory.decision_composition import advance_join, prepare_join

    world_ids = tuple(f"world-{i}" for i in range(80))
    domain = scope(worlds=world_ids)
    threshold = port(domain, "threshold", [(2, world_ids[70:]), (3, world_ids[:70])])
    gains = port(domain, "gain", [(2, world_ids)])
    plan = prepare_join(domain, threshold, gains)
    prefix = advance_join(plan, domain, 1, signing_key=KEY)
    assert prefix["fail"] == list(world_ids[:70])
    checkpoint = json.loads(json.dumps(prefix["checkpoint"]))
    assert isinstance(checkpoint["failed"], str) and int(checkpoint["failed"], 16) == 2**70 - 1
    result = advance_join(plan, domain, 1, signing_key=KEY, checkpoint=checkpoint)
    assert result["pass"] == list(world_ids[70:])
    assert result["fail"] == list(world_ids[:70])
