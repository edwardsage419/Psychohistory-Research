# R296 Rescorla–Wagner 1972 (original 239 #02-001) finite artificial E1

Original catalogue: **02-001**, P1. Reproduces a simple exact shared compound error equation across **8 synthetic worlds and 40 source states**, testing cue blocking/unblocking and an independently constructed cue-specific error negative control. **Does not replicate the original 1972 Pavlovian conditioning experiment or any real human/animal measurements.**

[Prospective protocol freeze 78e947a3](https://github.com/edwardsage419/Psychohistory-Research/commit/78e947a3de8dbeb209edc473ae74f98eb6937904) | [Full prospective contract](../../protocols/R296_RESCORLA_WAGNER_BLOCKING_UNBLOCKING_40_SOURCE_PRESCORE_FREEZE_2026-10-23.md)

* [Runnable exact model and 211 unittest checks](r296_exact_rescorla_wagner.py)
* [All 40 original synthetic A/B cue associations](R296_ALL_40_ORIGINAL_RW_CUE_BLOCKING_STATES.csv)
* [8 world complete stage trajectories and closed-form reference checks](R296_EXACT_BLOCKING_UNBLOCKING_RESULTS.json)
* [Original source/result byte SHA256](R296_MACHINE_RECEIPT.json)
* [Independent source-level audit and 14 adversarial tests](../catalogue_audit/independent_r296_source_audit.py)
* [Full scientific report, equations, source limitations](R296_SCIENTIFIC_REPORT_2026-10-23.md)
* [Final bounded E1 acceptance](R296_FINAL_ACCEPTANCE_STATUS.json)

[Observed GitHub Actions successful three-job run39920891647](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39920891647). Permanent all-source archive commit [8133120b](https://github.com/edwardsage419/Psychohistory-Research/commit/8133120bc6b4270b13bc60ad472e4f643ec33ae8).

With α=1/2 and four AB trials, blocking B strength is 1/512 after eight A pretraining trials vs 1/2 without pretraining. AB reward upshift to 2 produces B=257/512. In the independent per-cue error control B=15/16 with or without A pretraining for reward 1. These are **artificial strength values**, not observed animals or probabilities. R073/PESEN v0.1 unchanged; catalog provenance is not evidence of broad empirical validity.
