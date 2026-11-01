# MKT201: Retirement calculator RCT, administrative contribution elections, and ITT versus tool-user effects

track: market
subflow: real decision-support effectiveness evidence
run_date_utc: 2026-11-01T14:24Z
target_key: (market,Goda-Levy-Manchester-Sojourner-Tasoff-Xiao-retirement-calculator,IZA-DP15758-2022-working-paper-v1,administrative-outcome-source-TOT-ITT-adoption-and-followup)
baseline_main: a11f866a0683ccf7159248e1a6eae41380146a40
status: COMPLETE_BOUNDED_ORIGINAL_FULL_TEXT_READING
evidence: MARKET-E2_ADJACENT_RANDOMIZED_INTERVENTION_WITH_ADMINISTRATIVE_ELECTION_OUTCOME
product_specific_effectiveness: NOT_VERIFIED
participant_level_reanalysis: NOT_RUN
registered_plan_comparison: NOT_RUN
production_product_runtime: NOT_RUN
R_E2_E3_new: 0
ci: NOT_RUN
billing_checked: NOT_VERIFIED
paid_actions: NONE
personal_sensitive_data: NONE

## 1. Distinct increment and source version

MKT200 had inspected the official abstract and explicitly left the USD 174 outcome's source and followup unresolved. This pass reads the original full text and appendix of the freely available 2022 IZA working paper (68-page version), rather than creating a second study count.

Primary full text: https://repec.iza.org/dp15758.pdf (IZA Discussion Paper 15758, November 2022), especially pp. 2-8, 14-18 and online Appendix A, Table A.4.
Institutional publication metadata: https://research.upjohn.org/up_workingpapers/378/ ; published journal article DOI https://doi.org/10.1016/j.jebo.2023.08.001 .
Preregistration identifier named in the working paper: AEARCTR-0002129; registry contents and version comparison NOT_READ.
The journal article's final full text was not compared line by line with this earlier working paper. Numerical statements below are attributed to the IZA version.

## 2. Real intervention and data input

Setting: US Office of Personnel Management employees with federal Thrift Savings Plan (TSP), an employer retirement saving plan. In December 2017, **5,426** employees were randomly assigned with equal probability to full projection or active control. **2,625 (48%)** used the assigned tool. Randomization was stratified by survey participation and baseline variables. This is one randomized experiment, with an active control that received a meaningful calculator.

User-entered inputs included date of birth, federal start date, salary, expected retirement age, desired retirement income lifestyle as 70%, 85%, 100% or 115% of current salary, TSP balance and contributions, pension and Social Security expectations. Both tools displayed a retirement income target. Full tool incorporated TSP accumulated savings and future contributions into projected retirement income, showed the target gap, and allowed real-time contribution-slider counterfactuals. Active control displayed pension and Social Security projections but required users to assess their TSP income themselves. Both gave TSP contribution-change instructions; no automatic account change is established.

The paper states a formula in Appendix G. Default income growth 3%, inflation 2%; randomized default nominal investment return 5% versus 8% and retirement lifestyle 85% versus 100%, with user override. Those randomized defaults had insignificant estimated effects in the reported appendix. The exact tool software implementation and current commercial pricing are not published as a supported commercial product. This is a research intervention, not ProjectionLab.

## 3. Outcome measurement newly verified

The authors explicitly state that the outcome data came from **administrative HR records** of monthly TSP **contribution elections**, with employee characteristics, covering **August 2014 through April 2018**. They link records to tool participation and an earlier voluntary survey. The main tool-user sample has 2,625 employees and 152,198 individual-month records across the panel; the reported main regression uses 151,732 observations. The separate survey includes 1,435 responders. The 2017-12-01 rollout leaves roughly four months of post-intervention records through April 2018.

This closes MKT200's uncertainty about whether the study relied only on self-reported *intended* saving: the outcome is an employer administrative record of contribution **elections**. The text read does not separately establish actual cash deposits or retirement account balances realized years later. Do not rephrase administrative elections as verified lifelong savings or net welfare.

## 4. Treatment-on-treated and intention-to-treat are materially different

Working-paper Table 3 column 1, among tool users, estimates annualized contribution elections **USD +174.184**, clustered standard error **75.621**, asymptotic p **0.021**. The average dependent variable in that sample is USD 7,078.012 annually, so the effect is about 2.46% of that baseline. The paper's abstract rounds this to USD 174 and 2.3%, using a different denominator or rounding; retain both source expressions rather than silently equating them.

