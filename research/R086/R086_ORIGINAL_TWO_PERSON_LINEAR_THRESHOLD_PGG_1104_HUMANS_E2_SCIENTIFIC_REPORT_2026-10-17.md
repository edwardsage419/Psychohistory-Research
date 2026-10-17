# R086正式科学报告：原作者两人线性/阈值公共品五种资源条件的1104真人贡献轨迹

日期：2026-10-17。**R086=CLOSED_BOUNDED；已取得E2真实原作者数据全面复算与两次独立SHA全字节一致证据**。禁止将这种已发表实验的描述性回顾分析解释为制度政策因果、一般社会人口预测或E3独立新实验。本研究未重用R085四人MAT失败文件，因此R085继续作为独立负面证据留存。PESEN v0.1继续冻结。

## A01：科研问题与源范围

原作者 Wang, Xiaomin; Hilbe, Christian; Zhang, Boyu (2025), *The dynamics of cooperation in asymmetric public goods games*，原数据、Matlab演化模拟源于 [官方Zenodo v2记录10.5281/zenodo.16918146](https://zenodo.org/records/16918146)。本次新模型家族着眼于**禀赋与生产率不对称条件下两人合作的短期轨迹**。两种实验分别是线性公共品、阈值公共品；每种5处理：FE（完全平等）、EI（禀赋不平等）、PI（生产率不平等）、AI（优势一致）、MI（优势错配）。与R071规范惩罚数学模型、R083真人条件惩罚策略、R084内生制度实验来源失败和R085四人MAT解析失败都属于不同原始科学样本或观察合同。

科学问题：在**同一参与者、同一次session内**，原始公共品贡献从第一轮到末轮是升、降还是保持不变？不同的线性/阈值规则和五原始处理组有无不同描述性轨迹？竞争性的符号层机制假设为 M0不定向、M1提升、M2侵蚀，仅观察有界的统计方向，不将符号解释为心理原因。

## A02：原作者二原文件的不可变来源资格

R086 Phase A [已在任何真人行动评分前冻结来源方法](../../protocols/R086_WANG_HILBE_ZHANG_TWO_PLAYER_PGG_ORIGINAL_XLSX_SOURCE_AND_OUTCOME_FREEZE_2026-10-17.md)，提交 `9384d806e85b18e50d8b30f0c531b0cc1203adc5`。 [第一次完整发布方原始工作簿来源检查 run 39003094721](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39003094721) 成功通过24项合成，并实际确认两件作者源：
- **线性** LinearPGG_ExperimentalData.xlsx，官方原发表MD5 `fc71d20de62c259629ceb56559d8a69e`，504163字节，首次全字节SHA256 `b423cda39bfd7d84f2edb7f56b4bccc0d03164743bb4df851d20f049725fb507`，作者5条件共**550名焦点真人**。
- **阈值** ThresholdPGG_ExperimentalData.xlsx，官方MD5 `c40171abb172da8e16b0839db98a2cf2`，217396字节，全字节SHA256 `825b1cd3226aeca7a19d76d9594f655114b12059648f9ca03b3291c3cf9ab200`，共**554名焦点真人**。

两个文件各实际有10个原作者工作表，为5处理×Type1/Type2，工作表历史源英文拼写中线性Full_equlity、Misaliged_inequality与阈值Full_equality、Misaligned_inequality不同，均按原始精确名称读取，不假称失效或静默编辑原文件。

## A03：评分前冻结的真实个体/角色/轮资格

在首次真实贡献计算前提交[Phase B原始人类行动合同](../../protocols/R086_PHASE_B_TWO_PERSON_FULL_ORIGINAL_BEHAVIOUR_WITHIN_SESSION_FROZEN_SCORE_2026-10-17.md)，commit `4a0475972655b8662a52f2b53f9d06585a9112d0`。每一sheet首行为标题，其后每4行属于**唯一焦点参与者**，非4独立人；前2行第1session的玩家1/2，后2行第2session的玩家1/2。Type1该人第1session取每block第1行、第2session取第4行；Type2该人分别取第2行、第3行，因此同一个人每session计入一次，互换角色并更换伙伴后仍是同一原受试者。真实行为列C至V对应阈值两session各20轮，线性第1session C至X共22轮，第2session C至W共21轮。参与者身份元数据只在运行内检查，不在报告、日志或源保存；原始同伴行为、问卷、个人记录都不向Git输出。每个选定贡献单元格要求有限非负数值，任何缺失/错误直接拒绝本游戏全量估计，未插补。

因此当前实际审计了**1104个原作者焦点真人**的全部两场有效个人决策：线性550×(22+21)=**23650**个原始真人个人决策槽，阈值554×(20+20)=**22160**个，共**45810次真实自身贡献记录**。这些是可复算来源的原始个人贡献而不是模拟仿真；未乘四行、未把同一真人两session当两新真人。与R085不同，此次真实Excel文件内容已成功被解析用于完成真人初末指标。

## A03：两游戏、五处理、两session预定20格真实结果

每人自己的session末轮贡献减该session首轮贡献，再对该条件全员等权取均值。全部指标保留**原始数值单位**，不同条件的禀赋不一定相同，不能仅因数值大就推论总体效率更高。每条本人与同伴互动及角色交换的行为可能相关，无预先组/配对推断合同，不做显著性检验。

| 类型 | 原始处理 | 原始真人 N | Session1 ∆ | Session2 ∆ | 同号? |
|---|---|---:|---:|---:|---|
| 线性 | FE | 114 | −0.175439 | −1.061404 | 是，均负 |
| 线性 | EI | 110 | +1.272727 | −0.563636 | 否 |
| 线性 | PI | 110 | +1.236364 | +1.800000 | 是，均正 |
| 线性 | AI | 106 | +5.094340 | +2.254717 | 是，均正 |
| 线性 | MI | 110 | +0.436364 | −0.272727 | 否 |
| 阈值 | FE | 110 | −0.345455 | −0.545455 | 是，均负 |
| 阈值 | EI | 118 | −0.813559 | −0.593220 | 是，均负 |
| 阈值 | PI | 112 | +0.053571 | −0.303571 | 否 |
| 阈值 | AI | 104 | −0.865385 | −1.644231 | 是，均负 |
| 阈值 | MI | 110 | −0.227273 | −0.700000 | 是，均负 |

**观察：**线性5处理的10个session中6个末初差正、4个负；阈值10个session中仅PI第1session近乎0的正向+0.053571，其余9个负。线性AI和PI在两场均正，线性FE在两场均负，线性EI/MI方向切换。阈值FE/EI/AI/MI均两场负，阈值PI第1场微弱正转第2场负。这个模式说明**实验制度形式和人群/处理结构相关的短期合作动态异质性**，没有独立显示不对称本身的随机因果作用。

## A04：必须一同保存的负例、零变化与内部异质性

个体delta正/负/零不是均值符号的同义词。部分真实原作者条件中大量人没有改变自身首末选择：

- 阈值FE第1session：7人增加、18人减少、**85人不变**（110人）；第2session：4增加、13减少、**93人不变**。
- 阈值PI第1session：17增加、23减少、**72人不变**（112人）；第2session：3增加、12减少、**97人不变**。其第1场平均值轻微为正不能推出“多数人提高”。
- 线性AI第1session：60增加、21减少、25不变（106人）；第2session：44增加、25减少、37不变。
- 线性FE第1session：39增加、46减少、29不变（114人）；第2session：40增加、37减少、37不变，虽均值负、个体增加者人数在第2场反而多于减少者。

完整20格中每人的增加/减少/不变人数及20/21/22轮平均曲线、Type1/Type2角色分层，都在永久存档JSON；此次未基于哪一条曲线“好看”而调整源权重或控制变量。这样保留一组与“多数个人行为持续侵蚀”相反的真实反例，禁止只看总体均值制造一致性故事。R085四人MAT原作者MD5通过但无法解析的失败仍独立保留，不能混入R086两人样本。

## A03/A06：两次官方原始字节重取与完全独立重复

- [Phase A来源固定+24 synthetic+真实原件结构run 39003094721](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39003094721) success。
- [第一次真实完整本人贡献E2 job run 39003367675](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39003367675)：两job success，24+29=**53项纯合成**成功、两原始源MD5与首次原件SHA256严格核对后才重构真人贡献并计算20主格。
- [第二次原始两Excel独立完整重下、53 synthetic及逐字节归档run 39003432643](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39003432643) success，真实结果**85566字节**、SHA256 `600104f42f2b896646abe543cc6d8ab10450f1d30ed823d9feeeaf6d20a1628c`，对首次全文件逐字节一致。第二次永久Git提交[所有五处理二角色两session匿名指标JSON](R086_ORIGINAL_1104_HUMAN_TWO_PERSON_LINEAR_THRESHOLD_FIVE_ARM_E2_RESULTS.json)，Git blob `51c69cdd2c41cd8e688ddd9d8129167746552d83`。
- [匿名可重放实际人类贡献程序](r086_original_two_person_full_human_contribution_E2.py)、[24项source-only合成](test_r086_original_zenodo_two_player_xlsx_source_gate.py)、[29项全行为源/角色合成](test_r086_original_two_person_full_human_contribution_E2.py)、[首次真人CI](../../.github/workflows/r086-original-2025-two-person-linear-threshold-complete-human-E2.yml)、[独立永久归档CI](../../.github/workflows/r086-independent-author-XLSX-human-E2-exact-replay-and-archive.yml)。

## A05：科学边界

本次观察为2025年作者已发表实验的**E2原始数据复算**，不是新受试者或E3独立外部复验。两次session同一个人更换角色及重新配对，不能说是两个相互独立随机参与者总体。线性与阈值实验为不同参与样本及实验规则；直接比较原单位∆并没有证明游戏形式的随机因果作用。FE、EI、PI、AI、MI之间不确定的处理分配/角色资源和生产力参数差异、二人博弈相互影响，缺少对应随机化与聚类计量推断，因此不作p值或群体政策平均处理效应。所有调查问卷在行为之后收集，未用事后答案拟合行为预测或宣称机制。仅20/21/22轮的短期合作现象不能推出制度演化或历史事件长周期。

## A01–A06正式有界验收与移交

A01研究问题/合同PASS；A02来源及两个原作者实际MD5/首次SHA/样本映射PASS；A03 53项合成、两次完整原始真实来源计算、完全一致JSON PASS；A04保留30个角色子格/20主格方向异质和个体增减零、先前R085失败PASS；A05局限 E2、不升级E3或因果PASS；A06协议、代码、数据、真实CI、科研报告和Git主分支索引PASS。

**R086=CLOSED_BOUNDED，原始真人E2数值来源与完整匿名可复算包PASS，因果、独立外部E3、跨制度/历史动力学OPEN；PESEN v0.1=FROZEN。**

下一项R087建议选择不同原作者/制度模型的真实群体层来源，优先考虑网络、行为传播或可随机化制度变更的原始多组数据，并在新来源分母合同与效应模型冻结前不得把R086当作政策“因果效应”。
