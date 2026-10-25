# R170 third-method prescore freeze: naming-game observation ladder

Date: 2026-10-26 Asia/Singapore. Track: R main. Evidence target: internal exact E1 only. This protocol is an append-only extension to the previously closed R170 finite four-agent naming game; the original protocol, results, R073 and PESEN v0.1 remain unchanged.

## Prior facts and source identity

Original catalogue P2 / 07-012, R170 CLOSED_BOUNDED_E1. Read original protocol `protocols/R170_TWO_WORD_NAMING_GAME_72_INVENTORY_MARKOV_WORLDS_PRESCORE_FREEZE_2026-10-21.md`, original source and scientific report. Baronchelli et al. 2006 DOI 10.1088/1742-5468/2006/06/P06014 motivates naming games, but this project's two-token noisy channel and feedback alternatives are artificial and are not original-author code. Original 72 exact worlds and timepoints t=0,1,2,3 are already known; do not count reexecution as a new independent empirical result.

## Prespecified question and frozen grid

Can observing bilingual memory counts, word-inventory histograms and contact-local mismatch statistics identify the channel-noise and listener-feedback controls as well as observing each labeled individual's complete inventory?

Keep exactly four fixed graphs path, star, cycle, complete; three fixed initial inventories split=(1,1,2,2), alternate=(1,2,1,2), bilingual=(1,3,2,3); noise nu in {0,1/4,1/2}; feedback in {both_confirm,listener_only}; four masks 1=A, 2=B, 3=AB; original edge selection, orientation, utterance, independent token flip, recognition and feedback rules. For each graph and initial-inventory stratum compare its six controls, never compare different starting strata. Exactly 12 strata, 72 worlds, 180 within-stratum unordered pairs.

At t=1,2,3 compute the exact law of four nested observations:
* O1: total number of bilingual inventories (mask 3).
* O2: three-element histogram of inventory masks (number A-only, number B-only, number AB).
* O3: O2 histogram plus the number of fixed contact edges with disjoint endpoint vocabularies (bitwise intersection zero).
* O4: complete labeled four-person inventory vector.
Each O is a deterministic coarsening of O4, with O2 refining O1 and O3 refining O2. Use exact Fraction/BigInt rational arithmetic. Equal laws are equal only if every rational state mass matches. Report per time and observation the sum of within-stratum equivalence classes, uniquely identified worlds, ambiguous worlds, and distinguishable control pairs out of 180. Report O1 to O4 refinement monotonicity, including whether O3 adds any distinctions.

## Witness, negative controls and independent route

Select the first lexicographically ordered stratum/time/control pair, if one exists, with TV(O1)=0 and TV(O4)>0; print both exact rational distances. A missing witness must be reported as absent without retroactive substitution. For each of the 12 strata, verify at nu=0 that both feedback modes yield identical first-step laws for the two initially all-monolingual patterns. Also verify that all state masses normalize exactly, all inventory masks remain in {1,2,3}, and graph edges remain fixed. Execute a mutation control replacing nu=1/4 by nu=1/3 for path/bilingual/both_confirm at t=1, while leaving all other parameters unchanged; require a nonzero O4 TV or report failed mutation sensitivity. This out-of-grid perturbation is a negative control, not an admitted R170 model world.

Main route: independently enumerate directed speaker-hearer contact pairs and the delivered A/B mixture, then propagate exact joint inventory-state distributions. Independent B route: independently enumerate undirected edges, orientations, speaker-held word, and channel-flip branches, applying feedback with a separately coded transition routine. Compare all 72 worlds at all four timepoints with exact state-level equality. The B route must not import/call the main route. Record first failures and any corrections.

## Acceptance and boundaries

Freeze before executing any new third-method code or observing its results. New source, compact receipt, scientific report and B audit must occupy distinct append-only paths. Preserve old files and the shared original239 v7.8 crosswalk and 154-item queue. Third-method PASS requires full exact cross-route equality, normalized laws, the stated controls and correct disclosure of failures. New E2 real human predictions=0, new E3 history predictions=0, external research-team replications=0. No claims of grammar acquisition, actual language change, empirical identification, population scaling, or original-author replication. No new costs or GitHub Actions without independent zero-cost confirmation.