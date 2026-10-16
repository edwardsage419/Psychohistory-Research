# 心理史学研究主控台 v5.0（2026-10-16）

继承 [v4.9](RESEARCH_CONTROL_v4.9_2026-10-16.md) 的全部已归档文件、证据类型和权限边界，保留 PESEN v0.1 冻结。

## R065 Phase J：作者有效样本的 24 人原始试次扩展

本轮首先写入[固定选样研究协议](../protocols/R065_PHASE_J_SCREENED_24_MODEL3_2026-10-16.md)，对作者固定处理 CSV 的 295 人应用原始全试次筛选，恢复 226 名合格参与者：121 人先高收益、105 人先低收益。两组内各按 ASCII ID 排序并取固定 12 个等距索引，得到**24 名已通过原作者筛选规则的参与者**（各组 12 人）。选样不是概率随机样本，也没有外部新队列。

GitHub 连接器实际读取这 24 人的固定原始 CSV，逐份核对 Git blob SHA1 及实验阶段完整的 136 天数据；总计 1,327 次 `play`。使用与公开作者 Model 3（复制最近一次观察动作）语义相同的程序，仅改变清空最近观察记忆的日期，并为每种规则独立拟合 β∈[0,30]；每名测试者的 β 都从其余 23 人的数据重新拟合。全部来源 Git blob 身份、去个人化充分计数及结果见 [Phase J JSON](../research/R065/R065_PHASE_J_SCREENED_24_RESULTS.json)。

| 指标 | 作者状态重置日期 | 对齐实验区块边界 |
|---|---:|---:|
| 匿名 MATCH/MISMATCH/UNIFORM | 453 / 275 / 599 | 487 / 303 / 537 |
| 固定 β=5 NLL/选择 | 1.35273846 | 1.42616817 |
| 全样本最佳 β | 0.499121 | 0.474531 |
| 全样本最小 NLL/选择 | **0.67658111** | 0.67685034 |
| 24 折留整人 NLL/选择 | **0.67843771** | 0.67867746 |

两规则的留人预测损失仅相差 +0.00023975（候选边界 − 作者）；作者方案对 13 人留出总损失较低，边界方案对 11 人较低。相较 Phase I 的十人便利样本，本次两方案接近得多。**不能由目前的限定非概率选样数据判定一套重置规则有稳定预测优势；不具备原创认知机制参数更新依据。**

## 复现和严格区分的层级

* GitHub 连接器读取真实原作者 24 份原始逐人文件并在执行环境计算源代码等价 Model 3；不是原作者 numpy/scipy Python 程序的原生执行。
* 本地使用 Python/SciPy 从临时匿名计数复算；与连接器 JavaScript 优化及留人分数在 1e-8 容差内一致。
* [本地来源选择与自动重放程序](../research/R065/r065_phase_j_screened_replay.py)、[十项合成单元测试](../research/R065/test_r065_phase_j_screened_replay.py)已真实本地执行 10/10 PASS；程序和测试的 Git blob 与提交版本一致。没有本地完整作者 24 份原始 CSV 的独立重放证据。
* 新增 [GitHub Actions Phase J 工作流](../.github/workflows/r065-phase-j.yml)，可以在 GitHub runner 下载并验证固定来源文件、执行全部 24 折验证。仅配置已入库；本轮尚未核实成功作业日志。
* 完整 [Phase J 研究审计](../research/R065/R065_PHASE_J_SCREENED_24_AUDIT.md)明确限制推断：事后、同一作者实验、固定确定性采样，不能称为外部或前瞻验证，也不能推断七模型的相对拟合。

## 当前关口

`R065_PHASE_J_FIXED_SOURCE_CONNECTOR_ANALYSIS=BOUNDED_COMPLETE`

`R065_PHASE_J_LOCAL_SELECTION_TESTS=PASS_10`

`R065_PHASE_J_CROSS_LANGUAGE_ARITHMETIC=PASS`

`R065_LOCAL_OR_CI_REAL_RAW_SOURCE_EXECUTION=NOT_VERIFIED`

`R065_NATIVE_SEVEN_MODEL_REFIT=OPEN`

`R065_FULL_RESEARCH_GATE=OPEN`

`PESEN_v0.1=FROZEN`

下一工作重点：在可验证执行环境取得 226 人原始数据的完整来源与模型拟合证据；若 GitHub Actions 不能实际运行，则先形成精确失败证据和最小闭合办法，禁止反复提交未得到运行日志的工作流即声称完成 CI。
