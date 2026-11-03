# TH221 Robinson (1950): ecological correlation and cross-level nonidentification

track: theory
subflow: primary theory
run_date: 2026-11-03 (Asia/Singapore)
observed_head_before_write: 35c4379cf7eb088799948740c7b7bf79e9b2e369
source: W. S. Robinson (1950), "Ecological Correlations and the Behavior of Individuals", *American Sociological Review* 15(3), 351–357. DOI: https://doi.org/10.2307/2087176
open scan read: https://www.stats.uwo.ca/faculty/aim/2015/9938/articles/Robinson1950AmericanSociologicalReview.pdf
evidence_scope: direct reading of printed pp.351–357 in university-hosted original journal scan, including Tables 1–3, equations (1)–(3) and conclusion. This is the original article, not a new empirical replication. Original 1930 census source tables were not independently retrieved.
status: COMPLETE (bounded original reading and constructed counterexample); empirical replication NOT_RUN; original omitted algebraic derivation NOT_RUN
ci_status: NOT_RUN
billing_checked: no paid service invoked; account billing NOT_VERIFIED

## Source-specific findings

1. Printed pp.351–354 distinguish correlation across persons from correlation across geographic units. The ecological statistic depends on group marginal rates; individual association depends on within-group joint cell counts. Identical group marginals can correspond to different individual associations.
2. Printed pp.353–354 report 1930 US Census population age 10+: race and illiteracy individual r=.203, ecological r=.946 for nine divisions and .773 for 48 states. Nativity and illiteracy individual r=.118, ecological r=−.619 for divisions and −.526 for states. These are Robinson's historical calculations, not independently verified numbers. Period-specific racial categories and language reflect the original census and are not adopted as current analytical categories.
3. Printed pp.355–356 give r_e=k1*r−k2*r_w, with k1=1/(eta_XA eta_YA), k2=sqrt(1−eta_XA²)sqrt(1−eta_YA²)/(eta_XA eta_YA). The author describes r_e as a population-weighted correlation for the algebra and reports a near-equal unweighted numerical example (.944 versus .946). The article expressly omits the derivation due to space (footnote 19). The precise weighting/within-group standardization assumptions require separate derivation before implementing this identity.
4. Printed p.357 concludes ecological correlations generally cannot substitute for individual correlations. This is a cross-level inference limitation, not a statement that group-level associations are intrinsically useless for group-level questions.

## New constructive identification counterexample (original arithmetic, not a historical observation)

Two equal-size areas each have 100 people. In area A, X=1 for 40 and Y=1 for 40. In area B, X=1 for 60 and Y=1 for 60. The area-level rates are (0.4,0.4) and (0.6,0.6), giving ecological Pearson r=+1 in both worlds.

World P: joint X=Y=1 counts are 40 in A and 60 in B. Everyone has X=Y, so pooled individual phi=+1.

World N: joint X=Y=1 counts are 0 in A and 20 in B. In A the four cells (X1Y1,X1Y0,X0Y1,X0Y0) are (0,40,40,20). In B they are (20,40,40,0). Pooled cells are (20,80,80,20), yielding phi=(20*20−80*80)/(100*100)=−0.6.

Both worlds have identical group marginals, equal group sizes and ecological r=+1. Their individual associations have opposite signs. All counts are nonnegative and exactly satisfy the marginals. This establishes nonidentification from the specified aggregate observations, not empirical prevalence or a causal effect.

## Competing explanations, scope and measurement

A strong area-level association could reflect composition, within-area relationships, between-area contextual effects, confounding or mixtures. The paper's warning concerns using aggregate correlation to answer an individual-level question. The opposite inference, from individuals to institutional/historical group effects, also requires an explicit cross-level model and independent evidence.

Individual-level cross-tabulations or suitable linked microdata can discriminate the constructed worlds. Observing only group rates cannot. Even observing microdata does not by itself identify causal effects without design assumptions. A future historical comparison must state the period, population, group boundaries, measurement invariance and data provenance. No private personal data used.

This complements the existing theory archive as a cross-level measurement and inference issue. It is not an R-track model fit, C-track daily output, D-track weekly output, project-wide synthesis or product implementation.

## Unread / open

The underlying 1930 Census original tables, the author's separate unpublished covariance derivation, and later competing ecological-inference models remain unread. No new numerical R evaluation, human experiment, historical causal estimation, or prediction has been run.
