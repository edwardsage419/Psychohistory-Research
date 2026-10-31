# R324 S120 scientific report: ordinal coarsening of constructed risk scores

Date: 2026-11-01 UTC. Track r. Status: PARTIAL_E1_EXTENSION. Original239 01-017.
Prescore freeze commit: dc2bc2ad22a0130984cf0ecb497c2c54f04803f8.
Original R324 source CSV Git blob: 1b0062eeea020606a3d510d566da43db03ace8d9.
New R code: research/validation/r324_s120_ordinal_observation.js.
Persisted 64 atom CSV blob: eeef39b66165e2ec0a918ccedb4f038b078cd05b.
Persisted JSON blob: a95be44193a4a7890203049d5615b4f27c93453e.

## Question and frozen universe
Given exactly the four previously frozen R324 scoring worlds (3,1), (1,3), (1,1), (2,2) and 16 equiprobable artificial binary hazard states per world, how much latent scoring-world information survives different measurements? All 64 atoms have prior probability 1/64. No fitting or stochastic sampling. The original 1978 psychometric factor loadings are not claimed.

## Exact results
For P0 to P5 the observer knows the sampled hazard state, and observes only the named additional measurement. Equal prior over four worlds. Bayes-optimal world classification uses the sum of the maximal world mass in each observation cell.

| Frozen observation | Distinct observation cells | Exact optimal accuracy |
| --- | ---: | ---: |
| P0 state only | 16 | 1/4 = 25.0000% |
| P1 state plus exact score | 45 | 45/64 = 70.3125% |
| P2 state plus fixed threshold score >= 4 | 26 | 13/32 = 40.6250% |
| P3 state plus ordinal comparison to 1100 | 30 | 15/32 = 46.8750% |
| P4 state plus ordinal comparison to 0011 | 30 | 15/32 = 46.8750% |
| P5 state plus both ordinal comparisons | 36 | 9/16 = 56.2500% |

P6 is a different and substantially richer measurement: observe the complete weak ordering across all 16 hazards for one world. Three distinct world profiles exist, yielding 3/4 = 75% optimal classification under equal priors. W2 and W3 have identical rankings for all pairs; their exact cardinal scores differ on 15 of the 16 hazards. A complete ordinal profile therefore cannot distinguish a positive rescaling of the scoring function. The P6 75% result must not be compared as if it had the same observation cost as a single P1 to P5 response.

The full-score policy P1 has a higher one-hazard accuracy than either single reference comparison. Thresholding discards cardinal information. These results are mathematical properties of the frozen four artificial scoring worlds and the chosen prior, threshold and references. They do not estimate population risk perception.

## Validation and negative evidence
The original 64 row source was read from GitHub and reconstructed exactly against its fixed blob. R V8 execution regenerated all 64 new atoms and the seven policy summaries. Independent B used 3x3 D/U multiplicity counts (1,2,1 per axis), verified the actual persisted source, CSV and JSON, and rejected nine deliberate mutations. A separate local Python Fraction oracle reproduced all six accuracies and the full ordinal profile result. The B audit initially failed from an incorrect intermediate group aggregation; the auditor was corrected, and the failure is retained in the B report. A subsequent V8-only structuredClone compatibility error was corrected before final B verification. No frozen R protocol or source was modified.

Archived Node command line execution on the newly committed files: NOT_RUN. GitHub Actions: NOT_DISPATCHED, billing balance NOT_VERIFIED. External blind independent reproduction: NOT_RUN.

## A01 to A06
A01 PASS for narrow constructed finite question. A02 PASS for original Git blob and frozen protocol, human data unavailable. A03 PASS for V8 in-memory replay and B remote-row oracle; native Node CLI remains OPEN. A04 PASS for recorded negative controls and development failures. A05 PASS for E1 scope only, E2 and E3 NOT_ESTABLISHED. A06 PASS for source, scripts, receipt, scientific report and GitHub archival once final commit is verified. Scientific status remains PARTIAL_E1_EXTENSION and is not a new full R324 acceptance.

## Research boundaries and next
No original Fischhoff et al. 1978 participant data, no factor analysis, no human out-of-sample validation, no calibration, no real longitudinal or historical test. R073 model and scoring rule and PESEN v0.1 stay frozen. Next R model is R325, subject to fresh HEAD and coordination review. Classification and fusion remain deferred.
