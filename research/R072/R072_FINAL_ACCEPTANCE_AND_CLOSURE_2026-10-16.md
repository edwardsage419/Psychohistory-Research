# R072 正式限定结题：信誉评价规范、间接互惠与公共报告误差

日期：2026-10-16。依据 [统一研究六门验收 v1](../../protocols/RESEARCH_ACCEPTANCE_STANDARD_V1_2026-10-16.md)，R072 在**E1 有限数学机制和真人来源适用性审计**内正式 `CLOSED_BOUNDED`。这不是把真人间接互惠 E2 / 外部独立 E3 / 原作者演化稳定性升级为 PASS；实证原件访问失败明确记负面证据并转入开放任务。

## 1. 独立科学问题和首次运行之前的冻结范围

R072 尝试比较：相同的人际捐赠选择环境里，**怎样定义信誉好坏**（IMAGE_SCORING、SIMPLE_STANDING、STERN_JUDGING）与**行为信息怎样公开**（VERIFIED准确、FLIP_EVERY_FOURTH确定性每第四次误报、NO_OBSERVATION不更新），能否独立改变固定有条件帮助者 DISC 的后续行为以及宏观合作？来源参考 Nowak & Sigmund (1998) DOI `10.1038/31225`、Ohtsuki & Iwasa (2004) DOI `10.1016/j.jtbi.2004.06.005`、Kandori (1992) DOI `10.2307/2297925`；仅借研究思想，**并非完整复现原文演化ESS或4096评判规则**。

[真正首次实验前的冻结协议](../../protocols/R072_REPUTATION_PUBLIC_SIGNAL_DONATION_E1_2026-10-16.md) 已在 commit `ee2b2145caa73b1273e1c07b96761b4f0e9fe2f4` 提交。四个抽象角色按 ALLC/ALLD/DISC 三选一（`3^4=81`），四个位的初始二元声誉 `2^4=16`，三个评判规则×三个公开报告通道，**11,664 个**完整组合；固定双轮全部12个有向人际配对，**279,936 次**合成选择。每次成功帮助真实捐赠人付1、对象收2，群体总净收益每帮助一次加1；报告翻转只更改随后的公共标签，不能改变已经发生的经济行动。

## 2. 真正执行、统计和反例

[GitHub Actions run 38920131192](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38920131192) `success`：**30项**合成源/时序/评判/受赠者先验/账务恒等式测试全部 PASS，同时真正跑完11,664个初始状态与279,936次模型决策。后续[永久归档 GitHub Actions run 38920307122](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38920307122) 再运行30项测试及全部数值，与初次真实输出 SHA256 `6137894586488cabcc684ae350e692ccd0c6c2a731d6e0787153197de3a8868a` 完全一致，永久提交**45,784字节**的 [R072_E1_FULL_11664_PUBLIC_REPUTATION_RESULTS.json](R072_E1_FULL_11664_PUBLIC_REPUTATION_RESULTS.json)，不只存在短期 CI 工件。完整源码 [r072_reputation_public_signals.py](r072_reputation_public_signals.py)、[30项测试](test_r072_reputation_public_signals.py)、[原始数值/解释/负结果审计](R072_E1_REPUTATION_SIGNAL_FULL_ENUMERATION_AUDIT.md)。

每项 rule×signal 单元包含相同的 **1,296 个**策略/声誉初态，因此没有不同人群结构的混杂，但是这些状态都是人为**等权排列**，**不是**代表现实人口分布。实际平均帮助率：

| 评判 | 准确公开 | 每第四次误报 | 不更新公开声誉 |
|---|---:|---:|---:|
| IMAGE_SCORING | 0.500000 | 0.500000 | 0.500000 |
| SIMPLE_STANDING | **0.568416** | **0.570473** | 0.500000 |
| STERN_JUDGING | 0.541667 | 0.527778 | 0.500000 |

**主反例：只看宏观均值会遗漏大量微观变化。** IMAGE 规则准确与错误信号下，群体总体帮助率均为0.5，然而在相同的1,296个初态里有 **912 个**的24次真帮助次数不同；固定准确公开、只将 IMAGE 换成 STANDING，有 **624** 个初态的帮助次数不同。NO_OBSERVATION 下所有规范规则的初始信誉不可更新，三种评判在人际帮助上的所有一对一差异归零（0/1,296）。这证明我们固定玩具模型里的**评判机制**与**观测制度**可分别引起不同微观行动；不证明任何一个机制在真实社会必定如此。

IMAGE在本设计下对三种制度的帮助均值都是0.5是对称枚举的产物，不能据此推断误报无害。错误信号对STANDING平均帮助率在这一固定时间排程下略有升高，也不构成“传播错误有利于制度”的一般命题。程序保存了反证性的虚构代理角色与声誉初态以便审计。模型也有两个重大实证缺口：固定24次访问同一个有向配对两遍，故**不是严格没有重复互动的间接互惠网络**；ALLC/ALLD/DISC没有学习、变异和淘汰。因此不能说它发现了新信誉规范进化稳定性或宏观历史规律。

