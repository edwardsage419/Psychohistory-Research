# B audit: R164 independent exact oracle and mutation execution

Date 2026-10-25, Asia/Singapore. Scope E1 synthetic internal verification of frozen R164 observational partition extension. Original 72-world JSON SHA256 ce27a70aee6ee82ca360efc93b12632c44f6bbd7a73b32bf1aaafc602df69f52, Git blob 087686b629cba4d0b94492d360893a47e334ecb2. Frozen extension protocol commit 95bf2e51fef98ba96c9f3b88176e5b4a4fa550ac.

## Independent executed calculation

The main partition calculation used exact rational prefix grouping of the original 72 frozen worlds. The separate executed JavaScript BigInt oracle reconstructed each next state through independent random-copy, salience-weighted-copy and symmetric-replacement channels. Its rational numbers were reduced by integer gcd, and every frozen state was checked by numerator/denominator identity.

Observed actual execution:
* Original Git blob 087686b629cba4d0b94492d360893a47e334ecb2.
* Partition receipt Git blob 1fd7ebff9d4fe11b5c29274b81d3ac580b677e73.
* 72 distinct worlds, 360 exact state comparisons: all equal.
* Six pooled regime membership signatures and twelve per-initial-frequency membership signatures: 18/18 equal.
* Mutation replacing r with 1, executed on applicable worlds: 32 first-step differences detected.
* Mutation omitting e, executed on applicable worlds: 35 first-step differences detected.

Both mutation computations actually evaluated altered transition formulas and compared their outputs to original frozen next states. These are error-detection controls, not measured causal effects.

A second Python Fraction implementation is archived at research/evidence_audit/r164_b_independent_observational_oracle.py. It does not import the main Python module. The Python file was committed but not directly run against checked-out GitHub files or in remote CI during this round. Future replay must execute it after materializing the repository and compare all receipt signatures. The executed BigInt oracle is internal programmatic independence, not independent authorship or external laboratory replication.

## Scientific scope and untested questions

R164 source is artificial binary content frequency with 72 selected parameter worlds. No human participant data, no baseline predictive comparison, no out-of-sample split, no probability calibration, no bootstrap or independent human sessions were available or appropriate for this exact identity audit. Therefore E2=0, E3=0, external independent replication=0. The finite-grid ambiguity count is not a claim about identifiable human psychological mechanisms. The original frozen model and score rules remain unchanged.

B result: PASS_BOUNDED_INTERNAL_BIGINT_EXACT_REPLAY; Python remote replay NOT_RUN; no new GitHub Actions triggered. No paid compute.
