# R110：2015 UCL 真实重复双人囚徒困境，原来源E1通过、行为字词编码资格限定结题

日期：2026-10-19。**R110=CLOSED_BOUNDED_E1_ORIGINAL_BEHAVIOR_TEXT_CODEBOOK_UNMAPPED；LEARNING_PARTIAL_SOURCE_BLOCKED；真人预测E2得分条目0；PESEN v0.1及R073 FROZEN。**

第一手论文：Bone et al. (2015), PLOS ONE, https://doi.org/10.1371/journal.pone.0117183 。原作者 S1 全文件SHA256：ea70b0f3d98075f9d3e4401becfcdec8f6bdb5cae00c4dad63a697f9b61d7b5f。真实原来源B1确认120独立匿名人物、每人两种游戏各50轮、12000个原人轮、18个公开字段；不能独立恢复原论文所述六实验室session或实际伙伴person ID。

研究阶段：
1. **A0/A1/B0/B1**：原出版社委托交付链与全源SHA严格核验，非行为人物×原游戏×轮唯一结构认证。
2. **C0（2026-10-18，原正式冻结）**：要求严格数值字面0/1的本人当前合作及前轮合作、作者前轮伙伴合作信号，M0–M4含同权收缩和同边际伙伴置换负对照，要求至少800同目标、40人、2游戏。真实运行严格退出：R110_C0_PRE_FROZEN_REAL_800_TARGET_40_ACTOR_2_GAME_GATE_FAIL。原失败收据永久保留，**没有任何可用原真人Brier成绩**。
3. **C1（2026-10-19）**：预冻只读匿名失败诊断后，真原源所有12000行 Player cooperated 与 Partner coop prev 均为非空非数值文字；严格按原C0分母，240首轮排除、之后11760行全部在本人当前合作数值门排除。13项纯合成测试、真正GitHub Actions两个job success，来源合法、匿名证据自动归档。
4. **C2（2026-10-19）**：查原PLOS S1对 Partner coop prev 明确 yes/no 的一手说明，另冻大小写与空白的yes/no映射，原源完全重新取得SHA成功。本人 Player cooperated 有7437 yes、2173 no、2390其它非空；作者伙伴上轮信号有7606 yes、4154 no、240其它非空。8项合成测试与真正GitHub Actions两job均success，但**词典精确覆盖失败**：C2_UNMAPPED_SOURCE_TEXT_REQUIRES_CODEBOOK。其它词不作猜测，不在C0上覆盖修改，也不另开真实预测评分。
5. **学习成果**：完成原2015 PLOS论文强/弱权力、不对称与合作惩罚/退出机制，以及二项GLMM、受试者随机效应、logit和AICc有限模型学习；模型作者报告结果与项目自身复算区分。

证据和文档入口：
* [正式研究终态](R110_FINAL_ACCEPTANCE_STATUS.json)
* [C1正式来源诊断报告](R110_PHASE_C1_GENUINE_SOURCE_BINARY_FIELD_ENCODING_BOUNDED_DIAGNOSTIC_SCIENTIFIC_REPORT_2026-10-19.md) | [真实C1机读收据](R110_PHASE_C1_LIVE_CI_2015_UCL_ORIGINAL_SOURCE_ANONYMOUS_ELIGIBILITY_OR_FAILURE.json) | [C1 GitHub Actions](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39222228439)
* [C2正式词典覆盖阴性报告](R110_PHASE_C2_FIRSTPARTY_YES_NO_COVERAGE_NEGATIVE_SOURCE_SCIENTIFIC_REPORT_2026-10-19.md) | [真实C2机读收据](R110_PHASE_C2_LIVE_CI_ORIGINAL_2015_UCL_AUTHOR_YES_NO_WORD_SCHEMA_OR_FAILURE.json) | [C2 GitHub Actions](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39222908506)
* [原论文数学统计与合作惩罚退出模型机制学习](R110_BONE_2015_POWER_ASYMMETRY_COOPERATION_PUNISHMENT_GLMM_MECHANISM_LEARNING_2026-10-19.md)
* [原C0不可变失败收据](R110_PHASE_C0_LIVE_CI_2015_UCL_ACTOR_PEER_SIGNAL_MATCHED_SHRINK_SHAM_E2_OR_BOUNDED_FAILURE.json)
* [C1另行冻结](../../protocols/R110_PHASE_C1_ORIGINAL_UCL_BINARY_AND_ELIGIBILITY_DIAGNOSTIC_SOURCE_ONLY_FREEZE_2026-10-19.md) | [C2另行冻结](../../protocols/R110_PHASE_C2_2015_UCL_ORIGINAL_AUTHOR_YES_NO_WORD_CODEBOOK_SOURCE_ONLY_PRESCORE_FREEZE_2026-10-19.md)

**止损并转下一既定R模型学习**：若将来作者提供精确原行为特殊词语及退出/破产合法状态码本，可申请另行事前冻结新研究版本。当前不再猜原词或绕过C2来源合同。当前的资料仅支持有界理论和来源学习，既不证明社会学习因果，也不支持历史演化或真实前瞻预测。R105同权收缩阴性与R106真实前轮对手历史正向均保留各自不同设计边界。
