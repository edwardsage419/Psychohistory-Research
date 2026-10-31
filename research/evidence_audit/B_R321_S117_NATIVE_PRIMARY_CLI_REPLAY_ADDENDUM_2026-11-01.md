# R321 S117 native primary Python replay addendum
Date: 2026-11-01 UTC. Status: COMPLETE for the scoped archived-primary-CLI replay gate. This addendum supersedes only the NOT_RUN primary CLI entry in the earlier S117 R/B reports and first R handoff; other evidence boundaries remain unchanged.

## Exact inputs and bytes
Original R321 source CSV was locally reconstructed using the frozen original generator's complete 7-bit enumeration, Bernoulli Fraction weights, first-stop rules and CSV field order. The locally regenerated CSV has 1024 data rows, 49521 bytes and Git blob d5e5e183a786e199fbf792589ed68735f30ca1b3, **identical to the remote original R321 CSV blob** independently fetched earlier. This is a deterministic local reconstruction, not a new empirical dataset.
The exact archived R primary Python source research/validation/r321_s117_terminal_policy.py was reproduced locally and its Git blob was verified as 31d0fba7c8a7ff27f7c2b7b6f14faa5a5aeb7ab1, identical to the remote file.
The exact archived R result research/validation/R321_S117_TERMINAL_FORCED_CHOICE_EXACT_RESULTS.json has Git blob f0d57719e37697090dcbc6af2ad42d7b08ced79d.

## Actual local commands and results
Python 3.13.5:
python /mnt/data/r321_s117_terminal_policy.py --source-csv /mnt/data/R321_ALL_1024_ORIGINAL_SEVEN_BIT_PATHS.csv --output /mnt/data/R321_S117_TERMINAL_FORCED_CHOICE_EXACT_RESULTS.json
Result: exit 0; all 8 worlds and 1024 original source rows verified. Emitted JSON Git blob f0d57719e37697090dcbc6af2ad42d7b08ced79d, **byte-identical to the persisted GitHub result**. Emitted SHA256 c948fcdb3d7fb00c6bda339cb431f65c591ebc50bd7230353a4e0c676fa940ee.
python -O /mnt/data/r321_s117_terminal_policy.py --source-csv /mnt/data/R321_ALL_1024_ORIGINAL_SEVEN_BIT_PATHS.csv --output /mnt/data/R321_S117_OPTIMIZED.json
Result: exit 0, output byte-identical to normal Python mode.
Five native CLI negative controls executed in isolated temporary directories, each nonzero exit 1: missing source row, duplicated source row, changed path probability, changed first-hit decision, changed censor flag. This complements the earlier 9/9 V8 source-mutation controls.

## Scientific and operational boundary
The archived R primary native CLI replay gate is now PASS, original 1024 source identities and persisted receipt exact byte equality verified. The B independent Fraction script remains a separate nonblind internal route. This does not constitute external blind replication, real human E2, historical E3, Wald infinite-horizon optimality, calibrated real behavior, or full-family acceptance. S117 remains PARTIAL_E1_EXTENSION; original R321 acceptance unchanged. No GitHub Actions triggered; billing and free quota were not independently inspected. No existing report, frozen protocol, original CSV or source was modified.
