from dataclasses import replace
from hashlib import sha1
from pathlib import Path
import json

import pytest

from psychohistory.decision_v05 import v05_registry


def candidate_registry():
    from psychohistory.decision_candidates import default_candidate_registry

    return default_candidate_registry()


def test_research_discovery_has_pinned_local_evidence_and_no_execution_authority():
    registry = candidate_registry()
    descriptions = registry.describe()
    assert {row["candidate_id"] for row in descriptions} >= {
        "C035", "C036", "robust_longitudinal_dp", "R258",
    }
    assert not ({item.key for item in v05_registry().methods()} & {row["key"] for row in descriptions})
    assert not hasattr(registry, "execute")
    project = Path(__file__).resolve().parents[3]
    for row in descriptions:
        assert row["admission"] == "NOT_ADMITTED"
        assert row["authority"] == "NONE"
        assert row["missing_admission"] and row["baseline"] and row["replay"]
        assert registry.describe(row["key"]) == row
        json.dumps(row)
        for source in row["sources"]:
            content = (project / source["path"]).read_bytes()
            git_bytes = b"blob " + str(len(content)).encode("ascii") + b"\0" + content
            assert sha1(git_bytes).hexdigest() == source["git_blob"]
            assert source["license"] == "UNVERIFIED"


def test_candidate_versions_are_explicit_and_can_be_replayed_without_replacing_history():
    from psychohistory.decision_candidates import CandidateRegistry

    registry = candidate_registry()
    initial = registry.get("C036@1.0.0")
    retained = replace(initial, version="1.1.0", title="新版研究候选")
    isolated = CandidateRegistry()
    isolated.register(initial)
    isolated.register(retained)
    assert isolated.versions("C036") == ("C036@1.0.0", "C036@1.1.0")
    assert isolated.describe("C036@1.0.0")["title"] == initial.title
    assert isolated.describe("C036@1.1.0")["title"] == retained.title
    with pytest.raises(ValueError):
        isolated.describe("C036")
    with pytest.raises(ValueError):
        isolated.register(initial)
    with pytest.raises(ValueError):
        isolated.register(replace(initial, version="latest"))


def test_candidate_and_execution_registries_reject_each_others_contracts():
    candidates, execution = candidate_registry(), v05_registry()
    with pytest.raises(ValueError):
        candidates.register(execution.methods()[0])
    with pytest.raises(ValueError):
        execution.register(candidates.get("C035@1.0.0"))
    with pytest.raises(ValueError):
        candidates.register(replace(candidates.get("C035@1.0.0"), missing_admission=()))


def test_discovery_results_are_safe_to_edit_locally_without_changing_registry():
    registry = candidate_registry()
    original = registry.describe("C035@1.0.0")
    edited = registry.describe("C035@1.0.0")
    edited["authority"] = "EXECUTE"
    edited["sources"][0]["git_blob"] = "0" * 40
    assert registry.describe("C035@1.0.0") == original
