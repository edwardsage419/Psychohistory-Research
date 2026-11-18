"""Read curated research evidence from immutable local Git objects."""

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
from shutil import which
import stat
import subprocess


MAIN_COMMIT = "7ea6eab94433e3669b6f492d802bb35316dc90d6"
MAIN_REF = "refs/remotes/origin/main"
_OBJECT_ID = re.compile(r"[0-9a-f]{40}")
_DOCUMENT_LIMIT = 2 * 1024 * 1024
_GIT = which("git", path=os.defpath)
_GIT_ENV = {
    "PATH": os.defpath,
    "LC_ALL": "C",
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_CONFIG_GLOBAL": os.devnull,
    "GIT_GRAFT_FILE": os.devnull,
    "GIT_OPTIONAL_LOCKS": "0",
    "GIT_NO_LAZY_FETCH": "1",
    "GIT_ALLOW_PROTOCOL": "",
    "GIT_TERMINAL_PROMPT": "0",
}


class SourceError(ValueError):
    """The source selector or the registered evidence failed validation."""


@dataclass(frozen=True)
class _File:
    role: str
    path: str
    sha256: str


@dataclass(frozen=True)
class _Profile:
    label: str
    scope: str
    files: tuple[_File, ...]


_PROFILES = {
    "R123": _Profile(
        "DeGroot Consensus Model",
        "Exact finite scalar consensus and influence in constructed stochastic matrices, including the distinction between universal and particular-initial-state consensus.",
        (
            _File("source", "research/R123/R123_FINAL_ACCEPTANCE_STATUS.json",
                  "e38c6061d4aab2093cf847e630efc51688709c216d116fee7fc60be9b1618fb2"),
            _File("model", "research/R123/r123_degroot_1974_berger_1981_exact_consensus.py",
                  "463551a6e838b8993d65faf3ba391146892d0ba56cd1b66fe41baaf028434e1b"),
            _File("experiment", "research/R123/test_r123_degroot_1974_berger_1981_exact_consensus.py",
                  "b4129098a953ce44684a3a35927763872e75e907b0cdf22066c18ea5b279eadf"),
            _File("freeze", "protocols/R123_DEGROOT_1974_BERGER_1981_CONSENSUS_STRUCTURE_AND_INITIAL_OPINIONS_FREEZE_2026-10-19.md",
                  "cc245b4c08ea395cdffdf07cb29c075ad8c56c5bfb667ef0a5a2a5af56fb87da"),
            _File("report", "research/R123/R123_DEGROOT_1974_BERGER_1981_ORIGINAL_CONSENSUS_AND_INFLUENCE_SCIENTIFIC_REPORT_2026-10-19.md",
                  "688fc4e7ae96118d316588caaadea401dce75b5fc2854f04573cf2f7daa19b54"),
            _File("receipt", "research/R123/R123_PHASE_A_ORIGINAL_DEGROOT_BERGER_58_TEST_226_MATRIX_CI_ACCEPTANCE.json",
                  "d4f8a676c9976e11dfb7dc15a13fd3c1798a911b5bb7f12f1d309ea94d41566f"),
        ),
    ),
    "R132": _Profile(
        "Replicator Dynamics",
        "Taylor–Jonker continuous and discrete equations, finite mathematical trajectories, and numerical artifacts across the two study phases.",
        (
            _File("source", "research/R132/R132_FINAL_ACCEPTANCE_STATUS.json",
                  "a4b4524fb123b2fd9f92fa0e65f307816337be04f76d72f0e5c29d359f71a39b"),
            _File("model", "research/R132/r132_replicator_1978_exact_invariants_and_trajectories.py",
                  "5dbb96ecfe19d9689b900369364f453b6311bf0cde87a3c2eeec263b37ad7e15"),
            _File("experiment", "research/R132/test_r132_replicator_1978_exact_invariants_and_trajectories.py",
                  "12438b38055ad51709493f48a130316bb54bbfb7ec5ea3f3c69a840af4ab5696"),
            _File("freeze", "protocols/R132_TAYLOR_JONKER_1978_REPLICATOR_TRAJECTORIES_AND_NUMERICAL_ARTIFACTS_PRESCORE_FREEZE_2026-10-20.md",
                  "10deef50abcc5b798d0893226abfd613842cf166c657567294e7a03f51e668fa"),
            _File("report", "research/R132/R132_TAYLOR_JONKER_1978_REPLICATOR_TRAJECTORIES_AND_NUMERICAL_ARTIFACTS_SCIENTIFIC_REPORT_2026-10-20.md",
                  "29e9379071b749ee6230f96ee8683c5296556c6cb96e4561e81949256ae3f47f"),
            _File("receipt", "research/R132/R132_PHASE_A_70_TEST_84_EXACT_STATES_RPS_ARTIFACT_CI_ACCEPTANCE.json",
                  "a779b3e219147d5664bd41ed0278833e0034773ccead892e1b7edbb8c0123ac1"),
            _File("model", "research/R132/r132_taylor_jonker_1978_replicator_trajectories.py",
                  "02e9f7a8bb1bc1d7f017ae831141e9ae98de4ef0d04d93004c32fa6eb68a36f2"),
            _File("experiment", "research/R132/test_r132_taylor_jonker_1978_replicator_trajectories.py",
                  "df931f98e5325907509fdb9eb9b0d98438cb028cd42020e6e94367244de195b1"),
            _File("freeze", "protocols/R132_TAYLOR_JONKER_1978_REPLICATOR_TRAJECTORY_EULER_DISCRETE_FREEZE_2026-10-20.md",
                  "816d226ccb47e498b492e583cdae15d245358b8b086b5391cc65a857d76b462b"),
            _File("report", "research/R132/R132_TAYLOR_JONKER_1978_FULL_REPLICATOR_TRAJECTORIES_EULER_ARTIFACT_SCIENTIFIC_REPORT_2026-10-20.md",
                  "1a4970e385c8f8c2bb8bfdd3523f27284c10527ca8eff5148b0553a7cd6bdbbf"),
            _File("receipt", "research/R132/R132_PHASE_B_70_TEST_216_TRAJECTORIES_CI_ACCEPTANCE.json",
                  "4401f9426307ce3ea1763e009166edabd1db1722718c849337bc62478b97ca54"),
        ),
    ),
    "R233": _Profile(
        "Measurement Invariance",
        "Eight artificial two-group measurement worlds with 256 exact exogenous atoms and observational alias pairs for measurement and latent changes.",
        (
            _File("source", "research/R233/R233_FINAL_ACCEPTANCE_STATUS.json",
                  "136c6137d076873cccbb232dadba30aec1fc20a38da79825c3e5aa79eb560b65"),
            _File("model", "research/R233/r233_exact_measurement_invariance.py",
                  "2ee077f4d1b895132a83768652dda11d6c29d014f638cc2cba979f8d091c3ff5"),
            _File("dataset", "research/R233/R233_ALL_256_ORIGINAL_TWO_GROUP_MEASUREMENT_SOURCES.csv",
                  "98c5b7f73f66a9c47f0106d20e13e516499de36fe81320b0a16f5223c2019a78"),
            _File("results", "research/R233/R233_EXACT_RESULTS.json",
                  "9a69bf114acd403b7a4ff5e6de2b521c97bc369bffedd79d48956fc5bb928c08"),
            _File("freeze", "protocols/R233_MEASUREMENT_INVARIANCE_8_TWO_GROUP_WORLDS_256_ORIGINAL_ATOMS_PRESCORE_FREEZE_2026-10-23.md",
                  "2d5e019faf159b6f4340b4ae3fc9a12b7ed4e831c98a74f19574445b8e1e1707"),
            _File("report", "research/R233/R233_SCIENTIFIC_REPORT_2026-10-23.md",
                  "d26eaedc5c408d2df166ef44d64d73a20518095493125ff0972c093c85bb9808"),
            _File("receipt", "research/R233/R233_FINAL_MACHINE_ACCEPTANCE.json",
                  "3abeb8b458b9d5e83bbff1549ac5164541635af3880e79ad28f5cea109ae173f"),
        ),
    ),
}

