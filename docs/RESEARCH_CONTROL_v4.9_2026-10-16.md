# 心理史学研究主控台 v4.9（2026-10-16）

本版继承 [v4.8](RESEARCH_CONTROL_v4.8_2026-10-16.md)，保留 R001–R064 全部归档及 R065 Phase A–H 的实证与方法边界。PESEN v0.1 仍冻结。

## R065 Phase I：模型三状态时钟差异的参数稳健性

本轮先提交 [Phase I 事后研究协议](../protocols/R065_PHASE_I_MODEL3_BETA_PROFILE_2026-10-16.md)，然后读取 Phase H 指定的十份固定版本原作者逐人原始 CSV，在 GitHub 连接器中重新解析每人 136 条实验试次和 542 次 `play`，转化为 Model 3 的匿名充分计数。

| 状态重置方案 | 复制最近示范 | 拒绝最近示范 | 无可用最近示范 |
|---|---:|---:|---:|
| 作者代码 [23,45,67,89,111] | 182 | 120 | 240 |
| 对齐区块 [18,35,52,69,86,103,120] | 188 | 135 | 219 |

使用与作者 `model_3_objective` 一致的 Softmax 和 `-log(p+1e-10)`，把 β 范围固定为 [0,30]：

| 指标 | 作者时钟 | 区块时钟 |
|---|---:|---:|
| Phase H 固定 β=5 NLL/选择 | 1.41768147 | 1.52946179 |
| 全样本拟合 β | 0.41651496 | 0.33116721 |
| 全样本最小 NLL/选择 | **0.68132114** | 0.68508810 |
| 十折留一整人预测 NLL/选择 | **0.68635134** | 0.69086496 |

对十人逐人留出、每次其余九人拟合 β 的前提下，区块重置相对作者重置的平均损失差约 +0.00451，远小于 Phase H β=5 的 +0.11178。这说明 Phase H 效应幅度对参数值敏感，不能简单解释为时间规则本身在真实人群中的确定优劣。

当前证据仍限定于便利选取的十人、未经过作者正式排除的样本和单一 Model 3，且新最优化是在既有问题发现后开展。不是七模型拟合、独立试验或认知机制证据。

## 精度修正与执行

本轮修订 Phase H `r065_phase_h_model3_reset.py` 的高 β 小概率分支计算方式，避免 `1−p` 在 β=30 附近的浮点消减误差，确保与作者 Softmax 直接分支语义一致。新增回归测试。**本地 Phase H 测试共 13 项、Phase I 新测试共 12 项，25 项全部通过**。

交付：
* [Phase I 审计](../research/R065/R065_PHASE_I_AUDIT.md)；
* [模型计数、全样本优化、留人结果 JSON](../research/R065/R065_PHASE_I_RESULTS.json)；
* [Python β 剖面与十折重放程序](../research/R065/r065_phase_i_beta_profile.py)；
* [12 项新测试](../research/R065/test_r065_phase_i_beta_profile.py)；
* [独立 GitHub Actions 离线与真实来源复算流程](../.github/workflows/r065-phase-i.yml)。

**真实来源状态**：十份原作者逐人 CSV 在 GitHub 连接器侧实际读取并计算；本地容器未取得这些原始文件，因此目前仅运行真实匿名计数算术与合成试次单测。本地 Python 逐人数据重放、原作者 native scipy/numpy 代码执行，以及全部七模型拟合仍未执行。GitHub Actions 工作流配置已提交，但无成功日志证据，不能当作已完成 CI。

准入：`R065_PHASE_I_SOURCE_EQUIVALENT_BETA_PROFILE=BOUNDED_COMPLETE`；`R065_PHASE_I_LOCAL_TESTS=PASS_25`；`GITHUB_ACTIONS_RUN=UNVERIFIED`；`SEVEN_MODEL_NATIVE_REFIT=OPEN`；`R065_FULL_GATE=OPEN`；`PESEN_v0.1=FROZEN`。
