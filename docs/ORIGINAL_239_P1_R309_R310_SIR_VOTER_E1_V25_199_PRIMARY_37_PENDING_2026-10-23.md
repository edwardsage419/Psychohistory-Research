# 心理史学：R309 SIR 与 R310 网络投票模型 E1、原始239来源索引v2.5

2026-10-23 Asia/Taipei，用户批准的主线「完成全部原始R系列模型学习研究→统一分类→最后熔炼」，个人决策系统暂缓。**这是两个可复现的有限人工数学机制，不是两组新的真人实验、疾病防治成果或政治历史预测。** 原239全体科学结题未成立。

## 原著问题与实作边界

**R309** 研究原始候选 **04-006 SIR Epidemic Model**，参照Kermack & McKendrick(1927), *A contribution to the mathematical theory of epidemics*, DOI https://doi.org/10.1098/rspa.1927.0118。原文为连续的疾病易感—感染—恢复动力学；R309是本项目新设五个虚拟人**同步离散接触和恢复**过程，并不重现原1927连续微分系统或真实感染率。21个完整S/I/R初始数目×9个接触/恢复参数共**189人工世界**。所有可能新增感染数与原感染者恢复数组合有**1,134条完整原始人工source**，包括零概率事件；独立审计则枚举**11,664个完全人工二元接触/恢复配置**，逐行重算概率与SHA。对于S3 I2、每接触p=1/2、老感染者恢复q=1/2，感染每位易感者的条件概率为3/4，下一步预期人数(3/4,13/4,1)，而没有新感染且两名感染者全部恢复的条件概率精确为1/256。若p=q=1，下一步为(0,3,2)，新感染者不会同一时步立刻恢复。没有真实病人、连续轨迹、R0估计、观念文化传播实测或干预成本收益验证。

**R310** 研究原候选**04-008 Voter Model**，理论根源Clifford & Sudbury(1973), *A model for spatial conflict*, DOI https://doi.org/10.1093/biomet/60.3.581，以及Holley & Liggett(1975) DOI https://doi.org/10.1214/aop/1176996306。四个抽象节点、三种路径/环形/完全无向拓扑、16种完整二元初态，形成**48个人工世界、416条完整原始异步有向邻居复制source**。每次随机选目标节点1/4，再从目标的直接邻居等概率复制，其他节点保留原值。三个图上的**度加权1意见比例**下一步条件期望均保持不变；两个规则图的普通比例也守恒；但PATH4从初态(1,0,0,0)出发，普通1比例从1/4变为下一步期望**7/32**，而度加权比例保持**1/6**。模型刻意不是实际政治选举、真人社会网络观测、共识时间预测或SIR传染过程。

## 预先冻结、独立来源与真实CI

