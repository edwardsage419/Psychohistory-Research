# R068 E2：四选项真实社会频率的时间语义及原作者自我选择扣除检查

日期：2026-10-16。**在本研究首次解析原始受试者频率列的数值范围和前一轮配对之前冻结。** 已完成的字节/CSV 结构门 GitHub run `38870499060`：2 份 LFS 文件全部 SHA256 PASS，群体条件 12,880 行/57 列，个体条件 7,929 行/56 列，13 项来源反例测试 PASS。采用同一固定作者 Git commit `6fca0b26c33af3a5b3c415719fa3df0dced15149`，group/indiv LFS SHA256 见先前源协议。

## 可核验的原作者操作与边界

Toyokawa & Gaissmaier (2022) 的在线实验：群体每轮**同步**选择，学习者在 t 轮能看见 t−1 轮各选项被选择的次数；没有其他人的实际收益作为这一公开社会线索。作者源 `experimentalAnalysis/model_fitting/multiVar_model_fitting_both_1022.R` 固定 Git blob `86558839d1763e795613b804ad5579de774bd0da`，第 63–110 行：`choice_num+1` 是 1..4 的选项索引，第 1 轮 F=0，t≥2 时的社会频率 `socialFreq_safe1/safe2/safe3/risky` 包括自身 t−1 选择，作者通过 `F[i,lastChoice,t] = F[i,lastChoice,t]-1` 除去自己。F 全为 0 时用 −1 哨兵标记**无同伴信息**。这是真实来源的数据解释合同，不能直接把 CSV 字段当作精确三示范者多数。

## 本关预先确定的完整结构检查

- 原始群体 CSV `allBehaviour1022_group.csv` SHA256 `b01af9eb32945c57b6a9528c2f7e291e955819c1df799cfc942708473cd4ceb3`，字节 `4144197`；个体条件 `allBehaviour1022_indiv.csv` SHA256 `06ddbf5dbe64893f841ef6801c6e1e00553869eb774ee05740b8cf0d1f6801c1`，字节 `2306541`。
- 必要字段 `amazonID,room,round,riskDistributionId,choice_num,socialFreq_safe1,socialFreq_safe2,socialFreq_safe3,socialFreq_risky,payoff`。在群体表中使用 `amazonID` 和整数 1–70 轮建立纵向配对；出现重复 ID×轮、跨多个 room 的同一 ID、非法轮数或选项编号时必须记录匿名阻断，不自行修补。
- 先记录四选项频率是否可解析为**非负整数**。允许记录缺失类型计数，但不能在不同试验条件下补零。若任何非首轮合法个人观测减去上一轮自身选择后为负，记结构反例；后续使用该受试者—轮次做模型预测须 fail closed。
- 统计所有群体原始行、具有 t−1 前态者、具有合法本人和前一轮选择者、完成自身排除后可观察至少一位**同伴**选项者，以及前态缺失/匿名断裂行、四选项频率不合法行、不同风险条件混用的 room 数量。群体字段在某些 riskID 条件可能含有不存在的选项栏，但不能据字段名推断每个 riskID 均恰有 4 可供选择；报告各 riskID 总体匿名计数与有效选项代码集合，但不输出具体 room/user。
- 个体条件用于记录无同伴信息的背景对照，仅字段名称/受试者覆盖数/轮次覆盖等汇总；**不把个体组 socialFreq=0 视为对“从众”的反证**。
- 原作者 `drawing_figures_rev2.R` 明言某个 room 混合 riskID 11/12 产生异常；先报告混用 room 总数及影响行数，禁止静默过滤。后续拟合另冻规则。
- 最重要的识别结论：本来源可同时观察**同伴上一轮行为频率＋学习者当前行为**，但作者论文表示群体只看到选择频率；未证明展示同伴**实际 payoff**，因此 R068 E1 的 success-weighted copying **不能直接用此源检验**。后续最多基于可见频率对中性/频率强化模型做有限 E2 比较，必须包含个体强化学习/历史保持等竞争解释，不可直接宣布三种文化机制在真实数据上已比较。

输出只有匿名全体结构统计和 SHA；严禁任何个人 ID、逐组频率/小单元、个体反应记录及来源数据行离开 runner。测试至少覆盖自身扣除、跨个人轮次错误配对、无前轮/无同伴、负频率、群组混合、无个人泄漏，具体结果以真实 CI 为准。

`R068_TEMPORAL_MEASUREMENT_PROTOCOL=FROZEN`
`R068_EXACT_THREE_DEMONSTRATOR_BINARY_MECHANISM=NOT_DIRECTLY_OBSERVABLE`
`R068_DEMONSTRATOR_PAYOFF_SUCCESS_BIAS=NOT_OBSERVABLE_FROM_SOCIAL_CUE`
`R068_REAL_PREDICTIVE_FIT=NOT_AUTHORIZED`
`PESEN_v0.1=FROZEN`
