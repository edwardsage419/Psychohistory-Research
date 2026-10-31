# R318 S114 finite CPT dominance and ranking: scientific report
Date: 2026-10-31 UTC. Track R. Status: PARTIAL_E1_EXTENSION. Frozen prescore commit c12d3c90d447bd43963332be3f6d3e076a47bf78.

## Research question and provenance
Does the original R318 two-outcome, rank- and sign-tail valuation preserve first-order stochastic dominance (FOSD) across the complete finite original lottery universe? How does an explicitly incorrect normalization of mixed-sign decision weights change the conclusion? What is the ranking sensitivity between the identity and original illustrative noncanonical probability transforms?
Original R318 source is frozen: research/R318/r318_exact_cpt_rank_sign.py Git blob cf04581003cc60dde398ee3c557e2d0ea1c60493; original 36 valuations JSON blob f70d84f7db8c354cf6f02726dfbab2ddb2cffde3; original prescore protocol blob ea658979b3d25f1dca1d688c6a6cd8f1f6cd1d03. Original Tversky and Kahneman (1992), DOI 10.1007/BF00122574. Original R318 weights remain a NONCANONICAL illustrative transform, with no fitted behavioral parameters.

## Exact fixed universe and findings
All 18 original lotteries were paired as 306 distinct ordered comparisons per transform, 612 records total. FOSD uses objective CDF inequalities at the four frozen outcome thresholds, and CPT valuation uses exact rational rank/sign tails. The independently computed R and B results agree on every recorded comparison.
- Identity transform: 117 ordered FOSD pairs; 0 CPT dominance violations; 0 normalized-control violations.
- Noncanonical transform: 117 ordered FOSD pairs; 0 CPT dominance violations; 2 FOSD violations after an intentionally incorrect mixed-sign normalization.
- Across 153 unordered pairs, 9 strict rank reversals between transforms, 2 pairs with a tie under at least one transform, 11 total sign disagreements including ties.
- In the noncanonical transform, 4 ordered comparisons change valuation-difference sign under the incorrect normalization.

Prespecified counterexample 1: A=(-2,+1), p_low=3/4 versus B=(-2,-1), p_low=3/4. A first-order stochastically dominates B. Actual CPT values A=-673/209, B=-40/11, delta A-B=87/209 >0. The naive normalized mixed-sign A=-673/182 yields delta=-123/2002 <0, violating FOSD.
Counterexample 2: A=(-2,+2), p_low=3/4 versus the same B. Actual delta=98/209 >0, normalized delta=-1/1001 <0.
These are finite synthetic arithmetic counterexamples to the normalized negative control. They do not show a CPT violation or empirical preference behavior.

## Executed verification
R scorer archived at research/validation/r318_s114_fosd.js; all 612 source rows at R318_S114_ALL_612_ORDERED_COMPARISONS.csv and exact summary at R318_S114_EXACT_SUMMARY.json.
- V8 isolated execution of the exact archived R compute function regenerated CSV and JSON byte-for-byte equal to remotely fetched GitHub archives.
- All 36 original source valuations were compared on five fields each (180 exact field matches) against the original R318 JSON.
- B independent BigInt rational odds-based script verified all 612 remote rows, unique keys, original lottery identities, FOSD and signed-tail valuations, aggregate ranks, and witness values. Its eight archived mutation controls all rejected.
- Independently written Python 3 Fraction script ran locally and agreed on 306 rows and 117 FOSD cases per transform, 2 normalized violations, 9 strict reversals, 2 tie pairs and 11 sign disagreements. Its archived source matches the executed local Git blob 4d4cfd58bd2d9592b5274b997cadcee8f7936573.
- Native Node CLI on archived program: NOT_RUN. External blind replication: NOT_RUN. Real human holdout, empirical Brier/calibration, historical prediction: NOT_RUN.

## Unified acceptance gates
A01 PASS bounded exact finite question; A02 PASS original source identity and English paper reference; A03 PASS two independent exact implementations and V8 byte replay, native Node OPEN; A04 PASS negative-control counterexamples preserved; A05 PASS E1 synthetic only, E2/E3 OPEN; A06 PASS archive of report, sources, audit and handoff after commit verification (final commit to be read from Git history). Overall PARTIAL_E1_EXTENSION; original R318 PASS_BOUNDED_E1_ONLY unchanged.
No original239 crosswalk or 154 pending queue modification. R073 and PESEN v0.1 frozen. No model fusion or personal decision system.
