# R285 多重比较控制（原目录12-015，P1）

正式科研状态：**CLOSED_BOUNDED_E1_ARTIFICIAL_HOLM_BH_MULTIPLE_TESTING**。原239目录最后一项。两个独立四次二元检验H1/H2、三人工真实假设机制、RAW/HOLM/BH三政策，共9world，每world全部256个原八bit来源，共**2304个完整模型标签人工source类型**，逐来源与不调用完整原source的独立5×5二项计数法完全一致。

[事前冻结协议](../../protocols/R285_TWO_HYPOTHESIS_HOLM_BH_2304_COMPLETE_SOURCE_PRESCORE_FREEZE_2026-10-23.md) · [执行模型和unit tests](r285_exact_multiple_testing.py) · [完整2304原来源和FDP/FWER CSV](R285_ALL_2304_ORIGINAL_MULTIPLE_TESTING_SOURCES.csv) · [完整风险结果JSON](R285_EXACT_RESULTS.json) · [SHA256机器凭证](R285_MACHINE_RECEIPT.json) · [正式科学报告](R285_SCIENTIFIC_REPORT_2026-10-23.md) · [最终机器验收](R285_FINAL_ACCEPTANCE_STATUS.json)。

冻结alpha=1/2**只供小样本离散阈值对比，不推荐用于现实研究**。两真null时未校正FWER135/256、Holm31/256、BH47/256。两p都5/16时RAW两拒、Holm零拒、BH两拒。适当区分FWER=P(V>0)与FDR=E[V/max(R,1)]。

[最终GitHub Actions run39906881178](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39906881178)三个job completed/success，Python3.11及3.12各80项真实unit test共160通过，第三独立来源重构和永久原CSV/结果JSON/SHA256归档[commit41643378](https://github.com/edwardsage419/Psychohistory-Research/commit/41643378604f670fc72234ab608965422c2f4e60)。

无新增真人E2、真实历史E3或历史独立预测效度。R073与PESEN v0.1保持冻结。下一研究不是自动开始熔炼，而是**对原239候选目录逐项核查是否已完成研究和证据验收**，随后根据实际结果才统一归纳分类。
