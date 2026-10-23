# 心理史学原始239模型：R295 习惯形成 E1验收、v0.9来源目录与下一R主线

日期：2026-10-23 Asia/Taipei。严格保持：先逐项完成R系列学习/验证，之后统一归纳分类，最后才开展模型熔炼。当前原始239项整体科学结题**未成立**。

## 完成的R295原始模型条目

原目录ID **01-019 Habit Formation**，P1。研究的原作者锚点是Dickinson 1985年 *Actions and habits: the development of behavioural autonomy*（奖励重估与目标控制），Wood & Neal 2007年 *A New Look at Habits and the Habit–Goal Interface* DOI https://doi.org/10.1037/0033-295X.114.4.843（情境–反应联结和目标交互），Lally et al. 2010 *How are habits formed* DOI https://doi.org/10.1002/ejsp.674（日常自动性学习）。本项目使用新定义人工数值方程，不冒充原作者真人数据、动物实验或拟合公式。

[预先冻结协议](../protocols/R295_HABIT_CUE_DEVALUATION_180_ORIGINAL_STATES_PRESCORE_FREEZE_2026-10-23.md) [commit638948a4](https://github.com/edwardsage419/Psychohistory-Research/commit/638948a4fb2fdcc370dbbc2c2f9f634f4d61a57b)先于模型。三个人工学习率α、三个目标–习惯混合份额λ、两种情境、两种当期结果价值V和五个训练节点，完整36组训练世界、**180条人工原始来源状态**。每个训练率强度 H_n=1−(1−α)^n，人工选择A得分=(1−λ)*V+λ*cue*H_n，备选B分值1/2，严格平局选B。

对应**90组精确奖励贬值配对**：完全目标控制λ0为30/30个模型配置发生A→B转换；混合λ1/2为8/30；完全习惯控制λ1为0/30。关键可审计例子：α1/2训练4次H=15/16；同情境纯习惯执行的A对V1/V0均不改变，切换情境后行动变B；混合机制在V1 A得分31/32，在V0 A得分15/32，则贬值后会改变。这是给定人工结构的代数结果，**不能推断真实被试是否有习惯自动性、脑机制或干预效应**。

[完整科学报告](../research/R295/R295_SCIENTIFIC_REPORT_2026-10-23.md)、[完整180来源CSV](../research/R295/R295_ALL_180_ORIGINAL_HABIT_CUE_REVALUATION_STATES.csv)、[全部90匹配结果JSON](../research/R295/R295_EXACT_HABIT_CUE_AND_DEVALUATION_RESULTS.json)、[SHA256凭证](../research/R295/R295_MACHINE_RECEIPT.json)、[独立来源审计程序](../research/catalogue_audit/independent_r295_source_audit.py)、[正式机器验收](../research/R295/R295_FINAL_ACCEPTANCE_STATUS.json)全部在GitHub main。

**科学CI [39920355215](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39920355215)**三项作业completed/success。Python3.11/3.12分别731项主单测与14项独立来源测试，第三作业独立重建180 source及90配对后永久归档[commit324eced6](https://github.com/edwardsage419/Psychohistory-Research/commit/324eced68a19401078b1c60d72c83ae77549b30b)。没有真实人E2，历史E3=0，已接受的科学范围为**CLOSED_BOUNDED_E1_ARTIFICIAL_R295_HABIT_CUE_OUTCOME_DEVALUATION**。

## 239来源交叉索引 v0.9 的严格变更

| 原239逐项映射状态 | v0.8（R294后） | v0.9（R295后） |
|---|---:|---:|
| 已确认主R关联（不同证据等级） | 182 | **183** |
| 共享之前有限数学机制链接 | 3 | **3** |
| 只有之前有限研究范围链接 | 5 | **5** |
| 已核材料未建立逐项链接 | 49 | **48** |
| 待确认主R的原候选数 | 54 | **53** |
| 原始候选总数 | 239 | **239** |

[v0.9完整原239行目录索引](ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v0.9_2026-10-23.json)相对于[v0.8](ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v0.8_2026-10-23.json) **仅01-019一行**改动，附有R295 README Git blob SHA1、研究报告、正式E1验收和真实CI run。原始候选目录及其优先级保持不变，[当前待核53项队列](ORIGINAL_239_PENDING_53_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv)为P1=26，P2=27；较上版恰好删去01-019。

**目录专项CI [39920555825](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39920555825)**三job completed/success，双Python版本各14项真实目录检查，第三次独立重算来源字节和239个原模型归档指向。183条主R关联是**来源追踪覆盖**，不能等价成183个原论文或独立真人实验已经复现。

## 下一原始目录编号

优先队列下一项为 **02-001 Rescorla–Wagner Learning Rule**。作者Rescorla & Wagner (1972), *A theory of Pavlovian conditioning: Variations in the effectiveness of reinforcement and nonreinforcement*, 收录于*Classical Conditioning II* 64–99，作者Wagner在[耶鲁大学的发表记录](https://wagner.yale.edu/publications)。R296应独立研究共享预测误差、阻断（blocking）和复合线索学习，并与既有R系列强化学习研究作“共享数学、不同原目录条目”的来源区分。所有真实动物实验和原创论文参数实证复现需另立E2关口。R073、PESEN v0.1仍然冻结。
