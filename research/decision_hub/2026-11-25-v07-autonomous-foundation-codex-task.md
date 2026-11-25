# Psychohistory Platform v0.7 自主决策基础平台：完整阶段工程任务
日期 2026-11-25。项目所有者确认：整合现有资源，先交付已具备工程条件的部分，后续随着数据积累提高产品质量。任务定位为一个可独立运行及验收的基础版本候选，继承完整B01–B12目标，不把尚未证实的长期能力冒充完成，不启动训练、PR合并、公开部署或新增费用。本文是一次性工程任务包，不取代产品轨唯一近期交接；不改写历史规程、冻结协议或科研结论。

## 1. 基线及执行方式
- 仓库 edwardsage419/Psychohistory-Research。准备基线 main `5627ea49ee889773c8af1db373b3da0dfdf21f8d`，PR #61 open Draft，head `4c133cd2eed4d5c5f0f164aca1efa2b07cdabf9e`。查询比较为diverged，main领先141、落后5，254项文件列表；main侧platform仅START_SKILL.md列出。正式main为v0.5；#61作者原验收不代表最新候选或独立验收。#59/#60已被#61复用，禁止重复整合或合并。
- 启动时重新检查当前main、PR、AGENTS.md、docs/PROJECT_WORKFLOW_REQUIREMENTS_V3_2_2026-11-25.md、docs/RESEARCH_SYNC_WORKFLOW_2026-10-15.md、platform/future_model/docs/START_SKILL.md、唯一近期交接 research/coordination/DECISION_WORKBENCH_PRODUCT_PRIVACY_HANDOFF_2026-11-19.md。核对并保存当前工作区，不覆盖其他研究。默认现有Psychohistory-Platform云端环境，实际实例和设置需核实。Python3.12、Node24 LTS、现有锁文件；支持环境不足如实报告。
- 从最新main建立独立v0.7候选开发分支，在候选分支内审查并整合#61符合v3.2的代码及回归修复；记录原始提交、整合方式、冲突和差异，不合并任何旧PR或main。用户本次同意推进阶段工程，提交独立分支并准备Draft PR供审阅；不改变生产、历史版本和外部部署。
- 禁止Qwen/Ollama/GPT/Claude等外部AI推理、第三方预训练权重/嵌入/重排/生成依赖及训练。普通免费开源工程库允许。安装网络仅必要免费依赖；核心运行断网。不得新增费用或扩大权限；费用不明的CI不触发，必要提交用[skip ci]并实际执行本地可用回归。
- Codex按完整任务自主排序、分阶段提交但不拆成多个无闭环的小任务，不擅自缩减B01–B12。不等待五轨新增研究；锁定实现清单，后续资产另列评审，不移动验收目标。

## 2. 本次必需交付及后续边界
B01：锁定main/#61代码、依赖、历史数据格式；复用现有数学核心、API/CLI、React、SQLite与手机已有工程。执行支持环境基线和完整回归；复核首次取消、迟到响应及确认竞态。保存旧数据读写/导出兼容。不得把旧PR整体视为已合格。

B02/B03：创建自主认知引擎及版本化解析接口。原文义务、可舍弃候选、独立未知、可信确认分离；保留原文跨度、角色、主体、条件、否定、比较方向、数值、单位、时间、指代、修订及来源。接入已有组合中文数词（规范大数、口语省略候选、比例）、日期候选、数量单位周期分离；有限逻辑推理仅在已核实语义域内使用。禁止把手工确认的零值当自动语言识别，禁止靠持续扩大固定业务词表假装开放理解。有限规则与结构化降级真实标记；首答尽量给出有依据的局部结果、至多一个优先澄清，重大风险例外，不强制技术表单。移除新运行路径及依赖中的第三方AI；历史记录保留原origin；旧use_local_model=true采用R60候选的自主路径+明确退役通知，或明确拒绝并记录兼容决定；绝不调用旧模型。开放语义、可学习解析器、CRF/组合语法训练接口可设计与测试固定参数算法，训练、权重产生及自主进化暂缓。

B04：构建实际本地全文索引，复用既有154份清单、BM25及版本/字节核验，逐份报告成功、缺失、重复、来源许可及变更；覆盖可用的当前知识而非只登记标题。知识卡含理论、事实类型、来源、版本、日期、许可、适用边界；查询相关性与证据资格分离。按决策目标反向提出证据和方法需求，不能把检索到的文字直接当事实。已验证公开资料可离线索引；联网事实更新实现受控接口与来源隔离、时效、恶意内容防护和离线降级；实际联网功能未完成则明确状态，不调用外部AI、不默认发送个人数据。

