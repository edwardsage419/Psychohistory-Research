# R126 / 05-002 Table 3: cross-column constraint on proposed weights (2026-11-15)

Scope: independent arithmetic audit of the **published rounded aggregate transcription**, not an original-human-data replay, not a correction to the author's table, and not an E2/E3 claim. Read-only scientific status: ACTIVE/provisional for itemwise provenance; existing bounded E1 unchanged.

## Inputs and identity

Main at selection: `2a81424a5326acb7ce00a02893f82ad2b532cc14`.
Primary project transcription: `research/R126/R126_FEHR_GAECHTER_2000_ORIGINAL_PGG_COSTLY_PUNISHMENT_TABLE3_SCIENTIFIC_REPORT_2026-10-20.md`.
Its four three-session vectors, in order [10-round no punishment, 10-round punishment, final-round no punishment, final-round punishment], are:
`[2.7,4.0,4.5]`, `[10.9,12.9,10.7]`, `[1.3,2.3,2.0]`, `[9.8,14.3,13.1]`.
Published Mean vector: `[3.7,11.5,1.9,12.3]`.
The underlying paper page and individual records were not newly fetched in this audit; all source numerals here are from the repository's existing transcription.

## New independent check

The previously proposed *illustrative* weights 5:4:5 yield the displayed-session weighted means:

* Ten-round no punishment: `(5*2.7+4*4.0+5*4.5)/14 = 52/14 = 3.714285714...`.
* Ten-round punishment: `(5*10.9+4*12.9+5*10.7)/14 = 159.6/14 = 11.4`.
* Final-round no punishment: `(5*1.3+4*2.3+5*2.0)/14 = 25.7/14 = 1.835714285...`.
* Final-round punishment: `(5*9.8+4*14.3+5*13.1)/14 = 171.7/14 = 12.264285714...`.

If each session number is a nearest-tenth rounded value, its underlying value differs from the displayed number by less than or equal to 0.05 (endpoint conventions matter). Therefore the weighted ten-round punishment mean for these weights lies within the 11.35 to 11.45 boundary; publishing 11.5 under ordinary half-up rounding requires at least 11.45. Since each component's upper rounding interval is open under the usual convention, the aggregate is strictly below 11.45. **Thus 5:4:5 cannot simultaneously explain the published 11.5 ten-round punishment Mean and 12.3 final-round punishment Mean under that shared-weight, ordinary-rounding assumption.** It remains a purely illustrative way to obtain 12.3 from the last column alone, and must not be presented as evidence of the author's actual weights.

For equal weights, the last-column displayed mean is 12.4. With usual nearest-tenth input rounding the underlying equal-weight mean lies in [12.35,12.45); its reported value cannot be 12.3 under conventional half-up rounding. This does not determine the author's actual computation rule.

A different, column-specific weighting, a different underlying aggregation unit, nonstandard rounding, or a transcription/printing issue remains possible. No claim about which occurred is supported by this audit. Source-level resolution requires original Table 3 notes, session denominators, and any reported Mean computation method.

## Acceptance and regression guard

Do not use 5:4:5 as a resolved explanation. When any candidate session weights are proposed, check **all four** Table 3 Mean columns against the same weighting assumptions and input rounding intervals, before assigning explanatory status. Keep the source's printed 12.3 unchanged. Do not infer individual-level predictive performance or causal identification.

New scientific closures: 0. E1/E2/E3 upgrades: 0. New human records: 0. CI: not run. Existing R126 frozen protocols and scientific conclusions unchanged.
