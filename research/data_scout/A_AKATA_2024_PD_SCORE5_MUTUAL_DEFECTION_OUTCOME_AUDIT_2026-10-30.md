# A轨：Akata等2024人机重复博弈合作指标方向核验

date_utc: 2026-10-30
target_key: (A,eliaka/repeatedgames@224a605a,PD-author-script-score5-vs-score8-joint-cooperation)
status: PARTIAL, critical downstream interpretation gate
sources:
  experiment script: https://github.com/eliaka/repeatedgames/blob/main/human_experiment/experiment/js/script.js ; blob 4b7be85e8b3b964bfd0722d796f5ed6c2b8f0a19
  author instructions: https://github.com/eliaka/repeatedgames/blob/main/human_experiment/experiment/README.md ; blob 77115c8edb43dbc7ef8bc46e596f67d58f2c8f81
  analysis: https://github.com/eliaka/repeatedgames/blob/main/human_experiment/analysis/repeated_games.Rmd ; blob ca9991b6d0917156672e1e2fea923548562d945e
  public cleaned CSV: https://github.com/eliaka/repeatedgames/blob/main/human_experiment/analysis/repgames.csv ; blob 2dd67c6ff80f2d7aa07a70b470e26fe3592c6d95

## Actual inspection and result
Read author experiment JavaScript calculate_points_pd() and instructions, plus Rmd PD analysis and full 3900-row public cleaned CSV. Author code maps action 1 to J, action 0 to F. PD scores are J/J=8, F/F=5, J/F=0, F/J=10. Hence J is the cooperative action in the payoff-dominant social dilemma and F is defection.

The author Rmd line near 299 computes dpd$cooperated <- ifelse(dpd$score==5,1,0), then uses that variable in glm(cooperated~opponent) and a figure titled "Joint cooperation". Under the author experiment's own payoff mapping, score==5 denotes F/F mutual defection, whereas score==8 denotes J/J mutual cooperation. This is a concrete static source-code outcome-label inversion risk. It is not a verified re-estimation of any paper's published coefficient or figure.

Direct CSV read: 3900 total rows, 1950 PD rows. PD action|score counts: 0|10=235, 1|0=213, 0|5=783, 1|8=718, 0|0=1. Therefore the Rmd score==5 flag selects 783/1950=40.15% of PD rows as “cooperated”; actual mutual cooperation by documented matrix corresponds to score==8, 718/1950=36.82%. The anomalous id153 CSV line3061 (action0,score0) remains incompatible with deterministic matrix and was preserved. One cannot infer the corrected regression sign, significance or the final published conclusion without running the exact author R analysis and tracing exported data.

Identity: 195 anonymous participants, 10 PD rounds each, human versus LLM. Round index inferred from contiguous rows; no explicit partner action or unique human dyad. Original file license for participant-level redistribution remains unconfirmed; no raw data redistributed. R073 fixed 100-round human-human direct replication: INELIGIBLE. E2 new predictive result=0; E3=0.

Next: independently reconstruct score-based cooperation variable and rerun author PD regression with participant clustering, conditional on permission and reproducible analysis environment. Preserve anomalous row and distinguish original Rmd definition from corrected alternative. Do not modify author files or infer causal effect from the coding discrepancy.
