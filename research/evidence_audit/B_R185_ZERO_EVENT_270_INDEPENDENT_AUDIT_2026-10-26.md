# B轨：R185零事件NB与Poisson 270组独立枚举复核

日期：2026-10-26。状态：PASS_BOUNDED_INTERNAL_NUMERIC_AUDIT。对应计算前冻结提交 `8fc8a534280e97f35d036dd83700c1acceb27b7a`。

独立读取原R185来源JSON，Git blob `857dcb286bf66692952930fc736e133bc3d2b3aa`，135个固定来源与形状世界，每世界两组。主程序采用BigInt有理数幂计算NB零概率及解析Brier风险。B程序单独通过r次乘法计算NB零概率，完整枚举未来零与非零两个结果的Brier损失，并核对R收据。

实际通过270项NB零概率身份核对、540项两预测器风险核对，最大绝对误差1.6653345369377348e−16。故意把NB零概率的指数由r变成r+1，270组全部检测到不同概率。全部人工来源与shape未变更。

范围限制：B为项目内部另一路数值计算，尚未执行GitHub Actions远端CI；真实数据独立预测、概率校准外推、外部团队复现均未完成。NB预测使用人工真均值，不代表可实施的真人预测器。此B结果不升级R185原正式有界E1结题。

脚本：`research/evidence_audit/b_r185_zero_event_binary_enumeration_20261026.js`。机器收据：`research/evidence_audit/B_R185_ZERO_EVENT_270_AUDIT_RECEIPT_2026-10-26.json`。
