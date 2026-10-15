# R064 Pre-Data Protocol — Independent Levy et al. (2025) Observational Learning

Frozen locally **before** reading outcomes of `data/processed/unified_data_2025-01-16_00.csv`.

Primary dataset: `arielevy8/obs-learning-fishing`, tree SHA1 `fd5f435b5368b69916e7acc6a9991aa5f46b3ddb`, processed file Git blob SHA1 `01bf211468abe093618dfa5e5c39e883230c9c03`. Levy, Roberts-Gaal, Cushman (CogSci 2025). New *independent research team and experimental task* relative to Najar et al. R061-R063; NOT a prospective test because published direction is already known.

Precommitted question: Does stake level predict an individual copying the demonstrator's action in a two-step observational learning task? Not a test of Najar metaVS or PESEN.

**Eligibility**: The processed file `unified_data_2025-01-16_00.csv` is an author-computed unit-level dataset. Accept only records with nonmissing `participant_id`, `stakes`, `copied`, `accurate` and `comprehension_check_repetitions`. Apply author-reported exclusion criteria using participant averages: accuracy < 0.45 OR mean comprehension-check repetitions > 2. Require copying to be binary and stakes to have exactly two distinguishable values; otherwise stop the planned comparison and return schema audit only. Require at least 10 eligible participants with both stake conditions. No imputed outcomes. Record how exclusions affect N.

**Primary estimand**: Per-participant (mean copied under high stakes) - (mean copied under low stakes); then average these differences with equal weight per participant. High/low label must be established by column's semantically grounded values; do not guess which numeric code means high. Report participant-level paired bootstrap 95% percentile interval with seeded RNG, 20,000 draws. A CI covering zero fails to establish a reliable direction. No causal P-value unless assignment provenance is demonstrated. Also report simple pooled contrast, but not as primary.

**Predictive comparison**: Leave one whole participant out. M0 predicts copying by globally pooled training-participant rate smoothed with Beta(4,4). M1 predicts by training-participant separate stake-level rates each with Beta(4,4). No information from held-out participant may determine parameters. Compare log loss and Brier on the same held-out rows, average per participant (macro), report subject-level winning fraction and participant bootstrap of model loss differences (20k resamples). Models do not use full future outcome history. No hyperparameter tuning on test data. If a required field is missing, report non-evaluable without inventing fields.

**Sensitivity**: Retain all valid participants before exclusion and report primary stake contrast changes; list missing and exclusion counts; inspect stake balance and per-participant within-stakes trial counts.

**Non-goals and attribution**: Does not identify imitation vs emulation, social-reward psychological parameter, long-range historical dynamics, or R063 metaVS. Published paper's directional claims are known so this is strictly retrospective independent-author evaluation.

PESEN v0.1 stays FROZEN. If author processed CSV inaccessible, produce an access/availability audit and no empirical estimate. Do not retroactively relax primary endpoint after seeing outcomes.