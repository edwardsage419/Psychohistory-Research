# R300 Hidden Markov Model: exact forward inference and i.i.d. hidden negative control

Original 239-candidate **02-008** P1. Entirely **synthetic E1** known-parameter two-latent-state HMM, 16 complete length4 binary observation strings ×4 prefix times ×2 Markov regimes = 128 fully labeled source states. No real human/animal data, hidden parameter estimation, Viterbi, causal identification or historical E3.

Original first-party paper Rabiner (1989), *A Tutorial on Hidden Markov Models and Selected Applications in Speech Recognition*, https://doi.org/10.1109/5.18626.

[Prescore frozen protocol ef56b01c](https://github.com/edwardsage419/Psychohistory-Research/commit/ef56b01c3c2b5da98e433f9d2fefdd61fd9028c3) | [Full protocol](../../protocols/R300_HMM_FORWARD_FILTER_IID_NEGATIVE_CONTROL_128_SOURCES_PRESCORE_FREEZE_2026-10-23.md).

* [Executable exact forward filter and 394 unit tests](r300_exact_hmm_forward_filter.py)
* [All 128 original artificial source rows](R300_ALL_128_ORIGINAL_HMM_PREFIX_SOURCES.csv)
* [Full two-world 128-prefix forward/posterior/prediction result JSON](R300_EXACT_HMM_FORWARD_RESULTS.json)
* [CSV/JSON source SHA256 receipt](R300_MACHINE_RECEIPT.json)
* [Completely independent hidden-path enumeration with 16 adversarial tests](../catalogue_audit/independent_r300_source_audit.py)
* [Scoped scientific report and methodological limits](R300_SCIENTIFIC_REPORT_2026-10-23.md)
* [Formal bounded E1 acceptance](R300_FINAL_ACCEPTANCE_STATUS.json)

PERSISTENT (stay 3/4) hidden posterior P(H4=1|1110)=19/46 vs P(H4=1|0000)=3/22; next-observation1 predictions 11/23 vs 9/22. Under IID-hidden stay1/2, both observations ending 0 have same P(H4=1)=1/4 and next observation1 P=1/2. All artificial. Do not equate hidden label to real psychological category.

[Three completed/success GitHub jobs run39927762571](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39927762571) dual-Python + third independent archive; original sources permanently committed [38830d98](https://github.com/edwardsage419/Psychohistory-Research/commit/38830d98e6c12c891e5fc542903b39ca6976f4ec). Original239 catalogue unchanged until independent v1.4 linkage; R073/PESEN v0.1 frozen.
