# R322 S118 prospective complementary protocol: output versus process-label observation

UTC date: 2026-10-31. Baseline main: 5437a44e9b03ecdd4aed43b2b9d5f7eba94af917. Track R, original239 01-012. Scope: artificial E1 only, nonblind to R322 v1 original 256 rows and original report. This freezes NEW observation/noise calculations before their execution. Existing R322 acceptance, R073 and PESEN v0.1 remain untouched.

## Fixed input and model identity

Use exactly the original four 64-state binary policy worlds from research/R322/R322_ALL_256_ORIGINAL_BINARY_STATES.csv (Git blob 0cd38ecc22adc5941832c2b00e6928d48be8d896). Compare gated_intervention and lookup_equivalent under identical uniformly distributed six-bit state (h,a,y,d,r,w). They are observationally equivalent on output but have different latent intervention labels. No new fitted parameters, subjects, empirical outcomes, or original source modification.

## Frozen observations, sampling, scores

For each policy, derive exact probability mass of observation (h,a,d,r,w,output) (behavior_full), (h,a,output) (behavior_partial), (output) (behavior_only), (output, observed_intervention) (label_only), and (h,a,d,r,w,output,observed_intervention) (label_full). y is never observed. Intervention indicator is either noiseless or independently flipped with known symmetric probability eps in {0,1/4,1/2}. Noise is artificial, independent of all states and policy; marginalize with exact rational arithmetic. All 64 exogenous states have probability 1/64 per policy. Compute total variation TV=1/2 sum absolute mass differences and equal-prior Bayes accuracy=(1+TV)/2 for each observation and eps. Include conditional strata r=0, r=1, and d=r=w=1 with normalized conditional state weights, compare behavior_full and label_full. Fixed negative controls: behavior-only and all behavior observations have TV=0 for the two candidate policies; label_full with eps=1/2 has TV=0; r=0 label_full has TV=0. Positive witness h!=a,d=r=w=1 has differing intervention label.

## Validation and boundaries

R route: standard-library exact Fraction aggregation of original 256 rows, strict source universe checks, explicit coverage and mass conservation, frozen score outputs. B route: independent no-import algebraic enumeration of binary states and an independently written observation-mass aggregator; compare exact fractions across all specified observation/noise/stratum cells. At least six deliberate mutation controls covering missing state, duplicated state, corrupted intervention, output, weight, and evidence-grade promotion. Preserve failing tests. No calibration or empirical holdout claims, no human E2 or historical E3, no external-team independence. If any original blob mismatch, stop rather than substituting regenerated rows. No GitHub Actions without verified free billing.
