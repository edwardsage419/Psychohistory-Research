# R318 Cumulative Prospect Theory: exact finite signed rank weighting E1

Date 2026-10-24 Asia/Taipei. Original239 model **01-003 Cumulative Prospect Theory**, P2. New study scope: **only 36 artificial two-outcome lotteries and 72 outcome contribution source records**.

## Origin and frozen design

Tversky and Kahneman (1992), *Advances in prospect theory: Cumulative representation of uncertainty*, *Journal of Risk and Uncertainty* 5:297–323, DOI https://doi.org/10.1007/BF00122574 . Their theory applies rank-dependent cumulative probability decision weights separately for gains and losses; the present project study tests the algebra but deliberately uses a **noncanonical illustrative rational weight transform**, so it is not a replication of their empirical calibrated inverse-S weighting function. The frozen [R318 prescore protocol](../../protocols/R318_CPT_TWO_OUTCOME_SIGN_RANK_72_ATOMS_PRESCORE_FREEZE_2026-10-24.md) has Git commit `93138708c98f94da71d83f9bf7829b810b5bc8a7`, before any calculations.

Artificial outcome values X={−2,−1,1,2}, all 6 unordered sorted pairs, p for the low outcome in {1/4,1/2,3/4}; 18 lotteries. Each is valued in two predeclared cases: identity w0(p)=p, illustrative asymmetric w1(p)=p²/(p²+2(1−p)²). Value function v(x)=x for positive x, 2x for negative x (illustrative loss factor 2, linear both sides). Each lottery contributes two original exact rational source rows, producing 36 valuations and 72 rows.

Weights for two pure gains: high outcome w(p_high), low 1−w(p_high). For two pure losses: low outcome w(p_low), high 1−w(p_low). For mixed outcomes low negative and high positive: low weight w(p_low), high weight w(p_high), both separately. Nonidentity p transform need not preserve weight additivity across mixed signed outcomes; it is still a pre-specified rank-/sign-tail calculation.

## Frozen exact checks

* Identity w0 valuation equals directly computed p_low v(low)+(1−p_low) v(high) for **all 18 lotteries**.
* For the noncanonical transform, w1(1/4)=1/19, w1(1/2)=1/3 and w1(3/4)=9/11. Every pure gain or pure loss pair decision weights sum to 1 by construction.
* Prespecified mixed witness x_low=−2, x_high=+2, p_low=1/4: identity valuation=1/2; noncanonical weights are (1/19,9/11), sum **182/209**, giving valuation **298/209**. A naive single normalized probability weighting would conceal this sign-specific CPT mechanism.
* All source contributions and complete valuations match exact Fraction arithmetic and a separate no-import odds-formula reconstruction. All 72 source atoms retained without fitting, changing samples or selectively recording favorable comparisons.

## Critical limits

Neither probability weighting function is estimated from original 1992 respondents. The illustrative rational weighting rule is a user/project synthetic pedagogical instance **and is not the article's published original weighting shape**, and lambda=2 is fixed rather than empirically identified. Nothing establishes population loss aversion, behavioral probability inversion, preference reversals, bounded rationality causal factors, individual forecast gains or historical evolution from these 36 synthetic lotteries. Real human E2=0; historical E3=0.

[Main source and tests](r318_exact_cpt_rank_sign.py), [72 original contribution CSV](R318_ALL_72_ORIGINAL_RANK_SIGN_OUTCOME_SOURCE_ATOMS.csv), [36 valuations JSON](R318_EXACT_36_TWO_OUTCOME_CPT_VALUES.json), [independent odds audit](../catalogue_audit/independent_r318_cpt_source_audit.py) and [GitHub CI workflow](../../.github/workflows/r318-cpt-sign-rank-e1.yml). Only after 3 green CI jobs and source Git blob verification can E1 formally close and original239 map only 01-003 to R318. R073/PESEN v0.1 remain frozen.
