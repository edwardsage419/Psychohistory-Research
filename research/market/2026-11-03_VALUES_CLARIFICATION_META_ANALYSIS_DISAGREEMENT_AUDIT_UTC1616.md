# 决策辅助工具价值澄清机制：两项综述的证据分歧审查

track: market
date_utc: 2026-11-03T16:16:29Z
baseline_main: 7a54ae323a7c081d7f853915fbc82bc3e2509d54
status: PARTIAL_BOUNDED_LITERATURE_AUDIT
evidence: MARKET-E2_REVIEWED_RANDOMIZED_TRIAL_SYNTHESIS_AUTHOR_REPORTED
native_execution: NOT_RUN
independent_recalculation: NOT_RUN
commercial_product_effect: NOT_VERIFIED
new_cost: ZERO

## 研究问题
在个人多目标决策辅助中，显式让用户选择价值权重，是否比隐式澄清更能改善真实决策？本轮只研究已有医疗决策辅助试验的外部证据，不能直接外推到一般人生规划。

## 来源一：2021年Witteman等系统综述
Medical Decision Making 41(7):801–820, DOI 10.1177/0272989X211037946。
https://journals.sagepub.com/doi/10.1177/0272989X211037946
https://pubmed.ncbi.nlm.nih.gov/34565196/
作者纳入33篇文章，43种价值澄清方法的随机试验。显式澄清相对于对照或隐式方法，价值不一致选择的合并风险差为-0.04（95%CI -0.06至-0.02），决策冲突SMD -0.20（95%CI -0.29至-0.11）。多准则决策分析在作者分组比较中显示较高价值一致性。异质性与模拟选择场景限制显著。

## 来源二：2025年网络荟萃分析
The Effect of Patient Decision Aid Attributes on Patient Outcomes: A Network Meta-Analysis of a Systematic Review。
https://pubmed.ncbi.nlm.nih.gov/39968925/
作者筛查209项随机试验，其中149项有可纳入主要结局。摘要报告：隐式与显式价值澄清在评价结局上未见差异；概率信息缺失与较差知识得分相关，MD -3.86，95%可信区间 -7.67至-0.03。

## 分歧与限制
2021综述的显式价值澄清与对照/隐式混合比较，和2025网络荟萃分析的属性间比较，估计对象及纳入试验不同；不能把两组结论当作同一统计检验的直接相反结果。2025全文、网络结构、偏倚与敏感性尚未逐项核验。两篇研究都没有直接测试Exist、ProjectionLab、ARDA、Dcider或PaOS，也没有证明长期生活质量改善。

## 产品研究候选评价
分别测量：目标权重表达稳定性、用户实际选择与其声明价值一致性、预测校准、客观行为、决策后悔、成本、退出率及群体差异。明确允许用户修改指标和权重，防止默认属性集合决定结果。评价指标应事前冻结，避免用系统自己定义的价值一致性自证有效。

## E和F边界
E：本轮只读查询最新main HEAD为上述基线；开放PR搜索返回12项，PR描述的内部测试不可直接提升main证据等级；R272 P0历史未取得关闭证据。正式待核队列未重算。F：本周既有F010完成状态尚未由本轮原件独立核实；原则研究强调自主权与跨文化指标选择，未触及个人数据。

CI主动触发NOT_RUN；Actions当前HEAD PR触发查询为空，不代表所有触发类型已检查。GitHub计费额度NOT_VERIFIED，未购买、未部署、未改冻结协议。