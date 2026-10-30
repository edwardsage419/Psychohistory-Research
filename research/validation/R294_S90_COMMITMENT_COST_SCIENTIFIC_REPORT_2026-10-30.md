# R294 S90: exact finite-grid commitment-fee sensitivity
Date 2026-10-30 UTC. Track R. Status PARTIAL, E1 synthetic, nonblind internal calculation. Original R294 CLOSED_BOUNDED_E1 status unchanged.
## Provenance
Prospective protocol was committed at 905467c19d04c01b4fea3f26592625fbc8229d13 before S90 results. Original 144 source rows Git blob 098e45b9ba81de9bd7dc59c0a3466083b03e6ab4 and original R294 frozen protocol commit 9c78d082902cedffb8ad64159915d8d6f5e12299. Original 72 worlds: 30 hyperbolic, 18 exponential, 24 quasi-hyperbolic. Original reversal counts 8/0/7 were recomputed from the original exact utilities and choices.
## Predeclared counterfactual
An agent knows its own t1 uncommitted choice. At t0 it can pay a commitment fee measured in t0 utility units to force implementation of its t0 preferred option. Perfect anticipation and perfect enforcement are assumed. For each original world, the ex ante commitment gain is the t0 discounted value of its planned choice minus the t0 value of the choice that would otherwise be implemented at t1. On unchanged choices this is zero. On original B to A reversals this equals V_B(t0) minus V_A(t0). Fee grid is exactly 0, 1/4, 1/2, 1; purchase iff gain > fee; equality means no purchase. Net gain equals max(gain minus fee,0).
## Exact results
72 worlds x 4 fee settings = 288 complete artificial source cells. Source: research/validation/R294_S90_ALL_288_COMMITMENT_CELLS.csv. Reproducible JS: research/validation/r294_s90_commitment_cost_20261030.js. Exact summary: research/validation/R294_S90_EXACT_RESULTS.json.
| Family | Worlds | Fee 0 purchases | Fee 1/4 | Fee 1/2 | Fee 1 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Hyperbolic | 30 | 8 | 4 | 0 | 0 |
| Exponential | 18 | 0 | 0 | 0 | 0 |
| Quasi-hyperbolic | 24 | 7 | 6 | 3 | 1 |
| Total | 72 | 15 | 10 | 3 | 1 |
Hyperbolic total net ex ante improvements across its 30 grid worlds are 317/140, 17/30, 0, 0 at the four respective fees. Quasi-hyperbolic totals are 18/5, 51/25, 49/50, 1/25. These are sums of constructed utility units, not dollars or population averages. At fee 1 the sole purchaser is the quasi-hyperbolic world a=3,b=7,beta=1/2,delta=4/5: exact ex ante gain 26/25 and net gain 1/25. The largest hyperbolic ex ante gain is 1/2, and strict tie handling excludes purchases at fee 1/2.
## Audit
The generator independently reconstructed both original date utilities and original choices using exact BigInt rational arithmetic, checked 144 original rows and 15 reversals, then emitted 288 cells. A separate direct-formula B audit read persisted original and S90 sources and checked all 288 rows, 12 aggregate cells and nine injected defects (eight row/grade defects plus one summary defect). Internal nonblind PASS; external team replication NOT_RUN. Original Node CLI from remote checkout NOT_RUN, GitHub Actions NOT_RUN. Scientific acceptance of S90 PARTIAL.
## Boundaries
The hypothetical contract, exact knowledge of future preferences, enforceability, and utility-denominated fee are imposed assumptions. These artificial purchase counts do not estimate human demand for commitment, welfare improvements, discount rates, causal effects, or field intervention performance. No real E2 or historical E3 added. Original R294 E1 formal acceptance unchanged. R073 and PESEN v0.1 frozen. Original239/pending queue unchanged. Next scientific step would require actual human longitudinal choice and contract acceptance data with prespecified independent prediction, if publicly and lawfully accessible.
