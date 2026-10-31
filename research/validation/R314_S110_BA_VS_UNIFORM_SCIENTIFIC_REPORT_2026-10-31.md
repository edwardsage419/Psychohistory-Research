# R314 S110 scientific report: exact discrimination of preferential and uniform attachment

Date: 2026-10-31 UTC. Frozen protocol: `research/validation/R314_S110_BA_VS_UNIFORM_OBSERVATION_IDENTIFIABILITY_PRESCORE_FREEZE_2026-10-31.md`, commit `c1708f290390b348a6e7b0756c9ef3ec421f85d7`. Baseline main `6eeb7b2f76cdd3992bdab24bea7c8f0a896dba8c`. New extension acceptance: **PARTIAL_E1_EXTENSION**. Original R314 `PASS_BOUNDED_E1_ONLY` unchanged.

## Research question and prespecified comparison
Three original labeled connected seeds P3, K3, S4, exactly two sequential single-edge vertex arrivals. Compare original R314 degree-proportional BA mechanism with a uniform choice among existing vertices. Equal prior on the two mechanisms. No estimated parameters. Original 54 conditional source atoms (blob `063fd8b52f3aa425ccb9d61f26496d2db8365b9a`) and 44 BA paths (blob `e49b94e282fde0b2772af3a8d42b8ed84b000564`) remain immutable. Four prespecified observations: ordered target pair, final labeled degree vector, sorted degree multiset, and maximum final degree.

For distributions P and Q on an observation, total variation is TV=1/2 sum|P-Q|. With equal hypothesis priors, optimal classification accuracy is (1+TV)/2 and error (1-TV)/2.

## Complete exact result

| Seed | Ordered paths | Labeled degree cells | Sorted degree cells | Max degree cells | TV at all four observations | Optimal accuracy |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| P3 | 12 | 9 | 3 | 3 | 1/6 | 7/12 |
| K3 | 12 | 9 | 3 | 2 | 1/8 | 9/16 |
| S4 | 20 | 14 | 4 | 3 | 23/80 | 103/160 |

**Finding:** For these three finite seeds, two arrivals and this specific BA-versus-uniform pair, the final maximum degree alone preserves the same optimal equal-prior discrimination accuracy as the complete ordered attachment history. This equality is an exact finite result. It does not imply that maximum degree preserves the complete likelihood ratio, predictive information under every loss, or sufficiency in general preferential-attachment networks.

The final maximum-degree probability distributions provide a direct independent check:

| Seed | Maximum degree | BA probability | Uniform probability |
| --- | ---: | --- | --- |
| P3 | 2 | 1/6 | 1/3 |
| P3 | 3 | 7/12 | 7/12 |
| P3 | 4 | 1/4 | 1/12 |
| K3 | 3 | 5/8 | 3/4 |
| K3 | 4 | 3/8 | 1/4 |
| S4 | 3 | 5/16 | 3/5 |
| S4 | 4 | 7/16 | 7/20 |
| S4 | 5 | 1/4 | 1/20 |

Each maximum-degree bin contains no BA-versus-uniform path probability differences of opposite sign, which explains equality of total variation after coarsening. In the K3 negative control, the first arrival alone is exactly uniform under both hypotheses, TV=0; second arrival creates the 1/8 difference.

## Source and program checks
R generator enumerates all 44 distinct labeled paths, outputs complete 44-row CSV and 12-observation JSON using Fraction arithmetic. A separate nonimporting Python oracle computes second-step degree from the first selected target, checks every row, each likelihood ratio, each observation partition, exact total mass and TV. Both normal Python and `python -O` rejected all eight deliberately nonempty mutations. Remote original R314 54 source atoms were independently rechecked against exact degree numerators, denominators, old/new edge sets and old node counts: 54/54 PASS. Remote original 44 BA paths were separately rechecked with integer fraction cross-products and final edge identity: 44/44 PASS. These are **internal nonblind** source and mathematical checks.

## Scientific limitations
This is E1 finite artificial enumeration with no random samples or fitted models. There is no empirical held-out forecast, calibration curve, confidence interval, causal mechanism identification in humans, or external independent replication. Equal prior is a prespecified classification assumption. Real network arrival timestamps, growth-only event identity, exogenous edge formation and human behavior have not been verified. Neither power-law exponent nor real-world scale-free claim is evaluated. E2=0, E3=0. R073 and PESEN v0.1 frozen.

## Reproduction
From a checkout of this commit:
```sh
python research/validation/r314_s110_exact.py --out /tmp/r314_s110
python research/evidence_audit/b_r314_s110_nonblind_exact_oracle.py --csv /tmp/r314_s110/R314_S110_ALL_44_PATHS_BA_VS_UNIFORM.csv --json /tmp/r314_s110/R314_S110_12_OBSERVATION_TV_SUMMARY.json --mutations
python -O research/evidence_audit/b_r314_s110_nonblind_exact_oracle.py --csv /tmp/r314_s110/R314_S110_ALL_44_PATHS_BA_VS_UNIFORM.csv --json /tmp/r314_s110/R314_S110_12_OBSERVATION_TV_SUMMARY.json --mutations
```
Compare emitted files byte-for-byte to the two persisted research/validation outputs. No GitHub Actions dispatch is required.
