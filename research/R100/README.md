# R100：独立历史与伙伴行动增量的跨实验复验，Phase A 原源审核（进行中）

**2026-10-17。阶段状态 = PHASE_A_E1_SOURCE_AUTHENTICATED_WORKBOOK_DIRECTORY_ONLY。真人新模型成绩 = 0。PESEN v0.1 = FROZEN。**

基于 [R099已结题 E2](../R099/README.md) 与 R095/R096 的正反及配对异质性结果，R100 转向在相同下一轮个体目标上独立拆开本人的上一轮与伙伴上一轮贡献。[跨实验边界矩阵](R100_CROSS_EXPERIMENT_EVIDENCE_MATRIX_AND_SOURCE_CANDIDATES_2026-10-17.md)明确了不能混合二元Brier和连续MSE，也不能把R099的24四人组当作8真实实验室session。

首选新资料来自 Wang/Hilbe/Zhang (2025) [Zenodo v2原出版方](https://zenodo.org/records/16918146) 的双人阈值公共品 `ThresholdPGG_ExperimentalData.xlsx`。该作者与R098四人线性实验使用相同发表记录，**并非另一全新原作者团队**。出版方说明的同一人跨两个先后20轮阶段重复出现，不能把两阶段当互不重叠招募样本。其官方**已经在GitHub Actions真实下载逐字节复算通过的文件MD5**为 `c40171abb172da8e16b0839db98a2cf2`。

已在任何本阶段真人来源读取前提交 [Phase A严格来源与隐私冻结](../../protocols/R100_PHASE_A_WANG_2025_TWO_PERSON_THRESHOLD_PGG_ORIGINAL_ZENODO_XLSX_PUBLISHER_SOURCE_ONLY_FREEZE_2026-10-17.md)。[原始来源检查程序](r100_2025_original_threshold_pgg_zenodo_xlsx_source_directory_only.py)仅允许精确Zenodo网址、全文件官方MD5、内部SHA256及安全XLSX工作簿目录；**不得打开任何worksheet、sharedStrings、双方历史贡献、人物或问卷**。[20项纯合成测试](test_r100_2025_original_threshold_pgg_zenodo_xlsx_source_directory_only.py)验证恶意网址、损坏/重复ZIP、XML问题、大小限制和零行为读取；[GitHub Actions工作流](../../.github/workflows/r100-2025-threshold-PGG-Zenodo-XLSX-E1-source-only.yml)已入库，包含先合成后真实第一手来源认证两个job。

**当前只能确认这些源代码和前置协议已提交，尚无GitHub Actions success收据或真实原文件SHA256，故 E1_SOURCE_VERIFIED=NO/UNKNOWN，模型 E2=NO。** 如果 CI 运行失败，必须保留原始错误并执行fail-closed；禁止随意换源、放宽host白名单或用论文数字伪装实测。

接下来以严格科学次序推进：A 已完成一手原字节取得及MD5/工作簿目录认证；B 先冻结真正参与者/配对/两阶段重复的非行为身份解析，避免四行重复计算；C 确认原始两人双方20轮实际行动、制度可比性并在看分前冻结M0/M-own/M-peer/M-both；D 严格合法参与者簇或来源独立单位留出、结果逐次复算及反例保留。**若文件没有真正独立实验室场次编码，任何预测都不得标成lab-session LOSO。**

复验结论不跨越原始设计：不同连续贡献目标不可自动声称 R073 旧模型不变复现；真实心理因果、制度交互因果、历史长时段预测仍未建立。


**后续 A2/B预冻结更新**：[严格源重定向拦截与可审计自动提交补充冻结](../../protocols/R100_PHASE_A2_OFFICIAL_ZENODO_XLSX_REDIRECT_PREFLIGHT_AND_AUDIT_RECEIPT_FREEZE_2026-10-17.md)增加两项纯合成负例，先验对齐20项。[Phase B真实身份及跨阶段重复配对审计冻结](../../protocols/R100_PHASE_B_CANDIDATE_ORIGINAL_PERSON_PAIR_TWOSESSION_NONBEHAVIOR_ROSTER_PRESCORE_ELIGIBILITY_2026-10-17.md)明确真正双人配对不能按四行焦点重复算两遍。出版方554真人、11,080原配对轮等数字迄今仅是原文推算，需B实际核实后方可使用。

## 2026-10-17 · B0真实来源工作表A/B字段结构审核有界通过

来源本身已全217396字节官方MD5/项目SHA精确验证后，先冻结[Phase B0 XML标签零值读取协议](../../protocols/R100_PHASE_B0_AUTHENTICATED_XLSX_SHEET_COLUMN_A_B_STRUCTURE_ONLY_PRESCORE_FREEZE_2026-10-17.md)，再在GitHub CI先运行20项A2+15项B0纯合成测试，后对原文件10张真正工作表XML仅计数行标签和A/B身份列标签，不访问任何单元格值。[机器人实际来源B0匿名收据](R100_PHASE_B0_LIVE_CI_SOURCE_AB_TAG_RECEIPT.json)已经[自动提交 main](https://github.com/edwardsage419/Psychohistory-Research/commit/3a71b97ffa731b9f54c7ac571ce5b34d87305872)。

真实匿名工作表每张的行标签分别 **221、221、237、237、225、225、209、209、221、221**，A/B列标签逐张均同数量，合计**2226行含10行结构性表头，对应2216个候选数据行**，与原作者五处理554人×四行公布格式一致。**这仍未从原A列值认证554个不同人，未从B列值重建任意真实配对，也未读任何C:V的20轮动作。**

[正式B0来源结构科学报告](R100_PHASE_B0_GENUINE_ORIGINAL_10SHEET_AB_TAG_ANONYMOUS_E1_STRUCTURE_REPORT_2026-10-17.md)和[机读边界状态](R100_PHASE_B0_CURRENT_STATUS.json)已归档。**R100 A=E1_PASS、B0=PASS_BOUNDED、B1真实人配对互证=PENDING、E2真人预测=0、PESEN v0.1 FROZEN**。后续只按[Phase B真正独立参与者及伙伴去重资格](../../protocols/R100_PHASE_B_CANDIDATE_ORIGINAL_PERSON_PAIR_TWOSESSION_NONBEHAVIOR_ROSTER_PRESCORE_ELIGIBILITY_2026-10-17.md)推进，不能把同一配对双方焦点重复记录当成新实验。


## R100 限定正式结题：原始来源E1成功，源本人/伙伴互指B1阻断（2026-10-17）

在B0的真原XLSX结构通过后，追加预冻[B1a实际A/B代码诊断](../../protocols/R100_PHASE_B1_PINNED_XLSX_AB_ONLY_LITERAL_ROSTER_SCHEMA_DIAGNOSTIC_PRESCORE_FREEZE_2026-10-17.md)、[B1b来源人物和对手互指假说](../../protocols/R100_PHASE_B1B_AB_FOCAL_ROLE_RECIPROCAL_PARTNER_GRAPH_PRESCORE_FREEZE_2026-10-17.md)、初次真正source失败、[B1c匿名sheet命名差异诊断](../../protocols/R100_PHASE_B1C_ORIGINAL_XLSX_SHEET_NAME_ANON_METADATA_FAILURE_DIAGNOSTIC_FREEZE_2026-10-17.md)、[B1d仅去掉Type前空格的source方案修订](../../protocols/R100_PHASE_B1D_ONLY_EXACT_TYPE1_SHEET_NAME_COMPATIBILITY_FIX_FREEZE_2026-10-17.md)和[B1e最后一次A/B来源唯一码基数审计](../../protocols/R100_PHASE_B1E_FOCAL_AB_KEY_IDENTIFIABILITY_BOUNDARY_DECISION_FREEZE_2026-10-17.md)。

**真正原作者源B1a**仅A/B值匿名确认554个四行焦点记录块，A每块一非空数值、B每块四非空字符串，B三个不同码542块、两个不同码12块全保留。[实际匿名B1a](R100_PHASE_B1A_LIVE_CI_AB_SOURCE_FORMAT_RECEIPT.json)。B1b第一次真实来源workbook名`Type1`与预注册`Type 1`不匹配，严格拒绝并[保留最初失败](R100_PHASE_B1B_LIVE_CI_PAIR_RECIPROCITY_SOURCE_RECEIPT.json)；B1c真实匿名目录诊断确认全部10张符合源`Type1/Type2`；仅修正名后[B1d真实源码双向配对假说被来源反例阻断](R100_PHASE_B1D_LIVE_CI_PAIR_RECIPROCITY_SOURCE_RECEIPT.json)，没有声明参与者缺失或实验错误。

**最终真实B1e**[A/B匿名身份码基数收据](R100_PHASE_B1E_LIVE_CI_AB_KEY_CARDINALITY_RECEIPT.json)确证每个原处理两张role sheet A数字完全集重合、B预设本人重叠位在整张sheet仅一个不同值；两role的所有B字符串只有一个共同值，直接相等不满足原作者真实同伴唯一互指合同。B码余下两个位置各有焦点人数那么多种不同字符串，说明编码仍包含结构性差异，但本研究没有核验能唯一映射A人的外部原作者码本，严禁从实际贡献相等反推同伴身份。

[最终科学有界结题报告](R100_FINAL_BOUNDED_E1_PAIR_IDENTITY_NOT_ESTABLISHED_SCIENTIFIC_REPORT_2026-10-17.md) · [机器验收](R100_FINAL_ACCEPTANCE_STATUS.json)。

**R100=CLOSED_E1_PAIR_IDENTITY_NOT_ESTABLISHED，真官方来源E1=YES、独立配对身份=NOT_ESTABLISHED、真实E2贡献预测=0、PESEN v0.1=FROZEN。** 该失败不是模型预测阴性，下一步转R101独立作者组公开可证实source session/person/opponent/round逐回合数据。
