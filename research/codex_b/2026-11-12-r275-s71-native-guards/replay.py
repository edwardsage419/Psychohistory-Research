#!/usr/bin/env python3
"""R275/S71 archived native replay and assertion-only patch qualification."""
import argparse
import ast
import copy
import csv
import hashlib
import io
import json
import platform
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BASE = "d4740c2cd999b8da06a25b0ef407aeaf8a56ab6c"
R = "research/validation/r275_s71_noisy_pair_exact_20261030.js"
B = "research/evidence_audit/b_r275_s71_independent_gate_20261030.py"
CSV = "research/validation/R275_S71_ALL_3072_NOISY_PAIR_ROWS_2026-10-30.csv"
JSON = "research/validation/R275_S71_EXACT_RESULTS_2026-10-30.json"
HELPER = '''def require(condition, message):
    if not condition:
        raise ValueError("R275_S71:" + message)
'''
EXPECTED = {"source_rows": 3072, "epsilons": 4, "confusion_cells": 36,
            "MAP_values": 4, "status": "PASS"}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def identity(data):
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
            "git_blob": hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()}


def capture(pins):
    for path, expected in pins.items():
        data = (ROOT / path).read_bytes()
        require(identity(data) == expected, "SOURCE_IDENTITY:" + path)
        require(data == subprocess.check_output(["git", "show", BASE + ":" + path], cwd=ROOT),
                "SOURCE_VERSION:" + path)
    return pins


