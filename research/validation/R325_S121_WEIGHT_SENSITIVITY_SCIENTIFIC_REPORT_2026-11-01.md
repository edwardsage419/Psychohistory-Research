# R325 S121: exact state-weight sensitivity in project-constructed regret comparison

Date: 2026-11-01 (Asia/Singapore). Track R. Status: **PARTIAL_E1_EXTENSION**. Original239 01-020.
Frozen prescore protocol: commit `fff93b2a837d63be4047e932b1c6f66bfff9a0a7`. Parent R325 accepted only for bounded constructed cubic E1, with 1029 original source rows and three fixed kappa worlds. Parent files and acceptance unchanged.

## Mechanism and new question
Original Q(d)=d+kappa*d^3 for kappa 0, 1/4, 1. Enumerate 343 ordered triples from {-3,-2,-1,0,1,2,3}^3. Replace equal state probabilities with four predeclared probability vectors U=(1/3,1/3,1/3), EARLY=(1/2,1/3,1/6), LATE=(1/6,1/3,1/2), CENTER=(1/4,1/2,1/4). Compare EU=sum p*d and F=sum p*Q(d). All 4 x 3 x 343 = 4116 artificial rows, no fitted data.

## Exact counts
| Profile | kappa | A | B | ties | strict EU/regret reversals | changed choice vs U | strict sign disagreement vs U |
|---|---:|---:|---:|---:|---:|---:|---:|
| U | 0 | 153 | 153 | 37 | 0 | 0 | 0 |
| U | 1/4 | 162 | 162 | 19 | 6 | 0 | 0 |
| U | 1 | 162 | 162 | 19 | 6 | 0 | 0 |
| EARLY | 0 | 163 | 163 | 17 | 0 | 72 | 24 |
| EARLY | 1/4 | 168 | 168 | 7 | 14 | 50 | 26 |
| EARLY | 1 | 165 | 165 | 13 | 16 | 50 | 20 |
| LATE | 0 | 163 | 163 | 17 | 0 | 72 | 24 |
| LATE | 1/4 | 168 | 168 | 7 | 14 | 50 | 26 |
| LATE | 1 | 165 | 165 | 13 | 16 | 50 | 20 |
| CENTER | 0 | 159 | 159 | 25 | 0 | 66 | 18 |
| CENTER | 1/4 | 165 | 165 | 13 | 16 | 34 | 16 |
| CENTER | 1 | 163 | 163 | 17 | 16 | 34 | 12 |

Strict reversal means EU and F have opposite strict signs. Changed choice includes transitions involving ties; strict sign disagreement excludes ties. Counts are complete mathematical enumerations over constructed inputs, not rates of human behavior.

## Concrete witness and interpretation
At d=(-2,1,3), EARLY and kappa=1/4, EU=-1/6 and F=1/24, a strict preference reversal. At d=(-3,1,2), CENTER and kappa=1, EU=1/4 and F=-13/16, another strict reversal. EARLY and LATE have identical aggregate counts due to reversal symmetry of the full ordered universe, yet their predictions differ on 110 of 343 triples at kappa=0 and on 82 triples at each nonlinear kappa. Aggregate equality therefore conceals state-order dependence.

The uniform profile reproduces the original 0,6,6 reversal counts. Kappa zero yields F=EU for every profile. All nonnegative difference triples produce nonnegative F, all nonpositive triples produce nonpositive F. This finite coordinatewise monotonicity check does not establish general empirical stochastic dominance.

## Reproduction and boundaries
Primary script `research/validation/r325_s121_weight_sensitivity.js` reads and checks original source blob `b4964ef88aded2c9bd2a70280c067176fedcd597`, validates every original mathematical row, and deterministically generates `R325_S121_ALL_4116_WEIGHTED_STATES.csv` and `R325_S121_EXACT_WEIGHT_RESULTS.json`. The persisted output blobs are `8df84f30ad1d680758aa526d3f8f05a911523bd0` and `b1c4bf4d07f0479fdefb1dc22aa202b8e6526531`. The JS calculation was executed in the connected V8 runtime; archived native Node CLI execution remains NOT_RUN.

Independent Python Fraction reconstruction of all 4116 rows generated the exact same two Git blobs. A second archived Python row checker ran in ordinary and optimized modes against independently reconstructed local copies and rejected four live mutations in each mode. This is internal, nonblind, method-distinct E1 verification. No external independent team, human E2, historical E3, out-of-sample forecast or empirical calibration.

Primary sources: Loomes and Sugden (1982), DOI 10.2307/2232669; Bell (1982), DOI 10.1287/opre.30.5.961. The cubic Q and probability profiles are project-created illustrations and are not original-author estimated parameters.

CI for S121 NOT_RUN due to unverified free billing allowance. R073 model and scoring and PESEN v0.1 remain frozen. No model classification, fusion or personal decision product development.
