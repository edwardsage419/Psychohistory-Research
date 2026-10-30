# R301 S97 prospective freeze: hazard misspecification and genuinely held-out artificial fifth observation

UTC date 2026-10-30. Baseline main HEAD eb1e40292489d0637e456b72f361da815da19de3. This new study is an additive E1 exact artificial extension. Original R301, its frozen protocol and acceptance, R073 and PESEN v0.1 are unchanged. No real E2 or E3 claim.

## Question and independent predictive evaluation

For the original Beta(1,1) Bernoulli BOCPD with inclusive run length, use a fixed true hazard h* in {0,1/4,1/2}. Generate all 16 four-bit histories under that exact true model. For each history, the *fifth* bit is an unobserved, independently generated conditional future outcome. Score a candidate model using a fixed assumed hazard h in {0,1/4,1/2}, with no fitting or post-hoc selection. All 3x3x16x2=288 fully enumerated joint outcome atoms are retained, including positive and zero masses. Score q=P_candidate(Y5=1|Y1:4) with Brier loss (q-Y5)^2. Probability of each atom = P_true(history) P_true(Y5|history). The true model's conditional forecast is the oracle. Also score the constant q=1/2 baseline. Report nine mean Brier risks, oracle risk per true hazard, constant baseline 1/4, and nine nonnegative exact excess risks.

## Frozen evaluation gates

Use exact Python Fraction, deterministic history order lexicographic, candidate hazards in the listed order, outcomes 0 then 1. Preserve 288 rows with unique (true hazard, assumed hazard, history, outcome). Each true hazard's 32 unique joint atoms sum to 1; the same true atom masses repeat across assumed hazards and must not be counted as independent data. For each pair, sum joint mass * squared loss. Independently compute regret as sum over unique histories P_true(history)*(q_candidate(history)-q_true(history))^2. Require exact equality to Brier candidate minus Brier oracle. When assumed hazard equals true hazard, regret is zero. All conditional forecasts must be within [0,1]. No sample-level confidence interval, no empirical calibration or real changepoint inference.

## Independent B track prespecified before outcomes

Independently enumerate the 2^3 segmentation vectors for each 4-bit history under each hazard, integrate each segment with Beta factorial marginal likelihood and evaluate the fifth-bit predictive by enumerating 2^4 segmentations. This independent B oracle shall not import the original R301 code or the R S97 generator. Compare all 288 source rows, nine risks, nine regrets and exact source universe. Mutation tests must reject duplicated atom, omitted atom, tampered joint probability, candidate forecast, outcome, risk summary, and false E2 promotion. Record all failures and run context. B internal nonblind replication is not external independent team replication.

## Scientific scope and operations

No tuning, no human/animal data, no historical event forecast, no paid service or Actions dispatch. Preserve original R301 formal acceptance, R073/PESEN freeze, original239 index and pending queue. Code execution and repository archive are distinct from scientific validation. CI may be NOT_RUN. A data track independently checks a real public dataset and records explicit R073 eligibility gate. Additive paths only; verify main HEAD, target paths and concurrent PR before every write. [skip ci].
