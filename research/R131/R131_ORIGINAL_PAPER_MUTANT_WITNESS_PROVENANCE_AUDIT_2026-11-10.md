# R131 source witness provenance audit (2026-11-10 UTC)

Track: R; scope: source attribution and independent exact algebra, without changing the frozen protocol or historical acceptance. Observed main before write: `76e1c1f5860465dc13b570479245299aebbe9721`. Existing closure-track itemwise audit: `research/coordination/closure/ORIGINAL239_05-007_R131_INDEPENDENT_MATH_ITEMWISE_AUDIT_2026-11-10.md` (blob `ccef1b57bb0b04982ddc7166680593b0c0494ccb`). This R-track note covers a distinct source-witness attribution issue.

## Original primary source independently opened

Peter D. Taylor and Leo B. Jonker (1978), *Evolutionarily Stable Strategies and Game Dynamics*, *Mathematical Biosciences* 40, 145–156, DOI 10.1016/0025-5564(78)90077-9. Author publication page: https://sites.google.com/view/peter-taylor/biology/publications . Author-linked publisher facsimile PDF: https://static1.squarespace.com/static/5dc9917c4cdb1467e1e54c4c/t/6526a5647942e33b89ab7af1/1697031525653/1978%2Bevolutionarily%2Bstable%2Bstrategies%2Band%2Bgame%2Bdynamics.pdf . Accessed 2026-11-09 UTC; directly inspected printed pp.150,151,153 (PDF zero-based pages 5,6,8), including matrix typography and the explicit mutant witness.

Printed p.150 gives the epsilon cyclic matrix `[[-epsilon,1,-1],[-1,-epsilon,1],[1,-1,-epsilon]]`, matching the R131 source-attributed matrix family. Printed p.151 gives `[[2,1,5],[5,alpha,0],[1,4,3]]`, matching R131 at alpha=1.

**Important provenance distinction:** On printed p.153, the original authors explicitly choose `q_original=(18,17,0)/35` at `p=(15,11,9)/35` for alpha=1. The R131 frozen project report instead chooses `q_project=(0,0,1)`. Both are mathematically valid counterexamples, but they are different witness vectors. The project report already describes its witness as a specified mutant, so the correct archival clarification is to attribute the **matrix family and non-ESS phenomenon** to the 1978 paper and identify the pure-strategy mutant vector as a **project-chosen alternative witness**, not the paper's printed witness.

## Independent exact arithmetic

Using the matrix `A=[[2,1,5],[5,1,0],[1,4,3]]`, `p=(15,11,9)/35`, `r=(1-u)p+u*q`, directly evaluated `(q-p)^T A r` with SymPy rational arithmetic, without importing R131 code. For the printed original `q_original=(18,17,0)/35`, the exact invasion advantage is `27*u/1225`. For the project alternative `q_project=(0,0,1)`, the exact advantage is `3*u/35`. Both are strictly positive for every u>0. The two distinct coefficients demonstrate why provenance of the mutant witness matters even though the final non-ESS inference remains valid. No random seed.

The project-added finite-population Moran illustration remains separate from the 1978 source. The existing historical E1-only bounded acceptance is unchanged. This audit does not establish an E2 or E3 prediction, rerun the historical 63 tests or CI, independently validate receipt SHA256, or close the original239 provisional source gate. It adds a directly checked primary-source witness identity and an exact two-witness comparison.

Status: COMPLETE for the cited original witness identity and exact rational comparison; PARTIAL for overall itemwise source and execution closure. No changes to frozen R131, R073 or PESEN v0.1; no new Actions requested. Next: verify original CI receipt and executable independently, then evaluate the existing itemwise closure gates with the closure track without duplicating its work.
