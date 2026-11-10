# C015补充：Chen与Chen（2014）区间中点符号一致性核验

track: theory
subflow: C
date: 2026-11-10 (Asia/Singapore)
observed_main_head: 0484eed67dca2128d39876a3b4b74c2e8904c731
target_key: (theory-C,ChenChen2014,PLoSONE9e87752,reported_estimate_interval_consistency)
status: PARTIAL
prior_record: research/decision_methods/C015_CHEN_CHEN_2014_N_OF_1_INTERVAL_CONSISTENCY_2026-11-10.md

## 原始来源与实读范围
Xinlin Chen, Pingyan Chen (2014), A Comparison of Four Methods for the Analysis of N-of-1 Trials, PLOS ONE 9(2):e87752. DOI: https://doi.org/10.1371/journal.pone.0087752
本轮直接读取出版社公开HTML的 Methods（Model 1至4）、Examples（两个真实案例）及Discussion，特别是Examples第一段。未获得作者原始案例数据、SAS脚本、勘误全文；其余附录表未独立复算。

## 独立新增算术证据
原文第一案例Model 1/2报告估计值 -137.7，95% CI (-38.4, 313.8)；区间中点 (-38.4+313.8)/2 = +137.7，半宽176.1。
Model 3报告估计值 -118.7，95% CI (-63.0, 300.3)；区间中点 (-63.0+300.3)/2 = +118.65，按一位小数约为 +118.7，半宽181.65。
因此两个置信区间的中点与相应点估计的**绝对值**一致，仅符号相反（第二项存在四舍五入误差）。如果这些区间使用以点估计为中心的对称t或Wald构造，估计值负号误植是高度具体、可检验的候选解释。另一个候选解释是点估计与区间采用了相反的A-B/B-A方向。原文并未在该段交代足以确认原因的区间计算细节。

重要边界：一般置信区间不必包含点估计（例如某些偏态百分位法区间），所以“点估计在区间之外”本身不构成普遍数学矛盾。本次中点精确匹配提供了更强的**报告内部可疑证据**，仍不能宣称已证明论文出错或确定更正数值。

## 方法学影响
作者模拟的配对t检验将不同个体的周期差合并，Model 1的说明明确不计个体间效应。其推荐范围是指定的正态、CS/AR协方差、3或4周期、0/20%上一期残留等模拟条件。模型选择的真实因果效度仍取决于随机化、洗脱、时变趋势、缺失及个体内依赖。单个临床案例的报告疑点不能推翻所有模拟结论。

## 可证伪关口与执行状态
1. 找到原始OTCD案例论文及其效应方向定义、数据或可复算表；复核点估计和CI的共同方向。
2. 检查出版社正式勘误及作者可公开获得的代码。
3. 若原始数据不可得，保留UNKNOWN，不自行改写作者数字。

原始出版HTML指定段落阅读 COMPLETE；区间中点手工算术核验 COMPLETE；作者原始数据复算 NOT_RUN；正式勘误全面排查 NOT_RUN；外部真人预测 NOT_RUN；CI NOT_RUN。未调用收费服务。R073和PESEN v0.1冻结状态不变；本记录属于C015补强，未创建C016或TH编号。
