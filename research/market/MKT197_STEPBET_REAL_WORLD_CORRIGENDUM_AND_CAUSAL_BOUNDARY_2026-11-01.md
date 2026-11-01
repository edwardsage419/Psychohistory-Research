# MKT197: StepBet真实产品数据、论文勘误与因果边界

track: market
subflow: commercial product mechanism and real-world effectiveness
run_date_utc: 2026-11-01T10:20Z
target_key: (market,StepBet+deBuisonje2023+Corrigendum2023,2023-paper+2026-09-03-privacy+2026-01-21-FAQ,real-world-tracker-outcomes-corrigendum-and-causal-attribution)
baseline_main: 8c687e3a6aeca91a143af41867131c82442b057b
status: COMPLETE_DOCUMENTARY
product_runtime: NOT_RUN
scientific_reanalysis: NOT_RUN
data_download: NONE
sensitive_user_data: NONE
paid_actions: NONE
billing_checked: NOT_VERIFIED
ci: NOT_RUN
evidence_scope: MARKET-E1_OFFICIAL + MARKET-E2_DIRECT_OBSERVATIONAL_WITH_VENDOR_COAUTHOR; MARKET-E3_LONG_TERM_CAUSAL_WELFARE=NOT_VERIFIED
read_scope: NONBLIND, English official StepBet FAQ, help, privacy, peer-reviewed 2023 study abstracts and indexed full-text excerpts, institutional repository abstract, published corrigendum and 2024 adjacent RCT abstract.

## 1. Why this is new relative to MKT193 to MKT196

MKT193 studied Beeminder plus an adjacent randomized exercise commitment intervention. MKT196 examined 3,857 self-selected stickK contracts with self-reported weight outcomes and a 619-user randomized contract-default experiment. StepBet offers a different directly measured outcome: third-party activity tracker steps, individualized thresholds and real-world participation from 2015 through 2020 (N=72,974). The 2023 paper has a published correction, which must be carried forward in any evidence reuse.

## 2. Product operation and documented trust boundaries

StepBet official FAQ (accessed 2026-11-01) describes selecting an activity tracker, using historical step data to calculate individualized Active and Power targets, paying a stake (most games USD 40), and meeting weekly goals in games usually lasting six weeks. Winner payouts are pooled; a failed weekly target eliminates the player from winning. StepBet describes a 15% gross-pot retention in standard games and a membership variant. The 2026-01-21 help page calls the target-generation algorithm customized; formula, model validation, uncertainty calibration and counterfactual recommendation logic are not publicly disclosed. Some games may increase targets week by week. The current FAQ should not be back-projected to all 2015 to 2020 historical games.

Input: wearable/phone step counts from selected providers including Garmin, Apple Health/Watch, Fitbit, and Google Health Connect; history of steps and game enrollment.
State: current tracker, historical step baseline, Active/Power goals, day/week progress, eligibility, stake and payout.
Goal: fulfill specified activity days and recover stake, potentially earn a share of losers' stakes.
Feedback: daily tracking, progress and game outcome; fraud detection and referee disputes. The product does not publish a validated multiobjective personal welfare function.
Source control: current FAQ requires one step source for a game; a source cannot normally be changed mid-game. Tracker loss, battery failure or sync delay can affect financial outcomes. FAQ says device/StepBet count discrepancies can be disputed, while lost or broken trackers do not automatically reverse disqualification.
Costs: typically USD 40 stake per game; games generally require payment; membership and 15% standard game retention are distinct. No paid account was opened.

Sources:
https://stepbet.com/faq
https://stepbet-support.zendesk.com/hc/en-us/articles/35418536256411-How-do-you-play
https://stepbet-support.zendesk.com/hc/en-us/articles/35418596343963-How-are-my-Active-and-Power-goals-calculated
https://stepbet-support.zendesk.com/hc/en-us/articles/35820259376027-What-do-I-get-with-StepBet-membership

## 3. Direct platform observational study

de Buisonjé DR et al. (2023), Internet Interventions 31:100610, DOI 10.1016/j.invent.2023.100610. Study dataset supplied by platform operator WayBetter, 72,974 StepBet participants/challenges 2015 to 2020, prechallenge reference based on 90 days of historical step counts.

Reported mean daily steps increased from 7,774 (SD 3,112) baseline to 10,197 (SD 4,162) during challenges: +2,423 steps, +31.2% (SD of individual change 3,462). Challenge success rate 73%. Successful cases n=53,281, mean change +3,465 steps (+44.0%, SD 3,013); unsuccessful cases n=19,693, mean change -398 steps (-5.3%, **corrected SD 2,993**). January 1 to 14 starters had 77.7% success versus 72.6% other dates; the source reports a small association.

