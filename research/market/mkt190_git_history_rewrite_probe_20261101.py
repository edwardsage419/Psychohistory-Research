#!/usr/bin/env python3
"""Local, synthetic Git decision-history persistence probe. No network or real user data."""
import json
import pathlib
import subprocess
import tempfile

def run(repo, *args, ok=True):
    result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    if ok and result.returncode:
        raise RuntimeError(f"git {args} failed: {result.stderr}")
    return result.stdout.strip() if ok else result.returncode

def main():
    with tempfile.TemporaryDirectory(prefix="mkt190_synthetic_") as directory:
        repo = pathlib.Path(directory)
        run(repo, "init", "-q", "-b", "main")
        run(repo, "config", "user.name", "Synthetic Research")
        run(repo, "config", "user.email", "synthetic@example.invalid")
        path = repo / "decision.json"
        path.write_text('{"decision":"D1","forecast":0.8,"status":"OPEN"}\n', encoding="utf-8")
        run(repo, "add", "decision.json")
        run(repo, "commit", "-qm", "record synthetic forecast")
        forecast_commit = run(repo, "rev-parse", "HEAD")
        path.write_text('{"decision":"D1","forecast":0.8,"status":"SELF_REPORTED_SUCCESS"}\n', encoding="utf-8")
        run(repo, "add", "decision.json")
        run(repo, "commit", "-qm", "record synthetic self report")
        outcome_commit = run(repo, "rev-parse", "HEAD")
        assert outcome_commit != forecast_commit
        assert outcome_commit in run(repo, "rev-list", "main").splitlines()
        run(repo, "reset", "--hard", forecast_commit)
        assert run(repo, "rev-parse", "HEAD") == forecast_commit
        assert outcome_commit not in run(repo, "rev-list", "main").splitlines()
        assert outcome_commit in run(repo, "reflog", "--format=%H").splitlines()
        assert run(repo, "cat-file", "-t", outcome_commit) == "commit"
        run(repo, "reflog", "expire", "--expire=now", "--expire-unreachable=now", "--all")
        run(repo, "gc", "--prune=now", "--aggressive")
        deleted = run(repo, "cat-file", "-e", outcome_commit, ok=False) != 0
        assert deleted, "Expected unreachable synthetic outcome object to be pruned"
        print(json.dumps({"result": "PASS", "git": run(repo, "--version"),
                          "forecast_commit": forecast_commit, "outcome_commit": outcome_commit,
                          "outcome_reachable_from_main_after_reset": False,
                          "outcome_in_reflog_before_expiration": True,
                          "outcome_object_exists_after_forced_gc": not deleted,
                          "scope": "local synthetic only; forced expiry not default Git retention"},
                         ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
