# 心理史学研究主控台 v4.2（2026-10-15）

本文件是 [v4.1](RESEARCH_CONTROL_v4.1_2026-10-15.md) 的独立增量；历史原件保持原样。研究主仓库：`edwardsage419/Psychohistory-Research`，分支 `main`。

## 当前研究与档案基线

* R001 至 R064 的全部 64 个编号均在历史研究归档清单有对应项，现有清单含 74 份 ZIP（71 个不同 SHA256）和 163 份独立原件。此声明来自记录审计，并不表示本次对全部 ZIP 重新解包、对所有历史实验重新验证。
* R063：metaVS 与固定 VS 的参数语义和作者 Figure 6 审计已归档；人群前瞻留出与完整本地原始 trial CSV 回放未完成。
* R064：独立作者处理 CSV 的全试次预定探索性比较已完成连接器侧分析；无本地完整 CSV 字节复现。
* R065 Phase A：固定 Levy 处理 CSV 的 Git SHA1 在连接器端重新计算匹配，16,103 行、40 列；226 名合格被试、1,808 次关键选择；受试者等权高低收益模仿差 +0.004425，区间跨零；已有 SHA 约束复现代码和 9 项合成测试。
* **R065 Phase B 新增**：追踪 8 个关键实验块的模仿率。前 2 块 46.68%，末 2 块 34.07%，受试者等权前后差 +0.126106，20,000 次受试者 Bootstrap 区间 [0.064159, 0.188053]。每块的模仿概率线性投影斜率 −0.019912，Bootstrap 区间 [−0.029499, −0.010272]。
* R065 Phase B 条件顺序：`counterbalance=1` 对应先高收益 121 人，`counterbalance=0` 对应先低收益 105 人；每人高低收益各 4 次并交替出现。两个顺序组的高减低模仿差分别 +0.026860 与 −0.021429，组间差 +0.048288，其 Bootstrap 95% 区间 [−0.023318, 0.120838]，跨零。随机分配规则仍未核实。
* **本地 Python 测试实际执行**：R065 两个模块合计 15 项构造数据测试全部通过。真实 CSV 的本地下载受网络环境限制，原始数据 Python 完整回放仍 OPEN。研究真实数值来自固定 SHA1 的 GitHub 连接器端分析。
* 原始来源与结果详见 [Phase A](../research/R065/R065_EVIDENCE_AUDIT.md)、[Phase B](../research/R065/R065_PHASE_B_ORDER_AUDIT.md)、[Phase B JSON](../research/R065/R065_ORDER_RESULTS.json)。

## 研究状态与规则

`R065_PHASE_A=COMPLETE`、`R065_PHASE_B=COMPLETE`、`R065_FULL_RESEARCH_GATE=OPEN`、`ORIGINAL_CSV_LOCAL_REPLAY=BLOCKED_BY_ACCESS`、`PESEN_v0.1=FROZEN`。

本轮新增的模仿率随实验块变化是回顾性描述关联，不能自动推出社会学习从模仿转向目标推断，也不能将时间投影斜率当作心理学习率或历史社会演化参数。下一关优先原始 CSV 的本地全字节重算，以及作者 `counterbalance` 生成规则与试次前信息识别。
