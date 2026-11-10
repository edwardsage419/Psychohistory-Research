# R077 exact paired Brier direction supplement

Base main e5f2baa7f6b13b1a2bf95f48ed49571f732e7611; independent branch
codex-b/r077-exact-paired-ties-20261110. User authorized continued numerical
engineering, synthetic counterexamples, independent verification and draft PRs.

Actual defect: unmodified R077 float accumulation changes equal/better votes
when the same seven artificial events are permuted. Coherent32-row source gives
p(M1)=1/2 and p(M3)=5/14 for one history; three positive/four negative targets
have exact Brier1/4 for both. Of35 permutations, Python3.12 currently reports
24 ties and11 improvements, even though all exact risks are identical. This is
not a deliberate source mutation and not a historical human re-score.

Implement a minimal reusable exact paired-loss kernel accepting strictly typed
(binary outcome,Fraction candidate probability,Fraction reference probability)
records. Average within sessions, then equal-weight sessions; report exact
rational risks/deltas and categorical counts with no epsilon. It does not fit,
choose models, extract raw histories or replace the original scoring protocol.
Keep original programs/receipts unchanged and label the output as a supplementary
internal artificial computation. Do not duplicate PR16's complete seven-model
scoring oracle; this package addresses its documented exact-tie boundary.

Independent proof: put both probabilities over denominator14, squared integer
error sums are343 for each, denominator7*14^2=1372, giving1/4. Recompute all35
permutations with that integer route. Include a genuine arbitrarily small
nonzero rational delta to prove the repair does not silently turn small effects
into ties; include unequal-size sessions to protect macro weighting.

Files: exact_pair.py (exact loss/summary/check), case.py (fictional source, target
permutations and integer witness), test_exact_pair.py, legacy_regression.py
(intentional failing regression on original code), replay.py, evidence/, report
and handoff. Python standard library only, existing3.12/3.13 runtimes, normal/-O.
No dependency installation, human source loading/scoring, paid API/resource, CI
dispatch, parameter/split/metric change or automatic merge.

Review focus: floating exact ties vs real tiny effects; ordering invariance;
session vs row averaging; bool/float/NaN probability rejection; empty/vacuous
success and preserving expected FAIL of the original regression in reports.

- [ ] Record failing original regression and no-op exact-kernel RED.
- [ ] Implement exact supplement; GREEN and meaningful negative controls.
- [ ] Original23+24 and new scoped tests, integer proof and35 permutations in
  available Python3.12/3.13 normal/-O, authentic source hashes and raw logs.
- [ ] Fresh-context review, necessary corrections, final replay, latest main/PR
  scope refresh and dedicated draft PR with [skip ci]; never merge.
