# R077 一手来源结构修正：实际配对变动、局内非首轮观察、零样本预测预结果修订协议 Rev-002

日期：2026-10-17。**仅修订由真实原始数据来源审计揭示的资格/历史映射，不涉及、也尚未看到任何 R077 M0-M6 真人预测得分。** Rev-001 原文件 `protocols/R077_ZENODO_FOURTH_AUTHOR_TRUE_HUMAN_PROSPECTIVE_MODEL_SCORE_FREEZE_2026-10-17.md` 保留且不可删除或倒写。

## 1. 触发修订的明确失败证据

首次真实评价 [CI 38994977281](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38994977281) 的24项纯合成测试均 PASS，但真实作业在任何目标模型概率计算前被原协议保护拒绝；第二次增加安全失败原因而不改代码评估要求的 [CI 38995038132](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38995038132) 明确 `R077_PARTNER_PAIR_CHANGED_WITHIN_SAME_GAME`、`model_Brier={}`、`R077_FIRST_FOURTH_HUMAN_E3_FAIL_CLOSED`。错误不是模型性能不良，也没有生成真实第四样本七模型Brier。

随后独立源码层**纯结构不评分审计** [CI 38995148912](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38995148912)：
- 2025原作者Zenodo `cleandata.dta` SHA256 仍为 `1cc9a4f68a51992808d966b118226bb5a66ee3ee6054843a132157df8eeb1985`，3,620个人实际 C/D 事件和15个真实 session、1,810双人轮次全部通过。
- treatment=0：680个 `Session+Subject+game` 个体局，1,020次同局相邻观测，原 `Group` **0次变化**，从局内 t1 连续完整。
- treatment=1：760个个体局，1,160次同局相邻观测，`Group` 在**130次相邻观察**中变动，130个个体局发生组别变更；80个个体局的 `practiceperiod` 不等于完整 `1..n`，需要按实际 t-1/t-2 可见性而非强制每人每局均从1开始。
- **原始 `ClientNumber` 在两个处理的每个个体局内0次变化**；它是否标识当前对手不确定，不能由此证明对手稳定。所有1810个实际相遇的双人一轮 `otherleft` 与另一真人当期 `left` **100%双方镜像核对**，并且真实作者 `number 2.do` 用 `otherleft` 的**上一轮**来估计人的下一轮合作，故这里的 previous opponent 是**上一轮实际匹配/执行对手**，可能不是当前实际伙伴。与R073随机匹配处理的上一历史对手性质同类。不能借前后 `Group` 变动推出“同一伙伴互惠”。
- 此处全部证据是在**任何第四真人模型输出前**独立产生，不针对模型好坏挑样，不更改真实原始 `left` 和 `otherleft` 来源字段、R073来源参数、7模型、alpha=20、固定TFT/WSLS理论0.05或损失规则。

## 2. 唯一修订的 source time/pair 资格语义

Rev-001 把 `Group` 不变误设为 **every person-game 的强制完整性条件**。这不是 R073 七模型本体的强制条件，R073的 shuffled session 就是上一轮对手与当前对手可能不同的情形。对R077源，只需确认**真正上一轮对手的已经发生行动**对个人可观察，而不强行要求当前 partner identity 与前一轮相同。

Rev-002允许当前 `Group` 在同一 `Session,Subject,game` 局内变化；**每一行依然必须经过真正两人单轮相遇的镜像对手行动核验**，不可跨game或来源真实 session 使用任何对手未来/同时行动。

Rev-001 误要求每个参与者-game 从本实验局 t1 完全收集；真实源有80个局内缺观察前端或非完整本地序列。Rev-002事先明确共同风险：
`t >=3 AND same Session+Subject+game has original practiceperiod (t-1) AND (t-2) AND current t`。
只在**两次真实相邻完整历史**均出现在原始字节中时产生预测事件。既不补缺也不插值，不能借 t1 跳过 t2 拼接出一个二步事件；全部正常和变组条件同一门。原来的纯结构 pre-score G3 候选 **1040个**是按这一严格当前与 t−1/t−2 同局连续条件得出，修订后真正风险集必须恰1040，否则FAIL且不执行任何评价。源总参与者260、完整15场次、两个处理均保留，**没有删除某些负例处理或在评分后挑选更合适的样本**。禁止按照后来模型误差决定是否筛组稳定子集。

## 3. 完全不变的冻结评分与边界

仍唯一主要 donor R073_ALL_12_POOLED（12个原作者源session、18424次真人历史目标），原版`r073_human_ipd_memory_loso.py` Git blob `c8a0b47fd27bf05e7be5b87419a0824355fc911a`，M0..M6参数和所有 score 原样，绝无任何第四实验标签拟合。全部15个原始session等权，两个原始treatment分别报告全部七模型Brier/logloss与六组预先主/次对照，含所有改善/失败场次。

本次修订只修复两个已经真实观察到的本地源语义问题，属**预结果的实质修订**，后续结题必须披露此修订及两次失败作业，不得宣称Rev-001一次不修改直接通过，也不得声称第四实验是2025研究收集前便注册的预测计划。如果原始实验提供的反馈不足以认定跨当期group的上一轮对手行动真的被人看见，那么 R077 评分仍只能解释为客观行为历史下的条件预测，不能承诺心理信息集因果识别。

`R077_REV001_ELIGIBILITY_GATE=FAILED_BEFORE_MODEL_SCORING`
`R077_REV002_ELIGIBILITY_TIME_WINDOW=COMPLETE_ACTUAL_t_MINUS_1_AND_t_MINUS_2_IN_SAME_PERSON_GAME`
`R077_ALLOW_GROUP_CHANGES_IN_PREVIOUS_OPPONENT_HISTORY=YES_WITH_CAVEAT`
`R077_TARGET_TRAINING_DATA=ZERO`
`R077_E3_SCORES_AT_REV002_FREEZE=NONE`
`PESEN_v0.1=FROZEN`
