# R198 state-space third-method: outcome-dependent last-sensor missingness

Date: 2026-10-27. Scientific scope: additive, bounded, internally reproduced E1 artificial mathematical evidence. The original R198 32-world, 576-history accepted study remains unchanged.

## Precommitted question and source identity

The prescore protocol was committed first as `c9e3c76157caddb34c494782acd6ab6994b4268c`, before the main calculation. It fixes all four original hidden-state persistence values a={1/2,3/4,1/4,11/18}, both sensor reliabilities r={3/4,7/8}, and both T={4,5}. For each of the 16 original parameter settings, compare MCAR and outcome-dependent last-sensor missingness, giving 32 exact comparisons. The first T−1 noisy measurements are always observed. At T, M=1 hides YT. Under MCAR, both YT outcomes are missing with probability 1/2. Under the informative channel, P(M=1|YT=1)=3/4 and P(M=1|YT=0)=1/4. M is visible even when YT is hidden.

The outcome is the genuinely fresh noisy measurement Y[T+1]. Two prespecified forecasts use the same known true a,r. AWARE conditions on the observed M indicator; IGNORE_M discards M only when YT is missing. When YT is present, both correctly use it. Brier losses integrate over the complete true artificial source, with no sample-dependent tuning.

## Main exact findings

All 32 worlds normalize to source mass 1; P(M=1)=1/2 exactly in each, because the unconditional YT marginal is fair. All 16 MCAR settings have precisely zero forecast penalty for ignoring M. Under informative missingness, 12 of 16 settings have strictly positive excess Brier loss for IGNORE_M; the four settings with a=1/2 have exactly zero excess risk because the next hidden state is independently redrawn.

For a=3/4, r=3/4, T=4, the unconditional next-measurement Brier risk of AWARE is `1196848813537503521/4850903569217209504`, compared with `12636424629/51128636416` for IGNORE_M. Excess risk is exactly `3194405158415/7557763971709952`, approximately 0.00042267. The largest excess among the frozen grid is approximately 0.0018378015, for a=3/4 or a=1/4, r=7/8, T=4. Symmetric negative persistence can make the direction of a forecast adjustment reverse while the squared-error improvement remains positive.

In every world the full-source excess Brier equals the missing-case source-weighted squared gap between the two predicted probabilities, exactly. The observation-dependent missingness indicator is itself information about the unobserved sensor reading. A model that silently treats this indicator as ignorable can be miscalibrated even when its latent transition and sensor accuracy parameters are known. This finding is conditional on the fully specified observation channel and artificial Markov process. It makes no general claim about actual missing-data mechanisms in social research.

## Reproducibility and validation

Main archived executable: `research/validation/r198_informative_missingness_third_method_20261027.js`. Main complete rational receipt: `research/validation/R198_INFORMATIVE_MISSINGNESS_32_EXACT_RECEIPT_2026-10-27.json`. The forward algorithm enumerates all ordered prefix histories, updates hidden-state beliefs, incorporates the known missingness likelihood, and integrates future binary Brier loss.

The separate B algorithm enumerates 327680 full latent-path, observed-channel, and future-outcome atom contributions with integer numerators and a common exact denominator. All 352 cross-method field comparisons across the 32 worlds are exactly equal. B separately verifies 32 source normalizations and detects 12 prespecified wrong-channel reversals in the 12 informative dependent worlds. Archived R and B source scripts were read back from GitHub and actually replayed; their generated rows matched both archived receipts exactly. This is internal algorithmic independence, not external team replication.

The original R198 acceptance and original prescore freeze are untouched. E1 synthetic evidence only; new human E2=0, historical E3=0, external replication=0. R073 model and score and PESEN v0.1 remain frozen. No paid service or GitHub Actions was invoked. This third-method addition is a post-original-acceptance analysis, with its own prior protocol commit.

Background: Kalman (1960), DOI 10.1115/1.3662552; Rabiner (1989), DOI 10.1109/5.18626. These are theoretical references, not claimed replications.
