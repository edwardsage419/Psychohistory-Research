# R127 CI optimized-assert negative control (2026-11-10)

track: R-series independent closure
subflow: R127 05-003 integrity audit
run_date: 2026-11-10
observed_head: 27d22c5b52d8c9121fce8ea019726bd6e109154c
scope: .github/workflows/r127-van-huyck-1990-coordination-source-table-60-tests.yml (blob 4b22f653dc7516bb31ead23e45dcf7f62261d79d); historical run 39348775741, head 9c534a2a0604bf6191ba14393a22ea1ce07a752e
status: PARTIAL, confirmed local negative control; historical run itself is a genuine ordinary-mode success
evidence: engineering integrity negative control, NOT new E2/E3 science
CI: NOT_RUN in this audit
billing_checked: no new paid service requested; actual account billing NOT_VERIFIED

## Verified source and executable counterexample

The workflow's first inline Python receipt gate uses two bare `assert` statements to check the exact 60-test count and trailing OK marker, then unconditionally prints `R127_60_REAL_TESTS_SUCCESS`. The second inline Python gate uses bare `assert` for published aggregates, payoff checks, enumerated counts, and zero E2 evidence. Python optimized execution strips these statements.

Reproduce without importing the audited implementation:

```sh
cat > /tmp/r127_assert_probe.py <<'PY'
import re
log = 'Ran 59 tests in 1.0s\n\nFAILED (failures=1)\n'
assert re.findall(r'Ran (\d+) tests? in', log) == ['60'], 'R127_REQUIRE_ALL_60_TRUE_TESTS'
assert re.search(r'\nOK\s*
print('R127_60_REAL_TESTS_SUCCESS')
PY
python /tmp/r127_assert_probe.py; echo "normal_exit:$?"
python -O /tmp/r127_assert_probe.py; echo "optimized_exit:$?"
```

Observed local output:
```text
AssertionError: R127_REQUIRE_ALL_60_TRUE_TESTS
normal_exit:1
R127_60_REAL_TESTS_SUCCESS
optimized_exit:0
```

The synthetic failed log is an intentionally invalid input. This proves the *receipt parser's* optimized-mode fail-open behavior. It does not prove that the full CI job accepts a failed unittest run: `set -euo pipefail` plus the unittest command piped to tee will reject a nonzero unittest exit before the receipt parser. A subprocess that exits zero while printing incorrect count or a misleading OK marker is a narrower plausible route, untested end-to-end. The source's aggregate scientific assertions are also skipped under optimization. Historical CI ran normally and was successful; no historical numeric error established.

, log), 'R127_TRUE_TESTS_NOT_ALL_PASS'
print('R127_60_REAL_TESTS_SUCCESS')
PY
python /tmp/r127_assert_probe.py; echo "normal_exit:$?"
python -O /tmp/r127_assert_probe.py; echo "optimized_exit:$?"
```

Observed local output:
```text
AssertionError: R127_REQUIRE_ALL_60_TRUE_TESTS
normal_exit:1
R127_60_REAL_TESTS_SUCCESS
optimized_exit:0
```

The synthetic failed log is an intentionally invalid input. This proves the *receipt parser's* optimized-mode fail-open behavior. It does not prove that the full CI job accepts a failed unittest run: `set -euo pipefail` plus the unittest command piped to tee will reject a nonzero unittest exit before the receipt parser. A subprocess that exits zero while printing incorrect count or a misleading OK marker is a narrower plausible route, untested end-to-end. The source's aggregate scientific assertions are also skipped under optimization. Historical CI ran normally and was successful; no historical numeric error established.

## Recommended scoped handoff

R mainline owns workflow changes. Replace every integrity-critical `assert` in inline workflow checks with explicit `if not condition: raise SystemExit(...)` or a separate fail-closed validator. Retest ordinary and `-O` modes with wrong test count, wrong aggregate and nonzero E2 fields. Do not alter frozen research results or historical receipts. Check `PYTHONOPTIMIZE` environment assumptions. Do not dispatch CI until free quota is verified.

R127 remains CLOSED_BOUNDED in its final status; 05-003 remains PROVISIONAL in original-239 queue. No queue status changed; E1 mathematical results unchanged; E2/E3 new evidence 0.
source_links:
https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39348775741
https://github.com/edwardsage419/Psychohistory-Research/blob/27d22c5b52d8c9121fce8ea019726bd6e109154c/.github/workflows/r127-van-huyck-1990-coordination-source-table-60-tests.yml
blockers: no independent end-to-end optimized CI execution; historical source identity established; source-level guard remains weak.
next_action: mainline-owned minimal explicit-exit repair and local negative controls, followed by 05-003 itemwise closure review.
