# A 数据来源核对：DF2011 已有解码和 R074 同研究去重证据

日期：2026-11-01 UTC
轨道：R/A
基线 main：`7b2eb5e58cc7385a05e9d3c04dd8b37fac0e1051`
状态：COMPLETE_EXISTING_EVIDENCE_RECONCILIATION；NEW_R073_SCORE=NOT_RUN
目标键：(A,DF2011-stratEst/R074/NV_games-DF,2011-original-study-DOI,prior-decode-and-source-independence-status-regression)

## 发现的证据状态回退

2026-11-01 新增 `research/data_scout/A_STRATEST_DF2011_REPEATED_PD_SOURCE_LINEAGE_GATE_2026-11-01.md` 将 DF2011 标为 `RAW_ROWS_NOT_PARSED`、`R073_FROZEN_ELIGIBILITY_UNKNOWN`，并称需取得二进制后才能核对是否属于独立来源。

然而更早的正式归档已完成以下工作：

1. `research/data_scout/DF2011_FIXED_BLOB_ROW_DECODE_REPORT_2026-10-24.md`：在冻结协议后实际解码固定的 `data/DF2011.rda`，Git blob `52e216b02e1a7ab7fb1a6e335b5f7e2ef6b7f5a0`。归档 GitHub Actions run `40083592838` 报告 success，7,358 行、六字段、266 个处理与参与者组合、无六字段缺失、无四字段重复键、最大观察轮次 23。此轮没有重新运行该 CI，原始日志与数据仍需按需要独立复验。
2. `research/data_scout/DF2011_R074_SAME_ORIGINAL_EXPERIMENT_DEDUP_2026-10-24.md`：DF2011 与既有 R074 均明确引用 Dal Bó 与 Fréchette 2011，同一 DOI `10.1257/aer.101.1.411`，已判定 `SOURCE_STUDY_DUPLICATE_CONFIRMED`、`R073_NEW_INDEPENDENT_EXPERIMENT_INELIGIBLE`。两种整理版的逐行同一性仍未证明，不能把“同研究”误写为“逐行相同”。
3. `research/R074/README.md` 及 `R074_FINAL_ACCEPTANCE_STATUS.json`：R074 已在 2026-10-17 以原作者直接来源完成有界真人外部实验 E3 结构转移，18 场次、37,042 个个体行动、15,338 个 t>=3 评分事件。M3 相对 M1 的方向获得支持，M4 相对 M3 的方向失败。该既有结果不因重新发现 DF2011 而产生第二份 E3。
4. 上游原始英文文档已再次实际读取：`fdvorak/stratEst` 的 `man/DF2011.Rd`，Git blob `de410a6423521fe78f6995c17f3677b0d6164417`，明确论文 DOI、7,358 行、六字段、supergame 内 `period`；`JohnNay/datafsm` 的 `man/NV_games.Rd`，Git blob `be625b217505dd05781f5bd9c12925df673a7ac0`，明确 168,386 行，`data=DF` 代表 Dal Bó 与 Fréchette。NV_games 与 DF2011 的行级交集尚未直接验证。

上游版本（本轮查询的 master HEAD）：
`fdvorak/stratEst@c05aae64eadc8f5e2bbf8b98b14b884f5b393be7`；
`JohnNay/datafsm@c2e55eab12f1a24d3a5b09a9b42aeefff8bc5be4`。

## 修正后的资格状态

* `DF2011_RAW_ROWS_HISTORICALLY_DECODED = YES`，依据 2026-10-24 固定来源与归档 CI；本轮 `RAW_REDECODE = NOT_RUN`。
* `DF2011_SAME_STUDY_AS_R074 = CONFIRMED`，依据相同作者、论文及 DOI。
* `DF2011_AS_NEW_INDEPENDENT_R073_EXPERIMENT = INELIGIBLE`。这项决定早已成立，本轮只恢复正确证据状态。
* `DF2011_VS_R074_ROW_LEVEL_IDENTITY = UNKNOWN`；`NV_games_DF_VS_DF2011_ROW_OVERLAP = UNKNOWN`。
* `R074_EXISTING_E3 = CLOSED_BOUNDED`，仍保留其负结果和限制；本轮新增 E2=0、E3=0。
* `R073_MODEL_AND_SCORE = FROZEN`，`PESEN_v0.1 = FROZEN`。

## 科研风险和下一步

此项为已归档事实在后续数据侦察中被遗漏的状态回退，可能导致重复下载、重复实验计数或错误宣称独立外部验证。本轮发现了状态冲突，没有观察到新重复评分或新错误 E3 入账。旧记录保留原样，本文件作为追加勘误供后续 A 轨优先引用。

优先搜索真正不属于 R073、R074 及其他既有真人 R 系列来源的新实验；读取已有去重台账后才进入数据下载与冻结资格判断。若需对 DF2011 做行级映射，应单独冻结对应研究问题，并区分既有 E3 与新数据整理工作。

来源：
https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/data_scout/DF2011_FIXED_BLOB_ROW_DECODE_REPORT_2026-10-24.md
https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/data_scout/DF2011_R074_SAME_ORIGINAL_EXPERIMENT_DEDUP_2026-10-24.md
https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/R074/R074_FINAL_ACCEPTANCE_STATUS.json
https://github.com/fdvorak/stratEst/blob/master/man/DF2011.Rd
https://github.com/JohnNay/datafsm/blob/master/man/NV_games.Rd

CI 本轮 NOT_RUN；账单未核验；没有使用付费数据、API、Actions 或私人资料。
