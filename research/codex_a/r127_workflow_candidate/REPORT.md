# R127 candidate workflow repair preparation

Recorded 2026-11-11 11:50 Asia/Shanghai. Base main:
`ce6ae2dbf96f5346cf5062de3773b72c0ab90446` (tree
`b3109aec08c60fcd4ba2050f9d19a252f9f7eadf`). Scope: Codex A engineering only.

## Outcome and ownership

**COMPLETE**: exact guarded three-file candidate patch; actual original60 test /
138 result-leaf execution in disposable repositories under normal and optimized
Python; fail-closed negative controls; immutable Git sidecar publication to LOCAL
bare repositories; no-op and conflict controls; reverse-patch rollback test.

**PARTIAL**: production repair preparation. The real workflow, existing gate,
protocol, model, test, scientific report and historical receipt are untouched.
R-mainline must review/apply the candidate and approve the new sidecar archival
location/remote-advance policy. This PR does not activate the workflow.

**NOT_RUN**: actual Actions CI, Python3.11, historical CI log authentication,
external authentication of run/attempt/numeric job ID/time, scientific acceptance,
new human scoring or E2/E3. Local runtime was Python3.12.14. No paid resource,
dependency installation or workflow dispatch was used.

## Real obstruction and minimal change

PR26 gate is merged but the old production workflow still uses inline asserts
and its permissive log parser. `historical_controls.py` extracts those exact
inline blocks from the fixed base. With synthetic upstream snapshots, optimized
Python accepts bad E2=7, participants=108 and deviations=75118. It writes outer
E2=0 even with upstream E2=7. The normal parser accepts FAILED followed by OK;
optimization also accepts wrong/duplicate test counts. These are isolated inline
controls, **not proof of a full CI bypass**: original shell pipefail still matters.
The old unchanged-receipt unconditional Git commit also exits1.

Reuse `r127_local_gates/gate.py` rather than another mathematical validator:

* `run_workflow.py` authenticates tracked entry/gate/pins, runs gate26's isolated
  original commands, validates their raw streams and all138 typed result leaves,
  derives E2 upstream, and writes one immutable run/attempt/job-key sidecar.
* `publish.py` revalidates raw evidence and fixed source identities, stages only
  that sidecar, treats identical already-tracked bytes as exit0/no new commit,
  rejects rewritten receipts, unrelated changes and remote-main advances. Normal
  push and remote readback only; no rebase, force or deletion.
* `workflow.template.yml` wires these entries in the proposed workflow. The
  frozen protocol requires Git archival, so artifact-only upload was not adopted.
* `prepare.py` prints `candidate.patch` and `candidate_manifest.json`. Only the
  workflow, its pin entry and gate's pin-manifest SHA constant differ. Gate logic
  is unchanged. Original source/test/report/receipt pins are preserved. Stale or
  partially changed target bytes reject; already-applied candidates return no-op.

Claimed GitHub env IDs are recorded as claims. `job_key` is not numeric job ID;
`numeric_job_id=null`, `externally_attested=false`. Source identity and local
execution validation do not authenticate the external CI service. Old run
39348775741 is not re-attested here. No new source-data collection occurred.

## Reproduce and inspect

From repository root (Python stdlib only):

```sh
python3 -B -m unittest discover -s research/codex_a/r127_workflow_candidate -p test_candidate.py -v
python3 -B -O -m unittest discover -s research/codex_a/r127_workflow_candidate -p test_candidate.py -v
python3 -B research/codex_a/r127_workflow_candidate/prepare.py .
python3 -B research/codex_a/r127_workflow_candidate/prepare.py . --manifest
python3 -B research/codex_a/r127_workflow_candidate/exercise.py . --output /tmp/r127-candidate-fresh
python3 -B research/codex_a/r127_workflow_candidate/historical_controls.py . --receipt /tmp/r127-candidate-fresh/normal-sidecar.json --output /tmp/r127-old-fresh
```

Both output directories must not already exist. `prepare.py` only prints; do not
apply the patch to the real R workflow without its owner's authorization.
`exercise.py` applies it solely in disposable clones and explicitly replaces
origin with a temp LOCAL bare repository before executing publication shells.
It extracts and executes both exact candidate YAML Bash bodies; this is not an
Actions runner simulation or an actual GitHub run.

