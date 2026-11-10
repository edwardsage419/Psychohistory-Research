# R127 stage-two E2 receipt masking negative control

date: 2026-11-10
track: independent closure
source_main_sha: 727eeea969a5f0d7f54865762808d2447821deab
target_workflow_blob: 4b22f653dc7516bb31ead23e45dcf7f62261d79d
scope: existing optimized-assert P0 defect, distinct stage-two E2 field coverage
status: LOCAL_NEGATIVE_CONTROL_PASS; PRODUCTION_FIX_NOT_RUN
evidence_grade: engineering-only; new E1/E2/E3 = 0
CI: NOT_RUN

## Source-specific observation

The R127 workflow's second Python stage checks `assert original['new_real_human_E2_prediction_scores']==0`. Later, the receipt independently assigns the literal `'new_real_person_level_E2_prediction_scores':0`. Under Python optimization the assertion is removed. Consequently a nonzero upstream score can coexist with a receipt field that still says zero. The actual published R127 result is not shown to have such a mismatch. This is an additional impact demonstration of the **already recorded** optimized-assert defect, not a new P0 issue.

## Minimal standalone executable negative control

```python
import subprocess
import sys
program = """
original={'new_real_human_E2_prediction_scores':7}
assert original['new_real_human_E2_prediction_scores']==0
receipt={'new_real_person_level_E2_prediction_scores':0}
print(receipt)
"""
for flags in ([], ['-O']):
    p=subprocess.run([sys.executable,*flags,'-c',program],capture_output=True,text=True)
    print('optimized' if flags else 'normal',p.returncode,p.stdout.strip())
```

Observed with local Python:

```text
normal 1
optimized 0 {'new_real_person_level_E2_prediction_scores': 0}
```

This isolated test models the exact field names, assertion, and literal receipt assignment. It does not execute the original R127 module or full workflow. The value 7 is deliberately synthetic, not a claim about the underlying experiment.

## Required mainline fix and independent acceptance

Use explicit error checks for every source aggregate, payoff and E2 guard in stage two. Construct a controlled upstream value 7 and require nonzero exit in normal and optimized modes. Require the receipt's E2 field to derive from the validated upstream value rather than an unbound literal, or independently compare both before writing. Keep the historical receipt immutable and record workflow/run identity in a separate sidecar. Recheck the target blob before editing; this closure track does not own the workflow. No Actions run or paid services were used. Account billing was not independently checked.

R127 remains CLOSED_BOUNDED. Catalogue 05-003 remains provisional. No additional human prediction, E2/E3, or historical forecasting evidence.
