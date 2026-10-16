# R067 正式结题：从演化博弈数学机制到真人囚徒困境群体策略变化

日期：2026-10-16。正式状态：**CLOSED_BOUNDED**。验收依据 [统一研究验收标准 v1](../../protocols/RESEARCH_ACCEPTANCE_STANDARD_V1_2026-10-16.md)。这是一项科学上**限定范围**的正式研究资料包结题，不代表三种策略演化机制已被人类数据因果验证。

## 一、有限科学问题与已真实完成

**问题：** 三种简单策略比例更新（复制子 Euler、动态 Logit、最佳反应）在囚徒困境/协调博弈中有什么不同后果？在可核验的真人长期重复囚徒困境中，是否能有限比较场次总合作比例的一步条件预测？

1. 在冻结于 `protocols/R067_EVOLUTIONARY_GAME_STRATEGY_2026-10-16.md` 的数学机制上，囚徒困境矩阵 `((3,0),(5,1))` 与协调矩阵 `((4,0),(0,3))` 的合成 E1 试验、**22 tests**、真实 [CI run 38866940132](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38866940132) 全 PASS。[完整数学结果](R067_E1_GAME_STRATEGY_RESULTS.json)。Logit 动态反应**不是** McKelvey–Palfrey QRE 固定点求解。
2. R047 真实公共池资源来源 128 人/32 组、15 正式轮次：提取量 **45 种值**，32 组每组有至少三种提取行为；按已冻结协议判`DIRECT_BINARY_PD_MAPPING=BLOCKED_MODEL_MISMATCH`。真实来源及 10 tests 由 [run 38867710076](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38867710076) 核验 PASS；没有非法把资源提取值二分。
3. 独立真人长期重复 PD：原作者 `eladiomontero/PairwiseStrategies` 投稿固定 tag commit `4743f74d8a03a031b8f70aff64956f8ad5155182`。Git blob fixed `3bf78bf85f6642afee18d6f1965dca7272582f40`、shuffled `f5a86cd033b739da45d3fc7c5019068f612146a2`。源文件检查 [run 38868310370](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38868310370)：**188 人、12 场次、18,800 个明确定义 C/D 决策（7 tests PASS）**。原论文实验 payoff `R=3,T=4,S=0,P=1` 不等于数学 E1 玩具参数。正式 Dryad v8 的元数据真实核验成功，数据文件下载 403/401，故**投稿版与 Dryad 正式数据逐行等价 OPEN**。
4. [真人留场次协议](../../protocols/R067_E2_HUMAN_IPD_SESSION_HELDOUT_2026-10-16.md)在真实模型得分首次产生前冻结。使用实际 PD payoff，严格留出完整 12 场次中的一场，每折选参只基于另 11 场，逐次以该场次**已观察 x(t)** 预测下一轮 x(t+1)，总计 12×99=**1188** 个**相关的一步比例评价**，不是闭环 100 轮预测。真实 [run 38868663010](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38868663010) 两作业成功、12 tests PASS、源 Git blob 再验；[匿名聚合得分](R067_E2_HUMAN_IPD_LOSO_RESULTS.json)。

| 机制/基线 | **12 场等权留出 MSE** |
|---|---:|
| 动态 Logit 反应 | **0.0103771004** |
| 坚持当前合作率 | 0.0106089084 |
| 复制子 Euler | 0.0106249215 |
| 最佳反应 | 0.0106407025 |
| 其他同处理训练场次平均合作率 | 0.0219968829 |

Logit 相比持续性基线平均只略好，在固定伙伴 6 场甚至不如持续性预测；不能声称 Logit 已经解释人类策略心理机制。原论文个人 HMM、长期伙伴记忆的策略类型完全未复现。详细方法与反例见 [R067 E2 科学审计](R067_E2_HUMAN_BEHAVIOR_AUDIT.md)。

## 二、统一六门证据验收

| 门 | 结果 | 科学作用及明确限制 |
|---|---|---|
| A01 问题/范围 | PASS | 已完成 E1 双支付矩阵与有限 E2 真人单步群体比例预测；结题范围在阶段证据后限定，非声称原始宽泛目标全部通过 |
| A02 数据与来源 | PASS | 两套原作者 Git blob、两原始数据源及 R047 Stata/收益脚本、固定提交；Dryad 正式文件本身不能验证，必须记 OPEN |
| A03 实际可重放代码 | PASS | GitHub Actions 上真正验证源数据、合成数值、真人 12 场次留出及所有测试；不把 CI 运行状态等同未见科学假设 |
| A04 失败与反例登记 | PASS | R047 多动作不适用固定二策略、Dryad 403/401、投稿版本不保证最终一致、重复选择的统计相关性都保留 |
| A05 推断等级 | PASS | E1/E2/E3 严格分离、真实场次比例不是个人合作策略、固定/更换伙伴不同信息环境不构成因果机制验证 |
| A06 结题归档移交 | PASS | 正式结题报告、全部已运行 JSON、统计协议、开放科学问题和下一个模型家族 R068 已建立引用位置 |

## 三、严守科学结论边界

本研究没有复现原作者 HMM 的 AllC/AllD/TFT/WSLS 类别，也没有复原 Dryad 正式版数据、给出可靠的新 E3 队列或经济制度长期预测。数据虽有 18,800 行，但决定模型外推的不独立场次数是 **12**，并无场次级差异置信区间；不能把 MSE 数字差推广到全部社会。模型仅用前一轮观察到的合作比例进行下一轮预测，不能自称仅凭初始分布预测 100 轮过程。

**结题 `R067=CLOSED_BOUNDED`，而不是 `CLOSED_FULL`。** 后续策略记忆、博弈网络、外部实验、不确定性等进入 [开放证据清单](R067_POST_CLOSURE_OPEN_GATES.md)。下一主线转向社会学习与文化演化的另一模型家族 R068，不再不断加长 R067 内部阶段。

`R067_E2_HUMAN_ONE_STEP=PASS_BOUNDED`
`R067_CAUSAL_MECHANISM=NOT_ESTABLISHED`
`R067_DRYAD_FINAL_CONTENT=OPEN`
`R067_E3_EXTERNAL=OPEN`
`PESEN_v0.1=FROZEN`。
