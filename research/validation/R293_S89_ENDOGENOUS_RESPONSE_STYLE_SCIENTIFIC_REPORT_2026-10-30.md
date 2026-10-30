# R293 S89 scientific report: endogenous common response style can mask opposite latent values

Date 2026-10-30 UTC. Track R primary. Scientific status PARTIAL, synthetic E1 only, internal nonblind. This is a bounded sensitivity increment to original R293, whose formal CLOSED_BOUNDED_E1 acceptance remains unchanged.

## Freeze and provenance

Prospective S89 protocol was committed before this run's S89 outputs at a0a862befbf99ad5e350cdd2ae83aec02df6c2c4. The complete 2112 new source rows and exact four-world result JSON were committed at 24881b95b1fee8dc33b4a9a9674ad43302c69e3c. Original R293 frozen source data, result and 153-test status are preserved, not overwritten.

Sources: original R293 theoretical scope uses Schwartz 1992 DOI 10.1016/S0065-2601(08)60281-6, Schwartz 2012 DOI 10.9707/2307-0919.1116, and GESIS ESS Human Values Scale guidance https://zis.gesis.org/s/skala/Schwartz-Breyer-Danner-Human-Values-Scale-%28ESS%29?lang=en. This S89 experiment uses only ten artificial 0/1 value slots and shared shifts, never original survey responses.

## Exact design and complete sources

INDEPENDENT has 1024 latent ten-bit profiles; OPPOSED_PAIRS has 32 latent five-bit profiles expanded into five exact complementary pairs. Two new style mechanisms S=2*b0 and S=2*(1-b0) each reuse both latent worlds. Four worlds contain 1024+1024+32+32 = 2112 complete labeled synthetic sources. Within each world source mass sums to exactly 1. Each source records latent vector, response-style shift, raw vector, centered vector and rational mass.

Full source CSV: research/validation/R293_S89_ALL_2112_ENDOGENOUS_STYLE_SOURCES.csv, 278377 bytes, SHA256 a6632e8ddeded5efe7e82a1dc5a7f9c67bd6a0168f7d3f7a1e96e46bc29c16fd, Git blob 61e7c480fca45972760e37c72ed3e8e148603b13.

Exact result JSON: research/validation/R293_S89_EXACT_RESULTS.json, 17786 bytes, SHA256 47f2bac6dbe2231f5bb33630e388a52741807b6159d5e9854d70347b0c5d4f9b, Git blob 33fadc22d56f2fbb85cc34401c79668b31808a51.

## Main results

| Latent world | Style mechanism | Raw Cov(slot0,slot5) | Raw Var(slot0) | Raw Var(slot5) | Raw corr(slot0,slot5) | Centered corr(slot0,slot5) |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| INDEPENDENT | ANCHOR_PLUS | 3/2 | 9/4 | 5/4 | 2/sqrt(5) | -1/9 |
| INDEPENDENT | ANCHOR_MINUS | 1/2 | 1/4 | 5/4 | 2/sqrt(5) | -1/9 |
| OPPOSED_PAIRS | ANCHOR_PLUS | 3/4 | 9/4 | 1/4 | +1 | -1 |
| OPPOSED_PAIRS | ANCHOR_MINUS | 3/4 | 1/4 | 9/4 | +1 | -1 |

For the OPPOSED_PAIRS world, latent slots 0 and 5 are perfectly anticorrelated by construction. Their observed raw scores become perfectly positively correlated under either anchored response style. The earlier original R293 independent-style mechanism had raw correlation +3/5 for the same artificial opposite pair. Thus endogenous common style can strengthen the reversal even with identical latent-value distribution.

In all four worlds, subtracting the respondent's ten-slot mean removes any shared additive shift pathwise. All 400 centered covariance entries across the four worlds agree with their corresponding original R293 latent-world matrices. Independent latent slots still show centered correlation -1/9 due to the zero-sum constraint. Centering alone therefore does not establish substantive opposition or validate an empirical value circle. The uncentered absolute levels of the latent scores are not recovered by the centered profiles.

The four 10x10 raw and four 10x10 centered matrices contain 800 exact covariance entries. Full enumerated moments and a separately implemented latent covariance linear-transform oracle agree in every entry. The B route audited all 2112 source rows and rejected eight injected defects. Internal nonblind mathematical cross-check PASS.

## Scientific limits and next gates

This is an artificial measurement-identifiability counterexample, not a causal estimate of actual response style, not a validated 21-item ESS/PVQ score, and not a real cultural-value replication. No real human E2 or historical E3 was added. Formal S89 acceptance PARTIAL. The archived JavaScript has been exercised by V8 source construction but native Node CLI on the persisted remote checkout remains NOT_RUN. The independent Python script ran locally on exact-byte-identical source/result files; its remote checkout CLI remains NOT_RUN. External team replication NOT_RUN. No new GitHub Actions were launched because free-billing eligibility was not confirmed. Original239 v7.8, pending154, R073 and PESEN v0.1 unchanged.

Next R294 complementary study only after checking fresh HEAD, coordination and pending work. Original R293 closed bounded status must not be upgraded by this S89 increment.
