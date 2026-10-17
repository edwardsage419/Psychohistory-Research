# R088 正式科学报告：171个人类六人群组、多层公共品规则与64项缺失行为的全球合作锐界

日期2026-10-17。**R088=CLOSED_BOUNDED**（限定数据的描述性完整组行为E2，经独立两次来源实跑），**真实机制因果E3=OPEN**。这是原作者Pilgrim、Stewart、Raihani于2025-12-28在线发表的2026卷 `Scientific Reports` 已有真人实验结果的**回顾性原始数据独立复算**，不是2026年新招募真人或论文发表前预注册。论文 DOI https://doi.org/10.1038/s41598-025-30979-2，标题 *Social identity and cooperation co-evolve in a multilevel public goods game*。

## A01：新增跨尺度实证对象和实验设计

原作者原始在线20轮阈值公共品实验共171个**完整、六人**且两组三人的团体，每处理有57组，1026名真人，3420个组轮与20520个潜在人-轮行动。GlobalOnly（没有本地投资选项）、Balanced（可投资自身本地或其他本地或六人整体）、GlobalBoost（在Balanced基础上提高六人公共品达标的奖励），每轮只能将单个实验硬币分配到自己保留/自身本地/对方本地/六人整体一种行动。六人整体累计至少4人投资global即达标；其中`other`是向另一个三人组投资，**绝不是自留/缺失**。

R088在严守两层群体归属的前提下仅研究可验证的全球合作强度和六人达标事件。社会身份指标、分组内局部公共品达标和真实收益机制的跨层因果解释不在本研究中，禁止简单把三处理组观察差异当作制度因果效果。该研究与R087的134名真人双人条件策略迁移构成不同原作者/不同群体层的原始E2证据，不共享受试者。

## A02：完整一手作者文件与失败也要归档的来源链

