# R312 S108 prospective two-step random-dyad dispersion protocol

UTC date 2026-10-31. Baseline main 67091242a6f31a28a0fffdcce70d5f5d86ec7aca. Status PRESCORE_FREEZE; calculations and results must follow this commit. This is a bounded E1 extension, not an amendment to original R312 acceptance.

## Source and frozen universe
Use the eight ordered artificial four-person profiles A to H, three inclusive confidence radii {0,1/2,1}, two symmetric compromise strengths {1/4,1/2}, and six equiprobable unordered dyads exactly as frozen in protocols/R312_DEFFUANT_RANDOM_DYAD_ONE_STEP_1152_PERSON_SOURCES_PRESCORE_FREEZE_2026-10-23.md (blob 77ec37a7f2fef4567f9c73f4593c7b7b09146f20). Original R312 CSV blob 498eefccf66d71ebf28323be7caa97309b06e8f6 and source script blob a4e4873b65d6b155fc69abb76c0eb1382e8a4dc6 remain unchanged. Original paper Deffuant et al. (2000), DOI 10.1142/S0219525900000078.

Each artificial step samples one dyad uniformly, independently with replacement. Exactly 48 worlds, 36 ordered two-step paths per world, 1728 full paths; each path probability 1/36. Ineligible encounters leave all opinions unchanged. Both members update simultaneously using the pre-event opinions. No external social network, no real human contact process.

## Prespecified estimands and comparisons
For opinion vector x of length four, define D(x)=sum_i (x_i - mean(x))^2. For each world compute D0, E[D1], E[D2] exactly, and reductions D0-E[D1], E[D1]-E[D2]. Primary check: D0 >= E[D1] >= E[D2] for all 48 worlds. Summarize strict reductions at each step, zero reductions, maximum and mean reductions over the 48 equally weighted artificial worlds. Report at least one strict example if it exists, and an explicit zero-change negative control at epsilon=0.

Secondary checks: number of distinct terminal opinion vectors across 36 paths in each world; number of 15 unordered pairs of distinct dyad labels whose two opposite orders yield different terminal vectors (48*15=720 order contrasts). Report exact counts, and one concrete opposite-order example. Full path-level 1728 rows must retain profile, epsilon, mu, first pair, second pair, exact final opinions and D0,D1,D2; no rounding in primary results.

## Independent audit and stop rule
Generator uses integer 1/32 opinion units and rational arithmetic; independent auditor must use Python Fraction midpoint and half-gap expression without importing generator, reconstruct 1728 paths, check 48*36 uniqueness, probabilities, sum conservation, D monotonicity, expected values, source identity and deliberate negative controls. Run in ordinary and python -O modes with explicit exceptions; record actual successes and failures. Original 288 one-step event identities should be compared against original archived R312 data if accessible. Check source and output SHA/Git blobs. Preserve any failed attempts.

No claim of real-person E2, independent external team reproduction, historical E3, long-run consensus or causal identification. R073 model/scoring and PESEN v0.1 remain FROZEN. Scientific status for S108 is PARTIAL_E1_EXTENSION pending audit; do not alter R312_FINAL_ACCEPTANCE_STATUS. No paid compute, API, data or GitHub Actions. If any expected identity or check fails, report FAIL/OPEN and do not declare acceptance.
