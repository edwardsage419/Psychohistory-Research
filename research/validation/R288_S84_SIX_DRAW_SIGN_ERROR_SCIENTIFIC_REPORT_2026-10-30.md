# R288 S84: finite six-draw preference-sign error under reference-dependent value

Date 2026-10-30 UTC. Track R. NEW_SUBSTUDY_PARTIAL, E1 artificial internal nonblind.
Prescore protocol commit: 96a40fc1efe64aaa46c149b4c24d7f09294f5ec8.
Original R288 freeze: d94d9d7f275082a6672fbea0e191ac76a54bed87; original R288 status CLOSED_BOUNDED_E1 remains unchanged.
Source: Kahneman and Tversky (1979), Prospect Theory: An Analysis of Decision under Risk, Econometrica 47(2):263–291, DOI 10.2307/1914185. This project studies only the archived piecewise-linear loss multiplier submodel, without probability weighting, human choices, or original paper empirical replication.

## Frozen question and evidence
A six-draw sample of the original G gamble (independent 1/2 chance of +3 or -2 each draw) is used to infer the sign of G's reference value relative to a sure-zero option. How often does that sign disagree with the exact population sign? The frozen original nine worlds are reference r in {-2,0,2}, loss L in {1,2,3}. Each world has all 64 ordered six-bit outcomes, probability 1/64 each, for 576 original source atoms.
Original persisted CSV Git blob 0e6a3b7088d2742f0e5af05335d00638b15130a9. R route reads every persisted original row, verifies the six-bit identity, all six payoffs and reference values, sure value, source probability, realized mean and difference, then classifies every row. Independent B route derives all probabilities from seven binomial count cells per world, without importing the original enumeration.

## Exact results
All probabilities are exact fractions. CORRECT is the same strict sign as the population difference, WRONG the opposite strict sign, TIE exactly zero. No ties are removed from the unconditional denominator.

| r | L | population G minus S | correct /64 | wrong /64 | tie /64 | P(wrong given non-tie) |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| -2 | 1 | 1/2 | 42 | 22 | 0 | 11/32 |
| -2 | 2 | 1/2 | 42 | 22 | 0 | 11/32 |
| -2 | 3 | 1/2 | 42 | 22 | 0 | 11/32 |
| 0 | 1 | 1/2 | 42 | 22 | 0 | 11/32 |
| 0 | 2 | -1/2 | 42 | 22 | 0 | 11/32 |
| 0 | 3 | -3/2 | 42 | 7 | 15 | 1/7 |
| 2 | 1 | 1/2 | 42 | 22 | 0 | 11/32 |
| 2 | 2 | 1/2 | 42 | 22 | 0 | 11/32 |
| 2 | 3 | 1/2 | 42 | 22 | 0 | 11/32 |

In all nine worlds the probability of observing the correct strict sign is 42/64 = 65.625%. Eight worlds have 22/64 = 34.375% wrong signs. At r=0,L=3, the six-draw sample ties when exactly four high payoffs occur, probability C(6,4)/64 = 15/64 = 23.4375%; strict wrong signs have probability 7/64 = 10.9375%. The lower unconditional wrong rate in that world coexists with a substantial tie rate and must not be interpreted as a higher probability of correct classification. Conditional wrong among non-ties is 7/49 = 1/7.
These are properties of six artificial independent fair draws and the frozen value function. They are not empirical human preference error rates, and no model has been fitted or selected.

## Executed audit and boundaries
Original R route recomputed 576 persisted source rows and produced a 576-row derived CSV. All nine probability masses are 1 and every source key is unique. Five source mutations (duplicate, missing, probability, realized difference, bit identity) were rejected. Independent binomial 7-cell per world oracle matched all nine world summaries. Archived R JavaScript source was fetched again from main and executed in V8 against the original source; regenerated 576-row CSV was byte-identical to the persisted derived CSV and all nine JSON result objects matched. Archived original R Node CLI was NOT_RUN.
Independent local Python 3 route executed successfully with exact Fraction and math.comb; the newly archived B Python file has not been independently executed from its remote bytes. Six B summary mutations were rejected in the local equivalent implementation. This is nonblind internal replication, not external replication. No train/test split, calibration estimate, resampling confidence interval or historical population claim applies to this exhaustive artificial finite distribution.

## Artifacts and acceptance
Protocol: research/validation/R288_S84_SIX_DRAW_SIGN_ERROR_PRESCORE_FREEZE_2026-10-30.md
R source: research/validation/r288_s84_sign_error_20261030.js
576 derived rows: research/validation/R288_S84_ALL_576_SIGN_RECEIPTS.csv
Exact JSON: research/validation/R288_S84_EXACT_RESULTS.json
B source: research/evidence_audit/b_r288_s84_independent_binomial_20261030.py
B audit: research/evidence_audit/B_R288_S84_NONBLIND_BINOMIAL_AND_REMOTE_RECEIPT_AUDIT_2026-10-30.md

A01 PASS for bounded question; A02 PASS original fixed blob; A03 OPEN original native Node and archived B Python CLI; A04 PASS source mutations and explicit ties; A05 PASS E1-only inference boundary; A06 OPEN external review and full native replay. S84 SCIENTIFIC_ACCEPTANCE=PARTIAL. Original R288 status unchanged. E2 new human predictions 0, E3 historical predictions 0, external team replication 0. R073 and PESEN v0.1 FROZEN. No paid resources and no Actions initiated; actual account billing and free quota were not checked.