原作者仓库 [chasmani/PUBLIC_social_identity_and_cooperation](https://github.com/chasmani/PUBLIC_social_identity_and_cooperation)，原始上传固定commit `8ce2c0cac4784485232aa96295f48ff147290b05`，直接从固定Git raw读取作者经过既有排除的六人完整组源 `analysis/data/data_full_groups.csv`（2,270,643字节；Git blob `f902865203bdb465a505869b593eca432831b2fa`），另锁定 `analysis/analysis_exclusions.R` 原blob `5d7f6e65523df55a1f05bd69f48d60b9306783a9` 和 `analysis/analysis_cooperation_rates.R` 原blob `60793d82709a7807e86ceddd772fe2847733a6e2`。三个源均按精确Git blob头和完整内容核验，不把GitHub HEAD当作冻结来源。

本轮实际按科研失败优先规则经历三阶段，每个评分方法在看到其自身真实人类统计前均单独冻结：
1. **Phase A：原始全部行动完整性预先假设不成立。** [原始评分冻结协议](../../protocols/R088_SIX_PERSON_MULTILEVEL_PUBLIC_GOODS_171_GROUP_ORIGINAL_SOURCE_E2_FREEZE_2026-10-17.md)，提交 `1f84bf430e4bb3c4aff8bf25eb90ba54e008df24`。首次[GitHub Actions 39011042473](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39011042473)纯合成35测试PASS，但真人源行动出现非四类别，报 `R088_HUMAN_ORIGINAL_ACTION_NULL_OR_UNEXPECTED`，真实群体分数 **0**，job **failure**。没有把失败结果冒充已得E2。
2. **Phase B：真实标签身份/缺失、无合作得分。** [新增Phase B诊断前协议](../../protocols/R088_PHASE_B_ORIGINAL_ACTION_FIELD_DIAGNOSTIC_FREEZE_2026-10-17.md)，提交 `93008fb66516af9930c5a79d4a162fa744fa0a5b`；原作者完整20520个槽中观察合法行动20,456，**缺失空值64**，不存在大小写/尾空格可修复错误或另一个自定义行动类型。按处理分别 GlobalOnly19、Balanced26、GlobalBoost19；第一轮29、最后轮0缺失。源诊断[run39011243425](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39011243425)合成52项PASS，未计算真人合作或阈值结果。[真实安全缺失来源收据](R088_ORIGINAL20520_ACTION_LABEL_MISSINGNESS_E1_SOURCE_RECEIPT.json) **2144字节**，SHA256 `b52f6313f40beecdb761c5bb9b6013b318700c2e1c2f8f4d0a7682efee5edf18`，Git blob `1ddd9097eddf8447861285eb37191dd1d6f9ab1f`；第二次独立重读后逐字节归档。
3. **Phase C：不删任何人/组，冻结64个缺失行为的上下界。** [原始真人新评分前冻结协议](../../protocols/R088_PHASE_C_ORIGINAL171_MISSING_ACTION_SHARP_INTERVAL_SOURCE_FREEZE_2026-10-17.md)，commit `b8f819e806a5dc39c10f5c0de13c9f613145dae3`。保留前2阶段阴性，新算法只允许实际观察行动固定、missing可在该条件所有允许行动中取任意值，**绝不将missing当self或global插补**。对每组六人每轮实际global数g、缺失数m，本轮全球率分子严格 `[g,g+m]`；阈值达成指示严格 `[1(g>=4),1(g+m>=4)]`。在相同分母6×57×20/57×20下等权求原处理人/组界限；不同处理的差界 `[lower_A-upper_B, upper_A-lower_B]`。没有统计置信区间的伪装。

## A03：171个真实原作者群组完整20轮实证锐界

上下界为所有缺失行动可选择合法原游戏行动时的数据识别范围，**不是bootstrap、不代表95%置信区间**。

| 原始实验条件 | 完整六人组 | 原人-期缺失 | 20轮平均全球投资率锐界 | 20轮全球阈值达到比例锐界 | 本组末轮减初轮全球投资率锐界 |
|---|---:|---:|---:|---:|---:|
| GlobalOnly | 57 | 19 | **67.9532%—68.2310%** | **71.3158%—71.5789%** | **−27.1930—−24.8538个百分点** |
| Balanced | 57 | 26 | **44.6199%—45.0000%** | **42.9825%—43.5088%** | **−26.6082—−24.2690个百分点** |
| GlobalBoost | 57 | 19 | **60.6287%—60.9064%** | **64.3860%—64.5614%** | **−21.0526—−17.2515个百分点** |

全球阈值确知达成和可能达成的总group-round数：GlobalOnly **813—816** /1140；Balanced **490—496** /1140；GlobalBoost **734—736** /1140；总缺失诱发的不确定达标group-round为 **3+6+2=11**。全部3420个group-round保留，绝不能把1140组轮当1140个独立新群体或置信区间样本单位。

事先固定的处理对全球投资群体等权20轮均值差锐界：

| 对比 A−B | 无论64缺失如何的原始样本差区间 | 缺失稳健方向 |
|---|---|---|
| GlobalOnly − Balanced | **+22.9532 至 +23.6111个百分点** | 正 |
| GlobalBoost − Balanced | **+15.6287 至 +16.2865个百分点** | 正 |
| GlobalBoost − GlobalOnly | **−7.6023 至 −7.0468个百分点** | 负 |

即便每个缺失单元都取可能让一方更低、另一方更高的行为，**原作者已经筛选的完整组样本**仍显示本地选项共存情境下全球投资比例比GlobalOnly低，增加全球达标收益后相较Balanced出现较多全球投资，但没有完全恢复GlobalOnly的投入比例；这一描述发现与原论文已公开结论方向一致，属于对原作者数据的独立回顾性核证，不是新的随机因果识别。

## A04：第一轮到末轮、个体行动缺失与真实相反证据

三处理从初轮到末轮全球投资率均下降，锐界都为负，并且来源第20轮无缺失，因此第20轮的全球投资率有确定点：
- GlobalOnly 1轮87.4269%—89.7661%，20轮**62.5731%**，变化必在 **−27.1930—−24.8538**个百分点；
- Balanced 1轮61.4035%—63.7427%，20轮**37.1345%**，变化必在 **−26.6082—−24.2690**个百分点；
- GlobalBoost 1轮71.6374%—75.4386%，20轮**54.3860%**，变化必在 **−21.0526—−17.2515**个百分点。

“所有组都降低”是错误主张。按独立原始完整组及缺失锐界，至少 GlobalOnly **41/57**组保证下降、**1**组保证上升，11组保证首末完全相等；Balanced **37/57**组保证下降、**11**组保证上升，7组保证相等；GlobalBoost **35/57**组保证下降、**9**组保证上升，9组保证相等。由于8/8/11组的首末差受missing影响，以上保证正负/零计数**不构成互斥穷尽分解**；不能为了凑57把不确定的组当不变。这也是不能用第一轮完整案例或自由填补假设制造“所有组下降”的理由。

原始真实20,520应有槽中20,456实际行为明确归类，64为空；真实授权原始完整组不等于每人每期有决定：Phase A真实失败的科学价值就在发现原作者排除“最终轮非空/六真人完整”并未保障第1至19轮都不缺失。直接使用原作者group聚合 `global_group_contributions` 的重复记录易隐藏漏记风险，本次严格以六名实际行动去重组计数并界定缺测，不声称对所有招募者无选择偏差。

## A03/A06：独立执行、全部材料与最终科学验收

- [首次Phase C真实171组、81 synthetic run39011509370](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39011509370)：35项A+17项B+29项C合成全PASS，实际固定原始三个Git blobs读入、以171×6×20原始行动计分并成功得到64 missing的识别界限。首次安全匿名结果 **65,424字节** SHA256 `2b0f76fa8f7d1a42d2f91508c4acf52c0a7c0fc9523801ec1d9759559d8fb67e`。
- [二次独立真实来源重新取回、81 synthetic、两份证据完整字节复验并永久归档run39011582787](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39011582787)：全部job SUCCESS，先取回原CSV核对缺失来源审计安全收据2144字节SHA一致，再独立取回作者原CSV+R脚本SHA核证全部3420组轮行为区间与首次65424字节结果**逐字节相同**，方可提交永久原始宏结果Git。
- [匿名全部20轮、三处理、全部首末群体锐界结果](R088_ORIGINAL171_GLOBAL_COOPERATION_64_MISSING_SHARP_BOUNDS_E2_RESULTS.json) Git blob `1b97419451e6124d7d7449bdb87f743905f43789`，65,424字节，不含任何个人ID/群组ID/个体数据。
- [作者真实缺失安全来源收据](R088_ORIGINAL20520_ACTION_LABEL_MISSINGNESS_E1_SOURCE_RECEIPT.json) Git blob `1ddd9097eddf8447861285eb37191dd1d6f9ab1f`，2144字节。原始逐人/原始问卷/原始公司平台登录和完整CSV均不复制入本Git。
- [严格失败原Phase A源码](r088_original_171_groups_multilevel_global_cooperation_E2.py)、[安全字段诊断程序](r088_phase_b_original_action_schema_only_audit.py)、[缺失锐界真实源码](r088_phase_c_original171_missing_sharp_bounds_E2.py)，加全部对应35+17+29个完全synthetic tests与3次CI workflow一起保留。

A01 独立两层真人实验机制与清楚评分单位 PASS；A02 原作者固定完整组CSV和作者排除/分析脚本Git blob源核证 PASS，raw招募至完整组的数据加工独立重放 OPEN；A03 81synthetic和两次真实完整数据来源结果全字节一致 PASS；A04 真正缺失64、初次真实source fail、groups内保证上升/下降/不确定负例全保留 PASS；A05 回顾性已发表E2、不能识别因果/身份心理机制/历史长期演化 PASS；A06协议、正式报告、实际代码/测试、准确结果、独立归档及GitHub main永久索引 PASS。

### 必须保留的科研边界

1. 原论文经过其 **先验排除与事后完整组六人**筛选；本计算只适用于171完整组、而非所有起始招募受试者。跨组社会身份测量未纳入实跑，不能据此证明“身份和合作相互因果驱动”。
2. 缺失上下界仅证明**只因64个未知行为而产生的分类误差**不能颠倒三对的处理次序；**不处理**群体层抽样误差、政策随机化资格、post-treatment subgroup selection或会话内群组互依。
3. 本轮独立重算是同一原作者实验原始资料两次取回与相同代码复算，不是独立实验室E3；原2025/2026论文首发发现不是我们原创。
4. 即使初末组级差锐界全负，不能推出永久集体衰退或具体社会历史宏观冲突演化；仅是20轮小组微观行为数据。

**正式 `R088=CLOSED_BOUNDED`，`E2=171_GROUPS_MISSINGNESS_SHARP_INTERVAL_VERIFIED`，`CAUSAL_SOCIAL_IDENTITY_INSTITUTION/HISTORY=OPEN`，`PESEN v0.1=FROZEN`。** 下一R089优先另一原作者实证，或新增身份认同动态与合作时序的独立预测协议并预留场次/群体留出验证；不可把本源上继续增长的复杂模型当作更高证据级别。
