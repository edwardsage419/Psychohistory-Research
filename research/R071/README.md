# R071：群体规范形成、惩罚威慑与制度执行成本

建立/限定结题日期：2026-10-16。**正式状态 `CLOSED_BOUNDED`，E1 四种策略固定类型的规范/惩罚数学机制 PASS；真人公共物品惩罚 E2 来源字节未恢复且模型合同不匹配；独立 E3 OPEN。PESEN v0.1 FROZEN。**

本研究承接 [R070 完整空间迁移数学结题](../R070/R070_FINAL_ACCEPTANCE_AND_CLOSURE_2026-10-16.md)，研究从**个体行为选择 → 群体合作规范 → 惩罚制度执行及其资源成本**的条件性反馈。模型是自制抽象机制，启发来自 Ostrom (2000) `10.1257/jep.14.3.137`、Fehr & Gächter (2000) `10.1257/aer.90.4.980`、Boyd et al. (2003) `10.1073/pnas.0630443100`；**没有复现这些作者的原始人类数据或全部演化方程**。

## E1 冻结—代码—运行—永久实验收据

- [先于首次模拟冻结的协议](../../protocols/R071_NORM_COOPERATION_PUNISHMENT_E1_2026-10-16.md)，commit `dcf3a0b2e2137cb8f6430a2437b88cb8738b2f08`。
- [纯 Python 模型](r071_norm_cooperation_punishment.py)与[28 项反例/经济收益恒等测试](test_r071_norm_cooperation_punishment.py)。
- [真实 GitHub Actions 首次运行 38890695079](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38890695079)：success，56 种五人策略组成 ×2 合作阈值 ×2 初始规范 ×3 惩罚制度 = **672 个完整 E1 情形、5376 个群体回合**；28项测试 PASS。
- [独立原始 SHA 固定永久归档工作流 38890837355](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38890837355)：success，二次完全重算并通过 SHA256 `bd8bf1dcc97c5ee9c933e889b68ca50a7403f1d1cf05f67f08195a9cf9b280d8`；[完整 68,172 字节结果 JSON](R071_E1_COMPLETE_672_NORM_INSTITUTION_RESULTS.json) 已归入 GitHub main，不仅是短期 CI 附件。
- [正式数学与制度结果报告](R071_E1_NORM_INSTITUTION_FULL_RESULTS_AND_LIMITS.md)：无惩罚的规范初始值可使相同固定组出现完全不同合作终局；处罚在部分组有威慑效果，但固定监测制度保持同样合作行动的同时减少净收益。在 `θ=.5, seed=0` 的 56 组等权模型中，末轮合作率由无处罚 **0.560714** 变为处罚 **0.639286**，而完整八轮的组每轮净收益均值分别从 **2.765625** 降为变动处罚 **2.1875** / 固定监测 **0.6875**。这不是现实惩罚政策的真实福利估计。

## 真人 E2 数据——实际尝试失败，不得自称实证 PASS

[真实 Dryad 数据门冻结协议](../../protocols/R071_E2_DRYAD_PGG_NOISE_SOURCE_APPLICABILITY_2026-10-16.md)针对 `10.5061/dryad.n02v6wx03` 的 `noisy-PGG.csv` 尝试按官方可下载链接只提取来源 SHA256 与匿名 CSV schema。[实际 Actions run 38891213930](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38891213930)：**安全测试 11 PASS，真人源下载 HTTPError、真实来源 job FAIL**；原始 CSV 内容、哈希、行数和字段**没有获得**。公开论文页面的384人/96四人组、后续320人/80组都是作者报告，**不是我们的真实重新统计**。参见[匿名机器失败收据](R071_E2_DRYAD_SOURCE_ATTEMPT_RESULTS.json)、[其它真实实验数据适用性与负结果审计](R071_E2_SOURCE_CANDIDATES_AND_BLOCKERS.md)。

另外 [R067 对 R047 原始公共资源提取数据](../R067/R067_E2_R047_APPLICABILITY_RESULTS.json) 的复核与 R071 **五人、二元公共品贡献、固定惩罚人**的模型合同不等价。绝不能把四人多水平资源提取随意二值化以获得伪造的真人机制检验。真实社会规范、制度监测与福利的因果推断均 `NOT_ESTABLISHED`。

## 正式结题和开放范围

[完整六门限定验收报告](R071_FINAL_ACCEPTANCE_AND_CLOSURE_2026-10-16.md) · [机读形式验收状态](R071_FINAL_ACCEPTANCE_STATUS.json) · [尚未完成的 E2/E3 和演化问题](R071_POST_CLOSURE_OPEN_GATES.md)。

六门形式 PASS 表示**完整 E1 数值与真人来源失败证据按统一规范入档**，不代表三大真实规范和惩罚机制都得到科学确认。主项目 PESEN v0.1 保持 FROZEN。下一独立研究 R072 可转向重复博弈中的信誉、社会记忆及制度信号可信度；R071 的真实来源重试及模型精确适配保留为独立后续门。
