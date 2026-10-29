# F008 第十三阶段：Keyhive 固定版本 Rust 复验可行性与错误传播最小方案

日期：2026-10-29 UTC。目标键：(privacy_safety,F008,phase13,fixed-rust-runtime-feasibility-and-member-read-fail-closed-plan)。本阶段 COMPLETE_BOUNDED_STATIC_FEASIBILITY，F008整体 IN_PROGRESS。承接 phase12 已确认的并发成员读取测试覆盖问题，未重复申报PR #239补丁为新发现。

## 一手固定来源与环境检查

上游固定源码 https://github.com/inkandswitch/keyhive/tree/b93f55bd3a5c274c10497f5cf834f95f3ff86930 ，README、Cargo.toml、rust-toolchain.toml、beekem/src/tests/concurrent_membership_changes.rs 均在本轮直接读取。该固定版本 rust-toolchain.toml 将编译器钉在1.91.0，workspace.package.rust-version为1.90.0。官方README给出无Nix时的宿主测试命令：cargo test --workspace --exclude keyhive_wasm --features test_utils。仓库为多crate Rust workspace，包含测试依赖和Git修订依赖；所读取固定根目录未列出Cargo.lock，依赖完整字节身份及离线可用性尚需另行核实。

本轮执行本地环境探测：which cargo、which rustc 均无可执行文件；Node.js和Python存在。本执行环境不能在零新增安装和不可用外部下载条件下直接完成Rust原生测试。没有执行cargo test、安装编译器、下载依赖、使用GitHub Actions、租用设备或访问真实密钥。源码README将Keyhive标为pre-alpha，明确不推荐生产使用且尚未经安全审计；不能由现有正常路径单测推断生产级授权安全。

## Phase12衔接与新增可执行设计

PR #239 于2026-09-26合并的成员读取路径将member_ids变成可能返回Result的可变读取，并在读取前处理待应用结构变更；上层document.cgka_members应传播错误。上游正常路径已有并发添加、并发删除和待处理添加后撤销等测试。此前限定阅读的两份测试没有直接故障注入replay_ops_graph失败的覆盖，尚不能推断全仓库不存在相关测试。

候选最小验证协议 F008-P13-01，尚未执行：先固定仓库commit、Rust 1.91.0、全部解析依赖身份和测试选择器；构造待重放成员变更，在受控测试替身或最小注入点使重放返回明确错误；断言member_ids与document.cgka_members均返回错误，调用方拒绝授权决策，禁止返回旧成员列表作为成功值；恢复重放后再检查重复读取幂等性和各副本最终成员一致性。负例应包含错误吞没、旧成员缓存被误用、并发撤销后先读再授权、恢复后的重放双应用。必须区分源码可注入性、可编译性、真实测试结果、网络攻击效果与历史明文清除，逐项报告。

候选控制 F008-R13-01：权限成员列表读取失败时进入UNKNOWN且拒绝高风险自动操作。F008-R13-02：保留撤销发生的因果时点、授权版本与离线同步状态。F008-R13-03：历史密钥、已解密缓存和备份分别制定生命周期测试；成员收敛不能替代数据清除证据。全部UNADOPTED，不接入用户真实敏感数据，不开发个人决策产品。

## 证据与阻塞

上游固定README/manifest/源码属于 UPSTREAM_STATIC_SUPPORTED；本地工具缺失属于 LOCAL_ENVIRONMENT_OBSERVED；Rust编译、故障注入、设备同步、历史密钥擦除及外部安全审计均 NOT_RUN。零新增费用原则优先；未来只有在已有设备具备确认免费的本地Rust环境与完整固定依赖时才运行，否则继续静态审查。下一阶段F008 phase14可审查授权读取调用链的错误分支及相关设计文档，避免无效重复。账户实际账单和GitHub免费额度未独立核验。
