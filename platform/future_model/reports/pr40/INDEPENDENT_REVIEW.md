# Independent runtime/API/CLI/console review of PR #40

Reviewed head `23843c2afcfb5e3f28b3ce047804cd7f9144e4b9`, read `docs/OWNER_SPEC.md`, prior independent findings and fixes, runtime/service/API/CLI/console source, runtime/API tests and review regressions. Read-only review; all probes and this report are under `/tmp`. No source/index changes, GitHub writes or extra agents. Root owns storage/contracts/state review and baseline tests.

**Verdict:** Two Important and two Minor findings, no Critical finding in the local trusted-plugin, synthetic-only scope. Existing fixes for uncapped scheduler task queries and code/version identity checks are present; findings below describe remaining behavior rather than repeating the resolved findings.

## Important I1: Read-only CLI commands start and cancel approved tasks

**Locations:** `src/psychohistory/cli.py:44–63`, particularly unconditional `Service(...)` at line 46; `service.py:20`; `runtime.py:51`, `runtime.py:110–122`, `runtime.py:145–150`.

`runs`, `status`, `result` and discovery instantiate the complete Service and start its dispatch thread. Approved tasks can legitimately remain persisted after Web shutdown (shutdown cancels active workers but preserves the approved queue). A subsequent CLI read therefore dispatches an approved task. The CLI immediately closes the Service after obtaining its output, and Scheduler.close cancels the just-started task. This causes an ostensibly read-only observation to irreversibly change approved work into CANCELED; the output can even show the old APPROVED state and return success.

**Reproduction:** `PYTHONPATH=src python /tmp/pr40-cli-query-probe.py` against an isolated root `/tmp/pr40-cli-query-3cvpn3fx`. Persisted an approved valid 100-round/100-person task with the owner closed before dispatch. Ran `python -m psychohistory.cli --data <root> runs`. Output:

```text
BEFORE APPROVED
COMMAND_EXIT 0
CLI_PRINTED_STATUS APPROVED
DURABLE_AFTER ... status=CANCELED; started_at populated; worker_pid populated
logs include 'Spawned isolated trusted worker', 'Canceled; worker terminated if active'
```

**Recommended correction:** Separate scheduler ownership/lifecycle from CLI metadata reads and discovery. Read-only commands should open storage without dispatching work, including while a Web scheduler owns the root. Ensure short-lived submit/cancel/backup commands also cannot accidentally dispatch and cancel unrelated approved work. Preserve the single worker-owner lock for actual dispatch; do not remove it to make the CLI work.

**Regression:** Leave at least one APPROVED task after an owner closes. Invoke real CLI `runs`, `status`, and `result` and verify task status, logs, started_at and worker identity remain unchanged and no worker starts. Verify reads work while Web owns the root. Exercise an explicit target approval with unrelated approved work and ensure exiting that command cannot cancel unrelated work.

## Important I2: Console cannot find or act on older live tasks, although backend pagination was fixed

**Locations:** `web/src/App.tsx:20`, `:23`, `:27`, `:41`, `:44`; backend default `api.py:65–66` / `storage.py:114–116`.

The console always fetches bare `/api/v1/runs`, so its only source is the latest 200 runs. There are no paging controls, separate live-task query or ID lookup. Thus an older PENDING task becomes invisible after 200 later terminal tasks, even though it still occupies the authoritative 16-task queue budget. The owner cannot approve or cancel it in the console; old completed experiments likewise disappear from the only history selector. The counters present the page length as the experiment total. This is the remaining UI consequence of the old limit finding, distinct from the now-fixed backend safety accounting.

**Reproduction:** `/tmp/pr40-runtime-probes.py` creates one early PENDING run and 200 later canceled runs. Default endpoint returns 200 canceled tasks, zero pending; `?offset=200` returns the old pending task. `/tmp/pr40-browser-history.py` launches the real current console and logs in with the isolated token; Chromium reports:

```json
{"approval_buttons":0,"rows":200,"run_fetches":["http://127.0.0.1:8874/api/v1/runs"],"old_id_visible":0,"pagination_controls":0}
```

