# B轨 R187独立直方图科学审计

日期：2026-10-26。状态：PASS_BOUNDED_INTERNAL_E1_AUDIT。

冻结提交 `9ae693193b166cd8ecfa86bd828f8cfaca4434e1`，原始R187来源Git blob `6b1602aec4327d66b0586e8fba771306a8efcc62`，主结果收据Git blob `4f1030eb0c75e2486d41f52ffdca33cdb7503832`。主路线枚举有序等级样本并求概率绝对差，B路线另行枚举三级或二级直方图，用多项式重数与概率重叠质量计算TV，不调用主程序。

本轮实际完成54组TV逐分数一致、108项联合概率归一化、222个直方图配置、9项NULL观测等价负对照、36项观测粗化不等式、36项m单调性。故意把Y≤0阈值误换为Y≤1，18项比较中9项检出不同，另9项两阈值的TV确实相同。此处比较的是两阈值的TV而非原始观测事件本身，故部分错误在TV摘要中无法识别。后续如需检测阈值标签互换，必须比较事件概率及方向，不能仅比较TV。

本轮没有执行真实人类独立留出、概率校准、置信区间重采样或外部研究者独立复现。原R187正式CI历史结果与新增后验研究的CI状态分开，新脚本尚无远端CI PASS。人工E1结果不得计为E2或E3。

独立脚本：`research/evidence_audit/b_r187_ordinal_histogram_overlap_20261026.js`；收据：`research/evidence_audit/B_R187_ORDINAL_HISTOGRAM_AUDIT_RECEIPT_2026-10-26.json`。
