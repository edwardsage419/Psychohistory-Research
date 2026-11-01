# MKT196: stickK direct platform evidence, verification bias and commitment costs

track: market
subflow: commercial product mechanism and effectiveness evidence
run_date_utc: 2026-11-01T09:24Z
target_key: (market,stickK+Lesser2018+GoldhaberFiebert2010,official-FAQ-2026+2013-contract-cohort+2010-RCT,direct-product-outcome-versus-selection-and-verification)
baseline_main: 1d30e1ad829cfe21dc851606b275efa0abeb6083
status: COMPLETE_DOCUMENTARY
product_runtime: NOT_RUN
product_specific_long_term_welfare: NOT_VERIFIED
evidence: MARKET-E1_OFFICIAL, MARKET-E2_DIRECT_OBSERVATIONAL, MARKET-E2_DIRECT_RCT_CONTRACT_DESIGN
r_scientific_E1_E2_E3: N/A
read_scope: NONBLIND, official English FAQs and privacy policy, peer-reviewed journal abstract and indexed full-text excerpts, NBER working-paper abstract, existing MKT193 for deduplication
new_paid_actions: NONE
user_sensitive_data: NONE
ci: NOT_RUN
actual_billing: NOT_VERIFIED

## 1. Why this adds evidence beyond MKT193

MKT193 already examined Beeminder's financial commitment mechanics and an adjacent exercise commitment randomized trial with more than 4,000 participants. This run found a different, directly identifiable platform cohort: Lesser, Thompson and Luft's retrospective analysis of 3,857 stickK weight-loss commitment contracts voluntarily created in 2013, published online in 2016 and in the 2018 journal issue. It also read a separate 2010 randomized study conducted in a stickK web contract tool with 619 participants, which randomizes contract-duration defaults. These are direct platform evidence at different causal strengths and outcomes. No synthetic experiment was made.

## 2. Official product mechanism and commercial boundary

stickK is an online goal commitment service. Official FAQs describe free creation of one-shot commitments with one terminal report, or ongoing commitments with weekly reports. Users choose goal, deadline, timeline, optional financial stakes, recipient of forfeited stakes, referee, and supporters. Reporting records claimed success/failure; referees can confirm or dispute the user's report and may accept the user's word without physical proof. Supporters receive progress notifications and can comment. Official reporting FAQ states failure can be triggered by user report, referee failure report or no report within a current 72-hour reporting window. This timing is the current FAQ description, and must not be silently back-applied to 2013 historical contracts.

The state is a contract with a goal, time window, report and stake status. The observable feedback loop is periodic reporting, reminder/notification, social accountability and contingent loss. Official sources do not disclose a validated individual forecasting algorithm, adaptive multi-goal utility optimization, calibrated counterfactual effect model, or autonomous life-decision recommendation engine. No product login, live execution or independent API inspection was attempted.

Official contract creation is free; financial stakes are optional. The stakes FAQ states a minimum of USD 5 per reporting period, and the financial FAQ describes a temporary USD 1 card authorization and possible loss charges following unsuccessful reports. This is a real monetary risk for participants. The project did not create an account, provide a payment method or incur any stake.

Privacy FAQ distinguishes public commitments, member-only profile visibility and restricted commitments. Privacy policy describes invitations to referees/supporters, backup retention, account deletion requests, and sharing of public site data with third parties. Referee and supporter changes after acceptance may require contacting support. These are documented permissions and policy statements; implementation, actual deletion time, privacy defaults and third-party access were not independently audited. Public user journals were deliberately excluded from research to avoid collecting identifiable personal data.

Official sources, accessed 2026-11-01:
https://new.stickk.com/faq/commitment/Commitment%2BContracts
https://new.stickk.com/faq/reporting/Commitment%2BContracts
https://new.stickk.com/faq/referees/Commitment%2BContracts
https://new.stickk.com/faq/supporters/Commitment%2BContracts
https://new.stickk.com/faq/stakes/Commitment%2BContracts
https://new.stickk.com/faq/financial/Commitment%2BContracts
https://www.stickk.com/faq/privacy/stickK%2BPrivacy%2Band%2BSecurity
https://stickk.zendesk.com/hc/en-us/articles/360000872247-Privacy-Policy

