# R095 正式科学报告：八个原实验真实场次全部留出下，短期个人行动惯性预测优势未复现

2026-10-17。**R095=CLOSED_BOUNDED，真正新的独立实验室原作者首方人类二元重复博弈，八个原始实验场次可验证、逐一完整留出真实E2；M1在8/8场次对M0负向，是必须保留的重要原始实证阴性。** 同时注意，这不是与R089六人阈值公共品、R094网络公共品完全同一行为或游戏规则，不能用来推翻其各自的有界结果；非前瞻E3，不能推断历史长程机制。PESEN v0.1 FROZEN。

## A01 独立研究问题与严谨的真实性

Eric Schniter / Timothy Shields，2020 [*Participant Faces from a Repeated Prisoner's Dilemma*](https://zenodo.org/records/4321821)，原实验室Chapman University Friend-or-Foe变体的重复双人囚徒困境。原作者以学生为真人被试，匿名随机组成稳定双人配对，每人每轮亲自选“**Split**”（二元合作）或“**Take All**”（二元背叛），并在每轮后看见双方互动结果。原网页说明最少两轮，部分实验三轮。论文外的摄影、面部数据和调查年龄等**一律不接入研究项目**。

本次源文件不是后来研究者整理的二次数据：原作者公开[Zenodo v1 DOI 10.5281/zenodo.4321821](https://zenodo.org/records/4321821) 中 `Fields.csv` 及独立 `Fields_codebook.csv`，码本真实定义了 `ID`原参加者、`round`原轮次、`option`真实行动、`session`真实实验室场次、`group`真实固定双人配对、`other_split`原对手真实合作/背叛报告。原文上视频与情绪数据不作为自变量、标签或拟合目标，也未触及受限`MappingFile.csv`。

最重要区别：此前R094尽管原论文有80网络场次，次级CSV没`session_id`，无法实现真LOSO；本次数据**原作者的`session`列明确存在且独立实际验证**，首次在本组R089–R095对比线索中得到额外一个真正按实验室**场次**完整留出的新作者二元合作评估，与R073最初“整场次”检验设计思想更接近。

## A01/A02 不夸大预注册——网页预览曾暴露若干真实行动行

**明示方法限制：**在发现Zenodo公开源时，来源网页的`Fields.csv`预览意外展示了部分实际`option`选择行。因此原研究员在运行本项目原始行为评分之前，已接触过小部分原始行动，**不能对R095主张“完全事前盲法”的预注册**。正确描述是：**研究模型形式M0/M1/M2已在R089—R094时期冻结复用，并在第一次以程序计算R095全样本真预测之前单独提交了本来源的八场次完整留出协议。** 不以“完全没有看过任何结果”提高科学级别；E2严格回顾性结果仅作有限外部比较。

[Phase A源文件与组/场次资格协议](../../protocols/R095_SCHNITER_SHIELDS_ORIGINAL_2020_ZENODO_FRIEND_OR_FOE_SESSION_LOSO_SOURCE_GATE_2026-10-17.md)首个提交`2fc89465570f30cc94c3deaaa34376bf3943029d`，早于程序读取任何人类实际行动。原著第一手`Fields.csv`作者Zenodo公布MD5 **`4c30ac1861e12f46e0b9847c9d1857a7`**，完整原文件**22,312字节**，本项目先核实MD5再算来源SHA256 **`0678cc3d565d3a02e4766fedff211cc37b2e0e9d373e41c391466c6f84a56f4c`**。作者码本MD5 **`832565bb440c08c328ac0db0f16a0aac`** 是出版元数据，在项目未下载该码本单独作实际MD5复算，需区分码本网页证据与源CSV自身的严格字节校验。

[第一份实际真正源文件MD5身份、source roster但不读`option`的真实CI39020885386](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39020885386) **25项全合成+作者文件完整来源格式及独立现实群组数据核验success**。身份得到：
- **8个真正源实验室session**，每场次**12个互不重复被试**、每场次6对固定双人小组，原实验总**96人、48对真实匹配**；
- 各原人1、2轮完整且在原`session×group`中配对身份不变，实际原版CSV共**204人轮**（1轮96、2轮96、3轮仅12，即第三轮只存在一个真实session且6个原配对完整）；
- 严格跨场次身份证明与人口分母来源齐全，不通过人号前缀/文件顺序猜原场次。第三轮由于另外七个场次没有合法对比训练轮次，正式预先固定**不计入预测测试、也不作为训练资料**。

## A03 原来源真实选择读取前已固定的完整实验场次二元模型

正式[Phase C八场次LOSO真预测协议](../../protocols/R095_PHASE_C_SCHNITER_SHIELDS_8_REAL_2020_LAB_SESSIONS_96_BINARY_ROUND2_LOSO_M012_FREEZE_2026-10-17.md) commit`a9815804dd95859cee9c75e61c2c5e3df573eaf0`，由主项目R089—R094长期沿用的原样三组竞争模型，**未因数据正负结果重新调整任何权重或试验条件**。本次固定的预测目标恰好96个真实真人第二轮二元选择，Split=1，Take All=0，缺失/非此二元码全来源拒绝。作者源`other_split`按原双人组核验确与另一方的原实际二元行动一致（两轮48对配对、完整96个group-round观察），不是将`other_split`当预测特征。

对一个留出真实实验室session S的12个人中的i：
- M0＝**所有另外7个完整独立实验室session的84人第二轮真实合作比例**；训练不含S的任何一人、任何一轮选择，原全场次确实被隔离。这是完全原场次划分上的**跨场次留出测试**，但不同实验室场次在既往同周期发生，不是严格日历实时向前预测；
- M1＝留出S中目标i的**第一轮自己真实选择（0/1）**，这是第二轮预测时已知的个人既往行为，允许本组自己的历史，而并非完全未见过该组历史；
- M2＝严格固定50% M0 + 50% M1；
- 所有模型预测同96个人的t=2，标准Brier `(p−y)^2`。每个S的12人先聚合为场次改善，汇报**8个真场次的差值符号**，严格不把96人/204人轮当96或204个独立实验室场次。没有预冻结有效聚类bootstrap或多场次因果随机化检验，不给虚构p值/置信区间。

## A03/A04 真实阴性实证：8/8原实验室场次历史M1均不敌跨场次均值

第一份真实原作者8个真实原实验室场次整体留出输出与第二份原作者重新下载、精确全CSV验证和匿名输出逐字节相同，可信为**实际96名真人二元合作数据，非合成测试或未拟合烟测**：

| 已冻结预测器，全部96个第二轮原行动 | 真实Brier平均误差（低越优） | 相比M0同人目标误差改善M0−Mk |
|---|---:|---:|
| **M0跨场次另外84人当轮合作率** | **0.2521789966** | 基线 |
| **M1本人第一轮行动** | **0.3958333333** | **−0.1436543367（负）** |
| **M2固定0.5M0 + 0.5M1** | 0.2646196499 | **−0.0124406533（负）** |

- **真正独立实验室session层**：M1相对M0平均改善的8场次符号**0正、8负、0完全相等**。来源匿名按改善值排序的八个原场次差值（仅宏数据，不绑定原来源session标签）：`[−0.253401,−0.170068,−0.165391,−0.156463,−0.156463,−0.087160,−0.087160,−0.073129]`。一个正例都没有，不能以“某些个人可能改进”抹掉全部场次阴性。
- M2相对M0改善有**3场次正、5场次负**，均值轻度为负，说明并不是任何将个体历史加入外部场次信息的固定组合都必然提高表现。
- 源实测二元合作率：**第一次轮71/96=73.9583%**，第二轮**51/96=53.125%**。早期高合作率与第二轮降低可解释为什么直接重复上一轮在此具体短轮次实验中表现不佳，但“被试预期终局”“信任坍塌/信誉演化”“策略演变”等都属于**竞争机制假说，尚无本次因果识别**。实验被试知晓至少两轮，但第三轮只一个场次，存在实验长度与主体样本独特性，不外推至100轮固定/随机对手。

这是对模型具有科学意义的**负面边界证据**。以往R089（6人全球公共投资组历史阳性）、R090（气候俱乐部连续合作M1阴性）、R091（4人公共品合作组历史阳性）、R093（14天大型群体个体记录含机械代作历史阳性）、R094（二元网络合作个人历史按财富可见性正负反转）等都严格保留，不要求所有任务具有相同历史作用方向或合并异质目标。**R095当前的真LOSO只证明这个具体2轮友/敌二元游戏与当前冻结基线的可迁移信息不成立**，不能推翻其它任务，不证明个人记忆不存在，更不能推断长历史机制因果。

## A03/A06 完全重复原来源与阴性成果永久Git回放

首次[实际全部25+27=52项合成及原作者本轮数据评分CI39021166964](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39021166964)在真人原件的安全输出路径写入上发生`AttributeError: Namespace.parse_args`，合成成功但**不能核验该次的实际行为最终成果文件**；后仅修正CLI输出`pth=a.output`，严格不修改评分协议或模型。[完整首次成功的人类原作者实际八场次计分CI39021217536](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39021217536) 52synthetic+首方来源SHA+八场次全部真实96二元全部通过，输出匿名汇总**3,021字节**，SHA256 **`f45182131e0ec364fdd34c3eb36cb96f92c14a6db8c35de287dcc6632aea1b63`**。

[第二次实际作者Zenodo原实验资料完整重新下载、源MD5/SHA再验证与52项synthetic独立全复算CI39021289019](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39021289019) **SUCCESS**，原8个真实实验室场次96目标E2输出**字节数、完整SHA256逐字节完全相等**，真实匿名负面成果永久Git提交为[原始E2可复现JSON](R095_SCHNITER_SHIELDS_2020_8_REAL_LAB_SESSIONS_96_BINARY_ROUND2_LOSO_E2_RESULTS.json)，Git blob **`8c43d31eade559da84e0f877b34eff5cead76a9c`**。

构成证据链：[正式阶段A protocol](../../protocols/R095_SCHNITER_SHIELDS_ORIGINAL_2020_ZENODO_FRIEND_OR_FOE_SESSION_LOSO_SOURCE_GATE_2026-10-17.md)、[阶段C行为计分前固定LOSO](../../protocols/R095_PHASE_C_SCHNITER_SHIELDS_8_REAL_2020_LAB_SESSIONS_96_BINARY_ROUND2_LOSO_M012_FREEZE_2026-10-17.md)、[真实首方来源与配对核查程序](r095_schniter_shields_2020_original_session_roster_no_actions.py)、[真正全部96真人二元source评分](r095_schniter_shields_96_humans_8_full_original_sessions_LOSO_E2.py)、[25 source tests](test_r095_schniter_shields_2020_original_session_roster_no_actions.py)、[27 model tests](test_r095_schniter_shields_96_humans_8_full_original_sessions_LOSO_E2.py)、双工作流和完全匿名正式结果文件。绝不上传源原CSV、真人ID、每个人的合作选择、原配对、人口属性、声像内容，也不进行作者媒体与本研究参与者记录身份再识别。

## A01–A06严格限界验收

A01原作者新实验、不同二元行为定义、固定M0/M1/M2、明确公开source网页预览部分真实行动的非完全盲法限制，**PASS_BOUNDED**；A02真实一手发布者MD5+全SHA和8个真独立实验室session、48固定对手双组、96实际完整双轮全资格**PASS**；A03全部52synthetic、真正原作者96次二元预测、两次全原来源独立运行且匿名结果精确逐字节相等**PASS**；A04首次CLI失败、八个session历史M1全部负、五个session的混合M2负、第三轮不得不排除及非完全盲法限制全部保留**PASS**；A05只限于真人已发表原作者实验**回顾性E2**，非心理学习因果/新招募E3、非长实验结果，且与先前来源游戏定义不同**PASS**；A06冻结模型/来源协议、原始代码与synthetic、CI负证据、完整匿名JSON与Git报告/索引**PASS**。

**`R095=CLOSED_BOUNDED`, `M1_TRUE_ORIGINAL_EIGHT_SESSION_LOSO_GAIN=NEGATIVE_IN_ALL_8`, `M2_TRUE_SESSION_LOSO_GAIN=SLIGHTLY_NEGATIVE`, `OVERALL_HISTORY_UNIVERSALISM=REJECTED_AS_EXPLANATION_FOR_ALL_THESE_TASKS` (not a population-statistical theorem), `PESEN v0.1=FROZEN`.** 下一阶段R096优先另一独立原作者**≥6真实可识别场次，≥20轮二元行动**，例如Montero-Porras et al.2022原始Dryad（12个FP/SP场次、188人、100轮），以区分R095这种短博弈终局效应与更长历史依赖，并严格先验证原session ID和公开原数据读取权限。