| E1研究 | 先验冻结协议提交 | 人工世界 | 新增原始source | 双Python版本主unit tests | 真正成功CI |
|---|---|---:|---:|---:|---|
| R309 SIR五节点精确离散转移 | [aec096d7](https://github.com/edwardsage419/Psychohistory-Research/commit/aec096d72f66c44ac1b13dd5ed1ce9d169f21aac) | 189 | **1,134** | **3,417×2** | [run39955168677](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39955168677) 3/3 |
| R310 投票随机异步邻居复制 | [782990a1](https://github.com/edwardsage419/Psychohistory-Research/commit/782990a1cae101a3c0fd5ba37f89dc8ed9c2078c) | 48 | **416** | **1,262×2** | [run39955796344](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39955796344) 3/3 |

新人工source合计**1,550条**，双Python主数学测试合计**9,358项实际unittest通过**；两项还有各17项无导入独立source攻击测试、第三工作重新逐事件重算审计。R309来源和SHA永久归档[commit54997770](https://github.com/edwardsage419/Psychohistory-Research/commit/549977708267ac455d0ac61ec3fee0d0330b43ce)，R310来源和SHA永久归档[commit2dc71bae](https://github.com/edwardsage419/Psychohistory-Research/commit/2dc71bae2a70dd3affc892e33712d0541822525b)。全部人工来源记录，不得当作人体实验次数。

**第一轮R310 CI失败的可追溯性**：run [39955723523](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39955723523)独立审计器将相同CYCLE4无向边集合按字典序序列化，而冻结模型源码按设定顺序列出四条边，因此在“边集合字符串”处比对失败；主生产数学模型测试本身通过。修复[commit17a14103](https://github.com/edwardsage419/Psychohistory-Research/commit/17a14103c9f01f1b774883de77df831f759c7792)只固定独立审计的来源边顺序表示，未更改事前数学规则/数据公式，然后重新运行run39955796344三job成功。首次失败不会被改写为成功。

相关原始结果：[R309科学报告](../research/R309/R309_SCIENTIFIC_REPORT_2026-10-23.md)、[R309完整原始CSV](../research/R309/R309_ALL_1134_ORIGINAL_SIR_TRANSITION_SOURCES.csv)、[R309机读验收](../research/R309/R309_FINAL_ACCEPTANCE_STATUS.json)；[R310科学报告](../research/R310/R310_SCIENTIFIC_REPORT_2026-10-23.md)、[R310完整原始CSV](../research/R310/R310_ALL_416_ORIGINAL_VOTER_DIRECTED_UPDATE_SOURCES.csv)、[R310机读验收](../research/R310/R310_FINAL_ACCEPTANCE_STATUS.json)。原数据及结果SHA256分别保存在两个研究包中。

## 原始239条候选目录的独立更新

| 主R证据范围状态 | v2.3 R308后 | v2.4 R309后 | 最新v2.5 R310后 |
|---|---:|---:|---:|
| 主R来源关联 | 197 | 198 | **199** |
| 共享有限数学（非独立主R） | 3 | 3 | 3 |
| 仅早期有限范围证据关联 | 3 | 3 | 3 |
| 核验资料仍无逐项来源链接 | 36 | 35 | **34** |
| 仍待核候选主R来源 | 39 | 38 | **37** |
| 原始唯一候选总数 | 239 | 239 | **239** |

[原始239候选科学来源交叉索引v2.5](ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v2.5_2026-10-23.json)相对于v2.4**仅04-008一条来源/验收更新**；v2.4相对v2.3仅04-006一条更新。原始239模型ID、名称和优先级不改；R072 REV008原真人社会声誉处理编码仍缺独立来源，R307/R308保持E1研究，R073/PESEN v0.1仍冻结。**199条主R关联不等于199个原理论有真人独立验证**。

[当前待核37原模型清单](ORIGINAL_239_PENDING_37_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv)：P1 **10**、P2 **27**。下一项**04-010 Friedkin Johnsen Model**已有更重要的早期R066证据：16村庄、1,872条完整基线/期末态度配对调查，与R066原三模型整村留出经验预测数据，不能再开一个人造DeGroot/FJ玩具冒充研究发现。应优先独立实读R066、保留预测限定和初始失败来源，复用既有一手成果做逐项研究归属，必要时同样分开审查04-012 Hegselmann Krause Model。原R066的村庄留出不等于外部人群复验，更不等于对“模型引发社会变化”的因果识别。

四条完整三作业的独立成功工作流合计**12个真实job SUCCESS**：[R309研究39955168677](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39955168677)、[R309原239目录v2.4 39955485250](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39955485250)、[R310研究修复后39955796344](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39955796344)、[R310原239目录v2.5 39956069738](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39956069738)。每条目录均完成双Python跨版本原239规范ID和唯一变更的16条unittest及独立第三来源重算。

科学结论：两项新E1有界研究关闭，**没有任何本轮新的真人/动物E2或历史E3**。持久科研规范与可重复性有进展，原239科学整体结题尚未成立，仍按顺序完成全R系列，暂不开展模型统一分类或熔炼。
