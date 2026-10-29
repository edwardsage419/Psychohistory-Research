# F008 第20阶段：Keyhive内容heads水位、撤销retain缺省与应用层安全边界

日期：2026-10-30 Asia/Singapore；2026-W44。目标键：(privacy_safety,F008,phase20,content-heads-retain-omission-and-asof-revocation)。阶段状态COMPLETE_PHASE20_STATIC，F008整体IN_PROGRESS。仅公开源码和安全方法储备，无真实用户敏感数据，无产品开发。

## 1. 固定上游源码与真实调用链

固定 inkandswitch/keyhive Git提交930c4290b92940d7b716a2a18ecc46eb56308069，直接读取GitHub文件及Git blob：

* keyhive_core/src/keyhive.rs，blob 55551596c8059efcee300566c6e0f04ee72c7279；
* keyhive_core/src/content/heads.rs，blob f9ffdeb940bf69510a44bb53c8bf9a859d125238；
* keyhive_wasm/src/js/keyhive.rs，blob db80fa29074cbfed830a0c58bdadbf24cfcf2a32；
* keyhive_wasm/src/js/revocation.rs，blob 105337aaa786cbf301979ff29abf83cf000d3de1；
* keyhive_wasm/e2e/keyhive.spec.ts，blob 665f03eeeaa147c2086cd427c2dd654a34a3c978；
* design/threat_model.md，blob 863e2f4220ff5d404668e788317dc7d7bf62c2a1。

实际代码链：应用通过WASM Keyhive.setContentHeads(doc,heads)调用core Keyhive::set_content_heads，更新本地文档状态中的content_heads。撤销Keyhive::revoke_member在签名证书前调用content_watermark(subject)，遍历本地持有文档，依据subject和positive_power筛选，把非空content_heads映射进retain，再逐条调用Revocation::new(...).retaining(retain.clone())签名，最后批量insert_and_reconcile。JS Revocation.retained(doc)只读取证书中的retain条目，返回Option。

源码明确区分两种状态：存在的空水位与retain中根本没有该文档条目。content_watermark遇到空heads会省略文档，注释为“no heads known: say nothing, rather than keep none”。这使应用层不能将revocation.retained(doc)缺省解释成“撤销前已确认没有历史内容”，也不能解释成“该文档没有撤销”。应用未及时setContentHeads时，签名水位可能落后于真实应用内容，Keyhive本身不会追踪或签署应用CRDT内容。这是由代码和设计明确支持的风险边界，不等同于已证实漏洞。

## 2. 现有测试的正例和未证实的覆盖缺口

已存在WASM端到端测试“a revocation retains the heads the application set”（keyhive_wasm/e2e/keyhive.spec.ts约277至310行）：创建文档、设置一个32字节head、授权成员、撤销成员，断言revocation.retained(doc)包含该head，另一个未设置的文档返回undefined。这是静态审查确认的现有正例，不能把“无retain测试”作为新缺口。

本轮在上述固定源码与GitHub代码搜索范围内未找到专门模拟“曾有内容但应用未调用setContentHeads，随后撤销”的负例；也未找到对空heads、过期heads、重连后水位落后等情形进行完整应用内容层拒绝验证的测试。检索范围有限，不能断言整个项目没有相关测试。没有执行Playwright、Rust、WASM或真实离线攻击实验，现有测试源码被阅读，未被本轮运行。

上游威胁模型T5承认：retain记录的是应用最后设置的heads，缺失则跳过；真正旧操作迟到与倒填操作仅凭因果图无法区分。撤销证书是否签名有效、应用内容是否可因果接收、未来密钥是否泄漏是三项不同的判断。

## 3. 未来候选安全控制

在零新增费用的未来设计阶段可考虑：一，记录文档head版本、写入时间与本地最后同步状态；二，高风险分享或撤销前要求应用刷新可验证heads，若未知则拒绝自动扩大共享范围并标记“水位不可证”；三，撤销审计记录signed revocation ID、retain条目是否存在、已知heads及本地状态，区分UNKNOWN与EMPTY；四，离线重连时将待接收内容隔离，逐条按可见授权版本和因果前驱复核；五，对无法判断真实时间顺序的操作显示不确定性和人工申诉路径；六，避免把本机时钟当作可信第三方时间戳。以上仅候选方法，不部署、无默认人生效用权重。

固定上游链接：
https://github.com/inkandswitch/keyhive/blob/930c4290b92940d7b716a2a18ecc46eb56308069/keyhive_core/src/keyhive.rs
https://github.com/inkandswitch/keyhive/blob/930c4290b92940d7b716a2a18ecc46eb56308069/keyhive_core/src/content/heads.rs
https://github.com/inkandswitch/keyhive/blob/930c4290b92940d7b716a2a18ecc46eb56308069/keyhive_wasm/e2e/keyhive.spec.ts
https://github.com/inkandswitch/keyhive/blob/930c4290b92940d7b716a2a18ecc46eb56308069/design/threat_model.md

## 4. 证据、成本及后续

证据等级：上游固定源码与测试文本直接支持，静态范围检查；实际运行时行为、可利用漏洞、独立安全审计NOT_VERIFIED。没有新增真人E2、历史E3或外部安全复现。W44撤销/本地优先专题持续满足每周研究要求，F008总体仍IN_PROGRESS。无账户、无敏感数据、无收费API、无付费工具链或CI。账户账单和GitHub免费额度未独立核验。

下一项F008 phase21：检查Keyhive应用层实际内容接收路径是否使用retain水位判断编辑权限，优先公开示例和测试；若源码未提供该层，登记责任边界，避免重复搜索同一已确认代码。