Final fixture commit `f3896820fe0b7625b459e432cca42bd3dacceb30`, tree
`669f30b266c64d05e477e21eae9f8c7676d31798`, is a **local test fixture**, not a
GitHub delivery commit. `integration-final/candidate.bundle` in the evidence
archive preserves it; `git bundle verify` succeeded. Prerequisite is base ce6.
A disposable clone can fetch that bundle's HEAD and detach it to inspect the
exact tested tree. Do not push fixture commits or synthetic receipts to main.

## Actual results

| Check | Normal | Optimized |
|---|---|---|
| New boundary/patch unit methods | 7 pass | 7 pass |
| Original mathematical test methods | 60 pass | 60 pass |
| Original stage-two typed fields | 138 matched | 138 matched |
| Invalid/count/log/E2/aggregate/enumeration/immutable/staged/remote/source controls | 9 rejected | 9 rejected |
| Sidecar-only LOCAL Git publication | pass | pass |
| Identical publication retry | exit0, same commit | exit0, same commit |
| Old unchanged-receipt Git commit | expected exit1 | expected exit1 |
| Historical receipt and four frozen source objects | unchanged | unchanged |

Historical inline controls:16 actual subprocess cases, all expected outcomes
matched. Initial RED stub:7 methods with8 assertion/subtest failures; retained
`red.log`. Final GREEN logs are archived. No known test failure was relabeled as
scientific success.

`evidence.tar.gz` + `evidence_members.json` contain final raw child streams,
commands, old controls, local Git bundle, source identities, rollback record,
source-only PR snapshots and independent review. Every member has length/SHA256.
`sources.json` authenticates20 base files, including protocol/workflow/gate/pins,
queue, workflow requirements and R-mainline handoffs. `artifact_hashes.json`
identifies this package. Exact patch SHA256:
`ed2b03c7985d93db9c915abaa4e3bffeae665803dbd00db8364eba14a62cf44e`.

Key unchanged source hashes:

* original workflow blob `4b22f653dc7516bb31ead23e45dcf7f62261d79d`, SHA256
  `77fefd0b06a896232b4cc4a7679b1633051f19eba9d082e062faa8e9d2ace586`;
* gate blob `a06c3266541785886356baacbc520beb8cdfcb78`, SHA256
  `521a4a48e88ffaaae29bab333950d62909f3eef7b284b41c1a8c1f6fbd310cb5`;
* historical receipt blob `55bdf82b9e7869c63d46aa4f76ba6bc672dddecb`, SHA256
  `303402ce0a505b46b19c7ed3dbaa153629661d5586230dcb1c254b1a216ed7c9`;
* frozen protocol blob `4734ede5133701d622acfda76c4f9474bf660b21`, SHA256
  `15bb9f0fdfe961968ef1ffd751e55f036dcbc6cd3448bbd67cfd0f32592bfbc2`.

## Rollback, limits and next queue

Reverse apply/check actually restored all three target files byte-for-byte in a
temp clone. After future deployment, disable/revert candidate workflow wiring in
a new owner-approved commit; preserve every existing historical and new sidecar
receipt. Never reset public history. If a remote race/push fails after a local
commit, publisher stops and leaves it local for inspection; it does not retry by
rebasing. Receipt-path validation follows file reading, so the publisher is a
fixed-template entry, not a generic untrusted file-reading service.

Fresh read-only independent reviewer found no Critical/Important issues and ran
7 lightweight candidate tests; no math suites repeated for review.

05-003 remains provisional and pending itemwise scientific audit; CLOSED_BOUNDED
is not promoted. Source identities/log correctness do not establish new human
prediction, transition identification or historical CI provenance. R073/PESEN
and frozen experimental parameters remain unchanged.

Next R127 task: R-mainline review of candidate patch, sidecar archival location,
remote concurrency policy and required external run authentication; confirm free
CI and test the actual Python3.11 runner only after approval. Separate R077
checklist package closes adoption/evidence checks without scoring data. PR30
metadata review is acceptable but unmerged/unauthorized. Newly observed B PR31
owns its scalar/independent-integer readiness audit; do not duplicate that math.
Delivery: [draft PR32](https://github.com/edwardsage419/Psychohistory-Research/pull/32),
implementation commit `41b13d97882fec225ec9d6b88311e1cec2ed83b0`.
`DELIVERY.json` records remote commit and5 critical blob readbacks, empty Actions
run/check lists (NOT_RUN), unchanged main and no merge. Later metadata-only
delivery commits do not replace the locally bundled candidate test identity.
Companion R077 checklist is independent draft PR33. No main merge performed.
