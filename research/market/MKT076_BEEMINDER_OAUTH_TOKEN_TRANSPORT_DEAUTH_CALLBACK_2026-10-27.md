# MKT076 Beeminder OAuth令牌传输、撤销回调与日志边界审计

日期：2026-10-27，Asia/Singapore。轨道：market。状态：COMPLETE_BOUNDED_MARKET_E1。主动新增费用：0。

## 去重、来源和固定版本

开始时main HEAD为17fbd1827966ae7a79f559d51aa31c3bf7f88118。已读取MKT071至MKT075目录记录、MKT075全文、E044、F002、R212和R213增量登记。本轮从MKT075的第三方JS客户端URL认证位置，转向官方OAuth协议和授权撤销回调，避免重复审计同一客户端。

英文官方API参考：https://api.beeminder.com/ 。对应公开官方源码：https://github.com/beeminder/apidocs/blob/21e92e36bc15add4bcbe2944842215ab24e9aa0a/source/index.html.md ，固定提交21e92e36bc15add4bcbe2944842215ab24e9aa0a，Git blob 8af20e66b6663ef1deefabb9493e145c64b0f30d，提交时间2026-09-29T23:47:58Z。官方帮助：https://help.beeminder.com/article/110-apps-and-api ，描述用户可撤销应用授权。两者为产品自身说明，尚未进行真实账户验证。

## 新增机制证据

1. 官方文档区分个人auth_token与第三方客户端access_token；二者参数名称不同。个人令牌用于自己的账户，第三方OAuth用于用户授权的客户端。
2. 官方OAuth文档要求response_type=token，授权完成后把access_token与username作为redirect_uri的查询参数交付。示例使用http回调地址；文档示例不能推断实际生产服务器接受所有不安全回调地址。查询参数可能被完整URL日志、浏览器历史、监控系统保存，实际泄露未验证。
3. 官方同时支持以URL参数access_token或HTTP Authorization: Bearer传递客户端令牌。Bearer头能使普通API请求URL不含令牌；它无法消除授权重定向时URL查询参数的风险。MKT075第三方JS客户端的URL令牌问题与此相邻。
4. 可选的Post De-Authorization Callback在用户撤销客户端授权后向应用POST，文档明确请求体只有access_token字段。公开参考未说明回调签名、重试保证、时序或送达SLA。不能据此断言服务器没有额外安全保护，也不能把收到回调等同于所有旧缓存和外部副本已经删除。
5. 官方API另提供Charge Resource和POST /charges收费端点。令牌授予的实际权限范围、是否存在细粒度scope和服务端风控没有独立验证。候选未来集成必须对财务动作实行明确拒绝和人工授权；本项目不调用任何收费端点。

## 离线实验

脚本research/market/mkt076_oauth_deauth_synthetic_20261027.js使用纯虚构令牌、构造URL及本地状态机。31项检查，失败0，网络请求0。验证查询参数令牌可进入原始URL日志；Bearer请求URL不含令牌；针对URL、Authorization和auth_token的候选脱敏可移除合成令牌；未通过候选校验的回调不改变授权状态；已通过校验的合成撤销事件使generation递增、取消队列、使衍生状态过期，并拒绝旧generation在途响应。

校验开关validated是人工模拟的前提，未实现真实服务端回调身份验证。脱敏正则仅覆盖示例文本，不是生产级安全保证。31项检查只支持条件性工程结论，不能作为Beeminder真实漏洞、真实撤销成功或安全认证证据。

## 产品方法字段

真实数据输入：目标、数据点、时间戳、第三方应用授权与OAuth令牌；本轮没有读取任何真实账户数据。状态表达：目标轨迹和历史数据点，以及应用授权状态；generation、派生数据失效标记为项目候选状态，并非官方产品字段。算法：官方API允许读写目标和数据点，Beeminder的轨迹计分和聚合已在MKT071至MKT074审阅；OAuth令牌机制自身不是个人预测算法。目标与反馈：目标图、承诺和偏离反馈。自我修正：历史数据编辑、撤销应用访问、回调通知；旧数据派生物清理效果未验证。隐私权限：个人令牌、第三方访问令牌、可撤销授权、日志和重定向边界。解释性：接口参数可核，令牌权限的细粒度范围和撤销时序未充分公开。费用：官方存在有限免费目标、会员和脱轨收费及收费API；本轮未注册、调用API、购买产品或启用付费功能。局限：官方文档不是独立安全审计，生产日志、实际撤销和长期行为效果均未验证。

## 候选控制与风险

MKT076-C1：未来外部服务若支持Bearer请求头，应优先避免把访问令牌写进普通API URL；日志、异常、追踪和导出统一脱敏。授权重定向另行审计，不能因API调用使用Bearer而忽略重定向URL。
MKT076-C2：收到撤销回调前先验证来源及关联授权，防止伪造事件导致拒绝服务；文档未给出可直接依赖的签名机制，应标记实际验证方案待研究。
MKT076-C3：授权撤销使generation增加，停止后续读取、取消待处理任务、使依赖旧授权的派生数据待复核；保留外部副本未知状态。
MKT076-C4：付款、收费、删除或其他不可逆动作默认禁止自动执行，未来如有需要须独立人工授权。
MKT076-R1 HIGH：令牌进入URL日志或重定向记录。R2 HIGH：撤销后旧队列继续处理。R3 MEDIUM：伪造回调导致错误撤销。R4 HIGH：授权范围或收费能力误判。均为候选风险，尚无真实事故证据。

## 证据等级与后续

官方API固定源码及官方帮助：VENDOR_DOCUMENTED。离线31项：SYNTHETIC_CONTRACT_CHECK。实际生产行为、漏洞、权限范围和长期决策收益：UNVERIFIED。MARKET E1知识储备，不提升真人E2、历史E3，不设唯一人生效用权重，不提前开发决策产品。F002本周已完成，不重复创建F003。下一轮MKT077：核对官方OAuth文档中回调重试、令牌权限及服务端测试是否有新增公开证据；若无，切换ProjectionLab或Exist的目标修订机制。

归档：本文件和独立脚本增量写入research/market。提交SHA须以远端写入后实际核验为准。零新增费用；GitHub账户总体账单未独立核验。
