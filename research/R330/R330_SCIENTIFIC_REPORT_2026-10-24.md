# R330 scientific report: exact four-instance cue and recency retrieval
Date 2026-10-24. Original239 **02-013 Instance Based Learning**, P2. Formal scientific grade **PASS_BOUNDED_E1_CONSTRUCTED_FOUR_INSTANCE_RETRIEVAL_ONLY**.

## English primary source and reuse
Gonzalez, Lerch & Lebiere (2003), *Instance-based learning in dynamic decision making*, Cognitive Science 27(4):591–635, DOI 10.1207/s15516709cog2704_2. Their theory discusses situation-action-utility instances, similarity-based recognition, adaptive strategies and feedback. This R330 study implements only a project-defined four-instance weighted retrieval analogue. It does not implement the authors' ACT-R cognitive model or reproduce their original human experiments.

Before freeze, inspected R295 habit cue/valuation, R302 Bayesian bandits and R303 observational learning scoped reports. None proves this fixed cue-similarity and recency retrieval score. Historical ZIP itemwise audit remains open.

## Prescore protocol, full artificial data and algorithm
Frozen protocol committed as [0d51148a63e16abdc9505e2c57fab0488e27e0b5](https://github.com/edwardsage419/Psychohistory-Research/commit/0d51148a63e16abdc9505e2c57fab0488e27e0b5) before the source/code commit [dfa4e045d08ae60459cb1ad355ca5dd417ea1694](https://github.com/edwardsage419/Psychohistory-Research/commit/dfa4e045d08ae60459cb1ad355ca5dd417ea1694).

The four artificial memories are (time1,A,cue0), (time2,B,cue1), (time3,A,cue1), (time4,B,cue0), each with binary utility. All 16 binary outcome histories are crossed with 2 query cues and 2 decay exponents. This yields 64 worlds and **256 complete artificial memory source rows**, with exact rational weights w_i=(1 for cue match, otherwise 1/2)*(5-time_i)^(-decay). Each action's score is its own weighted utility average, and ties choose A. No real participants or sampled empirical observations.

## Frozen counterexamples and results
For history 1001 and cue0, decay0 gives A=2/3 and B=2/3, so tie-break A. Decay1 gives A=1/2 and B=6/7, so B. For history 1100 and decay0, cue0 gives A=2/3, B=1/3 and selects A; cue1 gives A=1/3, B=2/3 and selects B. These are deterministic model-generated reversals caused by the predeclared cue and recency weights. Across the 64 constructed worlds, A is selected in 38 and B in 26.

## Independent audit and GitHub Actions
Standard-library Python regenerates both CSV and JSON byte for byte. Six unit tests cover row counts, score bounds, two prespecified counterexamples, zero-outcome control and byte replay. An independent auditor imports no production code and re-enumerates all 256 source atoms with rational arithmetic. A deliberate source alteration is rejected.

[GitHub Actions run 40035835578](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/40035835578) completed success, with Python 3.11, Python 3.12 and independent audit jobs all green. Machine receipt pins protocol/source Git blob identities.

## Scientific boundary
E1 proves arithmetic for a fixed four-instance artificial lookup scheme. It does not identify real human retrieval, memory trace decay, ACT-R activation, stochastic recall, feedback learning, original-author data, human E2, historical E3, or external predictive performance. Directory mapping is only provenance. R073 and PESEN v0.1 unchanged; classification, fusion and personal decision system deferred.
