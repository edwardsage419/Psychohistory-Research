# R067：真人博弈策略动力学的真实证据与阻断记录

日期 2026-10-16。研究层级：`E1` 数学机制、`E2` 真人来源与原实验内部场次留出；**非 `E3` 外部新实验**。

## 1. R047 数据为什么不能直接作为二策略囚徒困境

作者 `lrdegeest/InequalityCPR` 固定 commit `1142b0915a0a46e72264358378b3535948f6b2b4`，源 `data.csv` Git blob `73c02176bc9e060af987149594a85f9f7b591230`。作者 `theory_payoffs.R`（blob `8b6f116b0e1f4b750ceb312a46a0b6f505faf09d`）明确说明行为是公共资源连续提取和非线性群体收益，而非固定对称 2×2 C/D 支付。经过先冻结 [真实数据适用性协议](../../protocols/R067_E2_BEHAVIORAL_DATA_APPLICABILITY_2026-10-16.md)，[run 38867710076](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38867710076) 两作业成功、10 测试 PASS。2,048 条实验原始记录，剔除第 1 练习轮后 1,920 行、128 名独立被试、32 个四人组，提取量共有 **45 种不同数值**，且 **32 组均出现至少 3 种**。将它二值化会人为创造不存在的实验策略。因此 `R047_SOURCE=PASS`，`DIRECT_BINARY_PD_MAPPING=BLOCKED_MODEL_MISMATCH`，负面证据已经永久归档于 [R067_E2_R047_APPLICABILITY_RESULTS.json](R067_E2_R047_APPLICABILITY_RESULTS.json)。这不妨碍未来其他连续/多行动社会困境模型研究 R047。

## 2. 2022 年真人长期重复 PD 作者数据来源

正式原论文 Montero-Porras et al., *Inferring strategies from observations in long iterated Prisoner's dilemma experiments*, Scientific Reports (2022), DOI `10.1038/s41598-022-11654-2`；Dryad DOI `10.5061/dryad.37pvmcvmk`。Dryad v8 元数据/CC0 许可成功核验，但 [run 38868028814](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38868028814) 的真实数据下载得到 HTTP 403（文件流）和 401（API），尽管 8 项程序边界测试 PASS，**最终 Dryad 原始文件并未核验成功**。不得把这一 run 的 CI success 和内容可用混同。

另在**作者本人**的 `eladiomontero/PairwiseStrategies` 公开原始代码仓库找到不可变 `submission` tag commit `4743f74d8a03a031b8f70aff64956f8ad5155182`，其中包含可下载真实动作 CSV：`fix.csv` Git blob `3bf78bf85f6642afee18d6f1965dca7272582f40`（988,279 字节），`rand.csv` Git blob `f5a86cd033b739da45d3fc7c5019068f612146a2`（1,112,614 字节）。

在首次读取全部文件前提交 [作者投稿来源协议](../../protocols/R067_E2_AUTHOR_SUBMISSION_IPD_REAL_CSV_2026-10-16.md)，[run 38868310370](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38868310370) 真实 CSV 源哈希/格式全 PASS、7 项边界测试成功。匿名源统计：

| 处理 | 人数 | 场次 | 每人轮次 | 实际 C | 实际 D |
|---|---:|---:|---:|---:|---:|
| 固定伙伴 fixed | 92 | 6 | 100 | 5,161 | 4,039 |
| 随机更换伙伴 shuffled | 96 | 6 | 100 | 2,738 | 6,862 |
| 合计 | 188 | 12 | 100 | 7,899 | 10,901 |

此统计是行动行数，不是 18,800 名被试；源核验未发现无效 C/D、同一受试者同轮重复项或缺失的源行动。作者投稿 tag CSV 与 Dryad 正式 v8 **是否一致仍未知**；不把它标为 Dryad 内容已复现。所有输入个体记录仅在 CI 临时文件中，研究仓库中只发布匿名计数及哈希：[源审计 JSON](R067_E2_AUTHOR_SUBMISSION_IPD_SOURCE_RESULTS.json)。

## 3. 真实 12 场次 leave-one-session-out 动态预测

