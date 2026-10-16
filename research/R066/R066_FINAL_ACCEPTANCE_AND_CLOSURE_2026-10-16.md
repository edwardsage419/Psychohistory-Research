# R066 正式限定结题报告：三种群体意见动力学机制与实证村庄预测

结题日期：2026-10-16。状态：**R066=CLOSED_BOUNDED**（有限研究任务的正式证据/档案结题；不是三类模型真实机制的完成认证）。验收依据：[统一六门标准](../../protocols/RESEARCH_ACCEPTANCE_STANDARD_V1_2026-10-16.md)。本研究最早的三模型机制测试协议按结果前提交，但后续实证探索是已读文献及数据集结构后的**回顾性方案**；不可称初始对真实现场实验已预注册。原始实验 E3 外部新队列与历史层推断保持 OPEN。

## 1. 研究任务及真正取得的证据

**问题：** DeGroot、Friedkin–Johnsen (FJ) 与 Hegselmann–Krause (HK) 如何在相同初态条件下形成不同的群体意见轨迹？在具备真实调查意见与源可验证人际关系的数据集上，能否得到有局限的跨村预测比较？

- **E1 合成机制：PASS。** [三模型原始研究协议](../../protocols/R066_OPINION_DYNAMICS_THREE_MODELS_2026-10-16.md)先固定机制，三组测试初态 [0,0.2,1] 产生 DeGroot [0.4,0.4,0.4]、FJ [0.2,0.3,0.7]、HK [0.1,0.1,1]。GitHub Actions [38845611874](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38845611874) `success`，25 项测试 PASS。
- **两份较差匹配的实证数据：源审计 PASS、三模型状态识别 BLOCKED。** [Reddit + 标注帖子审计](R066_E2_TWO_DATASET_SOURCE_AND_MEASUREMENT_AUDIT.md) run [38861027481](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38861027481)，519,655 行互动与帖子得分，另有 9,944 条标注意见帖（300 个不同 ID；README 提及 100 名，口径差异 OPEN）；缺少同时可信的真实连续意见、社会影响边。这些失败是科学筛选结果，不能被忽略。
- **第三份真人网络加问卷数据：源与机制输入的技术性可复现 PASS。** Larson–Lewis (2026) DOI `10.1017/nws.2026.10038`，16 个乌干达村庄，Harvard Dataverse `doi:10.7910/DVN/RAHSVM` V1.0 CC0；2,125 行×66 列，六题形成 6–30 态度量表；1872 行基线和末次同时完整。全部源文件 SHA256 固定，代码本和作者 R 原件核验，元数据/原始文件/字段审计各 CI 成功，详见 [总来源审计](R066_E2_LARSON_LEWIS_REAL_SOURCE_AND_NETWORK_AUDIT.md)。
- **网络原始算法交叉核验：PASS。** 原作者 R `make_el`、`convert_to_hh` 用真实数据原封执行，Python 独立复算全部四类 14,767 条分类去重家庭边，**全集边差均为零**；类型合并后 8,659 条唯一无向家庭联系。[真实逐边报告](R066_E2_AUTHOR_R_CORE_EDGE_PARITY_AUDIT.md) · [GitHub Actions 38865507356](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38865507356)，11 项测试 PASS。完整作者 R/igraph 后续统计与作者论文因果结论并没有逐数重现。
- **内部整村真实预测：PASS_BOUNDED。** 在结果前独立提交 [16 村留出协议](../../protocols/R066_E2_THREE_MODELS_LOVO_2026-10-16.md)，用 15 训练村拟合每个模型族的参数网格和共同漂移，每折仅预测剩下一村末次态度，合计 16 折/1,872 个有真实基线和末次测量的家庭行。[GitHub Actions 38866210819](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38866210819) 双作业 `success`，17 项合成隔离测试 PASS。主要 16 村等权留出 MSE：Persistence+drift `0.04227103404620483`，DeGroot `0.028614616600241692`，FJ `0.0266149141842743`，HK `0.0265478188648263`，其后两者差 `0.0000670953`。个人加权 MSE/MAE 则 FJ 略低于 HK。该内部表现不是新的社会因果效应估计、不是新的 E3 队列、不是长期制度或历史预测。

