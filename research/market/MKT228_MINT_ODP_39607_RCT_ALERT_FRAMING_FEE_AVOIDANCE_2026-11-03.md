# MKT228：Mint Overdraft Prediction 的真实随机试验、提醒框架与损失避免边界

track: market
subflow: commercial_product_research + E_readonly_crosscheck + F_weekly_readonly
run_date_utc: 2026-11-02
local_date: 2026-11-03 Asia/Singapore
target_key: (market,Mint-Overdraft-Prediction,Ben-David-Mintz-Sade-FDIC-2020-working-paper+Management-Science-2025-final,39,607-randomized-alert-frames-objective-fee-vs-engagement-version-boundary)
observed_main_before_write: 6e9e5b92abda7c69b845abeb797aeccaa240925d
status: COMPLETE_BOUNDED_PRIMARY_WORKING_PAPER_TABLE_AND_FINAL_ABSTRACT_REVIEW
market_evidence_grade: MARKET-E2_BOUNDED_RANDOMIZED_FIELD_BEHAVIOR
original_participant_data_replay: NOT_RUN
final_2025_paper_tables_verified: NOT_VERIFIED
algorithm_production_execution: NOT_RUN
long_term_net_welfare: NOT_VERIFIED
new_R_E2_E3: 0
E_daily: E168_ALREADY_COMPLETE_2026-11-03_READ_ONLY
F_weekly: F010_ALREADY_COMPLETE_2026-W45_READ_ONLY
ci_status: NOT_RUN
billing_checked: ACCOUNT_BILLING_AND_ACTIONS_FREE_QUOTA_NOT_VERIFIED
paid_actions: NONE
personal_financial_data: NOT_ACCESSED

## 1. 选题去重及来源版本

MKT227考察Meniga移动访问推出的自然实验及《Mind the App》错峰推出的准实验。此次选择2018年Mint Overdraft Prediction（ODP）的四组真实随机试验，检验“预测未来一周账户透支风险→按需提醒→用户自主操作→真实银行收费变化”的可识别机制。目标键、识别设计、具体产品与待证缺口均不同。

直接阅读美国FDIC公开的Ben-David、Mintz、Sade 2020年工作论文全文，重点核对实验程序、样本、Table 2/3/5/6/7、收入异质性。另读取2025年5月14日正式在线发表的Management Science出版商摘要（2026年72卷1期204至222页）。**下列详细数值属于FDIC 2020工作论文版本；正式2025排印全文的相应表格尚未逐表核验。**不得将2020具体数值标注为2025最终版已确认。

原始来源：
* https://www.fdic.gov/system/files/2024-09/2020-ben-david.pdf （2020工作论文，公开全文）
* https://pubsonline.informs.org/doi/10.1287/mnsc.2022.00304 （正式期刊版本，2025-05-14 online）
* https://cris.huji.ac.il/en/publications/using-ai-and-behavioral-finance-to-cope-with-limited-attention-an/ （作者机构论文身份）
* https://onlinelibrary.wiley.com/doi/10.1111/jofi.13404 （2025年英国银行提醒独立实验）
* https://www.creditkarma.com/about/releases/intuit-credit-karma-welcomes-all-minters （官方Mint停止与迁移声明）
* https://support.creditkarma.com/articles/en_US/Knowledge/Intuit-Mint-and-Credit-Karma （官方功能、数据导出及删除说明）

## 2. 真实产品输入、状态、预测、建议、反馈

历史Mint允许用户连接银行及信用卡账户、查看交易、余额、债务和预算。ODP使用这些账户数据，通过机器学习计算用户**未来一周出现负余额**的风险分数。分数超过阈值触发邮件提醒；邮件可引导用户返回产品查看账户及可采取的行动。用户自行决定是否调拨资金、改变支付安排等。原始预测器的完整特征工程、训练样本、模型架构、阈值、校准及误报率未公开给本轮独立复验。风险预测准确性与提醒的因果效果必须分别评价。

Mint原服务已停止，Credit Karma官方2023年10月声明明确Mint退出并安排迁移；2024年5月后不再支持Mint迁移。Credit Karma提供部分账户聚合和财务分析，但官方支持文档确认预算功能与旧Mint不完全一致。历史ODP实验的邮件、模型与效果不能当作2026年Credit Karma同一功能的现行性能；现行产品价格、商业推荐利益冲突、第三方数据流及完整模型未在本轮独立审计。

## 3. 2018年四组随机试验：实际可核数据

2020工作论文报告2018年连续四个月真实平台实验，39,607名高透支风险用户。分配方式为随机ID的哈希函数，未按收入分层。各组：
* Control不发送提醒：10,972人。
* Base原有提醒：9,422人。
* Simplified Avoid简化、强调避免损失：9,725人。
* Simplified Save简化、强调节省收益：9,488人。

总数10,972+9,422+9,725+9,488=39,607，整数相符。22,775名此前收到过ODP Base邮件，16,832名首次进入ODP；这一历史接触差异在分析中控制。每人每周最多一封提醒，每月最多四封，实际平均3.2封；用户在实验期间至少随访三个月，最长四个月。作者报告无样本流失。实验样本属于算法先行筛选的高风险Mint用户，不代表一般人群。

FDIC版本Table 3的相对Control的NSF/透支收费**次数**变化：
* Base：首周 -5.3%；四个月 -3.3%（四个月仅标注p<0.10）。
* Simplified Avoid：首周 -9.25%；四个月 -8.9%。
* Simplified Save：首周 -9.44%；四个月 -4.9%。

