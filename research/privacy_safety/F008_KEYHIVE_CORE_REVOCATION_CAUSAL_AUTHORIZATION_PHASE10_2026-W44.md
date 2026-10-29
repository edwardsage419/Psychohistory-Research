# F008 第十阶段：Keyhive核心撤销测试与因果时序授权边界

日期：2026-10-29 UTC。目标键：(privacy_safety,F008,phase10,core-revocation-tests-and-causal-authorization)。阶段状态：BOUNDED_UPSTREAM_STATIC_REVIEW_COMPLETE；F008整体IN_PROGRESS。纯公开源码静态审查，未使用真实身份、密钥或个人数据。

## 固定英文一手来源

上游官方核心仓库 `inkandswitch/keyhive` 当前main固定SHA `b93f55bd3a5c274c10497f5cf834f95f3ff86930`。仓库 Apache-2.0 许可证；`rust-toolchain.toml` 指定Rust 1.91.0。上游安全政策明确写明pre-alpha、未经安全审计，不应用于生产数据保护：https://github.com/inkandswitch/keyhive/blob/b93f55bd3a5c274c10497f5cf834f95f3ff86930/SECURITY.md 。

实际读取以下核心测试文件，均为固定SHA：
1. `keyhive_core/tests/access_control.rs`，Git blob `ed37e9098b4f35e7afa9272349998403c8a91677`，约1001行。测试 `a_revoked_member_cannot_read_new_content`：先授权可读旧内容，撤销后验证成员不能解密新内容。
2. `keyhive_core/tests/cgka_authz.rs`，Git blob `9c78b5e19063cfa9733b113c9a4b1a2881f003b1`，约1439行。测试 `a_revoked_writer_adds_no_reader`：检查撤销写权限后的添加成员操作被拒绝。
3. `keyhive_core/tests/revocation_sync.rs`，Git blob `638eebbd507a39d6edc8028e53d4fe22932d19b1`，约166行。包含撤销后密钥事件同步的具体测试，语义需结合完整协议解释。

核心测试目录共23份Rust文件，其中上述三份有明确撤销相关测试。F008第九阶段发现的是包装层 `automerge/automerge-repo-keyhive` 限定8份测试中未检出直接撤销测试，不能据此推断核心依赖没有撤销测试。本阶段补足这一分层证据边界。

上游PR #236 `Properly account for revocations when determining which ops to sync to an agent` 于2026-09-26合并，merge SHA `35cded2089ab95822526cf47e1e386f54c12770e`。PR #238 `Prevent individuals never added to a document from adding themselves (or Public) to the CGKA tree` 于2026-09-28合并，merge SHA `0451b8ff17b54670fbc72aae26955909cbc4364d`。两份PR的状态均通过官方GitHub REST重新核验为merged=true。

特别注意PR #238作者说明：该补丁只检查主体是否曾获文档访问权限，尚未完全检查在相应CGKA操作因果历史时点是否拥有合法权限；作者明确保留了曾获授权者撤销后仍可能进入树的剩余风险。该说明来自PR正文，属于UPSTREAM_ACKNOWLEDGED_LIMITATION；本轮没有运行可复现攻击、没有证明当前main一定可被利用，也没有独立安全审计。不能将“已合并防护”直接升级为“撤销安全已解决”。

来源：
https://github.com/inkandswitch/keyhive/pull/236
https://github.com/inkandswitch/keyhive/pull/238
https://github.com/inkandswitch/keyhive/blob/b93f55bd3a5c274c10497f5cf834f95f3ff86930/keyhive_core/tests/access_control.rs
https://github.com/inkandswitch/keyhive/blob/b93f55bd3a5c274c10497f5cf834f95f3ff86930/keyhive_core/tests/cgka_authz.rs

## 候选安全控制和风险登记

F008-R10-01：授权必须同时绑定身份、权限、文档、操作发生的因果时点及撤销版本。仅检查历史上曾授权不足以证明当前操作合法。候选原则为默认拒绝及可审计的因果授权证明。

F008-R10-02：包装层API、核心权限引擎、同步传输、密钥轮换、缓存、历史副本各有独立验收边界。核心测试存在不等于包装层端到端通过。明确记录“撤销后新内容不可读”和“历史已取得明文无法强制远程抹除”的差别。

F008-R10-03：版本化保留失败测试，针对并发授权、撤销与重授、离线重联、直接及群组权限交叉，分别保留允许与拒绝收据。测试只能使用虚构身份和人工数据。

F008-R10-04：本地可复验前置为固定commit、Rust 1.91.0、已缓存的合法依赖、零新增费用确认和无真实敏感信息。当前没有下载或安装依赖，没有运行cargo test、没有证明任何端到端安全性质。无法确认免费资源则继续静态审查。

以上均为UNADOPTED候选安全知识储备，个人决策产品开发仍暂停。

## 证据与后续

本轮新增为固定上游源码、测试和已合并PR说明的静态证据。与第九阶段包装层审查互补。无新E2真人、E3历史或外部独立安全认证。没有接入真实个人数据、没有触发CI、没有新付费服务。

下一阶段优先在固定核心版本检索作者公开的因果时序测试与尚未解决的PR/issue，再决定是否具备完全本地、零费用的人工身份测试环境。不得把官方已合并PR描述替代真实运行结果。
