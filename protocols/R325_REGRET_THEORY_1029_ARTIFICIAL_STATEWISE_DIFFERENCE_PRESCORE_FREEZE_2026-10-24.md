# R325 prescore freeze: finite constructed regret comparison

Date 2026-10-24. Original239 01-020 (P2). Freeze precedes generator, results, scoring and CI.

## English primary literature
Loomes & Sugden (1982), *Regret Theory: An Alternative Theory of Rational Choice Under Uncertainty*, Economic Journal 92(368):805-824, DOI 10.2307/2232669.
Bell (1982), *Regret in Decision Making under Uncertainty*, Operations Research 30(5):961-981, DOI 10.1287/opre.30.5.961.
The original theoretical literature studies counterfactual outcomes and regret in risky choices. Our finite cubic comparison function is project-created and must not be attributed as an estimated or unique canonical equation.

## Reuse audit
Current original239 v4.2 lists 01-020 as pending. R287 finite EU arithmetic is reusable as a zero-regret baseline; R288 prospect valuation and R318 cumulative sign ranking are different from paired statewise counterfactual comparison; R324 risk composites are also different. No itemwise existing regret-theory R has been verified; full early ZIP content scan remains open.

## Frozen artificial universe
Enumerate all 7^3=343 ordered statewise A-minus-B payoff differences d1,d2,d3 in {-3,-2,-1,0,1,2,3}. Three equiprobable states per difference vector. For each of three project-created comparison worlds kappa=0,1/4,1, create one original CSV record for each vector, total **1029** source rows; each vector receives weight 1/343 within its world. Define Q_kappa(d)=d+kappa*d^3 and comparison advantage F_kappa=(Q(d1)+Q(d2)+Q(d3))/3. EU baseline E=(d1+d2+d3)/3. Strict preference for A if F>0, for B if F<0, otherwise tie. Use Python Fraction exact arithmetic; no estimated parameters, no real subjects, no randomness.

## Prespecified falsifiable checks
P1: Q is odd and strictly increasing for all real d when kappa>=0; within finite enumeration verify oddness and order for all seven d.
P2: For witness d=(3,-2,-2), EU advantage is -1/3; F_0=-1/3, F_1/4=7/12, F_1=10/3. Thus at kappa=1/4 and 1 the project-constructed regret rule reverses the strict EU preference.
P3: At kappa=0, F equals EU for all 343 difference vectors, with zero strict sign reversals.
P4: Exact 343 unique vectors per world, 1029 source rows, weights 1/343, and exact world mass 1. Sign symmetry under d -> -d must hold for all worlds. At least one strict reversal for each positive kappa.
P5: Independent no-import auditor enumerates 1029 rows, reconstructs exact fractions and counts, and fails on any source or result mutation.
P6: CI Python 3.11 and 3.12 tests plus separate independent audit must all pass before bounded E1 acceptance. Any failed CI is recorded.

## Evidence and governance
Finite project-created mathematical illustration E1 only. Do not infer Loomes-Sugden/Bell empirical replication, elicited regret, preference cycle, real human E2, historical E3 or causal mechanism. Original239 metadata is separate from scientific validity. R073 and PESEN v0.1 untouched. Complete all R-series learning/audit before taxonomy and fusion; personal decision-system implementation deferred.
