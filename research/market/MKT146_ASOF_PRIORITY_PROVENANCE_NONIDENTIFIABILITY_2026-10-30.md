# MKT146 历史来源优先级与聚合快照不可识别性

日期：2026-10-30 UTC。目标键：(market,HealthConnect,MKT146-v1,asof-priority-version-and-aggregate-nonidentifiability)。本轮初始main HEAD：5cc5060c169078fb055a38e2b09943502e6df0b7。状态：COMPLETE_BOUNDED_OFFICIAL_DOC_AND_ARTIFICIAL_E1。与MKT145互补：MKT145比较同一完整原始数据下两种优先级，本轮检验仅保留当前聚合总量时历史结果能否重建。

## 官方英文技术文档

Android Developers, Read aggregated data，https://developer.android.com/health-and-fitness/health-connect/aggregate-data ，本轮2026-10-30查阅。官方说明用户可以调整Activity和Sleep的应用来源优先级，聚合API对这两类重叠数据按用户优先级去重，数据总量随设置实时更新；其他数据类型按各自聚合语义处理。可按DataOrigin过滤来源；历史读取受权限窗口约束，卸载重装后原授权撤销并需重新授予。Android Developers, Synchronize data，https://developer.android.com/health-and-fitness/health-connect/sync-data ，说明变化令牌、更新及删除事件的拉取方法。

已审官方页面没有给出“任意历史日期的用户优先级版本可由第三方应用可靠重放”的明确接口保证。该点标记NOT_DOCUMENTED_IN_REVIEWED_PAGES，不能推断平台绝无此能力。实际Android API、设备权限、优先级历史接口和产品效果均NOT_TESTED。

## 机制矩阵

真实可能输入：来源应用、时间区间、数值、用户优先级、授权范围、查询时点。状态表达：snapshot_id、priority_version、data_version、时间窗口、permission_complete。算法：官方平台按用户优先级处理Activity/Sleep重叠；本轮人工程序以每分钟来源优先规则演示，绝不声称等于Health Connect内部实现。目标：避免重复计算并保留历史可解释性。反馈与自我修正：用户修改来源优先级或应用修改历史记录后，需保留旧快照及新规则以解释差异。隐私权限：健康数据需明确授权，跨来源身份关联可能暴露行为模式。解释性：展示数据来源、聚合时点、规则版本和缺失权限。费用模式：本轮仅公开免费文档及现有运行环境V8，未注册、购买或使用收费API；未来实际部署成本未评估。局限：官方功能说明不能证明改善长期人生决策的科学效度。

## 可复算人工E1反例

归档源码：research/market/mkt146_asof_priority_provenance_nonidentifiability_20261030.js，远端Git blob b02a1352bc8cd1b4b26707f09ca64c03b0c25ff2。该程序在隔离V8实际执行20项断言和异常输入拒绝，远端读取原源码后再次执行20项通过。原生Node命令行NOT_RUN。

构造两个20分钟人工世界。两世界的B来源前10分钟均为每分钟80步，A来源后10分钟均为每分钟50步。前10分钟A来源在世界1为每分钟100步，在世界2为每分钟200步。逐分钟仅选优先来源，非重叠时保留唯一来源。

| 人工世界 | B优先的当前聚合 | A优先的历史聚合 |
| --- | ---: | ---: |
| 世界1 | 1300步 | 1500步 |
| 世界2 | 1300步 | 2500步 |

两个世界的当前B优先聚合完全相同，但历史A优先聚合相差1000步。仅保留1300这个当前总量，无法唯一反推出历史A优先结果。若保留世界1全部来源数据且仅优先级未知，限定两种规则下可行值为1300或1500；世界2则为1300或2500。若来源完整性也未知，不能继续声称上述界有效。

人工asOf检查器在snapshot_id、priority_version、data_version、权限完整性或时间窗口不完整时返回ABSTAIN。它仅验证元数据存在及人工约束，不认证元数据真实性、签名、数据来源身份或平台实际权限。人工输入均虚构，无个人健康数据。

## 证据及下一项

MARKET_OFFICIAL_DOC：平台当前聚合与来源优先级机制，已核对英文官方文档。ARTIFICIAL_E1：20项可执行检查，远端V8复算通过。INFERENCE：单一当前总量无法在缺失历史规则及来源数据时唯一重建旧聚合。独立产品效果实验0，真实设备0，E2真人样本外预测0，E3历史预测0，外部独立团队0。没有把营销表述计作科学证据。

候选未来控制：在生成预测或评估快照时存储来源数据版本、优先级规则版本、时间窗口及权限完整性；缺失时拒绝给出确定历史归因。下一MKT147：对来源数据版本与优先级版本分别缺失的情形设计最小审计收据，检查是否可在不保留原始敏感数据的条件下解释历史变化。此项仅为知识储备，R系列完成前不实施个人决策产品。

本轮新增费用0；未触发Actions；账户实际账单与免费额度NOT_VERIFIED。R073及PESEN v0.1冻结，主线先完整R系列，再分类，最后熔炼。
