# MKT163 ActivityWatch 旧设备身份迁移与来源映射歧义

日期：2026-10-31 UTC。目标键：(market, ActivityWatch, aw-server-rust fe353a66, legacy-origin-migration-ambiguity)。证据等级：固定版本真实Rust源码、公开上游问题记录、内部人工E1。

## 新增实际机制
固定源码 https://github.com/ActivityWatch/aw-server-rust/blob/fe353a66ca3859231ce306a0f4faf15f732d8b41/aw-sync/src/sync.rs 的 get_or_create_sync_bucket 依次尝试原始来源ID、规范化来源ID、历史桶元数据扫描。历史回退扫描要求基本bucket ID相同，且 $aw.sync.origin 规范化后相同。唯一候选时重用；多个候选时明确拒绝并要求人工去重；没有候选时新建。规范化后为 unknown 的新导入会被拒绝。已检查的历史回退匹配条件没有比较 device_id。

2026-08 的上游 issue #649 曾描述来源元数据在push阶段不可靠。固定2026-10源码已明确在push staging清除 $aw.sync.origin，并仅在pull/import时写入。旧issue不能替代当前源码。上游 #302 仍为OPEN，设备ID全面取代hostname的迁移尚未闭合。#683和已合并#686解决了按设备ID筛选重复文件的特定问题，旧目的桶历史回填仍需另行处理。

## 人工实验
执行 Python 3.13.5 标准库 research/market/mkt163_aw_origin_identity_synthetic_20261031.py，11项断言通过。覆盖直接原始ID命中、规范化ID命中、单一旧桶重用、两个旧桶规范化来源相同而拒绝、未知来源拒绝、基本ID不匹配、新建和缺失旧元数据。两个不同device_id但同规范化hostname的人工输入可在唯一旧候选分支重用旧桶。该反例说明已检查分支缺少设备身份绑定；真实系统是否存在可触发的跨设备错误归属尚未验证，不声称发现已利用漏洞。原生Rust测试、真实数据库和真实同步未执行。

## 产品信息
数据输入：本地活动事件、设备ID、hostname、bucket ID、可选来源元数据及历史同步副本。状态：已有目的桶、规范化来源、同步游标。反馈：警告、拒绝、重用或新建。目标：跨设备活动数据汇集，没有发现人生效用优化算法。解释性：源码可审计。隐私：本地优先，跨设备数据可能经用户选择的同步服务复制；官方说明删除尚不跨设备传播。费用：核心功能免费开源，赞助可选，不购买任何服务。

## 候选知识储备
未来版本化个人数据应把设备不可变身份、事件来源、显示名称和历史映射分开保存。身份不明或多候选时保留UNKNOWN并要求审查。历史回填必须核对时间覆盖及删除状态。没有改变R系列主线、冻结协议或个人效用权重。新增真人E2=0，历史E3=0。

来源：https://github.com/ActivityWatch/aw-server-rust/issues/649
https://github.com/ActivityWatch/activitywatch/issues/302
https://github.com/ActivityWatch/aw-server-rust/issues/683
https://docs.activitywatch.net/en/latest/syncing.html
