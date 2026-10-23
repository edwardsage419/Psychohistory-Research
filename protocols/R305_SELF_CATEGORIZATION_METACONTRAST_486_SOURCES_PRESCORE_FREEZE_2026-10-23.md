# R305 prospective source-first protocol: context-sensitive self-categorization and comparative/normative fit

2026-10-23 Asia/Taipei. Original239 **03-004 Self Categorization Theory**, P1. This exact protocol must be COMMITTED BEFORE R305 source/score/outputs. Research grade **E1 project-invented finite numerical illustration**, no new real human or animal E2 and no historical E3. R073/PESEN v0.1 untouched; do not begin taxonomy/model fusion before all R models studied.

## Research lineage and strictly different 03-003

Turner, J.C. (1985), *Social categorization and the self-concept: A social cognitive theory of group behavior*, *Advances in Group Processes*, vol.2, pp.77–122 (bibliographic listing at [Harvard](https://inclusionandbelongingtaskforce.harvard.edu/publications/social-categorization-and-self-concept-social-cognitive-theory-group-behavior)). Turner, Hogg, Oakes, Reicher & Wetherell (1987), *Rediscovering the Social Group: A Self-Categorization Theory*, Blackwell, especially Turner chapter **A self-categorization theory** pp.42–67. Turner, Oakes, Haslam & McGarty (1994), *Self and Collective: Cognition and Social Context*, *Personality and Social Psychology Bulletin* 20(5), DOI https://doi.org/10.1177/0146167294205002. First-person SCT argument: personal vs social levels of categorization are context sensitive, group prototypes and comparative fit depend on the comparison set, normative fit and perceiver readiness are additionally relevant. General explanation in *Oxford Research Encyclopedia* [Social Categorization](https://academic.oup.com/edited-volume/62246/chapter/550943429), but its explanatory numerical examples are not taken as an author's fitted parameter model.

Prior R304 03-003 Tajfel1971 Social Identity Theory studied a **newly invented allocation utility** between recipients and ingroup favoritism, **NOT self-categorization cognition**. R305 uses no monetary allocations, discrimination outcomes, imitative actions, R063 Najar data or human experiments. The invented ranking below is **our project-defined operational example**, not Turner's 1985 equation, subject classification dataset, human level switching effect sizes or SCT validation.

## Synthetic four-stimulus world and comparative fit

Four synthetic objects i=0,1,2,3 with two externally defined valid category partitions:
- Candidate P labels=(0,0,1,1), within-pairs (0,1) and (2,3).
- Candidate Q labels=(0,1,0,1), within-pairs (0,2) and (1,3).
They are *competing possible categorizations* of the same objects; no underlying objectively true category labels.

Two focal comparison dimensions X=(0,1,4,5) and Y=(0,4,1,5), plus a MID context which is their arithmetic mean M=(0,5/2,5/2,5). Exactly THREE possible contexts {X,MID,Y}, not sampled data. In each context all same objects represented with the stated feature values. For candidate partition C, define mean within-category absolute pairwise distance W_C across exactly two within pairs (one per cluster) and mean between-category absolute pairwise distance B_C across all 4 cross-cluster pairs; **invented operational metacontrast score** MC_C=B_C/W_C. Every frozen world has W_C>0, so no zero denominator or smoothing rules. This is one mathematically precise version of comparative fit, but not the original author's parameter estimation or claimed psychological algorithm.

Analytic frozen values:
- Context X: P W=1, B=4 => MC=4; Q W=4, B=5/2 => MC=5/8.
- Context MID: P W=5/2, B=5/2 => MC=1; Q same 1.
- Context Y: P W=4, B=5/2 => MC=5/8; Q W=1, B=4 => MC=4.
This context-specific comparative fit **reverses the preferred partition** when X vs Y used, holding category labels fixed.

## Invented readiness, normative fit, and personal baseline

Perceiver readiness r∈{0,1/2,1}; normative fit n_P,n_Q each ∈{0,1/2,1}; **personal-identity competing baseline threshold** t∈{0,1,2}. For partition C compute invented **social-category salience score** S_C=r*n_C*MC_C, and personal baseline score S_personal=t. Choose P only when S_P strictly greater than both S_Q and t; choose Q only when S_Q strictly greater than both S_P and t; otherwise choose PERSONAL. Ties between P and Q choose PERSONAL too, deliberately conservative. No "universal human identity" level is implemented, and the psychological interpretation of readiness/normative fit is hypothetical.

This ranking directly encodes the SCT-level conceptual distinction. No actual observer's self perception is measured and no empirical recognition accuracy or bias is assessed. All values are exact rational arithmetic; no seeded simulation, fitted free parameters or independent participants.

Full source universe **3 contexts ×3 readiness values ×3 P-normative ×3 Q-normative ×3 personal-threshold levels =243 artificial decision worlds**, each with precisely 2 labeled candidate partition source rows **486 complete original synthetic source rows**, all 2-cluster member indices/within and across pair sets/marginal scores included. Every source row records context, four feature values, candidate category, pair means, MC ratio, r,n_P,n_Q,personal baseline, candidate score, competing candidate score, choice, whether the particular social category wins and whether personal identity wins. This is not 486 real people or 486 independent time series.

## Frozen negative/positive controls and scientific limits

- Context X r=nP=nQ=1, t=1 => P score4, Q5/8, personal1 => P; context Y with same inputs => Q. Swap context but don't swap P and Q names: **cross-context category reversal** is exact.
- MID r=nP=nQ=1 and t=1 => both social scores1 equal personal1 => PERSONAL, so strong social categorization is not a theorem from mere group labels.
- For context X r=1,nP=0,nQ=1,t=0 => P0,Q5/8,personal0 => Q, despite larger X comparative fit for P. **Normative gate is distinct**.
- With r=0 and any fixed context, norm and threshold, all social scores0 and choose PERSONAL; with both n=0 choose PERSONAL, regardless of context. Changing the physical comparative context cannot cause a social self classification under readiness0.
- In X context P and Q exact known MC values, independent of readiness/norms/threshold; in Y swap ratio pair. MID both MC1.
- For each category partition, both within and between pair counts fixed and all source membership/row pair indices must be audited independently.
- The numeric factor product, personal baseline, and tie rule are **project assumptions**, not validated Turner theory. Pairwise distances of 4 artificial numerical objects don't identify social motives, norms, group identity, collective action or chronology. **No E2/E3**.

## Completion gates

Executable native Python >=3.11 with --test, --emit. Generate all original 486 labeled source rows CSV, complete 243-world source/choice JSON, SHA256 receipt. Independent auditor must not import production code, independently derive within/across pair sets from the two label vectors, calculate all ratio values using Fraction and audit all 486 source rows, full JSON, SHA and adversarial alterations/missing rows/negative controls. GitHub Actions **two interpreter jobs and independent archive job all completed/success**, then commit original artifacts to main. Only after these passes write formal bounded E1 report and acceptance, update crosswalk v1.9 with **one changed row 03-004**; previous R304 social identity row 03-003 and early R063 remain untouched. Expected primary192→193, pending44→43 (P1 17→16), all 239 canonical candidate entries preserved. R073/PESEN frozen; original theory empirical acceptance still open.
