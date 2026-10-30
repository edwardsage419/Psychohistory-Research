# MKT162 ActivityWatch 设备身份重复与历史回填边界

UTC 2026-10-30，market 轨。初始观察 main 0534e0e2a7dff15b5ab6442b27f6027b99ef04cf。目标键：(market, ActivityWatch, aw-server-rust fe353a66, device-id-duplicate-history-and-largest-file-limit)。状态 COMPLETE_BOUNDED_SOURCE_SYNTHETIC_E1。

## 固定来源与时间
上游固定提交 fe353a66ca3859231ce306a0f4faf15f732d8b41：
https://github.com/ActivityWatch/aw-server-rust/blob/fe353a66ca3859231ce306a0f4faf15f732d8b41/aw-sync/src/util.rs
https://github.com/ActivityWatch/aw-server-rust/blob/fe353a66ca3859231ce306a0f4faf15f732d8b41/aw-sync/src/sync_wrapper.rs
https://github.com/ActivityWatch/aw-server-rust/blob/fe353a66ca3859231ce306a0f4faf15f732d8b41/aw-sync/src/sync.rs
上游真实故障 issue #683，2026-09-15 提出，2026-10-11 关闭：https://github.com/ActivityWatch/aw-server-rust/issues/683
上游修复 PR #686，2026-09-16 已合并：https://github.com/ActivityWatch/aw-server-rust/pull/686
官方 2026-10-06 同步说明：https://activitywatch.net/blog/syncing-your-activitywatch-devices/
官方当前同步说明：https://docs.activitywatch.net/en/latest/syncing.html
官方免费与可选赞助：https://activitywatch.net/subscribe/

## 真实产品机制
输入：设备活动时间、持续时间、事件内容、bucket 主机名、设备 ID、同步 SQLite 文件。状态：设备来源目录、远端数据库大小、目的 bucket 最新事件游标、已有历史覆盖范围。旧同步按目的最新事件推进，若同一设备在两个主机名目录出现，较短且较新的历史先导入，随后完整历史的旧记录可能被游标跳过。#683 记录了真实单设备两目录的故障报告，短库 4,068 事件与长库 1,027,343 事件，属于上游 issue 报告的现场观察，未由本轨独立取得真实数据库复算。

#686 已合并的代码按 device_id 合并远端目录候选，选择文件字节数最大的数据库，记录跳过的重复目录，并在来源事件数大于目的事件数且没有新增导入时发出历史缺失警告。修复说明明确：原有目的库已被截断时，不会自动回填；来源身份完全改为 device_id 的工作不在该 PR 范围内。不能把 issue 曾存在写成当前版本仍未修复。

目标：跨设备活动数据同步和可视化。反馈：aw-sync status、同步日志、警告；没有核实决策优化目标或个人效用权重更新算法。解释性：公开 Rust 代码、issue 和 PR，适于审计实际数据处理路径。权限和隐私：本地优先；跨设备复制取决于用户选用的 Syncthing、网盘或其他文件同步工具，外部副本需要独立盘点。官方文档明确删除不会同步传播，设置不参与同步，历史编辑同步存在七天窗口。

费用：软件完整功能免费开源，官方可选赞助 Personal USD 5/月或50/年、Business USD 20/用户/月；赞助不解锁额外功能。本轨未购买、安装、配置同步、访问真实用户数据或产生新增费用。

## 实际人工E1实验
执行 Python 3.13.5 标准库 research/market/mkt162_duplicate_device_identity_20261031.py，13 项断言通过。虚构完整事件为1至8，短库为6至7；短库先导入再导入完整库只剩6、7、8，反序可保留1至8。模拟按同一 device_id 选最大文件时可优先选择完整库，结果不再依赖发现顺序。另构造一个反例：100字节的较大文件只含6、7、8，10字节较小文件独有1至5；单纯按文件大小选取仍丢失5项旧事件。文件大小只是代理指标，不能证明时间覆盖完整。

## 证据与限制
官方说明与固定源码：实现层直接支持。上游 issue 真实案例：开发者问题记录，未经本轨独立原始数据库验证。已合并 PR：可核实工程修复范围。人工13项：E1，仅验证简化模型。原生 Rust 执行、真实跨设备回填、随机文件系统顺序及真实用户长期行为改善均 NOT_RUN。候选未来要求：稳定设备身份与历史来源映射、事件时间覆盖核对、修订与删除版本分离、历史缺口 UNKNOWN、可审计的手动恢复。保持先完成R系列后归纳与熔炼，不提前开发决策产品。新增E2=0，E3=0。
