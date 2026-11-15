# Independent final review — Psychohistory Platform v0.1

Reviewed base `0aa29bb2dc73c6667ea0a1ae40f1092276d025c6` → code head `b09e88d4` on 2026-11-15. Read OWNER_SPEC.md, IMPLEMENTATION_PLAN.md (including Review Focus), PROGRESS.md, supplied diff, every `src/psychohistory` module, tests, and the console source. This is a read-only source review; the only writes were isolated probes and this report under `/tmp`.

## Verdict

**Changes requested: five Important findings, no Critical findings, one Minor finding.** The implementation provides a real bounded synthetic workflow rather than an empty scaffold, but the important integrity and lifecycle gaps below prevent an unqualified claim that the storage, scheduling, contract validation, and version-lock requirements are complete. Fix and run the targeted regressions before final delivery. This is an engineering assessment, not an assessment of empirical model validity.

The existing 17 pytest tests, strict TypeScript/Vite build, and real Chromium workflow are reported passing by the implementer; I did not redundantly rerun those unchanged checks. I independently ran `/tmp/psychohistory-review-probe.py` against the reviewed source. All findings I1–I5 were reproduced in isolated temporary storage; output is summarized below.

## Strengths

- Core mechanism code uses the standard library and does not depend on API/database services. CLI and API share service admission and bounded synthetic parameters.
- Real two-model coupling, delayed feedback, paired branches, explicit version labels, probability output, and UNKNOWN are implemented. Results consistently distinguish synthetic scenario differences from identified causal effects.
- Discovered research is read only and never imported as executable code; original evidence records and R-series namespace are retained.
- Content-addressed objects are verified on read, snapshots isolate caller mutations, terminal task records reject subsequent updates, and restore requires a fresh destination.
- A single scheduler lock and serialized monitor cover ordinary completion/cancel races; workers have Linux CPU/address-space limits and a stated non-hostile-code boundary.
- API bearer protection, same-host Origin check, bounded requests, loopback CLI binding, symlink/path checks, token exclusion from backups, and in-memory browser credentials are concrete protections.
- The console is operational and explicitly communicates scientific limitations. Frozen research files remain outside the supplied change scope.

## Critical

None found within the authorized local, trusted-plugin, synthetic-only scope.

## Important

### I1 — The 200-row display limit also hides live tasks from scheduler safety decisions

**Locations:** `src/psychohistory/storage.py:115`; callers `runtime.py:40`, `runtime.py:48`, `runtime.py:100`, `storage.py:142`.

`Store.runs()` returns only the latest 200 rows, but it is used as the authoritative set for restart recovery, queue budgets, dispatch, and backup quiescence. An old PENDING task becomes invisible after 200 subsequent completed/canceled tasks. It can still be approved by ID, but will never dispatch. Old RUNNING rows can likewise escape restart recovery, and an old APPROVED row does not prevent backup.

**Reproduction:** Created one pending task and 200 newer canceled tasks. A fresh scheduler then admitted 16 more pending tasks, producing **17 nonterminal tasks despite the 16-task budget**. Approval of the old task left it APPROVED indefinitely. Backup then succeeded while that old task was APPROVED.

**Fix:** Separate paginated display history from uncapped authoritative queries. Query all nonterminal rows/counts directly for queue, dispatch, recovery, and backup; provide actual pagination for historical UI access.

**Regression:** Keep an early pending task, create over 200 later terminal tasks, then verify its visibility/dispatch, exact queue count, restart handling of an early RUNNING row, and refusal of backup with any APPROVED/RUNNING row.

### I2 — Backup can declare success while a referenced result artifact is missing

**Locations:** `src/psychohistory/storage.py:147`, `storage.py:159`; restore catches the inconsistency only at `storage.py:185`.

Backup verifies objects that happen to exist, but never checks that every result hash referenced by its SQLite snapshot exists in the copied object set. Deleting or losing one artifact therefore produces a COMPLETED backup and manifest which cannot restore. This is precisely the situation a disaster-recovery backup must detect before it claims success.