def check_patch_scope(original, candidate, inventory):
    """Expected AST is original, with only the 18 guard replacements + helper."""
    original_tree = ast.parse(original)
    nodes = sorted((n for n in ast.walk(original_tree) if isinstance(n, ast.Assert)),
                   key=lambda n: (n.lineno, n.col_offset))
    require(len(nodes) == len(inventory) == 18, "GUARD_INVENTORY")
    by_line = {}
    for node, entry in zip(nodes, inventory):
        require(node.lineno == entry["line"] and
                ast.get_source_segment(original, node.test) == entry["condition"], "GUARD_IDENTITY")
        by_line[node.lineno] = entry["label"]

    class Guards(ast.NodeTransformer):
        def visit_Assert(self, node):
            # Only the original duplicate guard has a message, which is retained.
            message = node.msg if node.msg is not None else ast.Constant(by_line[node.lineno])
            return ast.Expr(ast.Call(ast.Name("require", ast.Load()), [node.test, message], []))

    expected = Guards().visit(original_tree)
    last_import = max(i for i, n in enumerate(expected.body)
                      if isinstance(n, (ast.Import, ast.ImportFrom)))
    expected.body.insert(last_import + 1, ast.parse(HELPER).body[0])
    require(ast.dump(expected, include_attributes=False) ==
            ast.dump(ast.parse(candidate), include_attributes=False), "PATCH_SCOPE")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    out = args.output.resolve()
    require(not out.exists(), "OUTPUT_EXISTS")
    out.mkdir(parents=True)
    pins = json.loads((HERE / "pins.json").read_bytes())
    inventory = json.loads((HERE / "guard-inventory.json").read_bytes())
    summary = {"status": "FAIL", "main": BASE,
        "S71_freeze": "8c2964149055b7fa824bd9b10446ffd1e0613768",
        "python": sys.version, "platform": platform.platform(), "commands": [],
        "harness": identity(Path(__file__).read_bytes()),
        "package_inputs": {p: identity((HERE / p).read_bytes()) for p in
                           ["pins.json", "explicit-guards.patch", "guard-inventory.json"]},
        "bad_inputs": [], "artifact_comparisons": []}
    streams = {}

    def run(label, argv, expected=0, error=None):
        p = subprocess.run(argv, cwd=ROOT, capture_output=True, timeout=30)
        record = {"label": label, "argv": list(map(str, argv)), "exit_code": p.returncode,
                  "expected_exit": expected, "expected_error": error, "streams": {}}
        for kind, data in [("stdout", p.stdout), ("stderr", p.stderr)]:
            name = label + "." + kind
            streams[name] = data
            record["streams"][kind] = {"member": name, **identity(data)}
        summary["commands"].append(record)
        require(p.returncode == expected, "EXIT:" + label)
        if error:
            require(not p.stdout and error.encode() in p.stderr, "REJECTION:" + label)
            require(b"SyntaxError:" not in p.stderr and b"ModuleNotFoundError:" not in p.stderr,
                    "INVALID_REJECTION:" + label)
        else:
            require(not p.stderr, "STDERR:" + label)
        return p.stdout

    def gate(label, path, js, cs, optimized, expected=0, error=None, good=True):
        argv = [sys.executable, "-I", "-B"] + (["-O"] if optimized else []) + [path, js, cs]
        data = run(label, argv, expected, error)
        if expected == 0:
            parsed = json.loads(data)
            require(parsed == EXPECTED if good else parsed.get("status") == "PASS", "OUTPUT:" + label)
        return data

    try:
        summary["sources_before"] = capture(pins)
        node = shutil.which("node")
        require(node is not None, "NODE_NOT_AVAILABLE")
        summary["node"] = run("node-version", [node, "--version"]).decode().strip()
        with tempfile.TemporaryDirectory(prefix="r275-s71-native-") as tmp:
            t = Path(tmp)
            r = t / "R.js"
            r.write_bytes((ROOT / R).read_bytes())
            original = t / "original.py"
            original.write_bytes((ROOT / B).read_bytes())
            candidate = t / B
            candidate.parent.mkdir(parents=True)
            candidate.write_bytes(original.read_bytes())
            patch = HERE / "explicit-guards.patch"
            run("patch-check", ["git", "-C", t, "apply", "--check", patch])
            run("patch-apply", ["git", "-C", t, "apply", patch])
            before, after = original.read_text(), candidate.read_text()
            check_patch_scope(before, after, inventory)
            summary["patch_scope"] = {"guards": 18, "other_original_AST_unchanged": True,
                                      "candidate": identity(candidate.read_bytes())}
            summary["scope_mutations_rejected"] = []
            for label, mutant in [
                ("changed_likelihood", after.replace("F(1,16)", "F(1,15)", 1)),
                ("disabled_evidence_guard", after.replace(
                    "data['evidence']=='E1_ARTIFICIAL_NONBLIND'", "True", 1)),
            ]:
                require(mutant != after, "MUTATION_NOT_INJECTED:" + label)
                try:
                    check_patch_scope(before, mutant, inventory)
                except RuntimeError as exc:
                    require(str(exc) == "PATCH_SCOPE", "WRONG_SCOPE_REJECTION")
                else:
                    raise RuntimeError("ESCAPED_SCOPE_MUTATION:" + label)
                summary["scope_mutations_rejected"].append(label)
            archived_j, archived_c = t / "archive.json", t / "archive.csv"
            archived_j.write_bytes((ROOT / JSON).read_bytes())
            archived_c.write_bytes((ROOT / CSV).read_bytes())
            emitted = t / "emitted"
            emitted.mkdir()
            emit_output = json.loads(run("R-emit", [node, r, "--emit", emitted]))
            summary["emitter_output"] = emit_output
            generated_j = emitted / "R275_S71_EXACT_RESULTS.json"
            generated_c = emitted / "R275_S71_ALL_3072_NOISY_PAIR_ROWS.csv"
            for path, original_path in [(generated_j, archived_j), (generated_c, archived_c)]:
                equal = path.read_bytes() == original_path.read_bytes()
                summary["artifact_comparisons"].append({"generated": path.name,
                    "identity": identity(path.read_bytes()), "byte_identical": equal})
                require(equal, "ARTIFACT_BYTES:" + path.name)
            parsed_rows = list(csv.DictReader(io.StringIO(archived_c.read_text())))
            summary["zero_probability_rows"] = sum(row["true_source_probability"] == "0" for row in parsed_rows)
            for optimized in [False, True]:
                mode = "optimized" if optimized else "normal"
                for source, program in [("original", original), ("candidate", candidate)]:
                    for kind, js, cs in [("archive", archived_j, archived_c),
                                         ("generated", generated_j, generated_c)]:
                        gate(source + "-" + mode + "-" + kind, program, js, cs, optimized)

            # Exactly the six previously archived mutation categories, as actual files.
            mutations = [("duplicate", "duplicate source"), ("missing", "complete_source_keys"),
                         ("probability", "source_probability"), ("MAP", "MAP_and_correct"),
                         ("posterior", "posterior"), ("evidence", "evidence")]
            for label, guard in mutations:
                obj = json.loads(archived_j.read_bytes())
                rows = copy.deepcopy(parsed_rows)
                if label == "duplicate":
                    rows.append(copy.deepcopy(rows[0]))
                elif label == "missing":
                    rows.pop()
                elif label == "probability":
                    require(rows[0]["true_source_probability"] == "1/256", "MUTATION_ANCHOR")
                    rows[0]["true_source_probability"] = "1/255"
                elif label == "MAP":
                    require(rows[0]["MAP_selected"] != "FLIP_PAIR", "MUTATION_ANCHOR")
                    rows[0]["MAP_selected"] = "FLIP_PAIR"
                elif label == "posterior":
                    require(rows[0]["posterior_IID"] == "1/17", "MUTATION_ANCHOR")
                    rows[0]["posterior_IID"] = "1/18"
                elif label == "evidence":
                    obj["evidence"] = "E3"
                bad_j, bad_c = t / (label + ".json"), t / (label + ".csv")
                # Preserve the CSV bytes exactly for the JSON-only control.
                bad_j.write_text(json.dumps(obj, indent=2) + "\n")
                raw = io.StringIO(newline="")
                writer = csv.DictWriter(raw, fieldnames=list(parsed_rows[0]), lineterminator="\n")
                writer.writeheader()
                writer.writerows(rows)
                bad_c.write_text(raw.getvalue())
                if label == "evidence":
                    require(bad_c.read_bytes() == archived_c.read_bytes(), "JSON_ONLY_CONTROL")
                summary["bad_inputs"].append({"label": label, "candidate_guard": guard,
                    "json": identity(bad_j.read_bytes()), "csv": identity(bad_c.read_bytes())})
                for optimized in [False, True]:
                    mode = "optimized" if optimized else "normal"
                    # Preserve optimized false acceptance as expected RED, never count it as valid rejection.
                    gate("original-" + mode + "-bad-" + label, original, bad_j, bad_c, optimized,
                         0 if optimized else 1, None if optimized else "AssertionError", good=False)
                    gate("candidate-" + mode + "-reject-" + label, candidate, bad_j, bad_c, optimized,
                         1, "ValueError: R275_S71:" + guard)
            require(original.read_bytes() == (ROOT / B).read_bytes(), "TEMP_ORIGINAL_CHANGED")
            require(r.read_bytes() == (ROOT / R).read_bytes(), "TEMP_R_CHANGED")
            require(archived_j.read_bytes() == (ROOT / JSON).read_bytes(), "TEMP_JSON_CHANGED")
            require(archived_c.read_bytes() == (ROOT / CSV).read_bytes(), "TEMP_CSV_CHANGED")
            require(candidate.read_text() == after, "TEMP_CANDIDATE_CHANGED")
        summary["sources_after"] = capture(pins)
        summary["status"] = "COMPLETE_BOUNDED_PATCH_CANDIDATE"
        summary["original_optimized_false_acceptances"] = 6
        summary["candidate_bad_files_rejected"] = 12
        summary["scientific_status"] = "UNCHANGED_E1_ARTIFICIAL_NONBLIND"
        summary["production_patch"] = "NOT_APPLIED"
        summary["human_scoring"] = "NOT_RUN"
    except Exception as exc:
        summary["failure"] = str(exc)
        raise
    finally:
        archive = out / "streams.tar.gz"
        with tarfile.open(archive, "w:gz") as tar:
            for name, data in streams.items():
                info = tarfile.TarInfo(name)
                info.size = len(data)
                info.mtime = 0
                tar.addfile(info, io.BytesIO(data))
        summary["stream_archive"] = identity(archive.read_bytes())
        (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({"status": summary["status"], "commands": len(summary["commands"]),
        "streams": len(streams), "source_identities": len(pins), "candidate_guards": 18,
        "original_optimized_false_acceptances": 6, "candidate_bad_files_rejected": 12}))


if __name__ == "__main__":
    main()
