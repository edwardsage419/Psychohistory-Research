# R065 Phase M：七模型作者时钟与实验区块时钟的留人比较审计

日期：2026-10-16。**研究结论：六模型双时钟对比有效；Model 5 因预先规定的重跑锚点失配而 FAIL CLOSED；七模型总体关口尚未通过。**

## 1. 先于结果冻结的设计

[Phase M 正式协议](../../protocols/R065_PHASE_M_SEVEN_NATIVE_TWO_CLOCK_2026-10-16.md) 首先提交于 `5e0e41c03d0536f4c59eefe0a01dac15c993957a`。继续使用原作者 `arielevy8/obs-learning-fishing` 固定提交 `fd5f435b5368b69916e7acc6a9991aa5f46b3ddb`。作者 `objectives.py` 固定 Git blob `5e98133fa274ef2a112b24f6fdcd802d4f9d3eec`，`fit_utils.py` 固定 blob `6046f083a1181b10a7d991c8c9fd2e53c1f2b487`。以来源哈希验证 Phase J 固定 24 名参与者的实验记录，保留总共 1,327 次 play。

作者原生时钟为 `[23,45,67,89,111]`。研究候选时钟为实验块起点 `[18,35,52,69,86,103,120]`。仅在已校验的作者源码**内存副本**中精确替换七个原有重置选择条件，原作者源码字节从未修改。原始作者时钟与原作者时钟内存适配器在七个模型、两套固定参数探针下做了全体 24 人 NLL 一致性门控。修改后版本应始终称为「作者模型的受审研究适配器」，不能称为未修改原作者程序。

两套时钟使用相同 Phase L 受试者分层两折、两固定起点、SciPy L-BFGS-B 统一优化设置与容差。每个时钟单独拟合，在未参与训练的另一半受试者上评分。若原生作者时钟重跑 NLL 与 Phase L 各折绝对差超过 1e-7，协议规定该模型 FAIL CLOSED，不得比较两套时钟。

## 2. 真实 CI、聚合结果与异常

[Phase M 原始 GitHub Actions run 38844279247](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38844279247)：八项作业中七项成功、一项失败；合并结论为 **failure**。30 项合成对照测试成功。失败作业是 Model 5 原生时钟锚点，且该作业在退出前已保留各折匿名聚合优化结果。原始七份匿名结果通过 GitHub Actions artifacts 获取，包含原始及候选时钟训练、留出、参数和起点调用计数；下载后二次核对 24 人/1,327 play、所有折 667/660 play、来源时钟、七模型身份、折级 NLL 加权恒等式。

下表 `Δ = 候选区块时钟 NLL/选择 - 原作者时钟 NLL/选择`，负值代表**本次固定内部留人评分**里候选时钟预测损失更低。仅列成功通过全部门控者。

| Model | 作者时钟留出 NLL | 候选时钟留出 NLL | Δ | 门控 |
|---|---:|---:|---:|---|
| 1 | 0.652143146 | 0.652146660 | +0.000003513 | PASS |
| 2 | 0.654715246 | 0.654401622 | −0.000313624 | PASS |
| 3 | 0.677494411 | 0.677484281 | −0.000010129 | PASS |
| 4 | 0.654015923 | 0.653363048 | −0.000652875 | PASS |
| 5 | 0.653466007 | 0.653453595 | **不批准比较** | **FAIL CLOSED** |
| 6 | 0.648259169 | 0.647877259 | −0.000381910 | PASS |
| 7 | 0.650629545 | 0.650024571 | −0.000604974 | PASS |

六项通过门控者当中五项总体 Δ 稍为负，一项近乎零的正值；**六个模型的 A 折均改善、B 折均恶化**。此折别方向冲突说明结果对样本划分敏感，不支持「实验块边界重置普遍更好」的稳健判断。两套时钟也同时改变了重置发生次数（5 次 vs 7 次）；目前不能把这一观察单独因果归因于边界对齐。

机器可核验的结果、两折数值、Phase L 原生重跑误差、两次拟合的聚合函数调用数量及七份 GitHub Actions artifact 标识已提交于 [R065_PHASE_M_TWO_CLOCK_AGGREGATE_RESULTS.json](R065_PHASE_M_TWO_CLOCK_AGGREGATE_RESULTS.json)。

## 3. Model 5 的失败门控及后验诊断

Model 5 两套时钟下的两折训练均报告数值收敛。原生时钟却无法满足与 Phase L 精确重算的一致性条件：

- A 折留出 NLL/选择偏差约 `+1.99465e-7`；
- B 折偏差约 `+3.84035e-6`；
- 事先冻结的可接受绝对偏差为 `1e-7`。

原生模型没有被修改，原始输入文件均通过 byte Git blob 校验；通过两份 CI 原始匿名 artifact 比对，已确认 Phase L 和 Phase M 实际收敛的潜在参数向量存在轻微差异，训练目标值也略有不同。不能凭这项观察直接确认是 BLAS、优化器平台或局部最优中的哪一种原因。

为界定差异，**在获悉失败以后**独立冻结了 [固定参数诊断方案](../../protocols/R065_PHASE_M_MODEL5_POSTHOC_FIXED_PARAM_DIAGNOSTIC_2026-10-16.md)，没有动原先 Phase M 方案及其阈值。该诊断拿 Phase L 和 Phase M 保存的四组 Model 5 原生潜在参数，分别交给哈希核验的同一原作者目标函数作零优化的纯数值评分。

[固定参数诊断 GitHub Actions run 38844938066](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38844938066) 两项作业均成功，7 项附加 synthetic 测试通过；四组固定参数的训练/留出 NLL 全部重现到接近浮点舍入精度。详细核验见 [Model5 固定参数 JSON](R065_PHASE_M_MODEL5_FIXED_PARAM_DIAGNOSTIC_RESULTS.json)。

**可支持的结论：** 相同已保存参数下原生评分可以重复；Phase L 与 Phase M 的微小差异发生在**重新优化取得的参数向量**上。具体优化轨迹/数值终点差异的成因尚未归因。本诊断不使原 Phase M Model5 PASS，不得修改原先七模型总体失败结论。

## 4. 研究解释边界和后续

- 现有结果是已看过 Phase J/L 后同一个原作者实验内的 24 人回顾性留人评分；无新队列，也无参加者层差值区间，不能当作外部独立预测认证。
- 共享人群参数研究优化方法与原作者历史层级 EM、个体后验与 iBIC 严格区分。
- Model 5 既然未通过已冻结的源结果可重跑关口，本轮**不存在一个已批准的七模型时钟比较排名**，所有声称七模型双时钟 PASS 均不成立。
- 进一步验证需事前冻结 Model5 优化数值稳定性/多次独立重跑协议，不得在本轮根据观察调整容差。仍须扩展至全 226 名合格参与者并检查层级 EM/iBIC，以及外部独立队列条件。

`R065_PHASE_M_SIX_MODELS_PAIRED_CLOCK = PASS_BOUNDED`

`R065_PHASE_M_SEVEN_MODELS_COMPLETE = NO`

`R065_PHASE_M_MODEL5 = FAIL_CLOSED`

`R065_PHASE_M_MODEL5_FIXED_PARAMS = REPLAY_PASS_POSTHOC`

`R065_FULL_226 = OPEN`

`R065_AUTHOR_HIERARCHICAL_EM_IBIC = OPEN`

`R065_EXTERNAL_VALIDATION = OPEN`

`PESEN_v0.1 = FROZEN`