The result is a **tool-user treatment-on-treated (TOT)** contrast, not the assignment effect for all employees. The authors use individual, year and month fixed effects in a difference-in-differences specification, with individual-clustered standard errors. The original assignment was randomized, and both arms could use a calculator. Actual use is selected, so the tool-user estimate must retain its conditional interpretation.

Working-paper Appendix Table A.4 column 1, full invited population **intention-to-treat (ITT)**: annualized election difference **USD +61.055**, standard error **48.990**, **not statistically significant** at conventional thresholds. The paper explicitly states the main ITT effect is not significant. The experiment cannot be summarized as proving a significant average saving increase for all invited employees.

Selection and heterogeneity: tool users had higher prior TSP contributions than non-users. Greater financial literacy and education were associated with larger treatment effects. These subgroup results need multiple-testing and survey-response caution; 1,435 of 5,426 completed the pre-survey, and the survey sample differed on observed demographics. No causal proof that a specific individual's financial literacy level determines benefit is established.

## 5. Decision improvement, limitations, and privacy

This study directly measures an administratively recorded contribution **election**, closer to actual behavior than an attitude survey or a hypothetical repayment allocation. It still does not establish long-run retirement adequacy, debt displacement, consumption sacrifices, income shocks, calibrated future returns, net welfare, independent decision skill after tool removal, or transfer to non-financial life decisions. The followup window is short and confined to federal employees with TSP benefits.

Privacy boundary: the research linked sensitive HR financial contribution records with survey and participation data under institutional research protocols. No personal-level data were accessed in this market review. A future product would need local-first/minimal-input options, explicit data access and revocation, independent measurement provenance, and user-controlled final choices. These are candidate controls, not tested features of the research tool.

MARKET evidence scope: E2 for an adjacent randomized intervention with administrative contribution-election outcomes; E1 for the paper's documented mechanism, with production implementation uninspected; product-specific commercial effectiveness and long-term welfare NOT_VERIFIED. This is not R-series E2 or E3, and no model validation, code test, paid service or real personal-data access was performed.

## 6. Coordination snapshot, no duplicate E/F expansion

Read project workflow docs, MKT200, E166, F009 phase56, latest R and theory handoffs, live main and all open Codex PRs. At the pre-write HEAD, 12 open PRs were all Draft and unmerged. PR #1 and #3 address R257 S53; PR #3 was 1 commit ahead of its merge base and **1,075** commits behind current main in a compare from PR #3 head to main. This is review drift, not a proven merge conflict.

Since MKT200, R/B committed an additional **16-file historical claim identity gate** for R333 through R340, with 13 synthetic controls and 16 remote JSON blob checks reported in research/validation/R333_R340_P0_HISTORICAL_CLAIMS_STRICT_GATE_2026-11-01.md. E directly read its source and R report. It checks historical claim identities separately from the existing mathematical entrypoint. The R report explicitly states full real-checkout Node native execution NOT_RUN, complete Python 16-child native execution NOT_RUN, and mandatory composite caller adoption NOT_ESTABLISHED. Original optimized-mode false-accept P0 stays OPEN; no new E validator or B math recheck was created here. Prior original239 crosswalk and 154-item queue blobs remained unchanged across the six commits since MKT200; no closure is inferred.

F009 W44 phase56 is already COMPLETE_BOUNDED. No new independent security incident or new weekly F test was established. Relevant privacy and autonomy implications are recorded above without generating an artificial phase.

No Actions dispatched, no paid product registration, no API, no GPU/cloud or personal data. Actual GitHub billing/free quota NOT_VERIFIED. Existing R073 and PESEN v0.1 frozen status unchanged.

## 7. Next research and governance gates

1. Read preregistration AEARCTR-0002129 and compare outcomes, exclusions, analysis timing and subgroup plans with the IZA working paper and the published 2023 version. Avoid treating multiple versions as independent trials.
2. Seek an independent longer-followup administrative savings or debt outcome from a real decision-support deployment with an ITT denominator and welfare/cost measurement.
3. E/R owner review: execute both R333-R340 real-checkout identity and mathematical gates, authenticate the composite caller and make failure propagation mandatory before closing P0. Keep PR #3 source binding and prescore ordering separate.
