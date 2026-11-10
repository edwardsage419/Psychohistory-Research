# R077 numerical scoring acceptance plan

Base main: e5f2baa7f6b13b1a2bf95f48ed49571f732e7611.
Branch: codex-b/r077-score-leakage-20261110, independent of draft PR #13.

Goal: close the demonstrated R077 synthetic test gap: replace
pred=predict(model,row,fit) with pred=(predict(model,row,fit)+row[4])/2 and
all 24 original guards still pass. This contaminates prediction with the current
label, quarters Brier, and leaves the claimed target training count at zero.
Original implementation is not alleged to have this error.

Design: new Codex B directory only. Independently calculate probabilities from
synthetic source sufficient statistics using Fraction, squared loss exactly and
log loss with 70-digit Decimal logarithms. Group artificial events into 32 bins
per session; session-average then equal-weight aggregate. Compare the complete
public score tree (seven models, both treatment groups, six pairs/sign counts,
denominators/types/metadata), with bounded float tolerances. No original scoring
or prediction helper imported by the oracle.

Use coherent populated synthetic source tables at p0=1/2 and p0=1/4, all 16
history states, both current outcomes, unequal target session sizes, and flipped
targets. Include hand calculations, label-pair loss identities, empty/malformed
inputs and full-schema mutations. Run actual source-file mutations in temporary
copies: current-label contamination, Brier used as log loss, and row-weighted
macro as a detection control. Keep original source/frozen protocols unmodified.

Alternative: more string-inspection or fit-object immutability assertions do not
check numeric predictions; changing frozen R073 or rescoring humans is outside
scope. Autonomous execution/independent PR is already authorized by the user.

Files: score_oracle.py (independent math/full-tree validation),
test_score_oracle.py (synthetic fixture/hand and adversarial tests), replay.py
(commands, authentic source hashes, original suites, sandbox mutants), evidence/,
REPORT.md and this plan/progress record. Standard library only; no CI dispatch,
paid APIs/resources, dependencies, human downloads/scoring or model retuning.

Review focus: accidental current-label dependence; equal session rather than
row weighting; correct log loss and finite numerical types; paired signs/ties;
vacuous acceptance and stale success artifacts. Evidence is internal nonblind
artificial program verification, not new empirical E2/E3 or external replication.

- [x] Write regressions and record RED with a no-op oracle.
- [x] Implement independent scoring and full typed output comparison; GREEN/-O.
- [x] Run pinned original and actual-file mutant suites with numerical guard;
  record full commands, outputs, code/protocol hashes and counterexample.
- [x] Fresh-context review, RED/GREEN fixes as needed, final scoped replay,
  refresh remote state, push [skip ci] and create/attach a draft PR; never merge.
