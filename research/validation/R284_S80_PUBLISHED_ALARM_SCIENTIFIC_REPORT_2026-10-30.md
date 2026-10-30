# R284 S80 publication alarm versus complete registry, scientific report
Date UTC: 2026-10-30. Track: r. Status: COMPLETE_BOUNDED_NONBLIND_E1_CALCULATION; S80 formal scientific acceptance PARTIAL.
Pre-score protocol commit: dd478613b265823f620db2affb69ef94ffb7a955. Original R284 bounded E1 acceptance unchanged. Original R284 protocol, report, results and Python source were read first. Target: (r,R284,original-freeze-0a6eccd2+S80-v1,finite-four-study-publication-alarm-vs-complete-registry).

Four independent fair artificial study outcomes Y and four independent fair disclosure coins R. Three original frozen publication policies, 256 ordered original 8-bit sources per policy, 768 policy-labelled rows with mass 1/256. The published alarm requires K>=2 and J/K>=3/4; complete registry alarm requires T/4>=3/4. K=0 and K=1 remain in unconditional denominators.

| Policy | P(K>=2) | P(published alarm) | P(alarm given K>=2) | P(published alarm and no registry alarm) |
| --- | ---: | ---: | ---: | ---: |
| COMPLETE_REGISTRY | 1 | 5/16 | 5/16 | 0 |
| POSITIVE_ONLY | 11/16 | 11/16 | 1 | 3/8 |
| POSITIVE_PREFERRED | 243/256 | 13/32 | 104/243 | 3/32 |

All three policies have P(complete-registry alarm)=5/16. The extra published-only alarms are 0, 3/8 and 3/32 respectively. In these particular policies all positive studies are always published; hence the registry alarm is never missed by the published alarm. Counts of (published,registry) (00,01,10,11) are COMPLETE (176,0,0,80), POSITIVE_ONLY (80,0,96,80), POSITIVE_PREFERRED (152,0,24,80), each over 256 sources. Zero-publication masses are 0, 1/16, 1/256.

Interpretation: under a true fair 1/2 positive-study process, an unregistered publication-selected collection can cross the descriptive 3/4 positive-fraction threshold more often. The 3/4 threshold is not a calibrated significance level. This is a known artificial selection mechanism and cannot quantify real-world publication bias. This S80 alarm differs from original R284 expected conditional published positive rates 1/2,1,2/3.

R route: exact full 768-source enumeration and per-source CSV. B route: 45 multinomial category compositions across three policies, with six deliberately corrupted receipts rejected. R/B are internally nonblind and share the frozen mathematical specification, with separate implementations. V8 execution PASS. Native Node CLI and external-team replication NOT_RUN. No E2 human prediction or E3 historical prediction. R073/PESEN v0.1 FROZEN.

Artifacts: research/validation/r284_s80_publication_alarm_20261030.js, research/validation/R284_S80_ALL_768_SOURCES.csv, research/validation/R284_S80_RESULTS.json, research/evidence_audit/b_r284_s80_multinomial_gate_20261030.js. GitHub Actions not dispatched because zero incremental cost and free quota were not verified.