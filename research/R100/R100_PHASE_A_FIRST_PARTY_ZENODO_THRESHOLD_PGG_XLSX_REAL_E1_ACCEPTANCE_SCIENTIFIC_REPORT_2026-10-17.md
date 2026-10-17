# R100 原作者双人阈值公共品数据的正式来源 E1 验收报告

日期：2026-10-17。阶段：A + A2。**E1 原始出版源数据完整字节和XLSX工作簿目录通过**，但尚未进入真实人物配对审计或真人行为模型E2。PESEN v0.1 FROZEN。

## 一、证据来源及实际执行

新候选来自 Wang、Hilbe、Zhang (2025) [Zenodo版本v2](https://zenodo.org/records/16918146)，DOI 10.5281/zenodo.16918146，原始文件 `ThresholdPGG_ExperimentalData.xlsx`。出版记录直接公布文件官方MD5 `c40171abb172da8e16b0839db98a2cf2`，本项目先冻结 Phase A exact path、大小、哈希及匿名目录再执行。额外[Phase A2](../../protocols/R100_PHASE_A2_OFFICIAL_ZENODO_XLSX_REDIRECT_PREFLIGHT_AND_AUDIT_RECEIPT_FREEZE_2026-10-17.md)提前阻断所有未经批准 3xx 重定向并增加 synthetic 反例；真实行为全程没有打开。

真实GitHub Actions机器人工作流在合成测试闸门后已向 main 自动写回 [源E1永久机读收据](R100_PHASE_A_LIVE_CI_SOURCE_RECEIPT.json)，提交 [2b26fa8d8459e2fdd6deae8914980a3bf23e9648](https://github.com/edwardsage419/Psychohistory-Research/commit/2b26fa8d8459e2fdd6deae8914980a3bf23e9648)，本项目从main重新取回原收据并核验Git blob `89d1350d7dc2a3aa361ecedc8db9505627444172`。该证据来自真实原始源重新下载、非仅对论文引用数字的抄录。

| E1验收项 | 真实结果 |
|---|---|
| 官方 Zenodo v2 目标文件 | 通过固定 URL 白名单与完整文件MD5 |
| 原始源大小 | **217,396 字节** |
| 出版方原MD5 | `c40171abb172da8e16b0839db98a2cf2`，**实际匹配** |
| 本项目整文件SHA256 | `825b1cd3226aeca7a19d76d9594f655114b12059648f9ca03b3291c3cf9ab200` |
| XLSX工作簿目录 | **10** 张sheet |
| 原工作表姓名公开 | 否 |
| worksheet内容或sharedStrings加载 | 否，Phase A源码只读content types/workbook目录 |
| 本阶段真实贡献/问卷读取 | **0** |
| 本阶段原人模态预测评分 | **0** |

原作者设计公布FE110、EI118、PI112、AI104、MI110五个处理，每个真实人跨依次两个20轮阶段，第二阶段换伴并更换位置；这仍是**原作者文字报告**。原文件A阶段只验证目录，**没有通过真正身份数值证明554人，也没有证明哪一项原同伴关系**。此Zenodo来源的作者与之前R098四人MAT项目是同一团队，研究协议不同，不能混称全新团队独立招募。来源阶段编号Session1/Session2表示同一人的重复过程，不能说成两个相互独立的实验室样本。

## 二、失败可接受边界及诚实评级

`E1_SOURCE_AUTHENTICATED_WORKBOOK_DIRECTORY_ONLY=YES`；`ACTUAL_PAIR_IDS_VERIFIED=NO`；`ACTUAL_20_ROUND_CONTRIBUTIONS_VALIDATED=NO`；`PERSON_DISJOINT_HOLDOUT=NO`；`R073_EXACT_CROSS_EXPERIMENT_REPLICATION=NO`；`REAL_HUMAN_MODEL_E2=NO`。GitHub Actions成功的独立 run-level 页面在此阶段未再次查询；已有依赖纯合成闸门的机器人成功写回产物，足以证明实际源认证程序执行并成功归档。不得把这等同后续B或C成功。

## 三、下一阶段约束

B0已另行先冻结[真实sheet A/B身份列**标签**元数据检查](../../protocols/R100_PHASE_B0_AUTHENTICATED_XLSX_SHEET_COLUMN_A_B_STRUCTURE_ONLY_PRESCORE_FREEZE_2026-10-17.md)；其结果未在本文提前视为通过。再按[阶段B原人换伴去重协议](../../protocols/R100_PHASE_B_CANDIDATE_ORIGINAL_PERSON_PAIR_TWOSESSION_NONBEHAVIOR_ROSTER_PRESCORE_ELIGIBILITY_2026-10-17.md)评估是否能从A/B原来源重建匿名人物关系。出版文本推算的22160人轮严格留待源身份和逐轮合法性验证后才能称为实测。C阶段只在来源身份去重完成并再次冻结同目标M0、本人lag、伙伴lag和联合lag评分合同之后，才允许实际读取原贡献进行真正真人评分。

**R100 Phase A 结题：PASS_E1_SOURCE_ONLY；项目 R100 全部科研模型结题：NO；PESEN v0.1：FROZEN。**
