# R073：真人重复囚徒困境——自己与对手前一/前两轮行为记忆，留场次条件预测

2026-10-17。**正式状态 `CLOSED_BOUNDED`。真实本人C/D下一轮行为预测 E2 内部留场次完整复验 `PASS`；人类记忆/社会信息因果机制未识别，独立E3 `OPEN`；PESEN v0.1 `FROZEN`。**

R072 的 PLOS 2016服务历史资料已核对原始表8个匿名组回复频数，但服务历史/中性处理编码缺独立来源字典，不允许通过发表效果倒猜处理后再验证因果。R073另建独立研究，转向真正含可明确定义历史行为/目标的真人重复博弈。

使用 [Montero-Porras et al. 2022, Scientific Reports DOI 10.1038/s41598-022-11654-2](https://doi.org/10.1038/s41598-022-11654-2) 原作者仓库 `eladiomontero/PairwiseStrategies` tag submission commit `4743f74d8a03a031b8f70aff64956f8ad5155182` 的固定Git blobs `fix.csv`、`rand.csv`。**只确证投稿版原始CSV，不冒充已核验Dryad最终v8字节等价**。两个实验处理FP固定同伴6场/92人，SP逐轮更换同伴6场/96人，全部100轮/人，共18800真人动作。按共同 `t=3..100` 在真正个人层目标上评分 **18424个下一次C/D**，并明确把 shuffled 的 `last opponent` 看作**过去而不是当前伙伴**。

## 协议、程序、实跑、永久档案

- [在首次真实模型得分之前冻结的独立研究协议](../../protocols/R073_HUMAN_IPD_LAGGED_SOCIAL_MEMORY_LOSO_2026-10-17.md)，commit `8f8e5451692065f1b62db0338bc5b4fa5def486f`。
- [真实CSV SHA再审计、时间窗口、7种预测模型、12场次LOSO程序](r073_human_ipd_memory_loso.py)，[23项纯虚构安全/时间先后/漏泄检查](test_r073_human_ipd_memory_loso.py)。
- [真正包含12整场留出、23项单测及18424个人决策的GitHub Actions run 38931506064](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38931506064)：两job **SUCCESS**，无个体样本文件进入Git。
- [第二次重新下载真实作者文件并复算、用精确SHA固定永久归档的Actions run 38931698718](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38931698718)：**SUCCESS**。真实匿名结果 8079字节SHA256 `6d9f6dc6c7a5f7d29aaf81b36c8d53cb88957a00c86c827019073b319936607a`，永久保存在 [R073_E2_HUMAN_12_SESSION_MEMORY_LOSO_RESULTS.json](R073_E2_HUMAN_12_SESSION_MEMORY_LOSO_RESULTS.json)。
- [全部误差、场次胜负、理论反例与边界分析](R073_REAL_HUMAN_MEMORY_E2_METHODS_RESULTS_AND_LIMITS_2026-10-17.md)。

## 主结果：个人历史反馈有效，但不是每个场次必然获益

七种真人下一次 C 的预定模型在12场等权 Brier 误差（越小越好）：处理平均基线 **0.226411**；只用本人上一轮 **0.134197**；只用上轮对手 **0.177831**；用双方上一轮 **0.124758**；用双方两轮 **0.120546**；无训练固定5%错误率TFT **0.253900**；WSLS **0.465069**。

在相同18424个评估目标与12整场留出条件下：
- 在本人上一轮记忆上加对手上一轮选择：Brier `−0.009439`，固定6/6场次改善、随机4/6改善2/6恶化；
- 在双方上一轮记忆再加一轮自己＋对手历史：Brier `−0.004212`，固定4/6改善2/6恶化、随机6/6改善。
- 固定TFT平均甚至差于仅训练平均率的基线，WSLS更差；只是拒绝**人人固定同一种严格带5%噪音策略**的过强概率模型，**不**否定任何真人可能使用近似TFT/WSLS。

**最大科学边界：** 历史反馈预测价值不等于心理记忆器官/信任/互惠的因果作用；前两轮真实动作当时已被参加者看到，teacher-forced条件预测不等于开放循环实时部署；12实验场次不等于历史世界E3独立跨域验证。本实验没有 R072 的公开第三方信誉规范，也不能说评判规则IMAGE/STANDING/STERN已获真人证实。

## 正式结题

[统一六门正式限定结题和源证明](R073_FINAL_ACCEPTANCE_AND_CLOSURE_2026-10-17.md) · [机器验收](R073_FINAL_ACCEPTANCE_STATUS.json) · [真实外部E3和心理因果机制仍开放](R073_POST_CLOSURE_OPEN_GATES.md)。

**`R073=CLOSED_BOUNDED`，`E2_TRUE_HUMAN_CONDITIONAL_PREDICTION=PASS`，`HUMAN_CAUSAL_MEMORY=NOT_IDENTIFIED`，`E3=OPEN`，`PESEN_v0.1=FROZEN`。** 后续应优先寻找第二独立实验来源以复验已经冻结的个人前两轮特征效果，而不是从同一作者已经看过的完整样本继续寻优。
