# R298 S94 prescore freeze: noisy scenario notification and planning regret

Date: 2026-10-30 UTC. Track R. Key (r,R298,S94-v1,scenario-label misnotification and exact regret). Baseline main HEAD c560a57978fcee13b352e6adce83b8049974290a. This file is committed **before S94 computations**. All original R298 protocol, 64 source rows, code, final bounded E1 acceptance, original239 v7.8, pending154, R073 and PESEN v0.1 remain unchanged.

## Question and finite artificial universe

How does imperfect externally communicated environment identity change exact regret of the original known-model planner versus a fixed baseline value cache? This is a **synthetic four-scenario communication error**, not world-model learning or human behavior.

Reuse exact original R298 environment mapping/reward: BASELINE (L->S1=2,R->S2=1), REWARD_SHIFT (L->S1=0,R->S2=3), TRANSITION_SWAP (L->S2=1,R->S1=2), BOTH (L->S2=3,R->S1=0). Terminal discount gamma in {1/2,1}. No postchange experience, no fitting. Original model-based planner acts on the communicated scenario label M, cached controller always acts on BASELINE. LEFT wins exact ties. Actual environment T is hidden from the planner and used for evaluation only.

Fix symmetric conditional message probabilities for each actual T:
P(M=T | T,e)=1-e and P(M=m | T,e)=e/3 for each of three other m. e in {0,1/4,1/2,3/4,1}. Message probability may be zero, retain those rows. The four labels are equally weighted for a *synthetic descriptive aggregate* only, not a population prior. Controllers: MODEL_BASED_PLANNER and CACHED_VALUES. Cross 4 T x 2 gamma x 5 e x 2 controllers = **80 worlds**. Each world has four message branches = **320 message branches**, each two action-level source rows = **640 action rows**. No stochastic reward beyond the message channel.

## Frozen metrics and expected tests

For every branch, compute actual discounted action Q from T, predicted Q from M for planner or BASELINE for cache, chosen action, actual oracle, regret=max actual Q - actual Q(chosen), message probability. Exact Fraction arithmetic. For each world compute expected regret and wrong-choice probability by summing over all four messages. Aggregate over four equally weighted actual T separately for each gamma/e/controller. Record 80 world results, 320 branches and 640 action rows with unique keys and exact probability mass 1 per world.

Primary contrast: equal-T average expected regret planner versus cache for each gamma and e. Predeclared algebraic expectations: planner wrong-choice probability 2e/3 in all four T; planner expected regret 2e/3 times actual action gap (BASELINE gamma, REWARD_SHIFT 3gamma, TRANSITION_SWAP gamma, BOTH 3gamma). Cache wrong-choice probability 0 in BASELINE and BOTH and 1 in REWARD_SHIFT and TRANSITION_SWAP. Equal-T mean planner regret 4e*gamma/3; cache mean gamma. Equality at e=3/4, planner lower for e<3/4, higher for e>3/4. Negative control: at e=0 planner regret 0, at e=0 cache reproduces original R298 outcomes; at e>0 wrong messages can harm BASELINE and BOTH. These are algebraic expectations to be falsified by implementation.

## Gates and boundaries

R route: standard-library Python Fraction, read and SHA256-bind original R298 CSV, check its 64 rows and world factors, then independently construct the 640-row S94 extension. Must fail on source mismatch, duplicate/missing world/message/action, probability errors, incorrect message label, altered Q/choice/regret, incorrect summaries, and E1->E2/E3 promotion. Generate CSV/JSON, self-tests, machine receipt, report. B route: separate no-import exact algebraic oracle and mutation controls, compare all 80 world results and original 32 world decisions against original R298. Record tested versus untested native commands and GitHub CI truth. Scientific status S94 PARTIAL unless all independent reproduction and archival gates close.

This protocol adds one bounded sensitivity test only. It cannot infer causal effects of messages in real humans, learned model reliability, actual population error rates, calibration, or independent E2/E3 replication. No additional expense or paid runner. If CI billing-free eligibility is unconfirmed, skip Actions. Do not edit original sources, crosswalk, pending queue, or original acceptance.