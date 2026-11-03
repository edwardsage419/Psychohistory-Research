# TH221 Robinson (1950): exact covariance decomposition and identification limits

track: theory
subflow: primary theory mathematical follow-up
run_date: 2026-11-03 (Asia/Singapore)
observed_head_before_write: 583986758f1a5c815230da26041cce7c1c504ecd
parent_note_blob: 6933540a64eb5529459ec3c33ccedf98d2c6997e
source: W. S. Robinson (1950), "Ecological Correlations and the Behavior of Individuals", American Sociological Review 15(3):351–357. DOI https://doi.org/10.2307/2087176
original_scan: https://www.stats.uwo.ca/faculty/aim/2015/9938/articles/Robinson1950AmericanSociologicalReview.pdf
evidence_scope: independent algebraic derivation of the relationship recorded in the prior direct-reading note, using the author's printed p.355–356 formula. No fresh source pages read in this run; no 1930 census reconstruction.
status: COMPLETE (algebraic derivation under explicitly defined population weighting); original empirical replication NOT_RUN
ci_status: NOT_RUN
billing_checked: no paid service invoked; account billing NOT_VERIFIED

## Exact derivation and necessary interpretation

Let G be the grouping variable, X and Y finite-variance individual measurements with strictly positive total standard deviations. Let m_X(G)=E[X|G], m_Y(G)=E[Y|G], u=X-m_X(G), v=Y-m_Y(G). Expectations are over individuals, so group means are weighted by group population shares. Assume positive between-group variances and positive residual variances to define all correlations below.

The law of total covariance gives Cov(X,Y)=Cov(m_X,m_Y)+E[Cov(X,Y|G)]=Cov(m_X,m_Y)+Cov(u,v). The law of total variance gives Var(X)=Var(m_X)+Var(u) and likewise for Y.

Define eta_X=sd(m_X)/sd(X), eta_Y=sd(m_Y)/sd(Y); r=Corr(X,Y), r_e=Corr(m_X,m_Y) with population group weights, and r_w=Corr(u,v) on pooled person-level residuals. Then

r = eta_X eta_Y r_e + sqrt(1-eta_X^2) sqrt(1-eta_Y^2) r_w.

Consequently

r_e = [r - sqrt(1-eta_X^2) sqrt(1-eta_Y^2) r_w] / (eta_X eta_Y).

This reproduces the coefficient structure recorded from Robinson's p.355–356 equation: k1=1/(eta_X eta_Y), k2=sqrt(1-eta_X^2)sqrt(1-eta_Y^2)/(eta_X eta_Y). It is an algebraic identity for these definitions, not an empirical or causal law. It does not license replacing r_w with an unweighted arithmetic mean of group-specific Pearson correlations: groups with different residual variances and sizes contribute different covariance mass. Nor does it license replacing the population-weighted r_e with the ordinary equal-group ecological Pearson correlation when group sizes differ. If eta_X or eta_Y is zero, the displayed division is undefined. If residual variance is zero, r_w is undefined, although the undivided covariance decomposition remains valid.

## Exact check against TH221 constructed worlds

TH221 has two equally sized groups, X and Y marginal rates (0.4,0.4) and (0.6,0.6). Each binary variable has pooled mean 0.5 and variance 0.25; between-group variance is 0.01. Hence eta_X=eta_Y=0.2, eta_X eta_Y=0.04, residual variance for each is 0.24, and sqrt(1-eta_X^2)sqrt(1-eta_Y^2)=0.96.

World P: pooled individual r=1, residual r_w=1. Identity yields r_e=(1-0.96)/0.04=1.

World N: pooled individual r=-0.6. Between covariance 0.01; total covariance=-0.15; residual covariance=-0.16, hence r_w=-0.16/0.24=-2/3. Identity yields r_e=[-0.6-0.96*(-2/3)]/0.04=1.

The same r_e=1 and eta values therefore coexist with different r and r_w. Aggregate group means alone identify neither r_w nor r. The identity does not solve ecological nonidentification without information on within-group covariance.

## Scope, competing explanations and unresolved evidence

This algebra checks an omitted derivation for the stated weighting conventions. It does not independently establish that Robinson's historical notation used precisely these modern definitions in every empirical table; that requires further primary textual and census-method examination. The derivation is consistent with the printed coefficient form. Group-level context effects, compositional sorting and individual selection remain competing causal explanations; correlation decomposition cannot separate them.

No real participant data, private data, model fitting, R-track scoring, historical causal estimate or predictive test was used. C011 (2026-11-03) and D003 (2026-W45, completed 2026-11-02) remain prior registered outputs, not repeated in this note. R073 and PESEN v0.1 remain frozen; R E1/E2/E3 and MARKET evidence classes unchanged.

Next: inspect original wording of Robinson's r_w weighting and later ecological inference identification restrictions; then rotate disciplines. No new TH number.
