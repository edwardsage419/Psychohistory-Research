# MKT177 真实公开太阳黑子序列的逐年预测区间覆盖率
日期：2026-10-31 UTC。目标键：(market,statsmodels_sunspots_bf1aec0,MKT176_fixed_persistence,walkforward_1900_2008_expanding_vs_trailing30_80_90).

## 来源及产品机制关联
公开数据：statsmodels官方sunspots.csv，原样归档于 research/market/mkt176_statsmodels_sunspots_1700_2008.csv，Git blob bf1aec0ce46612fb472d08b66a43115538f405d5；上游 https://github.com/statsmodels/statsmodels/blob/main/statsmodels/datasets/sunspots/sunspots.csv 。官方数据说明 https://www.statsmodels.org/stable/datasets/generated/sunspots.html 。参考 scikit-learn 时间顺序评价 https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html ，2025年预印本综述 https://arxiv.org/abs/2511.13608 ，时间相关数据不自动满足可交换性。产品关联 ProjectionLab 官方 https://projectionlab.com/monte-carlo 和 https://cdn.projectionlab.com/help/plan-vs-chance-of-success ，其公开机制为固定计划与概率情景模拟。这里测试公开评价方法，未调用、注册或测试其产品内部引擎。

输入：1700至2008年309个公开年度SUNACTIVITY观测。状态：预测当年以前已见的年度值和已结算残差。算法：固定上一年数值作为点预测；逐年用截至上一年的绝对残差计算经验分位数；两种历史窗口（expanding、trailing30）乘以两种预先选择的名义覆盖率（90%、80%）。量化规则 k=ceil((n+1)*(1-alpha))，取历史残差第k顺序统计量，区间为点预测加减该半宽；不作数据驱动参数搜索。目标：样本外回溯区间覆盖率、平均区间宽度及时间分块稳定性。反馈：仅离线逐年残差更新，无自动人生决策。解释性：完整透明。隐私：公开物理序列，无用户敏感数据。费用：Node标准库、现有公开免费数据，无新增费用操作。

## 实际执行及结果
固定1900至2008年共109次一步预测，四组区间逐年只读取预测年份之前的数据。V8执行归档程序核心函数，源CSV经GitHub读取；程序语法另行校验。结果：

| 规则 | 命中/109 | 实际覆盖率 | 平均全宽 | 最长连续失配 |
| --- | ---: | ---: | ---: | ---: |
| expanding, nominal 90% | 86 | 78.90% | 70.20 | 2 |
| expanding, nominal 80% | 78 | 71.56% | 53.86 | 3 |
| trailing30, nominal 90% | 97 | 88.99% | 93.51 | 2 |
| trailing30, nominal 80% | 85 | 77.98% | 72.32 | 3 |

90%区间分段命中：expanding 1900至1929年28/30、1930至1959年22/30、1960至1989年21/30、1990至2008年15/19；trailing30分别27/30、24/30、27/30、19/19。较短历史窗口在本样本覆盖率更接近90%，同时平均区间宽度更大，不能将其认定为普遍最优。

负控制：将1981年观测加10000，1980年预测和四组校准半宽完全不变。构造含未来异常值的人工序列，若错误将目标残差纳入90%分位数，半宽由0变成1000，负控制正确揭示泄漏。

## 证据及限制
MARKET_SOURCE_OFFICIAL_DOCUMENTATION + PUBLIC_REAL_PHYSICAL_TIME_SERIES + INTERNAL_NONBLIND_RETROSPECTIVE_METHOD_TEST。此处的90%为名义目标，实际覆盖率可显著偏离。时序依赖及分布漂移使经典交换性覆盖保证不能直接移用；该有限数据回顾评价没有提供正式置信区间、显著性或独立实时版本数据。真实太阳活动数据的预测表现不外推至个人决策。没有验证ProjectionLab产品内部采样、校准或用户决策改善。R系列真人E2=0、历史E3=0。

原始MKT176数据和基线不修改；新程序 research/market/mkt177_sunspots_walkforward_intervals.js。下步MKT178：检查时间分段条件覆盖率与序列相关性下的区间宽度代价，考虑新产品机制避免连续只研究同一厂商。