[冻结协议](../../protocols/R067_E2_HUMAN_IPD_SESSION_HELDOUT_2026-10-16.md)在本研究首次真实预测损失出现前独立提交，commit `a7faa8051e252bb10a148d3db8363560ce9183ec`。真实实验静态 PD payoffs 为 `(R,S,T,P)=(3,0,4,1)`，而不是 R067 合成教学 `T=5`。此 PD 对所有总体合作比例的 `π_C−π_D=-1`，构成强的、从个体回报出发的复制子动态方向约束。

**真正预测目标：** 每个实验场次已有 `t` 轮合作比例 `x_t`，预测下一轮群体比例 `x_{t+1}`。每场 100 轮，99 次条件单步转移，共 **12 场×99=1,188 次**。每一折完全留出一场，训练另 11 场选择各模型的固定网格参数，留出场次下一轮比例只作为测试标签。每场 99 次转移不是 99 个独立实验单位；主要指标是 12 场平均 MSE。使用 t 轮**真实已观测比例**意味着测试是 *teacher-forced 一步*，绝不是从第 1 轮连续闭环预测 100 轮。

[run 38868663010](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38868663010) 两作业均成功、12 项数学与留出隔离测试通过；真实输出和全部参数选择频次保留在 [R067_E2_HUMAN_IPD_LOSO_RESULTS.json](R067_E2_HUMAN_IPD_LOSO_RESULTS.json)。

| 模型 | 12 场等权留出 MSE | 固定伙伴 6 场 MSE | 变更伙伴 6 场 MSE |
|---|---:|---:|---:|
| 无参数 Persistence | 0.0106089084 | **0.0082460986** | 0.0129717182 |
| 复制子 Euler | 0.0106249215 | 0.0083956139 | 0.0128542291 |
| 动态 Logit 反应 | **0.0103771004** | 0.0088193169 | **0.0119348840** |
| 最佳反应 | 0.0106407025 | 0.0084505898 | 0.0128308153 |
| 同处理训练均值（非动态） | 0.0219968829 | 0.0275238906 | 0.0164698753 |

Logit 在 12 场总体上略低于坚持性基线（差 `−0.00023180798`），但固定伙伴的条件单步预测反而更差；该模型最常被选择的是 `lambda=0.5,eta=0.1`（11/12 场），剩下 1 场 `eta=0.2`。复制子常选最小或次小步长 `dt=0.01/0.05`，最佳反应常选 `eta=0.01`，这意味着强制下降方向并没有稳定解释现实合作比例变化，不能据此宣布真人行为由特定理论生成。

## 4. 科学边界与阶段性决策

- 真人重复博弈的固定伙伴长期互惠、条件反应（TFT/WSLS）等行为无法被本轮只依赖总体 `x_t`、无需伙伴历史的单步动态充分辨识。原论文个人策略 HMM 没有复现，且不应该冒称已重建。
- 原作者 Git 提交是来源可校验的 E2，但与 Dryad 终版等价 `UNKNOWN`；不是 E3，不是可跨地区外推的独立人类队列。**只有 12 个场次**，没有事先配对误差置信区间、处理效应因果识别。
- 候选是结果前冻结的统一有限网格，五类比较存在不同参数复杂度。主要值差别不大，不根据这次排名升级原创主模型。
- 确认数据**真正二元**与 R047 的连续/多策略实证区别，正是选用该独立源的关键科学改进。
- 建议按六门验收做 **R067=CLOSED_BOUNDED**，将 HMM 策略识别、真实 Dryad 终版完整性、不同实验与个人异质性作为后续独立研究。下一主线转向新理论家族，不在一个 R 下无界扩展。

`R067_E1=PASS`
`R067_R047_SOURCE_VALID=PASS`
`R067_R047_BINARY_PD_MODEL_MAPPING=BLOCKED`
`R067_AUTHOR_SUBMISSION_HUMAN_DATA=PASS`
`R067_DRYAD_FINAL_BYTES=UNRESOLVED`
`R067_REAL_HUMAN_12_SESSION_ONE_STEP=PASS_BOUNDED`
`R067_E3_EXTERNAL=OPEN`
`PESEN_v0.1=FROZEN`
