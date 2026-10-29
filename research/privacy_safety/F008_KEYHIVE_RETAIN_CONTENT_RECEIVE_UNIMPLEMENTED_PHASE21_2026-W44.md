# F008 第21阶段：Keyhive撤销水位与内容接收执行边界

日期：2026-10-30 Asia/Singapore；2026-W44。目标键：(privacy_safety,F008,phase21,retain-watermark-content-receive-enforcement-gap)。阶段状态COMPLETE_PHASE21_STATIC，F008整体IN_PROGRESS。只读公开源码和官方设计，零敏感个人数据。

## 1. 固定来源与本轮新增确认

固定上游 inkandswitch/keyhive main HEAD 930c4290b92940d7b716a2a18ecc46eb56308069，未把设计文档当成已完成安全实现。实际读取：
* design/threat_model.md blob 863e2f4220ff5d404668e788317dc7d7bf62c2a1；
* design/convergent_capabilities.md blob bf11b5b0074b416af68b201d8682ade7f8bcfdc0；
* keyhive_wasm/src/js/revocation.rs blob 105337aaa786cbf301979ff29abf83cf000d3de1；
* keyhive_wasm/e2e/keyhive.spec.ts，及 keyhive_content/src/lib.rs blob d65a62cf68f5dc7ba58658f74b26fcf8377caa06、store.rs（限定静态范围）。

上轮F008 phase20已证明core在撤销时读取应用设置的content heads并签署retain，WASM接口可以读出retained(doc)，已有正例测试。**本轮新证据为上游威胁模型的明确Open Questions声明：当前没有内容层读取retain并执行T5检查。** 设计T5要求应用保持heads最新，内容层根据撤销签署的因果水位拒绝被撤销成员的越界操作；威胁模型明确Keyhive自身不签名或跟踪应用CRDT内容。故证书包含retain、WASM可读取retain、应用实际拒绝后撤销编辑，属于三个独立的安全关口。前两者的存在不能证明第三者已实现。该项目官方明确pre-alpha且未经安全审计。

此外威胁模型Known Gaps明确列出G1：已撤销成员可尝试以新密钥重新入树；G4：来自其他副本的证书变更不会自动触发本地树协调。这里是上游已披露的实现限制，不能称为本轮独立发现的新漏洞。代码静态审查范围未运行Rust/WASM/Playwright，未验证可利用性和生产环境影响。

## 2. 未来候选故障注入及拒绝策略

若未来实施个人决策数据协作，先使用完全人工的本地CRDT样例：创建合法h0，记录应用setContentHeads，签署撤销；构造被撤销身份声称为h0之后的h1，验证接收方在内容落库前明确拒绝；构造真正先于h0的延迟操作，单独测试其因果许可及完整性；若retain缺失、heads过期或无法确认作者身份，敏感数据自动传播应弃权并隔离待审。测试还需分别验证密钥树重新协调、旧设备重连、跨设备缓存和用户删除意愿。

不得用本机墙上时钟代替可信历史顺序；上游T5承认真实旧操作迟到与伪造倒填无法仅凭因果图可靠区分。候选控制为权限版本、撤销证书哈希、内容head证明、接收决策与申诉日志分别保存，避免把授权撤销误当已删除旧副本。未来是否采用Keyhive仍需审计，不应作为默认已安全组件。

## 3. 证据等级与后续

固定上游原始英文源码/威胁模型直接支持设计与当前声明；静态核查，不代表独立漏洞复现。真实运行时测试、完整源码覆盖审计、第三方安全审计均NOT_RUN。新增真人E2=0、历史E3=0。无个人账户、密钥、健康或财务数据、无付费服务或CI。

固定上游：
https://github.com/inkandswitch/keyhive/blob/930c4290b92940d7b716a2a18ecc46eb56308069/design/threat_model.md
https://github.com/inkandswitch/keyhive/blob/930c4290b92940d7b716a2a18ecc46eb56308069/design/convergent_capabilities.md
https://github.com/inkandswitch/keyhive/blob/930c4290b92940d7b716a2a18ecc46eb56308069/keyhive_wasm/src/js/revocation.rs
https://github.com/inkandswitch/keyhive/blob/930c4290b92940d7b716a2a18ecc46eb56308069/keyhive_content/src/lib.rs

下一项F008 phase22：对照已披露G1/G4与当前上游提交状态，调查是否有正式补丁及安全测试；若无变化改做独立最小数据与删除传播专题，避免反复复述旧问题。
