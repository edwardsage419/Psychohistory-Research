"""Verify the owner task's public inputs and replay selected research controls."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[3]
TASK = "research/decision_hub/2026-11-25-v07-autonomous-foundation-codex-task.md"
TASK_COMMIT = "6e44ecf50e9e8de0d8a3eb76766cd0d3bf44ab9c"
FIXED_MAIN = "5627ea49ee889773c8af1db373b3da0dfdf21f8d"
HUB = "research/decision_hub"
INLINE = (
    f"{HUB}/2026-11-24-version-integration-specification/README.md",
    f"{HUB}/2026-11-24-version-integration-specification/specification.json",
    "docs/PROJECT_WORKFLOW_REQUIREMENTS_V3_2_2026-11-25.md",
    f"{HUB}/2026-11-24-language-evidence-corpus/language_corpus.json",
    f"{HUB}/2026-11-24-semantic-proposal-contract/corpus.json",
    f"{HUB}/2026-11-24-native-method-contract-index/method_contracts.json",
    f"{HUB}/2026-11-24-method-corpus-index/corpus_index.json",
    f"{HUB}/2026-11-24-content-method-retrieval/probe.js",
)
REPLAYS = (
    ("version-integration-specification", "check.js", "results.json"),
    ("language-evidence-corpus", "lint_corpus.js", "lint_results.json"),
    ("semantic-proposal-contract", "probe.js", "results.json"),
    ("method-corpus-index", "replay_index.js", "identity_results.json"),
    ("feedback-replay-and-rollback", "probe.js", "results.json"),
    ("content-method-retrieval", "probe.js", "results.json"),
)


def command(*args):
    return subprocess.check_output(args, cwd=ROOT)


def git_tree(tree, *paths):
    rows = command("git", "ls-tree", "-rz", tree, "--", *paths).split(b"\0")
    entries = {}
    for row in filter(None, rows):
        meta, path = row.split(b"\t", 1)
        _, kind, blob = meta.decode().split()
        if kind == "blob":
            entries[path.decode()] = blob
    return entries


def worktree_blob(path):
    file = ROOT / path
    if not file.is_file():
        return None
    data = file.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def fixed_inventory():
    task = command("git", "show", f"{TASK_COMMIT}:{TASK}").decode()
    index = task.split("## 5.", 1)[1].split("## 6.", 1)[0]
    inline_hashes = re.findall(r"（([0-9a-f]{40})）", index.partition("###")[0])
    listed = re.findall(r"^- `([^`]+)`  `([0-9a-f]{40})`", index, re.M)
    if len(listed) != 53 or len(inline_hashes) != len(INLINE):
        raise ValueError("Fixed index shape changed")
    entries = [*zip(INLINE, inline_hashes, strict=True), *listed]
    actual = git_tree(FIXED_MAIN, *(path for path, _ in entries))
    rows = []
    for path, expected in entries:
        worktree = worktree_blob(path)
        rows.append({"path": path, "expected_blob": expected, "fixed_main_blob": actual.get(path),
                     "working_tree_blob": worktree, "fixed_main_matches": expected == actual.get(path),
                     "working_tree_matches": expected == worktree})
    return {
        "task_commit": TASK_COMMIT,
        "fixed_main": FIXED_MAIN,
        "working_head": command("git", "rev-parse", "HEAD").decode().strip(),
        "bullet_paths": len(listed),
        "inline_paths": len(inline_hashes),
        "total_paths": len(rows),
        "matches_at_fixed_main": sum(row["fixed_main_matches"] for row in rows),
        "matches_in_worktree": sum(row["working_tree_matches"] for row in rows),
        "rows": rows,
    }



def retrieval_numeric_drift(result, historical):
    original_rows = historical["rows"]
    if len(result["rows"]) != len(original_rows):
        return {"ranking_identity": False, "metrics_equal": False}
    changes = []
    same_ranks = True
    for new, old in zip(result["rows"], original_rows, strict=True):
        for strategy, rank in new["ranks"].items():
            original = old["ranks"][strategy]
            if [(hit["path"], hit["group"]) for hit in rank] != [
                (hit["path"], hit["group"]) for hit in original
            ]:
                same_ranks = False
                continue
            changes.extend(abs(a["score"] - b["score"]) for a, b in zip(rank, original, strict=True)
                           if a["score"] != b["score"])
    largest = max(changes, default=0)
    return {
        "ranking_identity": same_ranks,
        "metrics_equal": result["metrics"] == historical["metrics"],
        "rounded_scores_changed": len(changes),
        "maximum_absolute_score_delta": largest,
        "absolute_tolerance_met": math.isclose(largest, 0, abs_tol=1e-12),
    }



def language_negative_controls(node, folder):
    # The pinned lint CLI executes the positive linter. Invoke that exact lint function
    # again against isolated mutations to verify the historical negative controls.
    runner = """
