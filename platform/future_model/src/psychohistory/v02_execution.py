"""Versioned execution envelope and isolated Python process adapter."""
import hashlib
import os
from pathlib import Path
import subprocess
import signal
import sys
import tempfile

from .contracts import canonical


RUN_KIND = "prediction-comparison-v1"
RUN_KIND_TRAJECTORY = "mechanism-trajectory-v1"


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def source_snapshot():
    root = Path(__file__).resolve().parent
    files = {}
    for path in sorted(root.glob("*.py")):
        if path.is_symlink() or not path.is_file():
            raise ValueError(f"Invalid platform source file: {path.name}")
        files[path.name] = path.read_bytes().hex()
    return files


class ComparisonProcess:
    def __init__(self, run, output):
        self.run = run
        self.output = output
        self.process = None

    def start(self):
        files = source_snapshot()
        expected = self.run["code_sha256"]
        if digest(files) != expected:
            raise ValueError("Platform source changed before worker launch")
        # The bootstrap itself is part of the fingerprint and arrives as source
        # text. No repository path or cached bytecode is used to import it.
        command = [sys.executable, "-I", "-S", "-B", *("-O" for _ in range(sys.flags.optimize)),
                   "-c", bytes.fromhex(files["v02_worker.py"]).decode(), str(self.output),
                   str(os.getpid()), expected]
        with tempfile.TemporaryFile() as payload:
            payload.write(canonical({"config": self.run["config"], "files": files, "kind": self.run.get("kind", RUN_KIND)}).encode())
            payload.seek(0)
            self.process = subprocess.Popen(command, stdin=payload, stdout=subprocess.DEVNULL,
                                            stderr=subprocess.DEVNULL, env={"LC_ALL": "C.UTF-8"},
                                            start_new_session=True)

    @property
    def pid(self):
        return self.process.pid

    @property
    def exitcode(self):
        return self.process.poll()

    def is_alive(self):
        return self.exitcode is None

    def join(self, timeout=None):
        try:
            self.process.wait(timeout)
        except subprocess.TimeoutExpired:
            pass

    def terminate(self):
        from .worker_lifecycle import terminate_owned_group
        terminate_owned_group(self.process, signal.SIGTERM)

    def kill(self):
        from .worker_lifecycle import terminate_owned_group
        terminate_owned_group(self.process, signal.SIGKILL)


