# R100：独立历史与伙伴行动增量的跨实验复验，Phase A 原源审核（进行中）

**2026-10-17。阶段状态 = PHASE_A_E1_SOURCE_AUTHENTICATED_WORKBOOK_DIRECTORY_ONLY。真人新模型成绩 = 0。PESEN v0.1 = FROZEN。**

基于 [R099已结题 E2](../R099/README.md) 与 R095/R096 的正反及配对异质性结果，R100 转向在相同下一轮个体目标上独立拆开本人的上一轮与伙伴上一轮贡献。[跨实验边界矩阵](R100_CROSS_EXPERIMENT_EVIDENCE_MATRIX_AND_SOURCE_CANDIDATES_2026-10-17.md)明确了不能混合二元Brier和连续MSE，也不能把R099的24四人组当作8真实实验室session。

首选新资料来自 Wang/Hilbe/Zhang (2025) [Zenodo v2原出版方](https://zenodo.org/records/16918146) 的双人阈值公共品 `ThresholdPGG_ExperimentalData.xlsx`。该作者与R098四人线性实验使用相同发表记录，**并非另一全新原作者团队**。出版方说明的同一人跨两个先后20轮阶段重复出现，不能把两阶段当互不重叠招募样本。其官方**已经在GitHub Actions真实下载逐字节复算通过的文件MD5**为 `c40171abb172da8e16b0839db98a2cf2`。

已在任何本阶段真人来源读取前提交 [Phase A严格来源与隐私冻结](../../protocols/R100_PHASE_A_WANG_2025_TWO_PERSON_THRESHOLD_PGG_ORIGINAL_ZENODO_XLSX_PUBLISHER_SOURCE_ONLY_FREEZE_2026-10-17.md)。[原始来源检查程序](r100_2025_original_threshold_pgg_zenodo_xlsx_source_directory_only.py)仅允许精确Zenodo网址、全文件官方MD5、内部SHA256及安全XLSX工作簿目录；**不得打开任何worksheet、sharedStrings、双方历史贡献、人物或问卷**。[20项纯合成测试](test_r100_2025_original_threshold_pgg_zenodo_xlsx_source_directory_only.py)验证恶意网址、损坏/重复ZIP、XML问题、大小限制和零行为读取；[GitHub Actions工作流](../../.github/workflows/r100-2025-threshold-PGG-Zenodo-XLSX-E1-source-only.yml)已入库，包含先合成后真实第一手来源认证两个job。

**当前只能确认这些源代码和前置协议已提交，尚无GitHub Actions success收据或真实原文件SHA256，故 E1_SOURCE_VERIFIED=NO/UNKNOWN，模型 E2=NO。** 如果 CI 运行失败，必须保留原始错误并执行fail-closed；禁止随意换源、放宽host白名单或用论文数字伪装实测。

接下来以严格科学次序推进：A 已完成一手原字节取得及MD5/工作簿目录认证；B 先冻结真正参与者/配对/两阶段重复的非行为身份解析，避免四行重复计算；C 确认原始两人双方20轮实际行动、制度可比性并在看分前冻结M0/M-own/M-peer/M-both；D 严格合法参与者簇或来源独立单位留出、结果逐次复算及反例保留。**若文件没有真正独立实验室场次编码，任何预测都不得标成lab-session LOSO。**

复验结论不跨越原始设计：不同连续贡献目标不可自动声称 R073 旧模型不变复现；真实心理因果、制度交互因果、历史长时段预测仍未建立。


**后续 A2/B预冻结更新**：[严格源重定向拦截与可审计自动提交补充冻结](../../protocols/R100_PHASE_A2_OFFICIAL_ZENODO_XLSX_REDIRECT_PREFLIGHT_AND_AUDIT_RECEIPT_FREEZE_2026-10-17.md)增加两项纯合成负例，先验对齐20项。[Phase B真实身份及跨阶段重复配对审计冻结](../../protocols/R100_PHASE_B_CANDIDATE_ORIGINAL_PERSON_PAIR_TWOSESSION_NONBEHAVIOR_ROSTER_PRESCORE_ELIGIBILITY_2026-10-17.md)明确真正双人配对不能按四行焦点重复算两遍。出版方554真人、11,080原配对轮等数字迄今仅是原文推算，需B实际核实后方可使用。
