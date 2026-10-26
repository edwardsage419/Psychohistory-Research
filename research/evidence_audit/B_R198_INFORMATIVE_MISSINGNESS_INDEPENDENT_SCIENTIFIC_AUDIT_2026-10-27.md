# B audit: R198 informative missingness independent integer-path check

Date: 2026-10-27. Scope: internal independent algorithm and evidence audit for the third-method R198 addendum. Prescore freeze: `c9e3c76157caddb34c494782acd6ab6994b4268c`.

## Independent route

R uses forward filtering, conditional missingness likelihoods, and an analytic binary Brier formula. B separately enumerates the complete X0..X[T+1] latent paths, all Y1..YT observations, both M values, and the genuinely new Y[T+1] outcome. Each elementary path receives an integer numerator under a shared denominator `2 * denominator(a)^(T+1) * denominator(r)^(T+1) * 4`. No R filter function, R posterior, or R future probability is imported.

The B algorithm sums all atom masses by visible prefix, whether YT is missing, and the future outcome. It reconstructs the exact conditional probabilities from these integer joint masses, and integrates both forecasts' Brier losses directly over future outcomes. It also derives the IGNORE_M prediction from the full prefix joint mass, without reading R's forecasts.

## Executed results

32 frozen comparisons; 327680 atom contributions enumerated; 32 exact source normalization checks passed. 352 main versus B field comparisons passed, with 0 mismatches. These compare parameter keys, missingness probabilities, complete Brier risks, missing-conditional risks, and the exact squared-forecast-gap identity.

The MCAR channel yields 16 exact zero excess-risk controls. All four a=1/2 informative settings also yield exact zero excess risk. Twelve informative dependent settings yield positive excess risk. B additionally replaces the informative channel used by the predictor with its reversed likelihood. This deliberately wrong observation model strictly increases missing-case risk in all 12 dependent informative settings, as required by the frozen negative-control plan.

Both archived scripts and JSON receipts were re-fetched from GitHub and actually executed in a fresh JavaScript function environment. All 32 generated rows matched the archived rows for each route.

## Evidence limits

The exact checks demonstrate reproducibility of this fixed, fully artificial known-parameter state-space experiment. No parameter fitting, confidence interval, real sample calibration, independent external replication, or R073 frozen transfer was performed. The original R198 bounded E1 acceptance remains unchanged. E2 human=0, E3 historical=0, external independent replication=0. The programmatic separation of R and B does not establish independence of researchers.

Archived B program: `research/evidence_audit/b_r198_informative_missingness_independent_20261027.js`; machine receipt: `research/evidence_audit/B_R198_INFORMATIVE_MISSINGNESS_32_EXACT_AUDIT_RECEIPT_2026-10-27.json`. No CI triggered; any later CI claim requires a matching commit and run check.
