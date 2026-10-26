# E025 R189两点随机截距极端计数的720项独立只读复算

日期：2026-10-26（Asia/Singapore）。轨道：operations。状态：COMPLETE_BOUNDED_READONLY_EXACT_E1。独立检查前main HEAD `9e6141b8edf3f7c8144586b4e7cd303827ce0909`；MKT056随后仅新增market独立报告。今日E004已完成全轨日检，E024已审R187；本轮只针对R189最新实质增量、R188归档范围和本周F专题做去重及证据等级检查。零新增费用，未启动Actions或接入个人数据。

## 1. GitHub状态、归档和冻结边界

由GitHub连接器比较 E024 末尾HEAD `293c16fc6035e4eecc6518a3f38f3db377106f5d` 与本轮开始main，确认向前18次提交、无落后；新增包括R188和R189预计算冻结、主算法、收据、B独立算法及报告、A轨真人数据准备和TH059理论笔记。MKT056已独立写入 `research/market/`，不覆盖其他轨。

R189冻结协议 `protocols/R189_CLUSTER_EXTREME_TAIL_POSTSCORE_PRECOMPUTATION_FREEZE_2026-10-26.md` Git blob `e1620628faeca7cf4bcfd972a8f9327795bcfdb4`，冻结提交 `a2c5b488e482e074542eb4d510515d7de811e7d6`。比较冻结提交至main，结果为向前8次提交，后续主收据、报告和B轨成果均为新增文件。原始来源 `research/R189/R189_EXACT_RESULTS.json` Git blob `29180ee83570e4faef528b85d8d4daaada368344`，与冻结协议指向的对象完全一致。新增主收据 `research/validation/R189_CLUSTER_EXTREME_TAIL_48_EXACT_RECEIPT_2026-10-26.json` Git blob `5d7f5a0b0b32bea1d4d6d3d48395ca45059fca3c`，提交 `c9e0e8e80c79806fc4d71116c3993d6dfe8223cc`。B轨科学报告 `research/evidence_audit/B_R189_LATENT_EXTREME_INDEPENDENT_SCIENTIFIC_AUDIT_2026-10-26.md` Git blob `bd78bfc19c095bc43935d1039772eaddb1e36936`。

## 2. 独立方法和720项实际检查

本轮独立JavaScript BigInt有理数实现，直接读取原R189全部24个人工世界和主48条收据。完全从每世界的o、t、h、x计算隐藏成功率
`p1=(o*t^x*h)/(1+o*t^x*h)`、`p2=(o*t^x/h)/(1+o*t^x/h)`，按等权双点混合计算 `P(K=k)=C(n,k)*[p1^k*(1-p1)^(n-k)+p2^k*(1-p2)^(n-k)]/2`。没有调用R主脚本或B轨算法，且不仅比较已归档的两个端点。

每个条件核对全部 `n+1` 个原始PMF单元、归一化、来源边际成功率、主收据边际成功率、主收据7个端点及差额字段。对于n=2额外独立计算 `Cov=(p1-p2)^2/4` 并核对来源协方差和总极端差额两倍协方差恒等式。

**总计720项有理数身份检查，720通过，0不一致。** 24世界×2条件=48条件，其中h=1的24条件两端差额均0；h=3的24条件两端差额均严格正；n=2的24条件均满足两倍协方差恒等式。最小严格正总极端差额 `9/392`；最大 `25/128`，发生于world17、x=1、n=4、o=1/3、t=3、h=3。全部与主收据摘要一致。额外核对原PMF全支持分布，超出主报告仅复算端点的检查范围。

固定例o=1/3、t=3、h=3、n=2：x=0时真P0=53/100、独立P0=49/100，真P2=13/100、独立P2=9/100，合计极端概率超额2/25；x=1时真P0=真P2=5/16，独立两端各1/4，合计超额1/8。它们是固定人工概率恒等式，不是对真实人群的拟合收益。

## 3. 证据等级、CI及其他轨道

R189本次为 `INTERNAL_MATH_E1`，同一项目B轨已归档384字段精确复核及人工错误基线负对照。两套内部方法加本轮独立实现不构成外部研究团队复现；真人E2=0、历史E3=0、真实样本外预测=0。冻结的R073和PESEN v0.1均未被本轨修改。

针对R189主收据提交 `c9e0e8e80c79806fc4d71116c3993d6dfe8223cc`，GitHub关联workflow runs返回空数组，combined status亦空；这些接口覆盖有限，结论仅为**该提交远端CI PASS未证实**。不能把归档提交当作CI验收。

R188已在独立路径归档180世界×6整组删除×4种θ共4320个精确斜率，以及B轨5040项方法复核。该数字来自已读取的R188科学报告和冻结协议，本轮没有再次独立计算4320项，故只记为 `ARCHIVED_CLAIM_NOT_RECHECKED_HERE`。A轨Kuper-Smith与Korn 2025双人镜像准备程序已归档，但真实CSV未在最新轮重执行、许可仍待确定、R073第二独立真人复现未获批准；不得将合成SELFTEST计为E2。

今日全轨E004已归档 `research/operations/E004_DAILY_READONLY_R165_AND_C003_D002_2026-10-26.md`（Git blob `0117e933f6238f34c408bbb67ce195eeed461ae3`），本轮没有重复创建日检。2026年第44周F002已归档 `research/privacy_safety/F002_CONSENT_REVOCATION_DERIVED_DATA_BACKUP_LIFECYCLE_2026-W44.md`（Git blob `d76d0ea536bf41162cfe570e4a7db2bfeeb7e4ee`），状态为有限规范与源码研究已完成，F003为后续候选；本轮未写F目录。MKT056的预测撤回与隐私删除不同义列为F后续候选风险。

## 4. 治理问题与后续

E025-01 CLOSED_BOUNDED：R189原始24世界48条件720项独立精确核对一致；冻结协议与原始来源Git blob已核验。
E025-02 OPEN_CI：R189指定主收据提交未建立远端CI PASS证据；未经免费额度确认不主动启动CI。
E025-03 OPEN_EVIDENCE：R189仍仅人工E1，禁止宣传真人效果或外部独立复现。
E025-04 OPEN_R073：第二真人实验的镜像行检验、许可、信息集和冻结评分适配待完成。
E025-05 OPEN_LEGACY：R181交付语言/文件名偏离、R136原负对照失败、R170全状态、R175来源工作簿、R176后期复算、original239逐项证据审计仍待其他轨处理。
E025-06 SCOPE：本轮仅核验指定R189来源、协议、报告和新增提交，没有全仓哈希巡检、全部文件名冲突检查或账户整体账单核验。主动新增费用0，GitHub免费权益使用额度未独立核实。

下一次E优先独立审计R188删组结果中完整样本与删组公式的一致性，或检查新增R190及R181冻结交付偏离说明。维持只读为主，不擅改任何R/B/A/F/TH/C/D成果或共享索引；先完成R系列，再归纳分类，最后熔炼。
