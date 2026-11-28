# v0.8 研究资产整合与待接入清单

将当前 v0.8 规格的 26 份固定资产与工作树逐份核对 Git blob。平台工程基线另保留 v0.7 的 61 项历史身份与 154 份检索参考集。主线文献和冻结结论保持原始版本。不同报告的相同语料、算法或情景重复不作为独立证据。候选状态见表，依据与许可边界由原报告及规格维护。 [研发规格](../../../research/decision_hub/2026-11-26-v08-integrated-research-and-acceptance-spec.md) · [历史整合](V07_RESEARCH_INTEGRATION.md)

| 组 | 固定报告 | Git blob | v0.8 使用及接入条件 |
| --- | --- | --- | --- |
| A | [condition-polarity-attachment-candidate-audit](../../../research/decision_hub/2026-11-25-condition-polarity-attachment-candidate-audit.md) | `81df7d2fc56f29084ecc623b98cdf0991d3260d4` | 原文守卫与候选属性接入。有限组合研究和独立评分保持隔离。 |
| A | [external-ud-development-corpus-structural-audit](../../../research/decision_hub/2026-11-25-external-ud-development-corpus-structural-audit.md) | `db9cc100d96d49832fe32879a706f63830301773` | 同一外部中文 UD 开发语料的来源证据。未接入生产；标注及许可用途受限。 |
| A | [nonprojective-dependency-decoder-external-diagnostic](../../../research/decision_hub/2026-11-25-nonprojective-dependency-decoder-external-diagnostic.md) | `0218ff41ee8fd68e5df1b2886cdfbee3368c8426` | 依赖人工分词、词性等标注的解码诊断。未接入生产。 |
| A | [projective-dependency-decoder-external-diagnostic](../../../research/decision_hub/2026-11-25-projective-dependency-decoder-external-diagnostic.md) | `c40a09357a858644a0da922097cd6367ca696df6` | 与非投射诊断共用语料与标注输入。未接入生产。 |
| A | [source-bound-relation-support-projection](../../../research/decision_hub/2026-11-25-source-bound-relation-support-projection.md) | `dff5ab32d4ea2698256f725f1ae3726578e4a015` | 原文关系锚和作用域支持接入候选；与 R132/R93 去重。 |
| A | [ud-negation-head-candidate-diagnostic](../../../research/decision_hub/2026-11-25-ud-negation-head-candidate-diagnostic.md) | `d81cbedafee148a0c1e065f39254bac7abe6e14d` | 已知否定词元的依附诊断。保留外部开发用途，未接入生产。 |
| A | [unicode-grounded-language-candidate-bridge](../../../research/decision_hub/2026-11-25-unicode-grounded-language-candidate-bridge.md) | `e5c32f5fa91e79a33c06e5b95be491207c6a526d` | UTF-8 摘要和 Unicode 标量半开坐标接入宿主及客户端协议。 |
| B | [joint-guarded-policy-applicability](../../../research/decision_hub/2026-11-25-joint-guarded-policy-applicability.md) | `5fed5e9108fbc97257fbf0546d521aa3cf725769` | 共享守卫身份接入候选。联合适用性需要可信完整支持，求解器保持研究用途。 |
| B | [correlated-interpretation-question-separation](../../../research/decision_hub/2026-11-25-correlated-interpretation-question-separation.md) | `2ef743e0ea767dcc3ba551eff819eae71b1e2df7` | 与 R93 同一主要算法。原研究归档，不重复计为新能力。 |
| B | [adaptive-clarification-port-guarantees](../../../research/decision_hub/2026-11-25-adaptive-clarification-port-guarantees.md) | `9178ff491047925e17f88fb1ab82f843bd254285` | 有限自适应问询前沿保留研究。产品使用既有明确问题和单次优先追问。 |
| B | [shared-information-source-cost-frontier](../../../research/decision_hub/2026-11-25-shared-information-source-cost-frontier.md) | `bd639403c82166ee5ed98c94f09289f601209b92` | 共享来源获取成本与响应保证保持研究用途，未自动购买或获取数据。 |
| C | [v07-dismissed-claim-reproposal-audit](../../../research/decision_hub/2026-11-25-v07-dismissed-claim-reproposal-audit.md) | `95616e3d1c316a7f56f49fc81f07e51e16e6d13d` | 原生会话允许略过后重新提交，必须重新确认。 |
| C | [v07-knowledge-qualification-shared-parameter-bridge](../../../research/decision_hub/2026-11-25-v07-knowledge-qualification-shared-parameter-bridge.md) | `df5a962a58ba0601b6014fad47c39cd3ebdb0e33` | 本地知识重校验与公开参数资格适配器已测试。公开参数未自动进入生产。 |
| C | [v07-partial-result-authority-boundary](../../../research/decision_hub/2026-11-25-v07-partial-result-authority-boundary.md) | `2214aaf19b8fcf4dc8a5a3b9995e59b9ff3dfacf` | v8 局部计算端口与完整选择、计划、保存资格隔离。 |
| C | [v07-scenario-score-basis-regret-integration-audit](../../../research/decision_hub/2026-11-25-v07-scenario-score-basis-regret-integration-audit.md) | `57ba5834bae5ab139525e46d4afc4a6d0414f697` | 评分绑定原评价口径。同口径保留来源，口径变更前的分数需重新核对。 |
| C | [v07-semantic-projection-boundary-batch](../../../research/decision_hub/2026-11-25-v07-semantic-projection-boundary-batch.md) | `5442d4bbeb465bbd11d5901e150a5887263e61ca` | 严格比较、角色修订和测量优先级的部分修复接入，完整联合作用域仍未知。 |
| C | [v07-session-incarnation-reuse-audit](../../../research/decision_hub/2026-11-25-v07-session-incarnation-reuse-audit.md) | `03871df4f98e6670fa7fe0d1e4cd85b0ee7240b4` | v8 实例与修订绑定，v6/v7 一次性兼容标识，过期和迟到发布防护。 |
| D | [conditional-model-alternative-coverage](../../../research/decision_hub/2026-11-25-conditional-model-alternative-coverage.md) | `8fa6c050fd71d60823e4dc99d4f4f7310b579a0d` | 与两路联合计算配套的隔离竞争模型覆盖，正式调度未启用。 |
| D | [resumable-budgeted-world-join](../../../research/decision_hub/2026-11-25-resumable-budgeted-world-join.md) | `d4a85f1e92744d1179f76a47cf56926d17b18cf3` | 有限预算、签名续算与前缀计算隔离复算。未开放持久化续算。 |
| D | [world-bound-multistage-result-join](../../../research/decision_hub/2026-11-25-world-bound-multistage-result-join.md) | `af4daae1aaeee5a36a140d8a0f272a48c064368b` | 同一联合世界连接、缺失保留以及并发前置检查模型隔离复算。 |
| E | [cross-decision-obligation-union](../../../research/decision_hub/2026-11-25-cross-decision-obligation-union.md) | `19fa2b270056d448bd93b587049198d284c5eecf` | 原生共同现金义务按经核对的身份去重。未自动拼接已保存的不同记录。 |
| E | [joint-goal-deadline-extension-frontier](../../../research/decision_hub/2026-11-25-joint-goal-deadline-extension-frontier.md) | `6587769d44804abed17808e7986368178455fbdf` | G06 两个单工作槽目标的软期限分歧候选，运行输出保持无选择权。 |
| E | [ledger-to-budgeted-threshold-integration](../../../research/decision_hub/2026-11-25-ledger-to-budgeted-threshold-integration.md) | `cf792bd6aba79bc3edd2d9329084362604c4c63a` | 原研究代码可复算，账本到预算续算的完整调度仍隔离。发布了分开的账本和候选端口。 |
| E | [recurring-benefit-feasibility-threshold](../../../research/decision_hub/2026-11-25-recurring-benefit-feasibility-threshold.md) | `9c27c104e3be8f18eebc18f5ad8a0e10e2940fcf` | G06 已提供持续收益门槛及可复算日期见证，保持未准入。 |
| F | [bounded-residual-correction-gate](../../../research/decision_hub/2026-11-25-bounded-residual-correction-gate.md) | `0b4a892b4daf7c1b887dc93ca672797068d3da63` | 冻结合成/公开开发数据并对照误差与低估的隔离评价。生产参数无写回。 |
| F | [scope-qualified-residual-transfer](../../../research/decision_hub/2026-11-25-scope-qualified-residual-transfer.md) | `78baa41869cc982f067f36fe0e7de1e0702dd06f` | 跨范围收缩仅有隔离评价接口和有范围条件的实验，未使用个人观测或独立留出。 |

