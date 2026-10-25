# R168 effective opportunity identifiability: analysis freeze

Date: 2026-10-26. Parent HEAD at prewrite check: 3d99b2e06dcf4ffc192c37523170e4ef054bd8ff. Scope: additive E1 audit of already frozen R168 three-level cultural frontier; preserve original 64-world protocol, original source, results, R073 and PESEN v0.1.

## Provenance and exploratory disclosure
The existing 2026-10-21 R168 report already proved that single-channel access erases nominal population size and gave one pair of observationally equivalent worlds. Before this audit freeze, an exploratory read of all 32 existing kernels grouped them into 16 distinct kernels, with 23 of 32 parameter rows in non-singleton groups. These counts are **exploratory**, not independently preregistered discoveries. The following algebraic identity, counterfactual and negative-control procedures are frozen before writing and running the new confirmation program.

## Frozen target and analysis
For m=N under full_pool and m=1 under single_channel, let A=(1-u)^m and B=(1-f)^m. Derive the entire ordered 3x3 transition kernel in terms of A and B alone:
row0=(A,1-A,0);
row1=(A B,A(1-B),1-A);
row2=(0,B,1-B).
Check every entry of all 32 frozen original kernels using exact rational arithmetic and verify that grouping by (A,B) is identical to grouping by the full matrix. Count unique classes, ambiguous rows, singleton classes and class sizes. Check all 64 original world paths as a consequence of the same kernels, with no change to the source file.

## Prespecified independent scientific tests
1. Two counterfactuals: u=0, f=1/2, m=2 versus u=0, f=3/4, m=1 yield the same kernel; positive u=1/8 and f=1/2 at m=1 versus m=2 have distinct A and distinct kernels. The full-kernel equivalence is stronger than matching only one retention statistic.
2. Independent audit route shall infer A from K[0,0] and B from K[2,1] and reconstruct all other entries, rather than reading (u,f,m). Recalculate matrix classes and check full 64-path signatures grouped by the same parameter combinations.
3. Executed negative controls shall mutate K[1,0] by a nonzero rational amount and separately mutate K[2,1], and the reconstruction/parameter tests must detect each mutation. The mutant may be an invalid stochastic kernel; it tests algebraic integrity only.
4. No hypothesis tests, model fitting, confidence intervals, real human records, E2/E3 predictions or external independent replication will be claimed. A mathematical nonidentifiability result in the frozen artificial kernel is not a conclusion about original Derex participants.
5. Any discrepancies, failures or protocol corrections must be disclosed in a new addendum rather than replacing this file.

No GitHub Actions are authorized by this freeze. Run locally with free standard-library tools and preserve machine receipts.