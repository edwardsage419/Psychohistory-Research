# B audit: R320 S116 exact absorbing linear system and censoring

UTC date: 2026-10-31. Target: (B,R320,S116_2664cca0,independent_Fraction_Gaussian_and_survival_DP). Read scope: original R320 protocol, original 384-row CSV blob ece51a015bdfeb0a8233f7a24dffe641489e4282, original six-world JSON blob ec0f3702f956e0075444d1d3efafef0bced1d7a2, R320 acceptance, new frozen S116 protocol, new primary result. NONBLIND internal E1.

Precommitted B route: solve a-1 interior-state linear equations for eventual upper probability and expected absorption time using exact Fraction Gaussian elimination; separately propagate interior probability mass for six steps and derive all 36 original time/side cells. No import of R generator and no use of closed-form gambler's ruin formula.

Local Python 3.13.5 execution:
* Primary emit: PASS, six worlds and 384 exogenous paths.
* Primary archived JSON replay: PASS.
* B normal: 11 tests PASS, 0 failures/errors.
* B python -O: 11 tests PASS, 0 failures/errors.
* Ten targeted negative controls rejected: missing world, duplicate world, p mutation, eventual upper mutation, expected-time mutation, finite-survival mutation, residual-upper mutation, E2-label upgrade, first-hit-cell mutation, original-source-blob mutation.
* All six expected eventual probabilities and times, all finite-horizon first-hit cells, six survival masses, twelve residual masses and six conditional upper probabilities agree exactly.

The original source is an artificial enumerated experiment. No empirical leakage test, heldout human predictive score, empirical calibration, bootstrap uncertainty, external blind replication or historical E3 validation was performed. The complete source universe is checked as six worlds, and original CSV Git blob identity and 384 data-row count were independently read through GitHub; the B script itself uses the pinned original JSON blob identity and exact first-hit cell oracle. A future stricter gate could ingest the original CSV directly, verify every row's probability and compare it to a reconstructed path universe.

Scientific interpretation remains PARTIAL_E1_EXTENSION. Original R320 acceptance unchanged. CI NOT_RUN for S116; no Actions dispatched because free billing status was not verified. No new paid services.
