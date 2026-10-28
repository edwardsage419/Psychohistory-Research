# R243 S39 前缀信息对第四步增量方向的精确预测

日期2026-10-28。冻结协议 `protocols/R243_S39_PREFIX_FORECAST_BRIER_PRESCORE_FREEZE_2026-10-28.md`，先行提交 `dcfcaece2a1e8660e00e9c4605a8ea02480633e2`。原R243九世界144条来源保持不变。

## 主要发现
二分类事件 `Z=1{Y4-Y3>0}`，合法预测信息仅为 `Y0..Yn`，n=0,1,2,3。每世界事件正负各8/16。已知人工联合分布下，边际基线Brier风险恒为1/4。

| 人工世界 | n0 | n1 | n2 | n3 | n3改善 |
| --- | --- | --- | --- | --- | --- |
| ADDITIVE_SYMMETRIC | 1/4 | 1/4 | 1/4 | 1/4 | 0 |
| ADDITIVE_NEGATIVE_SIGMA | 1/4 | 1/4 | 1/4 | 1/4 | 0 |
| ADDITIVE_DOUBLE_SIGMA | 1/4 | 1/4 | 1/4 | 1/4 | 0 |
| ADDITIVE_DRIFT_ONE | 1/4 | 1/4 | 1/4 | 1/4 | 0 |
| COMMON_SHOCK_REPEAT | 1/4 | 0 | 0 | 0 | 1/4 |
| STATIC_HIDDEN_STOCHASTIC_SENSOR | 1/4 | 1/4 | 1/4 | 1/4 | 0 |
| HIDDEN_DOUBLE_SCALE | 1/4 | 1/4 | 1/4 | 1/4 | 0 |
| MULTIPLICATIVE_EM_ZERO_DRIFT | 1/4 | 1/4 | 1/4 | 1/4 | 0 |
| MULTIPLICATIVE_EM_POSITIVE_DRIFT | 1/4 | 1/4 | 1/4 | 1/4 | 0 |

COMMON_SHOCK_REPEAT在Y1后已揭示第一步共享扰动方向，第四步增量方向可完美预测。其余八个世界的第四步扰动独立于合法前缀，预测风险恒1/4。静止隐藏随机传感器、隐藏尺度别名、负扩散符号的观察分布别名仍与ADDITIVE_SYMMETRIC的合法预测结果一致。共享冲击与独立扰动的一步边际可以相同，跨期信息可区别。

非法将Y4纳入预测前缀时，九世界Brier风险全部变为0。此结果仅作为未来信息泄漏负例，严禁作为有效预测成绩。

## 计算与边界
R轨逐行读取原R243 CSV，用精确有理数直接累加每条来源的平方Brier损失。144来源，36合法条件，1152项源闭合与损失运算。B轨只读原正式观察联合PMF，使用独立条件二阶矩公式审计180项字段，失败0，故意篡改999被检出。属于内部数学复核，外部独立复现0。

此为已知人工机制的oracle分析，没有现实训练数据、样本外验证、概率校准或真实预测效用。有限四步Rademacher噪声与高斯Brownian不同，不能声称连续SDE结论。原R243正式有界E1验收保持不变，新增E2=0、E3=0；R073模型与评分规则、PESEN v0.1冻结。没有启动GitHub Actions。
