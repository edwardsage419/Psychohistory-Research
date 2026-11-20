# Fischhoff 1975: hindsight leakage in personal decision review
Date: 2026-11-20. Status: original-source audit and candidate acceptance preparation; no deployment or independent scientific acceptance.

## Source and inspected scope
Baruch Fischhoff (1975), *Hindsight ≠ Foresight: The Effect of Outcome Knowledge on Judgment Under Uncertainty*, Journal of Experimental Psychology: Human Perception and Performance 1(3), 288–299. DOI 10.1037/0096-1523.1.3.288. Author-affiliated Carnegie Mellon scan: https://www.cmu.edu/epp/people/faculty/faculty-images-and-files/jep-hpp-hindsight-foresight-1975.pdf .
Inspected original pp. 288–293, especially Experiment 1 design, results, Table 1 and relevance judgments; Experiment 2 design on p. 293. Remaining pages and individual raw observations were not independently audited.

## Verified reported findings
Experiment 1 randomly allocated participants to a Before condition (event description only) or After conditions (same description plus one purported outcome). In six subexperiments and 24 outcome comparisons, reported outcome knowledge increased assigned retrospective probability in all 24 comparisons. The author reports sign-test p < .001, individual significance in 22 comparisons, differences ranging from 3.6 to 23.4 percentage points, mean 10.8 points. These are author-reported aggregate statistics, not an independent raw-data recomputation. Relevance judgments of pre-event facts also varied with the stated outcome. The experiment deliberately sometimes supplied a false purported outcome, strengthening the interpretation that outcome information changes reconstruction, but not identifying a personalized effect size.

## Decision-system rule
At decision time preserve a timestamped immutable snapshot of options, constraints, known evidence, explicit subjective forecasts, missing data, model version, and the user's reasons. At review time display separately (a) ex ante forecast and chosen action, (b) realized outcome, (c) later-acquired information and changed preferences, and (d) counterfactual alternatives explicitly marked unobserved. Do not silently rewrite the ex ante forecast or claim that a single realized outcome establishes ex ante decision quality.

Candidate question: “在作决定的当时，你掌握哪些信息？哪些事实是在结果出现之后才知道的？”

## Synthetic acceptance cases
Case 1: at time t0 user estimates a 30% adverse outcome risk, with an explicit rationale; at t1 the adverse outcome occurs. Display the stored 30% unchanged and record outcome separately. Replacing it with 100% as the ‘original’ estimate fails.
Case 2: an event occurs and a previously unavailable warning is discovered later. Do not mark it as known at t0. Show provenance and availability time.
Case 3: an unchosen career option's result is unknown. Do not fill it with an imagined realized salary or claim actual regret; present only conditional scenario estimates.
Case 4: when new information becomes available at t1, the user may legitimately update their next forecast. Preserve both forecasts with their timestamps.

## Assumptions and alternatives
Possible competing explanations include rational updating when genuinely new evidence arrives, memory reconstruction, selection effects, genuine changes in goals, and outcome-conditioned causal explanation. A retrospective judgment may be valid for a new decision even if unsuitable as an unchanged historical forecast. The historical and clinical vignette experiments do not establish effectiveness of this proposed interface in individual career or financial decisions.

## Handoff and verification
Independent acceptance track: time-of-knowledge leakage tests, counterfactual unknown handling, frozen predecision record, and comparison to a simple timestamped baseline.
Model track: propose snapshot and review explanation interface only upon owner authorization.
Data track: provenance, availability timestamp, outcome observation and missing counterfactual eligibility.
Deduplication: checked workflow v3.0 and latest known status-quo audit; full cross-track semantic and open PR dedup remains pending. Unnumbered record avoids C-series identifier collision.
Completed: original source section review, explicit numerical extraction, candidate rule, synthetic cases, archival. Not run: raw-data statistical replication, program tests, real personal validation, independent scientific acceptance. No paid API, CI, private data or PR merge.
