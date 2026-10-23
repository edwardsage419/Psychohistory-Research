# R331 scientific report: exact heterogeneous retention mixture

Date 2026-10-24. Original239 02-014 Memory Decay Models. Formal grade **PASS_BOUNDED_E1_CONSTRUCTED_HETEROGENEOUS_RETENTION_ONLY**.

## Sources, prior work and reuse limits
Ebbinghaus (1885, translated 1913), *Memory: A Contribution to Experimental Psychology*, chapter 7, https://psychclassics.yorku.ca/Ebbinghaus/index.htm, studied relearning savings and retention over time. Wixted and Ebbesen (1991), *On the Form of Forgetting*, *Psychological Science* 2(6):409-415, https://doi.org/10.1111/j.1467-9280.1991.tb00175.x, compare empirical power and exponential forgetting functions. This study neither extracts nor fits their observations.

Before freeze, checked R330 four-instance retrieval source and report, R295 habit acquisition, R302 Bayesian bandits, original239 v4.8 and pending14 queue. R330's recency-weighted action retrieval does not establish time-delayed retention survival. Repository code search for forgetting, decay and Ebbinghaus found no exact reusable match. Historical ZIP itemwise review remains open.

## Temporal provenance and finite protocol
Protocol was committed first as [fce59316](https://github.com/edwardsage419/Psychohistory-Research/commit/fce59316d07acb73a2df5f1c6c60d7266faee4cc), followed by [c5350c6e](https://github.com/edwardsage419/Psychohistory-Research/commit/c5350c6e383b803f382f4c36785c80184e379822) containing executable source, independent auditor, exact raw CSV and JSON. No human or historical records were created or used.

Nine artificial worlds combine three distinct retention-base pairs (1/4,1/2), (1/4,3/4), (1/2,3/4) with fast-component mixture weights 1/4,1/2,3/4. At integer delays 0 through 8, the model records fast and slow contributions, their sum S(t)=w a^t+(1-w)b^t, and homogeneous one-step-matched comparator Q(t)=[w a+(1-w)b]^t. The full Cartesian product has **81 artificial source atoms** and nine world summaries, all exact rational fractions.

## Frozen predictions and exact results
At t=0 and t=1 the mixture and comparator agree in every world. For t=2 the gap equals w(1-w)(b-a)^2 and is strictly positive for all nine worlds. At t=2 through t=8 the gap remains positive. Mixture survival strictly decreases at each delay in all nine worlds.

The prespecified counterexample a=1/4, b=3/4, w=1/2 yields S(2)=5/16, Q(2)=1/4 and gap=1/16. At t=8, S(8)=3281/65536, Q(8)=1/256, gap=3025/65536. These are model-generated mathematical differences, and are not fitted estimates of forgetting.

## Independent audit and CI
Production Python standard library reproduces the CSV and JSON bytes. Seven unit tests cover world and row counts, equality at t=0/1, variance identity, late gaps, monotonicity, the frozen counterexample and byte replay. Independent no-import auditor independently enumerates all 81 atoms with Fraction, checks nine summaries, and rejects deliberate CSV tampering.

[GitHub Actions run 40041261725](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/40041261725) completed success at source commit c5350c6e with all three jobs green: Python 3.11 unit, Python 3.12 unit, and independent audit.

## Interpretation and strict evidence boundaries
This is a mathematical demonstration that aggregation of heterogeneous exponential survival rates produces a longer tail than a homogeneous exponential matched at t=1. It does not show that individual human memory traces follow either model, and it does not discriminate psychological decay from interference, retrieval failure or time-varying hazards. Original-author human E2=0, historical E3=0, original Ebbinghaus savings replication=NO, out-of-sample prediction=NO. Catalogue association is provenance, not empirical validation. R073 and PESEN v0.1 remain frozen; classification, fusion and personal decision system remain deferred.
