# MKT164 ActivityWatch 同名设备与直接目标桶命中边界

日期：2026-10-31 UTC。目标键：(market, ActivityWatch, aw-server-rust fe353a66, direct-raw-sanitized-destination-id-collision)。基线 main HEAD：6aa5c0419bbe3ad57b87b787ca069622eac74f0d。前序 MKT163 已研究 legacy origin fallback，本轮单独检查其前面的 raw 和 sanitized 直接命中分支。内部非盲态源码审计与人工 E1。

## 固定来源与机制

固定上游 Git commit fe353a66ca3859231ce306a0f4faf15f732d8b41，文件 aw-sync/src/sync.rs，Git blob 1daffa82dec2efe877923f4789bc8c4c897b5c95。
https://github.com/ActivityWatch/aw-server-rust/blob/fe353a66ca3859231ce306a0f4faf15f732d8b41/aw-sync/src/sync.rs

get_or_create_sync_bucket 的 pull 路线依次用原始来源名称构造目标桶 ID 并 get_bucket，命中即返回；否则使用规范化名称再次 get_bucket，命中即返回；之后才执行历史元数据候选扫描。两个直接命中分支均未检查 source device_id 与目标设备身份绑定。sync_datastores 中 src_did 主要用于来源 hostname 为 unknown 的 push 替换；该函数调用 get_or_create_sync_bucket 时没有将远端 RemoteDb.device_id 作为身份约束传入。源码注释明确把未来 (device_id,id) 身份改造指向 ActivityWatch/activitywatch#302。当前实现的命名来源可能发生别名碰撞。

新补充边界：原始 ID 直接命中发生在 unknown hostname 拒绝检查之前；已有同名目标桶时可能绕过后续 unknown 检查。这里只证明源码控制流的顺序，实际数据是否存在此类目标桶及真实影响尚未验证。

官方同步说明：https://docs.activitywatch.net/en/latest/syncing.html 。本地优先，设备间同步通过用户选择的文件同步工具，活动数据被复制到其他设备；设置不参与同步，删除传播尚不支持，编辑传播有七天窗口。核心开源免费，无需为本轮研究购买或注册服务。

## 人工实验

程序 research/market/mkt164_aw_direct_lookup_collision_20261031.py，Python 3.13.5 标准库实际执行15项断言，全部 PASS。两台完全虚构设备 device_A 和 device_B 分别使用 Office Laptop 与 office_laptop 名称；规范化后均为 office_laptop。已有目标桶属于 A，B 的 raw ID 命中同一桶，A 的 sanitized ID 也命中同一桶。模型中的 device_id 不同，直接命中仍复用目标桶。不同基础 bucket ID 不发生该特定碰撞；未知来源在没有既存 raw 桶时拒绝，存在既存 raw 桶时先命中。无任何真实用户数据。

这是从固定源码分支构建的局部人工反例。没有执行原生 Rust、Android、真实数据库或完整 sync_run，不能宣称当前发布版本存在已利用漏洞。模拟中的目标桶 device_id 字段属于人工附加的审计标记，不能冒充当前 ActivityWatch 数据库真实字段。

## 产品机制与候选知识

输入：设备文件夹 device_id、bucket ID、hostname、$aw.sync.origin、活动事件。状态：原始/规范化 ID、历史候选、目标桶、同步游标。算法目标：同步各设备活动事件，尚无个人长期效用优化。反馈：日志警告、拒绝、目标桶复用或新建。解释性：源码可检查。隐私与权限：本地优先，跨设备副本由用户选择的同步服务管理，设备身份和删除状态仍有边界。费用：免费开源，第三方同步服务费用需另行核实，本轮没有使用收费服务。局限：未执行原生端到端测试，不能推断真实故障发生率。

候选控制：把不可变设备身份、可更名显示名称、事件来源、历史迁移映射分开；所有直接命中分支也要求来源身份验证；旧桶缺少可验证 device_id 时标记 UNKNOWN 并提供受控迁移，不能凭 hostname 自动归属。未来个人决策数据须保留历史修订与删除状态。仅作为研究知识储备，不开发产品、不改变 R 系列冻结协议或个人效用权重。

证据：固定真实 Rust 源码为工程文档支持；15项人工 E1 为内部模型验证；营销声称不计作科研证据；原生系统实测 NOT_RUN；新增真人 E2=0，历史 E3=0。下一步研究目标桶设备身份迁移时的历史回填完整性与冲突拒绝规则。
