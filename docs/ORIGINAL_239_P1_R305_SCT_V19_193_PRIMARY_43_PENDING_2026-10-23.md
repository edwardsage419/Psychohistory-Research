# 心理史学：R305自我分类理论有界E1与原239证据索引v1.9验收

日期：2026-10-23 Asia/Taipei。既定主线：完成所有R模型学习研究→统一分类→最后熔炼。**本文件报告的是一项人工数学机制研究和证据索引覆盖，不等于原始239项全面科研验收。**

## R305 原候选 03-004 Self Categorization Theory：原文与自建公式分离

一手理论：Turner (1985), *Social categorization and the self-concept: A social cognitive theory of group behaviour*, *Advances in Group Processes* 2:77–122， [原章参考索引](https://inclusionandbelongingtaskforce.harvard.edu/publications/social-categorization-and-self-concept-social-cognitive-theory-group-behavior)；Turner、Hogg、Oakes、Reicher、Wetherell (1987), *Rediscovering the Social Group: A Self-Categorization Theory*；Turner等人(1994), *Self and Collective: Cognition and Social Context*, https://doi.org/10.1177/0146167294205002。原理论强调个人/社会身份类别的情境依赖、比较适配、规范适配和认知可及性。**本研究没有原作者的人类自我分类试验表，不拟合实测参数，也不是Turner原作者提出的量化得分公式。**

相关的[**R304 Social Identity Theory**](../research/R304/R304_SCIENTIFIC_REPORT_2026-10-23.md)以自造效用研究已假定内群体成员身份的分配偏好；R305研究相同四个虚拟对象面对不同特征背景时**哪一个类别被选择**，两个模型研究对象不同，没有重复确认的真人数据。R063 Najar社交学习源与R073真人重复博弈冻结实验也不作为新增E2使用。

[原协议](../protocols/R305_SELF_CATEGORIZATION_METACONTRAST_486_SOURCES_PRESCORE_FREEZE_2026-10-23.md)先行冻结 commit [a4dfc1f5](https://github.com/edwardsage419/Psychohistory-Research/commit/a4dfc1f582c9a58eec6cf45b63a34f577800e0eb)。人工对象四个，P和Q两种候选划分，特征情境X=(0,1,4,5)、Y=(0,4,1,5)、MID=(0,5/2,5/2,5)；以跨类别四个距离平均/类别内两个距离平均构造自定义MC比较适配指标。另将认知可及性、P/Q规范适配性及PERSONAL竞争阈值各取3档，构造**3^5=243人工世界×2候选类别=486完整人工原source**。本项目人为定义群体得分为可及性×规范适配×MC，只有严格高于另一类别及个人阈值才选择对应群体，否则退回个人层级。该机制未估计心理潜变量。

| 情境 | 计算MC_P | 计算MC_Q | r=nP=nQ=1,个人阈值1时选择 |
|---|---:|---:|---|
| X | **4** | 5/8 | **P** |
| MID | 1 | 1 | **PERSONAL** |
| Y | 5/8 | **4** | **Q** |

负对照：X中即便P的MC更大，将P规范适配设0、Q规范适配设1且个人阈值0时，模型选择Q；认知可及性0或两者规范适配0则全部返回PERSONAL。**选择变化来自人为冻结的特征、权重和保守并列规则，不说明真实人的身份改变或社会因果作用。**

主程序[1473项实际单测](../research/R305/r305_exact_self_categorization_metacontrast.py)、[486来源完整CSV](../research/R305/R305_ALL_486_ORIGINAL_SELF_CATEGORIZATION_SOURCE_CELLS.csv)、[243人工世界完整计算结果](../research/R305/R305_EXACT_SCT_COMPARATIVE_FIT_RESULTS.json)、[SHA256机器凭证](../research/R305/R305_MACHINE_RECEIPT.json)、[独立六对对象距离重算及18项恶意篡改测试](../research/catalogue_audit/independent_r305_source_audit.py)、[正式有限范围机器验收](../research/R305/R305_FINAL_ACCEPTANCE_STATUS.json)均归档。GitHub Actions [本体run39937267071](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39937267071) 3/3 SUCCESS，Python3.11/3.12各1473主unittest和18独立审计，第三job永久提交全部源CSV/结果JSON/SHA至 [commit c57d76c1](https://github.com/edwardsage419/Psychohistory-Research/commit/c57d76c1d8e42b95e83eff0ffe72f23a9803da7c)。

## 原239目录科学来源索引v1.8→v1.9

| 层级 | v1.8 R304后 | v1.9 R305后 |
|---|---:|---:|
| 已有候选主R研究来源链接 | 192 | **193** |
| 共享早期有限数学、非独立主R | 3 | 3 |
| 只有较早范围局限审计链接 | 4 | 4 |
| 核查资料未建立逐项链接 | 40 | **39** |
| 仍待核候选主R研究来源 | 44 | **43** |
| 原始目录唯一候选 | 239 | 239 |

[所有239行来源交叉索引v1.9](ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v1.9_2026-10-23.json)相对[v1.8](ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v1.8_2026-10-23.json)**仅03-004一行变动**，原239模型ID/名称/优先级不变，R304 03-003和R303 03-001原来源关联不变；所有跨类别旧证据未重用为新真人E2。**193条主研究来源关联只表示可追溯性，不是193项人类心理模型验证。**

[最新待核43项队列](ORIGINAL_239_PENDING_43_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv)，P1 **16**、P2 **27**，下一项**03-010 Social Sanction and Reputation Mechanisms**。它有既有完整R072间接互惠信誉机制E1和原始真人数据文件恢复及编码门未闭合记录，必须优先实读R072成果及最近REV008阻塞状态，切勿再次开办同一人为信誉模型，或用匿名组已知结果反推真人处理组编码。

[独立全239跨版本机器索引核验源码](../research/catalogue_audit/verify_p1_r305_crosswalk_v1_9.py)、[CI run39937550180](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39937550180) **3/3 SUCCESS**，Python3.11与3.12各16项元数据与source SHA验证，第三作业重算所有486原source并证明仅03-004变更。两次CI合计6job全成功。

**科学判定：R305有界E1完成。** 无真人/动物E2、无历史E3；不修改R073/PESEN v0.1，不开始整体分类或原创熔炼。
