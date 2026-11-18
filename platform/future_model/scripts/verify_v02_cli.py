"""Run real v0.2 CLI commands against a fresh data directory and verify restore."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


def verify(repo, report):
    project = Path(__file__).resolve().parents[1]
    environment = {**os.environ, "PYTHONPATH": str(project / "src")}
    commands = []
    with tempfile.TemporaryDirectory(prefix="ph-v02-cli-") as temporary:
        home = Path(temporary)
        data = home / "data"

        def run(*args, root=data, expected=0):
            command = [sys.executable, "-m", "psychohistory.cli", "--repo", str(repo),
                       "--data", str(root), *map(str, args)]
            response = subprocess.run(command, env=environment, text=True,
                                      capture_output=True, timeout=45)
            commands.append({"argv": command, "exit": response.returncode,
                             "stderr": response.stderr, "stdout_sha256": hashlib.sha256(
                                 response.stdout.encode()).hexdigest()})
            if response.returncode != expected:
                raise RuntimeError(response.stderr or response.stdout[:400])
            return json.loads(response.stdout) if expected == 0 else None

        try:
            for name in ("R123", "R132", "R233"):
                source = run("research", "register", name)
                run("research", "verify", source["source_id"])
                if name == "R123":
                    r123 = source
            protocol = run("research", "protocol", r123["source_id"], "--seed", 829)
            identity = protocol["protocol_id"]
            run("research", "submit", identity, expected=1)
            run("research", "approve-protocol", identity)
            comparison = run("research", "submit", identity)
            identifier = comparison["id"]
            run("research", "cancel", identifier)
            new = run("research", "retry", identifier)
            if new["id"] == identifier:
                raise ValueError("Retry did not preserve old run and create a fresh run")
            identifier = new["id"]
            completed = run("research", "approve", identifier)
            result = run("research", "result", identifier)
            if completed["result_hash"] != result["artifact_sha256"]:
                raise ValueError("Result artifact identity changed")
            if run("research", "submit", identity)["id"] != identifier:
                raise ValueError("Holdout was reopened after publication")
            backup = home / "backup"
            restored = home / "restored"
            run("backup", backup)
            run("restore", backup, root=restored)
            if run("research", "result", identifier, root=restored) != result:
                raise ValueError("Restored artifact differs")
            if run("research", "submit", identity, root=restored)["id"] != identifier:
                raise ValueError("Holdout was reopened after restore")
            summary = {"status": "PASS", "artifact_sha256": result["artifact_sha256"],
                       "protocol_id": identity, "metrics": result["result"]["metrics"]}
        except Exception as error:
            summary = {"status": "FAIL", "error": str(error)}
            raise
        finally:
            report.write_text(json.dumps({**summary, "commands": commands,
                                          "python": sys.version}, indent=2) + "\n")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    verify(args.repo.resolve(), args.report)
