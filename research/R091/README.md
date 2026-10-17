# R091：另一真实原作者灾害公共品实验190个四人组完整留出M0/M1/M2（正式结题）

日期2026-10-17。**R091=CLOSED_BOUNDED；真正不同原作者的已发表2025真人实验E2样本外组间预测成功，A01–A06全部有界PASS；不是新实验E3；PESEN v0.1继续冻结。**

Jonsson & Jonsson (2025) [*Cooperation in the face of disaster*](https://doi.org/10.1371/journal.pone.0318891)，*PLOS ONE*。一手原始作者仓库 [markusrobertjonsson/condcoop](https://github.com/markusrobertjonsson/condcoop) 固定commit `2a23fc3221e636c0119b1d1f1a9c4945bca83e85`；完整原作者工作簿 `Data_Main.xlsx` **571844字节**，原始Git blob `499787e08242c44c32a469b5d72b206ccf2c73f0`，源码实际核验全文件SHA256 `04d2ed5a59885cde2a1740f33b295a86bd374b80cd811d8ff84c88cded68a023`。原作者主sheet `DiffTreatments` 有15,200真人贡献行；另一瑞典概率扩展`DiffProb`的6,640行可能重叠，**绝不直接合并**。论文报告884人，但本次实际合格主sheet**760个真实不同人，190个跨20轮固定四人组**，国别菲律宾111组/瑞典79组，十个国别×实验条件层，每层至少12组。

研究首次经历源隐私检测合成失败[run39015518318](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39015518318)（头部错误可把隐私内容当列名）、真实来源映射FAIL CLOSED [run39015866343](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39015866343)，随后在完全不看原始贡献的[类别独立审计run39015992841](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39015992841)以首方原始文件证实 `Phils/Sweden`及`Control/10Prob/40Prob/40Impact/40Level`，分别先[冻结准确码本](../../protocols/R091_PHASE_B3_AUTHOR_ORIGINAL_FIXED_COUNTRY_TREATMENT_MAP_BEFORE_ROSTER_RERUN_2026-10-17.md)，再于[实际原作者全部190稳定四人组来源无行为审计run39016070946](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39016070946)全PASS。

在任何真实贡献数值评分之前提交[正式冻结跨原作者LOOG合同](../../protocols/R091_PHASE_C_190_AUTHOR_4PLAYER_GROUP_COMPLETE_LOOG_M0_M1_M2_BEHAVIOR_SCORING_FREEZE_2026-10-17.md)，提交`2992a91e64530d2405e2dd05e9e6808f8171afe5`：真实四人每轮0..20单位贡献合成组全球公共投入占比 `sum(c)/(4*20)`。逐次完整留出190个组（全部4人/20轮），只用其它同国家同处理组在同轮的M0基线；M1仅用目标组自己的上一轮记录；M2固定两者各半；t2..20每组19目标共 **3610个真实组轮预测**。M0能读取训练其它组同轮的实验记录，因此是**跨组留出泛化**而非完全历时实时预测。不得将四人连续贡献比率和R089六人二元global投资比率说成同一行为定义。

**真实结果：**

| 冻结模型 | 均方误差MSE（低更好） | 相对M0改善 |
|---|---:|---:|
| M0其它组同国同条件同轮 | 0.038495984 | 基线 |
| M1目标组自己上一轮 | **0.019200139** | **+0.019295846** |
| M2二者各半 | 0.019328371 | **+0.019167613** |

菲律宾111组M1增益+0.022346565，瑞典79组+0.015009391；所有10个国×处理分层M1、M2对M0平均增益均>0，但**190组中仍有48组M1劣于M0（142较好，0相等）**，所有反例均保留。对照[R089](../R089/README.md)内部六人二元群体历史阳性、[R090](../R090/README.md)独立六人气候俱乐部连续贡献M1阴性且249/2700记录为自动决策、R091本次四人连续贡献阳性，结果只支持**跨环境预测作用异质，不能宣布普遍群体学习规律**。

[首次实际原作者全量行为复算CI39016300977](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39016300977) 与 [独立再次原始Git固定blob下载、100synthetic重复和整个结果逐字节重算归档CI39016368841](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39016368841) 均SUCCESS；全部[匿名190组/国/处理3510? 正确**3610组轮**E2结果JSON](R091_INDEPENDENT_JONSSON_190_FOURPERSON_GROUP_3610_LOOG_M0_M1_M2_E2_RESULTS.json) **18471字节** SHA256 `1657ee31c5df7640ea7a0943886900133e68f70c0f9c3ac900302d36191f723b`，Git blob `2f39bcda3560abbcda780051dedf9ee5e8b08863`；完整[正式A01–A06科学报告](R091_JONSSON_2025_190_FOURPERSON_GROUP_CROSS_AUTHOR_HISTORY_TRANSFER_E2_SCIENTIFIC_REPORT_2026-10-17.md)和[机读限定验收](R091_FINAL_ACCEPTANCE_STATUS.json)、[原始来源实跑程序](r091_original_190_fourperson_disaster_group_loog_M0_M1_M2_E2.py)、[37项LOOG人工合成测试](test_r091_original_190_fourperson_disaster_group_loog_M0_M1_M2_E2.py)并连带其它63项source/隐私源测试一并归档。

**边界**：当前原始主sheet只包含论文884人中的760真人；原作者实验、模型在2026年才被我们冻结，属于回顾E2而非真正新采集E3；未知是否所有原行为完全自主（源无自动选择可靠标识），无作者session聚类抽样置信区间，没有风险引发群体合作的因果机制证明，更不能从20轮外推历史时间结构。保持R090阴性同等归档，PESEN v0.1保持FROZEN。下一阶段优先源行为定义和风险条件更一致的新二元公共投资数据，不在R091 190组上事后升级模型复杂度。
