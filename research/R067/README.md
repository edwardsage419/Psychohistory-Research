# R067：群体合作策略的演化博弈机制研究

建立日期：2026-10-16。**正式状态 CLOSED_BOUNDED（2026-10-16，有限科学研究包结题），E2 真人数据的一步留场次验证 PASS_BOUNDED。**

**最新正式入口：** [结题/六门验收报告](R067_FINAL_ACCEPTANCE_AND_CLOSURE_2026-10-16.md) · [机读验收](R067_FINAL_ACCEPTANCE_STATUS.json) · [未完成问题与续研究](R067_POST_CLOSURE_OPEN_GATES.md)；下文保留当时 E1 及寻找 E2 数据的原始研究时间线，不应用早期 `E2 OPEN` 取代最新状态。

 从 [R066 已限定结题的群体意见研究](../R066/R066_FINAL_ACCEPTANCE_AND_CLOSURE_2026-10-16.md)转入**群体策略学习/制度合作**机制，避免一个 R 项目无限扩展研究范围。项目整体长期目标仍是多层级可解释、可检验、可重放的心理史学模型。

## 已冻结研究问题

[独立研究协议](../../protocols/R067_EVOLUTIONARY_GAME_STRATEGY_2026-10-16.md)在任何 R067 固定数值结果产生前提交：把同一 2×2 囚徒困境、协调博弈中的合作频率 `x` 分别按照 Taylor–Jonker 复制子 Euler、Logit 有噪反应、最优反应更新，比较策略演化数学后果。

**精确文献锚**：Taylor & Jonker (1978), DOI `10.1016/0025-5564(78)90077-9`；McKelvey & Palfrey (1995), DOI `10.1006/game.1995.1023`。第二项是 Logit/QRE 原始理论来源，但我们实现的是动态 Logit 响应，不是 QRE 固定点求解，也没有实证拟合原文。

[可运行纯 Python 程序](r067_strategy_dynamics.py) · [22 项数学/反例/稳定性测试](test_r067_strategy_dynamics.py) · [全部固定数值结果](R067_E1_GAME_STRATEGY_RESULTS.json)。

## 已成功执行的 E1

[GitHub Actions run 38866940132](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38866940132)：单项作业 completed/success、**22 tests / OK**。在 `x0=0.5` 下：

| 模型 | 囚徒困境第 1 步合作频率 | 协调博弈第 1 步合作频率 |
|---|---:|---:|
| 复制子 Euler | 0.4625 | 0.5125 |
| 动态 Logit 反应 | 0.4094851746 | 0.5462117157 |
| 最佳反应 | 0.4 | 0.6 |

更新 5 步及 20 步的数值完整留存于 JSON。这个结果来自人工固定支付矩阵，并未包含任何人的行为记录，不应当作现实社会合作率、心理机制或历史走势的预测。

## 下一个 E2 源数据关口

优先核查心理史学 R047 公共池资源/不平等实验已归档的作者 CSV，确认能否严格定义无二义性的 `合作/背叛` 二策略、可重放轮次和群体构成。**不允许**仅凭数据中出现“公共资源使用量”就将其当作囚徒困境策略频率；还要处理惩罚、组内禀赋差异、轮次重置和选择自相关。若不可辨识，拒绝该数据关联并寻找更适合的社会困境实验。

下一研究持续依据 [统一验收标准](../../protocols/RESEARCH_ACCEPTANCE_STANDARD_V1_2026-10-16.md)。PESEN v0.1 仍 `FROZEN`。

## 真实 E2 行为来源及有限场次预测（2026-10-16）

首先 [完整核验 R047 原始数据与作者收益函数](R067_E2_R047_APPLICABILITY_RESULTS.json)：它的 45 种不同公共资源提取量/32 个多值行为实验组不是 R067 固定二策略 PD；所以真实来源 PASS，但固定二策略的直接解释 BLOCKED。Dryad DOI `10.5061/dryad.37pvmcvmk` 元数据成功，而真实下载 HTTP 403/401，应为 OPEN。

随后用原作者 `eladiomontero/PairwiseStrategies` Git 固定投稿版数据，188 人/12 场×100 轮、18,800 个合法 C/D 行动 [来源报告](R067_E2_AUTHOR_SUBMISSION_IPD_SOURCE_RESULTS.json)；real source [GitHub Actions 38868310370](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38868310370) PASS。

[真实模型前冻结的留一场次实验协议](../../protocols/R067_E2_HUMAN_IPD_SESSION_HELDOUT_2026-10-16.md)，[全部匿名聚合结果](R067_E2_HUMAN_IPD_LOSO_RESULTS.json)，[详细源和预测限制审计](R067_E2_HUMAN_BEHAVIOR_AUDIT.md)。[GitHub Actions run 38868663010](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38868663010) 双作业 success、12 tests PASS；12 场次×99 个相邻轮次合作比例，整场留出训练其它 11 场，实验实际 PD `R3,T4,S0,P1`。总体 12 场等权 MSE：Logit 0.0103771、Persistence 0.0106089、Replicator 0.0106249、Best Response 0.0106407、其它同处理训练场平均 0.0219969。Logit 在固定伙伴场次不如 Persistence；单步模型差距很小，未验证个人策略的因果机制。

**依照六门统一标准，R067=CLOSED_BOUNDED；作者 HMM、Dryad 正式数据逐字节同一性、外部 E3 与历史跨尺度有效性均 OPEN。** 下一个研究编号为 R068，研究文化传播的从众/成功偏好和随机漂变。PESEN v0.1 保持冻结。
