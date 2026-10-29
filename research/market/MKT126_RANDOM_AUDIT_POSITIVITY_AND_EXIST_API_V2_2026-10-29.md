# MKT126 随机反馈审计与总体风险可识别性，Exist API v2机制

日期：2026-10-29 UTC。目标键：(market,MKT126,none,randomized-audit-positivity-risk-identification)。基线main HEAD b0d843e52feed0232aa7ec3a9e46941736fd072a。状态 COMPLETE_BOUNDED_SYNTHETIC_E1。承接MKT125的200条人工延迟反馈，保持个人决策产品开发暂停。

## 来源与证据等级

* 原始科研：Kleinberg等，2017，The Selective Labels Problem: Evaluating Algorithmic Predictions in the Presence of Unobservables，https://www.kdd.org/kdd2017/papers/view/the-selective-labels-problem-evaluating-algorithmic-predictions-in-the-pres 。研究选择性结果标签的评价难题，属于原论文方法背景，本文人工设计并非其原实验复现。
* 原始科研：Decision-Making Under Selective Labels: Optimal Finite-Domain Policies and Beyond，ICML 2021，https://research.ibm.com/publications/decision-making-under-selective-labels-optimal-finite-domain-policies-and-beyond 。讨论选择性标签下的策略学习，不能当作人生决策效果证据。
* 产品官方文档：Exist API v2 https://developer.exist.io/guide/ ，OAuth2范围 https://developer.exist.io/reference/authentication/oauth2/ ，读写分离及按组授权 https://developer.exist.io/guide/write_client/ ，导出及相关性 https://exist.io/page/faqs/ ，隐私原则 https://jenny.exist.io/about/values/ ，公开价格 https://exist.io/signup/ 。全部为DOC_SUPPORTED，未注册或实际调用API。

## 人工随机审计设计与计算

完整总体200条虚构二元标签。高预测组100条，预测概率4/5；低预测组100条，预测概率1/5。每组45条已成熟且可见，55条尚未取得结果。可见高组15正30负，低组30正15负，90条可见Brier=11/25=0.44。未观察110条在不增加假设时，整体Brier界限为[11/50,11/20]，即[0.22,0.55]。

两种隐藏真值世界在MKT125已冻结的可见部分完全相同。A的隐藏高组45正10负，低组10正45负，真实总体Brier=7/25=0.28。B的隐藏高组0正55负，低组55正0负，真实总体Brier=11/20=0.55。

新设定：对每个55条隐藏组独立进行不放回均匀抽取11条，共22条人工审计标签，固定一阶入样概率1/5。采用设计型Horvitz Thompson总体风险估计：(可见90条总损失 + 5×被审计22条总损失)/200。只针对已固定的200条真值及不改变结果的观察过程。

标准库BigInt精确超几何枚举。A有121种正概率审计计数组合，审计估计的设计期望为7/25，设计方差3/5000=0.0006，标准差约0.024495。B只有1种正概率组合，设计期望11/20、方差0。A两组审计都错过少数标签的概率为1536085093321/213443772381225，约0.007196；因此单次审计仍可能得到误导性结果。未审计的可见90条风险0.44在A与B均无法识别真实总体。0入样概率情形由测试拒绝，说明无覆盖组无法用逆概率权重恢复。

可执行归档：research/market/mkt126_random_audit_exact_20261029.js。隔离V8执行成功，12项内置断言全部通过。精确枚举已实现，原生Node CLI及独立第二算法复验未执行。人工E1，真人E2、历史E3及外部团队复现均新增0。随机审计估计在设计期望上无偏，单次样本并不保证准确；真实延迟标签可能无法通过主动审计加速成熟。若行为决策改变了潜在结果，仍需另外处理反事实不可观测问题。

## Exist产品机制补充

输入为手机、可穿戴设备、日历及用户手工记录，状态以日期和属性值为主；官方说明至少三周数据后才开始提供属性相关性，每周更新相关性。它提供趋势和相关性反馈，未公开可独立复算的因果识别或人生效用权重算法。API v2通过OAuth2按活动、睡眠、情绪、健康等组划分read与write scope；写入前需取得属性所有权。官方声明允许账户导出、删除账户后清除其数据库数据，但支付及客服记录另行保留。其价值观页面明确表示不加入大语言模型分析，采用统计方法。

2026-10-29公开注册页显示试用30天，之后每月6.99美元；相关页面亦显示每年62.90美元。产品使用需要账户和潜在收费，本轮只读官方公开网页，没有注册、付费或访问任何个人数据。营销的“优化行为”尚无本轮独立因果检验。

候选方法：未来研究必须记录预测时点、标签成熟时点、拒答/弃权、抽样资格、审计概率、已知选择机制及设计方差。只有存在合法、可实际观察的结果和正入样概率时，才使用随机审计估计。高风险自动建议应保留人工复核、申诉和停止权；此处为UNADOPTED知识储备。

## 阻塞与下一步

真实长期反馈成熟机制、跨用户迁移、个人隐私授权及标签获取成本尚无实证；不为审计收集真实敏感信息，不增加费用。下一项MKT127比较非均匀审计概率和未观测结果导致的不可识别边界，并区分观测缺失与决策反事实缺失。
