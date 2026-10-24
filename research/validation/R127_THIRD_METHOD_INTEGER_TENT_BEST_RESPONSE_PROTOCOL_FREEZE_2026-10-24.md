# R127 third-method integer tent-payoff and best-response protocol freeze

Date: 2026-10-24. State: FROZEN BEFORE THIRD-METHOD CODE AND RESULTS. Original239 next item 05-003 Coordination Game; strict reuse existing R127.

## Original sources and prior scope

Van Huyck, Battalio and Beil (1990), *Tacit Coordination Games, Strategic Uncertainty, and Coordination Failure*, AER 80(1):234–248. Original publisher scan https://econweb.ucsd.edu/~jandreoni/Econ264/papers/Van%20Huyck%20et%20al%20AER%201990.pdf . Existing R127 read printed Eq.(1), treatment A payoffs and original Table 2, and has 60 unit tests, 2793 complete finite group profiles, 75117 artificial deviation checks, 1296 constructed symmetric 2x2 games, CI success 39348775741. Existing original source Git blob `6964fa57e291e719e8cc071cc3a70d73836363e4`, test Git blob `1e9338c5a8504d86d3032b139ab3f9546907d1ec`, report Git blob `df3be9770d0a762b8564d08652736353d3b0c7c0`.

## Falsifiable third-method finite protocol

For n=2,3,4 enumerate every ordered integer effort profile from `{1,2,3,4,5,6,7}^n` (49+343+2401=2793 complete profiles). For each participant independently calculate integer payoff numerator `10*u_i = 6 + 2*min(e_1,...,e_n) - e_i`, denominator 10, with no call to original R127 payoff helpers. Compare each person with the unchanged original `payoff_vector(profile, experimental=True)`; expected 10731 person-payoff exact comparisons. Archive one row per complete group profile containing n, efforts, integer payoff numerators, minimum and exact comparison flag.

Independently enumerate each ordered opponent effort profile of lengths 1,2,3 (7+49+343=399) and each own effort 1..7 (2793 artificial candidate deviations). Derive `q=min(opponent efforts)`; use piecewise integer formula `10u=6+e` for `e<=q`, and `10u=6+2q-e` for `e>=q`. Require exactly one maximizing own effort, equal to q, for every opponent profile. Compare this third-method best response with the unchanged original R127 best response or payoff evaluator without modifying the original model.

Frozen controls: all-one efforts payoff 7/10 each, all-seven payoff 13/10 each, one effort 7 versus opponent effort 1 payoff 1/10, nonuniform (1,7,7,7) gives payoffs [7/10,1/10,1/10,1/10]. Reject wrong original source Git blob and mutated raw CSV. Rerun unchanged 60 tests under Python 3.11 and 3.12 using public standard free Ubuntu runners.

Published Table 2's 107 human participants are author-reported aggregate evidence, not newly acquired individual records. Distinguish maximin security effort 1 from risk dominance in a two-player 2x2 game. New E2=0, E3=0; no new empirical learning mechanism or external replication. Maximum acceptance `PASS_BOUNDED_INTERNAL_INTEGER_TENT_BEST_RESPONSE_E1`. Preserve R073 and PESEN v0.1 frozen. Do not decrement original239 pending until execution, report, machine CI and formal acceptance.
