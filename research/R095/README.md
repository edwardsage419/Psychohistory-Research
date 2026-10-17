# R095 — 原作者真实8个独立实验室场次、96名真人二元重复囚徒困境，全场次LOSO负面实证E2

2026-10-17。**R095=CLOSED_BOUNDED，全部A01–A06限定PASS。首次获得额外一项真正以原实验真实session为整体留出单位的首方独立实验室二元行为对比；本人过去行动M1在8/8源场次不如场次外部均值M0，固定M2在5/8场次不如M0。** 不将其夸大为所有二元/长程游戏中记忆无用的通用结论；PESEN v0.1保持FROZEN。

**原作者** Eric Schniter & Timothy Shields，Chapman University, [2020《Participant Faces from a Repeated Prisoner's Dilemma》Zenodo v1](https://zenodo.org/records/4321821)，数据DOI `10.5281/zenodo.4321821`。一手原版 `Fields.csv` 源发布MD5 **`4c30ac1861e12f46e0b9847c9d1857a7`**，已真核验完整文件**22312字节**，本项目SHA256 **`0678cc3d565d3a02e4766fedff211cc37b2e0e9d373e41c391466c6f84a56f4c`**。原作者`Fields_codebook.csv`定义`ID,round,option,session,group,other_split`；正式source原件无任何个人数据、年龄、其他受试者行动行、会话代码再上传。实验采集了人脸视频和个人年龄，但研究全部忽略，不访问受限制身份映射。

真原作者从`session`直接记录和确认**8个确切不同实验室场次，各12真人=96人**，每场次**6个固定两人合作/背叛组，合计48原配对**；第一轮96来源真人决策、第二轮96、第三轮只12名真人，总204源人轮。原组匹配在两个主要轮次内稳定，`other_split`原报告伙伴行动与另一人真`option`一致。本次八个独立实验场次完全留出，而不是像R094虽论文声称80session、次级文件却缺少session ID，不能做本关口。

冻结[Phase A来源资格](../../protocols/R095_SCHNITER_SHIELDS_ORIGINAL_2020_ZENODO_FRIEND_OR_FOE_SESSION_LOSO_SOURCE_GATE_2026-10-17.md)，真实源[CI39020885386](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39020885386) **25 synthetic、来源MD5、8真实session数据不看行为全部PASS**，再冻[Phase C真人二元评分合同](../../protocols/R095_PHASE_C_SCHNITER_SHIELDS_8_REAL_2020_LAB_SESSIONS_96_BINARY_ROUND2_LOSO_M012_FREEZE_2026-10-17.md)，原样保持过去各研究反复使用的三个信息结构：目标原人t2 Split=1 / Take All=0，M0=**其余7整个原实验室场次84名真人t2合作均值**（不含测试场次任何真实行为）；M1=被试本人t1行动；M2=固定0.5M0+0.5M1。Brier误差低好，恰对96个原始第二轮源真实选择全部计分；第三轮仅一个session，无法形成可比其它session的同轮预测，所以事前排除主要评分。所有八个true session是最小独立实验单位，不能冒称96个独立实验。

| 一手源真人8完整场次LOSO模型 | 实际第二轮96目标的Brier损失（低更优） | 对M0同目标改善 |
|---|---:|---:|
| **M0 其它7实验室场次t2合作基线** | **0.252178997** | 基线 |
| **M1 本人真实第1轮行动** | 0.395833333 | **−0.143654337** |
| **M2 固定二者各半** | 0.264619650 | **−0.012440653** |

**M1在全部8/8原实验室场次均负面**（0正/8负），M2 3正/5负，且平均稍差。原实验**第一轮71/96=73.96%合作、第二轮51/96=53.13%合作**，本来源非常短且存在合作变化，历史复制模型不适宜可能与长度/终局效应有关，但此研究**没有识别终局心理因果机制**。与R089、R090、R091、R093、R094行为定义、目标层级、匹配规则不同，不能拿这些结果加总成统一历史作用指数。

**方法诚实披露**：原数据网页预览在协议提交之前已显示部分真实行动行，故只能说算法M0/M1/M2在项目既往阶段已固定、在首次程序完整评分前冻结场次协议，**不能说这项实验在研究者未接触任何结果前完全盲法预注册**。该点载于原研究报告与验收。原52项synthetic虽PASS，首次运行[CI39021166964](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39021166964)遭CLI输出路径`Namespace.parse_args`错误，未能生成可验收结果；仅修复CLI后[真实第一场次评分CI39021217536](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39021217536)SUCCESS。

[再次独立重新取回作者原版MD5/SHA、重复52 synthetic与全部96真人场次LOSO及永久匿名负面证据归档CI39021289019](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39021289019) SUCCESS，结果**3021字节** SHA256 **`f45182131e0ec364fdd34c3eb36cb96f92c14a6db8c35de287dcc6632aea1b63`**，永久Git blob `8c43d31eade559da84e0f877b34eff5cead76a9c`。[匿名原研究真实E2结果](R095_SCHNITER_SHIELDS_2020_8_REAL_LAB_SESSIONS_96_BINARY_ROUND2_LOSO_E2_RESULTS.json) · [正式科学报告](R095_SCHNITER_SHIELDS_2020_EIGHT_TRUE_LAB_SESSION_LOSO_BINARY_FRIEND_FOE_NEGATIVE_E2_SCIENTIFIC_REPORT_2026-10-17.md) · [A01–A06有界验收](R095_FINAL_ACCEPTANCE_STATUS.json) · [原始可复算真评分源码](r095_schniter_shields_96_humans_8_full_original_sessions_LOSO_E2.py) · [源资格程序](r095_schniter_shields_2020_original_session_roster_no_actions.py) · 25+27 synthetic与工作流均同步GitHub main。

**科学限制**：八个true session、仅一轮前历史，短实验的合作衰减，不足外推其它长期游戏；当前跨session原评价并非真正将来才收集样本的新E3；原预览曾暴露行为，缺完全盲法；不声称社会心理记忆在一般情况下失效或形成历史预测理论。下一阶段 R096 优先其它原作者更长期实验，例如 Montero-Porras et al. 2022 原著12个真实session、188名人、100轮固定或更换对手的原始Dryad资料 `10.5061/dryad.37pvmcvmk`，先确定真正session-ID再冻结行为比较。PESEN v0.1继续FROZEN。
