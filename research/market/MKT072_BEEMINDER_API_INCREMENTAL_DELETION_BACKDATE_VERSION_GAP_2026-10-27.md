# MKT072 Beeminder API增量同步与历史更正的契约边界

日期：2026-10-27 Asia/Singapore。研究轨：market。状态：COMPLETE_BOUNDED_MARKET_E1。起点main HEAD：ce519a61b608cf202a905445f38f259658f4a296。主动新增费用0。

## 已有工作与官方来源
已核MKT071、MKT029至031、MKT043、E040、F002及最新R208。MKT071已研究2026-08-18发布的sqrt日聚合。本轮检查公开API如何表示历史记录与更正。
Beeminder官方英文API文档 https://api.beeminder.com/ ，本日读取。Goal属性包括aggday、roadall、fullroad、updated_at、secret、datapublic、numpts、pledge。单目标GET可选择datapoints，独立datapoints GET可全量或分页读取。User GET的diff_since按创建或更新时间返回目标和点，并明确列出deleted_goals；skinny只给最近点；datapoints_count按updated_at排序，历史日期的补录也可能排到最前。Datapoint包含id、timestamp、daystamp、updated_at、origin、creator、is_dummy、is_initial、requestid。POST的requestid是目标内幂等键，相同键不同内容会更新点。官方还提供点的PUT和DELETE。
对照官方2026-09-24更新的自定义目标帮助 https://help.beeminder.com/article/97-custom-goals 与2026-08-18博客 https://blog.beeminder.com/sqrt 。

## 真实机制与条件性风险
输入为手工或授权集成的datapoint。目标状态包含原始记录、日聚合规则、红线、缓冲、图像和可能产生收费的脱轨。用户选择目标，平台按规则反馈，未见经过独立验证的长期人生效用优化算法。
公开文档明确deleted_goals，但**没有明确承诺deleted_datapoints墓碑或增量删除事件**。如果第三方镜像只将diff_since记录合并进本地，原点被删除时可能留下幽灵数据。这属于文档契约缺口及条件性工程风险；不能据此断言实际服务器不发送删除事件。skinny及限制datapoints_count均不适合作完整历史备份。updated_at是更正时间，daystamp是行为日期，两者必须分开保存。
aggday作为Goal属性可读取；核对的Goal更新参数清单未列aggday，故无法确认公开API可以写入该字段。没有发现公开文档提供完整的历史配置版本或不可变评分收据。不能把“文档未载明”当作服务器绝对没有功能。

## 独立合成检查
执行无依赖Node脚本 `research/market/mkt072_beeminder_incremental_sync_synthetic_20261027.js`，30项断言全部通过。人工a/b/c三条记录总和300，模拟b从100改25、a从服务端删除，增量合并本地仍保留a，总和225；服务端当前真值125；全量对账后恢复125。skinny只保留最新c时漏掉b历史更正。另核对更新顺序与行为时间反转、sqrt日内拆分一致性。仅模拟假设的客户端和响应结构，没有连接Beeminder、验证真实删除响应、实际收费或真实长期行为效果。

## 隐私、费用与证据
secret与datapublic是独立的可见性字段；公开图可能暴露派生趋势。没有验证权限撤销后缓存、外部副本或历史评分删除。Beeminder存在订阅与脱轨收费，本轮仅阅读免费官方资料，未注册、购买、调用认证API或启用计费功能。
官方文档证据=DOCUMENTED_VENDOR_CONTRACT；30项模拟=INDEPENDENT_SYNTHETIC_CLIENT_TEST；服务器实际删除行为、版本保存、真实长期收益=UNVERIFIED。内部市场E1不代表真人E2或历史E3。

## 治理与下一轮
E041单独审计R208。2026-W44 F002已完成，新增风险候选为“删除后镜像残留”和“历史更正后派生评价未失效”，本周不重复创建F专题。MKT073优先固定Beeminder公开客户端与图计算源码，审查requestid同键更新、历史重算和回归测试。R系列完成后才统一归纳及模型熔炼。