Control均值：首周每人0.91次；四个月每人8.08次。以上是作者按实验组比较报告的相对次数变化，不能与2023年Meniga的不同观察窗口估计相加，也不能把负百分比解释为费用金额百分比。按Control四个月8.08次和Avoid相对下降8.9%粗算约0.72次/人，**仅为工作论文公开均值的算术换算**，不等于个体级原始数据复算或调整后因果效应。

邮件参与度：Base开启率27.5%、点击探索率1.4%；Avoid分别30.85%、2.5%；Save分别30.51%、1.51%。Avoid相对Base的开启率提升12.1%和点击率提升78.4%是**相对增幅**，开启率绝对差约3.35个百分点，点击绝对差约1.1个百分点。参与度属于中介/过程指标，不能直接代替银行收费或用户福利。

工作论文Table 5：Base相对Control四个月Tobit log(1+NSF)系数 -0.0316（SE 0.0192，p<0.10）；Avoid相对Base四个月 -0.0530（SE 0.0200，p<0.01）。Table 6复发事件Cox模型中Base相对Control系数 -0.00875（SE 0.00825，未显著），Avoid相对Control -0.0183（SE 0.00824，p<0.05）。**不同模型对Base的统计显著性存在差别**，不能写成所有分析均确认Base有效。Cox风险系数也不可直接当成收费次数的百分比变化。

工作论文另报告四个月Avoid相对Control平均减少25.16美元收费，Save相对Control减少13.85美元，差11.31美元（论文文字约11.33美元，涉及四舍五入/表格口径待核）。金额估计是工作论文作者报告，原始个体交易未开放，本轮没有复算。收入异质性：短期中25百分位以上组较可能受益；四个月完整期间显著效应主要在75百分位以上。收入较低者可能面临实际流动性约束，单纯提醒不足以消除问题。分组多重比较、预注册和最终版本差异均未独立核验。

## 4. 独立研究交叉对照与外推限制

Grubb等《Journal of Finance》2025年英国银行真实随机现场试验，使用银行自动加入的即时短信提醒，报告未安排透支和拒付收费下降17%至19%，已安排透支收费下降4%至8%。增量提前预警的统计效果未确认。论文明确比较了Mint邮件研究：其邮件开启率约28%至31%，英国短信触达/开启更高。该研究涉及不同国家、银行系统、用户风险集、提醒渠道和处理方式，构成**独立同类机制的外部对照**，不能视为对Mint原算法、相同效果量的直接复现。英国论文披露监管机构FCA提供数据并有机构利益关联。

两项研究共同支持在特定场景下降低信息注意成本可以减少可观测的收费。仍须区分预测准确性、提醒是否被看到、用户是否有足够流动性行动，以及总体长期净福利。收费减少可能来自主动避错，也可能伴随延期支付或其他代价；实验未覆盖所有长期结果。

## 5. MARKET证据分级、F风险与未来研究问题

MARKET-E2仅覆盖真实随机分配的邮件提醒策略对高风险用户短期收费次数及参与度的研究证据。2020工作论文的表格可以核对，2025最终正式版的具体表格未核，真实用户数据未复算，完整AI预测算法未独立执行。厂商官方当前功能与产品政策属于MARKET-E0/E1资料；研究结果不能转化为R系列真人预测E2/E3或原创心理史学模型科学验收。

未来产品研究的可证伪指标应区分：提前预警命中率与误报、用户能否行动、实际避免的无收益费用、因误报或行动产生的替代成本、对流动性较低群体的公平性、长期总福利。隐私涉及完整银行流水、余额、交易时间、信贷特征和风险评分；未来方法应优先最小化、本地处理、明确授权与撤回、导出删除、用户最终选择权。本轮仅研究公开论文和官方政策，没有读取个人敏感数据、部署产品、验证删除行为。F010本周专题已完成，本轮不新增F编号。

## 6. E只读核对、协作、费用与下一步

本轮main写入前为6e9e5b92abda7c69b845abeb797aeccaa240925d。E168已于本地11月3日完成实质审计；其R272 P0报告已指出生产workflow有contents: write及自动推送main能力，候选单入口尚未强制采纳。R轨新提交c4b064b9bc0315fc646dd545d607e3fec24c2f53新增R272单入口YAML候选和结构检查器，三模式各12项人工反例本地通过，仍在research/validation目录；真实完整checkout及生产采纳NOT_RUN，P0继续OPEN。R333至R340八个工作流复合门调用仍缺乏完成证据。R073/PESEN v0.1冻结不变。

本轮重新读取12个open PR，均Draft、merged=false。PR #3相对main diverged，main独有1202提交、PR独有1提交；仍需来源身份、冻结协议和盲态验收。队列CSV blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f，交叉索引blob 36f24235901172642c46853298aebb421f1a3552，均与E168一致；该版本154项（P0 27、P1 82、P2 45），文件级净减少0。本轮无合并、无跨轨文件改写、无CI触发。最新main的Actions按head_sha查询为0项；这不穷尽所有触发方式。实际GitHub账单/免费额度NOT_VERIFIED，故不触发可能收费的Actions。

下一高价值任务：若能合法免费获取2025最终论文完整统计表，核查工作论文与最终版估计是否变化及多重比较；随后转向非金融场景的客观错误避免与长期决策改善证据，避免同类金融提醒研究无限扩张。E继续只读追踪R272生产权限与强制调用的真实关闭证据，F本周维持只读。
