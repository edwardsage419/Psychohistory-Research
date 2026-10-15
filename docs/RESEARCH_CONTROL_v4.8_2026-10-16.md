# 心理史学研究主控台 v4.8（2026-10-16）

继承 [v4.7](RESEARCH_CONTROL_v4.7_2026-10-16.md)，不覆盖先前研究轮次 R001–R064 或 R065 Phase A–G 的既有文件与结论。PESEN v0.1 继续冻结。

## R065 Phase H：真实作者逐人实验试次的 Model 3 重置敏感性

先于新的 Phase H 结果提交 [限定范围研究方案](../protocols/R065_PHASE_H_MODEL3_SENSITIVITY_2026-10-16.md)，固定作者 Git 提交、模型源码、十份原作者逐人 CSV 路径、参数 β=5、原始重置日期与替代重置日期。由于 Phase C 已发现源码重置问题，本阶段仍是事后技术敏感性研究，不是前瞻性或发表结果的独立完整复现。

GitHub 连接器直接读取固定作者仓库 `arielevy8/obs-learning-fishing` 十份原始逐人实验文件，核对每份 Git blob 及每人 136 条连续正式实验试次，取得 542 条 `play` 行。只选择作者简单的 `model_3_objective`（复制最近一次观测动作），在连接器侧执行与作者源码语义等价的程序计算；**原作者 scipy/numpy 函数及模型参数优化没有被原样执行**。本地新建同源语义的 Python 复算程序与测试，但因 DNS 无法获得十份真实 CSV，本地真实来源的 Python 回放仍 OPEN。

| 指标 | 原作者日 23、45、67、89、111 重置 | 块边界日 18、35、52、69、86、103、120 重置 |
|---|---:|---:|
| 10 人的 542 次 play 平均 NLL | **1.417681470** | 1.529461786 |
| 10 人的 day89 平均 NLL | **0.693147180** | 4.506715335 |

两套规则改变了 21 个 `play` 概率，十人的 day 89 全部发生变化。新时间轴在本次固定 β 和非随机样本上提高了 NLL（更差），**不能把“源码日期与区块不对齐”直接推理为“修复后必然提高预测性能”**。

科研范围：这十份是按公开路径固定的便利样本，未经正式筛选、没有新队列、没有优化任何参数，不能对全部 226 合格参与者、作者七个拟合模型或潜在认知机制做推断。先前 Phase E 的 `copied` 概率基线与本阶段预测具体动作的 Model 3，研究目标和参数不同，不应混同。

## 交付与验证

* [Phase H 正式审计](../research/R065/R065_PHASE_H_AUDIT.md)
* [机读汇总与十份来源 SHA1](../research/R065/R065_PHASE_H_RESULTS.json)
* [标准库 Python 源码等价程序](../research/R065/r065_phase_h_model3_reset.py)
* [12 项本地实际执行全部通过的测试](../research/R065/test_r065_phase_h_model3_reset.py)
* [GitHub Actions 自动来源获取与结果检查](../.github/workflows/r065-reproducibility.yml)，新增 `model3-raw-sensitivity` 独立作业，但未获得成功作业日志，不能将该 CI 列为 PASS。

**最新研究关口：** `R065_PHASE_H_FIXED_SAMPLE_SOURCE_PORT=COMPLETE`；`R065_PHASE_H_LOCAL_SYNTHETIC_TESTS=PASS_12`；`R065_NATIVE_AUTHOR_SEVEN_MODEL_FIT=OPEN`；`R065_FULL_RESEARCH_GATE=OPEN`；`PESEN_v0.1=FROZEN`。

下一优先行动：核实 GitHub Actions 具体作业日志，在允许的执行环境获取全部固定原作者逐人 CSV，并开展完全相同模型与优化预算下的两种重置日期真实样本对照。没有这些实证证据前，不以已有实验作原创模型参数更新。
