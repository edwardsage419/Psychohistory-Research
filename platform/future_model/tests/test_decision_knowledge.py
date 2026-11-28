"""Development regression of B04 against the fixed, public repository corpus."""
from pathlib import Path
import shutil

import pytest


ROOT = Path(__file__).resolve().parents[3]
MANIFEST = Path("research/decision_hub/2026-11-24-method-corpus-index/corpus_index.json")
POLICY = Path("docs/PUBLICATION_POLICY.md")
GATE_SOURCE = Path("research/decision_methods/C028_INTERVAL_HARD_CONSTRAINT_FEASIBILITY_2026-11-20.md")


def test_all_154_fixed_sources_are_indexed_from_verified_bytes():
    from psychohistory.decision_knowledge import KnowledgeIndex

    report = KnowledgeIndex(ROOT).report()
    assert report["manifest"]["actual_blob"] == "6862d5a2cd3c7eb3f2da9a85d79c8b3386f2a102"
    assert report["counts"]["indexed"] == 154
    assert report["counts"]["identity_verified"] == 154
    assert report["counts"]["byte_duplicates"] == 0
    assert report["counts"]["documented_duplicate_supplements"] == 1
    assert report["counts"]["historical_source_changes"] == 1
    assert len({row["path"] for row in report["documents"]}) == 154
    gate = next(row for row in report["documents"] if row["path"] == GATE_SOURCE.as_posix())
    assert gate["actual_blob"] == "7cb8d5e3631dd17c0650cec06139d88b5bfcc700"
    assert gate["licence"]["status"] == "NO_OPEN_LICENCE_DECLARED"


def test_full_text_search_finds_a_body_only_term_without_admitting_evidence():
    from psychohistory.decision_knowledge import KnowledgeIndex

    index = KnowledgeIndex(ROOT)
    result = index.search("CERTAIN_PASS point-estimate midpoint", 5)
    gate = next(hit for hit in result["hits"] if hit["card"]["path"] == GATE_SOURCE.as_posix())
    assert gate["relevance"] > 0
    assert "point-estimate midpoint" in gate["snippet"].lower()
    assert gate["card"]["fact_type"] == "PROJECT_RESEARCH_NOTE"
    assert gate["card"]["evidence_qualification"] == "RESEARCH_REFERENCE_ONLY"
    assert gate["card"]["applicability_boundary"]
    assert result["authority"] == "NONE"
    assert index.search("qasgfjuwxkz")["hits"] == []


def test_unverified_missing_symlink_and_unlisted_content_stay_out_of_search(tmp_path):
    from psychohistory.decision_knowledge import KnowledgeIndex

    for relative in (MANIFEST, POLICY, GATE_SOURCE):
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, target)
    (tmp_path / GATE_SOURCE).write_text("<script>poisonlexicalx</script>", encoding="utf-8")
    scope = (tmp_path / GATE_SOURCE).parent
    (scope / "VOI_FOUR_SIGNAL_POLICIES_MAXIMIN_CERTIFICATE_2026-11-21.md").symlink_to(
        ROOT / GATE_SOURCE
    )
    (scope / "unlisted.md").write_text("poisonlexicalx", encoding="utf-8")

    index = KnowledgeIndex(tmp_path)
    report = index.report()
    assert report["status"] == "UNAVAILABLE"
    assert report["counts"]["identity_verified"] == 0
    assert report["counts"]["missing"] == 152
    assert report["counts"]["changed"] == 1
    assert report["counts"]["unreadable"] == 1
    assert report["unlisted_paths"] == ["research/decision_methods/unlisted.md"]
    assert index.search("poisonlexicalx")["hits"] == []


def test_modified_manifest_and_missing_publication_policy_fail_closed(tmp_path):
    from psychohistory.decision_knowledge import KnowledgeIndex

    for relative in (MANIFEST, GATE_SOURCE):
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, target)
    assert KnowledgeIndex(tmp_path).report()["status"] == "UNAVAILABLE"
    with (tmp_path / MANIFEST).open("ab") as manifest:
        manifest.write(b" ")
    result = KnowledgeIndex(tmp_path).report()
    assert result["manifest"]["status"] == "CHANGED"
    assert result["counts"]["indexed"] == 0


@pytest.mark.parametrize("goal", ["我不需要判断方案是否违反底线", "猜出我的未来收入", "<script>confirm()</script>"])
def test_unclear_negated_and_injected_goals_never_select_a_method(goal):
    from psychohistory.decision_knowledge import discover_knowledge

    result = discover_knowledge(goal)
    assert result["authority"] == "NONE"
    assert result["methods"] == []


def test_goal_backchains_to_evidence_and_native_gate_before_comparison():
    from psychohistory.decision_knowledge import discover_knowledge

    result = discover_knowledge("比较各目标的优势", limit=1)
    assert result["status"] == "CANDIDATE"
    assert len(result["search"]["hits"]) == 1
    method, = result["methods"]
    assert method["method"] == "pareto@1.0.0"
    assert method["status"] == "NEEDS_SCOPE"
    assert method["frontier"][0]["id"] == "scope"
    tasks = {item["id"]: item for item in method["requirements"]}
    assert tasks["scores"]["category"] == "QUALIFIED_EVIDENCE"
    assert "gateReceipt" in tasks["scores"]["after"]
    assert method["authority"] == "NONE"


def test_changed_historical_source_requires_timing_method_review():
    from psychohistory.decision_knowledge import discover_knowledge

    result = discover_knowledge("比较现在行动和等待")
    method, = result["methods"]
    assert method["method"] == "timing_actions@1.0.0"
    assert method["status"] == "REVIEW_REQUIRED"
    assert method["frontier"][0]["id"] == "reviewSources"
    assert method["authority"] == "NONE"
