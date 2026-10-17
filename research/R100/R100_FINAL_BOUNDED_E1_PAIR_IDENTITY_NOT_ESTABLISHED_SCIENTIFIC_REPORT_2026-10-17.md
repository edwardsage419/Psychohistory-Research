# R100 正式限定结题：真实双人阈值公共品数据E1来源认证通过，原伙伴身份互证不成立

2026-10-17。**R100=CLOSED_E1_PAIR_IDENTITY_NOT_ESTABLISHED**，来源可追溯和身份编码的限定审计已结束。**没有真正真人贡献值被读取、没有新模型的E2预测分数**；PESEN v0.1保持FROZEN。本结题只针对本项目预先冻结的跨来源可检验身份合同，**不认定原作者实验无效、数据造假或社会历史模型为阴性**。

## A 原始出版源E1确证

来自Wang、Hilbe、Zhang (2025) [Zenodo原作者v2记录](https://zenodo.org/records/16918146) 的 `ThresholdPGG_ExperimentalData.xlsx`。GitHub Actions两次以上完整真实下载与出版方MD5对应；实测完整 **217396 bytes**，官方MD5 `c40171abb172da8e16b0839db98a2cf2` 匹配，项目计算完整 SHA256 `825b1cd3226aeca7a19d76d9594f655114b12059648f9ca03b3291c3cf9ab200`，10张原XLSX sheet目录成功，最早[原源完整认证收据](R100_PHASE_A_LIVE_CI_SOURCE_RECEIPT.json)、[Phase A正式E1报告](R100_PHASE_A_FIRST_PARTY_ZENODO_THRESHOLD_PGG_XLSX_REAL_E1_ACCEPTANCE_SCIENTIFIC_REPORT_2026-10-17.md)与Git原机器人收据均归档。该论文报告554人，每人两阶段换伴20轮；这一数字和“换伴”规则起初为**论文描述**，不能以此替代本项目独立身份互指审核。

## B0/B1a 已实际观察到的可复核非行为事实

源真实B0 10sheet匿名原XML行数 221、221、237、237、225、225、209、209、221、221，共2226行节点，去十表每表一个标题结构位置得**2216候选数据行**。B1a进一步读取**仅A/B非行为单元**，确认**每张角色sheet焦点四行块55、55、59、59、56、56、52、52、55、55，共554候选焦点记录**；每块A源数值仅在一个位置出现，另外三行源 A 内容空，B四行皆为共享字符串编码。B每块三种不同码共542块，两种共12块；这12块全部保留，**无法仅凭两种码断言同一真人未换伴**。[B0实际来源收据](R100_PHASE_B0_LIVE_CI_SOURCE_AB_TAG_RECEIPT.json)、[B1a实际来源收据](R100_PHASE_B1A_LIVE_CI_AB_SOURCE_FORMAT_RECEIPT.json)、[B1a报告](R100_PHASE_B1A_GENUINE_554_FOCAL_BLOCKS_AB_SOURCE_FORMAT_BOUNDED_REPORT_2026-10-17.md)。

## B1b/B1c/B1d：固定解释、明确失败、有限兼容与再失败

在实际伙伴关系值参与互指计算**之前**冻结[原B1b焦点角色/对手位置识别假说](../../protocols/R100_PHASE_B1B_AB_FOCAL_ROLE_RECIPROCAL_PARTNER_GRAPH_PRESCORE_FREEZE_2026-10-17.md)：Type1预设本人位在B第1、4行；Type2预设本人位在B第2、3行，其余两个码预设表示同伴。B1b第一次真实来源因为原工作表名不满足含空格的`_Type 1`示意格式被安全拒绝，永久保留[原失败收据](R100_PHASE_B1B_LIVE_CI_PAIR_RECIPROCITY_SOURCE_RECEIPT.json)。随后先单独冻结[B1c完全零sheet单元读取的匿名元数据诊断](../../protocols/R100_PHASE_B1C_ORIGINAL_XLSX_SHEET_NAME_ANON_METADATA_FAILURE_DIAGNOSTIC_FREEZE_2026-10-17.md)，真实源10sheet均满足原预列候选`_Type1`/`_Type2`无空格样式，[B1c实际匿名来源收据](R100_PHASE_B1C_LIVE_CI_ANON_WORKBOOK_NAME_RECEIPT.json)归档。再冻结[B1d单项兼容](../../protocols/R100_PHASE_B1D_ONLY_EXACT_TYPE1_SHEET_NAME_COMPATIBILITY_FIX_FREEZE_2026-10-17.md)，**只**去掉源名类型和序号之间的空格，原先B1b工作流改为手动、第一次真实失败记录未被覆盖。

新的真正原作者B1d [实名代码只在内存处理的匿名互指失败收据](R100_PHASE_B1D_LIVE_CI_PAIR_RECIPROCITY_SOURCE_RECEIPT.json)报告：各处理候选焦点来源总数与论文110/118/112/104/110一致；但每处理两张role sheet的A数字**完全重叠**，跨角色直接用`(treatment,A)`不是唯一真人ID。原解释下的B焦点位在每处理仅有1个不同值，不满足唯一身份键，全部对手互指未建立，真实合法独立pair-session计数仍为**未确认**。这显示此前B1b固定语义假说**被源反驳**；失败收据中的“selfcode重复”等统计是**解析器假说诊断**，不可宣传为原作者真人都拥有相同ID、对手重复匹配或真实缺失配对。

## B1e 最后事前冻结的匿名基数审计与止损

因B1d不足以确定Source A/B编码含义，再冻结[最终有限身份键可辨识性协议](../../protocols/R100_PHASE_B1E_FOCAL_AB_KEY_IDENTIFIABILITY_BOUNDARY_DECISION_FREEZE_2026-10-17.md)，真实[原作者B1e匿名来源基数收据](R100_PHASE_B1E_LIVE_CI_AB_KEY_CARDINALITY_RECEIPT.json)确认：

| 匿名原处理 | Type1及Type2各焦点记录数 | 跨两角色表A数字重合个数 | 每角色表B焦点重复位置不同码数量 | 两表全部B码交集 |
|---|---:|---:|---:|---:|
| 1 | 55 | 55 | 1 | 1 |
| 2 | 59 | 59 | 1 | 1 |
| 3 | 56 | 56 | 1 | 1 |
| 4 | 52 | 52 | 1 | 1 |
| 5 | 55 | 55 | 1 | 1 |

每角色表在另两个B位置各有55/59/56/52/55种不同字符串，全处理B码并集分别**111、119、113、105、111**，表明数据还存在区分每段配对位置的编码信息，但该编码**不满足我们预先冻结的跨角色直接字符串同一性和互指合同**。尤其两表仅1个共同B码，直接利用B字面相等建立两人关系违反数据所证的身份边界。未来作者原始代码或独立码本也许可以明确这些文字与唯一人键的映射；本项目此次未核实这样的码本，禁止回看人类贡献相等来补配对。**当前真正554不同人、554不重复原pair-session及Session2确切不同伙伴，均尚未由本项目从源身份获得独立认证**。

## 科学验收与下一研究方向

* E1完整原官方文件真实性：**PASS**。
* B0/B1a/B1c/B1e来源结构和安全失败证据：**PASS_BOUNDED_DIAGNOSTIC**。
* B1b/B1d固定语义下人物互指资格：**BLOCKED_BOUNDED**。旧失败记录保留，未丢弃异常，未以行为分数改变量词。
* 身份不重叠训练留出、本人历史及对手历史各自增量评分：**NOT_ESTABLISHED**；实际20轮贡献数值读取 **0**；真实E2新预测 **0**。
* 研究R100行政限定结题：**CLOSED_E1_PAIR_IDENTITY_NOT_ESTABLISHED**。PESEN v0.1：**FROZEN**。

**下一研究R101** 应优先拥有来源本人唯一ID、逐轮对手ID、回合、不同原独立场次真实标识并能整体合法留出的独立研究团队公开CSV/TSV。不继续反复猜这个缺乏已证来源互指码本的Excel，也不把技术识别失败当模型阴性或因果结论。
