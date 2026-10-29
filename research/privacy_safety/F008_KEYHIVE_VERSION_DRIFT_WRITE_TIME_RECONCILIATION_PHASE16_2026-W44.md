# F008 第十六阶段：Keyhive版本漂移与写入时撤销核对

日期：2026-10-29 UTC。目标键：(privacy_safety,F008,phase16,upstream-version-drift-write-time-reconciliation)。阶段状态COMPLETE_BOUNDED_STATIC；F008周专题总体IN_PROGRESS。只读官方GitHub源码，不接触个人身份、真实密钥、设备数据或收费服务。

## 上游固定版本差异

此前F008第十五阶段固定inkandswitch/keyhive提交8c2ceb8c926496fb2a0a1e1cf0069686d4ca0200（2026-09-26）。本轮重新读取官方仓库，2026-10-29T16:02:31Z最新main提交5223ba1b436bd4f5b4f8b13613b4478391844274，标题Make Cgka generic over its membership view (#307)。Git compare显示新版本相对旧固定提交ahead=69、behind=0。生产源码 `keyhive_core/src/keyhive.rs` 的Git blob由2408054e857ff49210b7627e89b9bb2bf2948b4a变为64479c7a3d22a7ee97161b71564055c5a23aa7ac。

旧版本生产 `Keyhive::revoke_member` 在组成员撤销后遍历关联文档，使用 `if let Ok(Some(op)) = locked_doc.remove_cgka_member(...).await`，遇到Err会跳过该移除并仍可能返回Ok。第十五阶段的结论仅适用于旧固定版本。

新版本同一文件中已无 `if let Ok(Some(op))` 这一分支，`revoke_member` 改用Keyline delegations与权限检查，关联CGKA同步转到证书驱动的写入准备路径。不能把旧代码位置的缺失等同于全部安全风险已修复，也不能将旧版本静态风险直接描述为新版本同一接口仍存在。

## 新版写入时防护的静态证据

在新版本 `reconcile_before_writing` 中，`issue_implied_cgka_ops` 出错通过 `map_err(...)?` 传播；返回 `ImpliedCgkaOpsOutcome::RemoveBlocked` 时明确产生 `Err(EncryptError::CgkaMemberLacksRead)`。 `prepare_to_write` 先执行该核对，失败则释放写入锁并返回错误。公开 `try_encrypt_content` 调用 `try_encrypt_content_keyed`，后者在加密前调用 `prepare_to_write(doc).await?`。这形成可静态追踪的写入前拒绝路径，属于新版本候选防护证据。

另外，`cgka_from_ops` 对部分历史操作重放失败会记录警告并推迟重放，不能由此推断所有缓存、离线副本和历史明文都已同步撤销。新版本可能仍存在其他错误、并发和重放边界，需原生Rust测试和可重复故障注入后才可确认。代码搜索在默认分支未发现专门以 `CgkaMemberLacksRead` 为字面量的测试结果，这只是关键词范围观察，不是全仓覆盖缺失证明。

固定来源：
旧源码 https://github.com/inkandswitch/keyhive/blob/8c2ceb8c926496fb2a0a1e1cf0069686d4ca0200/keyhive_core/src/keyhive.rs
新源码 https://github.com/inkandswitch/keyhive/blob/5223ba1b436bd4f5b4f8b13613b4478391844274/keyhive_core/src/keyhive.rs
新提交 https://github.com/inkandswitch/keyhive/commit/5223ba1b436bd4f5b4f8b13613b4478391844274

## 候选安全控制与风险登记

控制一：每次撤销操作生成明确的资源、授权版本、密钥同步状态与完成收据。仅凭授权撤销API返回成功不足以宣称所有后续密文均安全。

控制二：写入前对授权证书和密钥树进行一致性核对。移除失败、状态未知或同步未完成时拒绝敏感写入，并保留可恢复错误码及人工复核路径。

控制三：对离线设备、旧密钥、缓存和备份单独制定生命周期与可见性说明，明确撤销对历史数据和未来数据的不同效力。

控制四：测试必须固定上游commit、Rust工具链和人工权限图，比较旧版与新版的直接文档撤销、嵌套群组撤销、错误注入及写入前状态重建，检查失败是否安全传播。不能把静态源码检查称为运行时安全审计。

## 证据与下一步

旧版错误忽略分支CONFIRMED_STATIC_OLD_VERSION；新版写入前拒绝路径CONFIRMED_STATIC_NEW_VERSION；实际故障可达性、加密安全、离线缓存撤销、全部调用路径及独立安全审计均UNVERIFIED。原生Rust NOT_RUN；新真人E2=0，独立E3=0。当前环境未确认可用免费Rust工具链，本轮不安装收费依赖、不触发GitHub Actions。

下一阶段F008第十七阶段：在新版固定提交中检索直接覆盖RemoveBlocked与群组撤销的现有测试、确认是否能在零费用本地工具链中执行最小人工故障注入。若无法执行，继续文档审查并保留OPEN，不擅自升级安全结论。个人决策产品继续暂缓。
