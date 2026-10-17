# R077 — 第四独立原作者真人重复博弈：首次评分前修订、零目标拟合数值迁移及边界反例

**日期：** 2026-10-17  
**归档状态：** `CLOSED_BOUNDED`，A01–A06 按有限范围验收；本项不是对全世界行为机制的因果验证，也不是数据收集前完成注册的前瞻性随机试验。  
**证据级别：** 来自不同原作者的独立真人实验新总体上的来源参数固定验证（E3，**仅就事先于本研究第四样本模型评分确定的评价方法而言**；原始实验是2025年已经发表的研究，研究者已阅读论文总体结论）。  
**主模型状态：** `PESEN v0.1=FROZEN`，R073 M0–M6 的定义和参数常数未更改。

## A01 研究问题与合格范围

在从未使用第四真人实验行动标签拟合任何参数的前提下：**仅把R073 Montero-Porras 2022全部12原始session上的固定数值条件概率搬到第四名实验作者独立收集的真人重复囚徒困境数据中，上一轮双方实际行动能否比仅本人上轮行动更好预测下一步合作？更进一步的两轮历史是否持续改善？**

第四真实来源为 Drouvelis & Pearce（2025），*Intelligence and strategy choice in indefinitely repeated prisoner's dilemma games: A replication of Proto, Rustichini & Sofianos (2022)*，*European Economic Review* 178,105075，[论文 DOI](https://doi.org/10.1016/j.euroecorev.2025.105075)。本研究不检验论文的智力差异、策略识别误差理论、信任机制，也不把原文中需要另外下载的 Proto et al. 原始样本并入第四作者自己收集的新人类总体。作者在 [Zenodo v1，DOI 10.5281/zenodo.15462528](https://zenodo.org/records/15462528) 提供自己的 `cleandata.dta` 和三个 Stata 脚本，明确写明复现完整原研究时还需要原论文数据——本项只使用本研究作者的 `cleandata.dta`，不使用前人原始数据。

## A02 真实来源和完全固定的资料边界

原作者发布 `cleandata.dta`，精确大小 **1,514,315 bytes**，MD5 `4cce04ea68b7a0492c242b206efebe53`（与 Zenodo 官方元数据逐字一致），SHA256 `1cc9a4f68a51992808d966b118226bb5a66ee3ee6054843a132157df8eeb1985`。其中3620条确实存在的真人合作/背叛行动、15个原始 `Session`、260个唯一场次内人物身份、1,810个真正双人互动轮、1440个真人参与者×game组合；两个原本处理组有7与8场次。

实际原作者 `number 2.do`（MD5 `563263f55bb3a7a1910b3b38e85fe22c`）及来源行为变量支持 `left=1` 是本人合作、`left=0` 是本人背叛，`otherleft` 记录对方实际动作。身份 `Session+Subject` 和 `Session+Subject+game` 的局内索引独立核验，15场不能被另一个 `sessionid` 字段所含26种数值错误放大为26场。1,810个 `Session,treatment,Period,Group` 双人单轮小组全部恰两人，双方 `otherleft` 均与对手真实 `left` 严格互证，未发现当轮对手标签错置。

前两轮历史共同风险集严格使用 **同一 Session、Subject、game** 中连续存在的 `practiceperiod=t,t−1,t−2`，总共 **1,040次下一轮选择**，不跨局串联。风险集数量在任何模型得分出现之前已通过独立仅做结构审计的[CI 38994709254](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38994709254)确认，是真人来源数据不是合成事件。

**未完全证明的含义：** `otherleft` 的确是实际对手做出的动作，且前一轮较当前早发生，作者统计分析也使用上一轮 `otherleft`；但跨轮换伙伴时参与者**是否实际在每轮完整收到该反馈**，没有单独核对实验客户端每项展示日志。本研究仅能把它称为可从原作者行为记录复原的既往对手行动，不得自动称为经独立核实的心理信息集，也不允许识别“同一对手回馈”。

## A03 冻结模型、执行与复现

