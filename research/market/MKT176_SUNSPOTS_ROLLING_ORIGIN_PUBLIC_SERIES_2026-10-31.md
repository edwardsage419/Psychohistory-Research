# MKT176 公开真实时间序列的滚动起点评价
日期：2026-10-31 UTC。目标键：(market,statsmodels_sunspots_1700_2008,public_domain_snapshot_bf1aec0,rolling_origin_1900_2008_four_prespecified_baselines)。

## 来源和适用范围
statsmodels 官方源数据 https://github.com/statsmodels/statsmodels/blob/main/statsmodels/datasets/sunspots/sunspots.csv ，Git blob bf1aec0ce46612fb472d08b66a43115538f405d5；官方数据描述 https://github.com/statsmodels/statsmodels/blob/main/statsmodels/datasets/sunspots/data.py 明确1700至2008年309个年度太阳黑子活动值、National Geophysical Data Center来源及public domain声明。此处保存原样CSV副本。源数据为公开物理时间序列，非真人个人信息。
市场产品关联：ProjectionLab https://projectionlab.com/monte-carlo 提供情景模拟，上一轮MKT175关注Brier和时间外评估。本轮引入独立真实公开序列检验评估方法，未测试ProjectionLab的内部算法，也未证明个人决策产品准确性。其他厂商本轮无经核验的新发布或价格变化，不重复记录。
输入：YEAR、SUNACTIVITY。状态：按年度递进的历史可见窗口。算法：每年只用该年之前的值预测当年；预先固定四条基线，persistence前一年值、lag11前11年值、trailing11过去11年均值、expanding历史全期均值。目标：比较一年期点预测MAE/RMSE/偏差。反馈：离线滚动评估，未实现在线自修正。解释性：全部四条规则透明。权限/隐私：只处理公开聚合物理数据。费用：公开免费数据和标准Node.js；无购买/注册/计费API。

## 实际执行
读取原样309行CSV，冻结评估区间1900至2008年109个年份，不依据评估成绩重新选择参数。V8 JavaScript核心程序实际执行并通过，未来年份数值干预的无泄漏检查PASS。
| 模型 | MAE | RMSE | Bias |
| --- | ---: | ---: | ---: |
| persistence | 21.719266 | 28.605886 | 0.084404 |
| lag11 | 23.475229 | 32.246977 | -1.796330 |
| trailing11 | 37.089491 | 43.793975 | 0.008590 |
| expanding | 38.420798 | 49.264564 | -14.242375 |

四个时间段的MAE（persistence/lag11/trailing11/expanding）：
1900至1929：14.4733 /16.1400 /25.1533 /24.1623；
1930至1959：25.9633 /26.7400 /42.8270 /48.7359；
1960至1989：25.7133 /28.0267 /42.6930 /40.9373；
1990至2008：20.1526 /22.7158 /38.0292 /40.6738。
本冻结比较中persistence整体误差最低。lag11对个别年份可能优于persistence，整体仍较差。没有进行显著性检验或模型调参。

## 证据边界与候选知识
真实历史观测属于PUBLIC_REAL_TIME_SERIES_DATA，评估属于INTERNAL_NONBLIND_RETROSPECTIVE_METHOD_TEST。原始序列可能在事后修订，未取得每一预测年份当时的数据版本，不能声称真实历史实时预测。物理太阳活动与个人生活目标的迁移有效性UNKNOWN。预测校准、概率区间及实际产品的时间外表现未测试。E1方法测试不能升级为真人E2或历史社会E3。
候选要求：保留预测时点、可见数据版本、冻结基线、滚动原点、误差分布及失败年份；对不同决策目标分别评分，避免单一人生效用权重。无新增费用，账单/免费额度未独立核验。下一轮研究滚动预测区间覆盖率与预先冻结的残差校准，避免用未来数据构造区间。
