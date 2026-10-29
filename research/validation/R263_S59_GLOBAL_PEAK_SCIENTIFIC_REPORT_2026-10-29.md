# R263 S59 finite genetic population global peak prediction
Date: 2026-10-29 UTC. Evidence: E1 finite artificial only.

Prescore protocol: protocols/R263_S59_PARTIAL_PARENT_INFORMATION_GLOBAL_PEAK_BRIER_FREEZE_2026-10-29.md, commit c8219ad6891c252a5382fb89a3b7423e01a0d50a. Original source CSV Git blob 514a619e700f98c5c5e0a575c4569810b2fc817d. The historical R263 model and acceptance remain unchanged.

## Executed method
Read all 9216 CSV rows through GitHub connector, each of nine worlds containing exactly 1024 unique ten-bit identities and source mass 1/1024. Verify parental genomes against source bits. An independently written integer-mask offspring calculation reproduced the global-peak Y label for every source, 0 mismatches. Five nested information sets F0, FB, FP, FPC, FF are exactly those prespecified. Compute each Brier risk using rational group counts k(n-k)/n/1024. A separate Python Fraction parent-pair x operator oracle executed locally, comparing all 45 exact risks, and four negative controls rejected.

## Exact Brier risks
| World | F0 | FB | FP | FPC | FF |
| --- | ---: | ---: | ---: | ---: | ---: |
| CLONAL_ONEMAX | 735/4096 | 0 | 0 | 0 | 0 |
| CROSS_ONEMAX | 735/4096 | 141/1760 | 15/256 | 3/128 | 0 |
| MUTATE_ONEMAX | 735/4096 | 999/7040 | 27/256 | 27/256 | 0 |
| CROSS_MUTATE_ONEMAX | 735/4096 | 5059/33792 | 129/1024 | 29/256 | 0 |
| ELITE_CLONAL_ONEMAX | 735/4096 | 0 | 0 | 0 | 0 |
| ELITE_CROSS_ONEMAX | 207/1024 | 15/352 | 1/32 | 1/64 | 0 |
| ELITE_MUTATE_ONEMAX | 14703/65536 | 945/11264 | 51/1024 | 51/1024 | 0 |
| ELITE_CROSS_MUTATE_ONEMAX | 59607/262144 | 61591/675840 | 297/4096 | 129/2048 | 0 |
| ELITE_CROSS_MUTATE_TRAP | 59607/262144 | 130133/1437696 | 297/4096 | 129/2048 | 0 |

All 9 nested risk sequences are nonincreasing and FF=0. CLONAL_ONEMAX and ELITE_CLONAL_ONEMAX reach zero risk once parent-best fitness is known. In MUTATE_ONEMAX and ELITE_MUTATE_ONEMAX, crossover-flag information adds zero risk reduction after full parent genomes because crossover is disabled; FPC nevertheless has twice the group count. In CROSS_MUTATE_ONEMAX, the crossover flag reduces risk from 129/1024 to 29/256. Equal global-peak prevalence does not imply equal conditional risk: the elite ONEMAX and TRAP worlds each have 358 positive source atoms but different FB risk, 61591/675840 versus 130133/1437696.

## Scientific limits and acceptance
The 9216 events enumerate an artificial finite universe, with no train/test split, no real calibration or external holdout. The integer-mask check and Python oracle are internal programmatic verification; B authored after reading the frozen model and current R results, hence nonblind. No long-run GA convergence, human or historical transfer, or causal mechanism identification is established. The original R263 bounded acceptance is unchanged. Source CSV Git blob verified by connector and every row parsed; a fresh local SHA256 and a native Node CLI run on the original CSV were not performed in this environment. A01/A02 PASS for bounded scope and remote source; A03 PARTIAL due native CLI gate; A04 PASS for tested negative controls; A05 PASS for explicit E1 limits; A06 PARTIAL until CI/archived replay. New E2=0, E3=0, external team replication=0. R073 and PESEN v0.1 frozen. Actions not initiated, account free-runner balance not independently verified.