## 2. 六门统一验收状态

| 门 | 状态 | 限定解释 |
|---|---|---|
| A01 具体研究问题与限定交付 | PASS | 三类意见模型数学机制、严格来源数据、一次真实研究内的整村留出及负结果均已记录；限定结题范围为**事后明确的已完成工作**，不能当成起点就采纳的完整方案 |
| A02 来源与证据可校验性 | PASS | 实验原论文/DOI、已发布 CC0 Dataverse V1.0、原作者 R、DOCX、原始数据 SHA256；只归档匿名聚合 |
| A03 完整可重放计算 | PASS | E1 25 tests；真实源/文件/网络/ R–Python 边全集与 16 折实验均在 GitHub Actions 有成功作业；每步程序在本仓库存档 |
| A04 反例及失败保留 | PASS | 前两候选测量受阻、README 100 vs 300 不一致、早期直接 ego ID 键未通过、同源完整 igraph 未复算；未删去或伪造通过 |
| A05 推断与计量边界 | PASS | E1 / E2 / E3 分离，明确 HK 全连接不使用真实 W，FJ/HK 几乎持平但无村级不确定性，记录非随机网络与干预复杂性 |
| A06 最终归档和移交 | PASS | 本文、匿名机读验收、原始复现档案、未完成科学问题 BACKLOG，以及新 R067 主线入口，GitHub main 已同步 |

六门 **PASS 的对象是完整归档的有限研究工作及诚实的边界说明**，绝非每个开放的科学主张都 PASS。它遵循 [统一验收规程](../../protocols/RESEARCH_ACCEPTANCE_STANDARD_V1_2026-10-16.md) 的 `CLOSED_BOUNDED` 定义。

## 3. 不可宣称与仍未解决的问题

1. **无实证机制因果识别。** 真实网络结构并非随机分配，研究处理复杂，模型状态和可能的干预后机制均有误差；四种模拟的差异可由一般意见收缩/共同漂移解释。
2. **无 HK 胜出稳健结论。** HK 主要指标仅略优 FJ；个人加权评分反而 FJ 略优，且两者使用不同网络信息结构与候选网格；当前没有村级配对置信区间。
3. **无外部独立验证。** 16 村均来自同一现场研究，包括 2021/2023 两批与地域差异；跨村留出是 E2，而不是 E3 的另一项研究。
4. **无原作者全部 R/igraph 分析复现。** 只证明作者两核心家庭边函数逐边计算一致，不表示完整图模型、统计回归与论文全部结论已重算。
5. **无心理史学历史尺度推断。** 三模型跨层级整合与制度动态尚需独立理论、数据、检验。PESEN v0.1 一律 `FROZEN`。

详细未解决项见 [R066_POST_CLOSURE_OPEN_GATES.md](R066_POST_CLOSURE_OPEN_GATES.md)；重启需要新协议，不自动扩大 R066。

## 4. 后续主线：R067 演化博弈与合作制度

下一编号转向另一模型家族：**演化博弈中群体合作/背叛比例的复制子动态、有限噪声行为选择和策略更新**，与本次意见形成层级不同。先开展数学机制、来源审计和简单的可计算反例，再寻找可合法复核的公共物品/社会困境原始实验；不把 R066 的模型排名引入 R067 当作真实合作行为参数。

最终归档：
`R066=CLOSED_BOUNDED`；
`R066_E2_REAL_16_VILLAGE_LOVO=PASS_BOUNDED`；
`R066_REAL_MODEL_CAUSAL_MECHANISM=NOT_ESTABLISHED`；
`R066_AUTHOR_FULL_IGRAPH_ANALYSIS=OPEN`；
`R066_E3_EXTERNAL=OPEN`；
`PESEN_v0.1=FROZEN`。
