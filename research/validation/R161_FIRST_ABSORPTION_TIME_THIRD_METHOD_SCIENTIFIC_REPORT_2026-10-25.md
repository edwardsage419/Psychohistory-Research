# R161 third-method scientific report: exact expected time to cultural fixation

Date: 2026-10-25. Supplement to existing R161 CLOSED_BOUNDED_E1, original candidate P1/07-003 Conformist Transmission. Precomputed protocol frozen in commit `4761f0e87f97d9975d0d80bb012047cafa383c23`. No changes to the original R161 model, acceptance, R073 or PESEN v0.1.

## Question and source

For the frozen artificial finite population Markov chain, how many generations are expected before the A count first reaches 0 or N? The original R161 report already derived ultimate A fixation probabilities and finite t=0..4 distributions, but did not give the expected first-absorption time. This extension uses the exact original kernel at `research/R161/R161_EXACT_RESULTS.json`, Git blob `0def18bac443d47b7bd77be536536c8c816bed1d`. The original source `research/R161/r161_finite_conformist_markov.py` has Git blob `a2bf01087f9e6f8fb473e3612396c25da93ec2dc`. Its published author-source context and artificial scope are retained.

For N in {5,7}, h in {0,1/4,1/2,1}, and initial A count k, set `q=(1-h)*(k/N)+h*(3*(k/N)^2-2*(k/N)^3)`. All N learners independently choose A with probability q. The absorbing counts 0 and N remain fixed. This is project-authored synthetic E1 mathematics, with no human observations.

## Exact method and actual execution

Rebuilt all eight binomial transition matrices using Node.js BigInt rational arithmetic and checked every entry by exact rational equality against the original immutable R161 JSON. Solved `(I-Q)t=1` with exact rational Gaussian elimination, using t(0)=t(N)=0. Checked the first-step identity and reflection symmetry for all 56 state positions across eight matrices. Recorded exact expectations for all 48 frozen initial states.

| Population N | h | E[T] from k=1 | E[T] from central k=floor(N/2) |
|---|---|---:|---:|
| 5 | 0 | 4.207920792079 | 5.693069306931 |
| 5 | 1/4 | 3.482006081363 | 5.019194702555 |
| 5 | 1/2 | 2.875288479407 | 4.446689316080 |
| 5 | 1 | 1.971118406059 | 3.563994807107 |
| 7 | 0 | 4.968771263653 | 8.410899422730 |
| 7 | 1/4 | 3.648003652270 | 6.923205846277 |
| 7 | 1/2 | 2.714067869449 | 5.811759445167 |
| 7 | 1 | 1.614887389544 | 4.360225713557 |

For N=5 and k=2, the exact neutral expectation is 575/101, while the h=1 expectation is 14209984375/3987094579. For N=7 and k=3, neutral expectation is 30173269/3587401; h=1 expectation is 3203175737287979933634091/734635302784526976199291.

All 30 within-grid comparisons of consecutive h values at transient k show shorter expected time at higher conformity. The central starting state's expected time falls by about 37.40% for N=5 and 48.16% for N=7 when h moves from 0 to 1. This is a bounded eight-kernel finding. No universal monotonicity theorem across arbitrary population sizes or copying rules was established.

The calculation concerns time to **either** absorbing endpoint. A shorter time does not by itself imply higher probability of eventual all-A fixation. Expected time zero for initially absorbing states is enforced. The chain assumes no mutation, migration, selective fitness or intergroup interaction.

## Independent method, controls and limitations

The B audit independently enumerated all 2^N learner configurations, reconstructed transition rows and summed survival probabilities `sum_{t>=0}P(T>t)`. For each kernel, the omitted tail bound `rho^L/(1-rho)` was below 1e-12. Eight kernels and 48 initial states agreed with exact expectations within 1.51e-14 absolute difference in the executed floating-point implementation. All original transition kernels matched to <=3.34e-16. The wrong absorbing-time and omitted-first-term negative controls were detected.

Main source `research/validation/r161_first_absorption_exact.js`; exact receipt `research/validation/R161_FIRST_ABSORPTION_8_KERNEL_48_WORLD_EXACT_RECEIPT_2026-10-25.json`. Independent audit source `research/evidence_audit/r161_b_independent_survival.js`; independent receipt `research/evidence_audit/R161_B_INDEPENDENT_SURVIVAL_8_KERNEL_RECEIPT_2026-10-25.json`. Run with Node.js standard library:
```
node research/validation/r161_first_absorption_exact.js research/R161/R161_EXACT_RESULTS.json
node research/evidence_audit/r161_b_independent_survival.js research/validation/R161_FIRST_ABSORPTION_8_KERNEL_48_WORLD_EXACT_RECEIPT_2026-10-25.json research/R161/R161_EXACT_RESULTS.json
```

The source was syntax-checked after GitHub readback and its computational core executed with original archive content in the connected runtime. New GitHub Actions were deliberately not triggered because account-level zero-charge runner eligibility was not verified. Remote CI for this extension is NOT_RUN.

## Scientific acceptance and next steps

A01 PASS for bounded first-passage question. A02 PASS for fixed original JSON and source blob provenance. A03 PASS for executed exact and independent local algorithms, remote CI OPEN. A04 PASS for negative controls and explicit failure reporting. A05 PASS for E1 scope only; empirical generalization OPEN. A06 PASS for append-only archival subject to final main HEAD and file readback verification. The original R161 CLOSED_BOUNDED_E1 remains unchanged. No new E2 human prediction, E3 historical prediction, or external independent replication. This extension does not discharge the original239 itemwise evidence queue. Continue R162 and subsequent R-series before classification and fusion.
