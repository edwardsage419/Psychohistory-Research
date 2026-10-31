# MKT179 Exist 与 Beeminder 历史更正和来源权威机制
研究日期：2026-11-01 Asia/Singapore；2026-10-31 UTC。目标键：(market,Exist_Beeminder,official_docs_2024_2026,source_authority_late_correction_reconciliation)。基线 main 829c49c43a5b48060aeb05dbc8591b6c437fe453。与 MKT178 的 Beeminder 历史结算反例互补，重点是 Exist 有限回填窗口和跨产品来源一致性。

## 直接核验的英文官方证据
1. Exist 2024-01-24 帮助页 https://kb.exist.io/article/53-how-can-i-fix-an-incorrect-data-point 明确说：第三方集成数据应在原始服务修改；该修改需处于过去7天，才会在后续 Exist 同步中更新。此为文档陈述，未在2026年真实账户中测试；具体集成可能存在差异。
2. Exist 开发者最佳实践 https://developer.exist.io/guide/best_practices/ ：官方集成通常每小时更新或更慢；建议同步昨日值及当日值、按需批量更新、OAuth 最小权限。https://developer.exist.io/reference/attributes/ 说明日级 date/value 和 service、manual、active 字段，带 values 的查询最多31天；API 版本2权限与属性所有权要求需按接口核验。
3. Exist 初次集成回填 https://kb.exist.io/article/63-how-much-data-will-sync-when-i-connect-a-service 2022-09-29文档称多数集成回填30天，部分至少14天。2019旧博客曾提及某些 iOS 属性60天，版本与集成不同，不能将初次回填与后续纠错窗口混为一谈。
4. Exist 手动记录 https://exist.io/page/help-manual-tracking/ ：数量、十进制、时长、1至9评分、时刻、百分比。部分数量/时长属性未填自动为零，其他类型未填保持缺失。https://kb.exist.io/article/99-how-can-i-delete-or-deactivate-an-attribute 说明集成/模板属性可停用但不能单独删除，用户自定义属性可删除。停用仍保留数据。
5. Beeminder 2026-09-24帮助 https://help.beeminder.com/article/41-can-i-export-my-data 说明CSV/TSV导出、datapoints API及webhook；webhook可能静默失败，建议完整对账。MKT178已读 https://help.beeminder.com/article/13-when-do-derailments-happen 的历史纠错可能重新触发偏离，未重新验证实际收费。
6. Exist 官方价格 https://exist.io/about/values/ ：月付 USD 6.99、年付 USD 62.90、30天试用后付费，官方取消说明 https://kb.exist.io/article/127-how-do-i-cancel-my-subscription 称无永久免费方案。仅审查资料，未注册、付款或调用API。

## 产品机制矩阵与证据边界
Exist输入为集成和人工日级值，状态为属性、服务来源、日期、数值、激活状态；相关性与趋势属于官方产品功能声明，真实因果识别及长期预测校准未获独立证据。其集成纠错由原始服务作为权威来源，已公开的七日回填限制形成较旧历史记录可能不同步的风险。Beeminder输入为目标datapoints及自动集成，状态为目标线、截止时间、累计值及偏离；历史纠错和webhook对账影响目标状态。产品算法完整实现、用户隐私安全有效性和现实行为改善效果均未独立验证。权限风险来自第三方连接、API及导出；具体实际授权记录没有读取。

## 实际人工实验
程序 research/market/mkt179_exist_beeminder_backfill_synthetic_20261101.js，归档Git blob eecca5b4bf7e0d57beb15c02ca9080b5941a076f。V8执行6项断言PASS。虚构日1至3值均为1，日2在日4更正为0，年龄2天，七日窗口假设下Exist镜像从3改为2，与来源一致；同一更正在日14才到达，年龄12天，假设按公开七日限制未重拉，Exist镜像仍3而完整来源2，标记UNKNOWN_RECONCILIATION_REQUIRED。另造丢失webhook的镜像2对来源3反例。Beeminder镜像2为研究用假设重放，不代表其真实API或产品实现。人工数据与日期无个人信息。
候选要求：来源版本和原始权威、有效日期与接收日期、可回填窗口、缺失值与真零、完整快照对账水位、纠错影响的已结算状态应分别记录。窗口外或数据不一致时保留UNKNOWN并暂停高影响自动处罚。此为未来知识储备，个人决策系统尚未开发。
证据：OFFICIAL_ENGLISH_PRODUCT_DOCS + INTERNAL_NONBLIND_SYNTHETIC_E1。真实产品独立测试 NOT_RUN，E2=0，E3=0。未新增费用。下步 MKT180：Exist 缺失与自动零对相关性/趋势的人工反例及不同集成的实际文档覆盖。
