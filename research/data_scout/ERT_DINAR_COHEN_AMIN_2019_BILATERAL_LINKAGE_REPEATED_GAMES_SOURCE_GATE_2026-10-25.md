# A 公开数据侦察：2019双边冲突议题联结重复博弈，R073 外部复验资格预审

日期：2026-10-25。来源为英文 Mendeley Data 官方公开记录。数据尚未下载和逐行解析，禁止登记为新增真人E2预测或已完成独立复现。

## 官方来源与可核实元数据

作者 Eyal Ert、Ariel Dinar、Shier Cohen-Amin。数据标题 *Data for: The Effect of Issue Linkage on Cooperation in Bilateral Conflicts: An Experimental Analysis*。2019-03-02发布，固定版本 V1，DOI https://doi.org/10.17632/6vsvptct74.1，公开页面 https://data.mendeley.com/datasets/6vsvptct74/1 。官方页面明确显示 CC BY-NC 3.0 许可、Download All 入口及行为实验类别。许可含非商业条件，未经逐文件条款确认不再分发原始行记录。

实验为 Isolated 与 Linked 两类条件下的双人重复互动，涉及两种游戏。官方变量说明：
* Period：每个游戏30期。Isolated条件下每期先进行 game1 再进行 game2。
* Subject：场次内受试者编号；Group：组编号；session：实验场次编号。
* choice：Isolated 为0/1，1表示合作；Linked 为1至4，对应两个游戏合作或背叛的四种联合选择。
* partnerchoice：该期匹配对手的行动；partner：30期配对的对手编号；player：玩家编号。
* cond：Isolated/Linked；TimeDecision：决策时间；FinalPay：按抽取一期计算的最终支付；raffle：决定抽取期的变量。

这些变量的存在和含义来自作者公开元数据描述，尚未以原始文件逐行验证。官网没有在当前可读文本中提供可核对的文件名、下载文件哈希、实际行数、场次数、独立参与者数或完整字段类型。

## R073 冻结协议适配初筛

高价值之处：公开描述同时提供二元本人行动、对手行动、场次、配对身份和30期时序，理论上可构造完整留场次评分。需要先确认同一场次内两个游戏的期次顺序、对手标识的实际唯一性、每个受试者的重复配对是否固定，以及是否存在缺失或错误记录。

**Isolated** 条件的0/1行动最接近R073冻结的C/D目标。**Linked** 条件的1至4是两个游戏联合行动，直接套用R073二元模型会违反冻结编码；若未来进行拆解，必须另行冻结数据映射和排除规则，不能事后择优挑选游戏。当前不做任何评分或调参。外部独立实验资格还需对照R073、R074、R075既有作者/实验及其他R系列来源。已读取三者README，现有明确来源分别为 Montero-Porras 2022、Dal Bó & Fréchette 2011、Fudenberg/Rand/Dreber 2012；本候选作者与论文不同，仍不能在逐行哈希和实验设计核验前宣称数据独立。

## 访问状态、许可与复现阻塞

本轮实际访问官方公开网页及公开API文档。网页的 Download All 入口可见，但当前文本接口没有暴露可核实的文件字节，公开API元数据端点在本次工具环境无法读取。没有注册账户、购买数据、访问私人数据或使用收费API。实际原始行获取状态 `BLOCKED_NOT_RETRIEVED`。缺口：原始文件字节及SHA、逐行字段、缺失值、场次数量、配对/期次一致性、独立样本资格、冻结适配的可执行评分准备。

附带复核：先前候选 DFS2020 的公开英文 R 手册分别说明原始 `DFS2020` 为569行7字段，派生 `data.DFS2020` 为569行8字段。后者多出的 `input` 描述与 choice 有关联；在未取得原始RData行前不能断言完全相等，但在预测 choice 时应将该派生字段列为潜在目标泄漏风险。该实验为三人社会影响而非R073双人重复PD，继续保留不适配状态。来源 https://search.r-project.org/CRAN/refmans/stratEst/html/DFS2020.html 和 https://search.r-project.org/CRAN/refmans/stratEst/html/data.DFS2020.html 。

本轮 A 子流程结论：`HIGH_PRIORITY_PUBLIC_METADATA_CANDIDATE_ACCESS_PENDING`。新增可核验独立真人数据集=0，新增E2/E3评分=0。R073及PESEN v0.1冻结不变。
