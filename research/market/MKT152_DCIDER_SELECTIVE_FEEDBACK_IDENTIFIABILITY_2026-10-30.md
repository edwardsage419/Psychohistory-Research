# MKT152 Dcider selective outcome feedback and value drift identifiability

UTC 2026-10-30. Track market. Target (market,Dcider,official-2026-10-30,selective-feedback-vs-value-drift). Baseline main 94cc5194a3810dd9963a44e0112d605d58dc29f8. Status COMPLETE_BOUNDED_ARTIFICIAL_E1. Read MKT150/MKT151 and market handoff before selection. This is a distinct follow-up, not a replay of MKT151.

## Product evidence and mechanism boundaries

English official site https://dcider.app/ read 2026-10-30: users define personal values and importance, receive AI option scores, retain the final decision, and can review past choices/outcomes. Users may change their values in Settings. Decision history and values can be viewed offline; AI analysis needs cloud connectivity. Site says encryption, account deletion, and no use of AI analysis for model training. These are vendor statements, not independent privacy verification. Current advertised price USD 4.99/month or USD 44.99/year after seven-day trial; iOS only. No registration or purchase.

Inputs documented by vendor: value weights, decision descriptions, chosen options, outcomes. State/feedback: historical choices and recorded outcomes. Internal scoring formula, counterfactual data, propensity logging, follow-up missingness policy, value version retention, feedback correction algorithm, actual user improvement, and independent scientific validation are UNKNOWN. The word objective on the site is a marketing description of alignment scoring, not an independently validated utility function.

Independent research context: Agarwal et al. KDD 2017 https://www.kdd.org/kdd2017/papers/view/effective-evaluation-using-logged-bandit-feedback-from-multiple-loggers reports limitations of naive combination across historical logging policies. Narita et al. AAAI 2023 DOI 10.1609/aaai.v37i8.26113 https://ojs.aaai.org/index.php/AAAI/article/view/26113 studies off-policy evaluation under particular support and model conditions. Their results do not establish identifiability for our fictional data without their additional assumptions.

## Executed artificial finite counterexample

Runnable research/market/mkt152_selective_feedback_exact_20261030.js executed locally with Node on 2026-10-30: 16 assertions PASS. Eight entirely fictional decisions. First four: historical weight 0.65, choose A, all four A rewards 0.75. Last four: weight 0.50, choose B, only two B rewards observed and equal to 1; other two B follow-ups missing. No known choice propensities. Observed selected-action reward rises from 0.75 to 1.00, naive difference +0.25.

The B potential outcome is unobserved for the four early A choices and the two late B choices without feedback. Enumerating all 2^6=64 binary completions, with all observed records fixed, yields B-always policy mean range [0.25,1.00], late B mean [0.50,1.00], and late B minus early observed A range [-0.25,+0.25]. Both apparent improvement and decline are consistent with exactly the same logs. The two worlds differ in missing potential outcomes; no data leak or new participant is involved.

These bounds assume each unobserved B reward is binary 0/1, and each observed reward is a fixed score in [0,1]. Without this bounded outcome assumption the range would differ. This is a finite identification counterexample, not a claim that Dcider implements an invalid estimator or that user preferences are objectively measurable.

## Candidate knowledge reserve

Keep decision-time preference version, action set, policy version, action selection mechanism and any known propensity, chosen outcome, observation time, follow-up eligibility, explicit missingness reason and revision provenance. Separate observed-action trends, contemporaneous preference alignment, and identified policy counterfactuals. When no overlap or missingness justification exists, show partial bounds or UNKNOWN. No forced randomized user experiments, no universal value weights, no personal data. Evidence: MARKET_OFFICIAL_DOC, RESEARCH_PAPER_ABSTRACT, INTERNAL_NONBLIND_ARTIFICIAL_E1. E2/E3 newly produced 0. Next MKT153: compare ARDA decision feedback or Beeminder behavior-control feedback with a verified technical specification, avoiding more Dcider toy variations unless new evidence appears.