The paper includes a company-affiliated author: Erika Litvin Bloom of WayBetter. This is a disclosed affiliation, not evidence of misconduct. The study is a peer-reviewed direct-platform naturalistic analysis, with vendor-supplied data. It does not randomly allocate app access or stakes. Participants self-selected; pre/post comparisons are vulnerable to motivation, seasonality, regression to the mean, activity-tracker measurement and challenge survival differences. Success versus failure is defined by post-enrollment performance, so the +44% and -5.3% subgroup contrast is not a randomized causal effect. Six-week activity and challenge success do not measure persistence after the game, financial losses, stress, spillovers or net welfare. Independent access to row-level dataset, source code and a new preregistered causal analysis was not established here.

Sources:
https://pubmed.ncbi.nlm.nih.gov/36873308/
https://repository.tudelft.nl/record/uuid:dfafd525-7101-41ad-98cc-21512fca775e
https://pmc.ncbi.nlm.nih.gov/articles/PMC9982638/

## 4. Mandatory published corrigendum

de Buisonjé et al., Internet Interventions 32:100626, published April 27 2023, DOI 10.1016/j.invent.2023.100626. The correction explicitly changes:
1. Standard deviation of daily step change among unsuccessful participants from the incorrectly printed **3,013** to **2,993**.
2. Exploratory regression subsample from the incorrectly printed **29,001** to **29,002**.

The correction does not change the reported total N=72,974, the mean -398 steps or the 73% success figure in the sources reviewed. Any future cross-product quantitative synthesis must cite both the original and correction, and retain the corrected subgroup SD and regression N. This is a substantive evidence-provenance correction, not a newly observed change to StepBet's live product.

Source:
https://research.tue.nl/en/publications/corrigendum-to-put-your-money-where-your-feet-are-the-real-world-/
https://pubmed.ncbi.nlm.nih.gov/37273937/

## 5. Adjacent randomized uptake study and boundaries

de Buisonjé et al., 2024, Psychology of Sport and Exercise 70:102532, DOI 10.1016/j.psychsport.2023.102532. A randomized 137-student smartphone-app study varied deposit matching and customization, reporting higher odds of uptake with matching (OR 4.08, p=.010) and customization (OR 3.53, p=.022), but no significant effect of those randomized features on the number of achieved daily step goals (matching p=.752; customization p=.143). Participants used a research app; this is adjacent mechanism evidence, not a StepBet product RCT. Small, short-term, student sample and intervention setting limit transferability. The paper's 2x2 uptake contrasts do not establish long-term health or welfare benefit.

Source:
https://doi.org/10.1016/j.psychsport.2023.102532

## 6. Privacy, permission and fairness

The official StepBet privacy notice says last revision 2026-09-03 and documents tracker-provider data sharing, contact and payment information, game participation, optional contacts, possible location data for game auditing, access/erasure/consent withdrawal requests and third-party services. User-submitted game discussion may be visible to others. Data minimization, retention/deletion completion and downstream tracking were not independently audited. Source:
https://stepbet.com/privacy

A specific candidate F risk is asymmetric loss: when device failure, syncing delay or measurement error produces disqualification, users can lose a stake despite uncertain true activity. The current FAQ offers some referee dispute resolution for mismatches and different treatment for lost/broken devices. This warrants future fairness and appeal study, not a new F phase without additional external evidence. No personal step or financial records were accessed.

## 7. Evidence ledger and next questions

MARKET-E0: promotional claims about motivation, effectiveness and long-term habit formation remain vendor claims.
MARKET-E1: documented current input, target, payout, tracker and privacy mechanisms. Runtime independently tested: NOT_RUN.
MARKET-E2_DIRECT_OBSERVATIONAL: 72,974 cases with tracker steps, vendor data and coauthor affiliation, published 2023 and corrected 2023; not causal.
MARKET-E2_ADJACENT_RCT: 137 students, randomized uptake design; no demonstrated randomized change in achieved steps.
MARKET-E3_LONG_TERM_CAUSAL_WELFARE: NOT_VERIFIED.
R scientific E1/E2/E3: N/A.

Priority follow-up: identify a directly randomized, matched-attention field trial with objective activity/financial costs and post-game follow-up; if unavailable, compare objective measurement failures and dropout across StepBet/stickK/Beeminder without claiming product superiority. Preserve correction provenance. No implementation or new fees.
