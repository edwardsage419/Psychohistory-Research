# B track: R292 S88 independent grouped conditional probability audit

Date: 2026-10-30 UTC. Target key (B,R292,S88-v1,nonblind conditional aggregation and mutation gates). Evidence E1 only.

## Scope and method

Read original R292 frozen model, original exact result JSON, new R292 S88 prescore protocol, the full 1536-row GitHub-persisted CSV and the full 24-world JSON. Independent auditor file: `research/evidence_audit/b_r292_s88_independent_grouped_conditional_oracle_20261030.js`. Mutation suite: `research/evidence_audit/test_b_r292_s88_mutations_20261030.js`.

The independent audit imports neither R292 original program nor new S88 generator. It parses all 1536 labelled rows, reconstructs the factorized joint source probability from A,N,C,I,F,Z, enforces 64 distinct source keys per world and total mass one, checks B=I*F and all source conditional probability fields. It groups weighted outcomes into four distinct observed information sets (A,N,C), (A,N,Z), (A,N) and the constant group. Bayes Brier risks are independently computed from conditional variance `sum_group [mass_B - mass_B^2/mass_group]/2048`. This is a distinct grouped-probability calculation from R's per-row squared residual sum. All 24 four-predictor risks agree with the persisted JSON; 6144 conditional forecast cell comparisons agree. Eight e=0 worlds reproduce the archived original R292 full and AN risks.

## Observed adversarial tests

Eight distinct malformed inputs were actually injected into the V8-executed independent checker. All eight were rejected:
* duplicate source row: duplicate source
* deleted source row: row count
* changed joint probability: source factor
* changed behavior: behavior gate
* changed conditional forecast: forecast conditional mismatch
* changed epsilon without updating world identity: world label
* changed summary risk gain: gain mismatch
* changed evidence label to E2: summary metadata

The original unmodified persisted inputs passed. Native Node CLI of the archived audit and R source NOT_RUN. The above are V8 runtime executions of the archived audit function and mutation suite, not external-team replication. No GitHub Actions launched. No independent human or historical predictive evidence, no probabilistic calibration on real persons, no causal identification. Original R292 bounded E1 closure unchanged, S88 scientific status PARTIAL, R073/PESEN frozen.

## Open audit gates

Run the exact archived R and B Node CLI from independently retrieved raw GitHub files, compare emitted bytes and independent SHA256, run the persisted mutation script, check zero-probability source handling in native Node, and seek truly external independent reproduction. Do not upgrade evidence on the basis of internal script execution.
