# R077 第四独立真人重复囚徒困境一手原作者数据：零样本概率前置评分冻结协议

日期：2026-10-17。首次 R077 第四实验**任何七模型真人预测 Brier/log loss 计算之前**冻结提交。延续先前 [R077研究资格门](R077_FOURTH_INDEPENDENT_HUMAN_DATA_SOURCE_AND_BLIND_SCORE_GATE_2026-10-17.md)。该实验发表于2025年，研究者已经阅读论文摘要中的总体发现，但**尚未在这份原始第四样本计算任何R073七模型的表现**。这属于“相对我们的评分完全未见的第四项独立作者真人实验”与原始作者事后追溯性复现；**不**是研究开始前对新收集的人类资料进行时间上先验注册、不意味着所有已发表人口研究完全未被查看。

## 1. 不可改源与观测意义

真实来源：Drouvelis & Pearce (2025)，*Intelligence and strategy choice in indefinitely repeated prisoner’s dilemma games: A replication of Proto, Rustichini & Sofianos (2022)*，European Economic Review DOI `10.1016/j.euroecorev.2025.105075`。作者本人的 Zenodo v1 DOI `10.5281/zenodo.15462528`，`https://zenodo.org/records/15462528/files/cleandata.dta?download=1`，**1,514,315 bytes**，公开作者MD5 `4cce04ea68b7a0492c242b206efebe53`，本研究锁定SHA256 `1cc9a4f68a51992808d966b118226bb5a66ee3ee6054843a132157df8eeb1985`。作者自己的 `number 2.do` MD5 `563263f55bb3a7a1910b3b38e85fe22c`，原分析明确把 `left=1` 视为合作，`left=0` 视为背叛，把伙伴当轮动作 `otherleft` 单独保存，并在 `practiceperiod>1` 构建两人的上轮动作联合作用。不能拿其它 Stata 游戏选择变量、心理测验 `choice1..20`、`Participate`、`B` 替代这项真实行为标签。

真实数据已由 [R077 Zenodo原始字节与字段审计 CI 38994451948](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38994451948)、[真正作者数值选择代码语义审计 CI 38994561545](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38994561545)、[双人互证和局内时间索引审计 CI 38994709254](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38994709254) 完成，均在本协议冻结前且全部为**无模型评分的来源审核**。3620个人行动；15个原始 `Session`，260个唯一 `Session,Subject` 参与者，10个 `game` 可取值，实践/实验局内 `practiceperiod` 从1开始最多7；共1810个原生 `Session,treatment,Period,Group` 双人互动轮，每组人数恰2且双方 `otherleft` 完全与对方 `left` 镜像相等。可完整复原给定局本人和对手 t-1,t-2 真实动作的 **1040个 t>=3 共同评分目标**，不允许跨 `game` 串联。

具体事件: 仅 `part==2`（来源3620行全部如此）、`treatment∈{0,1}`、`left,otherleft∈{0,1}`、同一 `Session,Subject,game` 内 `practiceperiod` 有完整真实连续1,2,...，当前 `left_t` 作为C=1 D=0监督目标，`(left_{t-1},otherleft_{t-1},left_{t-2},otherleft_{t-2})` 只作为**已经发生的双方公开历史**。原始 session 主键为 `Session`，每个 `Session` 恰一种 treatment；作者另外计算的 `sessionid` 26个不可直接改名为26个独立实验场次。禁止使用原始 `ID`、`sessionid` 或局部 `Group` 值跨真实 session 拼接。原始 `ID` 是 `group(Session Subject)`、恰260个，均只隶属一个 `Session`。

## 2. 唯一主要 donor 与完全无目标拟合

