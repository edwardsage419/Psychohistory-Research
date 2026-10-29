# MKT124 时间留出概率校准与弃权门，以及 Beeminder 承诺机制对照

日期：2026-10-29 UTC。目标键：(market,MKT124,none,calibration-abstention-temporal-transport)。状态：COMPLETE_BOUNDED_SYNTHETIC_E1。基线 HEAD e7b132dae1eccfc7627a31666b7657ce75ebd5a1。承接 MKT123 的用户及时间划分问题。

## 英文原始来源与来源等级

1. scikit-learn 官方概率校准 API https://scikit-learn.org/stable/api/sklearn.calibration.html 。支持 calibration_curve、CalibratedClassifierCV 的存在和用途。官方文档没有验证本轮人工实验。
2. scikit-learn 官方数据泄漏说明 https://scikit-learn.org/stable/common_pitfalls.html 。支持训练、校准、测试的隔离要求。
3. Beeminder 官方目标数据 https://help.beeminder.com/article/36-what-is-my-data 及红线反馈 https://help.beeminder.com/article/118-how-do-i-interpret-the-graph 。支持手工或集成数据、红线及安全缓冲显示。
4. Beeminder 官方七天承诺期 https://help.beeminder.com/article/45-what-is-the-akrasia-horizon 。降低目标难度、安排暂停、退出和降低承诺金额一般须等待七天。
5. Beeminder 官方数据导出 https://help.beeminder.com/article/41-can-i-export-my-data 。支持 CSV/TSV、API、webhook；官方明确 webhook 可能静默失败。
6. Beeminder 官方隐私 https://help.beeminder.com/article/102-privacy 。默认新目标图表公开而具体数据点私密，可调整目标隐私。
7. Beeminder 当前官方定价 https://www.beeminder.com/premium ，核心方案每月 $0，Infinibee $8，Bee Plus $16，Beemium $81；另有失约金风险 https://www.beeminder.com/money 。价格为查询时官网展示，未来可能改变。没有注册或付费。

上述 Beeminder 来源是产品官方自述及帮助文档，属于 DOC_SUPPORTED，不等同独立产品有效性验证；实际价格和功能可能受账号与时间影响。没有引用中文网站。

## 冻结的人工实验与运行结果

完全人工的8名已知用户，4个时期，每期2次重复二元回答。前3期偏好稳定，第四期用户0至3反转，其余4名保持稳定。已知用户的固定预测概率为0.1或0.9，另外4名新用户统一为0.5。训练集为时期0、1的32条，校准集为时期2的16条，未来集为时期3的16条，新用户留出8条。脚本原生 JavaScript，不运行 scikit-learn。

同一预测器的留出评价如下。ECE 为本轮两个固定预测概率组的经验校准误差，Brier 为平均平方概率损失。

| 评价对象 | 记录数 | 准确率 | Brier | ECE |
| :--- | ---: | ---: | ---: | ---: |
| 已知用户时期2 | 16 | 100% | 0.01 | 0.10 |
| 已知用户时期3，半数偏好翻转 | 16 | 50% | 0.41 | 0.40 |
| 全新用户时期2 | 8 | 50% | 0.25 | 0.00 |

使用时期2各预测概率组的经验频率做简单后验校准，时期2 Brier 变为0；应用到时期3则变为0.50，劣于原概率的0.41。这是特定人工数据的结果。校准集上零误差属于同集拟合，不能当作独立验证。

使用最大类别概率至少0.8作为自动建议阈值：时期2接受16/16，错误率0；时期3仍接受16/16，错误率50%；新用户全部弃权。额外设置时间有效期截至时期2的候选门，时期3接受0/16，错误率不可定义（null），避免把零覆盖率误写成零错误率。时间门可能过度保守，尚无最优阈值证据。

脚本：research/market/mkt124_calibration_abstention_temporal_20261029.js。归档后远端Git blob bb5962cc7851bf68bce49ab94e3c38ab2f496237，已在隔离V8环境重新读取并执行，99项显式断言通过，两个错误拆分控制成功拒绝。原生 Node.js CLI 和独立外部团队执行尚未完成。

## 产品机制对照与未来候选控制

Beeminder 输入手工活动数据或集成数据，状态为目标进度、红线、安全缓冲、承诺金额与等待期。目标是强化用户事前承诺，反馈来自进度颜色、临界日和失约后处理；更改承诺和退出受七天窗口约束。官网没有披露可供本轮独立验证的个人长期效用模型、预测概率校准或因果收益。风险包括支付承诺、错误数据导致意外失约、目标变更滞后、默认公开图表、webhook静默遗漏。零费用约束下仅阅读公开资料，不能创建真实付费承诺。

候选知识储备：把概率可靠性、可拒答状态、预测适用时限、目标承诺及人工紧急停止分开表达。未来模型不得用高概率数字自动替用户做不可撤销的金钱承诺，也不得预设单一人生效用权重。真实授权撤销、紧急安全例外、用户申诉与偏好变化需要独立设计。

## 证据和局限

MARKET E1，仅人工数学反例及源码可复算；官方产品文档为 DOC_SUPPORTED；营销或功能声称未升级为独立科研证据。真人 E2 新增0，历史 E3 新增0，独立团队复现0，真实商业转化、定价敏感性、跨文化公平、因果决策改善均 NOT_RUN。没有接入敏感信息、没有新订阅、没有支付、没有调用计费 API 或启动 CI。账户免费额度及账单未独立核验。

下一项 MKT125：审查有标签延迟、选择性弃权后的校准评价与目标承诺的紧急停止边界。