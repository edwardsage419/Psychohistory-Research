# R129 independent Python Fraction recomputation receipt

Date: 2026-10-24. Scope: project-internal E1. This note is additional to the earlier frozen protocol and JavaScript-generated R129 artifacts. No original R129 code or raw published table was edited.

After the archived CSV files were committed, a separate local Python implementation using `fractions.Fraction`, `itertools.product`, and `csv.writer` independently regenerated all 49 asymmetric p,q coupling worlds and all 25 original Table 1 rounding-interval records. The Python implementation directly enumerated both 12-atom couplings, checked their exact marginals, their collision bounds and the four-outcome welfare sum. It independently checked possible versus robust-strict best replies across all five printed columns. The Python output was compared to the archived Git blob identities by independently calculating the exact Git blob SHA1 of the generated UTF-8 CSV bytes.

Observed results:

| Artifact | Bytes | Independent SHA256 | Independent Git blob SHA1 |
|---|---:|---|---|
| R129_ASYMMETRIC_COLLISION_49_CASES_2026-10-24.csv | 1621 | `11539e2e90fd5a766446e45bc7fa71e2af170653d9d0180d660852a3651824c8` | `823142cf268a1f7225f5e99b1b26763c40981ff3` |
| R129_ROUNDED_TABLE_25_INTERVAL_CHECKS_2026-10-24.csv | 1342 | `2c40cc24b6160deda7a165c6f273be48811f1baf5c6dc5d02343c582e5b4e7b7` | `2a3bf574645469503accff9f6444d672e8d7e3c4` |

Both independently calculated Git blob identities exactly match the archived GitHub blobs. Two intentionally altered integer comparisons, `2 != 1` for collision count and `5 != 4` for marginal count, were separately executed and both rejected with `AssertionError`. These are synthetic tamper tests, not observational negative cases.

Evidence grade: **PASS_BOUNDED_INTERNAL_TWO_IMPLEMENTATION_E1** for the frozen 49 coupling worlds and 25 rounded payoff cells. The archived `verify_r129_asymmetric_collision_and_rounding.py` has not yet been executed in a full repository checkout, and no new GitHub Actions run exists for this extension. The original 1973 stochastic simulation is not rerun. New human E2=0; historical E3=0; external research-team replication absent. No original239 index or queue change. R073 and PESEN v0.1 remain frozen.
