# 心理史学研究主控台 v4.4（2026-10-16）

继承 [v4.3](RESEARCH_CONTROL_v4.3_2026-10-15.md) 全部历史版本并保留原始 Git 文件。心理史学正式研究仓库为 `edwardsage419/Psychohistory-Research` 的 `main` 分支。

## 当前档案与未变更的历史状态

R001 至 R064 的文件归档清单仍记录 74 个历史 ZIP 和 163 个独立文件。归档存在与 CRC、SHA 校验属于文件证据；大量旧轮次及外部真人研究的科学复现尚未逐一重跑。R063 的动态社会学习参数、R064 的观察学习全试次分析、R065 的关键诊断试次等项目原有研究状态保持。

PESEN v0.1 保持冻结。不能把本轮四种 Bernoulli 描述性预测模型的时间块参数当作已经识别的心理机制参数，更不能直接上推为社会制度与历史演化系数。

## R065 Phase D：回顾性四模型预测与训练泄漏纠正

已经先于本阶段新评分提交 [独立记录的后续比较方案](../protocols/R065_PHASE_D_RETROSPECTIVE_PLAN_2026-10-16.md)。因研究者已在 Phase B 看过时间下降趋势，此方案的身份仍为“事后冻结的探索性计算”，无独立前瞻性。

Levy 等人固定处理 CSV Git blob `01bf211468abe093618dfa5e5c39e883230c9c03`；16,103 行原记录、295 名原受试者，按同一作者排除标准选取 226 人的 1,808 个关键选择。四种概率模型均使用相同的 Beta(4,4) 平滑、留整人训练与每人平均 Log loss/Brier。

| 模型 | 特征 | Log loss | Brier |
|---|---|---:|---:|
| M0 | 总体统一模仿率 | 0.664809596 | 0.235934555 |
| M1 | 按收益 high/low | 0.665153759 | 0.236096921 |
| M2 | 按八个关键实验块 | 0.661562755 | 0.234359476 |
| M3 | 实验块×收益 | 0.663022395 | 0.235036474 |

M2 对 M0 的差值 `−0.00324684`，20,000 次参与者重抽样 95% 区间 `[−0.00824466,+0.00169014]`，跨零。M3 对 M2 的差值 `+0.00145964`，区间 `[−0.00247556,+0.00541067]`，也跨零。M1 对 M0 的差值 `+0.00034416`，是本批数据上的小幅预测下降。

**算法纠错**：第一版临时实现错误地只从训练率剔除当前行，泄漏同一被试的其他关键行为。该版分数被弃用，没有写入最终 Phase D 数据 JSON。正式版本以参与者全部 8 次记录从每个训练单元整体扣除；计算所得 M0/M1 与 Phase A 的已经保存数值完全一致（公差 1e−10）。

**区间边界**：参与者重抽样是在已产生的交叉验证损失上进行，并未对每个 Bootstrap 重新训练所有模型，因此是条件性区间，不能自动当作“换一个独立样本并重训”场景的完整统计不确定性。时间趋势在前一阶段已被看过，模型分数不构成独立发现。

## 文件与执行状态

* [Phase D 研究审计](../research/R065/R065_PHASE_D_PREDICTION_AUDIT.md)。
* [机读结果](../research/R065/R065_PHASE_D_PREDICTION_RESULTS.json)。
* [本地 Python 复算](../research/R065/r065_phase_d_loso.py)及[新增测试](../research/R065/test_r065_phase_d_loso.py)。
* [GitHub Actions 工作流](../.github/workflows/r065-reproducibility.yml)已提交，拟从原作者固定提交读取并哈希核对源码和 CSV，运行已有测试以及 R065 A、B、C、D 对照重算。工作流是否已经运行成功，**目前未获得肯定证据**；不能将其计入 PASS。
* 当前容器实际执行四项独立的 synthetic 留人逻辑测试，均通过；原作者完整真实 CSV 在本地下载受 DNS 限制，正式 Python 全数据复算尚未完成。

## 研究准入状态

`R065_PHASE_A=COMPLETE_BY_EXISTING_EVIDENCE`，`R065_PHASE_B=COMPLETE_BY_EXISTING_EVIDENCE`，`R065_PHASE_C=BOUNDED_SOURCE_AUDIT_COMPLETE`，`R065_PHASE_D=CONNECTOR_REPLAY_COMPLETE`。

`PHASE_D_LOCAL_RAW_CSV_REPLAY=OPEN`，`GITHUB_ACTIONS_EXECUTION=UNVERIFIED`，`R065_FULL_RESEARCH_GATE=OPEN`，`PESEN_v0.1=FROZEN`。

下一最小动作是获取工作流实际日志、处理若有的执行失败、记录准确的执行与来源证明。若工作流没有运行，不得把新增测试或完整数据重放标为完成。只有复现与严谨的第三方留出样本就绪后，才考虑复杂的时序认知模型比较。
