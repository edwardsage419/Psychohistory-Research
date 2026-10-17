# R079 Phase A/B：新原作者双人互动网络的真实组级二阶统计与随机匹配参考——结果前冻结

日期：2026-10-17，性质：`RETROSPECTIVE_REAL_HUMAN_E2_GROUP_STRUCTURE_DESCRIPTIVE_PROTOCOL`。**在任何 R079 双人配对相关性、跨组合作方差、随机匹配参照差数值结果出现前冻结。** 此前公开论文和R073–R078研究发现已被研究者读过，故不是研究实施前的预注册，不是新E3预测。模型PESEN v0.1冻结。

## 第一来源和适用范围

新来源 Andreozzi, Ploner, Saral (2020), “The Stability of Conditional Cooperation: Beliefs Alone Cannot Explain the Decline of Cooperation in Social Dilemmas”, *Scientific Reports* 10,13610，DOI `10.1038/s41598-020-70681-z`。**不同于R073/74/75/77原作者人群。** 作者 [GitHub](https://github.com/seyhunsaral/stabilitycondcoop) 固定 `master` commit `979abf87b5d3cfb7aa8be13b81ef233076c3bb75`，其清洗但未经本项目再加工的 `data/csv/subjects.csv` Git blob `bd4c1550002621bee7dfb50e0d15d317764d1ea9`，425701 bytes；作者 `code/process_raw_data.R` Git blob `522efd459f574ccaef3d9ce1dd2b086ffb70370e`，原作者README git blob `3292568ac99ec45c22ebcf009fa929028e07608a`。源许可证数据 CC BY 4.0，软件 MIT。固定 raw.githubusercontent.com 该 commit 的 exact URL，验证Git blob SHA1和大小**均一致**后才可以读任何真人数值。6个真正原始 z-Tree session 文件虽公开，但是本轮先用由作者本人脚本导出的 `subjects.csv`；**未证明每个cleaned字段与6份原始XLS逐字节重新导出一致**，该证明须另列OPEN，不得标成完全 raw reprocessing E3。

原作者定义 `treatment` 两制度（`NoCondInfo`、`CondInfo`），`session`原生场次，`period` 为前4个练习回合已剔除后重新编码的正式第1–10轮，`subject` 为场次内参与者，`group`为当前轮双人配对标识，`opp`为当前轮另一参与者，`action`本轮实际被执行的三档贡献0/50/100，`opp_action`为对手实际动作，`first_player` 是该轮第一行动者（角色互换可影响行为），`uc` 为不以本轮对手当前行为为条件的选择；`ccL/M/H` 是受另一动作条件的**策略菜单**。绝不将 `uc` 或策略菜单的未实现预案当实际贡献，不将已执行对手动作解释为在本人做出条件性选择前已知。 `opp_action_lag1` 由作者依 `subject_unq` 跨期生成，可用于未来时间研究，但本轮不会偷看同轮 `opp_action` 建立即时因果回归。

## 冻结风险单元和验证门

以 `(treatment,session,period,group)` 组成单轮双人配对主键；**每个组必须恰好两名不同 `subject`，每名参与者在 `treatment,session,period` 唯一，partner必须互指 `opp_i=subject_j`、`opp_j=subject_i`，`opp_action_i=action_j` 且 `opp_action_j=action_i`**。若缺失任一关键字段/非0、50、100/某组人数≠2/已实现伙伴不互证/一个人跨 treatment 或 session ID 被错误合并则FAIL CLOSED，不删除失败的某个pair。每个 `session,period` 中人数偶数、每人被配对一次，处理在session内唯一。原始 `period` 标准是否恰好1–10、两类处理各有多少原始session都由首次正式数据门计算并报告，不因结果择样。

数值 `y=action/100 ∈{0,0.5,1}`、只表示**实际贡献份额**（无0/1合作编码）；针对每个 `session×period` 成员观测 `y_i`：
- `mu=sum(y_i)/N`; `pop_var=Σ_i(y_i−mu)^2/N`;
- 所有真实无向组对 `(i,j)` 的 `cross=mean_pairs((y_i−mu)(y_j−mu))`。等价为每组均值的方差与个体方差之差，但这里聚合应优先直接 cross；它是**在该轮同组的两名真人的行为相关**，不是两个人具有共同心理原因的证据。
- **随机重组参考系**：固定该 `session×period` 当期每人的实际 `y` 不变，并假设所有完美匹配的可能配对等概率，配对产品的随机化期望 `random_match_cross=-pop_var/(N-1)`（抽样不放回有限人口的机械负相关），`excess=observed_cross−random_match_cross`。此非因果的**条件置换基准**并非实际实施的随机化因果试验：当期的y可能受到实际伙伴和制度影响，固定y后重组只做描述性参照、不表示 `do(partner)`。
- 同轮双人组均值 `m_pair=(y_i+y_j)/2` 的组内横截面**总体**方差 `V_pair=Σ_pairs(m_pair−mu)^2/(N/2)`；代数应严格等于 `(pop_var+observed_cross)/2`。其随机重组参考 `V_random=(pop_var+random_match_cross)/2`。每轮 (V_pair−V_random) 等于 excess/2；为独立每轮恒等式，不证明有跨组情绪/同质选择机制。
- 为防止重复测量和处理大小不均：首要报告对每个原始session先在该session 10轮里等权平均 `observed_cross, random_match_cross, excess, V_pair, V_random`，然后在**每个treatment内原始sessions等权平均**，再整体所有原始sessions等权摘要。任何某期缺人要如实标记/FAIL，而非把更多人/对局自动视为更多独立实验场次。
- 描述性正负结果与每session `excess>0,=0,<0` 场次数汇总，但不向Git发布任何单session编号/个人行动/单轮组均值，处理级的聚合可以发布。时间段（前5轮vs后5轮）的群体均值及处理级差仅作为**预先声明的次级描述**，不能解释为制度、实验分组或观察性学习因果。

**停止与标签：** 若全部原作者Git文件字节、配对互证和恒等式通过，完成首次跨个体组级真实 E2 描述；不会在R079启动任何R073模型后见调参。若人数结构不合约，保留阻塞并新版本化结构映射审计，不得改动期待结果来通过。当前仅两人实时对局群组，**绝不能当成R078构造里 n=10 群体或长期历史群体**，更不能据 `excess>0` 声称因果社会传染。

## 备选完整网络未来来源（本轮仅资格记录）

Hirokazu Shirado & Nicholas A. Christakis (2020)，*Network Engineering Using Autonomous Agents Increases Cooperation in Human Groups*，iScience DOI `10.1016/j.isci.2020.101438`，作者资料库 Mendeley Data `https://data.mendeley.com/datasets/t963ktp6ft/1`，DOI `10.17632/t963ktp6ft.1`，原文1024位真人、64个网络、包含某些人-机器人配对/实际网络重连；CSV/JSON原始文件和真人/机器人身份本轮尚未核验 exact bytes。为了不把模拟机器人当真人社会效应，必须未来独立审计源原始行为、实体身份、网络时序及实验分配；此候选不是本轮数学组方差的真人已计算数据。

`R079_SOURCE_GIT_BLOB_FROZEN=bd4c1550002621bee7dfb50e0d15d317764d1ea9`  
`R079_FIRST_REAL_PAIR_CROSS_STATISTICS_PENDING=YES`  
`R079_OBSERVATIONAL_DESCRIPTIVE_ONLY=YES`  
`R079_EVIDENCE_TARGET=E2_REAL_AUTHORS_CLEANED_GROUP_DYAD_DATA`  
`R079_CAUSAL_PEER_EFFECT_IDENTIFIED=NO`  
`PESEN_v0.1=FROZEN`
