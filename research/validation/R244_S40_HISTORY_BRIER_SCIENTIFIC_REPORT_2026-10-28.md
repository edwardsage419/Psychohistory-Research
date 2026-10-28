# R244 S40：历史信息对二态马尔可夫预测风险的影响

日期：2026-10-28。预评分冻结提交 `8b8a64314b62f1557993002ca76a7f0be6a4b366`。原R244九个人工世界、1152条原外生来源、原正式验收均未更改。主线 E1 精确人工研究。

## 结果

预测Y3，比较仅使用Y2与同时使用Y1、Y2的真实联合分布下oracle Brier风险。全部为有理数精确计算。

| 世界 | 仅Y2风险 | Y1与Y2风险 | 额外历史收益 |
| --- | ---: | ---: | ---: |
| IID_FAIR | 1/4 | 1/4 | 0 |
| PERSISTENT_3OF4 | 3/16 | 3/16 | 0 |
| ANTIPERSISTENT_1OF4 | 3/16 | 3/16 | 0 |
| ABSORB_ONE | 1/16 | 1/16 | 0 |
| TIME_ALTERNATING_RATE | 3/16 | 3/16 | 0 |
| LATENT_RATE_MIXTURE | 1/4 | 9/40 | 1/40 |
| STATIC_HIDDEN_SENSOR_ALIAS | 3/16 | 3/16 | 0 |
| COMPLEMENT_HIDDEN_COORDINATE_ALIAS | 3/16 | 3/16 | 0 |
| FIXED_SWITCH_POLICY | 1/4 | 0 | 1/4 |

隐藏速率混合世界从1/4降至9/40，收益1/40。固定隐藏切换策略世界从1/4降至0，收益1/4。其他七个人工世界历史收益均为0。原R244冻结的条件Markov缺陷在这两个世界分别为1/5与1/2。风险收益是任务特定的概率加权量，Markov缺陷是最大条件差，两者数值不应直接等同。

额外检查F0、F1风险及各合法条件正支持；泄漏负例故意把目标Y3加入预测条件，九世界风险全为0，明确非法。PERSISTENT_3OF4、STATIC_HIDDEN_SENSOR_ALIAS、COMPLEMENT_HIDDEN_COORDINATE_ALIAS三世界所有合法风险完全相同，隐藏真值机制仍不可由这些风险区分。

## 算法、审计与局限

R程序读取原R244完整四时点观察联合PMF，按条件格子使用正例质量和总质量计算Brier风险。B程序只读取原R244七位外生来源CSV，聚合原始观察标签计数，按整数二项方差公式独立计算。实际核对9世界×(5个风险各2字段+1个历史收益)=99项字段，失败0。故意将一个风险改成999后B程序拒绝，错误注入通过。B不调用R源码或R计算输出作为计算输入，最后才与归档收据比较。两条路线均使用同一项目冻结人工资料，属于程序性独立复核。

本轮没有拟合真人行为、训练测试分离、样本外预测、概率校准或外部团队复现。原R244正式有界E1验收保持不变；E2=0、E3=0。R073模型与评分规则、PESEN v0.1冻结。CI未启动，新增费用0，账单余额未独立核验。

程序：`research/validation/r244_s40_history_brier_20261028.js`。机器收据：`research/validation/R244_S40_HISTORY_BRIER_RECEIPT_2026-10-28.json`。B轨：`research/evidence_audit/b_r244_s40_source_count_20261028.js`。