const fs = require("node:fs");
const source = fs.readFileSync(process.argv[1], "utf8");
const lint = Function(source.split("const c=JSON.parse", 1)[0].replace(
    "const fs=require('node:fs');", "") + "return lint;")();
const original = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
const changes = {
    span: d => { d.cases[0].turns[0].claims[0].span = "absent"; },
    revision: d => { d.cases[0].turns[0].claims[0].supersedes = "absent"; },
    interval: d => { Object.assign(d.cases[0].turns[0].claims[0], {lo: 1, hi: 0}); },
    source: d => { d.cases[0].sources.push("absent"); },
    duplicate: d => { d.cases[1].id = d.cases[0].id; },
};
const output = Object.entries(changes).map(([k, mutate]) => {
    const sample = structuredClone(original);
    mutate(sample);
    try { lint(sample); return {k, rejected: false}; }
    catch { return {k, rejected: true}; }
});
console.log(JSON.stringify(output));
"""
    return json.loads(command(node, "-e", runner, f"{folder}/lint_corpus.js",
                              f"{folder}/language_corpus.json"))


def replay(node, name, entrypoint, expected_file):
    folder = f"{HUB}/2026-11-24-{name}"
    files = git_tree(FIXED_MAIN, folder)
    for path, expected_blob in files.items():
        if worktree_blob(path) != expected_blob:
            raise ValueError(f"Historical replay bytes changed: {path}")
    args = [node, f"{folder}/{entrypoint}"]
    if name == "content-method-retrieval":
        args.append(str(ROOT))
    output = command(*args)
    expected = command("git", "show", f"{FIXED_MAIN}:{folder}/{expected_file}")
    result = json.loads(output)
    historical = json.loads(expected)
    accuracy = {"comparison": "EXACT_JSON", "reproduced": result == historical}
    if name == "version-integration-specification":
        accuracy = {"comparison": "RECORDED_SPECIFICATION_CHECK", "reproduced":
                    result == historical["specificationCheck"]}
    if name == "language-evidence-corpus":
        controls = language_negative_controls(node, folder)
        summary = historical["summary"]
        sources = json.loads((ROOT / folder / "language_corpus.json").read_bytes())["sources"]
        verified = sum(git_tree(source["commit"], source["path"]).get(source["path"]) == source["blob"]
                       for source in sources)
        supplemented = {**result, "negativeControls": len(controls), "sourceIdentityChecks": verified}
        accuracy = {
            "comparison": "RECORDED_SUMMARY_AND_RERUN_NEGATIVE_CONTROLS",
            "reproduced": all(supplemented.get(key) == value for key, value in summary.items())
            and controls == historical["negativeControls"],
            "negative_controls": controls, "verified_source_identities": verified,
        }
    if name == "content-method-retrieval":
        drift = retrieval_numeric_drift(result, historical)
        accuracy = {"comparison": "RANKS_AND_METRICS_WITH_1E-12_SCORE_PRECISION", **drift,
                    "reproduced": drift["ranking_identity"] and drift["metrics_equal"]
                    and drift.get("absolute_tolerance_met", False)}
    return {
        "id": name,
        "command": ["node", *("." if arg == str(ROOT) else arg for arg in args[1:])],
        "historical_input_files_verified": len(files),
        "expected_output_path": f"{folder}/{expected_file}",
        "recorded_output_match": result == historical,
        **accuracy,
        "output_sha256": hashlib.sha256(output).hexdigest(),
        "summary": {key: value for key, value in result.get("summary", result).items() if key != "rows"},
    }



def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--node", default="node")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    inventory = fixed_inventory()
    if inventory["matches_at_fixed_main"] != inventory["total_paths"]:
        raise ValueError("Historical research identity mismatch")
    inventory["node"] = command(args.node, "--version").decode().strip()
    inventory["replays"] = [replay(args.node, *case) for case in REPLAYS]
    args.output.write_text(json.dumps(inventory, ensure_ascii=False, indent=2) + "\n")
    print(f"{inventory['matches_at_fixed_main']}/{inventory['total_paths']} fixed research identities")
    for row in inventory["replays"]:
        print(row["id"], "REPRODUCED" if row["reproduced"] else "OUTPUT_DIFFERS")


if __name__ == "__main__":
    main()
