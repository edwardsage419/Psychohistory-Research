# MKT199: TRIPPA secondary sedentary outcomes and financial incentive persistence evidence

track: market
subflow: commercial product evidence and cross-outcome effectiveness
run_date_utc: 2026-11-01T12:24Z
target_key: (market,FitbitZip_TRIPPA2016_secondary2018_plus_financial_incentive_review2025,2016+2018+2025,objective_sedentary_outcomes_and_post_withdrawal_persistence)
baseline_main: ee199bc8e030a3f44daa4071576fa44c72fcf1d0
status: COMPLETE_BOUNDED_DOCUMENTARY
evidence: MARKET-E2_SAME_TRIPPA_RCT_SECONDARY_OUTCOME; MARKET-E2_EXTERNAL_SYSTEMATIC_REVIEW; MARKET-E3_LONG_TERM_NET_WELFARE_NOT_VERIFIED
read_scope: NONBLIND; English 2018 open full-text secondary paper, 2016 PubMed original abstract, 2025 PubMed systematic review abstract, 2016 historical registry mirror description. Original trial paid full text, registry historical versions and participant-level data NOT_READ.
product_runtime: NOT_RUN
independent_data_reanalysis: NOT_RUN
new_R_E2_E3: 0
ci: NOT_RUN
billing_checked: NOT_VERIFIED
paid_actions: NONE

## 1. Question and previous work

MKT198 already documented the TRIPPA 2016 800-person randomized four-arm Fitbit Zip trial. Its primary outcome was objectively measured moderate-to-vigorous physical activity (MVPA) bouts. The previous report identified no improvement in measured weight or blood pressure and a lack of persistence for the cash-incentive advantage after withdrawal. This pass asks whether increased step or MVPA behavior also reduced objectively measured sedentary time and whether other RCT evidence suggests post-withdrawal persistence. No new 2016 trial is claimed.

## 2. Directly read new TRIPPA secondary publication

Sloan RA et al. (2018), BMC Research Notes 11:189, DOI 10.1186/s13104-018-3306-9, PMCID PMC5863802, full text https://pmc.ncbi.nlm.nih.gov/articles/PMC5863802/ .

This is a SECONDARY ANALYSIS OF THE SAME TRIPPA RANDOMIZED COHORT, not an independent 800-person replication. Four original groups: control 201, Fitbit 203, Fitbit plus charity 199, Fitbit plus cash 197. Independent sealed ActiGraph GT-3x+ accelerometers at baseline, month 6 and month 12. Objective outcomes: daily sedentary time (ST) as percentage of accelerometer wear time, and prolonged sedentary bouts (PSB) of 30 minutes or more. At least four valid days including one weekend day were required; authors used mixed models adjusted for age, gender and ethnicity, and assumed missing at random for likelihood-based analyses.

Main finding: no statistically significant between-group differences in changes in objective ST or PSB at either month 6 or month 12. In the control group, adjusted ST rose from 70.96% baseline to 72.05% at month 6 and 71.99% at month 12. The Fitbit group showed 70.88%, 71.38%, 70.91%; charity 70.42%, 71.78%, 71.51%; cash 70.75%, 70.74%, 70.64%. These within-group descriptive means do not establish significant treatment effects. The authors also found that within-person step increases were associated with reduced ST/PSB, which is observational and does not identify the intervention's causal effect on those outcomes.

At 12 months, valid accelerometer retention ranged from 73.9% to 81.1% by group. Missing-at-random assumptions and adherence differences limit inference. The secondary paper explicitly notes that original self-reported sitting improvements with cash incentives were not replicated in objectively measured sedentary time. This is a useful negative objective outcome, not proof that all physical activity or health outcomes are zero.

Product implication: a tracker can change its targeted activity measure while failing to change a nearby objective downstream measure. For future research, preserve the distinction between target attainment, measured activity, sedentary behavior, health, time and money costs, and participant-defined welfare. Do not assign universal weights.

## 3. External synthesis on incentive withdrawal

Salmani B et al. (2025), Preventive Medicine 192:108237, DOI 10.1016/j.ypmed.2025.108237, PMID 39870214, https://pubmed.ncbi.nlm.nih.gov/39870214/ . Read accessible English abstract, NOT the complete primary study set.

