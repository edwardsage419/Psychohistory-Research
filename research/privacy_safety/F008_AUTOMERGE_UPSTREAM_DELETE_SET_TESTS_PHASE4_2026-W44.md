# F008 第四阶段：Automerge上游实际测试中的并发删除与写入

日期：2026-10-29 UTC。track=privacy_safety；subflow=F；status=PHASE4_SOURCE_TEST_REVIEW_COMPLETE_OVERALL_IN_PROGRESS。target_key=(privacy_safety,F008,phase4,upstream-delete-set-and-conflict-visibility)。observed_head=acf61773c4f172d9c586084e842b33998268b674。本轮没有处理真实敏感数据或执行删除。

## 版本固定的第一手来源与阅读范围

Automerge官方文档 https://automerge.org/docs/reference/under-the-hood/merge-rules/ 描述map和list的并发delete/set以赋值保留为结果。https://automerge.org/docs/reference/documents/conflicts/ 描述同时set的确定性winner与getConflicts可见的其他值。上游代码固定提交5bae7757ef7b92c8cd6850def388f22767305ccb，实际读取两个英文测试源文件：

1. https://github.com/automerge/automerge/blob/5bae7757ef7b92c8cd6850def388f22767305ccb/javascript/test/legacy_tests.ts ，Git blob=1fa526ca21f9a70d1b8da37ec14dfa24a9a8fb01。阅读should handle concurrent assignment and deletion of a map entry、should handle concurrent assignment and deletion of a list element及相邻断言。
2. https://github.com/automerge/automerge/blob/5bae7757ef7b92c8cd6850def388f22767305ccb/rust/automerge-wasm/test/test.mts ，Git blob=6d00f1b0226e74be736a05612694377d4235f2a4。阅读should handle a concurrent map key overwrite and delete及getWithType/getAll断言。

## 新增实证层级与风险

JavaScript上游测试明确断言：共同祖先中bestBird先为robin，一支删除该字段，另一支赋值magpie，合并后bestBird仍为magpie，同时Automerge.getConflicts(s3, bestBird)返回undefined。由此可见，并发删除与赋值可以保留旧来源的新写，且没有可查询的set/set冲突对象。list测试对并发删除与更新同样断言更新后的starling保留，随后save/load仍一致。

Rust WASM测试从共同bird=Greenfinch出发，一支赋值Goldfinch，一支删除，交换增量后两个副本均读取Goldfinch；getAll只列出Goldfinch一项。这是上游测试的具体预期，已读取源代码及断言，未在本轮实际运行该库。

F008新增风险R10：仅检查getConflicts无法发现所有撤销与并发修改冲突。候选控制：权限版本由独立可信授权服务或受保护的本地权限层判断；旧epoch的合并写入在读取、同步与派生使用前再次检查；删除请求另存受保护的撤销事件与确认记录；离线设备、冲突历史、外部副本、密钥和备份分别审计。若完全离线，服务端撤销不能保证即时擦除旧设备上的数据。候选控制均UNADOPTED，不作为Automerge内建保证。

## 证据与费用

证据等级：官方文档和上游固定Git blob源码级测试证据，强于此前自拟状态机的语义假设；本轮库的测试执行、真实双设备同步、丢失设备清除、历史版本物理擦除均NOT_RUN。F008整体IN_PROGRESS；GLOBAL_ERASED=UNVERIFIED。Node环境未预装@automerge/automerge，本轮未下载依赖或注册服务。仅公开免费材料与现有环境，主动新增费用0；实际账单UNKNOWN。下一阶段F008可在确认零成本的现有依赖环境中原样运行上游测试，优先验证getConflicts盲区与撤销事件传播，保持个人产品开发暂停。
