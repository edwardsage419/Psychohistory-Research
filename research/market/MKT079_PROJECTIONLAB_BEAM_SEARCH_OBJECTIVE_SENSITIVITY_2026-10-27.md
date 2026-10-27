# MKT079 ProjectionLab 多目标财务策略优化的搜索预算与目标敏感性

日期：2026-10-27（Asia/Singapore）。轨道：market。状态：COMPLETE_BOUNDED_VENDOR_DOCUMENTATION_AND_SYNTHETIC_35。CI：NOT_RUN。主动新增费用：0。

## 1. 预检与本轮独立问题
开始读取main HEAD 50e7d9a810843642e29d0834db34fdb1aa17f5d4、market至MKT078、operations至E047、F002和R216 S12及A轨来源登记。MKT002、MKT027、MKT028已研究ProjectionLab蒙特卡洛、区块重抽样、弹性支出与必要消费底线；MKT044、MKT045、MKT078已研究计划时间归因、进度点与伴侣账户状态。此次专门深读2026年官方公开的税务策略Optimizer搜索目标、束搜索及非全局最优边界，避免重复前述题目。

## 2. 可核实的英文官方来源
S1：官方2026-07-22帮助《Can I model Roth Conversions using ProjectionLab's Optimize feature?》：https://projectionlab.com/help/roth-conversion 。列明六个优化目标：Lower Lifetime Taxes、Higher Net Legacy、Higher Net Worth、Lower Effective Tax Rate、Lower RMDs、Reduce IRMAA Surcharges；搜索深度Quick、Standard、Deep、Extreme，可设置Worker Threads。帮助文档明确称使用beam search逐步筛减候选，深度增加搜索范围，任何模式均不能保证全局绝对最优。结果显示已评价策略数量、获胜方案、其他指标影响，并提供Apply Strategy与Explore Alternatives。算法完整评分细节、剪枝准则、搜索空间和确定性未公开验证。
S2：官方2026-04-21发布说明《Optimize Your Financial Future》，v4.6.0：https://projectionlab.com/blog/whats-new-v460 。厂商称Roth conversions、drawdown、gain harvesting共享税务策略，约束包含税档、IRMAA、ACA、NIIT与配偶收入拆分；搜索策略、税档和时段。其“节省巨额费用”“几秒找出胜者”是营销及产品描述，没有本项目独立实证验证。
S3：官方2026-04-20更新日志：https://projectionlab.com/changelog 。v4.6.0列Tax Strategies、Optimize及相关模块。
S4：2026-10-27读取官方价格：https://projectionlab.com/pricing 。Basic $0/年、Premium $129/年、Pro $549/年；Tax Optimization列在Premium。没有注册、试用或购买。
S5：官方安全说明：https://projectionlab.com/security 。厂商自述加密、存储及用户控制，未开展第三方审计，不能将厂商陈述写成已独立证明的隐私保证。

## 3. 本轮新增的机制证据
产品允许用户在税务、遗产、净资产、有效税率、最低强制提取及IRMAA之间选择不同目标。即使使用相同输入计划，目标改变也可能改变获胜策略。帮助文档已明确承认beam search的剪枝可能遗漏全局最优，搜索深度是需要解释的实验设置。产品提供多指标对比及Explore Alternatives，用户可在结果界面手动Apply；没有证据表明它会自动学习个人真实长期效用权重。

## 4. 独立人工搜索反例
脚本 research/market/mkt079_projectionlab_beam_objective_synthetic_20261027.js 仅用Node.js标准库，离线运行35项断言全部通过。四个虚构候选A1、A2、B1、B2，目标向量分别为(税5,遗产7)、(税6,遗产9)、(税3,遗产3)、(税4,遗产4)。第一层虚构搜索启发分A=8、B=7；束宽1仅保留A，束宽2保留A与B。最小化税的束宽1返回A1(税5)，束宽2返回B1(税3)；最大化遗产的束宽2返回A2(遗产9)。四项均为该人工候选集的Pareto非支配项。附加“税≤4且遗产≥7”时无可行项。
以上数值和中间启发式由研究者人为指定，绝非厂商引擎输出，也未模拟真实税务法则、市场收益、遗产转移或用户行为。它只严格证明有限束宽可能剪掉更优的终局选项、目标选择会改变推荐、多个目标可互相冲突。厂商是否发生该具体反例未知。

## 5. 产品机制矩阵与研究边界
输入：用户财务计划、账户及现金流、税档或收入上限、税务策略、时间窗、目标与搜索深度。状态：年度现金流、账户与税务估计、候选策略、目标值和结果指标。算法：官方明确beam search，未提供完整实现或独立源码测试。目标：用户从六个财务目标中选择；未证明存在跨健康、关系、精神体验等领域的统一人生效用函数。反馈：可比较策略、调整目标、重跑搜索、手动应用；没有已验证的真实行为自我校准。解释性：官方展示搜索数、赢家及多项结果差值；搜索遗漏率、路径剪枝原因和外部误差校准未知。隐私：云端服务安全来自厂商自述，本轮无真实个人或第三人数据。费用：税务优化属于付费Premium，本项目仅免费阅读。局限：缺真实引擎执行、第三方对照、跨法域准确性复算和长期决策收益验证。

## 6. 候选知识储备与风险
MKT079-C1：未来决策研究需将目标函数版本、硬约束、搜索预算、候选集合、随机性与结果指标分别记录；禁止预先指定唯一人生效用权重。
MKT079-C2：为用户展示Pareto候选及冲突，允许保留未决定状态和人工最终选择；不同目标的赢家不得合并为一个“客观最优人生”。
MKT079-C3：区分“搜索范围内最佳”“全局已证明最优”“外部样本有效”三种证据状态。建议记录被排除方案和敏感性，若实现不提供则标记UNKNOWN。
MKT079-C4：税务等不可逆决策须独立人工审阅，不因模拟优化得分自动执行。
风险HIGH：把束搜索赢家误认为全局最优。风险HIGH：把财务单目标扩展为唯一人生效用。风险MEDIUM：搜索深度、估计模型或税制变更后，方案排名不稳定。均为原则性候选风险，未声称ProjectionLab实际失效。

证据等级：VENDOR_DOCUMENTED、SYNTHETIC_COUNTEREXAMPLE_35_ASSERTIONS、UNVERIFIED_RUNTIME。归档MARKET E1；无真人效果E2、历史演化E3或外部独立复现。

## 7. E与F协调及下一项
本轮E048对R215 S11完成来源级5736项独立检查，发现旧E轨对R073“缺少第二独立真人实验”的重复表述需要沿E006读时纠正。F002本周已完成，不重复立项；把目标锁定、搜索剪枝可解释性、拒绝越权自动执行留作F003之后候选。下一轮MKT080优先对比另一开源多目标决策或Pareto搜索工具的源码、许可、反例测试与用户可解释性；零新增费用，R系列先完成后归纳和熔炼。
