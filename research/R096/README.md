# R096：100轮长重复博弈、188名真人、12个真实实验场次的完整LOSO实证

**2026-10-17：R096=CLOSED_BOUNDED。固定配对FP 6场次92人、随机配对SP 6场次96人，每人100轮；事前冻结M0/M1/M2，实际18,612个下一轮目标。原作者固定Git源两次完全独立获取，源Git blob SHA及匿名结果SHA精确复算一致。全部A01–A06有限科学验收PASS。PESEN v0.1继续FROZEN。**

原论文 Montero-Porras, Grujić, Fernández Domingos & Lenaerts (2022), [*Inferring strategies from observations in long iterated Prisoner's dilemma experiments*](https://doi.org/10.1038/s41598-022-11654-2)。论文一手[Dryad正式数据](https://datadryad.org/dataset/doi:10.5061/dryad.37pvmcvmk)的官方文件下载HTTP403 / API401，因此**没有读取Dryad的原件，不能声称字节相同**。实际研究读源来自**原作者研究代码仓库**[eladiomontero/PairwiseStrategies](https://github.com/eladiomontero/PairwiseStrategies)发布tag `submission` 固定commit **`4743f74d8a03a031b8f70aff64956f8ad5155182`**，作者另在[Zenodo保存代码版本](https://zenodo.org/records/5765504)。作者仓库的完整 `fix.csv` 988279字节 Git blob`3bf78bf85f6642afee18d6f1965dca7272582f40` SHA256`c2adc0d68dbc15c4f5ec5f0eb9a05a988cc049a9c086b82f796521a642b6eae9`；`rand.csv` 1112614字节 Git blob`f5a86cd033b739da45d3fc7c5019068f612146a2` SHA256`bc2999d6ad44c60f2b93361eb46b75614b1f600967ae061c76ae51184a80848a`。

严格真实来源结构：FP六个源原`session`各人数匿名排序**8、14、16、18、18、18**，92人共9200个人物轮，100轮不换对手；SP六个源`session` **10、16、16、18、18、18**，96人共9600人物轮，96人均至少更换过对手。188人每人恰100个互不重复轮次；实际18,800源真实二元行动与对手原动作严格逐对符合。元数据审计从不输出source人号、原session、成对对手标识、微观行为序列或派生`context`。

**源类别码本**经独立无模型分数审计后确认仅C/D，C=合作1，D=背叛0，不存在空值或其它行为码。原来源代码转换在读过真损失之前单独冻结；初次错误假定源编码为数值0/1而fail-closed，失败永久保留。

**固定预测协议**：[Phase D完整场次LOSO](../../protocols/R096_PHASE_D_2022_MONTERO_12_TRUE_SESSIONS_188_HUMANS_100_ROUND_BINARY_SESSION_LOSO_M012_SCORE_FREEZE_2026-10-17.md)、[Phase D3仅原作者C/D码本修正](../../protocols/R096_PHASE_D3_C_TO_1_D_TO_0_AUTHOR_ORIGINAL_CODEBOOK_ONLY_AMENDMENT_BEFORE_REAL_SCORE_2026-10-17.md)。每个处理独立轮流留出一个原作者真实session的**全部人全部100轮**：M0＝同处理其它**五个真实原session**相同目标轮的动作均值，绝不使用留出session的任何记录；M1＝目标参与者自己上轮源动作；M2＝严格二者0.5固定混合。二元Brier损失同等目标，第2至100轮；不使用作者已有的`prev`,`context`,`y`或未来derived features。

| 已确证真来源Brier（低越优） | FP固定对手 (9,108) | SP换伴 (9,504) | 全部 (18,612) |
|---|---:|---:|---:|
| M0五其它完整原session同期二元源行动均值 | 0.252287936 | 0.205213179 | 0.228249762 |
| M1本人前一轮二元源行动 | 0.138998682 | 0.195496633 | 0.167848700 |
| **M2固定半混合** | **0.132553853** | **0.148988548** | **0.140946038** |
| **M1相对M0改善** | **+0.113289254** | **+0.009716546** | **+0.060401063** |
| **M2相对M0改善** | **+0.119734083** | **+0.056224631** | **+0.087303725** |

源真实实验场次方向：FP M1**6正0负**、M2 6正0负；SP M1**3正3负**，M2 6正0负。**负面必须保留**：原始SP第2至25轮M1比M0更差，改善**−0.041938666**，第26至100轮转为**+0.026246214**；FP前24轮M1几乎无优**+0.000986168**，第26至100轮则**+0.149226241**。这些分段和三模型均在实际真人分数检视前冻结，不能解释为学习心理机制已经得到因果证明。

阶段门槛与原样失败：[Phase A官方Dryad访问](../../protocols/R096_MONTERO_PORRAS_2022_12_SESSION_100_ROUND_ORIGINAL_DRYAD_SOURCE_ACCESS_AND_SCHEMA_FREEZE_2026-10-17.md) [CI39022157694](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39022157694) 23synthetic PASS但官方真403/401；[Phase B作者固定Git源](../../protocols/R096_PHASE_B_ORIGINAL_AUTHOR_GITHUB_PAIRWISESTRATEGIES_FIXED_SUBMISSION_GIT_BLOBS_PRESCORE_FREEZE_2026-10-17.md)首次因pandas无标题索引拒绝，另冻[Phase B2有限表头兼容](../../protocols/R096_PHASE_B2_ORIGINAL_AUTHOR_GIT_CSV_UNNAMED_INDEX_HEADER_ONLY_REPAIR_FREEZE_2026-10-17.md)实读[CI39022889186](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39022889186)才50synthetic与官方作者两源码成功；[Phase C真实源组/身份只读](../../protocols/R096_PHASE_C_MONTERO_2022_AUTHOR_FP_SP_SESSION_PLAYER_100ROUND_NONBEHAVIOR_ROSTER_FREEZE_2026-10-17.md) [CI39023131299](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39023131299)源12session188人在不看行为下确认；Phase D首次实读程序[CI39023515492](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39023515492)98synthetic全PASS但真人C/D非原数值0/1，**不是模型失效**；[Phase D2无分数作者行动编码类别冻结](../../protocols/R096_PHASE_D2_ORIGINAL_AUTHOR_BINARY_ACTION_CODEBOOK_REJECTION_AND_LITERAL_CLASS_AUDIT_FREEZE_2026-10-17.md) [CI39023662426](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39023662426)才核验源C/D；[Phase D3码本修复](../../protocols/R096_PHASE_D3_C_TO_1_D_TO_0_AUTHOR_ORIGINAL_CODEBOOK_ONLY_AMENDMENT_BEFORE_REAL_SCORE_2026-10-17.md)，过时synthetic`C must reject`先CI失败，然后修正新的预冻编码测试。不根据真实分数修改模型。

[首次110synthetic全部与作者Git真18612下轮模型CI39023796827](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39023796827)两项success，真实结果**11133字节** SHA256 `3aae5d183a33cce37a16d0637b2b887fb106a2b7432d8c8151b9a2dfafe452c2`。[第二次独立源作者Git完整双文件复下载、全源SHA+原行为、110synthetic+18,612所有真来源下轮回算与该匿名SHA逐字节一致、Git正式归档CI39023880006](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39023880006) success。[实际一手作者源码真E2匿名全文结果](R096_MONTERO_2022_188_HUMANS_12_TRUE_SESSIONS_100ROUND_FPSP_BINARY_LOSO_E2_RESULTS.json) (Git blob `1d98ceadcca53d6c09754ff0d2207dd99e8ee2f3`) · [正式科学报告](R096_MONTERO_2022_12_REAL_LAB_SESSIONS_188_HUMANS_100ROUND_FPSP_BINARY_LOSO_E2_SCIENTIFIC_REPORT_2026-10-17.md) · [严格A01–A06有界机读验收](R096_FINAL_ACCEPTANCE_STATUS.json) · [真正固定读源建模源码](r096_montero_2022_188_humans_12_true_sessions_100round_FPSP_LOSO_E2.py) · 其余四阶段来源和类别码本程序/110synthetic均入main。

**科学边界**：只有每处理六个独立原实验室session，188人/18612条不构成18612个独立实验，不能按人轮行虚构聚类显著性；M0使用其它来源session同一轮的真人行为，不是现实日历真正向前预测；原作者Git CSV不被证明等同Dryad原初采集文件；FP/SP差异不是单独识别的因果学习机制；原R095两轮双人Friend/Foe的8场次M1全部负面不能因R096的长100轮正结果而擦除；与R073自/对手过去行为模型并非完全同一冻结合同。新招募E3与历史宏观长期模型**尚未成立**。

**R096=CLOSED_BOUNDED；PESEN v0.1=FROZEN。R097优先另一独立实验室的长轮次真人游戏和真正场次ID，使“伙伴稳定性×轮次阶段影响个人行动历史预测价值”成为明确的跨实验可证伪候选，而不是继续在R096同一188人上优化模型复杂度。**