**Reproduction:** Created a COMPLETED run with a real stored result, removed that result object, and called backup. Backup returned successfully and recorded COMPLETED. Restoring the resulting backup rejected it with `Missing run artifact`.

**Fix:** Validate all result references and required schema/SQLite consistency against the snapshot before writing a success manifest/audit entry. Prefer publishing the backup directory atomically only after the complete verification passes; preserve the failure audit on rejection.

**Regression:** A missing referenced artifact must fail backup and leave no completed manifest; an unreferenced object must not substitute for it. Preserve existing tamper and successful fresh-directory restore tests.

### I3 — A queued run's recorded code identity is not enforced when it executes

**Locations:** `src/psychohistory/runtime.py:50`, `runtime.py:55`, `runtime.py:103`, `runtime.py:92`.

Submission records `code_sha256` and environment identity, but approval/dispatch always execute the currently installed engine and never compare its identity to the saved run. Thus a PENDING/APPROVED task preserved through a software change or restore can execute different code while its durable run metadata continues to claim the old code. Component version labels alone cannot prevent this, particularly when an implementation changes without a label bump.

**Reproduction:** Submitted a task, simulated a prior installation's persisted hash by setting its saved code hash to a different valid hash, then approved it. The task became COMPLETED; its durable `code_sha256` differed from `result.environment.core_code_sha256`.

**Fix:** At dispatch and worker/result acceptance, verify the approved code, component, protocol/data, and required environment identities. If the original implementation cannot be selected, transition to BLOCKED/FAILED with an explicit compatibility reason and require a new submission/approval under the new identity. Do not rewrite historical pins to fit the installed code.

**Regression:** Submit under identity A, restart with identity B, and assert the old task cannot produce a COMPLETED result under A. Same-identity recovery must continue to execute normally. Also reject a worker result whose identity differs from the approved run.

### I4 — Record validation accepts invalid identity/dependency shapes and inconsistent uncertainty metadata

**Locations:** `src/psychohistory/contracts.py:45`, `contracts.py:48`, `contracts.py:60`; `src/psychohistory/adapters.py:11`, `adapters.py:14`.

`subject_ref` need not be a list: a string is iterated as characters and passes the identity and state-length checks. Dependencies need only be truthy. Uncertainty metadata is re-created for validation but is neither required to be complete nor checked against the record's units, target, or dependencies. The adapter then silently replaces the incoming uncertainty with generic UNKNOWN. Invalid records are therefore accepted instead of rejected, contrary to the explicit contract requirements.

**Reproduction:** Each of the following adapted successfully to prevalence 0.5 for `[0,1]`: `subject_ref='ab'`; `dependencies='unknown'`; and a DISCRETE uncertainty carrying `units='kg'` plus dependencies for a different population while the record describes binary states and joint-population-state. The returned record retained the string identity/dependency in the first two cases.

**Fix:** Validate collection and scalar types explicitly (including nonempty record IDs/types, subject lists, dependency lists, and structured time/uncertainty metadata). Define the adapter's accepted uncertainty and unit/dependency mapping; reject unsupported or mismatched inputs instead of silently overwriting them. Distinguish any intentional lossy uncertainty mapping explicitly in provenance.

**Regression:** Reject string/dict subjects and dependencies; uncertainty unit/dependency mismatches; missing or malformed required metadata; invalid fractional/negative round semantics where rounds are discrete. Keep the built-in synthetic exchange valid with complete, consistent metadata.

### I5 — Stored branch histories contain unresolved parent snapshot hashes

**Locations:** `src/psychohistory/engine.py:38`, `engine.py:51`, `engine.py:55`.

Each branch begins by creating `root.fork(name)`, then its first tick uses that fork's hash as `parent_hash`. The fork snapshot is never included in the result artifact. Only the root and tick snapshots are saved. Therefore the saved chain cannot be traversed from the first tick back to the persisted root without reconstructing an omitted historical snapshot using today's implementation.