主唯一donor为 `R073_ALL_12_POOLED`，Montero-Porras 2022 原始12场、188位受试者、18424个t≥3完整来源条件频率，源仓库固定提交 `4743f74d8a03a031b8f70aff64956f8ad5155182`，fix/rand Git blob分别 `3bf78bf85f6642afee18d6f1965dca7272582f40` / `f5a86cd033b739da45d3fc7c5019068f612146a2`。直接复用 R073 七个模型 `M0_TREATMENT_PREVALENCE`、`M1_OWN_LAST`、`M2_OPPONENT_LAST`、`M3_JOINT_LAST`、`M4_JOINT_TWO_LAGS`、`M5_TFT_NOISY`、`M6_WSLS_NOISY`，原模型 Git blob `c8a0b47fd27bf05e7be5b87419a0824355fc911a`，先验平滑 alpha=20，TFT/WSLS 的固定理论错误率0.05。对 R077 **零条真人标签用于来源/目标拟合，也不根据目标合作率重新校准p0**。

七模型对完全相同的1040个目标事件评估 Brier 和 log loss，每个来源完整场次内平均，再15个真实session**等权**；处理0的7场、处理1的8场分别等权。六项固定配对 Brier 比较，不事后决定最佳单组、不筛掉配对重组情形。

### 七模型全部实际结果

| 冻结模型 | 15场等权 Brier ↓ | 15场等权 log loss ↓ | 处理0 Brier (7场) | 处理1 Brier (8场) |
|---|---:|---:|---:|---:|
| M0 同源训练合作率 | 0.224580 | 0.641904 | 0.239880 | 0.211192 |
| M1 上轮本人 | 0.151140 | 0.475515 | 0.157064 | 0.145956 |
| M2 上轮对手 | 0.155817 | 0.491324 | 0.145470 | 0.164871 |
| M3 上轮双方联合 | 0.120929 | 0.392645 | 0.124171 | 0.118092 |
| M4 前两轮双方联合 | **0.119010** | **0.384311** | **0.120530** | **0.117680** |
| M5 固定TFT | 0.177250 | 0.623005 | 0.143125 | 0.207109 |
| M6 固定WSLS | 0.512500 | 1.719809 | 0.459732 | 0.558672 |

### 事先指定的六项对比与反证（负数表示左侧更好）

| 左侧−右侧模型 | 15场等权 Brier 差 | 改善/持平/恶化场数 | 处理0差值 | 处理1差值 |
|---|---:|---|---:|---:|
| M3−M1 **主要** | **−0.030211** | **14/0/1** | −0.032893（7/7好） | −0.027864（7/8好） |
| M4−M3 **主要** | **−0.001919** | **8/0/7** | −0.003641（5/7好） | −0.000412（3/8好） |
| M1−M0 | −0.073440 | 12/0/3 | −0.082816 | −0.065237 |
| M2−M0 | −0.068762 | 13/0/2 | −0.094410 | −0.046321 |
| M5−M0 | −0.047330 | 10/0/5 | −0.096755 | −0.004083 |
| M6−M0 | **+0.287920** | **1/0/14** | +0.219852 | +0.347480 |

“提高合作预测表现”仅是**评估的条件概率和损失**改进，不能将固定TFT/WSLS值误解为回收了真实人的行动策略，也不把来自重复行为的1040个事件视为1040个独立实验样本。

### 实际运行顺序与可审计复现

- [原作者公开资料哈希/格式 38994451948](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38994451948) PASS；[原作者Stata源码字段语义 38994561545](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38994561545) PASS；
- [原始配对与时间结构 38994709254](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38994709254) PASS；[发生配对问题后的不评分精细审计 38995148912](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38995148912) PASS；
- **原先冻结的 Rev-001 [协议](../../protocols/R077_ZENODO_FOURTH_AUTHOR_TRUE_HUMAN_PROSPECTIVE_MODEL_SCORE_FREEZE_2026-10-17.md)** 已在任何真人模型分数出现之前存在，但其配对不变和每人局内完整从t1观测的资格要求在真实数据不成立。[CI 38994977281](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38994977281) / [38995038132](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38995038132) 真人分数均**无**，严格FAIL-CLOSED。随后查明处理1出现130次相邻 `Group` 改变、80个人局缺完整从t1开头序列（仍可逐个t核验t−1/t−2）；
- 在读取任何真人 M0–M6 得分之前明确另交 [Rev-002 来源语义修订协议](../../protocols/R077_PRE_FIRST_TARGET_MODEL_SCORE_SOURCE_SEMANTICS_AMENDMENT_REV002_2026-10-17.md)，冻结提交 `f79d59175098b4314c9c784394cfd5beb8083f2e`，只允许上一轮已真实发生的对手反馈、严格完整相邻两历史，**没有调参/改目标/挑模型/丢弃重组处理**。[CI 38995298362](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38995298362) 因过渡状态的合成测试断言未更新而在任何真人评分前失败；
- 更新同步后，[首次真正真人七模型评分 CI 38995309336](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38995309336) 两job SUCCESS（**24项合成守卫**先PASS、随后真人1040次实际评分），完全匿名结果9,835 bytes，SHA256 `8d8b8413e3e55cb5d856f34b873ee20c2ba470e04190bb8577f931d25ba509a4`；
- [完全独立重新下载、重算、逐字节同HASH永久Git归档 CI 38995401729](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38995401729) SUCCESS。匿名原始JSON [R077_FOURTH_INDEPENDENT_HUMAN_SOURCE_ONLY_E3_RESULTS.json](R077_FOURTH_INDEPENDENT_HUMAN_SOURCE_ONLY_E3_RESULTS.json)，Git blob `13946754afc06e529f2d3a2072a7bae297453fa9`。所有原作者行和具体单人、session编号以及逐场得分只在临时CI runner读取，不进入repo。

