# MKT066 pyeventsourcing缓存快进、历史读取和并发一致性边界

日期：2026-10-27 Asia/Singapore。轨道：market。性质：固定英文源码深读与人工合成验证。MARKET E1。新增主动费用0。

## 去重、来源及固定版本
已读取main最新HEAD、MKT065、E034、F002、本周子任务及最新R202。MKT065已经研究历史快照版本上界，本轮专门审计Repository.get()的缓存与历史读取两条执行路径，避免重复。固定上游pyeventsourcing/eventsourcing提交 bf665955d9243e728aaaa5bb62ac63b9cfe5ec19（2026-10-13），源码 eventsourcing/application.py 第203至360行，测试 eventsourcing/tests/application.py 第246至469行。英文官方说明 https://eventsourcing.readthedocs.io/en/stable/topics/application.html 。源码 https://github.com/pyeventsourcing/eventsourcing/blob/bf665955d9243e728aaaa5bb62ac63b9cfe5ec19/eventsourcing/application.py 。项目仓库 https://github.com/pyeventsourcing/eventsourcing 。官方项目BSD 3-Clause，公开源码审查免费，实际部署成本未验证。

## 新增机制与边界
输入：聚合体ID、持久化事件序列、可选version、cache_maxsize、fastforward、fastforward_skipping、deepcopy_from_cache和并发锁。状态：缓存的聚合体版本、已持久化最大版本、是否锁争用、是否按指定历史版本读取。

固定源码第265行仅当缓存存在且version=None时进入缓存分支。缓存命中并启用fastforward时，以缓存版本为gt查询新事件，尝试在锁保护下快进；若配置或单次调用允许fastforward_skipping，锁争用时可跳过快进并返回缓存对象的旧版本。未启用fastforward时，缓存命中亦可返回先前版本。指定version的历史查询绕过缓存，直接从事件与合格快照重建。第305至307行默认深拷贝缓存结果；明确关闭深拷贝时，调用者可获得共享缓存对象引用。

上游测试明确覆盖缓存快进、锁争用两种模式、禁用快进以及禁用深拷贝的共享引用行为。测试中禁用快进且缓存失效的案例可能造成写入IntegrityError。以上属于源码和测试支持的条件性行为，不能推断默认配置会发生持续旧读或安全事故。未运行上游完整软件包。

## 23项人工分支检查
独立Node标准库脚本 research/market/mkt066_cache_contract_synthetic_20261027.js 构造版本1:+5、版本2:+7、版本3:+3，分别检验正常快进、关闭快进、允许跳过且锁忙、单次跳过、指定历史版本绕过缓存、默认深拷贝与显式共享引用。23项断言通过，失败0。人工模拟选定的控制分支，不模拟上游完整线程调度、数据库事务或真实竞态；无法证明线上发生率。

## 对未来决策研究的候选映射
目标：历史回放无未来信息、当前读取显示新鲜度、并发时明确是否允许旧读。反馈：返回版本与持久化高水位差、旧读比例、历史版本重建一致率、缓存共享引用变异检测。解释性：输出requested_version、returned_version、observed_store_version及consistency_mode。候选状态FRESH_CONFIRMED、STALE_ALLOWED、HISTORICAL_VERSION_BOUNDED、FRESHNESS_UNKNOWN。若用于决策基准，重要建议需能请求版本固定的历史状态并显示不确定性；这些都是候选设计，未开发个人产品。

隐私权限：缓存、快照和旧版本可能保存已撤销来源的敏感值，单凭深拷贝或历史版本上界不能证明已删除。F002的授权generation、衍生依赖与备份生命周期候选控制继续适用。所查代码路径未显示完整授权撤销验证，不能据此断言整个库没有其他安全措施。无真实敏感数据输入。

证据：SOURCE_CODE_DOCUMENTED为固定源码分支和上游测试；SYNTHETIC_EXECUTED为23/23人工断言；INFERENCE为决策系统的版本可解释性和权限代际隔离。UPSTREAM_PACKAGE_EXECUTED=NO；REAL_INCIDENT=NOT_VERIFIED；EXTERNAL_REPLICATION=NO；PERSONAL_OUTCOME=NOT_VERIFIED。下一轮MKT067检查另一个事件存储实现的并发读取一致性或本库上游真实测试，并与MKT065、MKT066比较。R系列优先顺序不变。
