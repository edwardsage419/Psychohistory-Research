# F008 第十九阶段：Keyhive 因果权限、离线回放与倒填操作的不可判定边界

日期：2026-10-30 Asia/Singapore；2026-W44。目标键：(privacy_safety,F008,phase19,causal-not-temporal-revocation-backdating-and-local-first-controls)。阶段状态 COMPLETE_PHASE19_STATIC；F008整体IN_PROGRESS。未来个人决策模型的隐私安全候选研究，不接入用户真实敏感数据，不开发产品。

## 1. 直接读取固定上游版本

固定 inkandswitch/keyhive 提交 930c4290b92940d7b716a2a18ecc46eb56308069。GitHub连接器实际读取并核对Git blob：

* design/convergent_capabilities.md，blob bf11b5b0074b416af68b201d8682ade7f8bcfdc0；
* design/threat_model.md，blob 863e2f4220ff5d404668e788317dc7d7bf62c2a1；
* design/keyline/edge-cases.md，blob e521c95805e8a4c352a227f7bede8761b3c86756；
* design/causal_encryption.md，blob 5848719264a7331957cfe0090b4c10d019ac4a88；
* keyhive_core/tests/concurrent_instances.rs，blob 06e62a4dbaac63b10e4848dadb8d54bbb11ece15；
* keyhive_core/tests/update_predecessor_key_chain.rs，blob 1567f8a535611522032b560d1f1906a877a15dc4。

官方设计文档要求在离线分区中能够签署授权、撤销及操作，并在恢复同步后收敛。撤销证书和历史操作保留，以支持因果历史。设计文档明确局限：`Causal, not temporal`，一个真正早先发生但延迟到达的操作，可能无法与撤销者事后伪造为旧操作的行为区分。threat_model.md T5明确指出，撤销时可以记录当时已知的内容heads作为因果界标，内容层需要自己保持heads最新并进行拒绝判断；Keyhive本身不签署或追踪应用内容。应用若要求真实时间先后证明，需要另行引入时间戳或锚定机制。

这与F008 phase18所审查的两个分离测试形成新的边界：一项测试证明分区期间合法写入可合并，另一项证明并发撤销在已知事件集合下收敛；它们不能共同证明真实时间上的撤销后写入必被拒绝。该局限由上游设计文档直接承认，因此不是本轮推断出的已验证漏洞。设计文档还记录了若干开放威胁与候选修复，可能滞后于生产源码，不可将文档所有G项直接认定为当前仍可利用的漏洞。

## 2. 三类需要分开的安全判断

A. 签名和因果前驱是否有效：可以根据本地已知证书、heads、签名和密钥树进行检查。

B. 某个操作在现实时间是否发生于撤销之前：当分区节点既可能诚实延迟，也可能故意倒填时，缺少独立可信时间证据无法仅凭本地因果图确定。

C. 撤销后是否继续泄漏未来敏感数据：需要另行检查密钥轮换、离线旧密钥、应用层权限及缓存，不能从成员列表收敛或B的答案推导。

建议未来零新增费用的候选控制：本地记录签名操作ID、前驱heads、授权版本、撤销已知状态、接收时间与用户确认；离线期间的高风险共享写入进入待复核队列；重连时按已知撤销状态重新评价，遇未知或冲突时阻止自动扩大分享范围并提供人工申诉。记录本机时间只能用于审计线索，不能冒充不可伪造的第三方可信时间戳。若某未来用途确需强时间证明，标记依赖未满足并弃权，不得擅自采购收费时间服务。

## 3. 科学与执行边界

上游设计文件为直接文档证据；两份Rust测试为静态代码范围证据。没有实际运行Rust、故障注入、网络分区攻击或密钥撤销实验，安全认证与真实漏洞利用均NOT_VERIFIED。2026-W44 F008专题已覆盖撤销及离线安全，本阶段新增的是官方承认的因果顺序与现实时间无法等同的边界。用户数据0、收费API0、CI0、云GPU0。账户账单与免费额度UNKNOWN。E2/E3均0。

上游链接：
https://github.com/inkandswitch/keyhive/blob/930c4290b92940d7b716a2a18ecc46eb56308069/design/convergent_capabilities.md
https://github.com/inkandswitch/keyhive/blob/930c4290b92940d7b716a2a18ecc46eb56308069/design/threat_model.md
https://github.com/inkandswitch/keyhive/blob/930c4290b92940d7b716a2a18ecc46eb56308069/keyhive_core/tests/concurrent_instances.rs

下一项phase20：只读核对应用内容heads与撤销retain的实际源码调用路径，寻找“heads缺失或落后”的负例测试。若已有测试则记录覆盖范围及版本，不重复声明缺口。原生Rust测试仅在免费现成工具链可用且明确无收费时执行。
