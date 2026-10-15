# R065 Phase G retrospective aggregation and design-alias audit
Date: 2026-10-16.

This plan is recorded before any new Phase G result. It is a post hoc verification of existing Phase B and D findings, not a prospective hypothesis.

Fixed source: arielevy8/obs-learning-fishing processed CSV Git blob SHA1 `01bf211468abe093618dfa5e5c39e883230c9c03`. Preserve the original full-trial exclusions; 226 eligible participants, eight diagnostic days 4,21,38,55,72,89,106,123, exactly one observed outcome per participant per critical block, four high/four low. Prior Phase B: two alternating stake orders represented by `counterbalance`, with 121 high-first and 105 low-first; do not assume counterbalance randomization.

Tasks, in order:

1. From the exact Git blob, derive a public privacy-preserving 8×2 contingency table: for each block, stake level, eligible person count, and number `copied=1`. Verify 226 observations per block, 904 per stake over all blocks, 684 total copied, and 73 copied in block 6. Verify 121/105 first stake mapping. Do not publish individual records.
2. Independent local Python standard-library proof that each block×stake cell and block-only cell has *at most one observation per subject*. Consequently, the Beta(4,4) LOOCV log-loss and Brier means for the Phase D M2 (block) and M3 (block×stake) models are functions solely of cell totals `(n,k)`: `p_1=(k-1+4)/(n-1+8)` when held-out `y=1`, and `p_0=(k+4)/(n-1+8)` when `y=0`; sum individual case losses weighted by `k` and `n-k` and divide by 1808. Must reproduce archived Phase D M2 and M3 scores within absolute 1e-10. Do not claim this aggregated logic works for M0/M1: those require subject-specific 8/4 outcome counts to exclude ALL of their records from shared cells.
3. Audit formal design aliasing: if each eligible subject has a single alternating high-first or low-first sequence, then at a fixed block position, high vs low is mathematically identical to first-sequence group membership up to a deterministic reversal. Thus an M3 block×stakes score cannot isolate a stake effect from sequence-specific effects. The design may counterbalance some effects in aggregate, but the fixed-block interaction is not independently identifiable from sequence group.
4. Add fail-closed unit tests: known two-label cells, invalid counts, phase A sample totals, M2/M3 regression scores, changed cell counts, aliasing mapping. Run them locally and separately record evidence level. CI job should run these offline, not imply original human-level CSV replay.
5. Keep PESEN v0.1 FROZEN, R065 full gate OPEN, and results labeled retrospectively reconstructed rather than independent trial-level replication.
