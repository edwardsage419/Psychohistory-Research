# MKT200: Decision-support RCTs, assisted choice versus unaided learning and real-world transfer

track: market
subflow: commercial product mechanism and independent effectiveness evidence
run_date_utc: 2026-11-01T13:23Z
target_key: (market,FCA-robo-debt-advice-2022+Goda-retirement-calculator-2023,original-publications-v1,assisted-decision-quality-versus-unaided-learning-and-actual-outcome-verification)
baseline_main: 2c810266c58b0c24b339263a76ae286443f23e71
status: COMPLETE_BOUNDED_DOCUMENTARY
evidence: MARKET-E2-ADJACENT_RANDOMIZED_EXPERIMENTS; MARKET-E1-EXISTING_PROJECTIONLAB_OFFICIAL_DOCS_FROM_MKT195; MARKET-E3_PRODUCT_SPECIFIC_LONG_TERM_WELFARE_NOT_VERIFIED
product_runtime: NOT_RUN
participant_data_reanalysis: NOT_RUN
new_R_E2_E3: 0
ci: NOT_RUN
billing_checked: NOT_VERIFIED
paid_actions: NONE
personal_data: NONE

## 1. Why this is a distinct increment

MKT195 evaluated ProjectionLab official financial scenario planning and an adjacent 61-person educational RCT whose outcome was near-term self-reported planning. MKT198/MKT199 evaluated the Fitbit TRIPPA trial and secondary objective outcomes. This pass asks a higher-value question: does algorithmic decision support improve a mathematically scorable choice during use, does it transfer to later unaided decisions, and is any effect on actual real-world behavior separately measured? No new security-token, witness or synthetic test was created. The two studies below use *research interventions*, not commercially validated branded products. The current ProjectionLab mechanism is only a product comparison anchor.

## 2. Direct primary source: UK FCA robo debt repayment RCT

Original institution: UK Financial Conduct Authority (FCA), Occasional Paper 61, August 2022, `Robo-Advice for Borrower Repayment Decisions`, Chak, Croxson, D'Acunto, Reuter, Rossi and Shaw. Public English primary report: https://www.fca.org.uk/publication/occasional-papers/occasional-paper-61.pdf . Read the official original PDF text, especially experiment, baseline, treatment and learning sections, and the complete FCA research explainer: https://www.fca.org.uk/publications/research-articles-fca-research/can-robo-advice-improve-borrower-repayment-decisions . NBER related version DOI 10.3386/w30616. Registry named in original: AEARCTR-0006447; registry version and participant-level data NOT_READ. The FCA explainer was published 2022-08-30, with a 2026-06-03 system-only update explicitly labelled "No content change."

Input and state: nearly 3,500 UK consumer participants faced nine **hypothetical but realistic** repayment allocations, each with 2 to 4 debts, balances, APRs, minimum repayments, penalty fees and a fixed repayment budget. Interest rates ranged from 0% to 292%. They allocated a budget to minimize fees and interest. The task was an explicit single-objective constrained optimization problem with a known optimal allocation, under its stated assumptions; there is no general multi-objective life utility or prediction algorithm here.

Experimental mechanism: five randomized arms. Control never had robo advice. Four treatment arms offered free advice, free advice with educational tips, paid advice, or paid advice with tips. All completed unaided trials 1 to 3, treatment exposure was possible only in trials 4 to 6, and trials 7 to 9 were again unaided. The study offered an experimentally optimal allocation. Some participants declined the offer or overrode it. The experimental paid-advice conditions and elicited willingness to pay do not establish any present commercial subscription price.

Scoring: percentage of potential savings forgone relative to the optimum versus worst possible allocation. Unaided pre-period mean was 21.9%. In the FCA public explainer, among those accepting free help, losses declined from 21.9% to 2.4% (19.5 percentage points, treated-user comparison). The original PDF introduction reports a rounded 19.6-point TOT; retain that version difference rather than silently asserting identical digits. The intention-to-treat effect accounting for non-use was approximately **14.6 percentage points lower forgone savings**. About one quarter declined free advice, and 5.7% of advised subjects overrode recommendations. These percentages describe **hypothetical allocation task performance**, not verified actual debt balances or future wealth.

Transfer and adverse trade-offs: subsequent unaided tasks did not show a meaningful imitation or explanation-driven learning gain; the control group showed the largest unaided improvement, consistent with learning-by-doing being crowded out by assistance in this setting. The FCA reported lower trust among non-adopters and overriders and willingness to pay often above estimated monetary benefit. No participant-specific longitudinal real debt outcomes, welfare, durable independent skill, or live consumer deployment were established by these experiment results.

