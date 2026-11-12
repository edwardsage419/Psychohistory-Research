# R133 / original catalogue 05-009: itemwise bounded evidence disposition

Date: 2026-11-13. Closure-audit track. Starting observed recent main commit: `5943286dbf41f41f405d13bdaa98e1e7ddaec9d8`. This is an evidence assessment for the R mainline, not an authorized crosswalk status mutation or new formal scientific closure.

## Fixed evidence identities

* Catalogue entry: 05-009, Evolutionarily Stable Strategy, proposed R133, priority P2. Historical pending-154 queue blob `3b96d46b3d88ccafd779a08509c3cfd0e435772f` still labels it `PROVISIONAL_PRIMARY_README_LINK`.
* R133 final acceptance blob `72e60d3e0fa8f131c6a4864d0d6cc89afbe350fc` [verify identity against latest ref before any formal status change]; fetched final acceptance content states `CLOSED_BOUNDED_FIRSTHAND_1973_STRICT_ESS_625_2X2_AND_THREE_STRATEGY_MIXED_INVADER`.
* Machine CI acceptance receipt blob `b91625e942a583051c21ad442ba45bc073c138ed`. Historical Actions run 39368129476 on `a2c0ee1f5953de0fdce3b4fd0e62afa85a02d5bd`; Python 3.11 and 3.12 each report 36 passing tests.
* Independent mathematical replay: `research/coordination/closure/R133_05-009_INDEPENDENT_625_GAME_AND_MIXED_INVADER_REPLAY_2026-11-13.md` (commit `c051a02d00ede4fb6e261a60cba1c12d927abcff`).
* Historical CI log verification: `research/coordination/closure/R133_05-009_HISTORICAL_CI_LOG_IDENTITY_AUDIT_2026-11-13.md` (blob `9fa1274461c9b82548a8b0d7c5e7b313617f4f2e`).

## Itemwise evidence and limits

1. Original source: Maynard Smith and Price, 1973, *Nature* 246:15–18, DOI 10.1038/246015a0. Final acceptance records direct inspection of printed pp. 16–17, including 25 rounded payoff cells. Full unrounded 1973 stochastic simulation inputs and raw execution are unavailable in this audit. Original five-strategy ESS status remains unknown under printed rounding.
2. Independent exact enumeration: 625 constructed integer 2x2 payoff matrices; pure-A ESS 300, pure-B ESS 300, both 100, interior Nash candidates 200, interior strict mixed ESS 100, no strict ESS 25. A constructed three-strategy counterexample has pure-mutant second-order differences 1, 1, 8 and mixed-mutant difference -1/9. These validate the mathematical test implementation within the specified synthetic domain; they do not reproduce the original stochastic simulation.
3. Executions: historical CI logs substantiate 72 unit-test executions and hash checks at the stated CI head SHA. No new CI was triggered. Original ZIP SHA256 `e5ffa574bcbc0cdd2013cbc5312e5fea2ce4e49263e6abc57e65102f88195007`, source `161aae1cbfc609494798ee5c6921c3a091a93b0dabcef70f24bf038870160e3f`, test `56e7e4801a592ee3bcba35d135bdc25bc5141cb9225a39acab13bcca253c6957` are historical checked values; this closure track has not recomputed them from independently retrieved ZIP bytes.
4. Real-world predictive evaluation: no new animal or human trial, held-out forecast, historical forecast, or independent third-party reproduction is evidenced here. No E2/E3 upgrade. E1 remains bounded mathematical evidence.

## Proposed disposition for R mainline review

**Research-level status: preserve existing `CLOSED_BOUNDED`. Catalogue itemwise review: `ACTIVE` pending explicit owner-side decision on whether bounded original-source coverage satisfies the 05-009 catalogue gate.** The outstanding evidence is precise: original raw simulation reproduction unavailable, independent archive-byte hash recomputation pending, original rounded five-strategy outcome unidentifiable, and no E2/E3. If the catalogue rule permits bounded closure, record that limitation and the exact evidence references; otherwise retain the provisional entry. Do not equate the research-level closure with catalogue closure.

No changes to crosswalk, frozen R073/PESEN v0.1, R core code, or CI configuration. No paid service used.
