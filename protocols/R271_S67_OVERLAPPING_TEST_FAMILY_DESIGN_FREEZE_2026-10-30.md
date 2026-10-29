# R271 S67: overlap of candidate tests and finite familywise false-positive probability

Date: 2026-10-30 UTC. Track R. Baseline main HEAD: 38f714a2860fe4ff0e21776453e3f765068d05b0.
Original R271 remains frozen and its bounded E1 acceptance remains unchanged.

## Scientific status and exposure
This document fixes the exact computational extension before executing the archived S67 scripts. The researcher already derived possible overlap effects, including the rolling-window m=2 and m=3 examples, while designing the study. Therefore **STRICT_BLIND_PRESCORE_FREEZE=NO**, **PROSPECTIVE_CONFIRMATORY_STATUS=NOT_CLAIMED**, and all S67 results must be labeled exploratory finite artificial E1. This is a design/analysis version boundary, not a claim of independent preregistration.

## Frozen artificial source universe
All primitive bits are independent fair Bernoulli(1/2). Each candidate test observes a length-four bit window, tests H0:p=1/2 against p>1/2, and uses the exact one-sided Binomial(4,1/2) tail p-value. Candidate count m is exactly 1, 2, or 3.

Three observation designs:
1. IDENTICAL: every candidate uses bit positions {0,1,2,3}; primitive source length L=4.
2. ROLLING: candidate j uses positions {j,j+1,j+2,j+3}, j=0..m-1; L=m+3.
3. DISJOINT: candidate j uses positions {4j,4j+1,4j+2,4j+3}; L=4m.

Three reporting policies:
1. FROZEN_FIRST: test candidate 0 only, positive if raw p<=1/8.
2. FLEXIBLE_ANY: positive if any candidate raw p<=1/8; report lowest qualifying candidate index.
3. BONFERRONI_ANY: positive if any candidate raw p<=1/(8m); report lowest qualifying index.

Nominal familywise alpha=1/8. Exactly 3 designs x 3 family sizes x 3 policies = 27 worlds. Enumerate all 2^L primitive source strings for each world. The total number of policy-labelled source records is 3*sum_{m=1}^3 (2^4+2^(m+3)+2^(4m)) = 13584; these records include repeated primitive strings across designs and policies and are not independent human samples. For each world, primitive probability is 2^(-L).

## Frozen scoring and independent routes
R route: iterate all 13584 source records; calculate all candidate four-bit counts and exact p-values from raw bits, selected index, binary report and exact weighted familywise probability. Record the primitive bits, windows, p-values, selected index and source mass.

B route: without importing R source enumeration, compute the union of all-four-success events by inclusion-exclusion over the m windows. For any nonempty subset S of candidates, the intersection probability equals 2^(-number of distinct bit positions covered by S). For FROZEN_FIRST risk is 1/16. For FLEXIBLE_ANY risk is the exact union probability. For BONFERRONI_ANY use the same union probability only when 1/16 <= 1/(8m); otherwise risk is zero. Compare exact Fraction results for all 27 worlds. Include independent negative controls: identical windows cannot inflate above 1/16; m=1 designs agree; no positive risk under m=3 Bonferroni. Test mutation rejection of duplicate worlds, missing worlds, altered fractions, false E2 promotion and bool/int confusion.

Primary contrast: m=3 FLEXIBLE_ANY false positive rate across IDENTICAL, ROLLING and DISJOINT; secondary m=2 contrast. Do not treat the three designs as a causal evaluation of real preregistration policies. Source files, code, receipt and report must use new S67 paths, never alter R271 originals.

## Acceptance boundary
A complete S67 exploratory result requires local native Python execution, full primitive-source checksum, independent exact inclusion-exclusion agreement, and actual persisted receipt recheck. These are internal nonblind computational checks, not external independent replication. Any mismatch is retained as FAIL. GitHub CI is optional and must be skipped if zero-cost status cannot be confirmed. E1 only, new E2=0, new E3=0. R073 model and scoring, PESEN v0.1 and original R271 status remain frozen.
