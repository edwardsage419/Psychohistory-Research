# R172 third-method scientific report: historical hazard calibration and country dependence

Date: 2026-10-26 Asia/Singapore. Status: PASS_BOUNDED_INTERNAL_RETROSPECTIVE_E3_SOURCE_HISTORICAL; **NO_NEW_PROSPECTIVE_E3**.
Input frozen before new calculations at [protocol](../../protocols/R172_COUNTRY_CLUSTER_CALIBRATION_THIRD_METHOD_PRESCORE_FREEZE_2026-10-26.md), commit c758dd2f8815bcc9137dd404bfa963515887f530. Original [R172 historical source](../R172/README.md), Harvard Dataverse doi:10.7910/DVN/WFO1N1 (version 1.1, CC0). New executable [JS source](r172_country_cluster_calibration_20261026.js), machine-readable [receipt](R172_COUNTRY_CLUSTER_CALIBRATION_THIRD_METHOD_RECEIPT_2026-10-26.json). The exact input CSV Git blob was 00d0379d77ec8e776a00cbb9c6e9dd5a00958dce; new code Git blob 4e10f374a3cbb0d2f3c0491a161f6833bc266df9. All new calculations actually executed in V8 using the archived Node-compatible source and live GitHub-fetched CSV. No CI run was requested.

## Source and no-retuning gate

The 319 heldout country-year rows belong to 35 unseen regime episodes in 32 country IDs, with 18 observed first-breakdown events during 2000 to 2017. Every original exact rational prediction was read unchanged. The 32 country IDs include three countries with two heldout episodes each: MRT, NER and SLB. The existing historical split is episode-disjoint and calendar-cutoff controlled, yet same countries may appear in both original training and heldout partitions. The current audit does not refit the training source or certify contemporaneous covariate availability.

## Verified scoring and new calibration findings

| Model | Mean annual log loss | Mean annual Brier | Expected breakdowns (sum p) | Actual breakdowns |
|---|---:|---:|---:|---:|
| M0 constant | 0.235881126652 | 0.054407113235 | **7.1132** | **18** |
| M1 elapsed-time | 0.245235328446 | 0.054667027894 | **6.3208** | **18** |
| M2 duration plus baseline index | 0.234530415157 | 0.054105271593 | **7.5795** | **18** |

All original published scores matched within the frozen 1e-10 tolerance. The observed annual event frequency was **18/319 = 5.6426%**. All three models forecast only about 6.32 to 7.58 expected events, roughly **35.1% to 42.1% of the 18 recorded events**. This is a serious retrospective absolute-risk calibration warning within this specific later cohort. It is not a prospective external validation or proof of a universal model failure. Time drift, source coding and selection of post-1999 new episodes remain possible explanations.

Fixed probability bins [0,0.02), [0.02,0.05), [0.05,1]:

* M0: all 319 rows in middle bin, expected 7.1132, observed 18.
* M1: low bin 214 rows, expected 3.1798 and observed 12; middle bin 105 rows, expected 3.1410 and observed 6.
* M2: low bin 115 rows, expected 1.0601 and observed 5; middle bin 204 rows, expected 6.5194 and observed 13.
* All three models: no predictions in high bin. No posthoc bins or recalibration were introduced.

## Country-unit sensitivity

Full-data annual mean logloss differences versus M0 (lower is better): M1 **+0.00935420**; M2 **−0.00135071**. Full-data Brier differences: M1 +0.00025991; M2 −0.00030184.

Leave one entire heldout country out, recompute annual-weighted difference on all remaining years:

| Statistic | M1 versus M0 | M2 versus M0 |
|---|---:|---:|
| Minimum LOCO annual logloss difference | +0.00713230 | −0.00749860 |
| Maximum LOCO annual logloss difference | +0.01035770 | +0.00047526 |
| Positive / negative LOCO differences | 32 / 0 | **5 / 27** |
| Country deletions reversing full-data sign | none | **BGD, HTI, LBY, MRT, THA** |

Thus the small M2 advantage changes direction when any of five specific countries is excluded. These are descriptive influence checks, not independent tests. M1 remains worse under all 32 deletions.

The 1024 fixed-seed country-cluster bootstrap replicates sampled 32 countries with replacement, retaining all of each selected country's heldout years:

| Difference relative to M0 | Full sample | Country-bootstrap percentile 2.5% to 97.5% |
|---|---:|---:|
| M1 annual logloss | +0.00935420 | [−0.00115170, +0.02097833] |
| M2 annual logloss | −0.00135071 | **[−0.01813721, +0.01486294]** |
| M1 annual Brier | +0.00025991 | [−0.00013082, +0.00065916] |
| M2 annual Brier | −0.00030184 | **[−0.00101691, +0.00020569]** |

All four intervals cross zero. These intervals differ from the earlier 512-episode bootstrap because the clustering unit and resampling seed differ. They cannot be pooled or treated as guaranteed nominal coverage when countries share broader geopolitical shocks. Small 32-country cluster count, 12 original training events, and source hindsight remain important limitations.

## Executed negative controls and scientific disposition

Flipping the first heldout binary event changed its M0 logloss; replacing the first M2 probability with 1/2 changed its Brier loss. Both controls executed on disposable copies, **2/2 PASS**. The machine receipt retains all 32 country deletion results and all three fixed-bin tables.

**Disposition**: R172 original CLOSED_BOUNDED_REAL_HISTORICAL_RETROSPECTIVE_HOLDOUT remains unchanged. New R172 third method passes a bounded internal retrospective robustness audit and reveals meaningful underprediction of observed breakdowns and a fragile M2 relative improvement. There is no new genuine prospective E3 historical prediction, E2 human game result, causal identification, independent dataset, or external research-team replication. No original R172 data, model, test split, R073, PESEN v0.1, original239 crosswalk or pending queue were modified. Historical source material is kept separate from E1 synthetic and E2 human evidence.

## Reproduction and provenance

From the repository root, use `node research/validation/r172_country_cluster_calibration_20261026.js research/R172/R172_REAL_HELDOUT_PREDICTIONS.csv` with Node.js standard library only. Compare its JSON with the committed receipt. Independent B algorithm checks the country Brier deletion using exact BigInt rational arithmetic in [B audit](../evidence_audit/B_R172_EXACT_COUNTRY_DELETION_SCIENTIFIC_AUDIT_2026-10-26.md). Original Dataverse source: https://doi.org/10.7910/DVN/WFO1N1 . All work used free existing tools; account billing and free GitHub quota not independently verified.