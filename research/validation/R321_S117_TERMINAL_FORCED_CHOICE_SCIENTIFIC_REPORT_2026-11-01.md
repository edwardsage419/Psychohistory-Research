# R321 S117 scientific report: terminal forced choice versus seven-sample majority
Date: 2026-11-01 UTC. Research track R. Scope: artificial finite Bernoulli sequential likelihood-ratio stopping. Status: PARTIAL_E1_EXTENSION. Original R321 PASS_BOUNDED_E1_FINITE_WALD_INSPIRED_ONLY unchanged.

## Research question and temporal freeze
How does a finite threshold-stopping rule with mandatory terminal decision at sample seven compare to observing all seven Bernoulli samples before a majority decision? S117 protocol was committed **before** these calculations at a6a4034604d21ffc056086aa786ad93c24625d4a. Reused original frozen R321 source from 2026-10-24: 8 worlds, 1024 seven-bit exogenous paths, CSV Git blob d5e5e183a786e199fbf792589ed68735f30ca1b3, world JSON blob 5d8a6e807a099ab8b3e653c519a198497335fded, original protocol blob 211fc14095398194849995d2795a5e12c2feba69. Original R321 source and acceptance were not modified.

## Methods
S: accept H0/H1 on first threshold crossing, otherwise force a seven-bit majority decision at the horizon. F: always use seven samples and majority. A: original threshold policy with undecided mass at horizon. The exogenous seven-bit paths define the common mathematical counterfactual, including hypothetical suffixes after S would have stopped; those suffixes are not observed behavior under S. All calculations use exact rational mass under each frozen true Bernoulli hypothesis. Errors are unconditional wrong-decision probabilities for fully deciding S and F. Original A conditional error is reported separately and must retain its undecided fraction.

## Exact results
Each paired H0/H1 world has symmetric error and time, so the table shows both truths in one row. Every one of the eight original worlds was individually computed and checked.

| (p0,p1) | K | S error | F error | S minus F error | P(S disagrees F) | E[S samples] | A undecided |
|---|---:|---:|---:|---:|---:|---:|---:|
| (1/4,3/4) | 2 | 221/2048 | 289/4096 | 153/4096 | 63/1024 | 1579/512 | 27/512 |
| (1/4,3/4) | 3 | 605/8192 | 289/4096 | 27/8192 | 27/4096 | 609/128 | 729/4096 |
| (1/3,2/3) | 2 | 463/2187 | 379/2187 | 28/729 | 68/729 | 2458/729 | 64/729 |
| (1/3,2/3) | 3 | 43/243 | 379/2187 | 8/2187 | 8/729 | 47/9 | 8/27 |

In all eight artificial worlds, S takes fewer than seven samples on average and has strictly greater unconditional error than F. Every S/F disagreement is associated with an early stop; a path that reaches the horizon without stopping uses exactly the same majority rule as F. Raising K from 2 to 3 reduces the excess error and disagreement, while increasing expected samples and undecided mass under A. The quantitative tradeoff depends on these frozen two hypothesis pairs, thresholds, horizon and decision rules.

For example, under p0=1/4,p1=3/4,K=2, S error=221/2048 (~10.79%) and F error=289/4096 (~7.06%), a 153/4096 (~3.74 percentage point) difference; S expected sample count=1579/512 (~3.08) versus F=7. The 63/1024 (~6.15%) counterfactual disagreement is a different quantity from the error gap.

## Actual verification and limitations
R calculations read and checked the **actual original 1024-row CSV** via the connected GitHub repository and used integer exact masses. Independent B-route Python 3.13.5 Fraction enumeration was executed locally on all 8 worlds, and its result fields matched the persisted R result. A separate V8 full-source audit checked 1024 row identities and original fields, original eight-world receipts, and rejected 9/9 injected corruptions (missing row, duplicate, probability, first-hit time, decision, censor, path bits, world ID, truth label). An additional remote persisted-receipt comparison checked 56 expected values and original fields. B script exact local Git blob 4d4b10bcbbce72fc97f1663e87fd6cb3ebac7f8c matched the archived GitHub file. R Python source and results are archived for later native command-line replay; the archived R Python CLI has not been directly executed in this run. No external independent group replicated this result.

A01 scope PASS; A02 source identities PASS; A03 exact V8 and independent local Python PASS, archived primary CLI replay OPEN; A04 9 mutation controls PASS, empirical falsification OPEN; A05 E1 only PASS for boundary statement; A06 scoped archive and remote identity verification PARTIAL pending native replay. Scientific grade PARTIAL_E1_EXTENSION. No general Wald optimality, human reaction-time fit, independent real-person E2, historical E3, sample-out-of-distribution prediction, calibration or causal identification. R073 and PESEN v0.1 frozen. No CI dispatched because zero-cost entitlement was not independently verified.

## Replay paths
R program: research/validation/r321_s117_terminal_policy.py; exact receipt: research/validation/R321_S117_TERMINAL_FORCED_CHOICE_EXACT_RESULTS.json; B independent program: research/evidence_audit/b_r321_s117_independent_enumeration.py. R CLI: python research/validation/r321_s117_terminal_policy.py --source-csv research/R321/R321_ALL_1024_ORIGINAL_SEVEN_BIT_PATHS.csv . B CLI: python research/evidence_audit/b_r321_s117_independent_enumeration.py . Both require only Python standard library. No source files overwritten.
