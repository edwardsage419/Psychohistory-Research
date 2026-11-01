# MKT198：Fitbit 真实随机试验与奖励撤除后的长期行为变化

track: market
subflow: commercial product mechanism and independent effectiveness evidence
run_date_utc: 2026-11-01
target_key: (market,FitbitZip+TRIPPA2016,2016-randomized-trial-and-2026-current-Google-Health-docs,incentive-withdrawal-objective-activity-health-outcomes)
baseline_main: a6ac9575b2e50fb79e8362686db2889a130584eb
status: COMPLETE_BOUNDED_DOCUMENTARY
evidence: MARKET-E1_OFFICIAL_CURRENT_FEATURES; MARKET-E2_DIRECT_RANDOMIZED_HISTORICAL_FITBIT_ZIP_TRIAL; MARKET-E3_LONG_TERM_WELFARE_NOT_VERIFIED
read_scope: NONBLIND; English PubMed original peer-reviewed trial abstract, Duke scholarly record, current official Google Health goals documentation and official Fitbit privacy disclosure; full paywalled article and participant-level data NOT_READ.
product_runtime: NOT_RUN
raw_data_reanalysis: NOT_RUN
ci: NOT_RUN
billing_checked: NOT_VERIFIED
paid_actions: NONE

## 1. 选题去重与研究问题

前轮 MKT193 研究 Beeminder 与相邻承诺实验，MKT196 研究 stickK 自选合同及自报体重，MKT197 研究 StepBet 的 72,974 人真实追踪器观察数据及正式勘误。仍缺少随机分配、客观测量、干预结束后继续随访的产品机制研究。

本轮找到 TRIPPA 随机试验：历史 Fitbit Zip 产品与现金/慈善奖励，6 个月干预及随后 6 个月停奖观察。它可以检验在特定人群中奖励与可穿戴设备对运动指标的因果影响。其结果不能直接外推到 StepBet 的先付押金、stickK 的自选违约金或 2026 年的 Google Health AI 教练。

## 2. 当前产品的可确认机制，历史产品隔离

Google Health 英文官方帮助中心（2026-11-01 查阅）显示，Fitbit 等设备可记录步数、活动分钟及依型号而异的其他指标。用户可编辑每日步数或其他活动目标，设备在达到目标时提醒。官方当前说明还披露个性化每周 cardio load 目标通常依据最近四周平均负荷，至少七天数据后可建立目标。Google Health Premium 的教练可根据 Recovery、Maintain、Build 等训练重点调整计划，用户可手动或对话调整目标与训练。完整 AI 预测算法、个体健康结果校准及实际推荐收益未公开，独立运行未验证。

输入：设备测量的步数、活动负荷及用户主动输入的目标；其他可选健康数据由设备及授权决定。
状态：每日进度、每周目标、活动历史、设备和授权来源。
目标：自定步数或活动目标；Premium 提供可调整的个性化训练计划。
反馈：可视化进度、设备提醒、目标完成提示及可选教练建议。
费用：历史 TRIPPA 设备由试验提供；2026 产品使用可能涉及设备购买与 Premium 订阅。当前准确售价、免费功能边界和区域可用性未核实。本项目没有注册、购买或使用。
解释性：四周均值这一目标输入得到官方披露，完整算法和 AI 教练的因果推荐依据未披露。

历史 TRIPPA 使用 Fitbit Zip 和试验规定的每周步数奖励。不能把 2026 年动态 cardio load 或 AI 教练功能追认到 2013 至 2014 年试验。

官方机制：https://support.google.com/googlehealth/answer/14236914?hl=en-GA
设备指标：https://support.google.com/googlehealth/answer/14236510

## 3. 直接产品随机试验：TRIPPA

原始研究：Finkelstein EA et al. (2016), *The Lancet Diabetes & Endocrinology* 4(12):983–995, DOI 10.1016/S2213-8587(16)30284-4, PMID 27717766，注册 NCT01855776。2013-06-13 至 2014-08-15 招募新加坡 13 家机构共 800 名全职雇员，随机分为对照 201、Fitbit 203、Fitbit 加慈善奖励 199、Fitbit 加现金奖励 197。

