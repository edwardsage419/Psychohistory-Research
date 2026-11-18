import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from psychohistory import sources


REPO = Path(__file__).resolve().parents[3]
BASE = "7ea6eab94433e3669b6f492d802bb35316dc90d6"
ACCEPTANCE = "research/R123/R123_FINAL_ACCEPTANCE_STATUS.json"
MODEL = "research/R123/r123_degroot_1974_berger_1981_exact_consensus.py"


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args], stderr=subprocess.PIPE)


class SourcesTest(unittest.TestCase):
    def test_public_sources_keep_distinct_original_evidence_and_file_identities(self):
        catalog = sources.catalog()
        self.assertEqual([entry["research_id"] for entry in catalog], ["R123", "R132", "R233"])
        cases = [
            ("R123", {"source": 1, "model": 1, "experiment": 1, "freeze": 1},
             "total_synthetic_stochastic_matrices_verified", 226),
            ("R132", {"source": 1, "model": 2, "experiment": 2, "freeze": 2},
             "additional_phase_B_analytic_vs_RK4_mathematical_trajectory_cases", 216),
            ("R233", {"source": 1, "model": 1, "dataset": 1, "results": 1, "freeze": 1},
             "original_full_source_atoms", 256),
        ]
        for research_id, role_counts, evidence_key, evidence_value in cases:
            with self.subTest(research_id=research_id):
                record = sources.capture(REPO, research_id)
                self.assertEqual((record["commit"], record["origin"], record["permission"]),
                                 (BASE, "MAIN", "BROWSE_ONLY"))
                self.assertRegex(record["source_id"], "^[0-9a-f]{64}$")
                self.assertEqual(record["original_metadata"][evidence_key], evidence_value)
                self.assertEqual(record["scientific_status"], record["original_metadata"]["scientific_status"])
                for role, count in role_counts.items():
                    self.assertEqual(sum(entry["role"] == role for entry in record["files"]), count)
                for entry in record["files"]:
                    raw = git(REPO, "show", f'{BASE}:{entry["path"]}')
                    blob = git(REPO, "rev-parse", f'{BASE}:{entry["path"]}').decode().strip()
                    self.assertEqual((entry["commit"], entry["blob"], entry["sha256"], entry["size"]),
                                     (BASE, blob, hashlib.sha256(raw).hexdigest(), len(raw)))
                self.assertEqual(sources.verify(REPO, record), record)

    def test_explicit_commit_stays_browse_only_and_ignores_git_selector_environment(self):
        main = sources.capture(REPO, "R123")
        with patch.dict(os.environ, {"GIT_DIR": "/nonexistent/replacement", "GIT_WORK_TREE": "/nonexistent"}):
            candidate = sources.capture(REPO, "R123", BASE)
        self.assertEqual((candidate["origin"], candidate["permission"]), ("CANDIDATE", "BROWSE_ONLY"))
        self.assertNotEqual(candidate["source_id"], main["source_id"])
        self.assertEqual(candidate["files"], main["files"])
        self.assertEqual(sources.verify(REPO, candidate), candidate)

    def test_selectors_and_persisted_file_metadata_cannot_bypass_verification(self):
        for research_id, commit in [("../R123", None), ("R123", "HEAD"), ("R123", BASE[:12]),
                                    ("R123", "0" * 40), ("R123", BASE + ":" + MODEL)]:
            with self.subTest(research_id=research_id, commit=commit):
                with self.assertRaises(sources.SourceError):
                    sources.capture(REPO, research_id, commit)
        record = sources.capture(REPO, "R123")
        for key, value in [("path", "../../.git/config"), ("blob", "0" * 40), ("sha256", "0" * 64)]:
            with self.subTest(key=key):
                altered = copy.deepcopy(record)
                altered["files"][0][key] = value
                with self.assertRaises(sources.SourceError):
                    sources.verify(REPO, altered)
        record["permission"] = "EXECUTE"
        with self.assertRaises(sources.SourceError):
            sources.verify(REPO, record)

    def test_main_rejects_drift_missing_files_and_symlinks(self):
        with tempfile.TemporaryDirectory() as root:
            repo = Path(root) / "repo"
            self.checkout_evidence(repo)
            record = sources.capture(repo, "R123")
            path = repo / ACCEPTANCE
            original = path.read_bytes()
            path.write_bytes(original + b"\n")
            with self.assertRaisesRegex(sources.SourceError, "[Dd]rift"):
                sources.verify(repo, record)
            path.unlink()
            with self.assertRaisesRegex(sources.SourceError, "[Mm]issing"):
                sources.verify(repo, record)
            path.symlink_to(REPO / ACCEPTANCE)
            with self.assertRaisesRegex(sources.SourceError, "[Ss]ymlink|[Rr]egular"):
                sources.verify(repo, record)
            candidate = sources.capture(repo, "R123", BASE)
            self.assertTrue(any("worktree" in warning.lower() for warning in candidate["warnings"]))

    def test_candidate_metadata_is_read_only_and_uses_committed_bytes(self):
        with tempfile.TemporaryDirectory() as root:
            repo = Path(root) / "repo"
            self.checkout_evidence(repo)
            path = repo / ACCEPTANCE
            data = json.loads(path.read_bytes())
            data["scientific_status"] = "candidate text that must not be disclosed"
            path.write_text(json.dumps(data), encoding="utf-8")
            commit = self.commit(repo, ACCEPTANCE)
            path.write_text("working-tree change", encoding="utf-8")
            candidate = sources.capture(repo, "R123", commit)
            self.assertEqual(candidate["commit"], commit)
            self.assertEqual(candidate["permission"], "BROWSE_ONLY")
            self.assertNotIn(data["scientific_status"], json.dumps(candidate))
            self.assertEqual(path.read_text(encoding="utf-8"), "working-tree change")
            self.assertTrue(any("drift" in warning.lower() for warning in candidate["warnings"]))

    def test_candidate_rejects_invalid_json_mismatched_receipts_and_committed_symlinks(self):
        with tempfile.TemporaryDirectory() as root:
            repo = Path(root) / "repo"
            self.checkout_evidence(repo)
            path = repo / ACCEPTANCE
            original = path.read_bytes()
            path.write_text('{"research_id":"R123","research_id":"R233"}', encoding="utf-8")
            commit = self.commit(repo, ACCEPTANCE)
            with self.assertRaisesRegex(sources.SourceError, "[Mm]alformed"):
                sources.capture(repo, "R123", commit)
            path.write_bytes(original)
            (repo / MODEL).write_text("raise AssertionError('must not execute')\n", encoding="utf-8")
            commit = self.commit(repo, ACCEPTANCE, MODEL)
            with self.assertRaisesRegex(sources.SourceError, "[Hh]ash mismatch"):
                sources.capture(repo, "R123", commit)
            path.unlink()
            path.symlink_to(REPO / ACCEPTANCE)
            commit = self.commit(repo, ACCEPTANCE)
            with self.assertRaisesRegex(sources.SourceError, "[Ss]ymlink|[Rr]egular"):
                sources.capture(repo, "R123", commit)

    def test_unrelated_local_main_ref_cannot_approve_a_main_record(self):
        with tempfile.TemporaryDirectory() as root:
            repo = Path(root) / "repo"
            self.checkout_evidence(repo)
            tree = git(repo, "rev-parse", "HEAD^{tree}").decode().strip()
            unrelated = git(repo, "-c", "user.name=Tests", "-c", "user.email=tests@example.invalid",
                            "commit-tree", tree, "-m", "Unrelated root").decode().strip()
            git(repo, "update-ref", "refs/remotes/origin/main", unrelated)
            with self.assertRaises(sources.SourceError):
                sources.capture(repo, "R123")
            self.assertEqual(sources.capture(repo, "R123", BASE)["origin"], "CANDIDATE")

    def test_replacement_refs_cannot_redirect_a_commit(self):
        with tempfile.TemporaryDirectory() as root:
            repo = Path(root) / "repo"
            self.checkout_evidence(repo)
            record = sources.capture(repo, "R123")
            path = repo / ACCEPTANCE
            original = path.read_bytes()
            path.write_bytes(original + b"\n")
            replacement = self.commit(repo, ACCEPTANCE)
            path.write_bytes(original)
            git(repo, "replace", BASE, replacement)
            self.assertEqual(sources.verify(repo, record), record)

    def test_replicator_receipt_cannot_claim_artifacts_from_the_other_phase(self):
        with tempfile.TemporaryDirectory() as root:
            repo = Path(root) / "repo"
            self.checkout_evidence(repo, "R132")
            phase_a, phase_b = sorted((repo / "research/R132").glob("R132_PHASE_*_CI_ACCEPTANCE.json"))
            first, second = (json.loads(path.read_bytes()) for path in (phase_a, phase_b))
            field_a = "core_code_test_science_report_SHA256"
            field_b = "core_source_test_scientific_report_SHA256"
            first[field_a], second[field_b] = second[field_b], first[field_a]
            phase_a.write_text(json.dumps(first), encoding="utf-8")
            phase_b.write_text(json.dumps(second), encoding="utf-8")
            commit = self.commit(repo, str(phase_a.relative_to(repo)), str(phase_b.relative_to(repo)))
            with self.assertRaisesRegex(sources.SourceError, "[Hh]ash mismatch"):
                sources.capture(repo, "R132", commit)

    def test_candidate_warns_when_committed_files_differ_from_pinned_public_evidence(self):
        with tempfile.TemporaryDirectory() as root:
            repo = Path(root) / "repo"
            self.checkout_evidence(repo)
            freeze = next((repo / "protocols").glob("R123_*"))
            freeze.write_bytes(freeze.read_bytes() + b"\n")
            commit = self.commit(repo, str(freeze.relative_to(repo)))
            candidate = sources.capture(repo, "R123", commit)
            self.assertTrue(any("pinned" in warning.lower() and freeze.name in warning
                                for warning in candidate["warnings"]))

    def checkout_evidence(self, repo, research_id="R123"):
        git(REPO, "clone", "--shared", "--no-checkout", "--quiet", str(REPO), str(repo))
        git(repo, "update-ref", "refs/remotes/origin/main", BASE)
        git(repo, "reset", "--mixed", BASE)
        include = (f"research/{research_id}/", f"protocols/{research_id}_")
        for raw_path in git(repo, "ls-tree", "--name-only", "-r", BASE, include[0], "protocols").splitlines():
            relative = raw_path.decode()
            if relative.startswith(include):
                path = repo / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(git(repo, "show", f"{BASE}:{relative}"))

    def commit(self, repo, *paths):
        git(repo, "add", "--", *paths)
        git(repo, "-c", "user.name=Tests", "-c", "user.email=tests@example.invalid",
            "commit", "--quiet", "-m", "Candidate sources")
        return git(repo, "rev-parse", "HEAD").decode().strip()
