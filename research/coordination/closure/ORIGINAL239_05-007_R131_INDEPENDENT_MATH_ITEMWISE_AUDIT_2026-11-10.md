# Original239 05-007 / R131: independent mathematics audit, limited scope

Date: 2026-11-10. Track: closure. Baseline main: `fabbb3e1bffe609cb2e3bbd93f8ce632b7bf41be`.

## Purpose and provenance

This is a new, narrowly scoped, retrospective audit of the provisional catalogue crosswalk item `05-007` (Evolutionary Game Theory, proposed primary R131). It does not amend the frozen R131 protocol, the R131 original report, or the original239 crosswalk. The crosswalk's `PROVISIONAL_PRIMARY_README_LINK` remains unchanged until the full itemwise evidence gates are checked.

Read from main:
* `docs/ORIGINAL_239_PENDING_154_ITEMWISE_EVIDENCE_TRIAGE_QUEUE_2026-10-25.csv` blob `3b96d46b3d88ccafd779a08509c3cfd0e435772f`.
* `protocols/RESEARCH_ACCEPTANCE_STANDARD_V1_2026-10-16.md` blob `757a7ed7531e11bb9c0341777401fe3510d6e088`.
* `research/R131/R131_FINAL_ACCEPTANCE_STATUS.json` blob `3fa4bc6657ae38ee306e106dbd98f21edd48451b`.
* `research/R131/R131_TAYLOR_JONKER_1978_ORIGINAL_ESS_DYNAMIC_COUNTEREXAMPLES_AND_FINITE_DRIFT_SCIENTIFIC_REPORT_2026-10-20.md` blob `22a0877501a525f780fc8e525f9b682c1cde9eef`.
* `research/R131/README.md` blob `c499c843cb3124ab92dd515ef2440bd20a5be400`.

The existing R131 record attributes two mathematical examples to Taylor and Jonker (1978), DOI 10.1016/0025-5564(78)90077-9, and explicitly bounds the study to mathematical E1. The present audit did **not** independently open the 1978 original PDF, replay the R131 program, read the original frozen protocol in full, inspect the claimed GitHub Actions job logs, or validate its three-file SHA256 receipt. Those gates remain OPEN for this audit.

## Independently executed calculations

Executed with local Python and SymPy, constructing the two 3-by-3 matrices and the two-dimensional replicator vector field directly from the numeric matrices reported in the R131 scientific report, without importing R131 source code or using its reported Jacobian values as inputs.

For any matrix `M`, set `X=(x,y,1-x-y)`, `f=M*X`, `fbar=X.T*f`, and `g_i=X_i*(f_i-fbar)` for i=0,1. Independently calculate the exact symbolic Jacobian `Dg/D(x,y)`, then substitute the stated equilibrium.

**Example 1**: `M=[[-1/2,1,-1],[-1,-1/2,1],[1,-1,-1/2]]`, `p=(1/3,1/3,1/3)`. Computed exact continuous Jacobian `[[1/6,2/3],[-2/3,-1/2]]`, trace `-1/3`, determinant `13/36`, mean payoff `-1/6`. For the original reported discrete rule `x_i' = x_i(1+f_i)/(1+fbar)`, the fixed-point linearization is `I+J/(5/6)`, with trace `8/5`, determinant `28/25`. This independently confirms the reported local continuous stability and discrete instability for the stated example. It does not check the original article's equation typography.

**Example 2**: `M=[[2,1,5],[5,1,0],[1,4,3]]`, `p=(15,11,9)/35`. Computed Jacobian `[[-291/245,-60/49],[2013/1225,33/49]]`, trace `-18/35`, determinant `297/245`, mean payoff `86/35`. For `q=(0,0,1)` and `r=(1-u)p+u*q`, exact symbolic payoff advantage `(q-p).T*M*r = 3*u/35`. Thus the stated local continuous stability and the specified invasion counterexample agree with an independent calculation.

**Project-added finite-population illustration**: independent exact rational sum `1/sum((3/2)^i for i=0..4) = 16/211`, matching the R131 report. This is a constructed Moran-type mathematical example, not 1978 empirical evidence.

All calculations used exact symbolic/rational arithmetic, with no random seed. These checks are independent algebraic recomputations based on already reported inputs. They are **not** a blind independent source transcription, original code execution, real-human E2 test, historical E3 test, or external-researcher replication.

## Itemwise gate result

* A01 question/scope: PARTIAL. The R131 report clearly states a bounded mathematical scope; original frozen protocol has not been independently checked in this run.
* A02 source: PARTIAL. Author/title/DOI and claimed page range were read in repository metadata; direct original PDF page verification remains OPEN.
* A03 computation: PARTIAL/PASS for the exact algebra above only. The original executable, 63 tests, CI job `39360828291`, and SHA256 receipt were not rerun or revalidated here.
* A04 failure/negative evidence: PARTIAL. Both stability/ESS non-equivalence examples and limits are explicit; full source and negative test audit remain OPEN.
* A05 inference boundary: PASS for the reviewed report's explicit E1-only scope; no new E2/E3 or empirical validation.
* A06 final closure: OPEN for this new independent audit. The historical R131 `CLOSED_BOUNDED` status is preserved without retroactive upgrade or downgrade.

**Net scientific audit increment:** three exact mathematical claims independently recomputed (two source-attributed replicator examples and one project-added fixation fraction); one original239 provisional item has a documented partial audit, but **zero original239 items promoted or scientifically closed**. Original 154-row pending queue remains unmodified; its current scientific count has not been independently exhaustively recomputed.

## Next steps

Independently verify original Taylor/Jonker PDF pp.147,149–151 against source-attributed matrices and equations; inspect frozen protocol and the original CI receipt; replay the original Python implementation and its tests with controlled environment. Only then evaluate whether the catalogue item can be reclassified from provisional linkage to a verified bounded evidence link. Keep `R131` historical `CLOSED_BOUNDED` and E1 limitations unchanged pending that review.

GitHub write of this note, if successful, is archival evidence only. No CI or billable service was triggered intentionally.
