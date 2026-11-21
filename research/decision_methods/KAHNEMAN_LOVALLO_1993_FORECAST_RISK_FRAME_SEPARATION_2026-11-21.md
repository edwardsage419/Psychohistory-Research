# Kahneman and Lovallo (1993): forecast calibration and risk aggregation must be separated
Date actually reviewed: 2026-11-21. Track: personal decision theory. Status: candidate research, not scientific acceptance.

## Source and actual review
Daniel Kahneman and Dan Lovallo (1993), "Timid Choices and Bold Forecasts: A Cognitive Perspective on Risk Taking", *Management Science* 39(1), 17–31, DOI: https://doi.org/10.1287/mnsc.39.1.17 .
Open first-hand journal copy hosted by UCLA: https://www.anderson.ucla.edu/faculty_pages/keith.chen/negot.%20papers/KahnemanLovallo_ChoicForcastsRisk93.pdf .
Reviewed accessible article text and abstract, especially the introductory thesis, sections "Timid Choices", "Bold Forecasts", and "Inside and Outside Views" (article pages 17, 23–25). No independent full-page audit, original experimental dataset or quantitative replication was conducted.

## Distinct decision gap
The article discusses two potentially opposing errors: inside-view optimism in forecasts, and overly cautious assessment of isolated moderate risks when repeated opportunities could be aggregated. Its application domain is organizational choices among attractive risky opportunities, particularly intermediate-size stakes. It explicitly warns that encouraging greater risk taking before correcting optimistic forecasts could worsen decisions. These are arguments synthesized from prior research, not a calibrated correction formula for an individual.

The personal decision system must evaluate **forecast reliability** separately from **loss tolerance and aggregation eligibility**. A user may have an optimistic outcome estimate while reasonably rejecting a potentially ruinous downside. Repeated independent trials in an organization cannot be assumed for one-off health, relationship, migration, or irreversible career decisions.

## Candidate operational questions
1. "Your outcome estimate comes from your own execution plan, or from completed comparable cases? What is the source, sample period and relevant denominator?"
2. "If this attempt fails, can you realistically make further comparable attempts without violating any of your stated hard limits? What shared failure causes could affect all attempts?"
3. "What loss can you absorb before the next opportunity, and which consequences are irreversible?"

Record distinct fields: inside-view estimate, eligible external reference class, evidence qualification, scenario interval, shared-risk exposure, number and timing of truly repeatable opportunities, hard loss bound, user-confirmed risk tolerance. Unknown values stay unknown. Show forecast revision and risk decision separately, retaining user versions.

## Six synthetic acceptance counterexamples (design only)
1. Entrepreneur forecasts 90% success from a detailed plan without comparable-case data: do not treat 90% as verified.
2. Five projects share one funding source: do not claim independence or diversification.
3. One irreversible medical intervention: do not use portfolio aggregation to recommend taking more risk.
4. User can absorb one $100 loss but not ten consecutive losses: account for timing and liquidity, not merely long-run expected value.
5. External reference class mixes different regulations and eras: reject direct probability transfer until comparability checked.
6. After evidence changes forecast from 70% to unknown, retain original user probability and original risk preference separately; do not silently overwrite either.

## Competing explanations and limitations
Optimism may reflect private information or genuine skill; caution may reflect liquidity, asymmetric utility, moral obligations, correlation, irreversibility, and selection. The paper does not identify a person's true risk parameter, probability, or universal optimal risk level. It should not be used to automatically change a user's weights or force aggregation. Related existing research: Buehler et al. (1994) personal completion-time forecasting; Flyvbjerg (2006) reference-class transfer; C009 option value and reversibility; C029–C031 scenario regret. This note addresses the **joint error interaction and separation gate**, not a new forecast estimator or computational model.

## Responsibility and evidence
Theory track: source interpretation, three operational questions, six synthetic counterexamples prepared. Archive is not execution. Model track: candidate dual-panel explanation and explicit aggregation eligibility gate; no implementation authorization here. Data track: reference-class denominator, correlation and transfer eligibility. Independent acceptance track: independently held-out cases, user-value preservation and simple baseline comparison. No code run, numerical replication, independent validation, or real-world scientific acceptance. No CI, paid API, personal data, R-series edits or PR merge.
