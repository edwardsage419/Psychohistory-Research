# R074：原作者第二独立真人实验的冻结模型跨实验复验

日期：2026-10-17。**正式结题状态 `CLOSED_BOUNDED`**，证据等级为：独立作者、独立真人实验的 E3 结构转移，外部数据自身采用整场次留出。R073 原 E2 继续有效，PESEN v0.1 冻结。

- [前置第二来源及资格冻结协议](../../protocols/R074_SECOND_INDEPENDENT_HUMAN_IPD_SOURCE_GATE_2026-10-17.md)。
- [两个第三方二级文件的来源与实验场次缺口审计](R074_SECOND_INDEPENDENT_IPD_SOURCE_AUDIT_2026-10-17.md)：说明原始整理版不含 session，因而拒绝直接冒称 E3。
- [原作者第一手来源、18场次及同局成对历史资格 CI](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38988443861)：已核验原作者网站文本 SHA，37,042 人类个体动作、266 参与者场次、18场次、15338个 t>=3 有效预测风险事件、六处理各3场。
- [真实分数出现前冻结的外部模型与评分协议](../../protocols/R074_DALBO_AUTHOR_INDEPENDENT_HUMAN_E3_TRANSFER_FREEZE_2026-10-17.md)，commit `706d62a0f740262e20fed7bdec5c80cd97c4edd1`。
- [严格复用 R073 原始七模型公式的外部数据适配及整场留出程序](r074_dalbo_external_human_e3.py) 与 [20项完全合成防泄漏/负结果模型测试](test_r074_dalbo_external_human_e3.py)；还有 [9项真实来源语义合成测试](test_r074_dalbo_author_source_gate.py)。
- [首次真正模型评分 CI](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38988704451) success；[独立重算并显示匿名18场配对胜负与结果SHA的CI](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38988785984) success；[第三次校验并永久归档JSON的CI](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38988844437) success。
- [正式科学结果、负结果和推断边界报告](R074_REAL_EXTERNAL_HUMAN_E3_RESULTS_AND_SCIENTIFIC_LIMITS_2026-10-17.md)，[原始匿名宏指标永久归档 JSON](R074_EXTERNAL_REAL_HUMAN_18_SESSION_E3_RESULTS.json)，[统一验收状态 JSON](R074_FINAL_ACCEPTANCE_STATUS.json)。

**结果**：M3(上轮自己及对手) 对 M1(只用上轮自己)，18场等权 Brier `−0.022915328373344184`，16场好、2场差，因此对手上轮反馈增量获得独立第二实验支持。M4(前两轮双方) 对 M3，18场等权 Brier `+0.003170501040435799`，5场好、13场差，因此16态增加两轮历史的收益**未获跨实验稳定复现**。这一真实负结果必须与积极结果并报。R074 七模型最优宏误差是 M3 `0.07130947710579069`。

源：Dal Bó & Fréchette 2011 DOI `10.1257/aer.101.1.411`；原作者直接文本 `https://gfrechette.com/data/Dal_Bo_2011a_data.txt` SHA256 `357a12968546a8d9002c912c1f499e02e93d59113d2a0928de2dee48323a0ae6`；真实输出 **19,308字节** SHA256 `9946011d1d915c2cf4b29049f8d38d4e626106bd920d6b9b646b09bd3d56f448`。

**统一 A01–A06 均 PASS，仅在有界目标内结题。** 开放事项：零样本参数转移尚未测量，不能从已观察历史相关性推断因果记忆机制；只评估随机终止重复博弈中每次 match 的第3轮及以后、可用完整历史的决策；缺独立物理重返 roster，数字参与者标识未跨 date 重用不能直接证明无现实跨场次返场。原始个人行动、局内个人轨迹和逐场评分均不上传。下一研究应在**第三项新实验**上预先固定新检验，再独立展开，而不是在已见 R074 样本上选择更好的模型参数。

`R074=CLOSED_BOUNDED`; `R074_HUMAN_E3_EXTERNAL_SESSION_LOSO=PASS`; `M3_MINUS_M1_EXTERNAL_DIRECTION=REPLICATED`; `M4_MINUS_M3_EXTERNAL_DIRECTION=FAILED`; `CAUSAL_MEMORY=NOT_IDENTIFIED`; `PESEN_v0.1=FROZEN`.