B05：建立可信原生DecisionState投影，使用通用比较符、类型精确量、身份、期限、聚合口径、来源与义务覆盖。硬约束独立，不以候选数量、同名指标、自报boolean、缺失字段或确认等同真实事实/许可。明确不支持/UNKNOWN；条件未确认不得放宽底线。验证第55/56/57轮已知失败在完整入口中的行为。联合关系不能由独立区间冒充；新派生量必须按原始证据、模型版本和适用域重验。保留非适用、未确认、冲突、预算超限状态。

B06：连接现有原生注册表describe/validate/execute、版本化依赖和补证计划。基于问题及合格输入按需选择方法，硬约束优先，保留局部独立结果、条件比较、模型分歧、风险及敏感性；不虚构概率、平均竞争模型或统一人生总分。对旧规格15入口逐一核对实际当前注册表并测试合法、缺项、不适用、异常、边界和数学参照；不一致如实列明。科研候选方法保持隔离，不能因JS合成实验通过直接加入生产资格。至少将既有可用的原生可行性、分维度比较和风险/情景方法形成真实白话到确认再到数学计算的闭环。

B07：极简中文自然对话优先，先显示能够支持的实际分析，未知与关键问题可见，计算公式、数据来源、条件、风险及可编辑情景按需展开。计算结果、图表、解释、选择与修订身份一致。不能生成任意无依据的结论；可用受控解释，不伪称自由生成能力。用户最终选择和任何外部行动授权分离。

B08：统一语义诊断、方法准备、计算、解释等分层结果协议，绑定主体、会话、用途、版本、源、依赖、真实运行标记及截止时点。实现可信服务端验证及原子更新，防止旧响应、跨会话/版本/用途、ABA撤回恢复和缓存篡改；不能把研究中模拟布尔/JSON key视作认证。数学、工程、科研、真实使用结果分别报告。

B09：实现本地个人长期决策记录和可修订共享资源状态；至少支持目标/底线/偏好、实际与估计收入、实际支出及退款、时间与期限、任务进度、旧计划与新决策关联、事前预测与事后观察及复盘。确认后的真实状态驱动可行性重算；不同历史但相同当前资源和义务的未来判断一致；不得重复扣历史费或使用已过时间。最少交付现金/时间/期限/进度的跨轮修订与相关结果失效闭环，复用原生可用方法，复杂连续块、不确定工时、调查失败、长期DP可接入研究隔离入口供复算，未获独立准入不得宣传已上线。默认临时分析；保存、跨会话使用、研究、训练分别授权；用户可撤回、导出、删除、备份和恢复，防止旧授权复活。个人数据不上传公开仓库。原反馈预测不改写，未选行动反事实未知。

B10：建立可插拔候选方法/算法/知识版本登记、开发数据管理、反馈/复算与回退接口；记录实际结果和旧版本对照，未来经授权训练/更新；本次仅固定逻辑与确定性学习基础设施，不训练、不自动调权上线、不声称已实现持续自我学习。C035/C036、R系列及新研究DP等未准入候选保留，冻结协议、R073、PESEN v0.1及历史证据不变。

B11：现有32情节64轮167标注、28数值义务及所有已公开研究例仅作为开发/工程回归，不当独立留出。历史数值候选25/28，三项隐含0需要人工语义；现有64轮的开放领域自动理解未证实。分别测原文义务覆盖、误识别、正确未知、错误确认、硬约束漏失、错误放行/拒绝、条件、主体、单位、数学误差、来源、追问、时间与资源。固定工程集零关键错误只是该集验收要求；拒绝全部输入不是成功，须展示真实非空有用计算。与旧平台和简单基线做工程对照；独立轨掌握新情节、盲评及普通AI/专业工具对照，Codex不得获取并拟合独立样本。真实用户效果及优势留独立验收。

B12：复用现有Mac本地工作台和iPhone离线能力，建立同版本核心及跨端数据/计算契约；Web作为工程入口，最终独立App目标保留。至少完成可实测的本地Mac/Web运行、移动离线模块契约与工程回归（环境可用时），明确哪些核心能力独立离线，Mac辅助路径须用户控制、最小授权、无公网。实体iPhone/Mac连接、分发、安全同步、完整手机独立引擎若无真实设备/权限，标BLOCKED/NOT_RUN，不以浏览器或托管macOS代替；不购账号、不部署。

