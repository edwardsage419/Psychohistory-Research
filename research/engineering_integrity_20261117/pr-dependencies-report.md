# PR30/31/32/33/35/39 dependency audit — 2026-11-17

Audited against fixed fresh main `1e839d3b02cae02833b282c309f5abd58559949e`. Source repository, its index, HEAD and refs were not changed. All applied buffers and executions were confined to `/tmp/r-series-review-20261117/dependencies-checkout`; no commits, network, workflow dispatch, scoring or production calls were performed. PR metadata supplied by the parent was compared with locally fetched immutable Git objects.

## Decision

These six fixed packages are acceptable for engineering/evidence incorporation, with **PR30 before PR31**. There is no textual conflict among these packages or against fresh main. Incorporating the packages does not apply the embedded R127 workflow patch, install a production scorer, establish external CI provenance, or authorize scientific adoption. R077 production and human scoring, R127 workflow deployment/formal acceptance, and R333–R340 mandatory production integration remain **BLOCKED / NOT_RUN**.

| PR | Fixed head | Dependency / disposition |
|---|---|---|
|30|`8005fcb75e9e20545adb245edd45d72dbc374632`|Two preflight string changes plus metadata/manifest. Reverse both literals and the file is exactly fresh-main bytes, including AST. Production veto/scoring unchanged.|
|31|`b928dc8d97202005560e2e73129c13adfd374097`|**Requires corresponding PR30 adapter**. 16/17 external source pins match fresh main; only the preflight pin intentionally differs. All 17 match main+PR30. Current main alone must reject this package's source capture.|
|32|`16778c53b2e7a2c590ff65c854b1f7034169050d`|Adds candidate helpers/template and a patch under Codex A; no active workflow target changed. All three patch preimages and all 20 archived source-map entries match fresh main.|
|33|`9d5041acdfc3f13a002e2cfbb6c33d4dfaed6af4`|Optional retained-evidence checklist. Accepts precisely the old and PR30-reviewed adapter SHA256s; no override to enable production. Can operate before/after30, while intended combined verification follows30+31.|
|35|`9ae4eb923b7d1cbc78fdc0c81cddee591efc68ef`|Historical R127 acceptance/integration evidence and drivers. Its old PR31 NEEDS_PIN_REFRESH statement and old proposed patch are superseded by actual current31 adoption; preserve them as dated evidence. **Do not reapply its PR31 patch.** Its live reproduction drivers depend on32/fixed historical Git objects, not a change to active workflow.|
|39|`0596163690038c610c3c45c33fde64a6b39da0dd`|Optional authenticated local R333–R340 replay; all56 pinned inputs match fresh main, independent of30–38 changed paths. Integration report accurately supersedes35 with actual B-adopted pin evidence, but its combination was run on historical main d4740c2c, not fresh main.|

