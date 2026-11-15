# Scoped verification of PR #40 runtime/console fixes

Read-only review of `/tmp/pr40-runtime-fix.diff`, `/tmp/pr40-console-fix.diff`, current runtime/service/API/CLI/console source, and the new targeted regression cases. No source/index edits and no full-suite rerun. Isolated original review probes were rerun under fresh `/tmp` roots.

**Verdict: fixes address both Important and both Minor findings from `/tmp/pr40-runtime-review.md`. No new Important/Critical issue found in the scoped changes.**

- **I1, CLI read/dispatch/cancel:** read commands and discovery now open Store directly. Maintenance commands create `Service(dispatch=False)`; demo/approval explicitly opt only their target into dispatch. The worker-owner lock remains in place. Independently reran `/tmp/pr40-cli-query-probe.py`: `runs` exits 0 and preserves APPROVED, original logs, `started_at=None`, `ended_at=None`, and no worker PID. New isolated root `/tmp/pr40-cli-query-yvj58hdw`. Original live-owner status probe now exits 0 as well. The root's regression additionally covers submit and explicit approval with an unrelated approved queue.
- **I2, hidden old console work/history:** API live route precedes `/runs/{run_id}` and retains existing bearer protection. Console fetches live tasks separately, pages historical rows in groups of 50, deduplicates them, labels its count as the page plus live tasks, and fetches the selected run by ID. A completed selection remains available when changing pages. Request sequencing prevents an older refresh response from replacing the latest refresh. Source review supports the correction; root is separately exercising real Chromium paging/live-task flows.
- **M1, CLI approval exit:** approval now returns nonzero for any terminal outcome other than COMPLETED while printing the durable run record. Independently reran the original stale-code-pin probe: exit **1**, durable status **BLOCKED**. Successful CLI reads continue to exit 0.
- **M2, owner death:** Linux workers install `PR_SET_PDEATHSIG` before computation/resource setup and check their parent PID after installation, covering death before signal installation. The enforcement field is explicit; other platforms retain NOT_ENFORCED. Independently reran original kill-and-restart probe: the new scheduler records FAILED; the startup process exits by the one-second check and **no staging output is published**. A process can still be observed during interpreter startup before entering the guarded target; it does not execute the experiment after detecting parent loss. No native macOS claim was made.

Independent probe receipt:

```text
BEFORE APPROVED
COMMAND_EXIT 0
CLI_PRINTED_STATUS APPROVED
DURABLE_AFTER status=APPROVED, started_at=null, ended_at=null; original approval logs only
CLI_WHILE_OWNER 0
CLI_APPROVE_BLOCKED 1 BLOCKED
ORPHAN_AFTER_1S worker_state=Z, staging_exists=false
```

Root supplied full-suite evidence: 54 PASS, one inherited warning, and strict front-end build PASS. I inspected the relevant regressions rather than redundantly rerunning that suite. Final actual-browser and fresh-remote-recovery receipts remain with root.
