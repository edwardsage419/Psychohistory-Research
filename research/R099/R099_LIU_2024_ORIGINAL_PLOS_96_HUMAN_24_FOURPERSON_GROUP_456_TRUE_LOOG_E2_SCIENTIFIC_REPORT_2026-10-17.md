# R099 正式科学报告：2024年另一研究团队96名真人20轮公共品实验、24个真实四人组完整留出的历史预测正向证据

**2026-10-17。R099=CLOSED_BOUNDED，真实第一手原实验 E2 固定四人组留出预测已通过；不是实验室场次完整留出、不是前瞻E3，PESEN v0.1继续FROZEN。** 2024 PLOS 的完整原数据、90项纯synthetic与真人456个严格同目标下一轮组贡献预测，经两次独立官方完整源字节SHA重新获取重算，匿名真实结果 SHA256逐字节相等，正式归档。

## A01 独立原作者实验的来源与外推单位

**Chi-Hsiang Liu、Shih-Feng Tsai、Ting-Cih Chen、Hsiu-Wen Cheng**，2024 [*The signaling role of feedback in the repeated public goods game: Experimental evidence from the laboratory*](https://doi.org/10.1371/journal.pone.0299196)，*PLOS ONE* 19(2):e0299196，[出版方官方 S1 CSV](https://doi.org/10.1371/journal.pone.0299196.s002)。独立于R095作者Schniter/Shields二元Friend or Foe、R096作者Montero-Porras等100轮双人囚徒困境，也不同于R091作者Jonsson等四人离散灾害困境。

原论文报告中国Hubei University of Economics BEER Lab **2019年12月7至15日**在8个真实独立实验室场次招募96名真人：每场12名、简化反馈SF四场48人、详细反馈DF四场48人；无人跨原session参与。实验两阶段：先一轮策略法诱导分型，再**20轮固定四人组公共品博弈**。第二阶段每人每轮固定20代币，可贡献0至20，实验反馈SF仅显示自贡献、团体总额和收益，DF增加冗余细节及往期历史。本文只评估第二阶段20轮源真实动作；分型`Type`源第一阶段资料绝不作为预测器或标签。

PLOS 原始CSV**包含`subject,id,Period,group,DF,Contribution,OtherContri,Type`八列，没有单独命名`session`列**。因此科学上只能证明**24个原作者数据中身份不重合、每组固定4个真人×20轮的真正四人组**，而不保证8个原始实验室场次的准确文件内归属已重建。不能将24组说成24个独立招募session，也不能以原论文“8场次”文字代替未经来源字段验证的真正LOSO。为最大限度避免外推夸大，本次冻结为 **LOOG: leave-one-original-four-person-group-out**，非session-LOSO。

## A01/A02 分层冻结的原作者原文件来源链

源文件固定**官方完整可下载URL**：
`https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0299196.s002&type=supplementary`，PLOS期刊官网通过自己发行签名重定向将它交付于 **`storage.googleapis.com/plos-corpus-prod/10.1371/journal.pone.0299196/1/pone.0299196.s002.csv`**，签名主体wombat-sa@plos-prod.iam.gserviceaccount.com。保留严格只允许这一特定发布对象及签发人、算法字段的源host限制，不保存或上传真实短时效签名令牌。原出版方**未查得独立发布MD5**，所以严禁虚构；完整原CSV **43,467字节**，首次与多次独立重新下载计算完全相同 SHA256 **`75dc8ae8b63a6b3ea728df9acab9d27944b82ec4feb5c6055e26751ca9cc4a6e`**。

冻结顺序：
1. [Phase A官方原source URL/SHA安全与零行为预冻结](../../protocols/R099_LIU_TSAI_CHEN_CHENG_2024_PLOS_ORIGINAL_8SESSIONS_96HUMANS_20ROUND_4P_FEEDBACK_CSV_SOURCE_GATE_2026-10-17.md)首先存在。[CI39026768346](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39026768346) 25synthetic成功，但真实原source被默认重定向安全门槛拒绝；**没有来源身份或真人效应结果**。
2. [Phase A2独立冻结唯一PLOS签发的Google存储原CSV重定向](../../protocols/R099_PHASE_A2_OFFICIAL_PLOS_CORPUS_GOOGLE_STORAGE_SIGNED_CSV_REDIRECT_FREEZE_2026-10-17.md)，额外4synthetic反例保护其它桶/路径/签发人，运行[CI39026865693](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39026865693) **29synthetic加真实期刊原CSV整文件SHA和安全表头1,920行均SUCCESS**，且第一次源阶段完全不读取人类行动数值。
3. [Phase B真实原CSV participant×round×group身份元数据先冻结](../../protocols/R099_PHASE_B_PLOS_1920_ROW_96_PERSON_24_ORIGINAL_GROUP_NONBEHAVIOR_ROSTER_FREEZE_2026-10-17.md)并运行[CI39027055517](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39027055517)：共**53synthetic**（29+24）全部PASS；真实严格同一SHA元数据仅基于源`subject,id,Period,group,DF,Type`审核，**没有调用`Contribution`/`OtherContri`任何真实格**。实际独立`subject`和`id`各96、稳定配对96、每一人20期，`group`24唯一真实组，每组4人×20轮，共**1,920原人物轮**，反馈类别两个，合作倾向`Type`原来源有3类，但均不进入模型。source`group`作为唯一真实四人组key，原`id`是个体键，不能拿`id+group`错误构造96个单人“组”。实际源没有可证实`session`字段。
4. 然后在任何一份真人源`Contribution`数值计算之前正式[Phase C冻结24真实原四人组完整留出M0/M1/M2](../../protocols/R099_PHASE_C_FIRST_PARTY_PLOS_24_TRUE_FIXED_4PERSON_GROUPS_20ROUND_LOOG_M0_M1_M2_PRESCORE_FREEZE_2026-10-17.md)。所有竞争模型形式与研究前序R089—R096完全相同“外部组同期参照、自己历史、固定半混合”信息结构，没根据此作者真人损失拟合新参数或删样本。
5. [首次整源真人实际行为源CI39027265753](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39027265753)全部**90synthetic+源original SHA+96人24原组20轮所有1,920原行动整数贡献+456真正组轮预测**成功。 [再次独立同一出版方重新取回全部原CSV并同组留出真人重评分+匿名结果严格SHA归档CI39027344527](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39027344527)全部success，二次结果**7,098字节、SHA256 `91338505fac057c0dbc24f63430f7453f77cf824a1ccb40a737c047fc0449306`**逐字节完全相等，并永久commit[匿名真E2结果JSON](R099_LIU_2024_PLOS_ORIGINAL_96_HUMAN_24_FOURPERSON_GROUP_456_LOOG_M012_E2_RESULTS.json)，Git blob `ef851d7a8bf46da2d8d85472135667ca8d2b15a0`。两次来源认证不是在同一原内存中重复打分。

## A03 已冻结方法：24真四人组逐一留出，456个完全同目标组轮预测

所有原人一轮贡献`c(i,t)`实际必须为**0..20之间有限整数**，不填缺失、不删除行动、不在群内重组。对每个原四人组g，各完整四人固定合作20轮，定义组公共投入占比`Y(g,t)=sum_4 c(i,t)/80`。每个原组目标t=2..20，共**24×19=456组轮**（不是456个独立实验室样本）。每次把原组g的**全部四人20轮行为**从M0训练剔除，组自己的过去一轮仅被M1合法用于预测下一轮：

- **M0**：其它同一`DF`处理（来源验证每处理确切12组）剩下**11个原组**在相同原实验轮t的真实组均值`Y(h,t)`再平均。源留出g从未参与此条件平均，但其它实验组的目标同期动作已经发生，因此是回顾性组外泛化、**不是日历前瞻预测**。
- **M1**：被预测四人组g刚过去的`Y(g,t−1)`，即四个人过往共同总贡献，不是目标人的私有行动历史单独贡献，也无法区分另外三人的独立效应。
- **M2**：不可调整的固定`0.5 M0 + 0.5 M1`。
- 损失：`(预测投入比−真实投入比)^2`即组均方误差（MSE），为456个同目标等权平均；对应改善 `MSE(M0)−MSE(Mk)`，正值才代表新增历史的预测价值。
- 在真源评分之前冻结“较早t2..5 vs 余下t6..20”，**不能**把此分段与100轮R096的t2..25 vs t26..100视为同一早期比例、同一机制设计。
- 真正独立最小单位为来源24原组；报告两个处理各12组内提升的正负/零数、匿名排序组改善，不虚构把456组轮当456独立实验的p值/95% CI。

真实原CSV的类别`DF`仅核实有两个原始值，本项目按来源字符串排序**匿名称A和B**，没有另独立验证源原始码与论文SF/DF的映射，所以在真人分层报告中不把A直接写“SF”或“DF”。不读原`Type`合作类型，也完全不访问作者原`OtherContri`伙伴贡献源当期聚合，避免假设已经因果区分私人记忆、伙伴历史和反馈信号。

## A03/A04 一手真人真正原组留出结果：强阳性，同时保留两个相反组

**真实源24原四人组、456组轮相同目标的平方误差**：

| 固定模型 | 全24组456目标源真实MSE（低好） | 同目标较M0误差改善 |
|---|---:|---:|
| M0其余11个同类反馈原组同期贡献基线 | **0.0243801993** | 基线 |
| **M1自身原组上一轮投入占比** | **0.0069520970** | **+0.0174281022** |
| M2固定半混合 | 0.0094260079 | +0.0149541913 |

相对M0，M1的原始真实组层面 **22个组有改善、2个组变差、0个完全相等**；原始分层处理A 11/12改善、1/12反例，处理B 11/12改善、1/12反例。这两个真实反例绝不删除、也不能将结果宣传为所有四人组历史绝对优于外部经验。M2在24/24组较M0改善，但在该作者原样样本M1的整体MSE优于M2，**不能在见到效果后改M2权重以“提升模型”**。

两个匿名原反馈处理下结果分别：
| 类别 | 原组数 | 真实t2..20组轮数 | M0 MSE | M1 MSE | M2 MSE | M1较M0改善 | M2较M0改善 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 匿名A | 12 | 228 | 0.0246934809 | 0.0061554276 | 0.0092261326 | **+0.0185380532** | +0.0154673482 |
| 匿名B | 12 | 228 | 0.0240669177 | 0.0077487664 | 0.0096258833 | **+0.0163181512** | +0.0144410344 |

冻结轮段下，A的M1早期改善**+0.02428418**、后期**+0.01700575**；B的M1早期**+0.01697381**、后期**+0.01614331**，均为正，但分段目标各只有每处理48与180个，**不可据此建立心理学习阶段的普遍时间动态或显著性**。原论文讨论冗余历史反馈对人类合作的信号作用，本研究仅检验已冻结的组均值预测，不是复现其反馈因果识别，更不能拿组间MSE直接证明信号/信任的心理机制。

## A04/A05 与其它研究结果的严格区分

R095另一实验室2020年的双人两轮Friend/Foe（8原session×96人）在真完整session-LOSO下历史M1相对M0**8/8实验室场次为负**；R096另一团队2022年的100轮双人囚徒困境（12真session×188人）中，固定对手FP组个人上轮历史在6/6实验室场次有优势、随机对手SP仅3正3负并且早期为负；R099本次2024独立实验是**四人固定组合的连续贡献**，而且LOOG单位**组而非独立实验session**，故不同结果应作为条件性理论的界限证据，而不是元分析意义上可直接合并的三个同一参数效应。R097 E0 OSF源不可得和R098 E1 MAT文件真实哈希认证但无法读取完整源，**都不是正负模型结果**。

这项组历史预测优势可能来自各组稳定平均投入的异质性、自相关、参与者相互影响、反馈结构、回合趋向或其它共同制度约束；仅凭M1优于M0**无法**单独识别学习心理、伙伴信任、策略互惠、因果反馈作用。不能自称复现原R073冻结的个体历史+对手历史完整模型；R099只复用M0/M1/M2结构和严格来源留出评分，不是在另一实验中毫无修改应用原R073完整参数/规则。无新招募E3与长期历史尺度动态结论。

## A01–A06 最终有界验收

- **A01 PASS_BOUNDED**：独立2024原论文团队、可操作的新四人组贡献问题、纯组外同期/历史/半混合既往模型，来源真实行动计分前冻结。
- **A02 PASS**：整份官方PLOS S1 CSV固定签发存储对象可下载、43,467字节及完全SHA、96人20轮/24真实固定4人组来源非行为审核，两个反馈类别各12组。**真实原实验室8个session源码归属未建立**仍是有界证据负口。
- **A03 PASS**：90纯synthetic先成功，再两次各完整原PLOS下载和全96人1,920行动实际456组轮LOOG真实E2、独立匿名JSON字节及SHA精确重演。
- **A04 PASS**：首次PLOS签发存储重定向严格拒绝未冒充真结果，后来单独先冻结有限验证修正；24组中M1两反例真实保留、无经过样本外失利后调参。
- **A05 PASS_BOUNDED**：只宣称源原作者2024固定四人组LOOG的**回顾性E2**，不是作者8实验室session-LOSO、独立来源盲法前瞻E3、原作者论文反馈因果效应复现、R073全部特征同合同或100轮同一行为任务。
- **A06 PASS**：Phase A、A2、B、C前置冻结协议、原数据来源和严格哈希、真实Source/LOOG代码、90synthetic、双CI及原始匿名正负汇总JSON、正式科学报告、机器验收和项目根索引版本均已GitHub main归档与核验。

**`R099=CLOSED_BOUNDED`，`R099_FIRST_PARTY_ORIGINAL_E2_4P_LOOG=YES`，`R099_GROUP_LEVEL_HISTORY_GAINS_M1=22_POSITIVE_2_NEGATIVE`，`R099_ORIGINAL_FULL_SESSION_LOSO=NOT_ESTABLISHED`，`PESEN_v0.1=FROZEN`。**

**R100优先跨实验统一预测“固定伙伴 vs 随机换伴 × 短轮/长轮 × 单人与团体行动”的设计约束和证据等级矩阵**，寻求具原实验室`session`真实字段的独立合作资料在同目标行为下检验对手历史是否提供**超出自己历史**的额外预测价值。不要在R099同一96名真人继续调权重或过度复杂化。
