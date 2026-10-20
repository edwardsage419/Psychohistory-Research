# R153 Spatial interaction models: independent IPF versus scalar OD solution

Date: 2026-10-20. Original catalog **P2 / 06-011 Spatial Interaction Models**. Previous completed stage R152; prescore freeze [R153 protocol](../../protocols/R153_SPATIAL_INTERACTION_DOUBLY_CONSTRAINED_PRESCORE_FREEZE_2026-10-20.md), GitHub commit `99183f26cd5ef25677f27ea6fd4078044591aa04`. **Scientific level E1, author-replication level zero, no real spatial behavioral data or historical forecast added.**

## Primary sources actually checked, and boundaries
* Alan G. Wilson, *Entropy in Urban and Regional Modelling* (1970), [Routledge publisher 1970 original / reissue entry](https://www.routledge.com/Entropy-in-Urban-and-Regional-Modelling-Routledge-Revivals/Wilson/p/book/9780415696319). Its publisher description identifies entropy maximization and constraints as central to spatial model formation. This stage does **not** represent a page-by-page reproduction of Wilson's derivation or use his original numerical observations.
* David L. Huff, *Defining and Estimating a Trading Area*, *Journal of Marketing* 28(3), 34–38, July 1964; [SAGE primary article/abstract and DOI](https://journals.sagepub.com/doi/full/10.1177/002224296402800307). Huff's retail trading-area subject is separate from the artificial origin-destination tables below. Huff's data and specific model fit were **not** reproduced.
* A. S. Fotheringham, *A New Set of Spatial-Interaction Models: The Theory of Competing Destinations*, *Environment and Planning A* 15(1), 15–36, January 1983; [SAGE primary abstract](https://journals.sagepub.com/doi/10.1177/0308518X8301500103). The abstract raises spatial-structure-induced parameter interpretation and competing-destination specification. No author competing-destinations algorithm/data fit was attempted here.

A full paper/book-method audit remains open. The solved 2×2 maximum-entropy weighting example is a **project-authored controlled test of origin and destination constraints**, not an inference that real distance-decay coefficients have a particular behavioral interpretation.

## Prespecified experiment and independent algorithms
All 60 frozen parameter combinations: three artificial origin budgets (3,5), (4,4), (6,2); four destination budgets (2,6), (3,5), (4,4), (5,3); and five positive weight kernels W0–W4 in the frozen protocol. Here origins and destinations are separately labeled sets; diagonal cells represent permissible origin-to-destination flows, unlike R152's four-region no-self-migration setup. Total mass fixed at 8. Full ordered 60-case output: [R153_EXACT_RESULTS.json](R153_EXACT_RESULTS.json).

Origin-only allocation:
\[
S_{ij}=O_i W_{ij}/\sum_k W_{ik}
\]
It has exactly the prescribed rows but no guarantee about columns.

Doubly constrained allocation: maximize \(\sum_{i,j}T_{ij}\log(W_{ij}/T_{ij})\) under both positive origin and destination totals. Given positive weights, solution has \(T_{ij}=u_i v_j W_{ij}\) and is unique for this feasible 2×2 setting. For \(O=(a,b)\) and \(D=(c,8-c)\), any feasible T equals
\[
T=\begin{pmatrix}x&a-x\\c-x&b-c+x\end{pmatrix},
\quad x\in [\max(0,c-b),\min(a,c)].
\]
Two independent approaches: floating point iterative proportional fitting (IPF, alternately rescaling rows and columns) and separate bisection of the stationary cross-product equation
\[
x(b-c+x)W_{01}W_{10}=(a-x)(c-x)W_{00}W_{11}.
\]
Neither uses the other's numerical solution as initialization or target. Uniform W has a separate exact Fraction reference \(T_{ij}=O_iD_j/8\). Structural zero cases are adjudicated with an exact support interval for x.

## Verified outcomes
All 60 prespecified cases solved. **54 of 60** origin-only outputs miss at least one target destination total, while the doubly constrained outputs attain both row and column budgets to a maximum absolute discrepancy of **9.395×10⁻¹¹** across the stored 60 cases. The independent IPF/scalar algorithms agree at every table entry to **7.417×10⁻¹¹** maximum difference, below the prespecified 10⁻⁹ threshold. Maximum difference between origin-only and doubly constrained individual predicted cells within the 60 worlds is about **2.324555320337** artificial flow units. These are deterministic constructed examples, not measurements.

An intuitive preregistered uniform W case with O=(3,5), D=(2,6):
| | Origin 0 to destinations (0,1) | Origin 1 to destinations (0,1) | Resulting destination totals |
|---|---|---|---|
| Origin-only | (1.5,1.5) | (2.5,2.5) | (4,4) |
| Doubly constrained | (0.75,2.25) | (1.25,3.75) | (2,6) |
The second row is also exactly [[3/4,9/4],[5/4,15/4]], established by independent Fraction multiplication.

Row and column *positive* factorization cannot be identified from doubly constrained flows when margins are fixed: replacing \(W_{ij}\) by \(r_i c_j W_{ij}\), for positive r and c, has **exactly the same constrained optimum**. The tests check each of the five frozen kernels under independent row and column rescalings. Origin-only flows can change after a nonconstant destination multiplier. Thus observed exact margins do not separately identify all nuisance weight scales.

With structural zero W=((0,1),(1,1)) and O=(3,5), D=(4,4), the sole exact admissible solution is [[0,3],[4,1]]. Conversely, W=((1,0),(0,1)) is infeasible under these margins, and the solver explicitly rejects it. Misaligned totals, negative or nonfinite weights and unsupported whole rows/columns are also rejected. Structural zero tests are solved by the support-aware scalar routine, while the IPF implementation deliberately requires strictly positive kernels and rejects those inputs. **No general sparse-matrix IPF convergence guarantee is claimed.**

## Evidence and reproducibility receipts
* Precode freeze commit: [99183f2](https://github.com/edwardsage419/Psychohistory-Research/commit/99183f26cd5ef25677f27ea6fd4078044591aa04).
* Source and tests: [r153_spatial_od.py](r153_spatial_od.py), [test_r153_spatial_od.py](test_r153_spatial_od.py). Exactly 74 different discoverable unittest methods, of which 60 are separately named full scenarios. Supporting comparisons and type/structural controls are counted within the remaining 14.
* [CI run 39434054859](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39434054859): Python 3.11 (job118666298383) and Python3.12 (job118666298827) **74 tests each, success**, hashes and deterministic JSON/ZIP pass. Independent archive publication (job118666389772) ran 74 tests and all four fixed SHA256 checks successfully. **222 actual test executions, 74 distinct tests, zero failures**; these repeats are reproducibility checks and are not counted as three independent science studies.
* Main archive commit [9aaeccf](https://github.com/edwardsage419/Psychohistory-Research/commit/9aaeccf4290eb6b2d0badda85292cc7a199c57d4), containing full [55,110-byte JSON](R153_EXACT_RESULTS.json) and [standard-library ZIP_LZMA archive](R153_Spatial_Interaction_60_Cases_74_Tests.zip).
* Pinned SHA256: source `ed60ed3952c3e75efd046456e238f260082a839739e81b5cf87deec4c9185d97`; tests `3b9f0d49d5930fd4c353fc4b72ec1781c42695a084f49edd623391323c379ca7`; full JSON `9b2002c0aea89401660bd4b117b4dfcdec9c844479c7cd61e9e32b8fb5bc0f24`; ZIP `d7f5284aeabf3cc6e67317e3e38c67722c2b4d143197b235867401756252dd57`.
* Reproduction: from `research/R153` execute `python r153_spatial_od.py > R153_EXACT_RESULTS.json` followed by `python -m unittest -q test_r153_spatial_od.py`. Compare recorded SHA256. No third-party Python packages required.

R153 is **CLOSED_BOUNDED_E1** for this frozen 60-scenario test plan. The stage contributes no E2 person-level prediction and no E3 historical spatial validation, and it does not change frozen R073/PESEN v0.1. According to original catalog, next is **R154 P1/06-012 Stock and Flow System Dynamics**, which must be studied separately before any cross-model fusion.
