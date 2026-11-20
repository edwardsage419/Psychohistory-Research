# Aiyer et al. (2023): outcome bias replication and prospective decision review boundary

Date completed: 2026-11-21. Track: personal decision theory. Status: primary publication targeted review COMPLETE; independent reanalysis NOT_RUN; real personal effectiveness UNKNOWN.

## Decision capability and nonduplication
Capability: separate decision-time process evaluation from observed outcome and counterfactual hindsight. Prior repository work on hindsight leakage and C028 counterfactual identification addresses temporal information and identification. This note addresses the experimentally replicated *outcome-valence contamination of human ratings* and its transfer boundary. No R protocol, prior record, or scoring rule is changed.

## Primary sources and actual scope
Aiyer, S., Kam, H. C., Ng, K. Y., Young, N. A., Shi, J., & Feldman, G. (2023). “Outcomes Affect Evaluations of Decision Quality: Replication and Extensions of Baron and Hershey’s (1988) Outcome Bias Experiment 1.” International Review of Social Psychology 36, article 12. DOI https://doi.org/10.5334/irsp.751 ; open original https://pmc.ncbi.nlm.nih.gov/articles/PMC12372742 . Reviewed abstract, Background, Confirmatory Results, Discussion and limitations in the open original web text. Original target: Baron, J., & Hershey, J. C. (1988), Journal of Personality and Social Psychology 54(4), 569–579, DOI https://doi.org/10.1037/0022-3514.54.4.569 . Target original abstract checked at https://pubmed.ncbi.nlm.nih.gov/3367280/ ; original full tables not independently audited.

The 2023 preregistered replication used N=692, between-participants medical decision scenarios; the original Experiment 1 had N=20 and a within-participants design. Reported outcome main effect F(1,688)=152.37, mean difference 1.11, p<.001, with favorable outcome n=344 mean 1.78 versus unfavorable n=348 mean 0.68. This is the authors' report, not our recomputation. Authors report replication of direction and signal, with larger standardized effects than original, cautioning that designs differ. A single medical scenario limits generalization. Neither original nor replication included an outcome-unknown baseline, so absolute direction of distortion relative to baseline is not identified.

## Executable candidate interpretation rule
At initial decision, record time-stamped known facts, options, user-confirmed values and constraints, probabilities with evidence status, selected action, and rationale. At review, display separately: (A) ex ante process appraisal based solely on predecision information, (B) observed outcome, (C) lessons for updating future forecasts, with hindsight source tagging. If a result reveals genuinely new evidence, update the future model in a separate versioned step; do not silently rewrite the original information set or its prior evaluation. A bad outcome can coexist with a defensible process and vice versa.

Suggested question: “If you had not known how this turned out, given the information available on the day, would you still judge the process acceptable? Which facts were genuinely known then?”

## Synthetic acceptance counterexamples
1. Identical decision-time dossier, same action and probabilities; one synthetic branch succeeds and another fails by chance. System silently changes its ex ante decision-process score solely because of outcome: FAIL.
2. A chosen action succeeds once. System labels its predictive calibration validated from this one outcome: FAIL.
3. Unchosen action's outcome is not observed. System reports the alternative would certainly have done better: FAIL.
4. A later-discovered causal defect was unknown at decision time. System retroactively inserts the defect into the historical predecision dossier: FAIL. It may record the defect as new evidence for future decisions.
5. User has explicitly selected an ethical outcome-based responsibility standard. System erases that preference in the name of process-only evaluation: FAIL. Keep user moral evaluation separate from statistical process audit.

## Competing explanations and limitations
Outcome salience, hindsight reconstruction, responsibility attribution, moral evaluation and legitimate updating after new evidence can each change retrospective judgments. The experiment measures ratings of hypothetical medical decisions; it does not establish improved personal decision outcomes from a software guard. Study sample and design do not justify an individual-level correction coefficient. No effect size should be inserted into a user score. Human moral judgments of outcomes may be legitimate and require separate user-controlled weights.

## Handoff and status
Independent acceptance track: blind paired-case test with outcome labels reversed; check predecision dossier immutability and counterfactual unknown. Model track: evaluate a two-stage process/outcome review UI without implementing here. Data track: confirm OSF https://osf.io/knjhu/ licensing, preregistration, actual files and reproducibility before any reanalysis.

Archive COMPLETE if GitHub commit and readback verified. Paper primary text targeted review COMPLETE. Original 1988 full text PARTIAL. Program execution NOT_RUN. Statistical independent recomputation NOT_RUN. Real-world validation NOT_RUN. Scientific acceptance NOT_RUN. No paid API, CI, personal data or protocol changes.