Privacy and fairness: the study prepopulated all hypothetical account information. A real service would require comprehensive debt information, consent, access minimization and protection against lender conflicts of interest. Low trust and uneven adoption create possible distributional risks. These are candidate F questions, not measured security deployments.

## 3. Separate retirement projection RCT with an active comparator

Goda, Levy, Manchester, Sojourner, Tasoff and Xiao (2023), `Are retirement planning tools substitutes or complements to financial capability?`, Journal of Economic Behavior & Organization 214, 561–573, DOI 10.1016/j.jebo.2023.08.001. Official open institutional abstracts read: https://research.upjohn.org/up_workingpapers/378/ (2022 working paper DOI 10.17848/wp22-378) and https://www.nber.org/papers/w30723 (NBER DOI 10.3386/w30723). The paper lists preregistration AEARCTR-0002129; full registry, full methods, outcome measurement source and raw data NOT_READ. This is one experiment with multiple publication versions, not multiple independent replications.

Both randomized arms received a web-based retirement income goal projection. Treatment additionally displayed projected retirement income from defined-contribution savings, a gap relative to goal, and interactive exploration of alternative future contribution choices. The published abstract reports an average annual contribution increase of **USD 174 (2.3%)** in the treatment arm, with larger effects among financially knowledgeable participants. This provides a more behavior-oriented outcome than a self-report attitude score, but the available abstract does not establish whether the figure is based on payroll administrative records, self-report, intended changes or their duration. Do not label it verified realized payroll savings until full methods are inspected. No independent long-term retirement adequacy, cross-domain opportunity costs, calibration or net welfare was verified.

The intervention is a research calculator. Its algorithmic source, data privacy and ongoing price are not published in the materials actually read. It cannot be attributed to ProjectionLab or another commercial vendor.

## 4. Comparative evidence matrix and product relevance

| Dimension | FCA research robo adviser | Goda et al. research calculator | ProjectionLab product, MKT195 |
| --- | --- | --- | --- |
| Inputs | Hypothetical debt balances, rates, fees, budget | Retirement income target and defined-contribution assumptions | Assets, liabilities, cash flows, scenarios, user assumptions |
| State and objective | Fixed debts and one explicit interest/fee minimum | Retirement goal, projected gap, contribution choices | Multi-year conditional financial trajectories and user success criteria |
| Algorithm evidence | Experimental optimum in constrained allocation | Interactive projected gap, full algorithm not independently inspected | Official Plan/Chance-of-Success description; production implementation not verified |
| Feedback | Optimal allocation during selected trials, optional tips | Gap and interactive future contributions | Plan edits and simulated scenario comparisons |
| Direct human randomized evidence | Yes, hypothetical decisions; 14.6 pp ITT improvement | Yes, abstract reports USD 174 annual contribution effect; outcome source not yet verified | Product-specific randomized outcome evidence NOT_VERIFIED |
| Unaided transfer | No demonstrated learning benefit; control gained most | Not verified from available abstract | Not verified |
| Price and privacy | Experimental conditions only, not a consumer offering | Research prototype; actual pricing/privacy not established | MKT195 documented Basic free, paid tiers and cloud storage as of 2026-11-01 |
| Long-term net welfare | NOT_VERIFIED | NOT_VERIFIED | NOT_VERIFIED |

The contrasting results suggest a **research hypothesis**: decision aids can improve immediate performance in narrow objective tasks, while unaided skill transfer and long-term welfare require separate experiments. A real user may have multiple legitimate goals and constraints, so the FCA's unique numerical optimum cannot be generalized to a single life utility function. For future evaluation, separate (a) assisted task accuracy, (b) unassisted transfer after removal, (c) objective subsequent behavior, (d) long-term user-chosen outcomes and opportunity costs, (e) adoption, override, appeal, privacy and fairness. This is a candidate measurement framework, not a frozen R protocol or an approved product design.

MARKET-E1: official existing ProjectionLab functionality documented in MKT195, not rerun this pass.
MARKET-E2-ADJACENT: two randomized research interventions in distinct domains. The FCA outcome is an experimental hypothetical allocation; the retirement outcome's data provenance is NOT_VERIFIED at abstract-read scope.
MARKET-E3: independent long-term net personal welfare and product-specific durable improvements NOT_VERIFIED.
R E1/E2/E3: not applicable. This work does not upgrade any R acceptance state.

