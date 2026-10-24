# R342 original239 04-021 SAOM: prescore three-actor local choice protocol v1

Date: 2026-10-24. Status: FROZEN_BEFORE_R342_SOURCE_GENERATION.

## Sources and reuse
See docs/ORIGINAL_239_04-021_SAOM_REUSE_PREAUDIT_2026-10-24.md for Snijders 2001 and Snijders et al. 2010 and the scope comparison to R341, R317 and R314. Early binary ZIP audit remains OPEN.

## Exact artificial universe
Three actors 0,1,2. Six directed edge bits ordered (0->1),(0->2),(1->0),(1->2),(2->0),(2->1). Network strings from "000000" to "111111" in increasing binary order. Actor order 0,1,2. For each actor, the two other target nodes are sorted ascending. Choice order stay, toggle_to_first_other, toggle_to_second_other. Two parameter worlds r="1","2". For a candidate resulting network, local reciprocity count u is the number of outgoing edges from the selected actor whose reciprocal incoming edge is present. Choice weight w=r**u. Normalize over the three choices to obtain exact Fraction probabilities. One local decision only; no global stochastic clock or multi-step simulation.

## Frozen output
CSV research/R342/R342_ALL_1152_ARTIFICIAL_ACTOR_CHOICE_ATOMS.csv. Header r,network_bits,actor,choice,target,result_bits,reciprocity,weight,probability. Exactly 2*64*3*3=1152 data rows in r,network,actor,choice order. For stay target is "NONE"; for toggles target is node index string. Choice strings exactly "stay","toggle_first","toggle_second". Use str(Fraction) for weight and probability, integer fields str(int), csv.writer lineterminator="\\n" interpreted LF, UTF-8 final LF.

JSON research/R342/R342_EXACT_384_LOCAL_DECISIONS.json. Top-level insertion order schema,checks,decisions. Schema "R342_frozen_three_actor_local_choice_v1". Checks insertion order worlds,networks,actors,decisions,source_rows,uniform_choice_decisions,normalized_decisions. Values worlds=2,networks=64,actors=3,decisions=384,source_rows=1152,uniform_choice_decisions=192,normalized_decisions=384. Decisions array ordered r,network,actor. Each object insertion order r,network_bits,actor,probabilities. Probabilities array is three canonical Fraction strings in frozen choice order. JSON dumps indent=2, ensure_ascii=True, final LF.

## Falsifiers
F1: exactly 2 worlds, 64 networks, 3 actors, 384 local decisions, 1152 original artificial choice atoms.
F2: every local decision has three nonnegative weights and probabilities summing to one.
F3: all 192 r=1 decisions are exactly (1/3,1/3,1/3).
F4: the two toggles modify only the chosen actor's outgoing tie, stay changes no bits, all resulting networks are valid six-bit strings.
F5: for r=2, local choice odds equal the ratio of 2**reciprocity across candidates.
F6: all frozen checks dictionary values and output bytes match.
F7: independent no-import auditor re-enumerates CSV and JSON exact bytes and rejects deliberate CSV and JSON tampering.
F8: Python 3.11, Python 3.12 and independent GitHub Actions jobs all success before formal acceptance.
F9: source commit follows this protocol freeze; R073 and PESEN v0.1 unchanged.

## Evidence limits
Potential PASS_BOUNDED_E1_CONSTRUCTED_THREE_ACTOR_LOCAL_CHOICE_ONLY. This does not establish full stochastic actor-oriented model, actor clock, longitudinal social network estimation, observed human E2, historical E3 or original-author empirical replication. Catalogue linkage is provenance only. Personal decision system deferred.