**Reproduction:** Ran a one-round experiment and indexed every snapshot in its saved result. Both branches' first snapshot parent hashes were absent. The branch-level `parent_hash` points to the root, while the snapshot-level parent points to the unsaved fork.

**Fix:** Persist each initial fork snapshot in its branch record (or deliberately make the first persisted branch snapshot directly reference the persisted root with explicit branch-creation semantics). Every non-null parent reference should resolve within the immutable artifact/snapshot store.

**Regression:** Traverse every snapshot parent from both final snapshots through the initial branches to root, resolving and hash-checking each node after a backup/restore. No parent hash may require recomputation of a missing snapshot.

## Minor

### M1 — Snapshot and plugin-state restoration validates envelope identity but not state schema

**Locations:** `src/psychohistory/state.py:23`; `src/psychohistory/plugins.py:14`.

Plugin restoration checks model ID/version, but accepts any JSON `state`, including values incompatible with its declared binary-state mechanism. Generic Snapshot restoration checks only snapshot format version, so required branch/model/state metadata can be absent if the envelope is constructed with a matching hash. Hash integrity is useful but is not semantic state validity.

**Suggested fix:** Have each plugin validate its own restored state schema and define minimum snapshot-envelope requirements. Avoid advertising successful restoration for an unusable state.

**Regression:** Correctly hashed envelopes containing a wrong state type, unsupported model state version, or missing required metadata must reject clearly; valid states must round-trip. This is currently lower impact because the public execution path does not accept arbitrary snapshot uploads or resume through this API.

## Spec compliance and quality assessment

Most of the bounded Gate 03–06 and Gate 08–09 workflows are visibly implemented: two real plugins, a working adapter, synthetic event synchronization, immutable serialized values, explicit scientific labels, independent scenarios, source discovery, and an operational Chinese console. Baseline path/authentication checks and resource limits also materially support Gates 07 and 10.

However, Gate 04 contract enforcement is incomplete (I4); Gate 05's fully traceable stored history is incomplete (I5); Gate 07 authoritative task accounting/recovery is incomplete (I1); and Gate 10/11 version pinning and recoverable backup claims need I2/I3 fixed. Passing ordinary happy-path tests does not establish these edge-case guarantees. The implementation is promising and appropriately bounded, but **not ready for an unconditional completion claim at the reviewed head**.

## Explicitly declined to judge

- Empirical predictive validity, causal identification, competing-theory superiority, scientific completion, or original model fusion. These are expressly outside scope.
- Native macOS execution. Linux evidence cannot substitute; macOS must stay NOT_RUN unless actually tested.
- The root agent's concurrently written operator documentation, disaster-recovery scripts, remote-push receipts, and final acceptance matrix. I did not classify those in-progress deliverables as missing.
- GitHub PR creation/API reachability, deployment, public exposure, paid services, or merge authority.
- Hostile third-party code sandboxing, multi-user isolation, and protection against an attacker who already controls the process user or can rewrite the entire backup and its manifest. No such security boundary is claimed by this release.
- Exhaustive destructive crash/fault injection or every possible filesystem race; the review used targeted bounded probes and source inspection.

## Probe receipt

Command: `python /tmp/psychohistory-review-probe.py`

Observed output:

```text
queue_nonterminal_after_16_new_submissions 17
old_approved_status APPROVED
backup_with_old_approved_task ACCEPTED
backup_with_missing_referenced_artifact COMPLETED
same_backup_restore Missing run artifact
obsolete_code_pin_status COMPLETED
recorded_vs_executed_code_match False
string_identity ACCEPTED {'prevalence': 0.5}
string_dependence ACCEPTED {'prevalence': 0.5}
uncertainty_unit_mismatch ACCEPTED {'prevalence': 0.5}
first_history_parent_resolvable [False, False]
```

All probe data were confined to `/tmp/psychohistory-review-0bhzn5wz`; source, index, and HEAD were not modified.