_RECEIPT_HASH_MAPS = {
    "R123": ("code_test_report_SHA256",),
    "R132": ("core_code_test_science_report_SHA256", "core_source_test_scientific_report_SHA256"),
}


def catalog() -> list[dict]:
    return [{"research_id": research_id, "label": profile.label, "scope": profile.scope}
            for research_id, profile in _PROFILES.items()]


def _git(repo: Path, *arguments: str, error: str) -> bytes:
    if not _GIT:
        raise SourceError("Local Git executable is unavailable")
    command = [_GIT, "--no-replace-objects", "-c", "core.fsmonitor=false", "-C", str(repo), *arguments]
    try:
        return subprocess.run(command, capture_output=True, env=_GIT_ENV, check=True, timeout=15).stdout
    except (OSError, subprocess.SubprocessError) as exc:
        raise SourceError(error) from exc


def _committed_file(repo: Path, commit: str, file: _File) -> tuple[dict, bytes]:
    entry = _git(repo, "ls-tree", "-z", commit, "--", file.path,
                 error=f"Cannot read committed tree for {file.path}")
    if not entry:
        raise SourceError(f"Missing committed file {file.path}")
    match = re.fullmatch(rb"(100644|100755) blob ([0-9a-f]{40})\t" + re.escape(file.path.encode()) + rb"\0", entry)
    if not match:
        raise SourceError(f"Expected a regular committed file without symlinks at {file.path}")
    blob = match[2].decode("ascii")
    size = _git(repo, "cat-file", "-s", blob, error=f"Cannot size Git blob for {file.path}").strip()
    if not size.isdigit() or not 0 < int(size) <= _DOCUMENT_LIMIT:
        raise SourceError(f"Malformed or oversized committed file {file.path}")
    raw = _git(repo, "cat-file", "blob", blob, error=f"Cannot read Git blob for {file.path}")
    header = f"blob {len(raw)}\0".encode("ascii")
    if len(raw) != int(size) or hashlib.sha1(header + raw, usedforsecurity=False).hexdigest() != blob:
        raise SourceError(f"Git blob hash mismatch for {file.path}")
    return {"role": file.role, "path": file.path, "commit": commit, "blob": blob,
            "sha256": hashlib.sha256(raw).hexdigest(), "size": len(raw)}, raw


