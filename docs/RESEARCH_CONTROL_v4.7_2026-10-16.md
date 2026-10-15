# 心理史学研究主控台 v4.7｜2026-10-16

本文件为 [v4.6](RESEARCH_CONTROL_v4.6_2026-10-16.md) 的增量。历史档案、已冻结的 PESEN v0.1，以及 R001 至 R064 的原始文件均不修改。

## R065 第七阶段：时间分层模型的独立数值复算

在获得本阶段新统计结果之前，先提交 [Phase G 回顾性审计方案](../protocols/R065_PHASE_G_AGGREGATE_ALIAS_AUDIT_2026-10-16.md)。本分析目标来自已见 Phase B/D 结果，仍属于事后复现和设计识别审计。

从 Levy 等作者固定处理后实验数据 Git blob `01bf211468abe093618dfa5e5c39e883230c9c03`，连接器端读取完整 CSV，并重用原作者全试次排除规则。提取 226 名合格参加者的 1,808 个关键试次，形成 [8×2 个匿名计数单元](../research/R065/R065_PHASE_G_CELLS.json)。共有 684 次直接模仿（high 344、low 340），第六块 day 89 共 73 次；两种实验顺序组分别 121 和 105 人。

在本地 Python 3.13 仅使用此 16 单元 `(n,k)`，精确复算 Phase D 两个候选模型的留出整名参与者预测结果：

| 模型 | 对数损失 | Brier |
|---|---:|---:|
| M2 实验块预测 | 0.661562754612636 | 0.23435947600656398 |
| M3 实验块×收益预测 | 0.6630223954616713 | 0.23503647415522147 |

该四个数值与原 Phase D 真实记录端连接器分析结果在 1e-12 公差内匹配。12 项本地单元测试均成功，0 失败。独立程序、测试和运行结果分别见 [可运行代码](../research/R065/r065_phase_g_cell_certificate.py)、[单元测试](../research/R065/test_r065_phase_g_cell_certificate.py)、[结果 JSON](../research/R065/R065_PHASE_G_RESULTS.json)。完整证据与推断限制见 [研究报告](../research/R065/R065_PHASE_G_AUDIT.md)。

## 新增的重要识别限制

每位参与者的收益顺序只能是 `H L H L H L H L` 或 `L H L H L H L H`。给定实验块位置后，收益 high/low 正好对应两种先后顺序分组中的一个。对模型 M3 的 16 个交叉单元重新标记为 `实验块×先高/先低顺序组`，完全不会改变预测概率和分数。

故 M3 对 M2 增添的预测信息在当前定义下不能区分收益条件与序列组成员身份，**不具备单独识别因果收益效应的资格**。这不否定后续利用同一人在交替实验块上的重复测量、证据充分的随机分组与完整任务模型尝试识别收益效应。

注意：M0/M1 每个单元包含一名参与者多条试次，需要从训练集同时排除全部相关试次，只有 16 个聚合计数不足以独立重构其留人分数；由此也不能重建损失差的参与者配对 Bootstrap 协方差。

## 证据等级与下一关

* `R065_PHASE_G_SOURCE_AGGREGATION=GITHUB_CONNECTOR_VERIFIED`
* `R065_PHASE_G_M2_M3_AGGREGATE_REPLAY=LOCAL_PASS_12_TESTS`
* `R065_PHASE_G_STAKE_SEQUENCE_ALIAS=DEMONSTRATED_BY_DESIGN`
* `GITHUB_ACTIONS_FULL_REPLAY=NOT_VERIFIED`
* `R065_ALL_SEVEN_AUTHOR_MODELS_FIT_REPLAY=OPEN`
* `R065_FULL_RESEARCH_GATE=OPEN`
* `PESEN_v0.1=FROZEN`

当前 GitHub Actions 配置另设独立 Phase G 汇总数据校验作业，但**没有取得该作业成功日志**，不能把已提交配置列为已成功运行。下一优先项仍是固定作者版本的完整模型与实验原始记录的可执行拟合对照，独立验证状态重置时间轴对预测与参数的实际影响。
