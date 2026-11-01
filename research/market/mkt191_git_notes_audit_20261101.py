#!/usr/bin/env python3
"""Native Git notes annotation and provenance counterexample, artificial only."""
import json
import subprocess
import tempfile
from pathlib import Path


def git(repo, *args, check=True):
    p = subprocess.run(["git", "-C", str(repo), *args], text=True, capture_output=True)
    if check and p.returncode:
        raise RuntimeError(f"git {args}: {p.stderr}")
    return p.stdout.strip(), p.returncode


def run():
    with tempfile.TemporaryDirectory(prefix="mkt191_") as tmp:
        root = Path(tmp)
        src = root / "source"
        src.mkdir()
        git(src, "init", "-q", "-b", "main")
        git(src, "config", "user.name", "Synthetic Research")
        git(src, "config", "user.email", "synthetic@example.invalid")
        (src / "decision.json").write_text('{"id":"D1","forecast":0.8,"outcome":"UNVERIFIED"}\n')
        git(src, "add", "decision.json")
        git(src, "commit", "-qm", "synthetic forecast")
        commit, _ = git(src, "rev-parse", "HEAD")
        original_content, _ = git(src, "show", "HEAD:decision.json")
        git(src, "notes", "add", "-m", "outcome: SELF_REPORTED_SUCCESS", commit)
        note1, _ = git(src, "notes", "show", commit)
        note_ref1, _ = git(src, "rev-parse", "refs/notes/commits")
        unchanged_commit, _ = git(src, "rev-parse", "HEAD")
        assert unchanged_commit == commit
        assert note1 == "outcome: SELF_REPORTED_SUCCESS"
        assert original_content == git(src, "show", "HEAD:decision.json")[0]
        git(src, "notes", "add", "-f", "-m", "outcome: INDEPENDENTLY_CONFIRMED_FAILURE", commit)
        note2, _ = git(src, "notes", "show", commit)
        note_ref2, _ = git(src, "rev-parse", "refs/notes/commits")
        assert note_ref2 != note_ref1 and note2 != note1
        assert git(src, "rev-parse", "HEAD")[0] == commit
        git(src, "notes", "remove", commit)
        _, show_status = git(src, "notes", "show", commit, check=False)
        assert show_status != 0
        assert git(src, "rev-parse", "HEAD")[0] == commit
        # The historical notes commit still exists immediately, though the default note is absent.
        # Git notes tree sharding varies with object count, so inspect history rather than assume a path.
        notes_history, _ = git(src, "log", "--format=%H", "refs/notes/commits")
        assert note_ref1 in notes_history and note_ref2 in notes_history
        # Ordinary clone fetches main but generally does not include refs/notes/commits.
        dst = root / "clone"
        p = subprocess.run(["git", "clone", "-q", str(src), str(dst)], capture_output=True, text=True)
        assert p.returncode == 0, p.stderr
        assert git(dst, "rev-parse", "HEAD")[0] == commit
        _, note_clone_status = git(dst, "rev-parse", "--verify", "refs/notes/commits", check=False)
        assert note_clone_status != 0
        result = {
            "git_version": subprocess.run(["git", "--version"], capture_output=True, text=True).stdout.strip(),
            "assertions": 11,
            "status": "PASS",
            "original_commit_unchanged_across_add_overwrite_remove": True,
            "note_ref_changed_on_overwrite": True,
            "latest_note_removed": True,
            "historical_note_commits_remain_in_notes_ref_history": True,
            "ordinary_clone_missing_notes_ref": True,
            "synthetic_only": True,
            "independent_outcome_truth_verified": False,
        }
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return result


if __name__ == "__main__":
    run()
