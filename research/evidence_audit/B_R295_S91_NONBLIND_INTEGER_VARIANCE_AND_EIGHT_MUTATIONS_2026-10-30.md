# B R295 S91 independent nonblind mathematical and source audit

UTC 2026-10-30. B objective: independent conditional-variance check of the persisted R295 S91 E1 source atoms. Original R295 acceptance unchanged. Test design fixed in R295 S91 protocol at commit 4b67e0dd172f6633a37c4ba65f12e7b5269856b2.

## Read scope and methods

Reviewed original R295 source/README, original freeze, S91 freeze and persisted S91 CSV and JSON. This is an informed internal replication, not blinded and not an external independent team. R route uses original 180-row source actions and complete atom enumeration. B route uses its own integer-scale recurrence for habit strength H16 and action score32, then independently computes conditional Bernoulli probabilities and Brier risks directly from the 1080 persisted CSV rows. It does not import or invoke the primary generator.

Persisted B input Git blobs:
* R295 S91 CSV c724d9216b1faa060b01eacfc8025d031785af24
* R295 S91 JSON d0151a996639c65669575b9be98870c9c6d60a68
* B audit script 53672afe45942a318cbf506c3311f8b56cde8760

## Observed results

The B script was fetched from GitHub and executed in the JavaScript V8 tool runtime against the fetched persisted CSV and JSON. Positive audit PASS: 1080 distinct complete atoms, 270 settings, 180 explicit zero-mass atoms, 22 cue-sensitive settings at each error rate, complete probability and prediction fields, weighted squared losses, 270 result cells, three error summaries and nine lambda/error summaries. All checked values agree with the independent integer habit-strength and conditional Bernoulli variance calculation. A separate Python Fraction enumeration (3 learning rates x 3 controller shares x 2 valuations x 5 stages) confirms sensitive counts lambda0=0, lambda1/2=8, lambda1=14, and sensitive-world Brier (baseline, noisy) of (1/4,0), (1/4,3/16), (1/4,1/4) for e=0,1/4,1/2.

Eight actual mutation controls were executed and all rejected: duplicate source, missing source, altered source probability, altered action, altered conditional predictor, altered weighted loss, altered aggregate sensitive count and inflated E2 evidence label. The native Node CLI on a checkout was NOT_RUN because source download into the shell environment failed DNS resolution; this is a procedural execution gap, not a passed test.

## Scientific audit scope

Data leakage: the entire source is a fixed artificial generative universe with no fitting; predictions use known true probabilities, so no trained estimator can be evaluated here. Baselines: fixed no-cue Bayes predictor and true-cue oracle. Heldout: expectations concern an independent future synthetic draw under the same known mechanism; no observed out-of-sample human outcomes. Calibration: theoretical conditional probabilities are correct by construction, not empirically calibrated. Independent samples and uncertainty: exhaustive finite probability calculation, no sampling confidence interval applicable; external validity unknown. Negative controls: 68 cue-insensitive worlds have zero gain. Original R295 tie-to-B rule retained. No post hoc tuning, R073/PESEN v0.1 unchanged. New E2=0, E3=0.

Status: INTERNAL_NONBLIND_EXACT_MATH_AND_MUTATION_PASS; NATIVE_NODE_CLI_NOT_RUN; EXTERNAL_INDEPENDENT_REPLICATION_NOT_RUN; S91_SCIENTIFIC_ACCEPTANCE_PARTIAL. No CI or paid computation was initiated.
