# MKT075 Beeminder第三方JS客户端凭据位置与历史读取控制审计

日期：2026-10-27 Asia/Singapore。研究轨：market。状态：COMPLETE_BOUNDED_MARKET_E1。主动新增费用：0。

## 去重与固定来源

已读取MKT071至MKT074、E043、F002及当日仓库记录。本轮研究此前未覆盖的第三方JavaScript客户端实际URL构造与历史读取参数。Beeminder英文官方API参考 https://api.beeminder.com/ 规定数据点GET支持sort、count、page、per，page从1开始，指定page时count忽略，未指定page时per忽略，未指定count时默认返回全部数据点。GET/DELETE端点接受认证token，接口文档没有要求第三方把凭据置于URL查询字符串。

第三方客户端 https://github.com/czr/beeminder-js 固定master提交 a5f2c95b47f89d22d812f6bd3f49cc28180efcbc，beeminder.js Git blob 2a0f29c5ac34e76a90131b7bc860c54c70c9cdb8，beeminder.test.js blob 5de1f36f384fbdb24d45c35c3c7efc8c65832eb9，package.json blob 3a63c89f817f368e819b3025b0f6f953c0be4f37。源码许可证MIT，版权2019 Colin Z. Robertson。原样源码与许可证保存在fixtures路径供离线复核。

## 实质新增：源码级认证位置与客户端接口限制

固定源码中Goal.datapoints()和Goal.deleteDatapoint()将auth_token直接拼入请求URL的查询字符串。Goal.createDatapoint()和Goal.updateDatapoint()则将auth_token放入application/x-www-form-urlencoded请求体。测试文件对GET和DELETE完整带token URL进行断言，说明这一行为是固定版本测试所认可的接口形态。假设代理或调试日志记录完整URL，凭据将出现在这些日志中；没有证据证明任何真实日志已经泄露。

Goal.datapoints()无参数，调用axios.get后直接返回response.data。客户端没有暴露page、per、count、sort、diff_since参数，也没有create_all批量接口。官方文档默认返回全部数据点，因此不能把该客户端无分页参数直接解释为实际遗漏数据。对长历史和增量对账，调用者无法借该方法限定单页或更新窗口；实际内存、时延和API限流未测试。

离线复核使用从GitHub连接器取得并按原样保存的上游源码，计算Git blob SHA严格等于2a0f29c5ac34e76a90131b7bc860c54c70c9cdb8。Node VM注入模拟axios和qs，不安装依赖、不发送HTTP、不使用真实token。43项断言通过：GET/DELETE URL含虚构token；POST/PUT URL无token且请求体含token；完整URL模拟日志会包含token；模拟401错误的原始cause若带请求config仍可保存URL；返回51条模拟历史记录且未携带分页参数；客户端没有批量方法。仅模拟条件被验证，真实服务器、日志系统、依赖库行为和第三方部署均未验证。

## 产品机制及适用边界

输入：用户目标、时间戳、daystamp、value、comment、requestid。状态：按目标保存数据点、目标轨迹与缓冲。算法：官方支持多种日聚合及轨迹评分；本客户端只包装CRUD，无本地预测模型。目标：反馈与承诺执行。自我修正：官方允许修改或删除历史数据，客户端提供单点更新和删除；没有独立冲突版本检查或完整历史修订日志。解释性：原始数据点和目标图可见，旧规则重算解释仍须保留版本。权限：官方secret、datapublic及认证机制存在；第三方URL凭据、日志和外部缓存需分别核查。费用：官方产品存在有限免费目标、付费会员和偏离收费；本研究仅使用公开免费文档与MIT源码，未注册、购买或调用收费服务。

候选控制：使用不会进入URL日志的授权传输方式并确认服务端接受的机制；敏感token不得出现在调试日志、异常序列化和持久审计记录；完整读取需限制批量大小并校验分页终止；对历史删除和回填定期全量对账；撤销后旧凭据与缓存状态分别核验。均为未来候选控制，不提前开发个人决策产品。

证据：官方API参数为DOCUMENTED_VENDOR_CONTRACT；第三方源码与测试为PINNED_SOURCE_INSPECTION；43项为INDEPENDENT_OFFLINE_SOURCE_EXECUTION；真实服务日志泄露、行为收益与外部效果为UNVERIFIED。内部MARKET E1，不提升真人E2或历史E3。

下一轮MKT076：比较官方OAuth token处理和第三方客户端的日志脱敏、分页对账测试，优先固定源码及真实离线测试；不接入账户。
