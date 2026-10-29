# B R273 S69: independent grouped binomial and persisted receipt audit

Date 2026-10-30 Asia/Singapore. Audit type: internal, nonblind, methodologically separate algorithm. Prior original R273 risk results and new R S69 output were visible to the same operator; external independent or blind replication is NOT_RUN.

## Frozen gates and data inspected

S69 protocol commit 9051d6e27c1ef17ceff3b49883cbb274d7510871 precedes the S69 score calculation. Original R273 source and acceptance were read, but the original 1728-source CSV was not downloaded or byte compared this round. B inspected the actual persisted S69 JSON Git blob 78eeeaaceb082befd99284e4335519e857eb0d6c and actual S69 CSV Git blob 9d0488797e3ac362b011a0b3a9868c5ccd914dbb.

Independent B calculation uses K=0..4 with binomial multiplicities C(4,K) and J=0..2 with C(2,J), a total of 15 grouped cells per world. R directly enumerated ordered six-bit sequences. The B oracle does not import R source enumeration or stored result constants. Both routes use the frozen generator and model formulas; this is mathematical independence of implementation, not independence of investigator.

## Actual execution

* Nine worlds, 135 grouped cells, each exact probability mass 4096/4096.
* 158 persisted JSON fields compared against B grouped calculations and strict fixed metadata. Zero mismatches.
* 576 persisted CSV rows read back, all distinct by (world,sixbits), nine per-world exact masses 4096/4096, recomputed source weights, source/Laplace forecasts, two target score numerators and ranking labels. Zero mismatches.
* Eight mutated receipts rejected: duplicate world, missing world, altered probability, forged real-human E2, boolean substituted for integer source count, changed wrong-rank count, changed freeze identity, altered tie count.
* All arithmetic comparisons exact integer and reduced fraction; no floating tolerance.
* Original R source risk formula matches independent analytic expression in nine worlds.
* Runtime: V8 execution. Archived native Node CLI NOT_RUN; GitHub Actions NOT_RUN; external independent replication NOT_RUN.

## Scientific checks and open gates

Training uses four source bits; two independent target bits enter only final scoring. Paired comparison uses the same two target bits for both predictors, correctly retaining correlation of scores. SOURCE_ORACLE uses true source a and TARGET_ORACLE uses true target b, so both are truth-informed mathematical comparators. The finite paired sample ranking is a noisy model selection diagnostic; it does not guarantee improvement in future target cohorts. Calibration curves, clustered real-human uncertainty, and external replication are NOT_RUN.

A01 PASS bounded scope; A02 PASS for fixed source and result identities read; A03 PARTIAL pending native CLI and byte-level original CSV identity; A04 PASS for 8 rejected mutations; A05 PASS for E1 and nonblind limitations; A06 OPEN broader acceptance. Existing R273 CLOSED_BOUNDED remains unchanged.

No raw human data were used, no paid services invoked, R073 and PESEN v0.1 frozen.