## 3. 真实真人来源门独立失败，证据不得并级

[PLOS ONE (2016), *Indirect Reciprocity; A Field Experiment*, DOI 10.1371/journal.pone.0152076](https://doi.org/10.1371/journal.pone.0152076) 在出版社页面公开列出 S8 Raw Data XLSX DOI `10.1371/journal.pone.0152076.s008`，作者报告在线社区现场实验所发出189次服务请求（作者数字，**不是本研究独立重算**）。R072 **没有**从这份资料读出任何人的回应、公开信誉或独立行动机会。在第一次文件字节访问前提交[来源校验协议](../../protocols/R072_E2_PLOS_FIELD_SUPPLEMENT_SOURCE_IDENTITY_2026-10-16.md)，只要求出版社可信域名、ZIP/OOXML来源结构和 SHA256，不下载后再发行任何人类原始数据。

[实际 GitHub Actions run 38921163855](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38921163855)：来源安全 **13项**测试全部 PASS，但真实 XLSX 原件下载没有满足预注册的官方可追溯源 URL/redirect，真实来源 job FAIL、整体 workflow FAILURE。没有取得字节数、SHA256 或工作簿 schema，**`SOURCE_UNRESOLVED`**；见[独立研究候选与伦理适用性](R072_E2_HUMAN_REPUTATION_EVIDENCE_SCOPE.md)及[匿名机读失败收据](R072_E2_PLOS_FIELD_S8_SOURCE_ATTEMPT_RESULTS.json)。另 Milinski et al. (2002), DOI `10.1038/415424a` 的人类间接互惠论文报告跨公共物品与信誉任务的关联，但实验目的/可观察性与R072这套捐赠日程不同，未取得本研究可复现的逐动作数据。

所以科研结论为：**R072 E1固定数学体系通过，E2真实来源原件门失败且模型测量不能配对，E3开放**。S8附录链接存在并不等于出版者指定路径在本次 CI 环境可读，更不等于四人模型可以自然而然映射在线社区参与者。

## 4. 统一六门有界交付验收

| 门 | 验收 | 严格边界 |
|---|---|---|
| A01 问题范围 | PASS | 初次E1计算之前固定全部11,664情形和36组初态格局；真人 E2 另立下载协议，失败后没有改源以取得伪 PASS |
| A02 来源与测量 | PASS（限归档和 E1 对照） | 三篇原论文学术 DOI 核对；PLOS S8官方原件未恢复，真实来源 `SOURCE_UNRESOLVED` 仍未通过真人数据门 |
| A03 计算、重放 | PASS | 30项E1测试+全部279,936合成交易真实执行；45,784字节SHA固定永久结果；另13项来源隐私测试通过，真实下载单独失败 |
| A04 反例与失败 | PASS | 912个宏观均值抵消的微观异例，完整配对阴性对照；PLOS原件失败明确归档，无样本数/字段伪复核 |
| A05 推断边界 | PASS | 没有真人E2拟合、没有独立E3、没有ESS/长期文化模型，没有可靠的制度“误报改善合作”政策结论 |
| A06 正式移交 | PASS | 完整程序/测试/原始归档、中文数学审计、真实来源失败、机读状态和[所有开放门](R072_POST_CLOSURE_OPEN_GATES.md) |

本项目统一标准的六门 PASS 只证明**在先定义的数学研究成果和真实数据来源失败均已如实、可复核入档**，而不是 R072 的广义科学机理完成真人验证。若由 E1 输出与 E2 失败形成完整有界结题范围，则应标 `RETROSPECTIVE_SCOPE_DECISION`，不能事后声称启程时已决定在何时关闭 R072。

## 5. 状态与后续

`R072=CLOSED_BOUNDED`；
`R072_E1_FULL_REPUTATION_SIMULATION=PASS`；
`R072_E1_ARTIFACT_SHA=PASS`；
`R072_E2_PLOS_S8_REAL_BYTES=SOURCE_UNRESOLVED`；
`R072_HUMAN_REPUTATION_NORM_CAUSALITY=NOT_ESTABLISHED`；
`R072_E3_EXTERNAL=OPEN`；
`PESEN_v0.1=FROZEN`。

后续的优先事项不应只继续增加合成玩具模型：应**先获得一个合法可重放、行动机会与信誉测量语义明确的真人数据源**，如果仍无法获得，则对 E1 前期长串研究明确保持“未被实证检验”的状态；涉及多群体制度或文化演化的原创主模型若另立 R073 应独立冻结问题、反例和真正的跨尺度验证门。