## A04 失败、不稳定和负结果

1. Rev-001严格完整性门在真实样本 **FAIL**，没有授权放宽后伪装“原协议通过”。Rev-002的风险集明确限定同一个人、同一局两轮完整历史，实际存在重匹配，不能宣称同一伙伴行为惯性已获证实。
2. M3仅14/15完整场次优于M1；M4只有8/15优于M3，**7场反例**，其中会发生重新分组的处理1仅3/8场改善，更长记忆优势很弱且不稳定。
3. 理论固定 WSLS 在15场中14场劣于简单来源合作率M0，均值 Brier +0.287920，反证简单固定策略作为总体预测器的普遍有效性。
4. t≥3规则条件性选择在局内活到第三轮且有完整两轮观察的行为，不等于所有新参与者或全部起始回合。

## A05 科学推断与适用边界

本次目标是第四项新原作者真实人群，不与先前 R073/R074/R075 数据集重复；但论文及其总体结论发表于2025年，原始研究不是为本R计划招募的新实验，也不是实施前登记的临床式前瞻研究；**只能声称“在第四份此前未被我们的七模型打分的独立原作者实验中，于实际打分之前冻结的零样本预测”，不能声称新收集的真正前瞻队列**。对原始 `otherleft` 的历史信息本人是否完整看到、实际独立人群跨session重返、同一参与者是否看到另一局的数据，都需要原作者实验实施日志才能充分核验。

跨四独立研究的共同有限现象是，上一轮本人+对手的**行为历史变量**通常比只用本人上一轮更有预测力；这不识别社会反馈的因果处理效应、人的实际记忆机制、规范形成、不代表社会制度级或百年历史预测正确。两轮历史价值对实验处理、拟合来源敏感，R074 和 R076 的负结果均不得删除，绝不在R077真人打分后更新R073模型以反向提升该验证样本成绩。

## A06 结题与继续研究

A01 PASS（问题与唯一donor预定），A02 PASS（合法公开作者原始来源和fixed hashes），A03 PASS（24合成、真实GH Actions、二次SHA精确重放），A04 PASS（**记录FAIL而非将其抹掉**；两次初始资格失败及7场M4反例、14场WSLS反例永久保留），A05 PASS（第四既存实验与新建前瞻队列分开），A06 PASS（最终报告、原始匿名JSON、接受状态、GitHub主分支可核验）。这种 PASS 为**本报告对审计义务的通过**，并不表示初始数据门 Rev-001 PASS 或社会科学假设获得因果证明。

`R077=CLOSED_BOUNDED`  
`FOURTH_INDEPENDENT_HUMAN_SOURCE_ONLY_E3=COMPUTED_AND_SHA_REPLAYED`  
`R077_REV001_ELIGIBILITY_GATE=FAIL_RETAINED`  
`R077_REV002_PRE_FIRST_REAL_SCORE=FROZEN`  
`TARGET_LABELS_IN_FITTING=0`  
`M3_MINUS_M1_BRIER=-0.030210760470721517`  
`M4_MINUS_M3_BRIER=-0.001918699476466503`  
`M4_NEGATIVE_SESSIONS=7/15`  
`PESEN_v0.1=FROZEN`

**后续研究入口：** 新立 R078，在跨四研究结果已知的前提下预先冻结机制竞争模型和多层连接方案，并以另一独立真人实验或明示回顾性探索区分“可观测历史预测”与“可识别认知机制”。不得对已用于决定方向的R077数据进行隐形超参数择优。
