# Dawes (1979): simple linear prediction as an auditable baseline
Actual research date: 2026-11-21. Track: personal decision theory, research and acceptance preparation only.

## Primary source and inspected scope
Robyn M. Dawes (1979), “The Robust Beauty of Improper Linear Models in Decision Making,” *American Psychologist* 34(7), 571–582. DOI: 10.1037/0003-066X.34.7.571. Public copy of original article hosted by Stanford: https://stanford.edu/~knutson/jdm/dawes79.pdf .
Actually inspected: original article pp. 571–575, including original abstract, Oregon graduate applicant example, arguments on measurement and conditional monotonicity, sample-size caveat, Libby loan-officer counterexample and its subsequent reanalysis, and Table 1 opening. Later pages and original underlying participant data have not been independently reviewed or recalculated.

## Supported findings and exact boundaries
Dawes distinguishes optimized prediction weights from simple non-optimized weights, including equal weights, when numerical inputs predict a separately observable numerical criterion. His Oregon example reports correlation .48 for an equally weighted standardized predictor composite versus .19 for admissions committee judgments and .38 for a cross-validated optimized model. The article explicitly notes only 23 of the 111 students could be used in the committee judgment comparison because rating scales changed. These are historical correlations from a particular selected population, not universal model performance or evidence that an equal-weight *value function* should replace a person's preferences.
The article discusses the need for suitable variable coding, correct direction, and conditional monotonicity, and notes that the comparison can fail or change under predictor rescaling. Libby's loan-officer example initially favored human judgments over fitted judgment models before a later normalization analysis reversed that comparison. This is a review and methodological argument with cited empirical examples, not a new randomized test of a modern personal decision system.

## Distinct decision-system gap
Existing intuition-validity research asks whether confidence has track-record support. This study addresses a different question: when a decision system claims a complicated predictive model is better, what simple transparent prediction rule must it beat on the *same eligible outcomes*? Predicting an observable outcome is different from ranking life options by the user's chosen values. Hard constraints must be checked before scoring, and users retain all value weights and final authority.

## Candidate question and explanation rule
When offering a quantitative prediction, ask: “我们是否有可核查的历史结果，足以比较复杂模型与使用相同指标、统一量纲和方向的简单基线？如果没有，是否只展示假设情景而不声称预测更准确？”
Separate (1) observed outcomes, (2) predictor source and time, (3) normalization and sign, (4) simple baseline, (5) proposed model, (6) held-out comparison metric, (7) user-defined value weights. Do not silently assign equal *value* weights or replace confirmed preferences with empirical prediction coefficients. When there is no observed outcome or eligible holdout, label comparative predictive accuracy UNKNOWN.

## Six synthetic failure counterexamples, for independent acceptance
1. A and B have differently scaled attributes (income dollars and commute minutes); equal raw-number addition yields a ranking and is presented as valid without units, direction or normalization: FAIL.
2. System substitutes equal importance weights for a user's confirmed preference weights because Dawes recommends equal predictive coefficients: FAIL.
3. A complicated predictor is called superior using training fit only, while its transparent baseline is never evaluated on the same held-out cases: FAIL.
4. A single historical correlation .48 is shown as a 48% personal success probability: FAIL.
5. A high predictive score recommends an option violating a hard budget or deadline: FAIL.
6. A model trained on a historical population with different measurement scales is transported to a new population without marking measurement shift and unverified external validity: FAIL.

## Competing explanations and limitations
Simpler models may benefit from variance reduction and repeatable information integration; observed advantages may also depend on predictor selection, scale, missing data, criterion quality, selection bias and temporal or population drift. Nonlinear interactions, heterogeneous individuals and genuine expert signals can make linear baselines inadequate. No original participant-level data or independent replication was obtained in this track. Historical empirical correlation is not an intervention effect, and prediction quality is not personal decision quality.

## De-duplication and handoff
Checked current main workflow v3.0, recent commits, research/decision_methods names and open PR metadata on 2026-11-21. Existing Kahneman & Klein (2009) note covers intuitive expertise; current PR #57 covers active information planning and decision workbench. This note is scoped to the separate *predictive baseline versus value weights* distinction. Full semantic repository-wide de-duplication remains partial.
Model track: decide whether a simple, transparent prediction comparator can be exposed separately from user-value ranking, only after owner authorization.
Independent acceptance track: hold out six counterexamples and compare same-case metrics, missingness and shift; do not count this note as a passed test.
Data track: determine availability, rights, criterion timing, population and scale of eligible observational data.
Status: original primary-text review PARTIAL (pp. 571–575); rule and six synthetic cases COMPLETE as research artifacts; archival write/readback to be verified separately; statistical reproduction, code execution, independent validation and scientific acceptance NOT EXECUTED. No CI, paid API, private data or frozen-protocol modification.
