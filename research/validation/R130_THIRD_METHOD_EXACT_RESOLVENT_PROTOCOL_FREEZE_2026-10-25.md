# R130 third method exact state-resolvent protocol freeze

Date: 2026-10-25. State: FROZEN_BEFORE_NEW_IMPLEMENTATION_AND_RESULTS. Original239 05-006 Repeated Games. Reuse the existing R130 research and 65 tests unchanged. Primary first-hand anchors are Axelrod and Hamilton (1981), Science DOI 10.1126/science.7466396, and Nowak and Sigmund (1993), Nature DOI 10.1038/364056a0. Original R130 Python source Git blob acc82d15b23de015ca8e448cf622b077a4e8e6cd. No claim of original tournament or population simulation rerun.

## Independent method

For the original five project-audited deterministic strategies TFT, ALLD, ALLC, ALT_DC, WSLS, construct a deterministic finite-state transition graph from scratch, without importing the original R130 policy or cycle-detection functions. State is (previous realized action pair or initial empty history, parity of the next turn). Start at (empty, even). Implement the 1981 payoff matrix R=3, S=0, T=5, P=1 and the 1993 WSLS mapping CC to C, CD to D, DC to D, DD to C. TFT copies the other player's previous realized action, ALLD always D, ALLC always C, ALT_DC chooses D on even turns and C on odd turns. No implementation errors are injected for this primary comparison.

Enumerate only reachable states for each ordered strategy pair, construct a transition matrix P and immediate row/column payoff vectors. Solve (I-wP)V=r with exact rational Gaussian elimination, independently for each player, to obtain the initial state's infinite discounted payoff. Do not use cycle decomposition, closed-form geometric sums or original R130 functions to construct these values. Compare only after construction with the unchanged original independent_infinite_state_cycle_value function. Require exact equality for 25 ordered pairs and seven frozen discounts w in {0,1/4,1/2,3/5,2/3,4/5,9/10}, totaling 175 two-player exact payoff comparisons (350 scalar identities). Verify state count in 1..10 and matrix equation residual exactly zero in every state.

Frozen source-based controls: TFT/TFT at w=3/5 equals 15/2, ALLD/TFT equals 13/2, ALT_DC/TFT equals 125/16; TFT against ALLD no-invasion boundary w>=1/2, TFT against alternating DC boundary w>=2/3; w=3/5 passes only the first. One-sided first-turn error recovery of WSLS and TFT is outside this new resolvent computation and remains under original R130 evidence. Reject a deliberately altered original comparison value and an altered row payoff input. Any mismatch fails.

Archive full 175-row deterministic CSV, independent source, exact original source Git identity check, a scientific report and CI receipt if run. Original 65 tests must pass unchanged under Python 3.11 and 3.12. If the program or frozen counts fail, report failure without altering the frozen grid or acceptance conditions.

## Scope and operations

Maximum evidence is project-internal finite E1 mathematical replay. No new human E2, historical E3, external-team independent replication, empirical calibration, causal identification or real-world forecast. Original R130, R073 and PESEN v0.1 stay frozen. No modification of existing original239 overlays until the new result and CI are verified. Use only public repository standard Ubuntu runners after checking their free status. No paid API, data, cloud or GPU.
