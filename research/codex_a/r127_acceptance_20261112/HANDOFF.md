# R127 engineering acceptance and PR30–33 integration handoff

track: Codex A engineering
subflow: R127 workflow candidate acceptance; R077 pending-PR integration
run_date: 2026-11-12 UTC
observed_head: d4740c2cd999b8da06a25b0ef407aeaf8a56ab6c
status: COMPLETE bounded engineering review / PARTIAL production preparation
ci_status: NOT_RUN
billing_checked: existing environment + free open-source local runtime; no paid API/CI/resource
source_links: https://github.com/edwardsage419/Psychohistory-Research/pull/32 ; PR26,30,31,33 below
output_paths: research/codex_a/r127_acceptance_20261112/
commit_sha: implementation/delivery commits recorded by the independent PR and DELIVERY.json
blockers: R-mainline workflow ownership; free-CI confirmation; external CI provenance; B-owned pin adoption
next_action: owner review of fixed R127 patch, coordinated PR30/31 pin refresh, then explicitly authorized deployment

## Engineering decisions

| Candidate | Fixed head | Decision |
|---|---|---|
| PR30 | 8005fcb75e9e20545adb245edd45d72dbc374632 | APPROVE_CANDIDATE: two exact literal replacements; behavior and production veto preserved |
| PR31 | 03cf49d8970f273bb58ef0bfd125252166482dce | APPROVE_CANDIDATE against current main; NEEDS_FIX for the combined PR30 source pin |
| PR32 | 16778c53b2e7a2c590ff65c854b1f7034169050d | APPROVE_CANDIDATE: local3.11 and failure tests pass; activation remains BLOCKED pending owner approval |
| PR33 | 9d5041acdfc3f13a002e2cfbb6c33d4dfaed6af4 | APPROVE_CANDIDATE: source qualification only; production_ready=false and exit2 retained |

All four remain OPEN draft and were MERGEABLE at the review snapshot; no Actions
runs/checks were present. Empty lists mean NOT_RUN. PR26 is merged. Prior merge
authorization1–29 does not authorize any of30–33 or this delivery PR. No merge,
close, force update, CI dispatch or main push was performed.

Latest main differs from prior ce6ae2db only by two theory documents. Thirteen
relevant R127 sources/protocol/workflow-requirement/queue/handoff files are
byte-identical to that baseline. Old main in a historical evidence file remains
a historical fact, not an automatically stale scientific baseline. Queue05-003
is still provisional/pending itemwise scientific audit; no scientific closure.

## R127: scope, source identity and reused evidence

PR32 stores a candidate patch in Codex A's directory. The patch changes exactly:

1. `.github/workflows/r127-van-huyck-1990-coordination-source-table-60-tests.yml`
2. its workflow identity entry in `research/codex_a/r127_local_gates/pins.json`
3. the corresponding pin-manifest SHA constant in `gate.py`

The gate's implementation is reused unchanged. Its original model, tests,
scientific report and historical receipt pins do not change. R073, R077,
PESEN v0.1, R127 freeze, historical outputs and mathematical algorithms were not
modified. In this delivery even the three real target files stay unchanged:
patch application and reversal occurred only inside disposable repositories.

Fixed patch source:
`16778c53b2e7a2c590ff65c854b1f7034169050d:research/codex_a/r127_workflow_candidate/candidate.patch`
Git blob `c2926c379eb7a0c6d2a35fc830b8030a29ab6d14`; SHA256
`ed2b03c7985d93db9c915abaa4e3bffeae665803dbd00db8364eba14a62cf44e`.
The same exact patch generated/applied/reversed on latest-main+all-four-PR
fixture; all three original buffers restored byte-for-byte. Gate.capture checked
five adopted sources at the combined candidate checkout, without math execution.

Original workflow blob `4b22f653dc7516bb31ead23e45dcf7f62261d79d`, SHA256
`77fefd0b06a896232b4cc4a7679b1633051f19eba9d082e062faa8e9d2ace586`;
proposed workflow blob `d17cbee8750577a76ff386f5faebc3310adc3994`, SHA256
`e6f45b1ce4bf0b1b825f312b452828e3a6d56eefa04883600e35083be8f5c64a`.
Frozen protocol SHA256
`15bb9f0fdfe961968ef1ffd751e55f036dcbc6cd3448bbd67cfd0f32592bfbc2`.
Historical receipt SHA256
`303402ce0a505b46b19c7ed3dbaa153629661d5586230dcb1c254b1a216ed7c9`.
Full before/after identities are fixed in PR32's candidate_manifest.json;
`sources.json` inside this evidence archive authenticates current inputs.

