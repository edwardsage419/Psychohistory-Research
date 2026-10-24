# R122 independent asynchronous reachability scientific report

Date: 2026-10-24. Catalogue: original239 04-005. Study: Centola and Macy (2007), *Complex Contagions and the Weakness of Long Ties*, DOI 10.1086/521848, https://www.journals.uchicago.edu/doi/10.1086/521848 .

## Frozen contract and provenance

The third-method protocol was frozen before this executable at `research/validation/R122_THIRD_METHOD_ASYNC_BITMASK_PROTOCOL_FREEZE_2026-10-24.md` (blob `a0e341e963afb1309a021f2756d919bf9ebc645e`). Reuse of R122's original 2007 source review, first two mathematical solvers, 51 tests and existing bounded acceptance was mandatory. Original first failure run 39258433825 and corrected run 39258676907 remain historical records. No changes to the R122 original code, R073 or PESEN v0.1.

The original source, test and report Git blob SHA1 values independently checked by the new script were `bde1c39fc9b536aaa794209ceaf76c90407d0f16`, `6058f0f4ddb5f0fdcaf643e969374507f6a70063`, `7301d5a7b026feaa16ce7ac8e942d60a7ad1af63`.

## Executed audit

A new bitmask breadth-first search enumerates all reachable **single-node asynchronous** activation sequences. Each node's integer threshold is either 1 or 2, except n=1 where only 1 is legal. Distinct active neighbors are counted using bitwise set intersection. Every reachable terminal state must agree, and the terminal mask must exactly match both pre-existing R122 algorithms. The BFS does not call either original solver.

Complete finite test universe: all undirected labeled graphs with n=1..4, every per-node legal threshold vector, and all seed subsets. Per-n cases: 2, 32, 512, 16384. Total **16930** constructed worlds and **16930** archived CSV rows. CSV SHA256: `8b86493df9e51e46b95d08bc608f294441bdc9e84dee7b953c8cc5e4caeb8013`. CSV Git blob SHA1: `b219fc1da3db01fcd6d74c4006b637db755acd4c`. Source script Git blob SHA1: `d016296b5576e23f3edcc3e779965e2528133899`.

Negative controls: a repeated exposure from the same single source cannot satisfy threshold 2; narrow and dispersed cross-community bridges cannot activate the second triangle under threshold 2; three properly reinforced cross-community edges can. Wrong source blob identity and a modified CSV are rejected.

## Actual CI verification

GitHub Actions workflow `.github/workflows/r122-independent-async-bitmask-audit.yml` run **40087355161**, https://github.com/edwardsage419/Psychohistory-Research/actions/runs/40087355161 , commit `ed2a75a429e92a1d17cf78133b5ea30adff8f0d1`, completed with conclusion **success**. Python 3.11 job 120852896455 and Python 3.12 job 120852896288 both completed successfully. Both logs explicitly printed `R122_AUDIT_PASS cases=16930 negative_controls=4 source_blobs=3 csv_sha256=8b86493df9e51e46b95d08bc608f294441bdc9e84dee7b953c8cc5e4caeb8013 verify=True` and `Ran 51 tests ... OK`. The 51 original tests were re-executed on each Python version.

Local supplementary check before commit: an independently written synchronous bitmask update reproduced all 16930 terminal masks and the identical CSV SHA256. This was an internal test, not external replication.

## Scientific interpretation and exclusions

Result: **PASS_BOUNDED_INTERNAL_ASYNC_REACHABILITY_E1**. The claim is exact confluence and agreement of three finite deterministic mathematical algorithms within the frozen universe. The extra asynchronous search checks scheduling invariance in this irreversible count-threshold model. This property is a consequence of monotone dynamics; the 16930 worlds are constructed mathematical cases, not independent real-world observations.

No human E2 score, historical E3 validation, empirical network bridge-width identification, real causal mechanism identification, large stochastic lattice reimplementation, probability calibration, held-out human prediction or external-team independent replication was performed. Those gates are `NOT_RUN` or `OUT_OF_SCOPE`. R073 and PESEN v0.1 remain frozen.

Free public repository standard Ubuntu runner, no GPU or paid API, no data purchase and no new resource expenditure. Scope-limited original239 reattribution is justified after this report and a separate formal acceptance receipt.
