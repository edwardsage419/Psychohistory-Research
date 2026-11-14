# R183 / 08-007: 45-world held-out logloss independent scoring check

Date: 2026-11-14. Closure-track, bounded internal E1 numerical audit.

## Fixed source and method

Read `research/R183/R183_EXACT_RESULTS.json` from current main, Git blob `81f8fa790f0dea2715d99e1384ec33a6d2cf7a64`, and frozen protocol `protocols/R183_LOGISTIC_SEPARATION_45_WORLDS_PRESCORE_FREEZE_2026-10-21.md`, blob `e01003e1899739b42b2ed746f1837b8591e870b6`. Previous 45-world exact PMF and rational-field audit is `R183_08-007_ALL_45_WORLDS_INDEPENDENT_RATIONAL_AUDIT_20261114.md`, blob `2d14bd887c23add14e01f58cfe21b4d31ea0054e`. This check addresses the previously unverified *numerical held-out logloss* field only.

Independently implemented JavaScript IEEE-754 scoring loop, without importing the R183 Python scorer. For each of the 45 worlds, parse the archived rational source PMF entries to doubles, enumerate every ordered pair (k0,k1), compute half-count predictions q_x=(k_x+0.5)/(n+1), and compute the expected two-group held-out Bernoulli logloss:

L = 0.5 * sum_{k0,k1} P0(k0) P1(k1) * [ -p0 log(q0) -(1-p0) log(1-q0) -p1 log(q1) -(1-p1) log(1-q1) ].

Use Math.log(q) and Math.log1p(-q), then compare against each stored `halfcount_expected_test_logloss_float` at the prespecified 1e-12 absolute tolerance. The source PMFs were read from the audited JSON; their independent reconstruction is evidenced by the separate 1035-comparison exact audit. Thus this is an independent *score calculation conditional on the archived PMFs*, not a new independent upstream source identity check.

## Observed computation

45 worlds; 4125 ordered count pairs enumerated; 45 numerical logloss comparisons; zero mismatches at 1e-12; maximum absolute difference `4.440892098500626e-16`. The first world stored value was `0.5410010019653647`.

Reproducible core JavaScript (run in Node.js with `node audit.js` after saving the repository result JSON locally as `R183_EXACT_RESULTS.json`):

```js
const fs = require('node:fs');
const d = JSON.parse(fs.readFileSync('R183_EXACT_RESULTS.json', 'utf8'));
const F = s => { const [a,b='1'] = s.split('/'); return Number(a)/Number(b); };
let pairs=0, maxDelta=0, failed=0;
for (const w of d.worlds) {
  const n=w.n_per_group, p0=F(w.true_p0), p1=F(w.true_p1);
  const a=w.source_group0_full_count_PMF.map(F), b=w.source_group1_full_count_PMF.map(F);
  let score=0;
  for (let k=0;k<=n;k++) for (let j=0;j<=n;j++) {
    const q0=(k+.5)/(n+1), q1=(j+.5)/(n+1);
    const loss=0.5*(-p0*Math.log(q0)-(1-p0)*Math.log1p(-q0)
                    -p1*Math.log(q1)-(1-p1)*Math.log1p(-q1));
    score+=a[k]*b[j]*loss; pairs++;
  }
  const delta=Math.abs(score-w.halfcount_expected_test_logloss_float);
  maxDelta=Math.max(maxDelta,delta);
  if (delta>1e-12) failed++;
}
console.log({worlds:d.worlds.length,pairs,maxDelta,failed});
if (failed) process.exitCode=1;
```

## Scientific disposition

**PASS, bounded E1 numerical scoring verification**. The 45 stored half-count expected logloss values agree with an independent JS implementation using the archived PMFs. This adds one verification dimension beyond the previous exact rational arithmetic audit. The original 60-digit Decimal.ln pathway, original native Python execution, R177 source JSON SHA256, raw 4125-row CSV byte hashes, and CI-produced artifact byte identity remain unverified in this check.

Research status remains `CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_LOGISTIC`. Catalogue 08-007 remains ACTIVE/provisional pending itemwise disposition. New E2=0, E3=0, formal catalogue closures=0. No CI invocation, frozen-protocol edit, or PR merge.
