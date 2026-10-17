# R075 冻结阶段：第三项独立真人重复博弈来源适用性审计

日期：2026-10-17。目标：继续独立外部检验 R073 与 R074 相互矛盾的两轮记忆结论，以及较稳定的一轮本人＋对手共同预测信息。**本阶段仅恢复来源、核查实验场次与当时可观察历史，不执行任何 R075 真实模型拟合或评分。** 一切 E3 声称须另外预先冻结正式样本、特征和评分适配。

## 既有不可更改的研究背景

R073 Montero-Porras et al. 2022：12个整场次留出、18424次真人决策，M3−M1 Brier=-0.009439，M4−M3=-0.004212。R074 Dal Bó 与 Fréchette 2011：18场次留出、15338次真实行为，M3−M1=-0.022915（16好2差）、M4−M3=+0.003171（5好13差）。两者属于 teacher-forced 独立实验内留场次结构复验，第二实验并未直接应用第一实验已估计的条件概率；不推出因果心理机制。七模型 M0–M6、alpha=20、TFT/WSLS=0.05、t>=3同一实验局内历史、同处理整场留出与场次等权 Brier/log loss 维持冻结；第三数据集的分层结构必须先审计，不能假设与前两研究相同。PESEN v0.1 FROZEN。

## 候选 C1：Fudenberg, Rand, Dreber 2012

原作者论文 AER *Slow to Anger and Fast to Forgive: Cooperation in an Uncertain World* DOI `10.1257/aer.102.2.720`。官方复现档案 https://www.openicpsr.org/openicpsr/project/112512/version/V1/view DOI `10.3886/E112512V1`，外部 AEA 历史资料链接 `https://www.aeaweb.org/aer/data/april2012/20100629_data.zip`。论文可核验实验中的行动执行噪声，因此要严格区分本人**意向选择 C/D**、本人实际**执行 C/D**、对手的**实际执行 C/D**、被试当时确实观察到的结果、以及上一轮「模糊的意图」和真实反馈能否用于预测。

公开的第三方 R 整理包 `cran/stratEst` commit `a6373b23d80dc816a63f18f973d372c9e8421914`、`data/FRD2012.rda` blob `6b196ca1624081850b41dc2084c762257d59dd8f`，13,126 行，384个 treatment+id 受试者标签、1536个受试者-supergame、10,054个初步完整 t>=3 局内历史事件。第三方9列包含 treatment/id/game/period/last.choice/last.other/choice/bc/error，**不含原生 session 标识**。这是前次 R074 来源核查所得，不能推导该子集和论文的所有原始行相等，也不能在未恢复 session 时将 supergame 留出冒充独立场次。

一项后续论文 Nishi et al. 2016 DOI `10.1038/srep29622` 以所述 Fudenberg et al. 数据为 Study 3，报告该子研究 384 人、18场次、30,038次决策；这**不能确认**其所筛选资料字节和2012年论文源档案完全一致。该论文自身原始数据称可向 Yale 数据档案申请，不能冒充已下载。

## 候选 C2：Kamei 与 Nesterov 2024

论文 *Endogenous monitoring through voluntary reporting in an infinitely repeated prisoner's dilemma game: experimental evidence*，Economica DOI `10.1111/ecca.12539`，全文说明16场、360名受试者、2018年在 York 实验室执行、无人跨 session 重复参与。包含五处理、随机配对、报告/信誉披露。尽管公开作者设计包含适当的 session 层级，公开支持文件当前只确认了 Appendix PDF，逐轮原始数据可获取性**UNKNOWN**。信息集更复杂，当前人的上一对手反馈与当前对手公共信誉可能不同，必须检查当时可见字段；不能简单用观察的全数据代替信息集。

## 来源适用性及隐私强制门

S01：实验原作者/学会归档资料是可审计的原始来源；网络访问结果按 HTTP 状态或清晰错误类型如实记录。不把 HTML 登录页当 ZIP 解析，不拿下载进度替代字节、哈希证明。

S02：真实 session 身份、真实受试者在不同 session 的隔离、处理、supergame、局内 t、个人上一实际行动与对应伙伴上一实际行动都需独立恢复。不同局之间禁止串历史，整场次绝不能同时进入训练和测试。

S03：噪声条件下本人 `choice` 与当时可见 `last.other` 的含义必须有原始作者资料支持。任何处理的隐含态使用测试标签、当前对手同时行动或未来收益都禁止。

S04：若某处理只有一场或训练期 p0 极端为0/1，整场留出不能运行；必须事先决议，不准过滤后伪称全体结果。

S05：原始逐人记录、session ID、配对、轨迹不进入公开仓库或审计工件；只允许有限匿名文件目录、哈希和数据资格统计；清理 runner 临时源文件。

本审计阶段只授权来源可达性和内容目录（ZIP内成员路径、大小、CRC/hash 元数据如可能，避免公开单人信息）。**先找到并固定一手来源，再单独冻结外部计算适配和 E3 主假设，之后才准实际运行 M0–M6。** 未完成这些门则如实停在 `SOURCE_RECOVERY_PENDING`，不得声称第三实验验证成功。

`R075_SOURCE_ELIGIBILITY_PROTOCOL=FROZEN_BEFORE_ANY_R075_HUMAN_SCORING`
`R075_E3=OPEN`
`PESEN_v0.1=FROZEN`
