# C015 Chen and Chen (2014) N-of-1 统计报告内部一致性审计

track: theory
subflow: C
run_date: 2026-11-10 (Asia/Singapore)
observed_head: caa409101c23285c3fa08d75612765f4ff3a03d2
target_key: (theory-C,ChenChen2014,PLoSONE9e87752,reported_estimate_interval_consistency)
status: PARTIAL
source_links:
  - https://doi.org/10.1371/journal.pone.0087752
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC3913644/
evidence_scope: publisher open full text HTML, Methods sections Models 1–3, Results abstract and Discussion, two Real Data Examples paragraphs; original tables and supplemental data not independently reproduced

## 独立增量及证据性质
Xinlin Chen and Pingyan Chen (2014), A Comparison of Four Methods for the Analysis of N-of-1 Trials, PLOS ONE 9(2):e87752. 原文研究3及4周期的N-of-1设计，使用复合对称或AR(1)协方差，比较配对t检验、差值混合效应、混合效应及汇总元分析；设定0或20%残留效应。作者在这些模拟条件下推荐配对t检验，残留效应时考虑混合模型。这是有限模拟条件下的性能比较，不能推广为所有单人序贯决策的最优分析方法。

**原文内部数值一致性疑点**：Real Data Examples 第一例报告配对方法估计 -137.7，同时报告95% CI (-38.4,313.8)；混合模型估计 -118.7，同时报告95% CI (-63.0,300.3)。两项点估计均不在所列95%置信区间内。第二例点估计及区间未出现这一明显矛盾。原文是否发生负号、端点顺序或排版错误尚未确定；不得擅自改写作者数值。此为文献报告审计，非模型新发现，需核对作者原始数据及勘误后再判断原因。

## 适用范围与竞争解释
本研究针对单人多周期干预设计的估计报告可靠性，与C005的微随机试验可用性和近端效应、C006的单人序列季节性与负控识别问题不同。混合模型可调整周期及前期残留效应，但作者仅设定上一期残留，且模拟未覆盖缺失数据、不平衡周期及期内重复测量。观察到估计与区间矛盾的候选解释包括排版错误、区间方向定义不同或计算/报告错误；现有文本无法判别。

可观测量：每期处理顺序、周期、处理结果、残留指标、缺失指示、个体内相关、点估计及置信区间端点。测量误差、时间趋势、carryover与非随机退出均可能影响识别。可证伪检查：使用原作者明确的区间定义和原始数据重算，确认区间是否确实对应同一参数；在原始数据不可得时保持UNKNOWN。

## 边界及执行
原创数值审计：两处区间包含关系的直接算术核查 COMPLETE。作者源数据重算 NOT_RUN；独立模拟 NOT_RUN；真实个人实验 NOT_RUN；长期人生因果推断 NOT_RUN；CI NOT_RUN；billing_checked: no paid services invoked, actual account billing NOT_VERIFIED.
next_action: 查作者原始数据/勘误；避免将本文模拟推荐泛化到非稳定长期生活决策。D 2026-W46 仍待合格专题，未借此归档。
