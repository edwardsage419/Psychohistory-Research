# MKT065 pyeventsourcing历史版本快照选择与恢复边界

日期：2026-10-27 Asia/Singapore。轨道market。状态：COMPLETE_BOUNDED_SOURCE_SYNTHETIC_E1。初始HEAD：d4c79719256830b21e4418047983166a18f21701。主动新增费用：0。

## 去重与上游固定
已读取MKT064、E033、F002、R200和A轨当日新增记录。MKT064检查eventsource-py的快照前缀错误。本轮改查另一实现pyeventsourcing/eventsourcing，专门研究历史版本读取如何排除未来快照。固定官方默认9.5分支提交 bf665955d9243e728aaaa5bb62ac63b9cfe5ec19（2026-10-13），BSD 3-Clause。官方仓库 https://github.com/pyeventsourcing/eventsourcing ，固定源码 https://github.com/pyeventsourcing/eventsourcing/blob/bf665955d9243e728aaaa5bb62ac63b9cfe5ec19/eventsourcing/application.py ，blob 5b779166a6feed291cd912822e99937adfa7d7f8。固定上游测试 eventsourcing/tests/application.py blob 5bdd61289e2cb4b4eb22f30a73e2d752892f8e21。旧版英文官方文档 https://eventsourcing.readthedocs.io/en/v9.2.4/topics/application.html ，与固定9.5源码分开判断。

## 机制
输入：聚合体ID、持久化事件版本、目标历史版本、快照状态与快照版本。Repository._reconstruct_aggregate()约315至350行以desc=True、limit=1、lte=version选择不晚于目标版本的最新快照，再以gt=快照版本、lte=目标版本读取后续事件。无合格快照则从头重放。Application.take_snapshot()约826至851行调用repository.get()重建状态再保存快照。旧版官方文档与固定源码均支持历史版本查询。上游现存测试覆盖指定版本快照与历史恢复，测试文件本轮只读，未执行上游包。

## 19项人工验证
脚本 research/market/mkt065_asof_snapshot_synthetic_20261027.js，纯Node标准运行环境。人工事件v1:+5、v2:+7、v3:-3、v4:+2，快照v2/state12、v4/state11。19项检查全部通过。历史v3应得9，选v2快照后重放得到9；错误使用最新v4快照得到11。无快照、未来快照排除、同版本错误state99、跨分支错误状态、候选分支身份拒绝等边界均完成合成测试。仅模型化固定源码中的选择机制，未运行上游软件包或真实数据库。

## 产品方法映射
候选输入为事件ID、聚合体ID、事件版本、提交时间、记录时间、目标as-of版本、快照来源分支与授权generation。状态候选：ASOF_VERSION_BOUNDED、SNAPSHOT_PREFIX_UNKNOWN、BRANCH_MISMATCH、FULL_REPLAY_REQUIRED。目标：减少历史前视信息混入、提高回溯评分可重建性。反馈：快照与完整重放一致率、未来版本拒绝率、分支身份冲突率。解释性输出应列明采用快照版本和未验证前缀。候选保护：版本上界、从持久化事件重建、前缀摘要、分支绑定、提交高水位及抽样完整重放。均为研究候选。

官方README说明可选应用层加密、压缩、版本升级及并发控制，属文档支持，未作独立安全认证。历史快照可能保留撤销前敏感值，需沿用F002生命周期控制。BSD 3-Clause源码免费，默认内存与可选SQLite适合零新增费用审查，其他部署成本未核。未预设唯一人生效用权重。

## 证据与风险
DOCUMENTED：固定源码的lte快照选择、gt事件重放和take_snapshot重建。SYNTHETIC：19/19人工断言。INFERENCE：同版本错误快照仍可能被读取，所检查路径未展示事件前缀哈希或分支校验，不能据此声称整个项目没有其他保护。MARKET E1；UPSTREAM_PACKAGE_EXECUTION=NO；REAL_INCIDENT=NOT_VERIFIED；EXTERNAL_REPLICATION=NO；PERSONAL_OUTCOME=NOT_VERIFIED。
风险R1：历史请求误选未来快照。R2：同版本错误状态或异分支快照。R3：旧快照恢复已撤销敏感信息。
下一轮MKT066检查上游实际包的历史版本、缓存与持久化边界测试。F002本周已完成，不重复专题。保持先完整R系列、再归纳、最后熔炼。
