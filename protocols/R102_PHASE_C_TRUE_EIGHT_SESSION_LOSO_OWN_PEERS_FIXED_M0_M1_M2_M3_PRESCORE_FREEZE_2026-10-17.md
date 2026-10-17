# R102 Phase C: original human 8-session LOSO fixed own and previous six-person peer history M0–M3 PRE-SCORE FREEZE

Date: 2026-10-17. **FROZEN BEFORE ANY ORIGINAL CONTRIBUTION OR AUTOMATIC_DECISION VALUES ARE ACCESSED**. Earlier source Phase A2 genuine full-publisher MD5/SHA and Phase B2 **nonbehavior-only actual source roster** passed. Exact original CSV first-party file 419,189 bytes, official MD5 `56931608b717aea06105ad10a58ff937`, project full SHA256 `ebc8831011a1a3b4893a80ae158d5129ed0f35e57a8092eba36c6a7b0cbd4282`. B2 real anonymous roster counted **8 distinct `session.code`**, **180 distinct source participants**, **2,700 person-round records**, **15 contiguous rounds per source participant**, **450 complete six-person original group-rounds**, and four treatments **T1–T4 each with exactly 2 published sessions**. None of the source participant pseudonyms cross real source `session.code` values. Technical `participant._round_number` disagreed with source actual `subsession.round_number` in 2,520 records, so only the latter denotes the original game round. At B2 no contribution/choice values read. PESEN v0.1 and original R073 are unchanged.

## Exact target and legitimate information set

Observe for every real participant `i` and original `session s`, actual source `subsession.round_number t` and declared six-person group of prior round `t-1`. The target `Y_{i,t}=Contribution_{i,t}/Endowment_{i,t}`, provided the *actual source* endowment is finite strictly positive, contribution finite, >=0 and <= endowment, and source `player.automatic_decision` is exactly integer 0 or 1. **Any violation fails closed** without dropping or reencoding a game action. No imputation, fitting, clipping, parameter tuning, deletion of losing sessions or postscore treatment exclusions.

A participant's prior-round own normalized contribution `O_{i,t-1}=Y_{i,t-1}`. Their peer-history variable `P_{i,t-1}` is the **arithmetic mean of the other five humans recorded in that participant's actual source six-person group in round t-1**, each peer's contribution divided by their **own** round-t-1 endowment. The complete previous group is keyed by `(session.code, t-1, group.id_in_subsession, group)` for the focal source person at t-1. It is not permissible to derive peers from target-round t group assignments (potential future information). Group composition may vary with round; use only true previous-round membership. If any previous actor, position or complete peer group is absent, fail-closed, do not fill from another group.

Hold out **every one of the original eight full `session.code` at once** when computing the external training benchmark. M0 at target `t` is the **other** independent original session in the **same source treatment**'s mean `Y_{j,t}` at the identical original round t. As there are exactly two original sessions per T1–T4 treatment, there is one such training session per fold. All source person-rounds in the held-out session are excluded from M0. Other-source-session same-round values make this a *retrospective external-session source prediction benchmark*, **not chronological prospective prediction**.

## Exactly four fixed model scores, same target and no fitting

* `M0=mean(Y_{j,t}: other original session, same treatment)`
* `M1=O_{i,t-1}` (only own last source contribution)
* `M2=P_{i,t-1}` (only previous actual six-person group's other five contributions)
* `M3=0.5*M1+0.5*M2` (strict fixed half mixture, no outcome-adapted weight)

For each complete original source participant, score only targets `t=2,...,15`. Exactly **180×14 = 2,520 source participant-next-round targets** are expected if the original contribution columns satisfy source validity. Primary loss is mean squared error `(Y_{i,t}-M_k)^2` for each k at the identical set of 2,520 source actor-round targets. Smaller is better. Mandatory contrasts:
1. `MSE(M0)-MSE(M1)`: incremental predictive value of own history vs treatment external source mean.
2. `MSE(M0)-MSE(M2)`: previous peer history alone vs external source.
3. **`MSE(M1)-MSE(M3)`: whether adding previous peer history to own history by a PRE-FIXED half weight helps**.
4. `MSE(M0)-MSE(M3)`: combined previous group+self history vs M0.

Report all 8 independent original session-level gains with their positive/negative/zero counts, per-T treatment two original session summaries (do not name or expose their original codes), global means and group/participant action-count denominators. No pseudoindependent 2,520-session p-values. No claims of meta-analytic comparability between R095 binary Brier/R096 binary and this continuous contribution-fraction MSE. A positive M3 versus M1 is evidence of **additional previous group-member information under this frozen aggregator**, not a causal psychological social learning identification. A negative group-session is a required scientifically informative counterexample.

## Automatic contribution codebook and secondary diagnostic

Zenodo publisher calls `player.automatic_decision` an indicator that the *system* made a decision. **Primary full-source recorded-choice estimand includes BOTH manual and automatic original recorded contributions.** Do not call every such observation a voluntary human choice; source people provide the original decision environment. Report total actual automatic-target count and its distribution by source treatment/session. Pre-register one secondary simple diagnostic restricted to targets whose **current round** `player.automatic_decision==0`; reuse the *identical* four already-computed predictions with no refitting, report eligible target count and MSE. Previous-round actor and peer history may themselves contain automatic decisions; acknowledge secondary comparison therefore does not isolate purely human deliberation. Do not select or eliminate a treatment according to automatic-decision prevalence.

Report an additional fixed early `t=2..5` and later `t=6..15` contrast for primary all-recorded estimand, chosen before source scores; do not equate to R096's 100-round t2..25 early window.

## Validation and scientific limits

First write a pure synthetic fixture with multiple independent sessions under treatments, complete six-person previous group, heterogeneous endowments, 15 rounds, and deliberate counterexamples: missing person, swapped prior group, other-source fold leakage, two identical person-rounds, endowment zero, contribution>own endowment, invalid automatic flag, swapped signed group IDs, dropped stage and model postscore retuning. Enforce synthetic tests **before** reading any actual original contribution. All four models must score **the same source actor-round targets**, machine original source SHA verified, and an independent full file download + score rerun must yield **identical canonical output SHA256** before claiming reproducible real E2.

This is **new, separately pre-frozen group-peers model R102**, not a literal unchanged R073 own/single-opponent full feature and score-contract replication. E2 would mean retrospective leave-one-original-session-out on one experimental institution with eight original sessions and four treatments. It would not establish prospective E3, independent group-level social-learning causality, or any claim about centuries of historical evolution. PESEN v0.1 FROZEN.
