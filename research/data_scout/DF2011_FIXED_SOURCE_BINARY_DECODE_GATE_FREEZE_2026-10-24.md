# DF2011 independent source decoding gate, frozen before execution

Date: 2026-10-24. Parent HEAD inspected: `124c18bae7bd9fe94f2855b92e8d1b70a9f25779`.

## Scope and source

Dal Bó and Fréchette (2011), *The Evolution of Cooperation in Infinitely Repeated Games: Experimental Evidence*, AER 101(1):411–429, DOI 10.1257/aer.101.1.411. Fixed public CRAN mirror `cran/stratEst` commit `a6373b23d80dc816a63f18f973d372c9e8421914`; raw file `data/DF2011.rda`, Git blob SHA1 `52e216b02e1a7ab7fb1a6e335b5f7e2ef6b7f5a0`, size 3298 bytes. Official raw documentation `man/DF2011.Rd` declares 7358 observations and six fields. Data copyright and CC BY 4.0 documented in upstream `inst/COPYRIGHT.txt`; verify exact statement before any redistribution. The package software license is distinct.

## Frozen executable gates

1. Download exactly the pinned public binary in a free standard Ubuntu GitHub Actions job; verify exact byte length, Git blob SHA1 and bzip2 magic before parsing.
2. Use open-source pyreadr to parse the original RDA, print the actual object keys, dimensions, six column names, null counts and categorical value sets. Require 7358 rows and exactly `treatment,id,game,period,choice,other.choice` in that order.
3. Verify `period` and `game` are nonmissing positive integer values and actions are exactly `c` or `d`. Check duplicate keys `(treatment,id,game,period)`, the number of distinct `(treatment,id)` combinations, and whether `id` repeats across treatments. Preserve all discovered irregularities.
4. Report whether session ID, opponent pair ID and unique cross-session identity can be established from these six columns. If not, the R073 frozen evaluation gate stays BLOCKED and no held-out predictive scoring is performed.
5. Negative controls must reject modified raw bytes and a deliberately incorrect expected blob SHA. The script shall print a machine-readable JSON summary to CI logs and shall never upload or commit original participant-level rows.
6. Any failure to download, decode, verify or inspect must be recorded as BLOCKED; no pass and no E2 scoring claim. Python packages and public standard GitHub runner must be free. No paid API, registration, secrets, paid runner or private data.

This gate is only public human-data source inspection. It creates no new E2 predictive result. R073 model and scoring rules remain frozen. No cross-study tuning.