D 组三份报告的固定 Node 代码实际复算，得到 235,298 个竞争组合、24,480 个联合域以及相同联合域中的 79,168 个续算前缀。Python 独立枚举核对 1,024 个联合夹具及 225 个模型竞争夹具。E/F 六份原研究代码按依赖 blob 核验并重放，核对 3,456 组义务并集、3,888 组期限、5,184 组收益门槛、16,384 个预算请求、32,768 组残差评价及 40,960 个迁移夹具。另在工程测试中枚举 5,184 组门槛及 3,888 组期限的独立算例。相同研究夹具之间可能重合。所有计数都是理论或工程复算样本，真实使用和独立科学验收由各自条件决定。

未纳入生产的资产还包括 C035、C036、C025 训练或生产更新、R258 等历史隔离候选、复杂连续排程、外部句法标注和旧第三方 AI 适配器。接入前分别需要来源许可和用途核验、原始可验证输入、原生边界和反例回放、独立评价及明确采纳。 `timing_actions` 的历史来源状态仍待独立审查。既有结果保留原证据身份。 [隔离候选登记](../src/psychohistory/decision_candidates.py) · [联合计算与资源限制](V08_COMPOSITION.md)

开发期间主线新增的活动方法版本与精度报告已保留。候选吸收单一活动版本、精确来源及依赖匹配，提供真实宿主的切换回退试验。正有理单位转换与保守网格外包保持研究用途，现行硬门继续要求可比的明确单位和时域。 [活动清单与保守精度研究](../../../research/decision_hub/2026-11-26-extension-precision-and-active-version-contract.md)

Draft 创建窗口主线又增加有界有理数、共享转换与认证收据研究。该报告的公开 Node 核心重放得到 521 个规范量、32 个无效量、972 个算术配置与 5,040 个资格夹具。共享转换的 972 组预算配置中，共享完成 403 组，重复计算完成 377 组。完整研究包及其认证原型未在本候选复算；生产继续使用现有精确小数和隔离候选合同。 [有界数值与共享参数研究](../../../research/decision_hub/2026-11-26-bounded-numeric-wire-shared-parameter-receipts.md)
