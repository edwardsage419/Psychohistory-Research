# 手动研究资产固定索引与工程映射
2026-11-28。研究整合候选，非正式发布或独立验收。固定main f2febd55946432f739112c70dcbb4aff4cba18bd；开放PR63/62/61/60/59。18项文件实际读取并固定blob，长度为JS字符串长度，非字节数。范围仅近期手动窗口，未完成全库去重及唯一交接核查。
| 文件名（均为2026-11-28前缀及.md后缀） | Git blob | 长度 |
|---|---|---:|
| cross-revision-computation-reuse-publication | d8c272ad337e99afd0159385d9eccb38983a76db | 10118 |
| nonanticipating-plan-option-value | 699a865b5e47b1fc48e4f4802290c2dd469df3c2 | 2624 |
| delayed-resource-release-and-conditional-prefix | 1d1ba755f3166441f6fb5e4920ad9d0696065f7b | 3257 |
| event-order-and-two-stage-information | db220e03153e6e8e47acbd65f52fbcee387865f8 | 2954 |
| correlated-world-resource-complementarity | e48f23cc46fc1cd2644d88098628d00e4b2d2cd4 | 1615 |
| joint-plan-nonconvex-objective-frontier | 05335060ed89558f600ef63933f234dcddeae2b4 | 1894 |
| longitudinal-state-equivalence-compression | 18a0ca78dd3fe21b31e155415a14d7a13a46c3a6 | 2788 |
| budgeted-longitudinal-search-resume | c91ae9c351119f0b1c7f154f9c4b2669fe87b040 | 1958 |
| longitudinal-search-objective-bounds | 4ca2b8af05c31a33041d3b252022f70e7ec79004 | 1779 |
| vector-bound-search-path-witness | f59e2310fb3ed07ea7e21060373412414f2815e6 | 2015 |
| unified-policy-resource-frontier-prototype | 53d564e7a5b8584ea10b0081356459edc326ee05 | 2161 |
| unified-policy-bounded-frontier-resume | 17ad787fbaf9be0ab98090f782ba3d0895730c53 | 2563 |
| correlated-multistage-information-policy-reference | 5983a9e65a718dd3f8a1bbfc6800cf0b22f5e25f | 1864 |
| information-partition-state-compression | b8f1e75b5badecdf1d928ceebb45cbd7e27039d2 | 2204 |
| checkpoint-authentication-scope-replay | 0ab4aa011835b062f7727fb5dbceec4b775e93ea | 1895 |
| search-coverage-optimality-witness | 46f6f62490d44aea03cb9f8532b95a8298da05a4 | 2995 |
| unified-decision-state-contract | a3bec6480cf122fca90755b81cf12004619ad52a | 1770 |
| unified-state-policy-publication-replay | 5d949a602c5b29c4476f796f1d8fadb7c5dbd9dd | 2042 |
## 工程映射及去重
1. decision_resources：延迟到账、事件顺序、任务依赖、相关世界资源互补；以现有账本为唯一权威，禁止重复义务支付。旧固定期限研究作为回归。
2. decision_composition：非预知策略、信息分区、多阶段相关世界、联合前沿；复用CompositionScope及GroupedPort，不另造权威。非预知、两阶段、相关多阶段实验有嵌套范围；统一原型及发布复算也重叠，不累计独立样本。
3. 求解内部：状态等价、标量/向量界、预算续算；先证明状态充分性和界有效，再优化。保留未完成状态，不能以预算耗尽判不可行。节点数量不是设备性能。
4. ConversationHub与存储：跨修订复用、认证及发布。检查点认证已有v0.8合同，本轮为补充负向测试；必须验证原子发布、可信代次、撤回及崩溃恢复。禁止旧结果授权。
5. 验证：可达路径与搜索覆盖分离；标量覆盖和解析参照尚未组合，多目标联合覆盖仍缺。合同真值表与跨修订实验概念重叠，不能证明语义能力。
## 工程准备判定
可复用研究基础已存在，不能视为生产准入。固定PR63候选734686980b19da9291bdd08b67d4e2519c011acf的V08_ENGINE/V08_COMPOSITION是近期已读接口参考，不是已合并基线。正式任务前核实实际PR head、唯一交接、全库去重、语义/证据原生映射、完整联合原型、独立验收规格及环境。非预知报告第一实验缺完整脚本，检查点报告的历史执行记录需重新实际复算；不追认。下一步以独立可运行统一原型和真实持久化故障注入为主，避免继续重复小型参数扫描。无生产修改、训练、合并、部署、主动CI或新增费用。