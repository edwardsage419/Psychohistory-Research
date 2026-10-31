# A scout: Fioretti, Vostroknutov, Coricelli (2022) Dynamic Regret Avoidance

UTC checked: 2026-10-31T22:49Z. Target key: (a,Fioretti_2022_openICPSR_130441_V1,public_source_raw_license_field_gate).
Publication: https://doi.org/10.1257/mic.20180260
Institutional dataset description: https://cris.maastrichtuniversity.nl/en/datasets/data-and-code-for-dynamic-regret-avoidance/
Official deposit: https://www.openicpsr.org/openicpsr/project/130441/version/V1/view
Dataset DOI: https://doi.org/10.3886/E130441V1, V1 dated 2022-01-25.

## Actually verified public metadata
The original experiment concerns decisions to sell an asset while observing its price sequence. The design varies whether future prices after sale will be observed, distinguishing possible past and future regret reference points. Official V1 folder metadata lists `DRA_Rcode/newchoicedata.csv` (551.1 KB, text/csv, modified 2021-05-24), `datapreparation/newlongdata_withhlcrt.txt` (40.6 MB, text/plain, modified 2021-06-01), `datapreparation/dataprep.do` (1.4 KB), `DRA_Rcode/estimation.R` (61.5 KB) and multiple companion analysis files. The official file pages were opened and these names, sizes, file types and version were observed.

Official folder views:
https://www.openicpsr.org/openicpsr/project/130441/version/V1/view?path=%2Fopenicpsr%2F130441%2Ffcr%3Aversions%2FV1%2FDRA_Rcode&type=folder
https://www.openicpsr.org/openicpsr/project/130441/version/V1/view?path=%2Fopenicpsr%2F130441%2Ffcr%3Aversions%2FV1%2Fdatapreparation&type=folder

## Access and suitability
Direct root deposit access returned HTTP 403 in this runtime. Official file pages show download controls but the actual CSV/TXT bytes were not obtained. File header, participant and session identity keys, trial time unit, missingness, license or redistribution terms, full row count and checksum remain UNKNOWN. Public metadata establishes a plausible real human sequential decision dataset; no data record or license claim is inferred from a filename.

R325 applicability: potential later E2 research on dynamic regret, but its observed sequential sell/hold choice and future feedback are not automatically comparable with the frozen three-state cubic R325 toy mechanism. A separately frozen observation and likelihood model would be required before scoring. R073: HARD_NO_BY_TASK_TYPE, because this is individual asset-sale choice rather than 100-round continuous two-human-player PD with linked opponent histories.

Status: SOURCE_VERSION_AND_FILE_METADATA_VERIFIED; RAW_DATA_BLOCKED; FIELD_AND_LICENSE_GATE_OPEN; EMPIRICAL_REPRO_NOT_READY. No private data, registration, paid downloads or model scoring. Next: obtain publicly accessible V1 data dictionary/headers and rights statement through an authorized free route, then verify identity, time index and outcomes. Do not infer missing facts or modify R073/PESEN.
