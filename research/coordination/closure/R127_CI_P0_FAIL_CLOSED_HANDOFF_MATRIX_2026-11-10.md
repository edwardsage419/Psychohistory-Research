# R127 CI P0 fail-closed repair handoff and independent regression matrix

track: R-series independent closure
subflow: R127 05-003
run_date: 2026-11-10
observed_head: 60e1a27a4a8d9105ac72b8bed422eaae355e1b8a
target: .github/workflows/r127-van-huyck-1990-coordination-source-table-60-tests.yml
target_blob: 4b22f653dc7516bb31ead23e45dcf7f62261d79d
status: PARTIAL (local isolated controls completed; production workflow unchanged)
evidence_scope: engineering acceptance-integrity controls; new E1/E2/E3 evidence = 0
ci_status: NOT_RUN
billing_checked: no paid service requested; account billing NOT_VERIFIED
source_links: https://github.com/edwardsage419/Psychohistory-Research/blob/main/.github/workflows/r127-van-huyck-1990-coordination-source-table-60-tests.yml

## Scope and deduplication

This is an executable, consolidated handoff for the **previously established** optimized-assert and trailing-OK false acceptance defects. It does not count them again as new discoveries. Prior records:
* R127_CI_OPTIMIZED_ASSERT_NEGATIVE_CONTROL_2026-11-10.md
* R127_CI_LOG_TRAILING_OK_FALSE_ACCEPTANCE_2026-11-10.md
* R127_RECEIPT_WORKFLOW_RUN_IDENTITY_GAP_2026-11-10.md
* R127_CI_RECEIPT_REPLAY_IDEMPOTENCE_NEGATIVE_CONTROL_2026-11-10.md

## Reproducible local matrix

Run the following standalone Python 3 script. It does not import R127 or execute GitHub Actions. It reproduces the original two inline log-parser assertions and a candidate explicit-failure parser.

```python
import subprocess
import sys

historical = """import re,sys
log=sys.stdin.read()
assert re.findall(r'Ran (\\d+) tests? in',log)==['60']
assert re.search(r'\\nOK\\s*$',log)
print('R127_60_REAL_TESTS_SUCCESS')
"""

candidate = """import re,sys
log=sys.stdin.read()
counts=re.findall(r'(?m)^Ran (\\d+) tests? in [^\\n]+$',log)
if counts!=['60']: raise SystemExit('INVALID_COUNT')
if re.search(r'(?m)^\\s*(?:FAILED|ERROR|FAIL)(?:\\s|\\(|:|$)',log):
    raise SystemExit('FAILURE_MARKER')
if not re.search(r'(?m)^OK\\s*$',log): raise SystemExit('MISSING_OK')
if not re.search(r'\\nOK\\s*$',log): raise SystemExit('TRAILING_OK_REQUIRED')
print('R127_60_REAL_TESTS_SUCCESS')
"""

cases = {
    'valid': 'Ran 60 tests in 0.1s\n\nOK\n',
    'wrong_count': 'Ran 59 tests in 0.1s\n\nOK\n',
    'trailing_ok': 'Ran 60 tests in 0.1s\nFAILED (failures=1)\nOK\n',
    'duplicate': 'Ran 60 tests in 0.1s\nRan 60 tests in 0.1s\nOK\n',
}
for name, script in [('historical', historical), ('candidate', candidate)]:
    for optimized in (False, True):
        for case, log in cases.items():
            command = [sys.executable] + (['-O'] if optimized else []) + ['-c', script]
            result = subprocess.run(command, input=log, text=True, capture_output=True)
            print(name, 'optimized' if optimized else 'normal', case, result.returncode)
```

Observed locally (exit codes; 0=accepted, 1=rejected):

| Parser | Python mode | valid | wrong_count | trailing_ok | duplicate |
| --- | --- | ---: | ---: | ---: | ---: |
| historical | normal | 0 | 1 | 0 | 1 |
| historical | optimized | 0 | 0 | 0 | 0 |
| candidate | normal | 0 | 1 | 1 | 1 |
| candidate | optimized | 0 | 1 | 1 | 1 |

The historical parser text is transcribed from the pinned workflow blob. The candidate is an independently executed suggestion, not a patch applied to the workflow. These tests do not establish full CI bypass: the original unittest pipeline has `set -euo pipefail`.

## Mainline-owned minimal acceptance gate

1. Replace the two log-parser `assert` statements with explicit nonzero exit checks; require exactly one 60-test summary, one trailing OK, and absence of failure markers.
2. Replace every integrity-critical `assert` in the second inline Python stage with explicit checks that remain active under `-O` or `PYTHONOPTIMIZE`.
3. Independently mutate aggregate counts, E2=0 fields, and synthetic enumeration totals; require rejection in both modes. Confirm successful control inputs remain accepted.
4. Handle an unchanged receipt as a successful no-op rather than unconditional `git commit`. Preserve failure on actual conflicts.
5. Add an immutable sidecar for workflow blob, tested checkout SHA, run/job IDs and log hash. Preserve the historical receipt unchanged. Confirm the historical run source SHA `9c534a2a0604bf6191ba14393a22ea1ce07a752e` separately from result commit.
6. R mainline owns the workflow edit and final scientific conclusion. Recheck HEAD and target blob before any write. Do not trigger Actions until the free quota is confirmed.

## Scientific boundary

R127 remains CLOSED_BOUNDED, original catalogue 05-003 remains provisional pending itemwise scientific acceptance. No new human-level prediction, historical forecasting, external-team replication or E2/E3 evidence. This handoff does not reclassify the original 239 catalogue or alter frozen R073/PESEN v0.1 protocols.

blockers: original workflow still vulnerable; production repair and optimized end-to-end validation NOT_RUN; 05-003 closure NOT_RUN.
next_action: mainline-owned minimal workflow fix followed by independent local negative controls and bounded itemwise closure review.
