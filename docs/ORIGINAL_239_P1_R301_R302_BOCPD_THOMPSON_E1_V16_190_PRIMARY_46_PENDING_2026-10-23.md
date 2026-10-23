# 心理史学原239模型进度审计：R301贝叶斯变点与R302多臂老虎机独立人工E1、v1.6来源索引

日期：2026-10-23 Asia/Taipei。继续此前既定主线：完成全部R系列的学习、机制审计和有界验收；在全部完成后才统一归纳分类，最后进行原创模型熔炼。个人辅助决策系统继续暂缓。**本轮是精确人工机制E1，不是新增真人、动物实验E2或历史预报E3；原239全体模型正式科学结题未成立。**

## 1. 两项有界研究的实际成果、不可偷换科学证据

| 正式研究和原始239目录 | 事前冻结提交 | 完整原始人工source | 实际双Python主模型unittest | 科学三job CI |
|---|---|---:|---:|---|
| R301 Bayesian Change Point Detection（02-012 P1） | [1e0209ff](https://github.com/edwardsage419/Psychohistory-Research/commit/1e0209ffa2c8597d3d3f2a7ccef40eea0be4485e) | 192前缀记录 | **588×2** | [run39930227033](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39930227033) SUCCESS |
| R302 Multi Armed Bandits（02-016 P1） | [b3c92f9f](https://github.com/edwardsage419/Psychohistory-Research/commit/b3c92f9f013e795a0db4622dc48613f82eb38bca) | 162两臂计数源行 | **660×2** | [run39930778614](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39930778614) SUCCESS |

两个研究合计**354条人工原source**（不能当成354名受试者），Python3.11+3.12合计**2496次主模型unittest通过**，此外两项各执行16和17项独立来源/恶意篡改测试，双Python及第三job均核验来源JSON/CSV SHA256。R301源文件与结果永久归档[commitfc948ef4](https://github.com/edwardsage419/Psychohistory-Research/commit/fc948ef418947e4c6adc958b619796cc9e30b9de)；R302永久归档[commit25b895e3](https://github.com/edwardsage419/Psychohistory-Research/commit/25b895e30416f109d38e6bd083163ff08d0d5dd0)。

### R301：固定风险下的在线贝叶斯分段，不等于真实变点认定

原作者Adams & MacKay (2007), *Bayesian Online Changepoint Detection*, [一作原论文](https://lips.cs.princeton.edu/pdfs/adams2007changepoint.pdf)、arXiv:0710.3742。人工Beta(1,1)–Bernoulli模型，风险先验h∈{0,1/4,1/2}，16个完整四位字符串×4前缀×3风险=192条完整来源。全部每时点的连续段长度后验由BOCPD在线递推和**另一程序穷举2^(t−1)种独立完整分段**交叉精确验证；相同短前缀在多个完整字符串重复，归一化前去重。

典型预冻结概率：h1/4时`0000`最新变点后验135/757，`0001`后验135/323，下一观测1预测分别1717/6056与1301/2584；固定h1/2时`0001`变点后验15/23。风险h0时任何序列最新变点后验都0，但单段成功率的预测会更新，`0000`下一观测1预测1/6、`0001`为1/3。人工结果**不是对真实环境变点的确认、真实虚警率或历史事件概率**。准确阅读L_t=1为**当期观测前最近一次边界**发生变点的模型后验，而不是过去任何时刻曾出现变点的概率。

[完整研究科学报告](../research/R301/R301_SCIENTIFIC_REPORT_2026-10-23.md) · [192原source](../research/R301/R301_ALL_192_ORIGINAL_BAYESIAN_CHANGEPOINT_PREFIX_SOURCES.csv) · [独立穷举](../research/catalogue_audit/independent_r301_source_audit.py) · [正式机器验收](../research/R301/R301_FINAL_ACCEPTANCE_STATUS.json)。

### R302：Beta后验Thompson选择概率，不等于真实bandit收益

William R. Thompson (1933), *On the likelihood that one unknown probability exceeds another*, *Biometrika*, https://doi.org/10.1093/biomet/25.3-4.285。另参考Auer、Cesa-Bianchi、Fischer(2002), *Finite-time Analysis of the Multiarmed Bandit Problem*, https://doi.org/10.1023/A:1013689704352，但**未运行UCB1、未复现有限时间遗憾界**。

两个Bernoulli臂各自独立Beta(1,1)先验；每臂成功/失败次数都取0、1、2形成81个完整人工证据状态，每状态2条原source共162行。比较后验均值确定性贪婪行为（均值平局选A），与独立Beta后验参数抽样选择概率P(theta_A>theta_B)。完整概率使用Beta CDF二项式展开和**独立另一套带符号交错积分**逐条严格分数对照。

预冻结典型值：A和B都无证据时下一次Thompson选A概率1/2；A已有1次成功，B没有历史证据时选A概率2/3；A有2成功、B有2失败时选A概率19/20，选择B仍为1/20。均值同为1/2的Beta(3,3)与Beta(1,1)的方差分别1/28和1/12，表明后验均值相同并不等于不确定性相同。这仅是**给定人工观察计数后的抽样行动概率**，没有真实生成奖励率、实际连续行动或累计遗憾值。

[完整研究科学报告](../research/R302/R302_SCIENTIFIC_REPORT_2026-10-23.md) · [162人工arm source](../research/R302/R302_ALL_162_ORIGINAL_BETA_BANDIT_ARM_SOURCES.csv) · [独立Beta积分](../research/catalogue_audit/independent_r302_source_audit.py) · [正式机器验收](../research/R302/R302_FINAL_ACCEPTANCE_STATUS.json)。

## 2. 原始239目录科学来源索引 v1.4→v1.5→v1.6

| 来源层次 | v1.4 R300后 | v1.5 R301后 | **v1.6 R302后** |
|---|---:|---:|---:|
| 已建立候选主R研究来源 | 188 | 189 | **190** |
| 共享早期数学研究，但不是独立主R | 3 | 3 | **3** |
| 仅有旧有限研究范围关联 | 4 | 4 | **4** |
| 已查资料无逐项来源链接 | 44 | 43 | **42** |
| 尚待核实候选主R来源 | 48 | 47 | **46** |
| 原始唯一候选总数 | 239 | 239 | **239** |

[最新全239原候选v1.6来源交叉索引](ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v1.6_2026-10-23.json)相对于[v1.5](ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v1.5_2026-10-23.json)只改变**02-016一条R302主研究关联**，v1.5相对于v1.4只变动02-012一条R301主R关联。所有239个原模型ID、姓名、次序和P1/P2不变；此前R063社会学习旧有限证据、R073冻结结果、R299TD学习、R300HMM研究均未重分类或偷换研究归属。**190条主R证据来源指向，不等于190项独立真人模型验证或预测性能证实。**

[当前46项待核原候选清单](ORIGINAL_239_PENDING_46_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv)：P1 **19**、P2 **27**。未建立连接的条目尚待实读档案，不等于理论错误或从未研究。下一个P1原始候选为**03-001 Social Learning Theory**。应优先复核此前R061–R064、R063 Najar 2020 和相近模型的真实作者来源及原目录意义，再决定哪种机制仍欠独立数学和实证检验，避免重复开展同一社交强化学习。

四个GitHub CI工作流总计12个独立job SUCCESS：
* [R301本体CI39930227033](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39930227033)、[R301 v1.5目录CI39930492102](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39930492102)；
* [R302本体CI39930778614](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39930778614)、[R302 v1.6目录CI39931024459](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39931024459)。

目录各有Python3.11/3.12实际15条科学元数据与Git SHA/来源SHA tests，第三job独立重算本体全部源并核对唯一变化原候选行。归档完整性与真正科研实证效度严格分级。

## 3. 不得超出本轮的科学结论

R301和R302均只达有界精确人工E1；没有新真人/动物E2，历史E3零，不证明原作者模型在人类群体、长期社会演变或历史事件上的外推预测力。全部239候选研究主线仍未结束，不开展整体分类和新模型熔炼。R073与PESEN v0.1继续冻结。
