# MKT175 概率校准与时间外预测
日期：2026-10-31 UTC。目标键：(market,ProjectionLab_scikit_learn,official_docs_2026-10-31,probability_calibration_temporal_holdout)。已读MKT174，新增产品评估维度为“情景成功率是否在未来实际结局中校准”。无登录、注册、真实个人数据或付费操作。

## 英文原始来源
ProjectionLab 2026-10-01官方文章 https://projectionlab.com/financial-terms/monte-carlo-simulation 将成功率表述为指定市场分布与人生计划下模拟成功的比例，说明模拟结果依赖假设。官方功能 https://projectionlab.com/monte-carlo 允许历史回测、自定义分布、逐次查看和自定义成功类别；2025-04-11 https://projectionlab.com/help/increase-trials-in-chance-of-success 说明随机起点和随机重启最多2000次试验。均属VENDOR_DOCUMENTED，未获内部代码或独立真实预测校准。scikit-learn官方方法文档 https://scikit-learn.org/stable/modules/calibration.html 说明Brier和log loss是严格适当评分规则，混合校准与区分度因素；校准数据宜独立于训练数据。属INDEPENDENT_METHOD_DOCUMENTATION，并非对ProjectionLab的独立测评。

输入：计划余额、现金流、市场历史或假设、成功分类。状态：现金流与模拟路径。算法：历史/随机多试验及成功比例；真实联合采样细节UNKNOWN。目标：用户定义成功并比较情景。反馈：修改计划重跑。解释性：可查看逐条模拟。隐私：沿用MKT174已读官方云存储声明，权限与删除效果未独立审计。费用：沿用MKT174既有价格记录，未重新验证价格，无购买或收费API。

## 实际人工精确实验
执行Python标准库程序 research/market/mkt175_temporal_calibration_20261031.py PASS。虚构标签[1,1,0,0]，两组概率[0.51,0.51,0.49,0.49]与[0.9,0.9,0.1,0.1]的0.5阈值分类均为4/4，Brier分别2401/10000和1/100。分类正确率不足以衡量概率预测质量。

另一虚构12期序列前8期正例2/8，最后4期全为正例。事先冻结8/4时间切分，训练频率预测p=1/4，未来Brier=9/16；偷看全部12期得到p=1/2，在相同未来标签上表面Brier=1/4。后者使用未来信息，不是有效外部成绩。强分布漂移和小样本仅用于教学，不能声称任何真实算法优劣。

候选储备：预先冻结预测时间、信息可得性、结局、评分与时间外划分；同时报告Brier、log loss、校准曲线、基线、异质性与不确定性，保持多目标，不预设单一人生效用。真实结果配对数据与产品实际校准UNKNOWN。证据：官方产品陈述、独立方法文档、INTERNAL_SYNTHETIC_E1。新增真人E2=0、历史E3=0。零新增费用；账户账单/免费额度未核验。下轮研究公开可许可时间序列的冻结滚动外测。
