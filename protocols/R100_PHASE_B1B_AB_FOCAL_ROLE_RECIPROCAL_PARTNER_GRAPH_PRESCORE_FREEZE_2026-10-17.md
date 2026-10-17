# R100 Phase B1b：双人阈值游戏原始人物与真实伙伴互指映射的事前冻结

日期：2026-10-17。状态：B1B_BEFORE_PAIR_RECONSTRUCTION_FROZEN。前置证据：[A原字节E1收据](../research/R100/R100_PHASE_A_LIVE_CI_SOURCE_RECEIPT.json)、[B0 XML结构](../research/R100/R100_PHASE_B0_LIVE_CI_SOURCE_AB_TAG_RECEIPT.json)、[B1a真实AB编码诊断](../research/R100/R100_PHASE_B1A_LIVE_CI_AB_SOURCE_FORMAT_RECEIPT.json)均已归档。**严格在解释真实A/B人物配对之前冻结本协议**；不得读取C:Z任意实际贡献或问卷。PESEN v0.1仍冻结。

## 来源B1a已观察到的有限格式事实

10张匿名源表各有一个header和55/55、59/59、56/56、52/52、55/55个四行焦点块，合计554块。A每块只一个非空数值，B每块四个非空字符串引用。B每块通常三个不同值，**全来源12块仅两个不同B值**。这些是B1a未解释源本人/伙伴语义的事实，不能擅自删去12块或据此宣称12个违规真人。

## 预冻结具体身份解释假说与可反驳条件

1. 只承认出版方原本10 sheet元数据的名称 `<treatment>_Type 1`、`<treatment>_Type 2`，并通过来源 `workbook.xml` 与 `workbook.xml.rels` 映射真正sheet，不允许以字母排序或单纯 `sheet1,2` 猜测角色。五个原处理每处理一对sheet，规范编码仅于内存匿名 `(treatment, source_A)`。 A仅在四行块首行非空；若不满足则失败。
2. 对每个焦点块，原作者说明Type1人物在Session1担任Player1、Session2担任Player2，因此四行B值位置从0计应满足 `B[0]==B[3]`；Type2在Session1担任Player2、Session2担任Player1，预言 `B[1]==B[2]`。这一跨两阶段重复B码作为候选本人代码 `self_code`；其余两个B码分别为phase1、phase2对手代码。**这些是即将被原数据验证的可反驳模型，不允许据结果反向调换类型。**
3. 对每处理两sheet所有焦点块生成(A->self_code)双射：实际源A不得重复、self_code不得多人共用、两个角色sheet参与者不得交叠。阶段1/2候选对手B字符串必须唯一找到对方focus self_code；互为对手的两人在同一阶段必须互指，且实际角色相反。
4. 两阶段若同一人原对手相同，记录 `same_opponent_across_stages` 违规，而不是认为两个phase是独立招募；在有此违规时严格B1b资格拒绝，原作者所述“不同伙伴”存在可复核反例。一个完整双人pair-session应由两个对称焦点记录计一次，无向pair key包含真实处理+阶段+两人代码。
5. 每处理真实人数应等于原作者预先报告 110、118、112、104、110；每阶段原无向真实pair应分别为55、59、56、52、55，两个phase合计理论554个paired-session，两个20轮游戏如未来真实贡献完整才构成11,080不重复pair-round目标、22,160非重复actor-round。**这些目标仍不是B1b已读行为，不能因数量吻合就称为实际20轮行动。**
6. 不假定“同一实验session”是不同招募人的真实lab session；仅表示同一批人的两个阶段。采用处理内跨两阶段配对无向图的连通分量（connected component）作为未来PERSON_DISJOINT合法留出最低单位。报告各处理组件数量和最大/最小规模而不公开任何原ID。若某处理全图一分量，禁止该处理内部人的相互独立留出。
7. 遇无法解析sheet名称/关系、本人重复位置不符、B码不可互证、原ID别名、同对手再匹配、人数不符或任意不支持源码，**保留原始所有记录并固定 `B1B_BLOCKED_BOUNDED`**；匿名分项计数并行归档。不得试探C:V行为值修补配对。

## 审核级别

* B1b成功只证明原始A/B能够构造跨阶段配对与人图，提供后续模型留出的身份基础。
* B1b阻断仅证明当前预注册编码假说或原源未满足严格资格，不能解释为人类行为模型的负面预测。
* 两种结果均为来源E1范围内，真人20轮贡献真实来源读入=0、R073严格原模型跨实验复制=未成立、PESEN v0.1=FROZEN。

执行前须先运行模拟四行焦点、匹配双向、伙伴未换、B码不符、A重复、跨阶段图component泄漏等合成反例；真实结果只输出白名单匿名计数和完整官方SHA。每次GitHub Actions将机器结果和失败原因自动提交，科学报告需再次独立核验。
