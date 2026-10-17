# R091正式科学报告：Jonsson 2025独立四人公共品实验证实组历史行动的有限跨环境预测益处

日期：2026-10-17。**R091=CLOSED_BOUNDED，A01–A06有界验收PASS，E2原作者真人资料跨作者完整留出预测成功、双原件精确复算归档；E3新独立采集、因果心理机制、长时段历史预测均未成立。** PESEN v0.1继续FROZEN。

## 1. A01：研究目的与源独立性

Jonsson, Marijane Luistro & Jonsson, Markus (2025), **“Cooperation in the face of disaster”**, *PLOS ONE* 20(4):e0318891, DOI [10.1371/journal.pone.0318891](https://doi.org/10.1371/journal.pone.0318891)。论文描述在瑞典和菲律宾共**884名原始实验参与者**，四人群体成员不变连续互动20轮；各人每期将20货币单位中的整数0..20分配到公共品或保留，并在Control、10P、40P、Impact、Level等有无灾害风险的实验条件下完成互动。项目没有独立证明风险规则对合作的处理因果，也不因论文标题直接采纳作者机理。

R089对Pilgrim/Stewart/Raihani**六人二元Global投资率**做171个完整六人组各19轮留出，历史M1正向；R090对Antonioni/Sánchez/Cabrales的另一原作者30个六人组**连续贡献/禀赋比例**做各14轮留出，M1负向、M2池化略好，且249/2700为系统自动决策。R091转向真正**第三个原作者**、760个独立源参与者与**四人连续贡献率**，保持 M0/M1/M2 的**信息结构不改**，不把不同试验任务硬称为相同的预测目标。全部三组结果已在2026分析之前公开原始论文，均为回顾性E2，**不升级前瞻E3**。

## 2. A02：固定一手原始完整工作簿与防重复资格

第一手原作者 [markusrobertjonsson/condcoop](https://github.com/markusrobertjonsson/condcoop) 固定完整commit `2a23fc3221e636c0119b1d1f1a9c4945bca83e85`，原始`Data_Main.xlsx` **571,844字节**，原始Git blob SHA1 **`499787e08242c44c32a469b5d72b206ccf2c73f0`**，真实整文件SHA256 **`04d2ed5a59885cde2a1740f33b295a86bd374b80cd811d8ff84c88cded68a023`**。每次真实运行先按Git SHA1标准完整字节校验来源，再校验固定整文件SHA256，才解析原始XLSX；不复制原始个人/小组行为/问卷/ID入本项目GitHub。

作者README明确两sheet：`DiffTreatments` 15,201行含首标题（**15,200**真人原始参与者×轮贡献行），主五条件两国；`DiffProb` 6,641行含标题（6,640行），是瑞典概率扩展（Control、10P、40P与70P、100P），可能重复主sheet原被试。没有一个可信去重规则之前，**R091仅冻结使用`DiffTreatments`**，绝不假设两sheet加总为不同的真人，也不把论文884人直接当本次样本N。本次实际合格原始主体为**760名真人、190个独立四人小组、3,800个组轮、每人20轮共15,200真实贡献槽**，所有源个体ID在本组20轮均相同且每组每轮恰有四个不同原真人。两个国家各五处理共10个预定义层，最小组数量瑞典Level 12、最大菲律宾40P 23。

这项审计特别保留三个非行为学实测门及真实修复记录：
- [Phase A原始数据进入前协议](../../protocols/R091_JONSSON_DISASTER_PGG_ORIGINAL_XLSX_STRUCTURE_BEFORE_BEHAVIOR_2026-10-17.md) commit`9dd2fdec6c0d18d48065ea3249d1aabb8ff758c4`。首次[CI39015518318](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39015518318)发现synthetic测试中潜在的source header私密字段打印泄露，**在任何原件解析前失败**。固定首行和严格英文表头白名单后，[成功原作者整源结构CI39015557828](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39015557828)：21项synthetic全过，只有安全header和sheet行列数。
- [Phase B 20轮群体来源评分前协议](../../protocols/R091_PHASE_B_JONSSON_2025_MAIN_SHEET_4PERSON_GROUP_ROSTER_BEFORE_CONTRIBUTION_2026-10-17.md)，commit `b059eee1a9de37038aa292a73e6492cfd4450b96`。初次[CI39015826372](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39015826372) synthetic嵌套国别×条件计数对象错误，修复仅源报告布局，不改科学口径。随后[真实来源CI39015866343](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39015866343) 43synthetic PASS，但正确因源标签未映射而**FAIL_CLOSED**，真人贡献仍0。
- [Phase B2原始分类源安全审计冻结](../../protocols/R091_PHASE_B2_AUTHOR_COUNTRY_TREATMENT_SOURCE_LABELS_NONOUTCOME_FREEZE_2026-10-17.md) commit `c7735f73b75685a2def6e985d081ec9defcb913d`，原件[CI39015992841](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39015992841) 58synthetic、官方完整源SHA通过，**只读Country与Treatment源标签，绝未看贡献**，发现国家`Phils`(8880人轮)/`Sweden`(6320人轮)、处理`Control`(3200)/`10Prob`(3200)/`40Prob`(3120)/`40Impact`(2960)/`40Level`(2720)。另冻[Phase B3源码类别映射](../../protocols/R091_PHASE_B3_AUTHOR_ORIGINAL_FIXED_COUNTRY_TREATMENT_MAP_BEFORE_ROSTER_RERUN_2026-10-17.md) commit `8fbd644e8a90692f54afaa9c0e807d6b1db73d6a`，映射Phils→Philippines、10Prob→10P、40Prob→40P、40Impact→Impact、40Level→Level。再次[原作者全部群体身份、轮次无贡献实跑CI39016070946](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39016070946)，26项来源合成+21项原著源合成、全部190组×20轮实际身份核证成功。

## 3. A03：结果前冻结的跨组留出模型与评分

[Phase C正式贡献评分前冻结协议](../../protocols/R091_PHASE_C_190_AUTHOR_4PLAYER_GROUP_COMPLETE_LOOG_M0_M1_M2_BEHAVIOR_SCORING_FREEZE_2026-10-17.md)，提交 `2992a91e64530d2405e2dd05e9e6808f8171afe5`。不见R091贡献数据即固定全部三模型：对一个留出目标原始group G，country×treatment为唯一训练层，t=2..20，各轮 (y_{G,t} = sum_{i=1}^{4} c_{i,G,t}/80)，每人货币禀赋20且所有源贡献必须有限数值、整数0..20，一项不合格则全数据 fail closed。

- **M0** 使用同一国家/同处理的其它n−1个群体在同一目标轮t的历史实验平均 (y_{j,t})（严格排除完整留出group G的全部20轮）；
- **M1** 使用待预测group G前一轮 (y_{G,t-1})（允许真实下一轮在线观测的既往本组行为）；
- **M2** 固定 (0.5M0+0.5M1)，无参数拟合、无新正则与选择模型；
- 同一个原始四人组留出一次，共**190×19=3610组轮预测**，这**不是3610个独立原群体**；M0的其它组训练可看到对应目标轮的记录，故本任务是**跨组样本外评价**，不冒充预测所有场次在日历时间上首次发生；
- 误差MSE=((p-y)^2)，比较严格为同一G,t来源真实记录上的`M0_err−M1_err`以及`M0_err−M2_err`，分别报告全部、两国、五处理和十个国别×处理分层、正负组数，不做无冻结cluster CI或事后p值。

## 4. 190个真正独立原小组的主要跨原作者E2结果

全部190个四人群组各20轮已核验原始贡献完整且均为有限整数0..20，**并非模拟/合成选择**。所有100项本项目合成源/模型安全测试通过。

| 预先冻结预测器 | 全部3610组轮均方误差MSE | 相对M0同一目标的误差改善 |
|---|---:|---:|
| M0 其它group同国家处理同轮均值 | **0.0384959840** | 基线 |
| M1 本group上一轮贡献占比 | **0.0192001385** | **+0.0192958455** |
| M2 预设0.5M0+0.5M1 | **0.0193283712** | **+0.0191676128** |

因此第三独立原作者在**连续贡献率**而非R089的二元global选项上，仍显示本群体短期历史相对组外条件基线的**正的平均样本外预测信息价值**。此处预先冻结的M1不仅在池化上改善，两个国家分开计算也改善：菲律宾M1增益 **+0.0223465654**（111组、2109组轮）；瑞典 **+0.0150093910**（79组、1501组轮）。按五处理聚合：Control **+0.0465117672**，10P **+0.0078539341**，40P **+0.0074162738**，Impact **+0.0214008696**，Level **+0.0120739925**。按精确两国×五处理**10层M1与M2相对M0的平均改善全部正**，但不是一个全国推广的随机因果效应。

## 5. A04：不可省略的反向群体证据与跨实验限制

**190组中142组M1较M0的19期组平均误差较好，**另有**48组反而更差**，0组恰好相等。按事先冻结每层正/负计数：

| 原作者实验来源层 | 真实四人组 | M1平均改善 M0−M1 | M1改善组/恶化组 |
|---|---:|---:|---:|
| 菲律宾 Control |22|+0.053814|20/2|
| 菲律宾 10P |22|+0.009040|13/9|
| 菲律宾 40P |23|+0.007820|17/6|
| 菲律宾 Impact |22|+0.025636|17/5|
| 菲律宾 Level |22|+0.016084|20/2|
| 瑞典 Control |18|+0.037587|14/4|
| 瑞典 10P |18|+0.006405|11/7|
| 瑞典 40P |16|+0.006836|10/6|
| 瑞典 Impact |15|+0.015189|12/3|
| 瑞典 Level |12|+0.004723|8/4|

**跨三个原作者的证据仍是混合的：**
- R089六人`GlobalOnly/Balanced/GlobalBoost`二元`global`投资比例，在171组5折留出中M1较M0平均MSE提升 +0.0449179..+0.0456709（含64个缺失值锐界）；
- R090独立气候俱乐部30组六人原始连续贡献相对禀赋，M1较M0平均差 **−0.00831595**（反向），只有T1层改善，T2/T3/T4不改善，且2700人轮中**249次系统自动选择**；
- R091本次独立灾害四人公共品190组M1较M0平均差 **+0.01929585**，两国五条件均为正，但48组反向。

所以从“**大多数但非全部新的实验来源存在局部历史行为增量预测信息**”只能提出**机制异质性研究假设**，不能说M1已全环境复现、不能说R090负面现象被推翻或归因自动选择，不能在此三实验结果中挑正样本后合并统一“心理惯性参数”。另外R091数据`DiffTreatments`不包含另外一个瑞典概率sheet潜在的所有人，故不能宣称完成论文884真人的全部主分析。来源未带足够自动决策标记，因此**未能确认其每一次贡献都是独立自愿决定**，只是作者报告原真人行为的原始贡献记录。

## 6. A03/A06：两次真实原作者完整复算与正式科学证据等级

- [首次真实171? 不，实际**190组**的原作者复算run39016300977](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39016300977)（项目所有**100 synthetic PASS**后，再真实固定Jonsson XLSX完整Git blob和SHA读入、15,200真实行动、3610完整留出组轮预测SUCCESS）。
- [独立原始XLSX重新取回，100项合成重复，整个匿名结果逐字节比较、永久Git归档run39016368841](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39016368841)，SUCCESS：匿名全部国×处理/两国/五处理/原20期预测宏结果文件**18,471字节**、SHA256 `1657ee31c5df7640ea7a0943886900133e68f70c0f9c3ac900302d36191f723b`，第二次完整结果**字节完全一致**，永久Git blob `2f39bcda3560abbcda780051dedf9ee5e8b08863`，见 [匿名完整结果JSON](R091_INDEPENDENT_JONSSON_190_FOURPERSON_GROUP_3610_LOOG_M0_M1_M2_E2_RESULTS.json)。
- [严格SHA来源及隐私代码](r091_author_2025_disaster_xlsx_source_only_gate.py)、[角色/组/轮不看行为来源代码](r091_phase_b_main_sheet_group_time_roster_only.py)、[来源类别安全收据代码](r091_phase_b2_author_original_categorical_only.py)、[可真实重算190组的M0/M1/M2评分](r091_original_190_fourperson_disaster_group_loog_M0_M1_M2_E2.py)及全部4份合成测试和4次先执行正式冻结研究协议，构成独立证据链。
- 没有原始个人ID、集团ID、群体逐期可回识别真实行、完整原始工作簿、问卷或身份证明文件导出到本项目。所有差异源代码与CI失败都保留，**只修来源安全和编码，不在看贡献后改模型**。

**正式A01–A06限定验收**：A01真实新作者科学问题与竞争模型/目标预冻结PASS；A02一手原作者固定XLSX Git blob/SHA/76? 明确**760真人190稳定组**和source codebook内生资格PASS；A03 100synthetic、3610留出预测及独立全原始来源SHA逐字节复验PASS；A04 早期隐私源检测、真实代码本不匹配、48反向组和R090阴性全部保持PASS；A05已发表作者数据E2、不升级真人招募E3、无实验因果/独立RCT标识PASS；A06四阶段协议、可跑代码和synthetic、匿名原实证数据、双工作流、科学报告及repo主分支索引PASS。

**`R091=CLOSED_BOUNDED`, `EXTERNAL_AUTHOR_LOOG_M1=POSITIVE_AVERAGE_WITH_48_NEGATIVE_GROUPS`, `R089_R090_R091_CROSS_SOURCE_UNIVERSAL_HISTORY_RULE=NOT_ESTABLISHED`, `PESEN v0.1=FROZEN`.** 后续R092应把三个真人人类实验中的行动定义、自动代作与训练信息权限做跨研究对照，优先寻找第四个独立原作者**二元是否投资全体公共品**的原始数据，实现**行为目标相同**的实证再检验，不在190组上事后拟合调参制造无异质性结论。
