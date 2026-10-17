# R086：原作者两人不对称公共品博弈真实真人E2（正式有界结题）

日期：2026-10-17。**R086=CLOSED_BOUNDED，真实原作者 E2 全面复算通过，六项科研验收A01至A06已归档；PESEN v0.1继续冻结。**

Wang / Hilbe / Zhang (2025) [Zenodo官方原始记录 v2](https://zenodo.org/records/16918146) 包含真实实验，两人线性与阈值公共品各五条件FE完全平等、EI禀赋不平等、PI生产率不平等、AI优势一致、MI优势错配。**550名线性真人+554名阈值真人**，本轮完整评价每人自身两个session的贡献曲线。原作者为每名参与者用四行记录：两行第1session、第2session另两行，伴侣的决策不能被错误计为又一个独立真人；两个session同一人交换角色并换伙伴。

研究实际来源状态：[Phase A来源校验冻结](../../protocols/R086_WANG_HILBE_ZHANG_TWO_PLAYER_PGG_ORIGINAL_XLSX_SOURCE_AND_OUTCOME_FREEZE_2026-10-17.md)，commit `9384d806e85b18e50d8b30f0c531b0cc1203adc5`，并于[首次原始官方来源实测39003094721](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39003094721)真正下载两文件并验证作者MD5及全部十个原始sheet；之后在第一次真人贡献评分前先冻结[Phase B人/角色/轮次方法](../../protocols/R086_PHASE_B_TWO_PERSON_FULL_ORIGINAL_BEHAVIOUR_WITHIN_SESSION_FROZEN_SCORE_2026-10-17.md)，commit `4a0475972655b8662a52f2b53f9d06585a9112d0`。线性第1session22轮第2session21轮，阈值两session20轮；全源实际贡献按焦点真人一人一份记录，不保存ID。

[首次全真人E2工作流39003367675](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39003367675)与[独立原始Zenodo再次完整下载、MD5与SHA加双计算比对、永久归档39003432643](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39003432643)都SUCCESS；每次53项纯合成安全/角色/轮次测试通过。严格实读自身贡献记录 **45810**次，20个五处理×两实验×两session主结果表，另外Type1/2角色分层与全部匿名每轮均值曲线已写入[永久完整结果JSON](R086_ORIGINAL_1104_HUMAN_TWO_PERSON_LINEAR_THRESHOLD_FIVE_ARM_E2_RESULTS.json)，**85,566字节，SHA256 `600104f42f2b896646abe543cc6d8ab10450f1d30ed823d9feeeaf6d20a1628c`，Git blob `51c69cdd2c41cd8e688ddd9d8129167746552d83`**，两次原始真人全计算逐字节一致。

关键描述性结论：线性AI优势一致的本人首末贡献变化，第1session **+5.0943**，第2session **+2.2547**；线性PI也两场均正；线性FE两场均负。阈值AI两场分别**−0.8654、−1.6442**，阈值FE/EI/MI也两场均负，PI两场方向相反。负例尤其重要：阈值FE中两session **85/110、93/110**人的自身首末贡献未变；阈值PI **72/112、97/112**人未变，故不将均值下降描述为多数人都持续衰减。原始单位、不同禀赋、角色互换、两人相互依赖与跨游戏不同受试者，限制了处理比较和政策因果。

[完整A01-A06来源、全部20主格与真实负例、因果边界科学报告](R086_ORIGINAL_TWO_PERSON_LINEAR_THRESHOLD_PGG_1104_HUMANS_E2_SCIENTIFIC_REPORT_2026-10-17.md) · [正式机读验收](R086_FINAL_ACCEPTANCE_STATUS.json) · [可复算原始完整真人分析代码](r086_original_two_person_full_human_contribution_E2.py) · [纯合成来源/结构测试](test_r086_original_zenodo_two_player_xlsx_source_gate.py) 和 [全部本人角色/轮次测试](test_r086_original_two_person_full_human_contribution_E2.py)。没有上传原始Excel、本人身份、个人行为序列或问卷。**R086为已发表原始真人 E2 重算，独立全新实验 E3 与政策因果均未建立。** 原四人MAT数据的R085有限来源失败继续独立保留，绝不替换为此两人新来源。
