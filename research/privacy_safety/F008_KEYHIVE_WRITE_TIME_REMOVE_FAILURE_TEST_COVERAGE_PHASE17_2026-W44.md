# F008 第十七阶段：Keyhive 写入时撤销失败的测试覆盖与零费用复验门

日期：2026-10-30（UTC+08）。目标键：(privacy_safety,F008,phase17,write-time-remove-failure-test-coverage)。状态：COMPLETE_PHASE17_STATIC; F008 overall IN_PROGRESS。接续phase16固定版本差异，未触及真实用户资料、密钥或个人决策产品。

## 固定上游版本与新增静态证据

基线固定提交 inkandswitch/keyhive 5223ba1b436bd4f5b4f8b13613b4478391844274。最新上游 HEAD 930c4290b92940d7b716a2a18ecc46eb56308069，比固定版本领先1个提交。Git compare表明新增修改仅在 keyhive_core/src/keyhive.rs 的 relay/unjoined CGKA统计和 keyhive_core/tests/relay.rs 的计数测试，未看到本轮关注的撤销写入门发生改变。上游链接：https://github.com/inkandswitch/keyhive/compare/5223ba1b436bd4f5b4f8b13613b4478391844274...930c4290b92940d7b716a2a18ecc46eb56308069 。

固定版本 keyhive_core/src/keyhive.rs 约第620至760行：reconcile_before_writing 调用 issue_implied_cgka_ops，返回 RemoveBlocked 时显式 Err(EncryptError::CgkaMemberLacksRead)，底层查询失败映射到 PrepareToWrite；prepare_to_write 在错误时 finish_write 后返回 Err，理论上阻断本次敏感写入。该证据是静态调用路径及源码意图，尚未运行故障注入。源码：https://github.com/inkandswitch/keyhive/blob/5223ba1b436bd4f5b4f8b13613b4478391844274/keyhive_core/src/keyhive.rs 。

本轮实际读取固定版本以下测试并逐项审查相关用例：
1. keyhive_core/tests/cgka_authz.rs 约1111行 a_reader_whose_remove_failed_to_sign_is_removed_at_the_next_write：人工 RationedSigner 允许撤销证书签名但拒绝紧接的成员移除签名，测试先证实成员仍在 CGKA 树，随后恢复签名并成功写入，最终证实旧成员移除。这覆盖了失败后恢复路径；没有保持签名失败时尝试写入并断言明确 Err 的步骤。
2. 同文件约743行 a_revoked_writer_adds_no_reader：验证已撤销写入者没有继续添加新读者；约945行 an_authorized_op_the_cgka_refuses_reports_the_cgka_error：验证 CGKA InvalidOperation 错误向上返回。
3. beekem/src/tests/implicit_removes_protocol.rs 约125行 a_replay_lacking_a_membership_answer_doesnt_make_changes_until_answered：在成员查询信息缺失时返回 MembershipUnknown，树保持不变，恢复查询后移除成员。
4. keyhive_core/tests/revocation_sync.rs 验证撤销密钥传播范围；keyhive_core/tests/groups.rs 检查群组撤销授权边界。这些用例与写入前故障注入互补。

因此 phase16 的“新版有写入前安全门”已有多条现存测试间接支持；本轮限定检查范围尚未看到直接保持 RemoveBlocked 状态调用 try_encrypt_content 并断言 CgkaMemberLacksRead 且无新密文、无旧密钥继续使用的端到端测试。该发现仅为特定文件/特定故障路径覆盖缺口，不能据此声称所有上游测试缺失、生产漏洞存在或加密安全已认证。

## 零费用候选故障注入协议

候选用例A：构造已被Keyline撤销、CGKA尚未成功移除的成员；强制 remove 签名持续失败；尝试 try_encrypt_content，要求返回明确错误、不得产出新密文、旧成员不可取得撤销后新密钥。候选用例B：恢复签名后再次写入，要求 CGKA 移除完成且新密文对旧成员不可读。候选用例C：使 Keyline 成员查询失败，要求 PrepareToWrite 失败、状态可诊断、重试无越权写入。每项固定完整权限图、上游SHA、工具链版本、错误类型、发出CGKA操作和密文数量。若未满足可观测性，结果保持 UNKNOWN，不臆造 PASS。

当前本地执行环境检查 command -v cargo / rustc 均为空，Node存在；因此原生 Rust 测试 NOT_RUN。没有安装工具链、下载编译依赖、调用收费API、使用GitHub Actions或处理真实敏感信息。今后仅在确认现有免费工具链及所有依赖不会计费后开展本地人工测试；否则继续静态审查和待办登记。

## 证据边界与后续

本轮源码与上游测试为固定Git blob支持的 STATIC_CODE_AND_TEST_EXPECTATIONS，运行时故障可达性、离线设备旧密钥、缓存清除、完整权限撤销及第三方审计均 UNVERIFIED。未来个人决策系统候选控制：撤销后敏感写入采用 fail-closed，记录错误和密钥轮换收据，区分历史明文与未来密文访问，允许人工停用及申诉。不得把厂商安全承诺替代验证。F008本周专题已持续推进，本阶段新增具体故障注入门；新增E2=0，E3=0。

下一项 phase18：检查 Keyhive 在离线重连和并发密钥树更新时的写入失败回滚与密文可见性，继续只读审查，零新增费用。
