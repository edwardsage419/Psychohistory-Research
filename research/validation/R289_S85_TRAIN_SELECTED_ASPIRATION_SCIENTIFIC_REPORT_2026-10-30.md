# R289 S85: finite training selection of aspiration thresholds

Date 2026-10-30 UTC. Track R. E1 artificial, internal nonblind, NEW_SUBSTUDY_PARTIAL. Original R289 CLOSED_BOUNDED_E1 status unchanged.
Prescore protocol commit f018236900fa00368c8980db5402ce4267d59c7c; original R289 freeze commit 27fa695d5e0c612fd77fb3a3fc5af26a543c0a27. The original R289 six population means were already known before S85, so this is not a blind replication.
Theory pointer: Herbert A. Simon (1955), A Behavioral Model of Rational Choice, QJE 69(1):99–118, DOI 10.2307/1884852. The four-offer scenario is this project's constructed toy model.

## Question, data and scoring
Original iid four-offer values {1,3,5}, three frozen DGPs, two frozen aspiration policies H3 and H5, additional inspection cost 1/2. From m=1 or m=2 COMPLETE training episodes, retrospectively score BOTH policies on the same training offer sequences; select H5 if its mean net is strictly greater, else H3 (including ties). Evaluate the selected policy's expected net on an entirely new iid episode. This is an exact expected future reward, not an observed empirical test sample.
Training must expose all four offers even if a threshold would have stopped early. This full-information training assumption is stronger than actual online stopping data. The test episode is never used to choose a policy.

Fixed original baseline expected net H3/H5:
UNIFORM 67/18 versus 100/27; LOW_HEAVY 27/8 versus 197/64; HIGH_HEAVY 133/32 versus 35/8. Fixed first-only expected rewards 3, 5/2, 7/2 respectively.
Regret is relative to the better FIXED H3 or H5 population mean, excluding any future-knowing maximum.

## Exact results
| DGP | m complete training episodes | P(select inferior threshold) | P(training tie) | Expected fresh test net | Regret vs best fixed H |
| --- | ---: | ---: | ---: | ---: | ---: |
| UNIFORM | 1 | 25/81 = 30.864% | 14/27 | 8128/2187 = 3.716507 | 25/4374 = 0.005716 |
| UNIFORM | 2 | 2819/6561 = 42.966% | 212/729 | 657971/177147 = 3.714266 | 2819/354294 = 0.007957 |
| LOW_HEAVY | 1 | 55/256 = 21.484% | 9/16 | 54251/16384 = 3.311218 | 1045/16384 = 0.063782 |
| LOW_HEAVY | 2 | 19569/65536 = 29.860% | 2691/8192 | 13783965/4194304 = 3.286353 | 371811/4194304 = 0.088647 |
| HIGH_HEAVY | 1 | 93/128 = 72.656% | 43/64 | 17269/4096 = 4.216064 | 651/4096 = 0.158936 |
| HIGH_HEAVY | 2 | 4533/8192 = 55.334% | 469/1024 | 1115149/262144 = 4.253956 | 31731/262144 = 0.121044 |

All exact source weights and policy payoffs are stored in the 243-row paired-offer ledger. For each DGP the m=1 source universe has 81 ordered episodes and m=2 has 6561 ordered training pairs. Every world has probability mass 1. Training ties are retained and deterministically select H3.

## Mechanistic reading and negative results
With only one or two COMPLETE training episodes, choosing the threshold that appears best on the training sample has nonzero regret on an independent episode in all three DGPs. The population-optimal threshold is H3 for UNIFORM and LOW_HEAVY, and H5 for HIGH_HEAVY.
More training is not guaranteed to improve *finite-sample expected performance monotonically* under this fixed tie-breaking rule: from m=1 to m=2 the wrong-selection probability rises for UNIFORM and LOW_HEAVY, while it falls for HIGH_HEAVY. This is a finite-sample counterexample; it is not a statement that more data are harmful in general.
All six selected policies still beat the frozen FIRST_ONLY baseline in population expected reward. PERFECT_FORESIGHT_MAX is an infeasible hindsight benchmark, excluded from regret.
The full-training-offer assumption can produce optimistic estimates of what a stopped real agent could learn. This study contains no actual human decisions, no real-world model fit, no causal inference and no cross-experiment validation.

## Reproduction and acceptance
Frozen original source CSV research/R289/R289_ALL_486_ORIGINAL_SEQUENTIAL_OFFER_SOURCES.csv Git blob 261d821044278d05db1d15e85e20cef8aafbe5a4. New R script research/validation/r289_s85_train_selected_aspiration_20261030.js, 243-row CSV research/validation/R289_S85_ALL_243_PAIRED_OFFERS.csv, exact JSON research/validation/R289_S85_EXACT_RESULTS.json. Original R script/JSON unchanged.
R V8 source was executed and produced six exact worlds, independently checked by signed-difference polynomial convolution. Five ledger mutations (duplicate, missing, weight, payoff, difference) and a sixth wrong-tie negative control were rejected. B separately ran Python Fraction exact convolution locally and verified all six probability outputs, including nine positive assertions; the archived Python file has not been executed as native remote bytes.
An independent remote-persisted comparison checked all 486 original source CSV policy rows against the 243 new paired rows: all payoffs, probabilities and signed differences match. The six new probability summaries match a separately reconstructed signed-difference distribution. These are internal nonblind computational checks, not an external team replication.
A01 PASS bounded question; A02 PASS original source fixed Git blob; A03 OPEN archived native Node and archived B Python CLI; A04 PASS six negative controls and all ties retained; A05 PASS artificial E1 scope; A06 OPEN external independent review and full native archive replay. SCIENTIFIC_ACCEPTANCE=PARTIAL.
New human E2 predictions 0; historical E3 0; external independent replication 0. R073 model/scoring and PESEN v0.1 FROZEN. No paid tools, datasets or Actions were initiated; actual account billing and free quota not checked.
