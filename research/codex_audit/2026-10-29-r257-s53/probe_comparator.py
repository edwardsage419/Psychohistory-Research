#!/usr/bin/env python3
"""Nonblind forensic probes of the archived comparator; no historical edits."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
bp = root / "research/evidence_audit/b_r257_s53_independent_1d_20261029.py"
rp = root / "research/validation/r257_s53_capacity_shadow_20261029.py"
jp = root / "research/validation/R257_S53_EXACT_RECEIPT_2026-10-29.json"
spec = importlib.util.spec_from_file_location("archived_b", bp)
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)
receipt = json.loads(jp.read_text())
run = subprocess.run([sys.executable, str(rp)], text=True, capture_output=True, check=True)
assert json.loads(run.stdout) == receipt
assert b.compare(receipt) == 72
probes = {}
def probe(name, mutate, expected_accepted):
    data = copy.deepcopy(receipt)
    mutate(data)
    try:
        accepted = b.compare(data) == 72
    except (AssertionError, KeyError, ValueError):
        accepted = False
    assert accepted == expected_accepted, (name, accepted)
    probes[name] = {"accepted_by_archived_comparator": accepted,
                    "expected_for_complete_protocol_gate": False}
probe("wrong_minimum", lambda d: d["worlds"][0]["perturbations"][0].update(minimum="999"), False)
probe("duplicate_world_omits_seven_worlds", lambda d: d.update(worlds=[copy.deepcopy(d["worlds"][0]) for _ in range(8)]), True)
probe("duplicate_capacity_omits_one_scenario", lambda d: d["worlds"][0]["perturbations"].__setitem__(4, copy.deepcopy(d["worlds"][0]["perturbations"][0])), True)
probe("wrong_baseline_multiplier", lambda d: d["worlds"][1].update(baseline_lambda="999"), True)
probe("wrong_capacity_delta_identity", lambda d: d["worlds"][0]["perturbations"][0].update(delta="999"), True)
probe("wrong_local_derivative", lambda d: d["worlds"][1].update(local_derivative="999"), True)
probe("wrong_evidence_label", lambda d: d.update(evidence="E3"), True)
result = {"status":"COMPLETE", "scope":"nonblind comparator forensic audit, not model acceptance",
          "python":platform.python_version(), "platform":platform.platform(),
          "baseline_r_assertions_reported":127, "baseline_b_comparisons":72,
          "r_output_matches_archive":True, "probe_expectations_passed":len(probes),
          "probe_expectations_failed":0, "probes":probes,
          "source_sha256":{str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (bp,rp,jp)}}
print(json.dumps(result, indent=2))