主要结局为由封存加速度计独立测得的每周中高强度活动（MVPA）持续时段分钟数；意向治疗分析，6 个月为干预结束，12 个月为停奖 6 个月后的随访。奖励按每周步数触发。次要结果包含步数、每周 70,000 步目标达成、体重、血压和生活质量。

相对对照组的 MVPA 分钟数差异：

| 组别 | 第6个月每周差异及95% CI | 第12个月每周差异及95% CI |
| --- | --- | --- |
| Fitbit 单独 | +16 [−2, 35]，p=0.0854 | +37 [19, 56]，p=0.0001 |
| Fitbit 加慈善奖励 | +21 [2, 39]，p=0.0310 | +32 [12, 51]，p=0.0013 |
| Fitbit 加现金奖励 | +29 [10, 47]，p=0.0024 | +15 [−5, 34]，p=0.1363 |

第12个月现金奖励组相对 Fitbit 单独组为 −23 分钟每周，95% CI [−42, −4]，p=0.0184。研究没有发现体重、血压等健康结局在 6 或 12 个月得到改善的证据。现金奖励组第6个月的活动优势在撤除奖励后未持续。

这些是随机分配试验的报告效应估计，不是对每个使用者的预测；“没有检出健康改善”不等于证明真实效果严格为零。结果只适用于当时试验的设备、奖励规则、工作人群和观测期。

来源：https://pubmed.ncbi.nlm.nih.gov/27717766/
研究机构记录：https://scholars.duke.edu/publication/1147644
注册：https://clinicaltrials.gov/study/NCT01855776

## 4. 与既有产品证据的可比较边界

StepBet（MKT197）为自选参与、带押金的个性化步数挑战，观察到活动增长但因果识别不足，缺少停奖后追踪。TRIPPA 是随机分配的设备和外部奖励组合，并以独立加速度计测量主要结局。两者的激励方向、设备、招募机制及结果口径不同，不能直接比较百分比优劣。

stickK（MKT196）真实合同的部分结果为自报体重，存在验证偏差；TRIPPA 独立测量 MVPA 降低了主要结局自报偏差。TRIPPA 没有测量一般人生决策质量或整体福利，不能因此为通用个人决策模型提供已验证的效用权重。

一个可用于未来研究的方法候选是分开记录：干预期行为目标达成、撤除奖励后的持续性、客观下游结果、用户承担的金钱与时间成本、主动退出和负面外溢。所有权重留待未来用户自主确定。

## 5. 隐私与伦理

Fitbit 官方英文隐私政策注明 2026-02-27 更新。根据账户及服务，设备和应用可能采集步数、心率、睡眠、位置和用户提供的其他数据，设备同步可上传至服务端；第三方访问可撤销，支持数据导出与账户删除。政策称大部分账户信息通常在 30 天内删除，部分备份删除最长可能需要 90 天，并存在法律或安全保留例外。Google Account 用户另受 Google 政策约束。政策披露不等于独立部署审计。

候选 F 风险：为运动目标收集过多健康信息、撤销第三方权限与历史删除的不同步、行为激励造成自主性和压力问题。已完成 W44 专题，本轮不另增 F 人工阶段，不读取任何用户敏感数据。

官方政策：https://www.fitbit.com/privacy-policy
Google 文档：https://support.google.com/product-documentation/answer/14815921?hl=en-GB

## 6. 证据等级与未完成关口

MARKET-E0：厂商对 AI 教练、动机和个人化的宣传，真实改善效果尚待独立验证。
MARKET-E1：2026 官方帮助文档及隐私政策，产品未登录或运行。
MARKET-E2_DIRECT_RCT：2016 TRIPPA 800 人随机分配、独立活动测量、停奖后 6 个月随访，存在可检验的正结果及明确负结果；已直接阅读原论文公开摘要及研究机构摘要，未读取收费全文、数据字典或原始参与者数据。
MARKET-E3：通用人生决策长期净福利、跨领域迁移、2026 AI 教练的随机效果均 NOT_VERIFIED。
R E1/E2/E3：N/A。没有新增 R 科学验收。

下轮优先：核查 TRIPPA 的公开方案、原始注册结局和后续研究是否一致；寻找具有同等关注度、客观下游结果和干预撤除随访的个性化规划产品 RCT。若无公开资料则保持未验证，避免继续重复安全技术人工编号。