Review covers 29 studies (21 RCTs and 8 pilot RCTs), total 9,604 participants, studies published from 2018-06-01 to 2024-03-31. Median financial incentive about USD 1.19 per day. Among 21 main trials, 17 reported positive short-term effects; among follow-up studies, 3 of 8 reported positive effects. The step-count meta-analysis reported short-term standardized mean difference SMD 0.52, 95% CI 0.25 to 0.78, and post-withdrawal SMD 0.20, 95% CI 0.01 to 0.40, p=0.04. Only one long-term study reported step count, preventing a pooled long-term estimate. Moderator findings are exploratory across heterogeneous studies.

This pooled small follow-up benefit and the particular TRIPPA cash arm's nonsignificant 12-month comparison can coexist because interventions, populations, outcomes and timing differ. The review includes studies after 2018, so do not assume the 2016 TRIPPA trial is part of its sample. No direct evidence here demonstrates general life decision quality or long-term net welfare.

## 4. Registration and prespecification check

The original TRIPPA 2016 article cites NCT01855776. The historical registry mirror https://ichgcp.net/clinical-trials-registry/NCT01855776 describes a 12-month four-arm randomized study with 6 months of incentives followed by withdrawal, objective MVPA bouts assessed at baseline, 6 and 12 months, and cost-effectiveness objectives. This is consistent at a broad design level with the published abstract. The official ClinicalTrials.gov HTML viewer and historical registration version details were not readable in this run. Consequently, primary-outcome registration timing, exact outcome hierarchy, changes to outcomes, and cost-effectiveness reporting remain NOT_VERIFIED. Do not claim a completed preregistration discrepancy audit.

## 5. Product, privacy, costs, evidence limits

Historical product was Fitbit Zip, used with study-specified external cash/charity rewards. Data input: device step counts plus sealed research accelerometer data. State: weekly step goals and trial-group allocation. Feedback: activity tracking and reward eligibility. Outcome algorithm: objective MVPA/ST/PSB analysis documented in papers; contemporary Fitbit AI coach is outside this trial. No paid product was used. Contemporary pricing, data retention and algorithm details were addressed in MKT198 and were not rechecked because no relevant change was identified.

MARKET-E1: documented historical product and protocol mechanisms.
MARKET-E2: original TRIPPA randomized cohort, its 2018 secondary outcome analysis (same sample, no independent replication), and a separate 2025 systematic review of other incentive studies.
MARKET-E3: lasting cross-domain decision improvements and net personal welfare NOT_VERIFIED.
R E1/E2/E3: N/A. This is market evidence, not an R-series scientific acceptance upgrade.

F overlap: objective-vs-self-report outcome divergence matters for transparency and appeal in high-stakes behavior tracking. Existing weekly F009 already completed. No new F phase, personal health data, synthetic security experiment or safety deployment.

## 6. Coordination, costs and next action

Read main and recent R/theory commits, R127 itemwise audit, E166, R333-R340 candidate gate report and R handoff, F009 phase56, and Codex PR #1/#3. R127 05-003 gained independent full-byte bounded E1 verification but original protocol deviation still awaits itemwise disposition. R333-R340 mandatory production gate and complete 16-child native checkout remain NOT_RUN/PARTIAL as of inspected R report. PR #1/#3 open draft and unmerged. No new E audit or F phase needed today. Crosswalk/pending queue unchanged in latest five-commit diff relative to MKT198 HEAD. No Actions invoked; billing not independently verified.

Next market research: seek a randomized study of an actual planning/decision-support product with objective downstream outcomes, equal-attention comparison and withdrawal follow-up; alternatively investigate a direct real-world failure or calibration audit of ProjectionLab/Exist/Beeminder. Next E: follow mandatory R333-R340 gate integration and R127 05-003 protocol deviation, do not duplicate B mathematics. Preserve R073 and PESEN v0.1 freezes.

Sources accessed 2026-11-01:
https://pmc.ncbi.nlm.nih.gov/articles/PMC5863802/
https://pubmed.ncbi.nlm.nih.gov/27717766/
https://pubmed.ncbi.nlm.nih.gov/39870214/
https://ichgcp.net/clinical-trials-registry/NCT01855776
