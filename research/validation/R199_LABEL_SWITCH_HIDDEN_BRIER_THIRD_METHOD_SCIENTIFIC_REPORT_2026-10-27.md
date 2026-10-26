# R199 HMM third-method: probabilistic hidden-label risk under observationally equivalent label switching

Date: 2026-10-27. Prescore freeze commit `08f1a96574f93f296fa4dc461a310198c0d051c2`. Additive internal E1 synthetic inference; original R199 24-world acceptance unchanged.

## Fixed study

Use the original BASE (a=3/4,r=3/4) and LABEL_SWAPPED (a=3/4,r=1/4) known-parameter binary HMMs. For L=3 and L=4, enumerate every complete observed sequence Y and every artificial hidden sequence X. Compare three prespecified posterior probabilities for hidden Xt after seeing all Y: the correct source's posterior, the opposite-label source's posterior, and the unconditional probability 1/2. Score the actual artificial hidden label Xt with binary Brier loss, averaged over all time positions and the exact true joint distribution P(X,Y).

This measures in-sequence posterior inference about an artificially known hidden state. It is distinct from forecasting a genuinely new independent future observation and must not be represented as heldout E2 evidence.

## Four exact results

| True source | L | Correct hidden Brier | Opposite-label hidden Brier | Neutral 1/2 Brier | Opposite excess |
| --- | ---: | ---: | ---: | ---: | ---: |
| BASE | 3 | 509/2912 (0.174794) | 1385/2912 (0.475618) | 1/4 | 219/728 (0.300824) |
| LABEL_SWAPPED | 3 | 509/2912 | 1385/2912 | 1/4 | 219/728 |
| BASE | 4 | 74348859/430168816 (0.172836) | 207122239/430168816 (0.481491) | 1/4 | 33193345/107542204 (0.308654) |
| LABEL_SWAPPED | 4 | 74348859/430168816 | 207122239/430168816 | 1/4 | 33193345/107542204 |

All 48 observed-sequence likelihood comparisons across the two true sources and lengths are exactly equal, while all 176 paired time-position posterior comparisons are exact complements. The correct hidden posterior has lower expected hidden Brier than the neutral 1/2 baseline. The opposite-label posterior has substantially worse hidden Brier even though the entire observed-data likelihood is unchanged.

For every setting, the opposite-minus-correct Brier risk equals the exact source-weighted time average of `(1-2 P_true(Xt=1|Y))^2`. Thus a latent semantic label can be completely unidentifiable from Y alone while posterior confidence in one named label is high. External anchor information is required before giving that hidden label a real-world meaning.

## Computation and evidence boundary

Main program: `research/validation/r199_label_switch_hidden_brier_third_method_20261027.js`. Complete exact receipt: `research/validation/R199_LABEL_SWITCH_HIDDEN_BRIER_4_EXACT_RECEIPT_2026-10-27.json`. Main calculation uses forward-backward smoothing. B independently enumerates 640 hidden/observed joint atoms, reconstructs posteriors from full path mass and integrates hidden-label squared loss directly. All 40 cross-method row-field comparisons match exactly, 48 observed-likelihood checks and 176 posterior-complement checks pass in each route, and all four wrong-label negative controls detect higher hidden-label risk. Both archived programs were fetched and replayed with identical output rows.

No training-model selection, new human data, or actual hidden social labels were used. This is a post-original-acceptance third-method addendum with a prior committed protocol. Original R199 bounded E1 status, R073 frozen model/scoring and PESEN v0.1 remain unchanged. E2=0, E3=0, external independent team replication=0. No chargeable compute or Actions runs were triggered.

Background original sources: Baum et al. (1970), DOI 10.1214/aoms/1177697196; Viterbi (1967), DOI 10.1109/TIT.1967.1054010; Rabiner (1989), DOI 10.1109/5.18626.