def _worktree_bytes(repo: Path, path: str) -> bytes:
    directories = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    parts = path.split("/")
    fd = None
    try:
        fd = os.open(repo, directories)
        for directory in parts[:-1]:
            child = os.open(directory, directories, dir_fd=fd)
            os.close(fd)
            fd = child
        file = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=fd)
        with os.fdopen(file, "rb") as handle:
            if not stat.S_ISREG(os.fstat(handle.fileno()).st_mode):
                raise SourceError(f"Expected a regular worktree file at {path}")
            return handle.read(_DOCUMENT_LIMIT + 1)
    except FileNotFoundError as exc:
        raise SourceError(f"Missing worktree file {path}") from exc
    except OSError as exc:
        raise SourceError(f"Cannot read regular worktree file without symlinks at {path}") from exc
    finally:
        if fd is not None:
            os.close(fd)


def _strict_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def _reject_constant(_value):
    raise ValueError("non-finite JSON value")


def _json_evidence(raw: bytes, path: str, research_id: str) -> dict:
    try:
        data = json.loads(raw.decode("utf-8"), object_pairs_hook=_strict_object, parse_constant=_reject_constant)
        if not isinstance(data, dict) or data.get("research_id") != research_id:
            raise ValueError("wrong research identity")
        # Reject numeric overflow and malformed Unicode anywhere in the evidence.
        _canonical(data)
        return data
    except (ValueError, RecursionError) as exc:
        raise SourceError(f"Malformed research metadata at {path}") from exc


def _canonical(record: dict) -> bytes:
    return json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def _check_receipts(research_id, files, metadata):
    claims = [(entry, metadata[entry["path"]]) for entry in files if entry["role"] == "receipt"]
    if research_id == "R233":
        acceptance = metadata[files[0]["path"]]
        receipt = claims[0][1]
        by_role = {entry["role"]: entry for entry in files}
        for role, source_key, receipt_key in (("dataset", "source_sha256", "source_sha256"),
                                             ("results", "results_sha256", "result_sha256")):
            entry = by_role[role]
            if not entry["sha256"] == acceptance.get(source_key) == receipt.get(receipt_key):
                raise SourceError(f"Research receipt hash mismatch for {entry['path']}")
        return

    artifacts_by_role = [[entry for entry in files if entry["role"] == role]
                         for role in ("model", "experiment", "report")]
    phase_artifacts = zip(*artifacts_by_role, strict=True)
    for (entry, receipt), field, artifacts in zip(claims, _RECEIPT_HASH_MAPS[research_id], phase_artifacts, strict=True):
        original_hashes = receipt.get(field)
        if not isinstance(original_hashes, dict):
            raise SourceError(f"Malformed research receipt hash map at {entry['path']}")
        expected_hashes = {Path(artifact["path"]).name: artifact["sha256"] for artifact in artifacts}
        if original_hashes != expected_hashes:
            raise SourceError(f"Research receipt hash mismatch at {entry['path']}")


