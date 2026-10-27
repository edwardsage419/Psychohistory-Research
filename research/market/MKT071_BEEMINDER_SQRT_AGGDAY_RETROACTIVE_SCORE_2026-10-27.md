# MKT071 Beeminder 2026年sqrt日聚合与历史分数重解释

日期：2026-10-27 Asia/Singapore。轨道：research/market。状态：COMPLETE_BOUNDED_MARKET_E1。主动新增费用0。

## 起点与去重

读取main HEAD 3b4db1d8d37b0c03a0bb2a91b343bf1017bbcc75、MKT001至070、E039、F002及最新R/B/A/TH/C/D。MKT001已有分段红线，MKT029至031已有历史更正和隐私，MKT043已有描述基准与承诺漂移。本轮聚焦新的日聚合变换。

Beeminder官方英文博客2026-08-18介绍新的aggday=sqrt，官方Custom goals帮助页2026-09-24更新列出sqrt=square root of the sum。博客承认Beebrain与Beebody上线时间记录存在差异，故2026-08-18仅是公开介绍日，不代表所有服务端部署时间。

来源：
1. https://blog.beeminder.com/sqrt （2026-08-18）。
2. https://help.beeminder.com/article/97-custom-goals （2026-09-24更新）。
3. https://help.beeminder.com/article/19-how-much-does-beeminder-cost （2026-03-06更新）。
4. https://help.beeminder.com/article/102-privacy 。
5. https://help.beeminder.com/article/13-when-do-derailments-happen 。
6. https://help.beeminder.com/article/23-can-i-have-goals-without-pledges 。

## 输入、状态、算法、目标与反馈

输入为手动或第三方授权同步的日内datapoints，状态包含原始数值及日期、日聚合模式aggday、聚合后得分、累计进度、分段红线、剩余缓冲与截止时间。官方公式为 g_t=sqrt(sum_i x_ti)。多数Do More目标采用sum，unary仅计是否出现数据。sqrt先在日内求和再开方，不是逐条开方求和。

目标仍由用户配置。若原始目标是每天100单位，则sqrt计分目标可设10；额外投入得分递减，能保留超额反馈并减少集中投入产生的安全缓冲。博客举例以写作、步数和任务启动为用途。此处的计分变换不证明真实长期效用、因果收益或个体自我学习。官方未披露自动从长期人生结果中优化价值权重的机制。

历史更正：帮助文档明确更改aggday等自定义设置会应用于整个历史图，可能立即触发derailment。历史datapoint编辑和自动数据回填也可能改变安全状态。未取得生产环境的历史版本保留、收费撤销或日志完整性验证。

隐私：官方说明新目标默认图公开、具体datapoint默认隐藏，可改为私有；图像和统计仍可暴露趋势，工作人员在支持与故障处理场景可能访问。撤权后缓存和派生趋势删除未核验。费用：自定义目标通常需要Bee Plus或Beemium订阅，普通目标脱轨可能收费，7天0美元试用不能保证永久零费用风险。本轮仅阅读公开资料，未注册、订阅、购买或调用认证API。

## 合成算术测试

标准Node脚本 `research/market/mkt071_beeminder_sqrt_synthetic_20261027.js` 已执行24项断言，全部通过，0失败。仅检验官方公式数学含义，不模拟真实服务端的缓冲、舍入、扣费或历史状态。

| 两日原始投入 | 总原始量 | sqrt日分值合计 |
|---|---:|---:|
| 100,100 | 200 | 20 |
| 200,0 | 200 | 14.14213562 |
| 400,0 | 400 | 20 |

同日(30,70)和(100)都得10分。相同200单位分散在两日得20分，集中在一天只得约14.14分。若第二天100被更正为0，计分由20变为10。若同一历史从sum切换sqrt，原始两日累计分数由200变20。后两项是纯数学反例，不能推断真实生产服务追溯扣费或保存哪版评分。

## 候选控制、证据边界和下一项

候选：分别保存原始量、聚合函数版本、分段目标、缓冲与时间；历史重算要显示受影响日期、原值与新值。检验日内拆分不变性、跨日分配敏感性、单位尺度与脆弱情境的适用性。sqrt仅对非负总量有实数定义；负值、缺失、自动同步冲突及舍入行为待上游源码验证。用户始终保留人工撤回与纠错，禁止将单一行为得分当作人生效用。

证据：官方博客与帮助=DOCUMENTED_VENDOR_MECHANISM；24项合成断言=INDEPENDENT_SYNTHETIC_ARITHMETIC；上线全量覆盖、真实长期效果、外部验证=UNVERIFIED。MARKET_E1仅为内部商业机制标签。

E040另行归档R207精确审计。F002已完成2026-W44专题，本轮仅登记历史计分重解释与公开图派生信息泄露候选风险，F003仍在下周研究错误偏好归因与人工纠错。下一轮MKT072优先核对公开API中aggday字段、历史导出及版本保存契约，严格零新增费用。
