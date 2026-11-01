# R328 S124 scientific report: finite precision-weighted error update stability

Date: 2026-11-01 UTC. Track: r. Main baseline before report: e295f5ba5fdeda21a9b6634df2f8e019a04934c2.
Evidence: E1 deterministic artificial scalar dynamics. Status: **PARTIAL_E1_EXTENSION**. Original R328 bounded E1 acceptance remains unchanged.
Protocol frozen first: [b9838d4052c9632d950cffd2e22a9fa3e1ae47b5](https://github.com/edwardsage419/Psychohistory-Research/commit/b9838d4052c9632d950cffd2e22a9fa3e1ae47b5).
Original R328 source: `research/R328/r328_scalar_predictive_error.py` and 120 artificial rows, source blob `b699cf1100955e89ed2edee7757bee70083656b0`.

## Question, fixed design and exact derivation
The project-defined R328 scalar predictive error update has energy
`E(x) = r(x-m)^2/2 + p(y-x)^2/2`, optimum `x*=(r*m+p*y)/(r+p)`, and step update `x[t+1]=x[t]+alpha*(p*(y-x[t])+r*(m-x[t]))`. Original alpha=1/4 is held as a baseline; this extension adds alpha=1/2,3/4,1, with the same 24 artificial parameter worlds and t=0..4. Total 96 world cases and 480 labelled artificial source rows.

Let `lambda=1-alpha*(r+p)`. Then `x[t]=x*+(m-x*)*lambda^t`, and
`E(x[t])-E(x*)=(r+p)*(m-x*)^2*lambda^(2t)/2`.
For nonzero initial error, energy converges for `|lambda|<1`, stays at the same gap for `|lambda|=1`, and grows for `|lambda|>1`. A zero initial error stays at the optimum regardless of lambda, so it must be separated from neutral or expansive behavior.

## Full exact results
| alpha | zero-residual flat | contractive | neutral | expansive | worlds with at least one energy increase |
|---|---:|---:|---:|---:|---:|
| 1/4 | 8 | 16 | 0 | 0 | 0 |
| 1/2 | 8 | 12 | 4 | 0 | 0 |
| 3/4 | 8 | 4 | 0 | 12 | 12 |
| 1 | 8 | 0 | 4 | 12 | 12 |
| TOTAL | 32 | 32 | 8 | 24 | 24 |

All 480 row identities are unique. The 120 rows for alpha=1/4 agree field-by-field with the original frozen R328 CSV after removing the added alpha, lambda and gap fields.

Fixed witness m=0,y=2,r=p=2:
* alpha=1/4: x1=1, x4=1, E4=2 (optimum).
* alpha=1/2: x alternates 0 and 2, E0=E4=4; zero improvement despite four updates.
* alpha=3/4: x1=3, x4=-15, E0=4, E4=514; the update diverges in this finite constructed case.
* alpha=1: x4=-80, E4=13124.

The stability threshold for a nonzero initial error is `0 < alpha < 2/(r+p)`. At the boundary, a negative lambda of -1 produces persistent oscillation. Above the boundary, fixed-step correction overshoots and amplifies error. This is a mathematical property of the specified scalar quadratic, with no claim of neural or human learning-rate estimates.

## Reproduction and negative evidence
Primary archived JS source `research/validation/r328_s124_step_size.js` generated the 480-row CSV and 96-world JSON. Exact original archived JS was subsequently fetched and executed in a V8 adapter; regenerated strings matched both full remote files byte for byte. The independent Python Fraction closed-form script, `research/evidence_audit/b_r328_s124_independent_fraction.py`, ran in ordinary and optimized Python modes. It produced Git blob SHA identities identical to the persisted remote files and rejected five deliberately altered receipts. This is **nonblind internal** E1 verification. Original Node CLI and GitHub Actions for S124 have **NOT_RUN**; historical R328 CI does not certify this extension.

Data:
`research/validation/R328_S124_ALL_480_STEP_SIZE_STATES.csv`, Git blob `c2343a241f5389071eb1c8cdaf8c9e955f7daca2`, 18,220 bytes.
`research/validation/R328_S124_EXACT_96_STABILITY_WORLDS.json`, Git blob `9e06c249036ebe09316e9952017b043afe96df73`, 34,439 bytes.
Independent audit report: `research/evidence_audit/B_R328_S124_NONBLIND_FRACTION_480_ROW_FIVE_MUTATIONS_2026-11-01.md` (separately committed).

## A01–A06 bounded acceptance accounting
A01 PASS (fixed finite stability question). A02 PASS for original R328 source identity and prospective S124 freeze, with no original neural data. A03 PASS for V8 and independent Python exact receipt identity, native Node/CI OPEN. A04 PASS for expansive/neutral counterexamples and five mutation controls. A05 PASS for bounded E1 claims; E2/E3 NOT_ESTABLISHED. A06 PARTIAL because S124 native Node CLI and independent external replication remain open. Final S124 grade: PARTIAL_E1_EXTENSION; no promotion of original R328 formal acceptance.

Original English theoretical context: Rao & Ballard 1999 DOI 10.1038/4580 and Friston 2005 DOI 10.1098/rstb.2005.1622, as already pinned by R328. Their neural architectures were not rerun. R073 model and scoring and PESEN v0.1 remain frozen. Original239 index and 154-item queue untouched. No paid compute or Actions triggered.
