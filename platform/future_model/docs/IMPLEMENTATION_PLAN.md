# Psychohistory Platform v0.1 Implementation Plan

> Execution: superpowers:executing-plans, inline implementation; fresh final review. Owner explicitly authorized autonomous whole-stage execution and checkpoint pushes. Plans/specs remain under platform/future_model/.

**Goal:** Implement the complete bounded synthetic research workflow and Gates 01–11, without upgrading scientific evidence or touching frozen research.
**Architecture:** Modular monolith; stdlib-only core, immutable JSON snapshots, explicit versioned records/adapters, SQLite metadata and content-addressed artifacts, isolated trusted worker processes, shared service behind API/CLI and Chinese React console.
**Stack:** Python 3.12, FastAPI/Pydantic, SQLite, pytest; Node 24, React/TypeScript/Vite.
**Spec:** OWNER_SPEC.md plus owner task's Gate 11 persistence contract.

## Global Constraints
- Only platform/future_model/ changes. R073, PESEN v0.1 and all existing scientific protocols remain unchanged.
- No paid service, CI, GPU, public server, merge, restricted data upload or original-model fusion. Every commit uses [skip ci].
- Synthetic results are SYNTHETIC_ONLY; discovery never executes repository code and does not grant scientific permission.
- Linux tested; native macOS NOT_RUN. Full acceptance cannot be called COMPLETE with Gate 01 macOS unrun.
- Git branch from main 0aa29bb2dc73c6667ea0a1ae40f1092276d025c6. Existing snapshot HEAD 42f9c29fbdac502b33b42cf1632765f3db387869 was clean.

## Review Focus
- Future information, inconsistent subject/time/unit/dependency metadata must be rejected, not guessed.
- Mutable caller state, cross-branch contamination and hash tampering must not change frozen history.
- Simultaneous timeout/cancel/completion and process crashes must yield durable truthful terminal states.
- Traversal, symlinks, malicious backup manifests, oversized inputs and unauthenticated writes must fail closed.
- Fresh-directory restore must use remotely saved code/locks, verify every artifact, recover consistent SQLite, preserve failure evidence.

## Task 1: Contracts and independent mechanism engine
Files: src/psychohistory/{contracts,plugins,adapters,state,engine,relations}.py; tests/test_core.py.
Interfaces: run_experiment(seed:int, rounds:int, population:int, intervention:float)->dict; Registry.get(model_id,version); record/uncertainty validation; Snapshot.create/restore/fork.
- [x] Write tests for deterministic two-model delayed synchronization, independent branches, probabilities, UNKNOWN, future-time/unit/identity rejection, capabilities/version compatibility, cycles, tampering.
- [x] Run RED test suite before implementation.
- [x] Implement bounded individual-state and group-spread plugins, explicit adapter, event ordering, immutable snapshots and relationship validation; no API/storage imports in core.
- [x] Run tests GREEN; commit and push checkpoint with SHA readback.

## Task 2: Provenance, storage, admission and recovery
Files: evidence.py, storage.py; tests/test_storage.py.
Interfaces: Store(root:Path), create/update/get/list run/asset records; put/get artifacts; backup(destination), restore_backup(source,new_root); scan_asset(repo,path); immutable evidence admission.
- [x] RED tests: read-only real asset discovery/dedup, namespace preservation, invalid provenance/missing file, restricted-data rejection; SQL consistency, immutable CAS, safe paths/symlinks, backup/restore/tampering, schema migration and preserved failure journal.
- [x] Implement SQLite v2 migrations, manifest-verified consistent backup and restore, metadata-only scanner and explicit synthetic approval.
- [x] Run full platform suite GREEN; checkpoint commit/push/readback.

## Task 3: Isolated scheduler, shared service, API and CLI
Files: runtime.py, service.py, api.py, cli.py; tests/test_runtime_api.py.
Interfaces: Scheduler.submit/approve/get/cancel/wait/close; Service.submit synthetic run; create_app(root,repo,token); python -m psychohistory.cli.
- [x] RED tests: PENDING→APPROVED→RUNNING→COMPLETED, failure, cancel, timeout, resource/size/concurrency budgets, process isolation, truthful persisted logs; token auth, CSRF/cross-origin rejection, no real-data execution, CLI parity.
- [x] Implement spawn processes with POSIX resource limits, bounded queue/runtime, default loopback server, protected writes/read scope; secrets never persisted.
- [x] Full suite GREEN; real CLI/API/backup operations; checkpoint commit/push/readback.

## Task 4: Interactive console and real browser flow
Files: web/{src,package.json,package-lock.json,index.html,vite.config.ts}, tests browser script; README and scripts.
- [x] Build Chinese research dashboard, model browser, parameterized experiment form, submit/approve/cancel workflow, evidence/provenance center, logs/results/branch history. API-only mathematics.
- [x] Verify strict TypeScript and production Vite build; real browser exercise actual API submission/approval/results and error display. Use an installed free browser if available; report actual blockers.
- [x] Lock all dependencies; Linux startup/shutdown on loopback; checkpoint commit/push/readback.

## Task 5: Integration, disaster recovery, security review and PR
Files: scripts/{install,verify,disaster_recovery}.*, docs/{CONTRACTS,SECURITY,RECOVERY,VERSIONING}.md, reports/*, examples/*.
- [x] Run complete platform suite; run pure core with python -S; record current environmental facts and all failures.
- [x] Fresh clone from actual pushed branch, create a new venv and npm ci from locks, rerun synthetic experiment and compare deterministic scientific payload. Actual SQLite/artifact backup and restore checks.
- [x] Fresh whole-branch review and correct important defects with regression tests.
- [x] Gates 01–11 report with precise COMPLETE/PARTIAL/BLOCKED/NOT_RUN statuses, truthful PR/push/network evidence and native macOS NOT_RUN.
- [ ] PR BLOCKED by current-instance api.github.com policy; code checkpoints verified. Publish code checkpoints only to independent engineering branch; verify SHA after each push; create PR if GitHub API available. Do not merge or deploy. Preserve unresolved failure records and actionable resume commands.

## Interface conflict scan / rulings
Task 1→2: canonical JSON + sha256 snapshot payloads stored without mutation.
Task 2→3: scheduler owns live process objects; Store owns durable status/log/artifact records. One serialized scheduler monitor updates terminal states.
Task 3→4: /api/v1 JSON endpoints, bearer token entered only in browser memory, UI never directly accesses storage.
Task 2/3→5: backup stops/blocks active jobs; restore to empty root only, external audit journal retained and not overwritten by rollback.
Ruling: use the existing task-isolated checkout and independent branch, no extra Git worktree — environment Start skill requires this unless explicitly requested.
Ruling: choose inline execution to keep shared contracts coherent; a separate final reviewer checks the branch. Owner delegated implementation order and decisions.
