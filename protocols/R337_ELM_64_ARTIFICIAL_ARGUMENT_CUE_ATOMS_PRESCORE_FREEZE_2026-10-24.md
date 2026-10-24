# R337 prescore protocol: finite elaboration and cue weighting contrast

Date 2026-10-24. Original239 03-015 Elaboration Likelihood Model. State FROZEN_BEFORE_ARTIFICIAL_SOURCE. Scope constructed E1 only.

## Literature and reuse

Petty and Cacioppo (1986), *The Elaboration Likelihood Model of Persuasion*, DOI 10.1016/S0065-2601(08)60214-2; Petty, Cacioppo and Schumann (1983), *Central and Peripheral Routes to Advertising Effectiveness: The Moderating Role of Involvement*, DOI 10.1086/208954; Petty, Cacioppo and Goldman (1981), *Personal Involvement as a Determinant of Argument-Based Persuasion*, DOI 10.1037/0022-3514.41.5.847. These original sources report human persuasion patterns. No participant-level source data is available for R337.

[Strict reuse preaudit](../docs/ORIGINAL_239_03-015_ELABORATION_LIKELIHOOD_REUSE_PREAUDIT_2026-10-24.md) inspected R322, R291, R292, R307 and R336 reports. No exact existing factorial route-weighting model verified. Early R001–R064 ZIP itemwise audit remains blocked. This protocol makes no exhaustive novelty claim.

## Frozen complete artificial universe

Enumerate involvement i in {0,1}, ability b in {0,1}, argument quality q in {-1,1}, source cue e in {-1,1}, and cue visibility c in {0,1}. Exactly 2^5=32 distinct worlds. Each world stores two artificial source rows, ROUTE_GATE and FIXED_ADDITIVE, for exactly 64 original artificial records.

The project-created route gate g=i*b. ROUTE_GATE score = 2q if g=1; otherwise c*e. FIXED_ADDITIVE score = q+c*e for every world. Scores are arbitrary integers with no empirical calibration, likelihood or behavioral interpretation. This is a deliberately restricted binary schematic, not the complete ELM, its continuum or a universal claim about cognitive processing.

## Frozen falsification conditions

F1: exactly 32 complete worlds, 64 rows, two models per world, all inputs in their specified sets.
F2: exactly 8 central-gated worlds; 24 other worlds. When g=1, ROUTE_GATE is independent of cue e and visibility c. When g=0 and c=0, its score is zero in exactly 12 worlds.
F3: holding i,b,e,c fixed and flipping q, 4 central pairs change ROUTE_GATE score by 4 and 12 low pairs by 0.
F4: holding i,b,q fixed, with c=1 and flipping e, 2 central pairs change ROUTE_GATE by 0 and 6 low pairs change it by 2.
F5: ROUTE_GATE and FIXED_ADDITIVE agree in exactly 2/32 worlds and differ in 30/32. The two agreeing worlds have g=1, c=1 and e=q. This is a constructed observational equality case, not psychological identification.
F6: independent no-production-import auditor enumerates all 32 worlds via different index arithmetic, reconstructs CSV and JSON byte for byte and rejects a deliberately changed CSV score and JSON score.
F7: Python 3.11 and 3.12 production tests and an independent GitHub Actions audit must each complete success before formal bounded E1 acceptance.
F8: this protocol must precede source and result commits. Update original239 provenance only after successful CI and scientific report. No real human E2, historical E3 or original 1983 experiment replication.

R073 and PESEN v0.1 frozen. R-series research and evidence audit precede classification and fusion. Personal decision system deferred.
