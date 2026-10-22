# R217 合成控制法（09-008）：1024项完整独立处理后人工来源，正式E1结题

2026-10-22（Asia/Taipei）。原239项目录 **09-008 Synthetic Control（P1）**。**CLOSED_BOUNDED_E1_ARTIFICIAL_SYNTHETIC_CONTROL**。

[正式科学报告](R217_SCIENTIFIC_REPORT_2026-10-22.md) · [事前冻结协议](../../protocols/R217_SYNTHETIC_CONTROL_8_WORLDS_1024_ORIGINAL_PRE_POST_PAIRS_PRESCORE_FREEZE_2026-10-22.md) · [八世界机器结果](R217_EXACT_RESULTS.json) · [1024条完整原训练×独立处理后来源](R217_ALL_1024_ORIGINAL_INDEPENDENT_PRE_POST_SOURCE_PAIRS.csv) · [机器SHA及来源验收](R217_FINAL_MACHINE_ACCEPTANCE.json) · [正式科学结题验收](R217_FINAL_ACCEPTANCE_STATUS.json) · [纯Python与35单测](r217_exact_synthetic_control.py)。

人工组T和3个捐赠者，处理前t0/1/2与处理后t3/4分开；15种以1/4为网格的固定凸权重候选，只根据处理前真实观测SSE拟合，8个真源世界×8种训练T噪声×16种独立新测量噪声=**1024条真正完全联合人工来源**。预定训练最优权重的独立新因果效果损失与条件均值Bias²+(1+w1²)/16两路Fraction完整核验，不能把新噪声当作新真人或新地区。

真有效政策+2和真政策0但处理组政策后无处理潜在趋势恰好+2的两世界**所有实际观测完全一致**，同样训练SSE期望11/64；合成政策效果真实评估MSE却为9/64 vs 297/64，因此**训练匹配完美或观察后差异无法单独证明真实效果**。捐赠者D1处理后受到固定额外冲击，训练SSE仍11/64，新效应MSE增至57/64；处理前拟合失配世界训练SSE7/16，新效应MSE825/256。正常稳定结构下选择权重有限噪声也有误差：9/64，大于固定知道无污染真半半权重对照5/64。

[GitHub Actions run39745079161](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39745079161) Python3.11/3.12各35项共70通过，第三完整来源原文件、双Fraction及SHA归档job成功，机器人[原结果提交a213e616](https://github.com/edwardsage419/Psychohistory-Research/commit/a213e6160fb21709a1fb00ff723e222737242669)。**仅人工E1，新真人E2=0、历史E3=0，R073/PESEN v0.1冻结**。

下一原239目录：**09-009 Propensity Score Matching（R218）**。仍按全R先完成，再统一分类，最后熔炼。