## 3. 必须运行的端到端场景
使用虚构开发数据，至少运行真实API、CLI及实际可用浏览器入口，禁止仅mock数学或手写结果。场景覆盖：(1) 房租与停车联合预算、隐含币种或周期、超限与补证；(2) 岗位夜班零容忍，报告/承诺不当实际事实；(3) 已付培训费、实际退款、未来费与剩余现金，拒绝重复扣费及预测现金误放行；(4) 已有计划期限与时间共享、连续与可拆任务，条件未知保持未知，修订后相关输出重算；(5) 指标/主体/条件/否定/引用与不完整语句，候选丢弃不撤销义务；(6) 两轮纠正、同时修订多字段、并发/取消/撤权、旧结果复活与恢复；(7) 断网、旧local_model参数、旧环境变量及失效缓存，无外部AI网络调用；(8) 历史备份、删除、撤回、记录/复盘及跨端数据契约。对每项给出真实调用路径、输入、输出、版本、测试日志和反例，未完成项不能写PASS。前述例子都是已见工程开发用例；独立验收另做。

## 4. 证据与交付
先锁定实际资产清单，复算选用的原型，区分工程可用、研究隔离、未获独立验收、未实现/阻塞。以下索引仅优先入口，53项Git身份在固定main实际目录核对；没有本次重新执行其全部实验或逐文件全文复审。继续读取历史R34/R50及有关源，按B01–B12提交完整需求→实现→测试→证据/未完成矩阵，勿机械移植所有原型。任何不满足原生条件的新方法留隔离，列出缺失原因与下一研究问题。R34/R50中Qwen相关安排由v3.2取代。

交付完整候选源码、可安装启动说明、变更/迁移清单、依赖锁、研究方法与来源登记、逐门验收报告、明确失败和复现命令、独立验收交接（不含独立留出内容）、阶段后续清单。建议在候选分支建立V07_ACCEPTANCE.md、V07_RESEARCH_INTEGRATION.md、V07_INDEPENDENT_HANDOFF.md，状态以实际为准。验证旧功能、原生入口、隐私、回退、断网、数值与资源；执行现有支持环境verify及真实浏览器测试（可用时）。测试工具/运行平台不充分、功能没完成或关键错误未修复则候选仍待审，不发布。报告初始/最终HEAD、分支、Draft PR地址、实际测试计数、缺失项及阻塞。用户保留合并、部署、训练、费用及后续重大范围选择。不自动调整五轨。

## 5. 固定索引
历史完整规格：research/decision_hub/2026-11-24-version-integration-specification/README.md（66e7d855f548663fed140ec3df6f3fb5ac3d6453），specification.json（58163b4cd93b4b6cbd7212d599283ae8133a105a）；v3.2（7cee2ec8e740ef3b89c0b5d4b2fc7336fac19b85）。两语料language_corpus.json（be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb）、corpus.json（05c239f3f3b1f46235fa2464d2945c21c6c08132）。原生方法契约 research/decision_hub/2026-11-24-native-method-contract-index/method_contracts.json（4ff1666907c362066dcef697d955bc6fb689b75c）；知识清单 research/decision_hub/2026-11-24-method-corpus-index/corpus_index.json（6862d5a2cd3c7eb3f2da9a85d79c8b3386f2a102）；BM25 research/decision_hub/2026-11-24-content-method-retrieval/probe.js（7d78f8c89ac73a2228ddca40dd45ad8b02366554）。旧反馈复算目录2026-11-24-feedback-replay-and-rollback。独立留出不在本工程任务包。下列为优先入口的文件路径与Git blob：

### B01 基线与迁移
- `research/decision_hub/2026-11-25-autonomous-runtime-migration-contract.md`  `b6826e37638286947f1eff691d07d57bf4e7d10e`
- `research/decision_hub/2026-11-24-v06-first-turn-cancellation.md`  `093c01a5a44e9b3b64b7652d15204492c2b02787`
- `research/decision_hub/2026-11-24-50-round-integration-review.md`  `4d394d2cb6e1e1dfc667f2a8806f896a36bbdbef`

