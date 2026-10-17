# R096正式科学报告：2022年长重复囚徒困境中，自身过去行动的预测优势依赖固定伙伴及互动阶段

**2026-10-17。研究状态 `R096=CLOSED_BOUNDED`。真实原实验12个独立场次、188名真人×100轮，严格完整留出实验场次的 E2 回顾性预测已执行并经原作者固定源码两次独立复算。PESEN v0.1仍FROZEN。** 本报告保留早期负面结果、初始原始下载权限失败、作者源格式校验拒绝、来源不同版本以及统计/因果边界，不宣称实验室前瞻E3。

## 一、独立真人原实验与严格来源区别

Eladio Montero-Porras, Jelena Grujić, Elias Fernández Domingos and Tom Lenaerts, [*Inferring strategies from observations in long iterated Prisoner’s dilemma experiments*](https://doi.org/10.1038/s41598-022-11654-2), *Scientific Reports* 12:7589 (2022)。比利时Vrije Universiteit Brussel 的实验经济学实验室，原论文报告12次现场实验、188真人、100轮重复囚徒困境，固定对手FP六session 92人、每轮随机换对手SP六session 96人；受试者并未获知100轮确切结束时间，文中研究100轮的合作策略动态。

一手论文所列主要数据来源[Dryad正式 DOI 10.5061/dryad.37pvmcvmk](https://datadryad.org/dataset/doi:10.5061/dryad.37pvmcvmk)，`fix.csv`,`rand.csv`官方读取接口在首次[GitHub Actions 39022157694](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39022157694)及网页中为`HTTP403`，另一官方 API`HTTP401`。**从未读取、核验Dryad原始文件本身的SHA或字节；严禁宣称模型数据与Dryad发布文件逐字节相同。**

替代来自**同一原论文作者的正式研究代码仓库**：[eladiomontero/PairwiseStrategies](https://github.com/eladiomontero/PairwiseStrategies)，作者[Zenodo正式代码归档 10.5281/zenodo.5765504](https://zenodo.org/records/5765504)可追溯。锁定原作者提交tag `submission` → 精确commit **`4743f74d8a03a031b8f70aff64956f8ad5155182`**。Git源数据含预计算的`context`、`prev`等派生列，比Dryad网页显示大小不同，是**作者一手研究代码仓库中的后处理CSV**，非证明最早采集的完全原件。本研究没有使用派生的未来/策略结果列。

| 一手作者原Git文件 | 字节 | 经Git tree锁定Git blob SHA1 | 原文件完整SHA256 | 实核人物轮 |
|---|---:|---|---|---:|
| `fix.csv` | 988279 | `3bf78bf85f6642afee18d6f1965dca7272582f40` | `c2adc0d68dbc15c4f5ec5f0eb9a05a988cc049a9c086b82f796521a642b6eae9` | 9200 |
| `rand.csv` | 1112614 | `f5a86cd033b739da45d3fc7c5019068f612146a2` | `bc2999d6ad44c60f2b93361eb46b75614b1f600967ae061c76ae51184a80848a` | 9600 |

每次计算重新获取作者固定commit的整文件，先校验字节数、作者Git blob `SHA1(blob <size>\0<raw>)`与原件SHA256，再读取原来源，故能明确说明**本项目实际执行了哪些原作者版本字节**。

## 二、A01/A02：分阶段在实际行为计分之前独立冻结

阶段来源不可混称为结果：
1. [Phase A Dryad来源门槛](../../protocols/R096_MONTERO_PORRAS_2022_12_SESSION_100_ROUND_ORIGINAL_DRYAD_SOURCE_ACCESS_AND_SCHEMA_FREEZE_2026-10-17.md)，[23synthetic全部通过，Dryad真下载 403/401 失败CI39022157694](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39022157694)，**零人类行为评分**。
2. [Phase B作者Git原论文固tag+两个Git blob的身份/表头冻结](../../protocols/R096_PHASE_B_ORIGINAL_AUTHOR_GITHUB_PAIRWISESTRATEGIES_FIXED_SUBMISSION_GIT_BLOBS_PRESCORE_FREEZE_2026-10-17.md)。首次原作者实源表头含未命名pandas索引被严格拒绝，[首次CI39022585556](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39022585556)。随后[Phase B2仅修原作者CSV匿名表头索引识别](../../protocols/R096_PHASE_B2_ORIGINAL_AUTHOR_GIT_CSV_UNNAMED_INDEX_HEADER_ONLY_REPAIR_FREEZE_2026-10-17.md)，合成测试本身也有一项行宽fixture错误而失败；只修测试形状不降低原文件合法检验，在[CI39022889186](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39022889186)获得**50synthetic与源全Git blob双认证成功**，fix=9200行24列、rand=9600行25列。
3. [Phase C身份证明与真实session非行为审计冻结](../../protocols/R096_PHASE_C_MONTERO_2022_AUTHOR_FP_SP_SESSION_PLAYER_100ROUND_NONBEHAVIOR_ROSTER_FREEZE_2026-10-17.md)，[CI39023131299](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39023131299) **65synthetic与真实原作者12场次来源结构全成功**：固定FP 6真session 人数**[8,14,16,18,18,18]**共92人，全100轮partner不变；随机SP 6真session **[10,16,16,18,18,18]**共96人，96人都存在历史对手变化。每人严格有第1至100轮记录，`session×player×round`唯一，实核18,800人物轮。任何动作列均**没有**在本阶段读取。
4. [Phase D实际二元模型冻结](../../protocols/R096_PHASE_D_2022_MONTERO_12_TRUE_SESSIONS_188_HUMANS_100_ROUND_BINARY_SESSION_LOSO_M012_SCORE_FREEZE_2026-10-17.md)，首次[98synthetic全PASS、真来源严格编码拒绝CI39023515492](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39023515492)，因为原作者原CSV并非初始假设的数字0/1，而是字母行动码；**此轮没有可接受真人Brier分数**。
5. 单独先冻结[Phase D2真实作者行为编码“类别”审计而非模型成绩](../../protocols/R096_PHASE_D2_ORIGINAL_AUTHOR_BINARY_ACTION_CODEBOOK_REJECTION_AND_LITERAL_CLASS_AUDIT_FREEZE_2026-10-17.md)，[CI39023662426](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39023662426)11synthetic+实源完整SHA通过；确认FP行为码仅C 5161、D 4039；SP仅C 2738、D 6862，原自/对手原字段两类合计一致，没有未知或遗漏。原论文明确使用C=cooperate、D=defect，不依据预测分数做模型选取。
6. 在新的真人成绩计分之前独立提交[Phase D3仅C→1、D→0来源码本映射修正](../../protocols/R096_PHASE_D3_C_TO_1_D_TO_0_AUTHOR_ORIGINAL_CODEBOOK_ONLY_AMENDMENT_BEFORE_REAL_SCORE_2026-10-17.md)，**M0/M1/M2、整场次留出、平方损失和样本资格绝未改变**。编码后旧synthetic中的“C应失败”断言变得过时，先完整保留[CI39023767024](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39023767024)该synthetic失败再改为测试未知原码拒绝。[首份真正原作者188人全部二元行为E2 CI39023796827](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39023796827) **110合成全PASS + 真人18800来源行动/对手一致性检查 +18612真下一轮原人评分成功**。

本项目没有根据见到的真实损失反向拟合模型、优化混合权重或抛弃负面阶段。初始真源下载、表头、源编码和过时synthetic失败都按时间独立保留。

## 三、A03：完整留出真实实验场次的三个无参数预测模型

每个FP或SP处理含6个**真实不同实验室场次**。逐一留出目标场次S（8—18真人的**全部100轮**不进入基线M0），其余5个相同处理来源场次做训练；目标人i的100轮源记录严格有C/D，原对手`action_opponent`每轮与同session真实双人配对对方`action_player`逐一吻合，且全程无任何source缺失或重新编造样本。

对被试i在轮t=2..100：
- `Y(i,t)`=源`action_player=C`记1，否则原D=0；
- **M0** 另外5个独立原实验场次在**同轮t**所有真人C动作之比。对原测试场次整组所有人所有t完全隔离；该同期数据是事后横向可见基线、**不是日历真正前瞻预测**；
- **M1** 被预测者自己的上一轮源C/D（1/0），不使用当轮或未来；真正的第一轮来源历史作为后续t2已知输入；
- **M2** 固定`(M0+M1)/2`，无任何拟合、调参或随来源适配权重。
- 统一Brier损失`(p−Y)^2`，只评估完全相同源目标组，向高提升`L(M0)−L(M1/2)`。
- FP共**92×99=9108**次真下一轮，SP共**96×99=9504**次，总计**18,612个来源真人连续行动目标**；真独立原实验场次只有12个，不是18,612独立样本。事前固定 EARLY t2—25（24轮）对比 LATER t26—100（75轮），另预先划分t2—25、26—50、51—75、76—100四互斥时段。

原来源个体身份、原场次编号及全100轮轨迹不发布，只发表匿名真实6session损失的排序列表、每处理正负场次数和完整项目层宏统计。

## 四、真实结果：固定伙伴的个人历史预测优势显著强于随机换伙伴，早/晚效果异质

**实验双方源合作编码已核对、是真人实验原作者代码仓库的全部18,800合法源行动；实际18,612下一轮同目标配对Brier。**

| 固定预声明模型 | 全部18,612 Brier低好 | FP固定伙伴9,108 | SP随机伙伴9,504 |
|---|---:|---:|---:|
| M0 其它五个真实独立session同轮合作率 | 0.2282497625 | 0.2522879362 | 0.2052131793 |
| M1 本人上一轮原源C/D | 0.1678486998 | 0.1389986825 | 0.1954966330 |
| M2 固定M0/M1各半 | **0.1409460375** | **0.1325538528** | **0.1489885479** |
| **M1相对M0改善** | **+0.0604010627** | **+0.1132892537** | **+0.0097165463** |
| **M2相对M0改善** | **+0.0873037250** | **+0.1197340834** | **+0.0562246315** |

**真原独立实验室session的方向异质，不能只盯全部池化：**FP的M1较M0改善**6/6正、0负**，M2也**6/6正**；SP中M1只有**3正、3负**，M2**6正、0负**。随机配对场次原个人历史单独预测不稳定，固定二者半混合则在所有12个来源session总平均正。不能在12个场次尚无多源独立复制时宣布因果普遍规律。

| 事前冻结时段 | FP M1对M0改善 | FP M2对M0改善 | SP M1对M0改善 | SP M2对M0改善 |
|---|---:|---:|---:|---:|
| **EARLY 第2—25轮** | +0.0009861683 | +0.0648092649 | **−0.0419386656** | +0.0338432057 |
| **LATER 第26—100轮** | **+0.1492262410** | +0.1373100253 | +0.0262462141 | +0.0633866877 |

上述为预冻结时间分段的**描述性异质**。固定伙伴的历史直接延续M1在晚期表现强烈更好，早期则几乎与其它五原场次同期合作率相同；随机换伴初期直接沿用上次行动比跨场次同期更差，晚期才回正。作者论文认为少于25轮往往只观察到学习阶段的现象，和这里预冻结分段的变化方向相容，但**不能因此将观测差异识别为学习本身的因果效应**。其它混淆因素：不同伙伴稳定性、社交均衡、共同外部时间、结构选取、行为内生互动；源策略context等工程列有历史计算，本项目一概未使用。

## 五、A04/A05：外推、竞争模型、阴性及不确定性

R095是**2020另一作者**96真人在8个真正独立实验室场次中两轮Split/Take All二元游戏，M1相对M0的8个场次**全部负向**，不能用R096长100轮正向结果抹掉R095的真实反证。不同原博弈类型、未知时间终止机制与基础合作率均不同，因此不可用R096−R095简单差值宣称单独验证“轮次越长就必然使人类历史更有预测价值”。R096也不同R073最初完全留出实验场次的特定对手/自己历史模型，**本次R096只复用M0/M1/M2固定比较逻辑，不是假装原样执行R073冻结全部特征/评分合同**。

R096原作者研究场次**n=6/处理**，同一来源场次的人互相配对与对手结构耦合，不做只把188人或18612行当独立样本的伪显著性检验。本研究未在事前冻结实际session bootstrap/permutation检验，故没有编造p值或95%CI。同期M0仍使用其它场次同轮行为，不能做真实时间向前的前瞻预测。这个 E2 是**发表原作者研究代码中可重复的历史回顾性独立场次预测**，不是新实验室招募完全不同人群的E3，也不构成宏观制度/文化历史因果模型证据。

**来源适用边界**：原始实验采集的官方Dryad CSV依旧没有实际下载，原Git数据带来源转换列且与Dryad文件网页大小不同；首次作者Git源字段/数据身份可靠，但还不能声称与未访问Dryad的原件数值逐格一致。

## 六、A03/A06：两次独立真人原作者整源再次获取与Git结题

[首次真人全二元评分 CI39023796827](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39023796827) 110项原来源、对手伙伴真实性、编码反向对称性及竞争模型synthetic全PASS，真实12个session 18800动作逐一校验后**18,612下一轮源真实模型成绩**PASS，首次匿名真实结果**11,133字节** SHA256 **`3aae5d183a33cce37a16d0637b2b887fb106a2b7432d8c8151b9a2dfafe452c2`**。

[第二次全部原作者两Git blob+SHA全文重新独立下载复算、110synthetic、全部18,612真实目标字节严格一致、匿名结果永久Git提交CI39023880006](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39023880006) **SUCCESS**，生成完全相同11,133字节 SHA256，提交[正式真实源结果JSON](R096_MONTERO_2022_188_HUMANS_12_TRUE_SESSIONS_100ROUND_FPSP_BINARY_LOSO_E2_RESULTS.json)，Git blob **`1d98ceadcca53d6c09754ff0d2207dd99e8ee2f3`**。既往Phase A Dryad HTTP拒绝、Phase B原索引列表头失败/过时synthetic、Phase D数值源代码拒绝、Phase D3旧synthetic拒绝均被保留为可核验的技术负记录。仅原作者匿名研究宏数据入项目公开Git库，不含个人session/ID/选择序列。

详细[来源访问源程序](r096_montero_2022_original_dryad_100round_FP_SP_source_gate.py)、[固定第一手Git blob源审计程序](r096_phase_b_montero_author_git_tag_pinned_original_FP_SP_CSV_source.py)、[12场次真源组织结构](r096_phase_c_original_2022_author_fp_sp_six_true_sessions_roster.py)、[独立安全原作者C/D行动码本](r096_phase_d2_original_author_action_codebook_classes_no_scores.py)、[M0/M1/M2原作者188人100轮12session真实预测程序](r096_montero_2022_188_humans_12_true_sessions_100round_FPSP_LOSO_E2.py)、对应各阶段合成测试及全部CI和先期冻结协议，归档GitHub main。

## 七、A01–A06有界正式结题与后续

A01真正原作者长100轮FP/SP两处理，前期问题/预测器/评分冻结，**PASS_BOUNDED**；A02作者固定论文代码Git blob的原始字节/两个完整SHA及12个真正源实验室session与188人×100轮结构逐一验证，**PASS**；A03完整110synthetic和两次完整来源复算全部18,612真人二元行动一致，并精确结果SHA，**PASS**；A04Dryad权限失败、作者索引格式失败、最初未映射C/D行为编码拒绝、真实随机伙伴早期M1负向/3session负向与R095全部8session阴性公开保留，**PASS**；A05仅追溯性原作者处理源码E2，未证实跟Dryad官方原始CSV逐字节相同、未进行新增不同实验室前瞻E3或因果随机化检验，**PASS_BOUNDED**；A06所有前置独立冻结协议、全源码、原作者双真实源匿名得分、正式科学报告、机器验收、GitHub main/root导航核验，**PASS**。

**`R096=CLOSED_BOUNDED`，`TRUE_ORIGINAL_12_SESSION_100ROUND_LOSO=YES`，`FIXED_PARTNERS_OWN_LAG_GAIN_POSITIVE_ALL_6`，`SHUFFLED_EARLY_LAG_GAIN_NEGATIVE`，`R095_NEGATIVE_RETAINED`，`ORIGINAL_DRYAD_RAW_BYTE_IDENTITY_NOT_PROVEN`，`PESEN v0.1=FROZEN`。**

下阶段优先在**另一实验室**长期二元游戏或更换信息制度研究中冻结相同M0/M1/M2与前25轮/后期分段，检验“历史信息价值依赖真实交互伙伴稳定性”的条件性预测规律能否复现。避免在这188人上继续调整比例、引入未经实验间验证的任意复杂度。