Reused unchanged retained evidence: PR26's59 and PR32's109 archive members were
independently length/hash checked; PR32's15 current artifact entries verified.
Original inline failures (optimization removes assertions, FAILED→OK acceptance,
E2 literal0 masking upstream7, unchanged-receipt commit exit1) remain preserved.
Those isolated inline controls do not prove full old-CI bypass: original
unittest shell uses pipefail. Historical run39348775741 was not re-attested.

## Actual new Python3.11 and deployment-failure verification

Local CPython3.11.17, Clang23.1.3, OpenSSL3.5.9; installed only in the workspace
from free python-build-standalone via uv. Python executable SHA256
`ff9b2ac4362b81c68622ffb1730f7138eb269177d9846399c521a44c5daffb0e`.
The optional global executable symlink was denied by the filesystem; the absolute
workspace executable worked, so no escalation/system change was needed.
This standalone build does not authenticate GitHub setup-python's actual binary.

PATH was explicitly prefixed with that3.11 bin directory, including the candidate
YAML's literal `python` invocation. Sidecars confirm3.11.17 and matching -O flags.

| Actual new local check | Normal | Optimized |
|---|---|---|
| PR32 boundary/patch methods | 7 pass | 7 pass |
| Original R127 test methods | 60 pass | 60 pass |
| Stage-two typed fields | 138 match | 138 match |
| Source/log/E2/aggregate/enumeration/immutable/staged/remote rejection controls | 9 reject | 9 reject |
| LOCAL publication / identical retry | sidecar only / no-op | sidecar only / no-op |
| Historical receipt/source objects | unchanged | unchanged |

This fills the previously NOT_RUN local3.11 boundary. It is not another scientific
result. PR31 math and unchanged R077 full campaigns were not rerun.

Three further publisher failure cases used only LOCAL bare remotes and the
already-generated3.11 sidecar, so no mathematics ran:

* Commit hook rejects: exit1 BLOCKED, local HEAD and remote unchanged.
* Remote advances during the commit hook, detected AFTER_COMMIT: exit1 BLOCKED,
  competing remote object preserved, only a local result commit remains.
* Remote rejects push: exit1 BLOCKED, remote unchanged, local result commit remains.

No false success, rebase, force, hidden retry or historical rewrite. Stop and
inspect a retained local commit; do not blindly reset/rebase/force-push. The
existing driver already covers a remote advance before publication. Protected
branch/token permissions and real network outages remain production conditions,
not fabricated local PASS claims.

`py311-integration/candidate.bundle` preserves local fixture
`76f3b4c1a9ab1f8cb127de448c7d8caae88541cb`, tree
`2f1fcca053dbb0b7de499bee032002206a533e43`; it requires old public base ce6.
This is NOT a GitHub commit/run. Synthetic IDs1001/1002 are local claims only.

## Run identity and official mainline acceptance conditions

The sidecar binds tested checkout, workflow blob/SHA, five fixed sources,
entry/gate identities, commands, exits and raw stream hashes. Claimed run/attempt/
job key are validated and path-bound. `GITHUB_JOB` is a key, not numeric job ID:
`numeric_job_id=null`, `externally_attested=false` remain honest boundaries.
No trusted CI timestamp/run identity is inferred from local environment values.
Raw evidence validation is not cryptographic attestation of an external service.

Before official activation, R mainline must:

1. Review/authorize integration of PR32's A helper files and the exact three-file
   patch. Re-read latest HEAD/target blobs; stale/partial target bytes must reject.
2. Approve new immutable sidecar archival location and remote-advance STOP policy.
   Frozen acceptance requires Git archival; do not silently replace it with only
   an artifact upload. Original historical receipt remains immutable.
3. Confirm zero-cost Actions availability and repository bot/branch permissions;
   this review neither confirms billing nor authorizes CI/deployment.
4. After explicit authorization, test the actual setup-python3.11 Actions runner,
   record exact binary/version, real run/attempt/job identity and exit results.
5. Independently read GitHub run and jobs metadata, logs, source commit/workflow
   bytes and published result commit. Example read-only endpoints:
   `gh api repos/edwardsage419/Psychohistory-Research/actions/runs/RUN_ID` and
   `gh api repos/edwardsage419/Psychohistory-Research/actions/runs/RUN_ID/attempts/ATTEMPT/jobs`.
   Resolve actual numeric job ID/status/conclusion; compare head_sha and workflow
   identity to tested checkout and archived sidecar. Keep tested and result
   commits distinct. A copied receipt or claimed context alone cannot satisfy it.
6. Verify only the new sidecar was committed; compare archived byte/hash and
   remote main readback. R mainline owns the final scientific acceptance decision.
   None of this re-attests old runs or closes05-003 automatically.

For rollback before deployment, `git apply --reverse --check` then reverse on the
isolated candidate restored all three buffers. After deployment, disable/revert
wiring via a NEW owner-approved commit, preserve all historical/new receipts,
and do not reset public history. Old vulnerable workflow must not be relabeled
safe merely because wiring is rolled back; scientific acceptance remains paused.

