# A1 — Codex A v2.0 unfinished PR review

track: Codex A engineering
subflow: A1 independent review and integration preparation
run_date: 2026-11-10T23:41:20.901740+00:00
observed_head: 3221a84fba91731071b8931447837e07578210be
status: COMPLETE for bounded engineering review; PARTIAL for production adoption
ci_status: NOT_RUN
billing_checked: no paid service, dependency installation or workflow dispatch; free CI quota NOT_VERIFIED
commit_sha: supplied by this versioned PR; initial review f804fe1f preserved
source_links: docs/PROJECT_WORKFLOW_REQUIREMENTS_V2_2026-10-24.md; docs/RESEARCH_SYNC_WORKFLOW_2026-10-15.md; GitHub PRs 21–27
output_paths: research/codex_a/pr21_23_review/
evidence_scope: native engineering replay and negative controls, no new scientific acceptance

## Selection and work performed

The user supplied Codex A engineering v2.0. Its A1 is PR review, not the older source-tool roadmap label. Main's 154-item scientific queue, R077/R290/R300 acceptance status, target prescore/ODD pins, existing A/B handoffs and the latest seven open PRs were checked. #25 had not been independently replayed by A; #27 is new. Their mathematical implementations remain B-owned and unchanged.

Real sequential local merges of all seven fixed heads succeeded in an isolated clone on current main. Reused main's audit_queue.py: 21 PR pairs and seven main comparisons have no text conflict; proposed paths do not overlap. No remote merge was performed. The candidate snapshot pins #24's previous head; this A-only test/docs increment changes no underlying research executable or candidate numerical algorithm.

## Results and disposition

| PR | Engineering recommendation | Evidence / remaining boundary |
|---|---|---|
| #21 S75 | Eligible for owner merge review | Existing independent replay retained; 12 source fingerprints unchanged |
| #22 S78 | Eligible for owner merge review | Existing replay retained; 13 fingerprints unchanged; paired certificate still nonblind E1 |
| #23 S85 | Eligible for owner merge review | Existing replay retained; 14 fingerprints unchanged; no claim about arbitrary chronological implementations |
| #24 A review | Eligible for owner merge review | Existing entry reused/extended; no second framework |
| #25 S86 | Eligible for owner merge review | New A replay: original4+candidate12 methods per mode, 273 result leaves, 8 bad inputs rejected per mode |
| #26 R127 gate | Local candidate only; mainline integration remains open | Five original source pins unchanged; workflow P0 production repair NOT_APPLIED |
| #27 S96 | Eligible for owner merge review | New A replay: candidate12 methods per mode, 176 leaves/2016 source fields, 8 bad inputs rejected per mode |

#25 and #27 full replays passed normal/-O: four exits 0, 56 existing/candidate method executions, 192 stdout/stderr hash records rechecked and 14 source fingerprints per replay unchanged. #25 retained five original false accepts and three original correct rejections, and regenerated its JSON only (no archived CSV emitter). #27 retained five original false accepts/three correct rejections; its NEW adapter calls unmodified original exports, not an original-author CLI. Both regenerated outputs match their archived bytes. These existing B discoveries are not counted as new A discoveries.

The A test file now exports the fixed #25/#27 dependencies and artifacts alongside existing #22/#23 targets. Each mode passes 12 methods and 61 real CLI calls. New permanent cases cover metadata bool/float confusion, duplicate model identities, independent CSV/result ordering, nested duplicate JSON keys, nonfinite values and missing/extra success-shaped fields. Wrong default-parser copies yield eight expected assertion failures. No B numerical implementation defect was found in this scope, so none was invented or patched.

A fresh read-only review found no important issue in the incremental tests; all 17 exported objects matched their fixed Git sources and added artifacts matched current main. Old #21–#23/#26 native replays were NOT repeated: source/code identities were checked against their fixed prior receipts instead. Earlier A tests were rerun because the shared test entry was extended.

## Commands, sources and limits

Run existing candidate replay.py --output NEW_DIRECTORY for #25/#27 under python3 -B and python3 -O -B in an isolated clone with the pinned heads loaded. Exact argv, raw streams, source Git blobs/SHA256, fixed heads, candidate tree, queue inventory and case records are in a1_v2_evidence.tar.gz. Member hashes are listed in a1_v2_evidence_members.json; all members were reverified. Previous evidence.tar.gz remains unchanged. The fixed source anchor in the CLI tests remains 25bcd51d; those artifact bytes are identical on starting main3221a84f.

```sh
python3 -B research/codex_a/pr21_23_review/test_cli_contracts.py -v
python3 -O -B research/codex_a/pr21_23_review/test_cli_contracts.py -v
```

All seven PRs remain drafts/unmerged. There is no automatic extension of #1–#20 merge authorization. CI absence is NOT CI PASS. Production binding, Python3.11, whole-repository tests, other platforms and formal scientific acceptance remain NOT_RUN. R290/R300 retain their bounded artificial E1 status; human/E2/E3/external-team evidence and formal queue closures added=0. Original R077 exact-tie failure remains unresolved in the historical program.

blockers: owner authorization for adoption; production wiring and R077 exact probability/source qualification remain separate gates.
next_action: proceed to A2 R077 reversible, fail-closed integration preflight using B's existing exact supplement, without editing B mathematics or frozen historical scoring.