### B02/B03/B05 自主语义、义务及可信投影
- `research/decision_hub/2026-11-25-unified-semantic-quality-contract.md`  `ad1f8ab7be83d28391ee62ce77a44d5f59804bef`
- `research/decision_hub/2026-11-25-unified-semantic-annotation-bridge.md`  `af648d16ee96b9af4a3efb61b413d113208bb0ca`
- `research/decision_hub/2026-11-25-unified-candidate-obligation-interface.md`  `bdf9bc7a42f33d9c48708970d6ac03a78ef276de`
- `research/decision_hub/2026-11-25-unified-reference-candidate-interface.md`  `5b55d2104f74246d3e6d5accc31da1140c22bedd`
- `research/decision_hub/2026-11-25-unified-quantity-candidate-interface.md`  `d15592a912a7a15df3fb19b045e530c4b0d315cc`
- `research/decision_hub/2026-11-25-native-currency-period-bridge.md`  `d7eedbca02da7f66f06911fffedc8f8b82be3f90`
- `research/decision_hub/2026-11-25-native-negated-bound-direction.md`  `2c7810d1cad4986b9ecabdf727adab5600ed6fca`
- `research/decision_hub/2026-11-25-native-subject-attribution.md`  `e957deba40302b7f6d9ee61c34196d7ac28ce124`
- `research/decision_hub/2026-11-25-field-lineage-semantic-patch.md`  `307f8ba1291ec9ad83aca578bd5a02508d1e6110`
- `research/decision_hub/2026-11-25-raw-field-candidate-coverage-and-numerals.md`  `07dcbda9532dbc3b330abfd79a399cb52aa91aeb`
- `research/decision_hub/2026-11-25-temporal-quantity-candidate-separation.md`  `8a6b42f83b80283db6e215fe48f4fb2efbf8368c`
- `research/decision_hub/2026-11-25-civil-temporal-anchor-version-replay.md`  `cc9f6c6103e4ac863d2cdaa6961721149fd4189a`
- `research/decision_hub/2026-11-25-open-span-quantity-composition-audit.md`  `175f8b48a4cc46cb3b41b7b65b13b06448bf461a`
- `research/decision_hub/2026-11-25-colloquial-numeral-magnitude-ratio-candidates.md`  `f6684299a3720a533e44343b123edff085c7ee05`
- `research/decision_hub/2026-11-25-quantity-unit-period-evidence-composition.md`  `c89fbaede02776da34e6861328fa1933a855fb4c`
- `research/decision_hub/2026-11-25-implicit-zero-role-condition-inference.md`  `aa30d5d4cd66d4bc2bc736372b9c0485b63f1362`
- `research/decision_hub/2026-11-25-confirmed-semantic-field-replanning-bridge.md`  `76b92d0de008ad83d6a12bd2b7f247eea316932f`

### B04 科学知识与方法发现
- `research/decision_hub/2026-11-25-grounded-knowledge-provenance-inference.md`  `1a7a8560ff3349635966857a07a4e71b1680f7f6`
- `research/decision_hub/2026-11-25-native-method-backward-knowledge-planning.md`  `ca51e90ab907c50524243231dc905f7ad1067ea8`
- `research/decision_hub/2026-11-25-linked-method-source-coverage.md`  `63f76ee0322736a2866b04822d2cf0ac203504d7`
- `research/decision_hub/2026-11-25-unified-concept-knowledge-interface.md`  `c1593a63195955f492140d21a54f34162fbcea8a`
- `research/decision_hub/2026-11-25-knowledge-revision-method-receipt-bridge.md`  `33b87eae4f6500e3bab01854f97850ceb27a178e`
- `research/decision_hub/2026-11-25-contextual-goal-discovery-method-preparation.md`  `6e566bb73ae1b34a25945ef29843d6a16d07b5b9`
- `research/decision_hub/2026-11-24-incremental-byte-verified-retrieval.md`  `3941256a5e560a8cdc55af8b974cb89a090438ea`

