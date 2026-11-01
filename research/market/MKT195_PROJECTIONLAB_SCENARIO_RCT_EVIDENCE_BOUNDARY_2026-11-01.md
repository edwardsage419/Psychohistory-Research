# MKT195: ProjectionLab scenario mechanics and direct human evidence boundary for personalized projections

track: market
subflow: commercial product and method evidence
run_date: 2026-11-01 UTC
target_key: (market,ProjectionLab+Zhu2024,official-2026-08-and-RCT-2023-10,real-product-scenario-mechanism-versus-verified-decision-improvement)
baseline_main: 1bf50f76432e1cfd9c92c8aa4306a9f1e3c904b9
status: COMPLETE_DOCUMENTARY; PRODUCT_RUNTIME_NOT_RUN; PRODUCT_SPECIFIC_RCT_NOT_FOUND
evidence: MARKET-E1 official documentation; MARKET-E2-ADJACENT peer-reviewed randomized intervention, not a ProjectionLab trial; MARKET-E3-PROJECTIONLAB NOT_VERIFIED
read_scope: NONBLIND, official English web documents and full open-access journal text, prior MKT174 and MKT175 read for deduplication
paid_actions: NONE; private_user_data: NONE; new_API_accounts: NONE; ci: NOT_RUN; actual_billing: NOT_VERIFIED

## 1. Product input, state, algorithm, goal and feedback

ProjectionLab official public pages describe a financial life-course planner. Users specify balances, asset and liability types, income and expenses, time-dependent events, investment growth/dividend and inflation assumptions, milestones and a plan's financial goals. The Plan tab computes a single annualized trajectory using fixed assumed growth rates; other non-Monte-Carlo tabs use this Plan path. Chance of Success uses the same plan inputs but varies returns, dividends and inflation across historical or randomized trials. It reports scenario success categories and permits per-trial return-sequence inspection. The 2026-08-18 Plan versus Chance of Success help article explicitly distinguishes the two outputs. Account-level growth rates and user-defined historical sequences are documented separately. Users can customize success/failure categories and thresholds, and random-start/random-restart modes can increase trial counts to 2,000; fixed historical no-looping does not allow arbitrary repetition of a fixed sequence.

The model state is financial, with year-by-year cash flows and projected balances. The product offers user-controlled assumptions, what-if changes, milestones and progress overlay; these are planning and feedback tools. Actual production simulation source, joint return/inflation distribution, full calibration, selection effects and decision-policy learning were not inspected. The product's probability is conditional on its chosen assumptions and success definition, not a validated probability that a user's life choices improve.

Pricing read 2026-11-01: Basic USD 0/year lists planning, Monte Carlo and historical backtesting; Premium USD 129/year adds multiple plans, compare mode, advanced tax and cash-flow features; Pro USD 549/year is advisor-focused. No registration or use. Security page updated 2026-08-12 states Google Cloud/Firebase and Firestore storage, transport and at-rest encryption, MFA, export and account deletion. Vendor notes cloud-provider SOC certifications do not certify ProjectionLab itself. No bank linkage is required. The vendor's claims about access controls, deletion and security were not independently tested.

Official sources:
https://projectionlab.com/
https://projectionlab.com/help/plan-vs-chance-of-success (2026-08-18)
https://projectionlab.com/help/model-investment-growth (2023-01-22)
https://projectionlab.com/monte-carlo
https://projectionlab.com/help/increase-trials-in-chance-of-success (2025-04-11)
https://projectionlab.com/pricing (accessed 2026-11-01)
https://projectionlab.com/security (updated 2026-08-12)
https://projectionlab.com/help/data-security (2023-06-09)

## 2. Independent human randomized study, carefully scoped

Zhu, Alex Yue Feng (2024), "Upgrading financial education by adding Python-based personalized financial projection: A randomized control trial," British Journal of Educational Technology 55(2):731-750. First published 2023-10-12. DOI 10.1111/bjet.13401. Full open-access article directly read:
https://bera-journals.onlinelibrary.wiley.com/doi/full/10.1111/bjet.13401

This is an independent study of a separately developed Python-based financial projection intervention, **not** a study of ProjectionLab. The study recruited Hong Kong university administrative staff aged 18 to 35 with stable earnings, excluding finance/computer-science degree holders, prior formal financial-course takers and existing Python coders. The descriptive table reports 44 experimental and 17 control participants, total 61. Both groups received a two-hour standardized financial education course; the experimental group additionally received seven hours of Python and projection training (total nine hours). Thus treatment assignment changes simulation/code exposure and contact/training time together; the randomized contrast cannot isolate the simulation's interface, algorithm transparency or extra instructional hours.

The study uses two waves (pretest and immediate post-test). Its primary financial-planning outcome is one four-point self-report item about ease of financial planning, not verified savings, debt repayment, retirement adequacy, prediction calibration or longitudinal welfare. Temporal discounting uses hypothetical reward choices. The paper reports a standardized post-test financial-planning coefficient beta=0.19 with covariate controls (p<0.05), and a positive financial-attitude coefficient beta=0.21 (p<0.05). The author's mediation analysis suggests financial attitudes mediate the self-reported outcome, but the paper explicitly notes two-wave mediator/outcome associations are cross-sectional and sample size restricts structural controls. The published data-availability statement says participant data are available from the author on reasonable request; no participant-level replication was run.

The experiment supports a bounded possibility that interactive transparent projections with additional instruction can change near-term reported attitudes/planning in this recruited population. It does not establish a durable change in objective financial behavior, an isolated effect of algorithm transparency, or any effect of ProjectionLab's software. The published comparisons with an older masked-code study are across distinct studies, not a direct randomized arm comparison of the two interfaces in this RCT.

## 3. Deduplication and next evidence gate

MKT174 already investigated structural model misspecification versus Monte Carlo precision; MKT175 already investigated temporal holdout and Brier scoring with synthetic data. This MKT195 adds actual peer-reviewed human intervention evidence, its explicit design and measurement limits, and an updated official product mechanism/cost/privacy check. No additional artificial Monte Carlo experiment was made.

Candidate future independent evaluation: freeze an objectively measurable savings or debt outcome, record model input and forecast timestamp, randomize interactive scenario exposure with **equal training/contact time**, use long-term follow-up and attrition analysis, separately score prediction calibration, real financial outcomes, time cost and autonomy. For product-specific efficacy, require ProjectionLab user-level randomized or prospective observational data with a defensible comparison group and independent outcome confirmation. No product development is authorized.

MARKET-E0: vendor claims of better confidence and decisions, unverified.
MARKET-E1: official documented functionality, price, privacy/security statements; source code/runtime not independently validated.
MARKET-E2-ADJACENT: published RCT of a different Python projection intervention; direct product effect NOT_ESTABLISHED.
MARKET-E3: independent long-term net-welfare/decision improvement for ProjectionLab NOT_FOUND.
R E1/E2/E3: N/A.

next_action: seek independently measured behavioral savings or debt outcomes in personalized projection RCTs; audit intervention contact-time balance and follow-up. Do not duplicate MKT174/175 simulation work.
