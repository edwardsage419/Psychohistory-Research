# MKT202: Retirement projection RCT preregistration claims and heterogeneity evidence boundary

track: market
subflow: decision-support effectiveness and independent outcome validity
run_date_utc: 2026-11-01
target_key: (market,Goda-Levy-Manchester-Sojourner-Tasoff-Xiao-retirement-calculator,IZA-DP15758-2022-v1,preregistration-heterogeneity-ITT-TOT-exploratory-factor-distinction)
baseline_main: 8168366e47e727f7077da91c642b4ac3d17806c1
status: COMPLETE_BOUNDED_AUTHOR_PAPER_COMPARISON
registry_primary_version_comparison: BLOCKED_HTTP_403
evidence: MARKET-E2_ADJACENT_RANDOMIZED_TRIAL_REPORTED_RESULTS; MARKET-E1_AUTHOR_DOCUMENTED_METHODS
commercial_product_specific_effect: NOT_VERIFIED
independent_registry_preanalysis_audit: NOT_RUN
participant_level_reanalysis: NOT_RUN
R_E2_E3_new: 0
ci: NOT_RUN
billing_checked: NOT_VERIFIED
paid_actions: NONE
personal_sensitive_data: NONE

## Research question and nonduplicate scope

MKT200 read institutional summaries, MKT201 established that the USD 174 effect is from administrative **contribution elections** among actual tool users, while the all-invited ITT is USD 61.055 with SE 48.990 and no conventional significance. This pass audits **which heterogeneity results the authors explicitly say were prespecified**, which were exploratory, and whether the all-invited versus user-selected estimates agree. It adds no second trial, product claim, synthetic test or new market study count.

Original open full text: Goda, Levy, Flaherty Manchester, Sojourner, Tasoff and Xiao, *Are Retirement Planning Tools Substitutes or Complements to Financial Capability?*, IZA Discussion Paper 15758, November 2022, https://repec.iza.org/dp15758.pdf . Read main paper sections 2.4.4 and 3.1–3.3, Tables 1–4, Appendix A Tables A.1–A.4 and author preregistration statement on PDF p.12. Institutional corroboration: https://www.nber.org/papers/w30723 and https://research.upjohn.org/up_workingpapers/378/ . Published version: Journal of Economic Behavior & Organization 214 (2023), 561–573, DOI 10.1016/j.jebo.2023.08.001; final journal version was not independently compared line-by-line.

The paper names AEA RCT Registry **AEARCTR-0002129**. Direct retrieval of https://www.socialscienceregistry.org/trials/2129 returned HTTP 403 in this pass. The actual registration timestamp, attachments, protocol revisions and complete original preanalysis text were therefore **NOT_READ**. The classification below is **the authors' disclosure**, not an independent registry-versus-publication concordance finding.

## Newly verified prespecified versus exploratory split

The authors explicitly state (IZA PDF p.12) that they **prespecified** heterogeneity checks for exponential-growth bias, time preferences and financial literacy. They explicitly state that the **factor analysis and regressions using the factors were not prespecified** and should be viewed as exploratory. Their PCA produced 14 factors; six with eigenvalues greater than 1 were retained; the third was interpreted as financial capability because it loads on schooling, exponential-growth bias and financial literacy. This factor is a data-derived composite, not a preregistered single individual life-utility score.

The reported prespecified financial-literacy interaction is positive in the user-selected TOT Table 3: USD **+328.038** per one standardized financial-literacy unit, SE **130.793**, two-star significance in the authors' table. The prespecified exponential-growth-bias and present-bias interactions were not significant in that table. The same financial-literacy interaction in the all-invited ITT Appendix Table A.4 is USD **+238.383**, SE **99.264**, two-star significance; Appendix text reports the associated heterogeneity test **p=0.016**. This is evidence of treatment-effect heterogeneity in a specific employee retirement-contribution election outcome. The all-invited main effect remains USD **+61.055**, SE **48.990**, nonsignificant. The two facts can coexist.

