# F008 第十五阶段：Keyhive生产组撤销传播中的错误吞并边界

日期：2026-10-29 UTC。目标键：(privacy_safety,F008,phase15,group-revoke-cgka-error-suppression)。状态 COMPLETE_BOUNDED_STATIC；F008周专题整体IN_PROGRESS。固定上游inkandswitch/keyhive提交8c2ceb8c926496fb2a0a1e1cf0069686d4ca0200（2026-09-26已合并PR #239对应版本）。本轮只读上游Rust源码与既有测试；未安装Rust/Cargo、未运行真实故障注入、未访问身份私钥或用户敏感数据。

## 生产路径的新增静态发现

在keyhive_core/src/keyhive.rs，Git blob 2408054e857ff49210b7627e89b9bb2bf2948b4a，约540至670行，公开生产方法`Keyhive::revoke_member`首先调用resource.revoke_member(...).await?。若资源是Group，它随后遍历包含该组的文档，计算已撤销成员且不再经其他路径可达的个人ID，尝试从各文档的CGKA树移除这些ID。关键分支：

```rust
if let Ok(Some(op)) = locked_doc.remove_cgka_member(id, &signer).await {
    update.cgka_ops.push(op);
}
```

当remove_cgka_member返回Err时，此分支直接跳过该错误；在该循环之后方法仍可发送已有cgka_ops并返回Ok(update)。这说明调用者无法仅从此方法成功返回推断每一个下游文档的CGKA移除操作都成功。需要在特定可达图和失败条件下做原生复验，才能确定实际状态差异及可利用性。

对照keyhive_core/src/principal/document.rs，Git blob 355c3f1a695e6b33bf989a1c3e1942670d51680a，约335至386行，文档直接撤销路径`self.cgka_mut()?.remove(id, signer).await?`会向上传播错误；`remove_cgka_member`本身返回Result<Option<...>, CgkaError>。两种路径错误处理策略确有差异。该差异尚不足以证明生产加密或授权可被绕过，因为上游资源撤销与后续加密权限存在不同状态层，且错误发生的实际可达性仍未验证。

另见keyhive_core/src/keyhive.rs约765至779行的公开`try_pcs_key_hash`：`cgka_mut().ok().and_then(|cgka| cgka.try_pcs_key_hash().ok())`将若干内部错误折叠成None。该接口返回Option用于PCS密钥哈希可见性，当前没有证据表明它直接决定授权；仅登记诊断粒度和调用方解释风险。第十四阶段`cgka_members_for`错误折叠只存在test_utils路径，本轮确认生产组撤销循环是一个独立的新问题。

## 测试范围和反例边界

读取keyhive_core/tests/membership.rs（Git blob 3981945fc79800e5f1378c867c64cd35afc537b3）、revocation_sync.rs（b62131a7a09087f234755cc725455713e035825e）及transitive_access.rs（9a695f984b6265b748bff642de3bdbd6a0011adf）。这些测试包含正常组撤销、嵌套组成员移除和撤销后读取新密文等情形；本轮在上述限定文件的关键词检查中未发现针对`remove_cgka_member`返回Err后公开`Keyhive::revoke_member`仍成功返回的专门故障注入。不能把有限搜索当成全仓测试缺失证明。

建议未来在确认本地Rust工具链免费可用后，于隔离人工身份和人工文档中固定以下测试：组撤销前后保留成员/不保留成员两种模式；为一个包含该组的文档注入CGKA移除错误；同时检查资源撤销、文档树成员、未来加密内容可读性、错误返回、事件收据及恢复/重试；与文档直接撤销路径的Err传播对照。任何未成功完成的移除应有类型化错误与未完成状态记录，未知状态的权限操作建议拒绝并允许人工复核。此为候选控制，尚未采用到个人决策系统。

## 风险等级和证据

固定版本生产源码静态支持：生产组撤销传播循环存在Err忽略路径，CONFIRMED_STATIC。是否能够在真实有效撤销时触发、是否保留未来密钥、是否构成可利用漏洞均UNCONFIRMED。原生Rust运行时NOT_RUN，安全审计认证NOT_RUN。零新增费用，不启动GitHub Actions或云GPU。下一阶段优先检索上游是否已有修复及相关故障注入测试，再考虑本地可复现的最小人工实验。F008继续IN_PROGRESS，个人真实数据与产品开发仍不接入。
