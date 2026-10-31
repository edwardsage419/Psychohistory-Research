# MKT171 ProjectionLab 情景模拟与 Beeminder 偏离反馈机制
UTC 2026-10-31T08:19Z。目标键 (market,ProjectionLab+Beeminder,official_docs_2026-10-31,deterministic_vs_stochastic_scenario_and_feedback)。上一MKT170为ActivityWatch设备身份迁移，本轮转向新的产品机制。仅公开英文官方资料及人工示例，没有注册、购买或输入个人数据。

## ProjectionLab 机制及证据
输入：用户自行录入账户余额、资产、债务、收入、支出、投资增长率、税务设定、人生里程碑与退休等计划；不要求连接银行账户。状态：同一基线计划及其可编辑变体、逐年现金流与资产余额、目标达成及历史进展。算法：Plan页使用固定增长率的单一路径；Chance of Success基于历史或随机化市场回报、股息和通胀进行多次试验。官方2026-08-18帮助文章明确两者共用计划输入，其他页面沿用Plan假设而非Chance of Success试验结果。官方2025-04-11文档说明随机抽样方式可增至2000次，Historical No Looping因固定历史序列不可增加试验次数。官方2026-06-30说明逐年模拟收入、扣缴、费用、债务、股息、前一年税额等现金流，年度盈亏按规则进入储蓄或提款。What If可把调整后的计划与基线并排比较。目标是财务规划及风险情景分析；用户自行调整假设形成反馈，官方还提供历史进展日志。尚无独立验证其预测校准或真实人生最优性。

官方2026-10-01文章说明成功率是给定假设下的模拟频率，结果受市场分布、通胀和序列风险影响。该解释为供应商文档，非独立验证。官方自称优化器测试数百种税务与提款策略，优化范围限于用户设定的财务目标；没有证据支持跨健康、关系与精神价值的统一人生效用。

## 费用、隐私、权限及局限
官方2026-10-31可见定价 Basic $0/年，Premium $129/年，Pro $549/年。Basic列有Monte Carlo及历史回测，Premium列有更深现金流、税务、What If、Compare和多计划。用户零新增费用约束下仅审查公开资料，不注册、不试用付费功能。官方2026-08-12安全说明使用Google Cloud/Firebase、TLS和静态AES-256加密、支持JSON导出与账户删除；删除后备份按其政策到期，具体周期本轮未独立验证。官方2025-03-06宣布自托管版本停止未来更新，原自托管版本维护已在2025-12-31结束。产品属于云端托管，不能由文档推定完整本地优先或独立可验证。

## Beeminder互补机制
官方帮助与FAQ确认时间戳数据点、目标红线、安全缓冲天数、截止时间和偏离后的重新上轨；违约可能产生质押收费，费用依设置及偏离次数变化。2026-03-06定价帮助称可免费建立三个活跃目标，同时存在第一周未建目标的收费条件及偏离收费。对本项目仅研究反馈机制，绝不注册或启用质押。目标偏离报警属于用户设定承诺的执行反馈，不能直接视为目标合理或生活质量提升的实证证据。惩罚机制可能造成指标游戏化和心理压力，需要未来伦理审查。

## 人工E1精确示例
独立Python Fraction人工两期资产模型，初始100，每期收益先发生、随后提款50，每期收益率独立取+20%或-20%，四条等概率路径。两期末余额依次为(+,+)=34、(+,-)=6、(-,+)=-14、(-,-)=-26。严格路径非负的人工成功率2/4。固定平均收益率0的单一路径为50、0，恰好通过。两条收益率集合相同而顺序相反的路径相差20。实际运行7项断言PASS。该模型不是ProjectionLab代码、其采样机制或真实资产预测。

候选知识：保留基线计划与情景版本、明确固定路径和概率路径的分离、记录抽样假设与失败情景、用户可选择多个目标及风险容忍度、定期对照实际偏离并允许人工纠正；不得预先规定单一人生效用权重。需另行检验抽样有效性、跨目标冲突、外部校准及行为反馈风险。新增E2=0、E3=0。

官方来源：
https://projectionlab.com/help/plan-vs-chance-of-success
https://projectionlab.com/help/simulation-engine
https://projectionlab.com/help/increase-trials-in-chance-of-success
https://projectionlab.com/help/using-what-if
https://projectionlab.com/financial-terms/monte-carlo-simulation
https://projectionlab.com/pricing
https://projectionlab.com/security
https://projectionlab.com/blog/update-on-self-hosting
https://help.beeminder.com/article/19-how-much-does-beeminder-cost
https://www.beeminder.com/faq
程序 research/market/mkt171_scenario_order_synthetic_20261031.py。
证据等级：官方文档支持+内部人工E1；未做产品实际操作、独立安全评估或效果试验。下一项MKT172考察ProjectionLab的自定义增长分布、历史样本重采样和成功阈值可追溯性。