### B06/B07/B08 数学调度、解释、来源与当前性
- `research/decision_hub/2026-11-25-shared-parameter-lineage.md`  `412a98c4bd335864a32f27aa796fc8a42414e7f4`
- `research/decision_hub/2026-11-25-certified-decimal-projection-native-c028.md`  `f72aaacdf7253505cde3ad8050c45a5a2a99ea50`
- `research/decision_hub/2026-11-25-derived-receipt-native-shadow-verifier.md`  `1a6572805eaeb9400ca5b8429a14e1f518493a91`
- `research/decision_hub/2026-11-25-integrated-language-derived-joint-native.md`  `260a316b07e98772a065c3ab1c548e848f64d842`
- `research/decision_hub/2026-11-25-method-publication-revision-transaction.md`  `36b1d776ec4d71ad7f28d27c68feae438a8acb07`
- `research/decision_hub/2026-11-25-unified-research-result-envelope.md`  `177574fed228e81752863c7993527aa2118aeee5`
- `research/decision_hub/2026-11-24-faithful-conditional-explanation.md`  `0377f7f24cfa45014f4536b770d292872266a080`
- `research/decision_hub/2026-11-24-partial-regret-publication-certificates.md`  `84a8abdd595152a81b270f7cc21c8361ceee71f8`

### B09/B10 长期状态、资源、反馈及研究候选
- `research/decision_hub/2026-11-25-authority-bound-selective-restore.md`  `75deb196da9b81a4d872ac29187101235194ac1c`
- `research/decision_hub/2026-11-25-purpose-bound-feedback-lineage-replay.md`  `5d2695da1f5a380369714adb5dd6fe0a5cdaa8db`
- `research/decision_hub/2026-11-25-purpose-qualified-robust-personal-planning.md`  `c9f8c9741eb2b021dddb2e9f795da624068f8f7f`
- `research/decision_hub/2026-11-25-semantic-resource-ledger-temporal-bridge.md`  `65008b82d4720e931c99bd66ed03228b1f8ef69e`
- `research/decision_hub/2026-11-25-integrated-ledger-planning-candidate.md`  `907f12081ddce7bb752ae498bcf21f4b4b218a60`
- `research/decision_hub/2026-11-25-anchored-deadline-shared-time-feasibility.md`  `e5a2b2921d9c810b82a1e449200b17caf987cf7d`
- `research/decision_hub/2026-11-25-contiguous-task-window-feasibility.md`  `089e7d446004f5303a26a6de25ff328fc857295e`
- `research/decision_hub/2026-11-25-correlated-workload-observation-scheduling.md`  `227daac97ef9bc28b62d0c5f3087602a05e0cb8b`
- `research/decision_hub/2026-11-25-costed-information-time-cash-feasibility.md`  `e828e2cb88fcc9d1fc4825908f27b7684fdb31b1`
- `research/decision_hub/2026-11-25-delayed-failed-information-fallback-scheduling.md`  `a5c9bd9dcfd5955d7487ab60e928d7626273b415`
- `research/decision_hub/2026-11-25-realized-cost-incremental-replanning.md`  `43edd309981f55ff110de8fb57be0248f9a075df`
- `research/decision_hub/2026-11-25-selective-replanning-dependency-invalidation.md`  `ffac85bbee74bcd78cb7e34ab91d65d260753a91`

### B10/B11/B12 学习、真实数据与产品验证
- `research/decision_hub/2026-11-25-full-native-language-evaluation.md`  `445c19d01268bc4ec5e5d8b6a9eb1cfc237ab1b2`
- `research/decision_hub/2026-11-25-autonomous-language-learning-readiness.md`  `82f53eb20bcb7b49e0e56088a7c2c586000627fa`
- `research/decision_hub/2026-11-25-autonomous-language-data-resource-readiness.md`  `e770b0a21fdd337561a941d2b21dae9ec00923b5`
- `research/decision_hub/2026-11-25-partial-supervision-crf-objective.md`  `0fae5d3a25e09632b0ad3d49593393b74f0589e6`
- `research/decision_hub/2026-11-25-partial-supervision-crf-numerical-crosscheck.md`  `84b2c651b628139c84ea43ee1d7c7ff3989756b8`
- `research/decision_hub/2026-11-25-joint-multilabel-span-partial-objective.md`  `fdaab2691c5b86a383f4daf5b7875d4279e67920`

## 6. 阶段原则
本版本验收重点是可运行的自主基础平台和长期决策闭环，能力不足必须明确展示；长期产品的自主开放语义、知识推理、可学习模型、真实数据效果、独立移动App与竞争力仍是后续完整目标。科研继续并行，后续以真实使用缺陷、合法数据、独立留出、资源预算、模型准入和可验证提升驱动版本升级。本文不声称全部130轮已重验、正式开发已完成、云端环境设置已修改或独立验收已执行。