Isolated root: `/tmp/pr40-runtime-83gwhit2/history`; old ID `8fecd09e67904ce3b025c1769e0fca60`. The temporary server was stopped.

**Recommended correction:** Offer real history pagination and preserve access to all live work (e.g. a dedicated live query plus paginated history), or provide a supported run-ID search. Fetch a selected run by ID when outside the visible page. Label page counts accurately or return actual totals.

**Regression:** Populate more than 200 later terminal runs after one old pending and one completed run. Through the real console, find/approve/cancel the pending task and select/retrieve the old completed result. Verify paging does not discard the current selection or mislabel the visible page as the full experiment count.

## Minor M1: Failed or blocked CLI approval exits successfully

**Location:** `src/psychohistory/cli.py:59–64`.

`demo` checks its terminal state before declaring success; `approve` waits and unconditionally exits zero even when the task is BLOCKED or FAILED. A restored or pending task blocked by the new identity guard therefore looks successful to shell automation.

**Reproduction:** `/tmp/pr40-runtime-probes.py`: submit a task, set the persisted code hash to a different well-formed hash (simulates a prior installed version), close its owner, run CLI approve. Observed `CLI_APPROVE_BLOCKED 0 BLOCKED`.

**Recommended correction/test:** After waiting, return a nonzero exit for every non-COMPLETED terminal outcome while retaining the structured durable reason; assert real process exit codes for BLOCKED and FAILED, and zero for COMPLETED. This does not require changing the API's successful acknowledgement of an approval request.

## Minor M2: Scheduler crash leaves its real worker alive and unowned

**Locations:** `src/psychohistory/runtime.py:15–28`, `:49–50`, `:119–122`.

The spawned worker has no parent-death guard. After SIGKILL of its scheduler process, restart acquires the released owner lock and labels the old run FAILED while the old worker remains running with PPID 1. It can continue consuming resources while the replacement scheduler starts another worker, and it writes unclaimed staging output after the failure record. In this release the trusted built-in work and CPU/memory budgets bound the likely damage, so classified Minor rather than a hostile-code or scientific-integrity issue; the advertised single-worker/wall-time behavior nevertheless stops at parent death.

**Reproduction:** `/tmp/pr40-runtime-probes.py` starts an ordinary valid 100-round/100-person task in a subprocess and SIGKILLs only its scheduler immediately on RUNNING. A new Scheduler on the same root observes:

```text
CRASH_RESTART {status:FAILED,worker_pid:1287,worker_proc_exists:true,worker_ppid:"1",worker_state:"R"}
ORPHAN_AFTER_1S {worker_proc_exists:true,worker_state:"Z",staging_exists:true}
```

No SIGSTOP or replacement worker implementation was used. The actual orphan finished and became a zombie before cleanup, proving it executed beyond its owner death and published an unclaimed staging file. The probe's scheduler subprocess was reaped and any remaining live worker killed; PPID-1 zombie reaping is controlled by the container init.

**Recommended correction/test:** On Linux, set a parent-death signal and check the expected parent after installing it to close the installation race; document/enforce the corresponding supported-platform boundary. Do not kill an arbitrary persisted PID without validating process identity. A subprocess regression should kill the scheduler owner during actual worker startup/execution and verify the worker exits, cannot publish a post-restart result, and replacement ownership never overlaps a surviving old worker.

## Additional confirmed limitation and checks

While a Web/other scheduler owns the root, even CLI `status` currently exits 1 with `Another scheduler already owns this data root`. This follows the same unconditional Service creation as I1 and should be addressed by that fix rather than relaxing worker ownership. I found no confirmed authentication or API input-admission bypass within the declared local synthetic-only scope. The existing bound/strict input checks, backend permission guard and worker identity validation are concrete protections.

No full suite rerun; root is running the baseline. Actual probes used installed Python 3.12.14, FastAPI 0.141.1 / Pydantic 2.13.4 and Chromium. Full probe scripts remain at `/tmp/pr40-runtime-probes.py`, `/tmp/pr40-cli-query-probe.py`, `/tmp/pr40-browser-history.py`.
