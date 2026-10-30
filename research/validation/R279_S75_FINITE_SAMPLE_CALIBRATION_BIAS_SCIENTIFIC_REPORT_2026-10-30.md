# R279 S75 科学报告：四位样本经验校准分解的精确偏差

日期：2026-10-30 UTC。研究对象：原 R279 的三个 Bernoulli 双组生成世界和三种固定预测政策。新增冻结：research/validation/R279_S75_FINITE_SAMPLE_CALIBRATION_BIAS_FREEZE_2026-10-30.md，冻结提交 fb5fbd79c2589842d4b4ae27d59fe95f087cade4。已阅读原 R279 结果，研究为非盲态探索性人工 E1。原 R279 的 CLOSED_BOUNDED_E1 正式状态未变。

## 问题
原 R279 的 population Murphy 分解使用真实组发生率。本轮检查每组只有两次观察时，将真实发生率替换为样本分桶发生率，对可靠性 REL、分辨力 RES 和不确定性 UNC 的估计产生什么偏差。每个世界完整枚举16个有序四位来源，九世界共144行，99行正质量，45行零质量保留。

## 冻结定义与计算
每条来源先按相同预测概率 q 合并桶，再计算经验 REL=sum w(q-o_q)^2，经验 RES=sum w(o_q-o)^2，经验 UNC=o(1-o)，及四位均值 Brier。逐行满足 Brier=REL-RES+UNC。用原 DGP 概率精确加权，不把144行当成144名独立真人。

| 真世界 | 政策 | population REL | E[empirical REL] | REL偏差 | P(empirical REL=0) |
| --- | --- | ---: | ---: | ---: | ---: |
| CALIBRATED_RATE | ORIGINAL_BUCKETS | 0 | 3/32 | 3/32 | 0 |
| CALIBRATED_RATE | FLAT_HALF | 0 | 3/64 | 3/64 | 59/128 |
| CALIBRATED_RATE | REVERSED_BUCKETS | 1/4 | 11/32 | 3/32 | 0 |
| DETERMINISTIC_GROUP | ORIGINAL_BUCKETS | 1/16 | 1/16 | 0 | 0 |
| DETERMINISTIC_GROUP | FLAT_HALF | 0 | 0 | 0 | 1 |
| DETERMINISTIC_GROUP | REVERSED_BUCKETS | 9/16 | 9/16 | 0 | 0 |
| INVERTED_RATE | ORIGINAL_BUCKETS | 1/4 | 11/32 | 3/32 | 0 |
| INVERTED_RATE | FLAT_HALF | 0 | 3/64 | 3/64 | 59/128 |
| INVERTED_RATE | REVERSED_BUCKETS | 0 | 3/32 | 3/32 | 0 |

对于 CALIBRATED_RATE 和 INVERTED_RATE，两个组的 Bernoulli 方差之和为3/8。两桶政策 REL 期望偏差为3/32，RES 期望偏差为3/64，UNC 期望偏差为负3/64；单桶 FLAT_HALF 的 REL 期望偏差为3/64，RES 偏差0，UNC 偏差为负3/64。DETERMINISTIC_GROUP 方差为0，各分解偏差为0。九世界 E[样本 Brier] 与原 population Brier 全部精确相等。

## 关键反例
CALIBRATED_RATE + ORIGINAL_BUCKETS 的 population REL=0，说明固定预测概率按真实条件率完全校准。但每个预测桶只有两次观察，经验桶发生率只能是0、1/2或1，永远不等于报告的1/4或3/4，因此经验 REL=0 的概率严格为0，期望经验 REL=3/32。由此不能把有限样本 REL 大于0直接解释成预测模型真实失准。

FLAT_HALF 在相同 DGP 中的 population REL 也是0，样本经验 REL=0 的概率为59/128；该政策在原 R279 的 population RES 为0。校准指标的抽样性质、分辨力及真正样本外评分必须分开报告。

## 方法与核验
R 路线：V8 中直接枚举全部144个有序来源，使用精确 BigInt 分数，逐行检查 Murphy 恒等式并保存完整 CSV/JSON。B 路线：Python Fraction 在独立9个组成功计数组合上计算 REL 偏差、P(REL=0) 与 P(REL<=population REL)，与 V8 九组结果相同；另由 Bernoulli 方差恒等式验证三项偏差。远端持久化收据由独立 V8 检查器重新读取并逐行核对144行、九组、全部来源质量和摘要，七项错误注入全部拒绝。

程序：research/validation/r279_s75_finite_sample_calibration_20261030.py。归档 Python 源码的原生命令行执行 NOT_RUN，原生 Node CLI NOT_RUN。实际运行的是本轮 V8 精确枚举、Python 独立小型解析计算和 V8 严格收据审计。归档 Python 的完整 CSV/JSON 字节再生验收仍 OPEN，不能称为已通过。

## 科学与验收边界
A01 问题范围 PASS；A02 原 R279 来源与冻结 PASS；A03 V8/独立数学计算及持久化审计 PASS，归档 Python 原生命令行 OPEN；A04 七项反例注入 PASS；A05 人工 E1 范围 PASS；A06 本补充的正式完整科学验收 OPEN。研究结论是固定有限 DGP 的精确数学性质，未进行真人样本外预测、概率校准外推、外部团队复现。E2=0，E3=0。R073 与 PESEN v0.1 冻结。

原始 R279：research/R279/R279_FINAL_ACCEPTANCE_STATUS.json；原冻结：protocols/R279_FORECAST_CALIBRATION_9_WORLDS_144_FULL_SOURCE_PRESCORE_FREEZE_2026-10-23.md；理论来源 Murphy 1973 DOI 10.1175/1520-0450(1973)012<0595:ANVPOT>2.0.CO;2。下一步补齐原生 Python/Node 命令行及归档字节核验，然后推进 R280 互补问题。