## PR30/31 pin failure and minimal candidate repair

All six pairwise file-overlap sets are empty; no textual patch conflicts.
Nevertheless PR31 pins the exact A preflight bytes for provenance. PR30 changes
that file's two strings, so combined capture fails closed on SOURCE_BLOB. This is
an actual integration dependency, not a defect in the R077 scoring mathematics.

| Capture-only test on latest main + fixed four candidates | Normal | Optimized |
|---|---|---|
| Original PR31 pin after PR30 | exit1 SOURCE_BLOB | exit1 SOURCE_BLOB |
| Candidate one-entry refresh | exit0,22 identities | exit0,22 identities |
| PR33 checklist on combined tree | exit2, production_ready=false | exit2, production_ready=false |

PR33 preserves11 original failures/35 synthetic corrections and reports no math
rerun. PR31 never imports/runs the A adapter; its pin is evidence-only. Refresh
only one entry in B's pins.json (3 values): blob2a6d2e6a…→833512df…, bytes13845→
13835, SHA256101adc…→8e0409…. Exact candidate text is
`pr31-pr30-pin-refresh.patch`, SHA256
`e635a8ce238d80091a19e4590b428126527ff29a83df53fee214621d52482f38`.
B's real directory and PR31 have NOT been modified. Its owner must review/adopt
the candidate; capture-only GREEN is not a fresh mathematical run. Preserve the
original normal/-O numerical summaries, streams and hashes unchanged and append
any new provenance qualification separately. No historical evidence rewriting.

PR30:10 artifact identities and exact two-string delta verified, prior --help /
metadata outputs reused. PR33:6 artifact identities and28 archive members
verified; success cannot turn off the production veto. PR31: independent review
verified17 pins,22 source records/mode,6 stream records/mode, B28's64 explicit
stream records and A29's11/13 archive members. Retained numerical certificates
are unchanged; no mathematical conclusion is independently re-awarded here.

Recommended integration: PR32's A helpers and PR33 are independent and can be
reviewed first. Coordinate PR30 with B-approved PR31 pin refresh; then requalify
PR31 source capture. Merging PR31 first does not eliminate the later PR30 break.
Without B refresh approval, keep that combined execution blocked. Actual R127
workflow patch is a separate R-mainline-owned step after helper adoption and
explicit deployment/CI authorization. No integration is performed by this PR.

## Reproduce with existing tools

Fetch/read the fixed heads above. Use local clones; do not activate workflow.
Let REPO be a full repository checkout and PY311 an existing local3.11 executable.

```sh
"$PY311" -B research/codex_a/r127_acceptance_20261112/verify_combination.py \
  --repo "$REPO" --python "$PY311" --output /tmp/r127-combination-fresh
```

To repeat the new-runtime check, detach a disposable clone at fixed PR32 head,
prefix PATH with PY311's bin directory, and run its EXISTING entrypoints:

```sh
"$PY311" -B -m unittest discover -s research/codex_a/r127_workflow_candidate -p test_candidate.py -v
"$PY311" -B -O -m unittest discover -s research/codex_a/r127_workflow_candidate -p test_candidate.py -v
"$PY311" -B research/codex_a/r127_workflow_candidate/exercise.py . --output /tmp/r127-311-fresh
```

`exercise.py` preserves its exact bundle and sidecar; they can feed this bounded
failure driver (from this delivery checkout):

```sh
"$PY311" -B research/codex_a/r127_acceptance_20261112/deployment_failure_checks.py \
  --repo "$REPO" --python "$PY311" \
  --bundle /tmp/r127-311-fresh/candidate.bundle \
  --receipt /tmp/r127-311-fresh/normal-sidecar.json --output /tmp/r127-publish-fresh
```

Output directories must not already exist. Both new drivers operate in temporary
clones; only the original existing exercise executes math. No new hash/math/
generic audit framework. Archive contains actual argv/cwd/raw output/hash records,
runtime identity, source manifests, GitHub snapshot, candidate patch and fresh
read-only review. Do not treat deleted temporary commits as remote deliveries.

## Remaining work

COMPLETE: candidate engineering approval, new-runtime compatibility, deployment
failure handling, combined-source RED/GREEN and exact patch/rollback preparation.
PARTIAL: source-compatible future integration; pin candidate and workflow wiring
are unadopted. BLOCKED: actual deployment/CI pending mainline/owner decisions.
NOT_RUN: real CI, historical provenance authentication, human rescoring,
scientific reacceptance, new E2/E3, paid resources.

Highest-value next work is owner-reviewed R127 integration plus actual external
run identity/readback after authorization, and B-reviewed pin adoption before the
combined PR30/31 run. No other confirmed current-main engineering defect justifies
building a new framework. Maintain R073/R077/PESEN and all frozen boundaries.