The paper's exploratory factor interaction for 'financial capability' is reported in Table 4 as positive and significant, but its exploratory status must remain attached to any citation. Neither a positive financial-literacy interaction nor the factor result establishes that a financial-literacy intervention would causally increase calculator effectiveness. Multiplicity, selected survey responders and different user uptake also constrain generalization.

## Sample selection and measurement

The study randomly invited **5,426** employees; **2,625** used the assigned calculator; **1,435** completed the pre-intervention survey. The authors report that survey completers differ from noncompleters on administrative characteristics, and that participants with higher pre-intervention Thrift Savings Plan contributions were more likely to use the calculator. The heterogeneity analyses rely on the selected survey sample and may have lower transportability to less financially capable users.

The treatment calculator let users enter retirement income targets, expected pensions, account balances and contribution assumptions, view projected defined-contribution retirement income and a goal gap, and adjust contributions through a slider. Active controls received a less complete calculator. The observed outcome is administrative **contribution elections**, not a verified realized lifetime balance, downstream debt/consumption adjustment or net welfare. Product runtime and exact projection software were not independently inspected. There is no supported commercial product price or independent product-specific RCT here.

## Evidence decision and product research implications

* MARKET-E2: one adjacent randomized experiment, administrative contribution-election outcome, authors' reported ITT/TOT and heterogeneity. It remains the same experiment already counted in MKT200/MKT201.
* MARKET-E1: documented intervention and author-reported prespecification statement. Independent registration audit BLOCKED by inaccessible primary registry; no claim of complete preregistration concordance.
* MARKET-E3: independently verified long-run welfare, multi-goal opportunity cost, durable unaided skill and named commercial-product causal benefit NOT_VERIFIED.
* R-series E1/E2/E3: no new acceptance, no frozen protocol change.

Candidate future market evaluation: report randomized assignment ITT, tool adoption, tool-user contrast, survey participation, prespecified subgroup interactions, exploratory composites, objective behavioral outcome and post-intervention welfare **separately**. If actual tool effectiveness is stratified by prior capability, check whether a low-literacy group benefits before asserting equitable assistance. These are evaluation proposals, not a deployed product design.

## E/F coordination read-only snapshot

At baseline main, read required workflow documents, MKT201, E166, F009 phase56, latest R and theory handoffs, and current open Codex PR metadata. R/B have since added `research/evidence_audit/r333_r340_composite_acceptance_20261101.py` (blob `104beae6d60e4df8e879841567ca08c4088438a4`), requiring pinned mathematical and historical-claim gates, ordinary and optimized Python, and bounded E1 output. Its own R report records 14/14 synthetic tests in normal and 14/14 in optimized mode, but authentic full-checkout execution NOT_RUN and mandatory production adoption NOT_ESTABLISHED. Original optimized false-accept P0 remains OPEN; no E-track duplicate mathematics was run. Twelve Codex PRs were open Draft and unmerged at this snapshot; PR #1 and #3 remain separate R257 S53 review issues. PR #3 versus baseline main: diverged, 1083 main-only and 1 PR-only commit, not a demonstrated merge conflict. Crosswalk blob `36f24235901172642c46853298aebb421f1a3552` and pending queue blob `3b96d46b3d88ccafd779a08509c3cfd0e435772f` unchanged; R's last direct count 154 (P0 27, P1 82, P2 45), file-level net closure zero. R073 and PESEN v0.1 remain frozen.

F009 phase56 weekly topic already completed with 81 synthetic states; no new phase, no real identity infrastructure or sensitive user data accessed. Financial-literacy uptake differences raise a future fairness/accessibility question, not a measured deployed safety failure.

No paid service, registration, data purchase, API or CI dispatch. Actual account billing and free allowance NOT_VERIFIED. Next market action: obtain a freely accessible timestamped original AEA registry plan, if possible, and check prespecified outcomes/analysis/sample restrictions; otherwise move to independent product-specific decision outcomes. Next E action: verify the composite caller's authentic checkout execution and mandatory adoption only after R/B and owner evidence, while preserving historical P0 and PR review boundaries.