A practical serial incorporation order is **30,31,32,33,35,36,37,38,39** (36–38 are outside this audit's implementation review). Only30→31 is a necessary new runtime pin edge among these six.32 and33 should precede35 for coherent supporting-helper adoption;39's integration report references36 but its authenticated replay does not import36. Independent packages36/37/38 share no changed path with these six or each other. Their domain-specific review belongs to the other audit.

## Exact source identities and retained-evidence verification

PR31 requires preflight blob `833512df7f3fde37f84a76df30bc176ffc58c6b7`, 13835 bytes, SHA256 `8e04095a1b984d47245563a363309f5a7e332326584e53f0a17545235cf8ef23`.
Fresh main retains old blob `2a6d2e6a45e5bce1d2f676613a57ab7668f4ed39`, 13845 bytes, SHA256 `101adc1271e7ccbcf10f02e62afc0916bccd96d80278e9258cc9bfae6f45baaf`.
Current31 pins-manifest blob is `43e06956dc98d387c7eaf738f738cd170359d97f`, SHA256 `1bf54f4da4cbd02b137050dc5237262289ac350ec60fa91f2171f17cf2c85ac6`.

Fresh comparisons against original PR31 `03cf49d8` prove all33 other preexisting files unchanged, with only pins.json's three preflight identity values changed; new maintenance/evidence files are additive. The original math evidence therefore remains historical and byte-identical. The four retained PR31 command manifests authenticate 6+6+18+18 streams; all match. This verifies recorded bytes, not a new execution of the7-method mathematical campaign.

All artifact entries authenticated at fixed heads:30=10,32=15,33=6,35=8,39=7. All archive-member manifests match every retained member:32=109,33=28,35=100,39=86. PR35's 13-source archived map also matches fresh main completely. Archive hash integrity does not itself independently reproduce each historical test outcome.

Read actual independent reviews: original and pin-refresh B31 notes;32/33 retained delivery review;35 retained R127 and PR31 interface review;39 review-summary, actual-combination-independent-review, and actual-combination/result. They consistently distinguish local internal review from external replication. PR39 records correction of the refs/replace/GIT_DIR helper-loading defect before publication; source now disables replacement objects, sanitizes Git selectors and authenticates helper SHA before exec.

PR39's historical six-head combination is30/31/32/33/35/36, deliberately excluding37/38. Its6 recorded commands/12 raw streams authenticate exactly: B31 normal/-O capture0/22; A33 normal/-O2 with production false/11 failures/35 corrections; PR32 prepare0/exact patch; R127 source capture0/5. Local fixture commits were not GitHub deliveries. Nothing in that evidence is presented as a fresh test of main1e839d3b.

## Checks newly executed during this audit

1. Git `apply --check` succeeded individually against fresh main for all six packages. Exact package patches then applied sequentially to the isolated working buffers in30,31,32,33,35,39 order, with successful checks before each. No commits were created. All36 pairwise changed-path intersections across nine heads30–33,35–39 are empty. Harmless preserved trailing whitespace exists in some PR31 logs/PR32 historical content.
2. PR32 `prepare.py .` freshly exited0 in that isolated checkout, emitted9448 bytes exactly equal to fixed candidate.patch, SHA256 `ed2b03c7985d93db9c915abaa4e3bffeae665803dbd00db8364eba14a62cf44e`. It only generated bytes; no R127 target patch was applied.
3. PR39 `capture()` freshly exited0 in ordinary and optimized isolated Python, authenticating all56 sources against HEAD1e839d3b and live buffers. The entrypoint was the exact externally overlaid PR39 source. This is **source-only evidence**, not adoption of the overlaid packages at HEAD and not replay of the composite/math child.
4. Static inspection of push/pull_request/pull_request_target path filters from all workflow YAML at fixed main found no match for these six packages' changed paths. Thus package incorporation itself adds no active workflow and does not select an existing path-filtered workflow. This is repository-static evidence, not a claim of observed GitHub Actions results or billing eligibility.

Because no commits were permitted in this task, the combined working buffers were intentionally not passed off as an adopted HEAD. No new combined B31/A33 adoption run is claimed; parent should run those checks after constructing its actual combined integration commit.

## R127 activation boundary

The actual old workflow remains blob `4b22f653dc7516bb31ead23e45dcf7f62261d79d`, SHA256 `77fefd0b06a896232b4cc4a7679b1633051f19eba9d082e062faa8e9d2ace586`.32's stored candidate changes exactly workflow, r127_local_gates/pins.json and gate.py's manifest SHA constant. Gate logic, original model/test/report/protocol/receipt pins stay unchanged. All3 preimages still match fresh main. The proposed workflow depends on32's tracked run_workflow.py/publish.py and26's adopted gate. It would use ubuntu-latest/setup-python3.11 and a contents:write bot, then publish only an immutable sidecar on main.

Reuse35's retained CPython3.11.17 local60-test/138-field evidence, nine reject controls per mode, local sidecar/no-op/conflict handling, commit-hook failure/remote-advance/push-rejection cases and rollback. Those were not rerun. They establish neither actual setup-python/GitHub binary equivalence nor externally attested numeric job ID, official run metadata, billing eligibility or branch/token permission.32/35/39 explicitly retain owner approval of exact workflow wiring/sidecar/archive/STOP-on-remote-advance policy and authorized no-cost actual CI as separate gates. A helper merge alone satisfies none of these deployment decisions. Scientific05-003 remains provisional.

The unchanged old workflow's inline assert/parser/receipt issues remain relevant to production; merely archiving32/35 does not repair them. Historical failed receipts must remain preserved. Subsequent deployment would be a separately authorized operation; do not apply candidate.patch in the production checkout as part of this archive/evidence incorporation.

## Small final combination check recommended to parent

On the actual committed combined checkout (including independent R132 repair), use existing interfaces only:

- B31: import its `run_audit.py` with `importlib.util` and call only `capture()`; ordinary/-O must exit0 with22 fingerprints and the exact PR30 preflight pin. Do not invoke `run()`/main to repeat the math campaign.
- A33: `python3 -B research/codex_a/r077_integration/mainline_checklist.py .` and optimized equivalent; require exit2, `production_ready=false`, original_failure_cases11, candidate_correct_orders35, mathematical_programs_rerunfalse. This revalidates retained synthetic output and source adoption; no new human scoring.
- PR32: `python3 -B research/codex_a/r127_workflow_candidate/prepare.py .`; compare bytes/SHA to the fixed9448-byte patch. If a5-source candidate-gate adoption check is wanted, apply only in a disposable clone of the combined commit, commit there if separately permitted, call existing gate.capture, then reverse/check all3 buffers. Do not activate a workflow or run publisher/exercise.
- PR39: source-only capture is sufficient for detecting unrelated-source drift; all56 pinned inputs are unchanged. Its retained normal/-O eight-test/receipt replay evidence can be reused. A fresh replay is optional bounded artificial verification, not required to establish this dependency edge.

Do **not** use35's `verify_combination.py` as the final fresh-main verifier: it hardcodes historical main and old31, constructs a deliberate RED then applies the old candidate pin patch. Likewise39's archived orchestration is fixed historical six-head evidence. Re-running either unchanged would answer a historical question, not test the parent's latest combined commit.

Scientific limits remain explicit: no current raw human recovery/license/risk-set qualification was attempted here; historical R077 vote impact remains UNKNOWN. No E2/E3, frozen protocol, model, historical result or production authorization changed. Successful synthetic engineering incorporation does not close scientific queue items.

Machine-readable details: `pr-dependencies-summary.json`, `dependency-merge-checks.json`, `dependency-workflow-path-matches.json`; raw fresh prepare/capture streams are retained beside this report. Audit source scripts are `audit_dependencies.py` and `check_dependency_merge.py`.