def validate_result(run, result):
    """Check the worker's v1 comparison envelope before publishing or reading it."""
    import math
    import re

    from .degroot import DeGroot, source_reference
    from .prediction import aggregate
    from .state import Snapshot

    required = {"input", "protocol_id", "source_id", "code_sha256", "scope", "evidence",
                "metrics", "study_results", "weight_sensitivity", "trajectory",
                "mathematical_verification", "provenance", "limitations", "selection"}
    if not isinstance(result, dict) or not required <= result.keys():
        raise ValueError("Incomplete comparison result")
    config = run["config"]
    spec = config["spec"]
    if (result["code_sha256"] != run["code_sha256"] or result["input"] != config
            or result["protocol_id"] != config["protocol_id"] or result["source_id"] != config["source_id"]):
        raise ValueError("Comparison result provenance mismatch")
    evidence = result["evidence"]
    if (result["scope"] != "SYNTHETIC_ONLY" or not isinstance(evidence, dict)
            or evidence.get("kind") != "UNKNOWN" or evidence.get("scope") != "EMPIRICAL"):
        raise ValueError("Invalid comparison evidence scope")
    provenance = result["provenance"]
    if (not isinstance(provenance, dict) or provenance.get("protocol_sha256") != digest(spec)
            or provenance.get("protocol_version") != spec["protocol_version"]
            or provenance.get("dataset_version") != spec["dataset_version"]
            or provenance.get("seed") != spec["seed"]
            or provenance.get("source_reference") != source_reference()
            or not re.fullmatch(r"[a-f0-9]{64}", str(provenance.get("input_sha256", "")))):
        raise ValueError("Invalid comparison dataset or protocol receipt")
    selection = result["selection"]
    if (not isinstance(selection, dict) or selection.get("split") != "validation"
            or selection.get("test_used_for_selection") is not False
            or selection.get("horizon") not in spec["parameters"]["horizons"]):
        raise ValueError("Invalid comparison selection receipt")

    def metrics(value):
        if not isinstance(value, dict) or set(value) != {"r123-degroot", "train-prevalence"}:
            raise ValueError("Missing comparison model scores")
        for scores in value.values():
            if not isinstance(scores, dict) or set(scores) != {"brier", "log_loss"}:
                raise ValueError("Incomplete comparison metrics")
            for score, bound in (("brier", 1), ("log_loss", -math.log(1e-12))):
                val = scores[score]
                if type(val) not in (int, float) or not 0 <= val <= bound:
                    raise ValueError("Comparison score outside finite bounds")

    metrics(result["metrics"])
    studies = result["study_results"]
    scenarios = result["weight_sensitivity"]
    expected_studies = spec["dataset"]["studies"]
    expected_scenarios = spec["weight_sensitivity"]
    if not isinstance(studies, list) or len(studies) != len(expected_studies):
        raise ValueError("Incomplete comparison study results")
    if not isinstance(scenarios, list) or len(scenarios) != len(expected_scenarios):
        raise ValueError("Incomplete weight sensitivity scenarios")
    for study, expected in zip(studies, expected_studies, strict=True):
        identifier = expected["study_id"]
        n_train, n_test = (
            spec["budget"]["trials_per_session"] * sum(
                session.startswith(identifier + ":") for session in spec["split"][split]["session_groups"])
            for split in ("train", "test")
        )
        if (not isinstance(study, dict) or study.get("study_id") != identifier
                or study.get("study_label") != expected["label"] or study.get("n") != n_test):
            raise ValueError("Invalid comparison study identity or observations")
        baseline = study.get("baseline")
        if (not isinstance(baseline, dict) or baseline.get("training_n") != n_train
                or type(baseline.get("training_events")) is not int
                or not 0 <= baseline["training_events"] <= n_train
                or type(baseline.get("prevalence")) not in (float, int)
                or baseline["prevalence"] != baseline["training_events"] / n_train):
            raise ValueError("Invalid comparison study baseline")
        metrics(study.get("metrics"))
    for scenario, expected in zip(scenarios, expected_scenarios, strict=True):
        calculated = aggregate(studies, expected["weights"])
        if scenario != {"label": expected["label"], **calculated}:
            raise ValueError("Weight sensitivity does not match the protocol and study scores")
    if any(study["evidence"] != evidence for study in studies):
        raise ValueError("Study and result evidence disagree")
    if result["weight_sensitivity"][0]["metrics"] != result["metrics"]:
        raise ValueError("Comparison summary disagrees with equal-study scores")
    trajectory = result["trajectory"]
    if not isinstance(trajectory, dict) or not isinstance(trajectory.get("branches"), list):
        raise ValueError("Incomplete comparison branch snapshots")
    root = Snapshot.from_dict(trajectory.get("base"))
    root_payload = root.restore()
    branches = [Snapshot.from_dict(branch).restore() for branch in trajectory["branches"]]
    if (len(branches) != 2 or len({branch["branch"] for branch in branches}) != 2
            or any(branch["parent_hash"] != root.content_hash for branch in branches)):
        raise ValueError("Comparison branch lineage mismatch")
    model = DeGroot()
    for payload in (root_payload, *branches):
        if payload["model_id"] != spec["candidate"] or payload["model_version"] != spec["model_version"]:
            raise ValueError("Snapshot model identity mismatch")
        model.validate_state(payload["state"])
    if not isinstance(result["mathematical_verification"], dict):
        raise ValueError("Missing mathematical verification")
    if not isinstance(result["limitations"], list) or not result["limitations"]:
        raise ValueError("Missing comparison limitations")
