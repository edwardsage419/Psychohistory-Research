# 心理史学研究主控台 v4.3（2026-10-15）

继承 [v4.2](RESEARCH_CONTROL_v4.2_2026-10-15.md) 的全部历史记录。本文件只加入 R065 第三阶段的已核验证据和下一道研究关口，旧版内容保持原字节，不回溯修改 R001 至 R064 研究。

## 当前继承

* 历史记录：R001 至 R064，现有清单含 74 个历史 ZIP、163 项独立文件，已记录以前归档过程的 CRC、SHA256 与 Git blob 状态。本次不重新声称所有单轮研究科学结论都已重算。
* R065 Phase A：Levy 等人固定处理后 CSV 的 SHA1 核对和关键试次统计，完成连接器端真实数据分析。
* R065 Phase B：时间趋势、收益条件先后顺序和参与者 Bootstrap，完成回顾性真实数据分析。初末实验块之间的直接模仿比例变化尚不能确认心理机制。
* **R065 Phase C：原作者固定源码的七模型状态重置日与八块正式实验时间轴对齐审计**。研究报告：[R065 Phase C](../research/R065/R065_PHASE_C_RESET_AUDIT.md)。

## R065 Phase C 新证据

源文件 `arielevy8/obs-learning-fishing/model_fitting/objectives.py` 的 Git blob SHA1 为 `5e98133fa274ef2a112b24f6fdcd802d4f9d3eec`；GitHub 连接器直接取得并核对七模型源程序，每个模型都使用 `[23,45,67,89,111]` 作为状态重置条件。模型拟合入口 `fit_hierarchical.py` 从 `data` 目录读取原作者逐参与者文件，`fit_utils.py` 筛选正式试次。

原作者单人原始文件确认正式实验日 1 至 136 共 136 个连续日期。处理后固定 CSV 确认 295 名参与者均有日 4、21、38、55、72、89、106、123 的关键选择；每 17 日一个区块，内部边界 18、35、52、69、86、103、120。七模型源码重置日期与真实区块起点没有重合。第 89 日属于关键选择，源码会在当前行预测前清零模型历史状态；在任务的等权初始信念、规范化三代币转移矩阵与两条可选船下，各模型会退化到约 `[0.5,0.5]` 选择概率。这是结构反例，不代表发表结果已经被独立推翻。

本地新增可运行的 SHA 严格约束源码 AST 审计程序、代数校验和 10 项新测试；**累计 25 项本地构造样本与逻辑测试通过，0 项失败**。原始作者源码的本地 SHA 校验及人类原始实验数据的模型拟合仍 **OPEN**。

## 状态与下一个最小关口

* `R065_PHASE_A = COMPLETE`
* `R065_PHASE_B = COMPLETE`
* `R065_PHASE_C_SOURCE_ALIGNMENT_AUDIT = COMPLETE`
* `R065_FULL_RESEARCH_GATE = OPEN`
* `PUBLICATION_FIT_EFFECT_OF_RESET_MISMATCH = UNKNOWN`
* `SOURCE_AND_TRIAL_LOCAL_END_TO_END_REPLAY = OPEN`
* `PESEN_v0.1 = FROZEN`

后续应从精确作者版本的 Python 代码和原始逐试次文件开始，核对实际拟合版本、相同参与者留出方案下两套重置方案的对数损失及不确定性。暂不将 R065 观察相关性改写为原创历史动力学参数。
