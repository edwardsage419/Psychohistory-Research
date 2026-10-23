# R324 prescore freeze: psychometric risk perception, artificial two-axis geometry

Date: 2026-10-24. Original239 ID 01-017 (P2). Pre-result, pre-generator and pre-score protocol. Frozen by its Git commit. All quantities below are constructed by this project and have no estimated psychological interpretation.

## English primary sources
Fischhoff, Slovic, Lichtenstein, Read & Combs (1978), *How Safe Is Safe Enough? A Psychometric Study of Attitudes Towards Technological Risks and Benefits*, Policy Sciences 9:127-152, DOI 10.1007/BF00143739. Their empirical study elicited judgments about 30 activities/technologies from 76 participants and examined descriptive risk attributes.
Slovic (1987), *Perception of Risk*, Science 236:280-285, DOI 10.1126/science.3563507. Original psychometric risk research studies judgments about hazards, not a fixed universal deterministic dread/unknown equation.

## Prior-research reuse decision
Crosswalk v4.1 original 01-017 has no itemwise primary R. Existing R288/R318 are prospect valuation and R319 is discrete mixed logit, not psychometric risk-attribute elicitation or factor analysis. R323 Boolean mediation arithmetic is not a psychometric risk model. Prior ZIP content has not been exhaustively scanned; this decision is limited to current repository itemwise evidence.

## Frozen finite test universe
Enumerate all 16 binary quadruples (dread1,dread2,unknown1,unknown2), lexicographic order. For each of four constructed scoring worlds W0=(3,1), W1=(1,3), W2=(1,1), W3=(2,2), create one original row for each quadruple: exactly 64 CSV rows, weight 1/16 per world. Define D=dread1+dread2, U=unknown1+unknown2, score=a*D+b*U. There is no fitted PCA, psychometric factor estimation, human subject or original-data reconstruction. The two axes are investigator-assigned composite scores.

## Falsifiable predictions and exact checks fixed before output
P1: W0 dread-only hazard (1,1,0,0) has score 6 and unknown-only (0,0,1,1) has score 2; W1 reverses them (2 vs 6).
P2: W2 gives equal score 2 for the two hazards, despite their distinct D,U pairs. Thus one scalar rating is insufficient to reconstruct the two-dimensional attributes in this artificial universe.
P3: W3 score equals 2*W2 score on every state; W2 and W3 have identical weak rank ordering despite different coefficient scales.
P4: 16 unique states per world, mass exactly one, 64 unique (world,state) records, and no nonbinary inputs.
P5: For each world independent auditor recomputes scores without importing generator, verifies all CSV bytes, JSON result values and rank-reversal witness. Mutation of a score must fail.
P6: Python 3.11 and 3.12 unit jobs and a separate independent no-import auditor job must all succeed before formal bounded E1 acceptance. Until then status is PENDING.

## Evidence gates
Only artificial finite arithmetic E1 is eligible. No assertion of the original empirical factor loadings, factor identifiability, general human risk judgments, policy risk prediction, real E2 or historical E3. Scientific report must record these absences. Preserve R073 and PESEN v0.1 bytewise untouched. Original239 crosswalk may be updated only after source and CI pass; 173 provisional README links remain provisional. R-series completion precedes classification and model fusion. Personal decision-system construction remains deferred.
