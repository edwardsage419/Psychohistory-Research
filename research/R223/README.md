# R223 未测混杂敏感性分析（09-014）：有界人工E1正式结题

**日期2026-10-22**。原239目录 `09-014 Sensitivity Analysis for Confounding (P0)`。状态 `CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_CONFOUNDING_SENSITIVITY`。真人E2新增0，历史E3新增0。

[计算前冻结协议](../../protocols/R223_CONFOUNDING_SENSITIVITY_7_SCM_448_ATOMS_PRESCORE_FREEZE_2026-10-22.md) · [完整科学报告](R223_SCIENTIFIC_REPORT_2026-10-22.md) · [全部448结构原来源CSV](R223_ALL_448_ORIGINAL_CONFOUNDING_STRUCTURAL_ATOMS.csv) · [七世界精确Fraction结果JSON](R223_EXACT_RESULTS.json) · [Python计算和48项测试](r223_exact_confounding_sensitivity.py) · [源SHA机器收据](R223_FINAL_MACHINE_ACCEPTANCE.json) · [正式结题验收](R223_FINAL_ACCEPTANCE_STATUS.json)。

七个固定二元U/T/Y人工因果世界×每世界64原结构状态=448行。结构零赋值32行概率为0，实际有正支持416行。最强反例NULL_CONFOUNDED与CAUSAL_ALIAS观察完整P(T,Y)相同、观察RR均11/5，真因果RR却是1和11/5；同一个点E-value约3.82480768，无法选择真正机制。CONFOUNDED_REVERSED观测RR1却真RR3/5；NO_POSITIVITY强制返回UNIDENTIFIED_NO_POSITIVITY。数学真机制与可观察数据严格分开，不用隐藏U/Y0/Y1偷补缺失条件结果。

[CI run39788126049](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39788126049)真实Python3.11/3.12各48项测试通过，共96次，三作业completed/success；[原资料机器人提交b2dd10d7](https://github.com/edwardsage419/Psychohistory-Research/commit/b2dd10d7c2383ad0a8490a98f4f5e9f4509add7a)已永久归档main。该研究仅数学E1，不涉及真实群体的因果验证或原作者实证复现。

下一真实原目录 **09-015 Negative Control Designs（P1）**，按连续研究编号应为R224。先逐项完成既定原R，再统一分类，最终熔炼；R073与PESEN v0.1保持冻结。
