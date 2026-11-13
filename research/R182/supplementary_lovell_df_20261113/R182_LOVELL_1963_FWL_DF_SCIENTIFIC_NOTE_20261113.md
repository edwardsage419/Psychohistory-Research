# R182 2026-11-13 independent Lovell 1963 degrees-of-freedom audit

Status: COMPLETE_BOUNDED_INTERNAL_MATH_E1 for the new postscore inference-denominator issue. No change to historical R182 score or its frozen research protocol. This is **not** a claimed replication of Lovell's seasonal data, a human experiment, or an original data-dependent hypothesis test.

## Source and provenance

Repository: `edwardsage419/Psychohistory-Research`. Observed starting HEAD: `269dfab8a0811497255b6e9265d35838b2d06685`.

Primary paper: Michael C. Lovell (1963), *Seasonal Adjustment of Economic Time Series and Multiple Regression Analysis*, *Journal of the American Statistical Association* 58(304):993–1010, DOI `10.1080/01621459.1963.10480682`, available as full printed journal copy at `https://www.stat.ucla.edu/~nchristo/statistics100C/partial_regr.pdf` (directly read published pp.1001–1004, Theorem 4.1 and Eq.(4.5)). Author's Cowles Foundation discussion paper dated January 1963 at `https://cowles.yale.edu/sites/default/files/2022-08/d0151.pdf` was independently visually checked at printed pp.32–34, where Eq.(5.10) gives the equivalent factor `sqrt((n-k)/(n-k-d))`. These are original-language source pages, not secondhand summaries.

Pre-existing untouched R182 research: `protocols/R182_OLS_FWL_240_WORLDS_PRESCORE_FREEZE_2026-10-21.md` and `research/R182/R182_SCIENTIFIC_REPORT_2026-10-21.md`. Original 240-world E1 FWL equality and 54 sign reversals previously verified with GitHub Actions run 39559935431. A separate 960-world E1 covariate-shift predictive risk audit and independent B validation were completed October 26, 2026. None of those experiments are repeated for new scientific credit. This audit isolates the **unreported conventional homoskedastic standard-error degrees of freedom** when reproducing the same regression coefficient from residualized regressors.

## New, exactly specified statistical mechanism

Original R182 synthetic model: `y=a+b*x+c*z+eps`, with the frozen (x,z) four-cell even counts, x,z binary. Full regression `y ~ 1+x+z` has rank 3 and residual degrees of freedom `N−3`. FWL first removes span{1,z} from y and x. The resulting residualized regression `y_tilde ~ x_tilde -1` has the same beta and exactly the same residual sum of squares, but a naive stand-alone univariate routine would assign `N−1` residual df, ignoring two previously estimated control parameters.

Write `Sxx_tilde=Σ(x_i−E_hat[x|z_i])²`. For the *conventional homoskedastic formula*:

`SE_correct² = [SSE/(N−3)] / Sxx_tilde` and `SE_naive² = [SSE/(N−1)] / Sxx_tilde`.

Thus where `SSE>0`, the exact arithmetic ratio is

`SE_naive² / SE_correct² = (N−3)/(N−1)`

or `SE_correct = SE_naive * sqrt((N−1)/(N−3))`. This is the special case k=1 retained predictor, d=2 removed controls of Lovell's published Eq.(4.5). These are finite-sample formula identities; whether their numerator is an unbiased conditional sampling variance estimate requires separate stochastic assumptions absent from these artificial deterministic rows. At SSE=0, both standard errors are zero and their ratio is undefined. Do not divide 0/0 or claim any nonzero t-test is valid from constructed deterministic errors.

## Independent algorithms and actual local execution

Two separate computational routes were executed with Python standard-library Fraction: (A) regenerate **every row** from the publicly frozen 4 design counts × 2 intercepts × 2 target slopes × 5 nuisance effects × 3 residual magnitudes, then independently remove the conditional z means from the two columns, compute actual FWL beta, SSE, `Sxx` by summing individual residualized rows; (B) compute `Sxx` directly from source four-cell counts using `n00*n10/(n00+n10)+n01*n11/(n01+n11)`, and SSE from `N*e²`. Both exact routes matched all 240 artificial worlds (total 2880 generated observations) and every conventional SE denominator identity. This regenerates the **source mathematical design**, without claiming to have downloaded and bytewise compared the entire historical CSV; an initial GitHub read verified the CSV's first rows and field encoding.

160 worlds had e>0 and SSE>0, with `SE_naive²<SE_correct²`; 80 e=0 worlds had SSE=0 and undefined SE ratio. For frozen example `a=0,b=1/4,c=-2,e=1/4`:

| Source design | N | Sxx_tilde | SSE | Correct SE² | Naive SE² | Naive/correct squared |
|---|---:|---:|---:|---:|---:|---:|
| BALANCED | 8 | 2 | 1/2 | 1/20 | 1/28 | 5/7 |
| POSITIVE | 12 | 8/3 | 3/4 | 1/32 | 9/352 | 9/11 |
| NEGATIVE | 12 | 8/3 | 3/4 | 1/32 | 9/352 | 9/11 |
| STRONG_POSITIVE | 16 | 3 | 1 | 1/39 | 1/45 | 13/15 |

The strongest ratio deviation is the smallest N=8 case. In a future genuine stochastic linear-model study with homoskedasticity and appropriate independence, the naive t-statistic would be larger by `sqrt((N−1)/(N−3))`; its formal significance cannot be transferred to the present deterministic data. The historical R182 primary report and acceptance files made no historical conventional standard-error claims, hence **no demonstrated error in original accepted R182 results**.

## Verification and evidence boundary

New files in `research/R182/supplementary_lovell_df_20261113/`:

* `r182_lovell_df_correction.py`: standard-library Fraction calculation, complete 240-world loop;
* `test_r182_lovell_df.py`: 8 distinct fail-closed and algebra tests;
* `R182_LOVELL_DF_EXACT_RESULTS_20261113.json`: complete exact design-level examples and audit counts;
* this note.

Commands actually run in local Python 3: `python -m unittest -v test_r182_lovell_df.py`, 8 passed; `python -O -m unittest -v test_r182_lovell_df.py`, 8 passed; and `python r182_lovell_df_correction.py` produced deterministic JSON. CI NOT_RUN. New genuine behavior E2=0; real historical forecasting E3=0; independent external reproduction=0. This is an internal mathematical E1 postscore supplement only. No changes to original R182/R073/PESEN files, evidence grades, experimental design, five automated workflows, or Codex work. No paid API or fee-generating CI used.

## Next science step

Prioritize original itemwise scientific acceptance whose sources or genuine external validation remain incomplete, instead of rerunning the already-accepted artificial OLS/FWL, R182 960 artificial shifts, R135 original 4096-case check, or concurrently assigned engineering PR fixes. A future real-data standard-error validation would need stochastic sampling assumptions, independent data and preregistration; none is claimed here.