## 5. E governance check, current snapshot and F weekly status

At baseline main `2c810266c58b0c24b339263a76ae286443f23e71`, directly read both required project workflow documents, latest MKT199 and E166, current R/theory handoffs, latest R/B historical claim receipt audit, actual unified gate source, and open PR metadata. Compared main against MKT199 commit `0278556e1c0a34aac0d69e7c2c4805acd1b1ae27`: four newer commits touched six paths, all in R evidence audit, data scout and theory; original239 crosswalk and pending queue unchanged in that bounded comparison. R/B direct audit reports 154 pending items (27 P0, 82 P1, 45 P2), net closure 0 in its inspected snapshot; E did not reparse all queue rows.

R/B newly inspected eight historical CI run objects and 24 jobs, reporting success for each. This market/E pass independently queried R340 run 40063363405 and its three jobs: completed/success and head `bf4547eeb7a070a0b04fc14e1f25d114c12c17d8`. Historical CI metadata is not a fresh native replay or proof of scientific acceptance. R/B's new **16 historical claim files coverage gap** is confirmed by direct inspection of `research/evidence_audit/r333_r340_acceptance_entry_20261101.py` blob `9822418253c6a2888119c2a823ffee62dd945d7c`: the gate authenticates four validator source blobs and delegates source/CSV/JSON checks; it has no code path that reads the eight MACHINE_RECEIPT or eight FINAL_ACCEPTANCE_STATUS JSON files. This is static input nondependence, not a newly executed mutated-checkout test. The original optimized-mode false-accept P0, complete 16-child native execution and mandatory production caller adoption remain OPEN / NOT_RUN / PARTIAL respectively. R/B already owns scientific mathematics and negative tests; no duplicate E checker or new E number is warranted.

GitHub pulls collection at the baseline shows **12 open draft PRs**, no merged PRs in that open collection. PR #1 and PR #3 are open draft, unmerged. PR #3 head `97d5f74df5d84916917db943156120f08144f445` versus baseline main is diverged, with 1068 main-only and one PR-only commits; this is review drift, not demonstrated merge conflict. PR #3 source authentication and prescore blind-order gaps remain. R073 and PESEN v0.1 frozen. E166 already fulfilled today's substantial E audit; this pass is a read-only incremental cross-check and risk handoff, with no duplicate E-number report.

F W44 topic already COMPLETE in `F009_OPERATOR_DOMAIN_SPOOF_SHARED_ROOT_PHASE56_2026-W44.md`. This pass adds an external practical privacy and autonomy issue: FCA notes real debt advice would need consented account aggregation and that consumer trust/adoption and lender incentives matter. It does not justify another synthetic F phase. F actual deployment NOT_RUN; no private data were read.

No Actions were dispatched. Baseline main combined status query returned an empty statuses array, which is not evidence that historical CI never ran. Actual account billing/free quota NOT_VERIFIED. No paid API, purchase, registration, GPU or external cloud task was performed.

## 6. Next action

Market: obtain the full open Goda et al. methods to establish whether the USD 174 contribution outcome was actually realized and independently measured; separately seek an independently evaluated **named commercial** planning/decision-support product with objective long-term outcomes, and avoid transferring research-prototype effects to ProjectionLab.

E: R/B owner review of a mandatory source-pinned historical claim receipt gate for the 16 uncovered files, complete native 16-child execution and production fail-closed wiring, while preserving original P0 evidence; prioritize PR #1/#3 source and blind-order merge-readiness review.

F: maintain W44 COMPLETE, prioritize consent revocation, human override and learning dependence when next independent evidence or real product need emerges.

Sources accessed 2026-11-01:
https://www.fca.org.uk/publication/occasional-papers/occasional-paper-61.pdf
https://www.fca.org.uk/publications/research-articles-fca-research/can-robo-advice-improve-borrower-repayment-decisions
https://www.nber.org/papers/w30616
https://research.upjohn.org/up_workingpapers/378/
https://www.nber.org/papers/w30723
https://doi.org/10.1016/j.jebo.2023.08.001
https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/validation/R333_R340_HISTORICAL_CLAIMS_COVERAGE_AUDIT_2026-11-01.md
https://github.com/edwardsage419/Psychohistory-Research/pull/1
https://github.com/edwardsage419/Psychohistory-Research/pull/3
