# A data scout: historical appliance shipments and R155 first-adoption target gate

Date: 2026-10-25 UTC+08. Priority: secondary R155 historical data candidate; R-series main work takes precedence. No new E3 score.

## English-language sources actually checked
* CRAN regclass documentation mirror: https://rdrr.io/cran/regclass/man/APPLIANCE.html
* English university CRAN manual: https://www.maths.bris.ac.uk/R/web/packages/regclass/refman/regclass.html
* Publisher source for Bass 1969, DOI https://doi.org/10.1287/mnsc.15.5.215
* R package metadata: https://www.quantargo.com/help/r/latest/packages/regclass/1.6/APPLIANCE

The documented `APPLIANCE` object has **26 annual observations from 1960 through 1985** and seven fields: `Year`, `Dishwasher`, `Disposal`, `Refrigerator`, `Washer`, `DurableGoodsExp`, `PrivateResInvest`. Appliance columns are US domestic factory shipments in thousands of units. The expenditure and residential-investment columns have different economic units. The documentation attributes historical appliance shipment figures to US Department of Commerce sources and a former Data and Story library.

## Scientific eligibility
Bass R155 describes the hazard and flow of **first-time adopters** of a fixed market. Factory shipments can include replacement purchases, distributor inventories and purchases by existing owners; they need not equal first-time household adoption. Therefore the documented 26-year shipment series cannot be inserted as an R155 first-adopter ground truth without a separate measurement model and independent historical denominator. This is a **target-definition blocker** even if all 26 records are eventually obtained. It also overlaps in subject matter with Bass's original historical appliance examples; do not claim a new independent replication without checking provenance and time ranges.

The annual temporal unit is verified from documentation. No participant identities, dyads, rounds, sessions, partner actions or experimental independence exist in this aggregate economic series. It is unsuitable for R073 frozen binary repeated-game scoring. The actual R data-object bytes, all 26 row values, missingness and package-specific redistribution rights were not independently acquired or verified in this run. A GPL package license does not automatically establish the licensing status of its underlying historical data.

## Gate result and next actions
`SOURCE_AND_SCHEMA_VERIFIED`; `RAW_ROWS_PENDING`; `FIRST_ADOPTION_OUTCOME_MISMATCH`; `LICENSE_FOR_RAW_DATA_UNVERIFIED`; `R073_INELIGIBLE`; `E3_NOT_SCORED`.

For any future R155 E3 evaluation, first obtain a properly licensed first-purchase/adoption cohort or justify an independently frozen observation equation for shipments, inspect original raw bytes and row keys, check historical train/test chronology and prevent future-year leakage. Continue higher-priority human repeated-game source scouting separately; existing Montero 2022, Dal Bó/Frechette 2011 and Fudenberg/Rand/Dreber 2012 sources were previously flagged as already used by R096, R074 and R075. No private data or paid access used.
