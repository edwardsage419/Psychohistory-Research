# MKT204: Beeminder 目标偏离控制机制、直接用户调查与承诺装置反例

track: market
subflow: 商业产品运行机制与独立有效性
run_date_utc: 2026-11-01
local_date: 2026-11-02 Asia/Singapore
target_key: (market,Beeminder,official-api-and-pricing-2026-11-02,dynamic-road-safety-buffer-pledge-direct-survey-and-adjacent-negative-rct)
observed_main_before_write: c437e2d2f6f17f0add227bda56655bd6343ca4b8
status: COMPLETE_BOUNDED_PRIMARY_DOCUMENT_AND_INDEPENDENT_ABSTRACT_REVIEW
product_runtime: NOT_RUN
product_specific_randomized_outcome: NOT_VERIFIED
independent_direct_product_survey: MARKET-E2_ASSOCIATIONAL_INTENTION_ONLY
adjacent_negative_randomized_evidence: MARKET-E2_OTHER_SERVICE
market_E3_long_term_welfare: NOT_VERIFIED
R_E2_E3_new: 0
ci_status: NOT_RUN
billing_checked: NOT_VERIFIED
paid_actions: NONE
personal_sensitive_data: NONE

## 研究目标与去重

前轮 MKT196 已研究 stickK 的金钱承诺与报告结果，MKT197 研究 StepBet，MKT198 至 MKT202 研究随机实验和金融决策。本轮转向 Beeminder 独有的连续目标轨迹、剩余安全时间和退出延迟，重点寻找直接产品研究及与厂商成功叙事相反的实验。仅研究公开英文原始来源，不注册账户或使用任何可能产生罚款的服务。

## 官方产品运行机制，MARKET-E1

1. 用户输入可量化目标，例如每日写作字数、运动次数或控制某项活动的上限。可手工提交带时间戳的数据点，也可连接 Fitbit、Strava 等来源自动同步。API 文档公开 goaldate、goalval、rate、runits、datapoints、autodata、losedate、pledge、secret、datapublic 等字段，目标创建需给出 goaldate、goalval、rate 三者中的两项。此为公开接口层证据，未实际运行生产计算器。
2. 系统以 Bright Red Line 表示承诺轨迹，数据点必须保持在目标方向允许的一侧。Safety Buffer 以不增加新数据为条件，显示距离偏离的剩余时间。用户能查看进度和提醒。不同目标类型的安全侧方向和数据处理规则不同。若跨越边界且到期未修正，会进入 derailment；产品默认提高下一次风险金额，允许设置 pledge cap。官方说明还包含人工申诉及异常情况处理。
3. 退出具有七日 akrasia horizon：普通旧目标须先预约归档，等待七天，期间仍可能发生偏离；新建不足七日的普通目标存在立即删除例外，No-Excuses Mode 有额外限制。归档后停止新偏离、保留既有数据并可导出。归档与删除是不同操作。
4. 价格核查：2026-11-02 公开 Premium 页面显示 Core $0/月，Infinibee $8/月，Bee Plus $16/月，Beemium $81/月。即使 Core 月费为零，官方 money 页面要求设置支付方式，偏离目标可能实际扣款。所有收费和账户操作均未尝试。具体目标的金额与扣费条件以届时官方条款为准。
5. 官方 API 给出目标斜率、风险额、数据点及隐私字段；完整服务器端计算逻辑、同步误差处理、扣款争议执行与实际用户的因果改善效果没有在本轮获得独立可运行验证。公开 API 不等于整个产品源码开放。

## 独立直接产品研究，MARKET-E2，限定为使用意向

Oduor 与 Oinas-Kukkonen（2017），《Commitment Devices as Behavior Change Support Systems: A Study of Users’ Perceived Competence and Continuance Intention》，Persuasive 2017，DOI 10.1007/978-3-319-55134-0_16。芬兰 Oulu 大学机构仓储的作者版摘要显示 N=173，使用结构方程模型，研究说服性软件功能、感知能力和继续使用意向。模型解释约37%的继续使用意向变异，主要任务支持的相关作用最强。2018 年同一研究线的博士论文明确标注研究产品为 Beeminder，调查时间为2016年3月至5月。此为真实产品用户的横截面问卷关联研究，不能将37%解释成37%的用户成功、实际行为改善比例或随机实验效应。问卷选择偏差、主观测量、长期流失与真实目标达成仍未闭合。同一论文和博士论文属于同一研究线，不重复计作两项独立实证。

