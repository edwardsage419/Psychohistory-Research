# MKT178 Beeminder 历史数据更正与同步完整性机制审查
日期：2026-10-31 UTC。目标键：(market,Beeminder,official_help_2026-09-24_2026-10-22,retroactive_deadline_webhook_reconciliation)。基线 main 189321329c2bc8760e193d75083b384f8f9d282a。

## 新增的官方机制证据
官方英文帮助文档 https://help.beeminder.com/article/13-when-do-derailments-happen （2026-10-22更新）明确说明：常规目标在每日截止时判定；历史 datapoint 删除或自动来源重写可能使上一次截止点的累计进度跌破红线，从而立即触发 derailment。该规则可能影响真实金钱质押，因此研究仅阅读公开资料。https://help.beeminder.com/article/39-how-do-i-fix-incorrect-data （2026-09-22更新）指出自动数据来源可能覆盖在 Beeminder 侧直接修改的历史记录，历史纠错通常需先修复来源。https://help.beeminder.com/article/41-can-i-export-my-data （2026-09-24更新）确认 CSV/TSV 导出、datapoints API 和 webhook，并明确 webhook 失败可能无通知，建议定期与完整数据对账。https://help.beeminder.com/article/37-how-do-i-enter-data-to-my-goal 说明日期、数值、备注输入及部分自动来源在截止前更新。官方收费说明 https://help.beeminder.com/article/19-how-much-does-beeminder-cost （2026-03-06更新）显示免费起步可能随偏离触发最低5美元收费，某些配置需要付费；本轮没有注册、付款或调用 API。

## 输入、状态、算法、反馈和限制
真实文档支持的输入为带日期/数值/备注的目标 datapoint，来源可能为人工输入或第三方自动数据。状态为目标累计进度、目标红线、截止时点、安全缓冲与偏离结果。算法的精确内部实现未公开核验。反馈机制包含临近截止提醒、历史更正后的状态重评和人工申诉；涉及金钱承诺的效应不能由营销描述推断为行为因果改善。隐私与权限方面，导出及 webhook 会把个人行为记录送往用户选择的目的地，权限与保存期需逐接口评估；没有检查产品实际安全控制、源代码或个人数据。

## 独立人工测试
实际执行 Node.js 22.16.0 标准库程序 research/market/mkt178_beeminder_event_time_replay.js，Git blob 8062bd36c705cfe4813fc7d5edbca301aea43f5d。虚构三日目标，截止日3、阈值3、三条各加1的记录。历史第2日数据在第4日更正为0，重放后的截止日3累计从3降为2，状态 SAFE 变 BELOW；未重算的旧快照仍错误显示3。模拟 webhook 丢失一条事件时镜像累计2、来源完整快照3；模拟重复事件时未去重累计3、按ID去重后2。完整来源快照对账恢复3；重复ID与未知纠错ID的守卫均按预期拒绝。Node --check 与实际运行 PASS。所有事件、阈值及数据均为人工构造，未调用 Beeminder API，也未验证其内部计算或收费行为。

## 对心理史学未来研究的候选知识
若未来需要目标偏离控制，应分别保存事件有效时间、系统接收时间、来源版本、纠错关系、上次截止快照和同步水位。同步缺失时标记 UNKNOWN，避免据此自动产生高影响处罚。目标权重保持用户可调整、可解释，不预设唯一人生效用。此处是产品机制知识储备，个人决策产品开发继续暂停。

证据等级：OFFICIAL_PRODUCT_DOCUMENTATION + INTERNAL_NONBLIND_SYNTHETIC_E1。独立真实产品验证 NOT_RUN；真实个人决策 E2=0，历史 E3=0。无新增费用。下步 MKT179：比较 Beeminder 与 Exist 的时间戳、回填和数据来源权威机制，或恢复 MKT177 真实序列分块覆盖率检验。