def capture(repo: Path | str, research_id: str, commit: str | None = None) -> dict:
    if not isinstance(research_id, str) or research_id not in _PROFILES:
        raise SourceError("Unknown curated research source")
    main = commit is None
    if main:
        commit = MAIN_COMMIT
    if not isinstance(commit, str) or not _OBJECT_ID.fullmatch(commit):
        raise SourceError("Expected a full lowercase Git commit ID")

    try:
        repo = Path(repo).resolve(strict=True)
        top = os.fsdecode(_git(repo, "rev-parse", "--show-toplevel", error="Missing trusted Git worktree").rstrip(b"\n"))
        if Path(top).resolve(strict=True) != repo:
            raise SourceError("Source repository must be the root of the Git worktree")
    except (OSError, TypeError, RuntimeError) as exc:
        raise SourceError("Missing trusted Git worktree") from exc

    if _git(repo, "cat-file", "-t", commit, error="Missing local source commit").strip() != b"commit":
        raise SourceError("Source selector must identify a commit object")
    if main:
        tip = _git(repo, "show-ref", "--hash", "--verify", MAIN_REF, error="Missing local origin/main reference").strip()
        _git(repo, "merge-base", "--is-ancestor", commit, tip.decode("ascii"),
             error="Pinned source commit is outside local origin/main history")

    profile = _PROFILES[research_id]
    origin = "MAIN" if main else "CANDIDATE"
    warnings = [] if main else ["Candidate sources are browse only."]
    files = []
    metadata = {}
    for file in profile.files:
        entry, raw = _committed_file(repo, commit, file)
        if entry["sha256"] != file.sha256:
            if main:
                raise SourceError(f"Pinned SHA-256 mismatch for {file.path}")
            warnings.append(f"Candidate file differs from pinned public evidence at {file.path}")
        try:
            if _worktree_bytes(repo, file.path) != raw:
                raise SourceError(f"Worktree drift from committed source at {file.path}")
        except SourceError as exc:
            if main:
                raise
            warnings.append(str(exc))
        files.append(entry)
        if file.path.endswith(".json"):
            metadata[file.path] = _json_evidence(raw, file.path, research_id)

    _check_receipts(research_id, files, metadata)
    acceptance = metadata[files[0]["path"]]
    if not isinstance(acceptance.get("scientific_status"), str) or not acceptance["scientific_status"].strip():
        raise SourceError("Malformed scientific status in source metadata")
    public_original = files[0]["sha256"] == profile.files[0].sha256
    identity = {"research_id": research_id, "commit": commit, "origin": origin, "files": files}
    return {
        **identity,
        "schema_version": "1.0.0",
        "source_id": hashlib.sha256(_canonical(identity)).hexdigest(),
        "label": profile.label,
        "scope": profile.scope,
        "permission": "BROWSE_ONLY",
        "engineering_status": "MAIN_PIN_VERIFIED" if main else "CANDIDATE_CONTENT_VERIFIED",
        "warnings": warnings,
        "scientific_status": acceptance["scientific_status"] if public_original else "UNVERIFIED_CANDIDATE",
        "original_metadata": acceptance if public_original else None,
    }


def verify(repo: Path | str, record: dict) -> dict:
    if not isinstance(record, dict) or record.get("origin") not in ("MAIN", "CANDIDATE"):
        raise SourceError("Malformed registered source record")
    commit = record.get("commit")
    if not isinstance(commit, str) or not _OBJECT_ID.fullmatch(commit):
        raise SourceError("Malformed registered source commit")
    current = capture(repo, record.get("research_id"), None if record["origin"] == "MAIN" else commit)
    try:
        matches = _canonical(record) == _canonical(current)
    except (TypeError, ValueError, RecursionError) as exc:
        raise SourceError("Malformed registered source record") from exc
    if not matches:
        raise SourceError("Registered source metadata or hash mismatch")
    return current
