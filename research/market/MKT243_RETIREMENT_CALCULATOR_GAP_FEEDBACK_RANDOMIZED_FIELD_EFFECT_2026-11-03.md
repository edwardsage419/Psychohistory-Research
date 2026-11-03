# MKT243 退休规划计算器的目标缺口反馈与真实储蓄行为

track: market
date_utc: 2026-11-03
baseline_main: 5ba9ff4f94bb255aca6e4de6ff71fa888d4e5c74
status: COMPLETE_BOUNDED_ABSTRACT_REVIEW
evidence: MARKET-E2_AUTHOR_REPORTED_RANDOMIZED_TRIAL
native_execution: NOT_RUN
independent_recalculation: NOT_RUN
commercial_product_effect: NOT_VERIFIED
new_cost: ZERO

## 原始研究
Goda, Levy, Manchester, Sojourner, Tasoff, Xiao (2023), *Are retirement planning tools substitutes or complements to financial capability?*, Journal of Economic Behavior & Organization 214:561–573. 2022年12月NBER工作论文w30723，预分析注册AEARCTR-0002129。
https://www.nber.org/papers/w30723
https://iza.org/publications/dp/15758/are-retirement-planning-tools-substitutes-or-complements-to-financial-capability
https://econpapers.repec.org/article/eeejeborg/v_3a214_3ay_3a2023_3ai_3ac_3ap_3a561-573.htm

作者报告随机对照试验。两组网页计算器均显示退休收入目标；处理组额外展示根据缴款预测的退休收入、目标缺口，以及调整未来缴款以探索缺口变化的交互功能。处理组平均年度退休缴款增加174美元，约2.3%；金融知识较高者效果更大。随机化识别整个额外反馈组合的作用，无法拆分缺口可视化、预测、交互调整的独立贡献。

公开摘要未提供充分的样本量、置信区间、失访和异质性预注册细节供本轮核验。原始数据复算NOT_RUN，长期净福利、退休实际收入和跨人群迁移NOT_VERIFIED。

## 产品机制对照
ProjectionLab官方2026-08-18文档区分固定增长率的Plan与历史或随机市场路径的Chance of Success。官方支持交互比较财务情景。研究者实验计算器并非ProjectionLab，因此2.3%不能视为ProjectionLab产品效果。
https://cdn.projectionlab.com/help/plan-vs-chance-of-success
https://projectionlab.com/monte-carlo

证据分级：论文作者报告真人随机实验及储蓄行为为MARKET-E2；ProjectionLab官方功能为MARKET-E1；向综合人生决策迁移为MARKET-E0假设。建议未来预注册客观行为、理解能力、时间与心理成本、长期结果及不同金融知识层效果。没有启动产品开发或购买服务。

## E与F只读协调
E：检查时main未保护，12个开放PR均Draft且未合并；E168当天已有历史登记，R272 P0缺少关闭证据。待核队列完整净变化UNKNOWN。F：本周F010已有完成登记，当前仅提出展示目标缺口时同步衡量用户理解、压力及自主权的原则研究；没有个人敏感数据处理。R073和PESEN v0.1冻结不变。
GitHub Actions主动触发NOT_RUN，免费额度及账单NOT_VERIFIED。