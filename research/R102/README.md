# R102：2025 独立真人六人重复公共品实验，八完整场次LOSO个人与五同伴历史预测

**2026-10-17 · R102=CLOSED_BOUNDED_E2 · A01至A06限定PASS · PESEN v0.1仍FROZEN。**

新作者团队 Alberto Antonioni、Ángel Sánchez、Antonio Cabrales，[Zenodo v2原始人类行为数据](https://zenodo.org/records/17610157)，`Climate_Clubs_data.csv`。原始发布方MD5 `56931608b717aea06105ad10a58ff937`，独立下载真正源文件**419,189字节**，完整SHA256 `ebc8831011a1a3b4893a80ae158d5129ed0f35e57a8092eba36c6a7b0cbd4282`。27列、2700个人轮、8个确实来源`session.code`、180名未跨session重复的人物编码、每人15轮、**450个实际六人组轮**，四类处理T1至T4各两场。实际 `participant._round_number` 在2520行不同于真实游戏轮 `subsession.round_number`，后者被唯一用作评分回合。

在读取任何贡献数值前，依序冻结[Phase A来源文件](../../protocols/R102_PHASE_A_ANTONIONI_2025_CLIMATE_CLUBS_ORIGINAL_ZENODO_CSV_MD5_HEADER_ONLY_FREEZE_2026-10-17.md)、[A2无末尾换行的唯一原格式修订](../../protocols/R102_PHASE_A2_ORIGINAL_CSV_NO_FINAL_NEWLINE_ONLY_COMPATIBILITY_FREEZE_2026-10-17.md)、[B人物/群体/实验轮来源身份](../../protocols/R102_PHASE_B_CLIMATE_CLUBS_ORIGINAL_SESSION_PERSON_GROUP_ROUND_NONBEHAVIOR_ROSTER_FREEZE_2026-10-17.md)、[B2真正实验轮代码修订](../../protocols/R102_PHASE_B2_PARTICIPANT_TECHNICAL_ROUND_NOT_TRUE_SUBSESSION_ROUND_ONLY_FREEZE_2026-10-17.md)，A/B真实首次来源严格失败均完整保存。真正原源E1收据：[A2](R102_PHASE_A2_LIVE_CI_FIRSTPARTY_CSV_MD5_HEADER_ONLY_RECEIPT.json)；真正原人非行为B2来源收据：[B2](R102_PHASE_B2_LIVE_CI_FIRSTPARTY_NONBEHAVIOR_ROSTER_RECEIPT.json)。

**在任何真实贡献进入模型前严格[冻结 Phase C 8真session完整留出M0至M3](../../protocols/R102_PHASE_C_TRUE_EIGHT_SESSION_LOSO_OWN_PEERS_FIXED_M0_M1_M2_M3_PRESCORE_FREEZE_2026-10-17.md)**：M0为同处理唯一其它整个session在目标同期轮次的贡献占比均值；M1为本人上一轮贡献占比；M2为上一轮真实同组六人**其他五人**平均贡献占比；M3固定`0.5M1+0.5M2`；同一2520个下轮人物贡献占比平方误差MSE越低越好。全部真正第一手人轮在t2至t15合法，无数据删改或调权。

| 冻结模型 | 2520同目标真人MSE | 较M0改善 |
|---|---:|---:|
| M0 外部整场同期基线 | 0.15617213 | 0 |
| M1 本人前轮 | 0.16939683 | −0.01322470 |
| M2 其他五人前轮 | 0.15075937 | +0.00541276 |
| **M3 本人与其他五人前轮各半** | **0.12987238** | **+0.02629975** |

**M3相较M1改善+0.03952444，八个真实原session 8正0负**；但M1相较M0 **2正6负**、M2相较M0 **3正5负**、M3相较M0 **5正3负**，所有负组保留。原作者数据包括**219个系统自动决策下一轮目标**，其余2301个目标为当前轮非自动，事前冻结的后者M3相较M1改善**+0.03806953**。t2..5早期和t6..15晚期增益分别+0.03751111和+0.04032978。

真实第一次评分前**37项纯合成校验全部通过**；之后两次独立重新下载完整出版方原CSV、实算相同2520个人目标，原匿名输出**19,451字节、SHA256 `c19f4e6e4d27650edc89c1586358d5338f9e60aae40b194db8d698b8691b1df9`**逐字节一致，[实际真人8场次匿名结果](R102_PHASE_C_ACTUAL_FIRSTPARTY_EIGHT_SESSION_E2_OR_SOURCE_FAILURE.json)及[第二次独立原作者源准确复演收据](R102_PHASE_C_DOUBLE_INDEPENDENT_FIRSTPARTY_E2_REPLAY_RECEIPT.json)已永久提交[原CI机器结果commit](https://github.com/edwardsage419/Psychohistory-Research/commit/021342676fcce64a3434a337c195999e71d4f21c)。

[完整正式科学报告及每场真实负面证据](R102_2025_180_HUMAN_8_TRUE_SESSIONS_2520_OWN_PEER_M0123_REAL_E2_SCIENTIFIC_REPORT_2026-10-17.md) · [A01至A06机读限定验收](R102_FINAL_ACCEPTANCE_STATUS.json)。

**必要边界**：来源八真正`session`全部留出成立，但M0用了其它场次同期目标行动，因此是回顾性E2，非未来部署E3；系统自动决策存在；M3同时将M1自己的历史权重减半，因此优势可能来自**收缩正则化**而非其他五人的具体行动信息，不能单独识别社会学习的心理因果；六人其他五人并非R073双人单个对手的逐字合同；不同实验Brier与MSE不能直接平均。**下一任务R103优先另外独立来源与事前等权收缩/伙伴历史置换负对照，避免继续在同一批180人中调参。**
