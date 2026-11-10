# R268 log-free selection certificate and S64 end-to-end check

Base main0d086e5565d93438e67e45b2901b5adc35841412. Dedicated branch
codex-b/r268-logfree-certificate-20261110; only this Codex B directory changes.

No original numerical error has been found. The reproducibility gap is that the
original two selection routes both use floating logarithms, while S64 shares a
transcribed archived decision table. Add an independent exact decision proof and
use its derived decisions to verify the source, selection probabilities and S64
risks; do not claim a bug merely to produce work.

Proof: exact R=(L_MLE/L_fixed)^2, with0^0=1 endpoint continuation. BIC compares
R with integer n. AIC compares R with e^2, rigorously bracketed by the positive
exponential series: 19/3<e^2<67/9. Every frozen23(n,K) state lies outside this
interval. Use ln(x)>=(x-1)/x to certify lower score-separation margins. No math
log/exp, archived labels or floating epsilon enter the decision engine.

Independently build count probabilities by n Bernoulli polynomial convolutions,
not the original comb(n,k) route. Integrate both future outcomes explicitly for
S64 risks using derived decisions. Check all3312 source identities/masses/qhat/
labels,69 archived per-K records,27 selection probabilities and81S64 risk/excess/
paired values. Original floating scalar log columns are NOT independently
certified by this proof; check finite syntax and native replay byte identity
separately and state this boundary.

Execute original R268 --test/--emit in a disposable exact-code copy, not the
research folder; compare CSV/JSON/machine receipt bytes. Reexecute archived S64 B
CLI and distinguish its shared-label input from the new proof. Original R-route
S64 source CLI was not archived; do not pretend this new auditor is that program.

Files: certificate.py (integer/rational proof, count DP, risks), audit.py (scoped
source/JSON checks), test_certificate.py, replay.py, evidence/, report/handoff.
Review focus: rigorous exponential tail bound; endpoint0log0; true n penalty;
strict comparisons/types/coverage; honest proof vs scalar-log/native identity
scope. Standard library/installed runtime only, no human sources, paid API,
resource purchase, CI dispatch, model/metric/split change or automatic merge.

- [x] Hand-derived RED tests and proof implementation GREEN.
- [x] Scoped native auditor and deliberate input mutation rejections.
- [x] Original84 tests, new scoped tests and native replay ordinary/-O; inputs,
  actual commands, all derived certificates and source identities recorded.
- [x] One fresh-context review, necessary fixes, refresh latestmain/open PRs and
  deliver independent draft PR [skip ci], preserving original scientific status.
