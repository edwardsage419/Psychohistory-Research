# R113 原作者发表汇总与合成识别反例的独立复审协议冻结

日期：2026-10-24。原目录 03-007 Empirical and Normative Expectations，既有 R113。冻结前 main HEAD `70142027360ca25fdf1f707f4a1cea54a1b5c7b2`。仅准备下轮独立复审，**本次冻结本身不构成审计通过**。

## 一手来源与原归档

Bicchieri, Lindemans and Jiang (2014), *A structured approach to a diagnostic of collective practices*, *Frontiers in Psychology* 5:1418, DOI 10.3389/fpsyg.2014.01418，作者公开全文 Table 1 和 Table 2。Table 2 引用 Bicchieri and Chavez (2013) 的**发表汇总数字**，没有原始逐人数据。

既有 R113 原源码 `research/R113/r113_social_norm_expectations_identifiability.py` Git blob SHA1 `14cb67a308fa7bac6207d0f206f3e779324a07af`，原收据 `research/R113/R113_PHASE_A_AGGREGATE_AND_SYNTHETIC_VERIFIED_ACCEPTANCE.json`，历史 CI 39234703188 记录 25 项合成/汇总数学测试。不得修改这些原件。

## 冻结的可反驳检查

1. 独立从 2014 作者原 Table 2 录入四行三列整数：行为 (44,12,44)、回应者经验预期 (44,28,28)、回应者个人规范判断 (100,22,52)、提议者规范预期 (100,10,79)。前两行和为100，后两行分别174、189，必须保留多选含义。
2. 经验预期减实际行为逐项为 (0,16,-16) 个百分点；规范预期减个人规范判断为 (0,-12,27)。若把后两行强制归一化为100或将差值称为因果效应，必须失败。
3. 用独立 Fraction 参数化规则计算两个合成世界：EE=NE=4/5 时两世界行动均为1；EE=NE=1/5 时无条件世界仍为1，条件世界变为0。独立计算器禁止调用 R113 原源码生成结果，原源码仅用于比较。
4. 独立单因素预期变化检查：经验专属世界仅受 EE 变化影响，规范专属世界仅受 NE 变化影响。人工系数为研究者设定，不能冒充原作者估计。
5. 检查 R113 源码、测试、报告的 SHA256 与原机器收据一致，重新执行原 25 项测试。至少两个篡改负例应被拒绝。
6. 任何数值或来源身份不符、CI 未执行、缺少原始文件均记 FAIL/BLOCKED。若全部通过，仅可标记 `PASS_BOUNDED_INTERNAL_INDEPENDENT_AGGREGATE_AND_SYNTHETIC_E1`。已发表的人类汇总是引用背景，不得声称重新获得个体 E2、因果识别或样本外预测。

仅用免费公开英文原文、Python 标准库、公开仓库免费标准 runner。R073 与 PESEN v0.1 冻结。完成所有 R 逐项审计前不统一分类、不熔炼、不开发个人辅助决策产品。
