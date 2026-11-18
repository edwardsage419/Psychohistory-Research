"""Create a backup with released v0.1 code and read the exact artifact with v0.2."""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile


def verify(repo, baseline, report_path):
    project = Path(__file__).resolve().parents[1]
    report = {"baseline": baseline, "commands": []}

    def run(command, source=None):
        env = dict(os.environ)
        if source:
            env["PYTHONPATH"] = str(source)
        result = subprocess.run(command, cwd=repo, env=env, capture_output=True, timeout=60)
        report["commands"].append({"argv": command, "exit": result.returncode,
                                   "stderr": result.stderr.decode(errors="replace"),
                                   "stdout_sha256": hashlib.sha256(result.stdout).hexdigest()})
        if result.returncode != 0:
            raise RuntimeError(result.stderr.decode(errors="replace"))
        return result.stdout

    with tempfile.TemporaryDirectory(prefix="ph-v02-legacy-") as tmp:
        work = Path(tmp)
        data = work / "legacy-data"
        backup = work / "legacy-backup"
        restored = work / "restored-with-v02"
        try:
            archive = run(["git", "archive", baseline, "platform/future_model/src"])
            with tarfile.open(fileobj=io.BytesIO(archive)) as bundle:
                bundle.extractall(work, filter="data")
            old_source = work / "platform/future_model/src"

            def cli(source, root, *args):
                return json.loads(run([sys.executable, "-m", "psychohistory.cli", "--repo",
                                       str(repo), "--data", str(root), *map(str, args)], source))

            original = cli(old_source, data, "demo", "--seed", 123, "--rounds", 6, "--population", 16)
            cli(old_source, data, "backup", backup)
            cli(project / "src", restored, "restore", backup)
            result = cli(project / "src", restored, "result", original["run"]["id"])
            if original["result"] != result:
                raise ValueError("Restored v0.1 artifact differs")
            records = cli(project / "src", restored, "runs")
            if records[0]["result_hash"] != original["run"]["result_hash"]:
                raise ValueError("Restored v0.1 artifact hash differs")
            report.update(status="PASS", v01_artifact_sha256=records[0]["result_hash"])
        except Exception as error:
            report.update(status="FAIL", error=str(error))
            raise
        finally:
            report_path.write_text(json.dumps(report, indent=2) + "\n")
    print("v0.1 native backup restored and verified by v0.2:", report["v01_artifact_sha256"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--report", type=Path, required=True)
    options = parser.parse_args()
    verify(options.repo.resolve(), options.baseline, options.report)