本轮 Oulu 作者版 PDF 链接访问返回403，直接阅读范围限机构仓储摘要和公开博士论文搜索可见文本。没有宣称全文表格、参数和模型拟合经过逐项复算。

## 相邻机制的负面随机试验，MARKET-E2，禁止产品效果归因

Savani（2018），《The Effects of a Commitment Device on Health Outcomes: Reputational Commitment and Weight Loss in an Online Experiment》，International Journal of Applied Behavioral Economics 7(4)，DOI 10.4018/IJABE.2018100101。UCL 机构仓储摘要记录随机分配364名在线减重服务客户，比较声誉承诺和预付月费退款方案，12周测量。声誉承诺组报告终点体重比比较组高约1.5 kg，即该条件下减重较慢，论文提及 commitment overload 作为可能解释。该实验使用另一在线服务，处理方式是声誉承诺，不能归因为 Beeminder 金钱承诺或具体软件。终点体重是否独立客观测量、组间脱落及模型细节未在本轮重新复核，摘要层级限制保留。

这项反例与 MKT196 stickK、MKT197 StepBet 的正向观察结果不能直接合并为产品排名。随机化、参与者筛选、承诺类型、测量方式、随访时长及退出成本不同。实际目标达成、财务损失、心理负担和长期净福利需要分别评价。

## F 风险的只读交叉观察

Beeminder 的七日退出延迟用于防止短期冲动放弃，也会在目标失去合理性或出现健康、财务、家庭紧急事件时形成真实约束。未来安全研究应区分可预先承诺的普通退出、紧急暂停、测量错误申诉、自动扣费前纠错、数据导出和账户删除。官方条款声称可按请求删除数据，但缓存或引用可能暂不消失；真实端到端删除未验证。目标与数据点的默认可见性须依据具体设置核验。此处仅为 F010 本周完成专题的增量来源观察，不新增 F 编号、不构建产品。

## E 只读治理快照

在写入前的 main c437e2d2f6f17f0add227bda56655bd6343ca4b8，R/B 新增 R333 至 R340 八份工作流源码可达性审计，报告确认既有八份工作流均未调用新 composite gate，且其 push.paths 均未覆盖新 gate 文件。该结论属于八个工作流定义的静态检查，完整原生运行及生产强制接入仍 NOT_RUN/PARTIAL，P0 不关闭。E167 本地当日实质审计已完成；本轮没有复制 B 数学复算或新建 E 编号。Codex PR #1、#3 仍为 Draft、未合并，属于另一 R257 S53 问题键。original239 crosswalk blob 36f24235901172642c46853298aebb421f1a3552，pending queue blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f；文件级净变化0，154项待核不视为已验收。R073 与 PESEN v0.1 保持冻结。

## 实际读取的英文原始来源及范围

Beeminder 官方总览: https://www.beeminder.com/overview
Beeminder API 文档: https://api.beeminder.com/
Beeminder 目标退出: https://help.beeminder.com/article/44-how-do-i-quit-a-goal
Beeminder 归档状态: https://help.beeminder.com/article/46-what-happens-to-an-archived-goal
Beeminder Safety Buffer: https://help.beeminder.com/article/55-what-is-safety-buffer
Beeminder 价格: https://www.beeminder.com/premium
Beeminder 罚款机制: https://www.beeminder.com/money
Beeminder 隐私与条款: https://www.beeminder.com/terms
Oulu 2017 原始研究仓储摘要: https://oulurepo.oulu.fi/handle/10024/24640
Oulu 2018 博士论文公开索引: https://oulurepo.oulu.fi/bitstream/handle/10024/36285/isbn978-952-62-1885-4.pdf?isAllowed=y&sequence=1
UCL 2018 原始随机实验摘要: https://discovery.ucl.ac.uk/id/eprint/10056803/

## 下一高价值任务

优先检查 Beeminder 直接研究的原始问卷测量、参与者选择与目标达成关联，若作者版全文无法免费获取则保留摘要限制。寻找独立、客观、具有随机分组或退出后随访的目标控制产品实验，尤其包含退出成本和用户净福利。E 轨等待 R/B 完整原生组合验收及正式强制调用证据；不自动修改工作流、合并 PR 或触发 CI。无新增费用、敏感数据或收费账户。
