# R066：群体意见动力学的可检验三模型研究

日期：2026-10-16。当前状态：**ACTIVE**。该编号研究群体层认知互动与观点演变，接替已 [CLOSED_BOUNDED 的 R065](../R065/R065_FINAL_ACCEPTANCE_AND_CLOSURE_2026-10-16.md) 成为下一条研究主线。

## 事前协议与真正取得的成绩

- [已冻结的三模型研究协议](../../protocols/R066_OPINION_DYNAMICS_THREE_MODELS_2026-10-16.md)：DeGroot 线性加权、Friedkin–Johnsen 固守/易感性、Hegselmann–Krause 同步有界信任。
- [基础数学实现](r066_three_opinion_models.py)与 [25 项纯合成输入测试](test_r066_three_opinion_models.py)。
- [结果与来源审计报告](R066_E1_AUDIT_AND_E2_DATASET_GATE.md)以及 [机器可验结果](R066_E1_THREE_MODEL_RESULTS.json)。
- [GitHub Actions run 38845611874](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38845611874)：completed/success，25 tests OK，合成 E1 三模型原始数值均复现。
- 公开社交互动时间序列数据候选：Monti、De Francisci Morales 与 Bonchi 2020 KDD 的 [learnable-opinion-dynamics](https://github.com/corradomonti/learnable-opinion-dynamics)，固定 master commit `5d31ba59e716e5bde85e4c56b9cdacc3920aaaf6`；四份压缩数据的 Git blob 和文件大小已核查，但数据行尚未读入，本研究不声称已验证真实意见数据。

第一轮固定合成意见 `[0,0.2,1]` 的更新分别为 DeGroot `[0.4,0.4,0.4]`，FJ `[0.2,0.3,0.7]`，HK `[0.1,0.1,1.0]`。不同结果展示机制设计差异，**不能作为任何实际社会的预测。**

## 下一条 E2 门控

首先确认真实数据中的重复个体意见观测是否可操作化，而非仅有互动痕迹或赞同代理。审核真实原始数据、隐私再分发限制、匿名主体完整性与时间上的训练/测试隔离。若不满足识别条件，明确标记 BLOCKED，再寻找更合适的人类实验数据集。

**`R066_E1=PASS`；`R066_EMPIRICAL_E2=OPEN`；`PESEN_v0.1=FROZEN`。**


## E2 双候选真实文件、测量可用性审计（2026-10-16）

[事先冻结的审计协议](../../protocols/R066_E2_TWO_DATASET_MEASUREMENT_AUDIT_2026-10-16.md) · [正式研究报告](R066_E2_TWO_DATASET_SOURCE_AND_MEASUREMENT_AUDIT.md) · [原始数据匿名聚合审计 JSON](R066_E2_TWO_CANDIDATE_RESULTS.json) · [程序](r066_e2_measurement_source_audit.py) · [13 项合成测试](test_r066_e2_measurement_source_audit.py)。

[真实 GitHub Actions run 38861027481](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38861027481)：两个作业均 completed/success。确实下载并按 Git blob SHA1 校验了 Monti 2020 Reddit 的 4 个原始压缩文件，共 519,655 行，和 Okawa–Iwata 2022 的帖子意见数据 9,944 行、300 个不同 `user_id` 值。对后者，作者 README「100 名最活跃用户」与文件标识数量不一致，不能凭这次统计决定实际人的数量。所有数据均只输出无个人身份的聚合结果，不在本仓库分发原始个体记录。

**两个真实来源的可重放数据结构验证 PASS；经验三模型对比因没有同时成立的重复连续意见测量与真实社交影响网络，仍 `BLOCKED_MEASUREMENT`。** 另已找到 2026 年 16 村庄调查和网络干预论文（DOI `10.1017/nws.2026.10038`）作为高匹配度候选，但关联 Dataverse DOI 的原始数据尚未取得，不能计作真实数据测试。

**截至本节：`R066_E1=PASS`、`R066_SOURCE_AUDIT_E2=PASS`、`R066_EMPIRICAL_MECHANISM_E2=BLOCKED`、`R066_E3=OPEN`、`PESEN_v0.1=FROZEN`。**


## 新进展：2026-10-16 Larson–Lewis 真实纵向网络与态度数据

[统一源证据/方法审计](R066_E2_LARSON_LEWIS_REAL_SOURCE_AND_NETWORK_AUDIT.md) · [Dataverse 目录版本](R066_E2_DATAVERSE_CATALOG_RESULTS.json) · [三文件 SHA256/66 列结构](R066_E2_LARSON_LEWIS_V1_SCHEMA_RESULTS.json) · [原作者代码本/变量映射](r066_larson_lewis_semantic_mapping.py) · [初始错误身份联结证据](R066_E2_VILLAGE_NETWORK_JOIN_AGGREGATES.json) · [按作者家庭映射派生的匿名网络统计](R066_E2_AUTHOR_HOUSEHOLD_NETWORK_RESULTS.json)。

真实原始来源为 Harvard Dataverse `doi:10.7910/DVN/RAHSVM`，V1.0，CC0。已核验下载表格 2,125 行×66 列、R 作者脚本与 DOCX 代码本，全部有精确 SHA256；GitHub Actions 目录 [38862426339](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38862426339)、原始文件 [38862848577](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38862848577)、字段映射 [38863264795](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38863264795)、初始直接联结 [38863706284](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38863706284)、原作者源码审查 [38864150195](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38864150195)、家庭网络计算 [38864457996](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38864457996) 均已真正完成。

主要成果：**16 个村庄、1,872 行基线/末次六题态度配对完整记录**；按照作者 R 的家庭成员映射与四类提名方式，经 Python 产生 8,659 条匿名去重家庭关系与 2,067 个至少一条关系的家庭节点。早先直接把 `ego` 当成唯一家庭节点出现重复和低匹配，已保留原失败记录，不能拿它否定经过家庭层转换的关系数据。作者 R/igraph 与 Python 的**逐边一致性仍未验证**，现阶段无 DeGroot/FJ/HK 真人数据参数拟合或真实预测名次。

状态：`R066_SOURCE_AUDIT_E2=PASS`；`R066_AUTHOR_DERIVED_HOUSEHOLD_NETWORK=PASS_BOUNDED`；`R066_SOURCE_R_PARITY=OPEN`；`R066_REAL_THREE_MODEL_PREDICTION=OPEN`；`PESEN_v0.1=FROZEN`。