## 3. Direct observational outcomes, sample and selection

Lesser LI, Thompson CA, Luft HS. Association Between Monetary Deposits and Weight Loss in Online Commitment Contracts. American Journal of Health Promotion 32(1), 198–204, 2018, online 2016-08-08. DOI: 10.1177/0890117116661157. Sources:
https://journals.sagepub.com/doi/10.1177/0890117116661157
https://pubmed.ncbi.nlm.nih.gov/27502832/
https://pmc.ncbi.nlm.nih.gov/articles/PMC5316505/

The study analyzed 3,857 eligible contracts from users voluntarily joining stickK in 2013. The published account describes 10,524 original contracts and exclusions including 4,650 test contracts and 1,716 repeat users. Participants chose goal, duration, weekly reporting and whether to pledge money; treatment assignment was not randomized. In multivariable regression, compared with contracts without deposits, weekly reported weight change was more negative by 0.33 percentage points for anticharity, 0.28 for charity and 0.25 for friend deposits, with P<0.001 for each. These are adjusted associations in self-selected groups, not causal treatment effects or product-wide success probabilities.

A material verification result: contracts without a verification method claimed greater weight loss than contracts with verification. The paper notes that a referee may verify by direct observation or a dated scale photo, while users can also self-report. Thus verification status is heterogeneous and does not guarantee independent ground truth. Reporting completeness differed across contract types; the observational sample and exclusions raise selection and attrition concerns. Neither adjusted regression nor referee presence removes unobserved motivation, reporting manipulation, measurement error or unmeasured confounding. The study does not establish long-term health or net welfare improvements.

## 4. Direct randomized contract-choice mechanism, distinct outcome

Goldhaber-Fiebert JD, Blumenkranz E, Garber AM. Committing to Exercise: Contract Design for Virtuous Habit Formation. NBER Working Paper 16624, December 2010. DOI 10.3386/w16624.
https://www.nber.org/papers/w16624

The study randomized web contract-creation default durations of 8, 12 or 16 weeks among 619 users, with 61% accepting/signing a commitment. Longer defaults shifted selected contract duration; acceptance, chosen exercise frequency and stakes did not differ materially by default group in the reported abstract. This supports a causal effect of interface defaults on **contract choice**, with the usual study-scope limitations. The abstract does not establish a causal improvement in objectively measured long-term exercise, health, or total welfare. The later >4,000-participant randomized study mentioned in MKT193 is a separate related evidence stream and is not counted here as a new finding.

## 5. Product comparison and falsifiable candidate questions

Beeminder tracks a quantitative trajectory and buffer, charging on derailment. stickK centers on discrete one-shot or periodic commitment reports, optional referee and supporters, and recipient-specific stakes. Both rely on user-selected goals and monetary consequences. In stickK, contract success, verified objective outcome and net personal welfare can diverge; missing reports can also trigger loss independently of actual goal attainment.

Candidate research questions for a future model, with no product implementation now: Does an independent measurement channel change apparent success rates relative to self-report? Does the commitment improve the pre-specified objective over a matched no-stake comparator after accounting for selection, missingness and differential reporting? What are the time, financial, stress, autonomy and spillover costs across competing goals? How are referee consent and revocation enforced? A suitable future evaluation would predefine outcomes, match contact time, record intention-to-treat and attrition, and measure longitudinal objective outcomes and welfare. No unique life utility weights are set.

MARKET-E0: platform marketing claims such as up-to-3x success remain unverified.
MARKET-E1: official documented contract mechanics, price and privacy disclosures; actual production behavior NOT_RUN.
MARKET-E2_DIRECT_OBSERVATIONAL: 3,857-contract stickK dataset, selection-limited and partly self-reported.
MARKET-E2_DIRECT_RCT_CONTRACT_DESIGN: 619-user randomized defaults, evidence for contract-choice response only.
MARKET-E3_DIRECT_LONG_TERM_WELFARE: NOT_VERIFIED.
R scientific E1/E2/E3: N/A.

next_action: seek an independent longitudinal stickK or similar platform trial with objective outcomes and explicit welfare/cost measurement, or examine an open-source adaptive goal tool with inspectable predictive algorithm. Avoid repeating generic commitment device theory or expanding security machinery without product evidence.
