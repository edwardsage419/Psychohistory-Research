# R074/R075 session training validation plan

Goal: close a demonstrated synthetic-test blind spot where repeating one eligible
training session and omitting another passes both archived suites (20/20, 24/24).
Base: e5f2baa7f6b13b1a2bf95f48ed49571f732e7611.

Design: retain every frozen research file. In this Codex B directory add an
independent 32-bin binary contingency-table oracle. Aggregate the full treatment
table then subtract the heldout table; project onto the four frozen state spaces.
Use exact Fraction arithmetic for prevalence and smoothed probabilities. Compare
the original trainers on unequal-size and equal-size heterogeneous fictional
sessions. Replay real subprocess suites in disposable copies, including both the
surviving duplicate-donor mutation and a heldout-leak positive detection control.

Alternatives: changing R073 violates the frozen-code scope; merely adding a
heldout-flip test duplicates existing protection. Distinct sessions plus full
count comparison address the observed blind spot without either change.
Python standard library only. All inputs generated here are artificial. No human
source downloads/scoring, parameter changes, CI dispatch, paid API, or merge.
Autonomous implementation and independent PR are explicitly authorized by the user.

Files: fit_oracle.py (independent math/fit validation); test_fit_oracle.py
(hand-calculated and adversarial regressions); replay.py (sandbox execution,
source hashes, original and mutant logs); REPORT.md; evidence/ (actual outputs).

Review focus: equal-total omitted/duplicated sessions; foreign-treatment/heldout
contamination; all conditional states including unseen; malformed numerical
types/NaN; distinguishing mutation survival from an actual historical model bug.

- [x] Write failing tests for hand-derived 3/8 prevalence, full state counts,
  malformed fit values, and counterexamples; preserve RED execution.
- [x] Implement exact oracle and cross-check frozen trainers on every fold,
  all 32 binary events, and label-flip prediction invariance; verify GREEN/-O.
- [x] Replay four archived synthetic suites; run duplicate and heldout mutants
  of R074/R075 as actual subprocesses; require old-suite survival only for the
  duplicate mutant, and new guard rejection for both mutations.
- [ ] Record sources/commands/environment, review branch, refresh main and open
  PR scope, and publish a draft incremental PR with [skip ci]. Do not merge.

Scientific acceptance unchanged; new human E2/E3 and external-team replication=0.
