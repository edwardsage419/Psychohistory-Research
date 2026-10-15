# R065 Phase E frozen retrospective protocol: Day-89 reset-to-uniform bound

Date: 2026-10-16. Status: retrospective analysis plan submitted BEFORE the new exact-source numeric calculation. The Phase C mismatch and Phase D model results were already known.

Question: given public objectives.py reset guards all reset state at day=89, what is the out-of-subject predictive loss of the implied two-action uniform choice forecast compared to a minimal cross-person day-89 rate? This does not fit or rerun the full seven author models.

Source: Levy et al. processed CSV blob `01bf211468abe093618dfa5e5c39e883230c9c03`; author objectives.py blob `5e98133fa274ef2a112b24f6fdcd802d4f9d3eec`; normalized 3-token boat transition rows and exactly two choices, as in the original author data.

Rules fixed before computation:
1. Full-trial author exclusion criteria: participant accuracy below .45, participant average comprehension repetitions greater than 2; union excludes. Only eligible participants with exact eight critical days 4,21,38,55,72,89,106,123 and exactly 4 high/4 low retained.
2. Restrict to day 89 `critical == 1`; enforce `accurate+copied=1`. Under original source function on day 89 the copied-choice probability is analytically 1/2 for models 1 through 7, subject to the publicly observed two-alternative and row-normalized transition structure.
3. Counterfactual comparator: per participant, use the Beta(4,4) posterior mean from the OTHER eligible day-89 participants only: `p_{-i}=(sum_j copied_j-copied_i+4)/(N-1+8)`. Single binary outcome per person.
4. Report `loss_uniform - loss_comparator` and `brier_uniform - brier_comparator`, positive when the simple comparator performs better. `loss_uniform=log(2)`, `brier_uniform=0.25` per person.
5. Report exactly 20,000 person-level paired bootstrap draws of frozen per-person loss differences with xorshift32 seed `20261016`; percentile indices floor(.025*(draws-1)) and ceil(.975*(draws-1)); no refitting inside bootstrap. Include day89 rates by high-vs-low and first-high/first-low counterbalance only as descriptive totals, without separate effect inference.
6. Cross-check day89 number of copied choices against previously published R065 Phase B block 6 rate, expected 73/226, and no test participant data in training. For completeness compare uniform to training base rate, but DO NOT claim actual seven-model published fit improves by changing reset code. This analysis is intentionally post hoc and has no new experimental cohort.

Important limitations: Since original source is reset at day89, the exact 0.5 prediction is derived from its initialized state and normalized task transition rows; proving local runtime behavior still requires exact source code and trials. The copy vs emulation labels are author-generated proxies. Predictive difference from a fitted cross-subject prior cannot identify cognitive strategy, causal learning, or publication error. PESEN v0.1 remains FROZEN.