**唯一主要来源预先定为 R073_ALL_12_POOLED。** 原始 Montero-Porras et al. 2022 `eladiomontero/PairwiseStrategies` 提交 `4743f74d8a03a031b8f70aff64956f8ad5155182`，`fix.csv` Git blob `3bf78bf85f6642afee18d6f1965dca7272582f40` (988279 bytes)，`rand.csv` blob `f5a86cd033b739da45d3fc7c5019068f612146a2` (1112614 bytes)。遵守未修改的 R073冻结代码精确 Git blob `c8a0b47fd27bf05e7be5b87419a0824355fc911a`，模型 `M0_TREATMENT_PREVALENCE`/M1/M2/M3/M4/M5/M6，固定alpha=20、TFT/WSLS 0.05理论错误预测率。**源的12场、188人、18424次t>=3事件全部一次估计一份 `p0` 及离散概率表**。不得根据第四项新实验目标标签调整参数、平滑、类别映射、观测风险样本、胜出模型等。M0同样是R073来源平均C；不得擅换为第四研究样本C率。源模型条件状态 `(own1,opp1,own2,opp2)` 一律使用可观察执行选择历史且 `M1..4`原样。

**唯一主要评价**：在 R077 所有合格原始真实15 session里用同一来源数值参数计算一个人下一次选择的条件Brier与log loss；每session对本session目标算术平均，再 **15个原始 `Session` 等权**。对 treatment 0/1 分别报告session等权宏均值与配对改善/变差场数，不能因一个处理真人行动较多而提高权重。七模型必须同一个 t>=3 风险集，不能只选择最优折/组合。每个score都不可以使用目标数据拟合任何概率，也不训练目标的11/14其它场。

## 3. 预定主对比、错误保护与结果等级

六个完整配对对照：M3−M1（对手上一轮历史）、M4−M3（第二轮完整历史）、M1−M0、M2−M0、M5−M0、M6−M0 的 Brier。每个对比报告15场总体等权差与改善/equal/变差场数，及两个 treatment 的等权宏差。M3、M4对M0的派生宏差亦可按上游已经定义的次要对比报告，但不可事后重新指定赢家。全部7个模型Brier和log loss一并保存。

数据门 fail-closed：
- Zenodo原始长度、MD5和SHA均固定；3600余行、15原始Session、260场次内受试者、1810双人局轮、全部双人动作严格交叉镜像，全部个人+局+局内t的key无重复；
- `practiceperiod` 每个 `Session,Subject,game` 必须从1连续递增至局末，同局 `Group` 与伙伴应稳定；如真实样本显示断档/替换则不得猜测拼接；
- 恰1040个t>=3候选事件，所有15个session至少有一条，可明确统计两个treatment的session数与共同风险集合；
- 每个输入 e 都必须5个{0,1}整数，源R073训练合作率在(0,1)，目标任一计算失败要明确 FAIL，不得挑样重试改变范围；
- 先通过至少20项完全合成源隔离/场次边界/样本/模型 invariants测试、再真实在GH Actions独立job评分；原始人员和局轨迹只存在runner临时目录，匿名结果仅保存7模型15场等权、两处理均值与six comparisons/场次好坏，不保留任何原始Session标识、个人编码或逐场分数。任何失败如实报，不许绕过。

**证据边界：** 这是第四项不同实验作者独立收集的真人反复双人博弈，第一份不曾计算过M0–M6结果的评估人群；其公开论文的背景结论早已存在，它也不是事前采样注册。统计结果不能推广到开放循环、不证明心理记忆原因、不证明数值模型可以预测所有地区/制度/历史演化。即便失败也应结题有界复现并完整归档负结果，模型不继续在该第四样本后拟合。PESEN v0.1始终冻结。

`R077_FOURTH_ORIGINAL_HUMAN_ZERO_SHOT_E3_SCORING_RULES=FROZEN_BEFORE_ANY_REAL_M0_M6_TARGET_SCORES`
`R077_MODEL_M0_TO_M6=EXACT_R073_BLOB`
`R077_PRIOR_DATA_RESULT_VISIBILITY=AUTHOR_PAPER_READ_BUT_OURS_UNSCORED`
`R077_SOURCE_TRAINED_ONLY_IN_R073=YES`
`R077_ALL_15_ORIGINAL_SESSION_RESULTS_PENDING`
`PESEN_v0.1=FROZEN`
