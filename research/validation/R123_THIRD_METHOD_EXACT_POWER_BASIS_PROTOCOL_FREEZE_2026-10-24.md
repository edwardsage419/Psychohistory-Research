# R123 next-queue preaudit and third-method protocol freeze

Date: 2026-10-24. Parent main HEAD: `16591101f0376450f67706aa2d77723ef444d80a`. Status: **PROTOCOL_FROZEN; NEW EXECUTION_NOT_STARTED**. Catalogue original239 04-009, DeGroot Consensus Model. Reuse existing R123. Do not modify its original source, tests, report or acceptance.

## Original non-Chinese sources and prior scope

Morris H. DeGroot (1974), *Reaching a Consensus*, JASA 69(345):118–121, DOI 10.1080/01621459.1974.10480137, original PDF https://pages.ucsd.edu/~aronatas/project/academic/degroot%20consensus.pdf . Roger L. Berger (1981), *A Necessary and Sufficient Condition for Reaching a Consensus Using DeGroot's Method*, JASA 76(374):415–418, original article PDF https://www.cse.cuhk.edu.hk/~cslui/CMSC5734/degroot_method-berger_jasa81.pdf .

Existing `research/R123/README.md` (blob `c31d4a37711d04b2e63e6c0c74b84ed2f6386782`) and `research/R123/R123_FINAL_ACCEPTANCE_STATUS.json` (blob `258aea476455ad6f54d6f08139b503f9613e27c8`) already document original printed sources, the important Berger correction, 58 original tests, 226 finite row-stochastic matrices and CI 39263259641. The existing work separates universal consensus for all initial vectors, per-person convergence, and one particular initial vector reaching agreement. Preserve this distinction. No duplicate R ID.

## New falsifiable third-method experiment

Write a separate standard-library Fraction auditor. Enumerate the exact same finite 226 row-stochastic matrices as the original R123 program: n=1 has 1, n=2 has 9, n=3 has 216, where each row has one 1 or two 1/2 entries. Independently construct W and multiply W by itself for **256** iterations using exact rational arithmetic. For each W, treat each column of W^256 as the resulting opinion vector from an independent basis initial opinion e_j. This uses neither original R123 long-run influence algorithms nor its structural classifier during power computation.

Compare each column's max-minus-min spread to an explicit fixed tolerance **2^-24**. Require the finite-horizon universal-consensus classifier to match the original graph-theoretic universal-consensus classification for all 226 matrices. If any disagreement occurs, report the exact matrix and stop; do not adjust the horizon or tolerance after seeing failures. Record all 226 matrix IDs, W^256 basis-vector spread maxima, classification and original classifier output in a raw CSV. Separately require the original R123 58 tests to pass on Python 3.11 and 3.12, verify original source/test/report Git blobs, and reject one mutated CSV and one false original-source SHA.

Negative controls: periodic two-person swap W=[[0,1],[1,0]] must fail universal consensus for distinct basis inputs but retain consensus for initial (1/2,1/2); two absorbing nodes W=I must fail universal consensus yet each person converges; a one-absorbing-leader network must pass universal consensus although the entire graph is not strongly connected; original 1974 two-person example must converge toward weights (1/3,2/3), with the chosen initial (0,1) approaching 2/3. Distinguish finite-time near-equality from a mathematical limit in the final report.

Expected success criterion: 226/226 classifications match, exact matrix roster count, four negative/positive controls, full CSV replay, 58 original tests in both Python versions, and a successful free standard Ubuntu CI. If finite-horizon equivalence fails, preserve the failure as evidence; do not relabel it as an original theorem violation without further analysis.

Maximum allowed new evidence: `PASS_BOUNDED_INTERNAL_FINITE_POWER_BASIS_E1`. No real human E2, historical E3, external-team reproduction, fitted real opinion trajectories or universal claims for matrices outside this finite roster. R073 and PESEN v0.1 frozen. Original239 v7.2 has 161 pending links; do not reduce pending count until actual new R123 audit and CI succeed.
