# MKT165 ActivityWatch 历史回填与来源完整性候选检查

日期 2026-10-31 UTC。目标键 (market, ActivityWatch, aw-server-rust-fe353a66, history-backfill-and-device-provenance-gates)。研究基线 main f23038027379166a7456692a912d84a11a4f7f2f，写前观察 main 2e80b378f2f419e612aad19ff1c75453b4329dd8。承接 MKT162 设备目录去重与 MKT163/MKT164 来源身份问题，本轮新增历史前缀与内部缺口的覆盖边界。非盲态 E1。

## 固定原始资料

ActivityWatch Rust 固定提交 fe353a66ca3859231ce306a0f4faf15f732d8b41，aw-sync/src/sync.rs Git blob 1daffa82dec2efe877923f4789bc8c4c897b5c95。该源码的 sync_one 以目的桶最新事件结束时间作为增量游标，并在游标附近协调七天内编辑。较早缺失事件不会因一般增量继续导入而自动补齐。官方 issue #683 记录真实重复目录导致历史遗漏，#686 已合并以 device_id 去重和警告。上游维护者明确将完整历史自动回填留给后续版本，并建议旧版本删除目的桶后重新拉取。当前 v2 分段同步仍处于实验阶段，不能将其计划视为已部署修复。

官方原始来源：
https://github.com/ActivityWatch/aw-server-rust/blob/fe353a66ca3859231ce306a0f4faf15f732d8b41/aw-sync/src/sync.rs
https://github.com/ActivityWatch/aw-server-rust/issues/683
https://github.com/ActivityWatch/aw-server-rust/pull/686
https://docs.activitywatch.net/en/latest/syncing.html

## 本轮人工执行

程序 research/market/mkt165_backfill_provenance_synthetic_20261031.py 使用 Python 3 标准库运行，20 项断言全部通过。全部设备和事件为人工虚构。

1. 目的桶已有事件 7、8，来源完整包含 1 至 8。以最新目的事件作为游标的简化模型继续只保留 7、8，缺少六条早期事件。候选完整事件身份回填可恢复 1 至 8。
2. 同一设备两份来源中，400 字节的较大文件只含 6、7、8，100 字节较小文件含 1 至 5。按文件大小选择不能证明时间覆盖完整。经来源身份核验后的人工集合并集可恢复八条。
3. 目的事件 1、2、4、5 与完整来源 1 至 5 具有相同最早与最晚端点，内部仍缺少事件 3。只比较时间范围无法发现该缺口。
4. 不同 device_id 即使规范化显示名相同也必须拒绝合并；同设备不同 bucket 同样拒绝。重复来源保持幂等。

这里的 event_id 是人工稳定身份假设，真实 ActivityWatch 当前数据库不保证与该人工抽象完全一致。候选集合并集不是对真实同步系统可直接应用的补丁，冲突、修改、删除和来源伪造都需额外协议。没有运行 Rust、Android 或真实跨设备同步；不能将局部反例等同于当前发布版本可利用故障。

## 产品机制记录

真实输入是本地活动事件、bucket、hostname、device_id、同步文件及时间戳。状态表示包括来源目录、目标桶、增量游标和历史副本。算法目标是设备活动历史复制与查询，没有长期人生效用函数。反馈以同步状态、日志和警告为主，未发现自动的历史完整性证明。权限由本地应用及用户选择的文件同步工具共同决定，可能产生第三方副本。可解释性来自公开源码与文档。核心软件免费开源，第三方同步服务可能有独立费用，本轮没有使用。局限包括删除不传播、编辑窗口和历史回填未闭合。证据为真实源码与维护者 issue 文档支持，20项人工E1仅验证局部模型，实际故障率未知。

候选知识储备：设备不可变身份、显示名称、事件身份、来源授权、历史覆盖证明、删除墓碑和恢复权限应分别记录。对缺少身份或覆盖证据的历史迁移标记 UNKNOWN 并交人工复核。保持零新增费用，不开发个人决策产品、不改变R冻结协议。新增真人E2=0，历史E3=0。

下一步 MKT166 检查 v2 按来源事件ID追踪的实际实现与版本适用范围，避免重复旧版游标问题。
