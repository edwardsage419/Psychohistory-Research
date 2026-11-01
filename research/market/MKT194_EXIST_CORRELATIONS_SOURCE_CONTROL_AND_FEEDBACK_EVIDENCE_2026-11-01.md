# MKT194: Exist daily correlations, data source control, independent feedback evidence and consent lifecycle

Date: 2026-11-01 UTC
Track: market
Key: (market,Exist,official-API-and-policy-2026-11-01,correlation-versus-causal-decision-improvement)
Baseline main: 6b19e3c861be726c2dc8650cd7b4198e211a6c82
Status: COMPLETE_DOCUMENTARY; PRODUCT_RUNTIME_NOT_RUN; PRODUCT_SPECIFIC_EFFECT_NOT_ESTABLISHED
Read mode: NONBLIND official English documentation and independent corrected open-access meta-analysis. No account, API token, payment card, trial, sensitive data, or new expense.

## 1. Real product and user workflow

Exist (Hello Code) combines third-party service sync with user-entered daily values. Official supported manual types include quantity, decimal, duration, time of day, percentage, scale 1–9, and boolean-like tags. An attribute is represented as date/value pairs at **daily granularity**. Missing days are represented as null. Datetime values require user-timezone handling. One connected service owns/writes a given attribute at a time; switching its source can change measurement provenance.

Confirmed output: daily dashboard, weekly summaries, averages/trends, correlation statements, and historical correlation values. Official documentation states at least three weeks of non-missing data are needed for correlation discovery, with updates weekly. The API guide describes correlations computed from up to a year of past data. Same-day associations and adjacent-day offsets are considered. The correlation API returns attributes, time offset, period, coefficient in [-1,1], p-value, five-star confidence display, explanatory text and user rating. The vendor explicitly warns that correlation cannot identify cause.

The official API schema is inspectable; the proprietary production correlation implementation, complete missingness handling, autocorrelation correction, familywise false-discovery control, exact feature selection and decision-policy learning were not independently inspected. The API response's p-value and stars are statistical summaries, not proof of causal effects, prospective prediction accuracy or improved decisions. The existence of a displayed percentage is not an observed improvement rate.

Practical source issue: the vendor documents one owner per attribute and a sleep-source selection policy in which only one source is used for a day. This makes a stable source identifier, source-switch history and missing-data coverage important for future longitudinal inference. A displayed correlation may change when input provenance or coverage changes.

## 2. Independent human evidence and corrected effect size

Krukowski, Denton and König (2024), open-access systematic review, included 19 studies / 3261 participants in 24 reports. The **corrected** meta-analysis of physical-activity interventions comparing feedback against no feedback reports Cohen's d=0.29, 95% CI [0.16,0.43]. On 2024-02-23 the authors published a correction: the original d=0.73 was affected by a standard-error versus standard-deviation input mistake. The corrected review also notes brief interventions, high risk of bias in many studies and heterogeneous feedback designs. It cannot identify the effect of Exist's correlation display or general personal life decisions.

An older university publication listing still shows d=0.73; for scientific reuse the publisher's corrected article and correction notice take precedence. This is an actual source-version discrepancy, not a new 2026 product change.

No independent randomized Exist-user evaluation, holdout prediction improvement, retention-adjusted decision outcome, or net-welfare measurement was verified in this bounded search. Avoid transferring the adjacent review's effect size to Exist.

## 3. Privacy, permissions, deletion and cost

The public privacy policy says a connected source continues syncing until disconnected. **Disconnecting stops new collection while previously collected data remains in Exist.** Deactivating certain predefined attributes hides them while retaining their data. User-created custom attributes/tags can be permanently deleted. Account closure removes the account's data from the live service subject to the privacy policy's backup/archival retention caveat; payment/accounting records and support correspondence may remain. The policy describes external processors and limited internal employee access. Therefore Exist is a cloud service, with sensitive multi-source aggregation and third-party processing boundaries.

Export documentation updated 2026-04-23 lists PDF, CSV and complete JSON exports. Official public pricing viewed 2026-11-01: US$6.99/month or US$62.90/year, 30-day trial, payment card at signup, no continuing free plan. Project action: documentary review only, zero new expense.

Comparison reference: ActivityWatch official documentation describes free MPL-2.0 local-first app/window/browser activity tracking, local SQLite storage and export/deletion. Its published scope does not establish the same multi-domain correlation service or a validated causal recommendation engine. It is a possible future privacy architecture comparison, not a measured efficacy substitute.

## 4. Research implications and measurable future evaluation, candidate only

For a future research protocol, pre-register one target outcome and a small set of explanatory variables; preserve original source IDs, missingness, lag, timezone, number of tested pairs and model version. Compare raw tracking against correlation feedback using independently observed prospective outcomes. Hold out future weeks and measure calibration, false discovery, attrition, time cost, autonomy and adverse spillovers. Where possible use random assignment or well-designed N-of-1 interventions with consent. Separate observation, explanation, causal identification and welfare assessment. No universal life utility weights or production product design are authorized.

## 5. Evidence classification and execution

MARKET-E0: Product claims that it can uncover meaningful relationships and help users optimize behavior.
MARKET-E1: Official API/reference, knowledge-base, privacy, export and pricing documents directly read.
MARKET-E2-ADJACENT: Corrected independent randomized-trial systematic review for feedback in physical activity, with no direct Exist attribution.
MARKET-E3-EXIST: NOT_FOUND; product-specific prospective outcome and net-welfare effects NOT_VERIFIED.
R E1/E2/E3: N/A.
Product code/runtime: NOT_RUN. User data: NONE. API calls to Exist: NONE. Purchases: NONE. GitHub Actions: NOT_RUN. Actual account billing: NOT_VERIFIED.

## 6. English sources read on 2026-11-01

1. https://exist.io/ (features, current listed price)
2. https://developer.exist.io/reference/object_types/ (daily attribute schema, p-value/stars)
3. https://developer.exist.io/reference/correlations/ (API fields and offsets)
4. https://developer.exist.io/guide/read_client/ (one-year lookback and weekly correlations)
5. https://kb.exist.io/article/18-how-long-does-it-take-to-find-correlations (three-week non-missing threshold)
6. https://kb.exist.io/article/55-will-exist-find-correlations-across-multiple-days (adjacent-day offsets)
7. https://kb.exist.io/article/37-what-are-correlations (causality disclaimer)
8. https://developer.exist.io/reference/attribute_ownership/ (one owner per attribute)
9. https://kb.exist.io/article/42-why-is-my-sleep-data-incorrect (source selection)
10. https://exist.io/privacy/ (sync, disclosure, deletion and retention)
11. https://kb.exist.io/article/99-how-can-i-delete-or-deactivate-an-attribute
12. https://kb.exist.io/article/14-how-do-i-export-my-data (updated 2026-04-23)
13. https://exist.io/signup/ (card required for trial)
14. https://doi.org/10.1186/s12966-023-01555-6 (corrected review)
15. https://doi.org/10.1186/s12966-024-01569-8 (2024-02-23 correction)
16. https://docs.activitywatch.net/en/latest/faq.html (free local-first comparison)

Next high-value market task: identify an independently evaluated quantified-self correlation app or publicly available prospective user dataset, preferably with pre-specified outcomes and attrition. No new product registration.
