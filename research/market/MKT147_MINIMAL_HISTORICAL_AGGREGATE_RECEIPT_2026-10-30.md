# MKT147 最小历史聚合审计收据：数据最小化与可验证边界

日期：2026-10-30 UTC。目标键：(market,HealthConnect,MKT147-v1,minimal-asof-aggregate-receipt-and-identity). 基线：R286 S82 后 main 532ab5698101d653a1e3a7019e7315100f7db1fd；本轮实际写代码前最新 main 为 eef27cd18d938be8ce9045933d5c70fb46d35334，包含理论轨 TH151。状态：COMPLETE_BOUNDED_ARTIFICIAL_E1。MKT145研究当前来源优先级，MKT146研究旧聚合不可识别；本轮独立研究如何保存最少元数据及其证明力。

## 英文官方资料及产品机制

Android Developers, Read aggregated data, https://developer.android.com/health-and-fitness/health-connect/aggregate-data （2026-10-30读取）：Health Connect 的 Activity/Sleep 聚合依据用户设置的应用优先级去除重叠来源；用户可以修改优先级，结果随之变化。API 支持按 DataOrigin 过滤。其他数据类型的聚合语义不同。默认历史读取受授权时间窗口限制，卸载重装后授权需重新取得。

Android Developers, Synchronize data, https://developer.android.com/health-and-fitness/health-connect/sync-data （2026-10-30读取）：clientRecordId/clientRecordVersion用于记录身份与版本；DeletionChange仅返回记录ID；变化令牌可能过期，需要重新读取和去重。官方并未保证第三方能重建任意过去时点的用户优先级，历史优先级回放能力在已读页面中为 NOT_DOCUMENTED，不能据此断言绝对不存在。

机制矩阵：真实潜在输入为来源记录、来源版本、优先级、时间窗口和授权；状态为来源版本、规则版本、查询时点、权限覆盖；官方算法是Activity/Sleep按优先级聚合，人工脚本采用逐分钟优先来源模拟，两者不能视为同一实现。目标为避免重复计数、追踪评价变化；反馈包括用户改优先级、记录更新及撤销授权；解释需区分原数据变化和规则变化。隐私风险为时间戳、来源ID及历史状态可泄露生活模式；费用仅使用公开文档与现有执行环境，未注册或购买产品，未使用计费API。官方功能说明没有独立的长期人生决策效果验证。

## 25项人工E1可执行测试

源码：research/market/mkt147_minimal_asof_receipt_evidence_gate_20261030.js，远端 Git blob 925092f44a6392cb934911bd0e41d4760316c634。源码经 V8 动态执行25项检查通过，远端内容回读与提交源码完全一致；原生Node CLI未执行。

两个20分钟人工世界均在B来源优先时得到1300步；A优先时分别得到1500与2500步。人工收据仅保存 snapshot_id、source_version、rule_version、priority、window、asof_utc、algorithm_version、permission_complete、source_complete 和 aggregate_value，不保存原始步数记录。仅凭当前1300聚合不能还原旧A优先聚合。

测试严格区分四类状态：ABSTAIN表示必需字段、权限或来源完整性缺失；CLAIM_ONLY表示收据有数字但无可供复算的原始数据；CONSISTENT_INTERNAL表示在给定原数据和上下文版本标签下人工重算一致；FAIL表示版本、窗口或可重算聚合不一致。25项包括缺字段、改版本、缺权限、非法值、重复来源与篡改总量。特别保留一个重要负例：将世界1的原始来源替换成世界2，沿用世界1的版本标签，B优先总量仍为1300，人工检查器返回CONSISTENT_INTERNAL，说明仅对聚合值复算不足以证明来源身份与真实性。

本轮标签为人工非加密版本名，未计算SHA256、签名或可信时间戳；即使未来引入加密摘要，摘要也只在有可信原始输入和验证根时提供绑定，不能独立证明记录真实或授权完整。对低熵健康记录的无盐摘要可能带来字典猜测风险。若需要独立历史重放，必须在合法授权、最小化保留和可审计的原始来源之间另作取舍，不能把保留一个数字称为充分可验证。

## 证据等级与后续

OFFICIAL_DOC：上述英文平台文档。ARTIFICIAL_E1：25项固定人工测试。INFERENCE：收据的声明、内部一致性与独立真实性是三个不同证据关口。真实Android设备0，独立产品有效性实验0，E2真人样本外预测0，E3历史预测0。未接触真实健康数据；未建立人生效用权重；R073/PESEN v0.1冻结。未触发Actions，新增费用0，GitHub账单及免费额度未核验。

下一MKT148：研究来源版本不可访问、优先级发生变化与用户撤销授权同时出现时，最小收据能否给出可信的上下界；同时扩大对Exist、ARDA等产品公开机制的轮换审阅，避免持续只研究一个平台。