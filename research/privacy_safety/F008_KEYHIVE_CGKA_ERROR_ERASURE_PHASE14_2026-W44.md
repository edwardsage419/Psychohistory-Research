# F008 第十四阶段：Keyhive成员查询错误传播的静态边界

日期：2026-10-29 UTC。目标键：(privacy_safety,F008,phase14,cgka-member-query-error-typing)。状态 COMPLETE_BOUNDED_STATIC；整体F008继续IN_PROGRESS。延续第十三阶段Rust本地工具链缺失，本轮转为固定上游源码调用链静态核验，没有运行Cargo/Rust测试。

## 固定来源和实际已读范围

固定Keyhive已合并PR #239对应提交 8c2ceb8c926496fb2a0a1e1cf0069686d4ca0200，https://github.com/inkandswitch/keyhive/pull/239 ，合并日2026-09-26。逐段读取以下文件：
* beekem/src/cgka.rs，Git blob 5f3756d24850b95f3cfc137bda37e686e89509c9，约375至391行。member_ids(&mut self)先resolve_structural_changes()，后者在有待处理结构变更时replay_ops_graph()?，失败向上返回CgkaError。
* keyhive_core/src/cgka.rs，Git blob b96c47b45e721c4ad7f56417b3a855a253c1641e，184至186行，使用?向上传播。
* keyhive_core/src/principal/document.rs，Git blob 355c3f1a695e6b33bf989a1c3e1942670d51680a，136至145行，cgka_members()使用?传播CgkaError，包括NotInitialized与重建失败。
* keyhive_core/src/keyhive.rs，Git blob 2408054e857ff49210b7627e89b9bb2bf2948b4a，750至765行。标注#[cfg(any(test, feature = "test_utils"))]的cgka_members_for()使用cgka_members().ok().map(...)，把底层CgkaError折叠成Ok(None)；未知文档仍通过?返回NotFound。
* keyhive_core/tests/membership.rs，约947、961、991行，调用该测试辅助方法后使用expect("the document has a tree")。如果出现折叠后的None，这些测试会失败；没有证据表明该路径可静默通过全部测试。

## 新增发现及限制

成员查询的BeeKEM、Cgka包装和Document层都保留重建错误。测试辅助API把未初始化与重建错误折叠为相同的None，降低故障定位能力。由于此辅助API受到test/test_utils编译条件限制，现有证据不足以认定生产授权路径也折叠错误，更不能直接断言已发现可利用漏洞。读取成员列表不等于完成权限授权、密钥失效、历史明文清除或跨设备撤销。上游API文档 https://automerge.org/docs/keyhive/ark-api-guide/ 说明成员操作会抛出异常，但该文档针对ARK JavaScript接口，不能替代上述Rust内部路径测试。

候选安全控制（未采用）：区分NO_TREE、REPLAY_FAILED、NOT_FOUND、REVOKED、AUTHORIZED；权限判定遇错误拒绝操作并保留类型化审计事件；在原生Rust可运行环境注入replay_ops_graph失败并分别核验Document层、测试辅助层和生产调用方；避免将None当成明确撤销或明确安全状态。禁止读取真实身份私钥或用户敏感数据。

证据为固定上游源码静态支持，运行时复验NOT_RUN，实际安全漏洞UNCONFIRMED，新增费用0，账户账单及免费额度NOT_VERIFIED。下一阶段优先查看公开生产接口是否存在同类错误折叠，再判断是否值得进行免费本地Rust复验。
