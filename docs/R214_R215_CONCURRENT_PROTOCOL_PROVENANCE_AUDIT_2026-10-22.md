# 并行研究协议核对：R214双冻结与R215主研究/三期补充的证据边界（2026-10-22）

性质：科研治理、文件身份与源证据的核对记录。只解释**已经实际存在**的原冻结协议、源码、数据、CI和正式结题收据。不得将不同来源空间、不同总体或不同测试统计合并成同一个已验证单一实验；本记录**不改变任何既有科研评分规则、结果、原文件SHA**。

## 1. R214 09-005 Regression Discontinuity：两个协议必须分开

A. **已执行且正式结题的R214主研究**：[12世界×16噪声原来源冻结](../protocols/R214_RDD_12_WORLDS_192_ORIGINAL_NOISE_SOURCES_PRESCORE_FREEZE_2026-10-22.md)，预冻结提交`2f697e74`，实际完整原结果位于`research/R214/R214_EXACT_RESULTS.json`、`research/R214/R214_ALL_192_ORIGINAL_RDD_NOISE_SOURCES.csv`、`research/R214/R214_FINAL_ACCEPTANCE_STATUS.json`、`research/R214/R214_SCIENTIFIC_REPORT_2026-10-22.md`，CI [run39740585568](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39740585568)三作业全部success。R214正式结题的数量和结论只依此源与验收。

B. **独立的未正式归档扩展研究设计**：[9世界×576潜在U、E、R来源及36局部条件均值外推冻结](../protocols/R214_RDD_9_WORLDS_576_ORIGINAL_SOURCES_36_LOCAL_EXTRAPOLATIONS_PRESCORE_FREEZE_2026-10-22.md)，后创建提交`38b5bf19`。该协议与A的图模型、原来源、R变量网格及评分都不同。主分支尚**没有**该9世界协议所述的576原来源CSV、36个原局部断点评分、相应独立GitHub机器验收及正式有界结题收据。因而**不得把它记为R214主科学结果已覆盖，或把576原来源加到R214正式192来源后汇总为768个同一实验**。其定位为**R214-SUPPLEMENT-PRESCORE-ONLY**，待单独执行、核验、归档方可有科研证据结论。后冻结不替代先冻结主研究。

## 2. R215 09-006 Difference in Differences：主二期与独立三期补充

A. **正式已结题主研究**：[12世界二期4人工单位×独立/人内持久两噪声3264条原来源冻结](../protocols/R215_DID_12_WORLDS_3264_EXACT_NOISE_SOURCES_PRESCORE_FREEZE_2026-10-22.md)，冻结提交`762c418d`；原数据`research/R215/R215_EXACT_RESULTS.json`、`research/R215/R215_ALL_3264_ORIGINAL_PANEL_NOISE_SOURCES.csv`，正式科学报告`research/R215/R215_SCIENTIFIC_REPORT_2026-10-22.md`、机读收据`research/R215/R215_FINAL_ACCEPTANCE_STATUS.json`。Python3.11和3.12各35测试合计70次通过，[CI run39741076513](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39741076513)三作业success，原机器人数据commit`1e58b4f6`。核心反例：目标政策真ATT2与0两世界有完全同一观察面板联合分布。**R215主研究正式结题仅对应该二期完整源。**

B. **独立三期补充（R215-3P）**：[12世界、两期pre−1与0及post1、768组×时间噪声原来源冻结](../protocols/R215_DID_12_WORLDS_768_ORIGINAL_GROUP_TIME_SHOCKS_PRESCORE_FREEZE_2026-10-22.md)，源冻结commit`d6884f2a`，程序`research/R215/r215_exact_three_period_did.py`，独立命名数据`research/R215/R215_3P_EXACT_RESULTS.json`、`research/R215/R215_ALL_768_ORIGINAL_GROUP_TIME_SHOCK_PANELS.csv`、`research/R215/R215_3P_FINAL_MACHINE_ACCEPTANCE.json`。此补充已有Python3.11/3.12各40测试、合计80次通过，[CI run39741554338](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39741554338)三个job success，原数据机器人commit`6f2a2d89`，实际原始机器数据入main。

**当前结题状态严谨分层**：R215-3P虽已完成实际原资料和CI，机器主结果仍标记`SUPPLEMENT_ARTIFICIAL_E1_AWAIT_CI`，这是机器人来源文件产生时的过程性旧状态；第三job后已出现独立的`research/R215/R215_3P_SUPPLEMENT_SCIENTIFIC_REPORT_2026-10-22.md`（提交`854883e0`），但仍需要对应的事后补充正式机器科学验收；报告存在本身不自动改变原机器结果中过程性旧状态，不能因为主R215已有完成收据就静默将补充材料也标成同一来源科学结题。两期3264、三期768不具有相同随机噪声单位或被解释的实验总体，原来源不能跨协议加权合并成一个样本。
初两次三期workflow失败（run39741409871和39741530183），正式第三次再使用独立命名文件避免覆盖主R215，并在并行main已有变更条件下安全归档。原过程失败均不记为通过的CI证据。

## 3. 目录覆盖、科学证据等级与后续执行

真实原239目录中`09-005`对应正式R214主研究一项、`09-006`对应正式R215主研究一项。附加研究**只能增加独立有界方法证据，不能扩大已完成的原目录条目数**。两项正式研究及R215-3P补充都只有人工数学E1，新增真人E2=0、真实历史E3=0；R073/PESEN v0.1继续冻结。

下一真实原目录条目[09-007 Event Study Design](MODEL_CANDIDATE_CATALOG_v0.1.json)，可登记R216。后续研究每次先确认实际239目录与最新main，写唯一清楚的本项模型协议和互不覆盖的证据文件；如确需两个研究方案，标明主研究/补充及其各自真实完成状态，并保留源hash、CI与真实人类证据边界。仍执行全原目录R学研完成→统一归纳分类→最后模型熔炼。
