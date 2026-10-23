# 心理史学：R297 Q-Learning 独立人工 E1验收与原239目录 v1.1 更新

2026-10-23 Asia/Taipei。原239项目录学研顺序保持：所有R候选依次研究、各自有限科学验收，然后才归纳分类，最后才尝试独立模型熔炼。**原239项整体科学结题仍NOT_ESTABLISHED**。

## 第一手原著及独立机制范围

原目录02-003 Q Learning（P1），Watkins, C.J.C.H. & Dayan, P. (1992), *Q-learning*, *Machine Learning* 8:279–292, https://doi.org/10.1007/BF00992698，作者原文 https://www.gatsby.ucl.ac.uk/~dayan/papers/cjch.pdf 。原始Q学习使用新状态最大动作值的离策略时序差分。1992年的渐近收敛结论有探索覆盖和学习率条件，这些**不能被本轮4次人工递推模拟视为重新证明**。

R061/R062/R063的真实研究侧重Najar et al. (2020)社会强化学习、模仿学习metaVS门控，R063对作者代码与Figure6进行机制审计。R297是Q Learning独立条目的**有限人工机制审计**，不得将既有真人社会学习E2升格给Watkins–Dayan 1992，或将R073囚徒困境独立实证证据挪用。

## 完成的实验合同与可核查结果

[预先冻结完整协议](../protocols/R297_Q_LEARNING_OFF_POLICY_COVERAGE_24_WORLDS_120_SOURCE_PRESCORE_FREEZE_2026-10-23.md)，[事前commit fd66badd](https://github.com/edwardsage419/Psychohistory-Research/commit/fd66badd5a110b36cc97564f7e1a29daba4298ba)。

两层三状态人工马尔可夫环境：起点S0安全动作奖1直接终止，探索动作奖0转S1，S1高奖动作奖3终止、低奖动作奖0终止；终止后不自举。折扣γ∈{0,1/2,1}、步长α∈{1/2,1}、S1高奖动作样本覆盖FULL/GOOD_MISSING、下一动作自举MAX/固定BAD，形成24个人工世界，逐轮0..4列出**120条全部完整Q值人工原source**。两个不同自举目标不能混为同一个策略假设；固定BAD自举仅为行为动作对照，并不宣称实现完整SARSA或对那个固定行为政策的最优性诊断。

[完整R297科学报告](../research/R297/R297_SCIENTIFIC_REPORT_2026-10-23.md)、[120源CSV](../research/R297/R297_ALL_120_ORIGINAL_Q_LEARNING_Q_VECTOR_SOURCES.csv)、[24世界结果JSON](../research/R297/R297_EXACT_Q_LEARNING_OFF_POLICY_RESULTS.json)、[来源及结果SHA256凭证](../research/R297/R297_MACHINE_RECEIPT.json)、[独立无导入源级复算](../research/catalogue_audit/independent_r297_source_audit.py)和[机读正式验收](../research/R297/R297_FINAL_ACCEPTANCE_STATUS.json)均已归档。四轮后γ=α=1/2 FULL+MAX下，Q安全=15/16、Q探索=39/32、Q下一状态GOOD=45/16，选择探索与完整环境最优一致；相同实验第2轮两动作Q=3/4严格平局，必须选择安全。24格人工配置中12与完整最优策略一致、12不一致，这只是**人为指定的参数设置数量**，不是现实人的比例；固定BAD政策本身与全自由动作最优控制的目标不同。全研究无动物E2、真人E2、历史E3。

[GitHub Actions研究CI run39924889538](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39924889538)三个job completed/success：Python3.11和3.12各运行611项主模型真实单元测试及16项独立源审计，第三独立来源作业重放全部120Q向量和24世界精确结果，并把CSV、JSON、SHA永久归档main [commit6d3b0496](https://github.com/edwardsage419/Psychohistory-Research/commit/6d3b0496111d58c03983941480398c1fd4bff85f)。

## 原目录239证据覆盖更新

| 来源状态 | v1.0 R296后 | v1.1 R297后 |
|---|---:|---:|
| 有主R研究来源指向 | 184 | **185** |
| 共享此前有界机制链接，不增加独立实验 | 3 | 3 |
| 仅此前范围有限旧文件，无逐条主R | 5 | 5 |
| 已核材料未找到逐项联系 | 47 | **46** |
| 待确认主R来源关联 | 52 | **51** |
| 原始候选条目总数 | 239 | 239 |

[239项v1.1原目录逐行完整证据索引](ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v1.1_2026-10-23.json)从v1.0只变动02-003一个候选关联，原始239条名目与P1/P2等级不变；[当前剩余51待核队列](ORIGINAL_239_PENDING_51_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv) P1=24，P2=27。**185个主研究来源链接不是185项原论文实证复现。** 相邻02-004 Model Based RL仍待独立研究，02-005 Model Free RL仍为R063社会学习的旧范围关联，不得双计为已完成独立主R。

[目录机读独立审计源码](../research/catalogue_audit/verify_p1_r297_crosswalk_v1_1.py)、[成功GitHub Actions run39925138650](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39925138650)三job全部completed/success，双Python各15项原目录元数据核验和第三独立对照120原source及SHA。此索引仅证明已查看文件和证据来源的链接完整性；学术效度必须按各R验收另审。

## 下一优先研究

**R298：原02-004 Model Based Reinforcement Learning**。应把有内在环境转移与奖励模型、知晓后重规划的机制，与R297的离策略缓存价值更新区分。重点设计无直接行动再学习时的奖励重新估值与转移结构变更，以及信息通知对规划的必要性；切勿在没有真实环境行为数据时将模拟规划敏感性视为人的目标导向行为证据。R073与PESEN v0.1继续冻结；原239全部研究完成后才分类与熔炼。
