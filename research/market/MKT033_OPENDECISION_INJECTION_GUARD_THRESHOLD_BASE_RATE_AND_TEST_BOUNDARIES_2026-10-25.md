# MKT033 OpenDecision 输入注入筛查阈值、基率效应与测试边界

run_date: 2026-10-25（UTC+08）
track: market
subflow: product
status: COMPLETE_BOUNDED_SOURCE_AND_SYNTHETIC_AUDIT
observed_head_before_write: 77caf0f300c31d063ba76a79ee483dfea4e49706
source_revision: GuilhermeBianeck/OpenDecision e5e096e9a96eea14375ce5ee0554e46d7aa32eb4
output_path: research/market/MKT033_OPENDECISION_INJECTION_GUARD_THRESHOLD_BASE_RATE_AND_TEST_BOUNDARIES_2026-10-25.md
ci_status: NOT_RUN
billing_checked: 本轮主动新增费用0；未独立查询账户账单及 GitHub 免费额度
commit_sha: 以 GitHub 写入返回和远端核验为准，不在报告中预填

## 1. 去重与实际新发现

先读 main HEAD、market MKT001 至 MKT032 文件名、MKT032 正文、E002/E003、F001、项目工作流规范及最新 R163、TH036 提交。MKT032 已分析校准和拒答，且仅概述注入风险。本轮聚焦固定源码的注入筛查机制、作者阈值实测、测试覆盖及人工基率计算，避免重复 MKT032。没有修改其他研究轨或索引。

新增机制：OpenDecision 的注入检测通过另外一个 statement scoring 问题对状态文本评分，默认两个检查陈述，取最大概率，超过或等于阈值0.2则标记。它只返回标记和分数，调用方需要自行拒答、升级人工或继续。作者报告在仅对 INJECTED_INSTRUCTION 单一陈述测试时，普通文字注入的检出率约54.2%，与带括号系统指令式注入的97.5%相差显著。降低阈值提升召回，同时增加正常状态误报。**作者单陈述操作点不能直接当作默认双陈述 screen() 的实际误报率或召回率**。

## 2. 产品机制与边界

输入：用户或第三方提供的状态文本、问题、有限候选、可选候选说明。guard 的输入是待审状态列表及两个预定义语句，输出 flagged、最大 probability、对应 statement、每个 statement 的 probability 和 threshold。源码的 statement_batch 只完成模型评分，不执行权限验证或操作封锁。

状态表达：文本及结构化状态通过模型的评分通道，外部指令与真实情景事实可能混合。算法：guard 源码 DEFAULT_THRESHOLD=0.2；DEFAULT_STATEMENTS 分别询问状态是否含有指向选项的指令，以及是否尝试覆盖阅读者的指令。每个状态两项打分，选择最高值，按 >= 阈值标记。空输入返回空数组，非法阈值或空陈述集合报错。

目标：减少外部文本改变候选评分的机会。反馈：可在离线验证集调整阈值，尚无证据表明部署后根据真实人生结果自动修正。解释：返回检测语句和概率，但概率没有独立校准为攻击真实性的后验概率。费用：项目 MIT 开源、代码公开，模型权重遵循各自许可；本轮不下载权重、不注册服务、不调用 API。隐私：普通本地推理无需外部 API，明确 pull 才访问 Hugging Face；服务默认 loopback 且没有内置身份与多租户隔离。官方安全文档要求调用方在模型外独立执行权限和费用限制。

## 3. 作者固定文档的有限样本操作点

来源：固定版本 docs/patterns.md、src/opendecision/guards.py。测试样本为40个 bracketed 注入、24个 prose 注入、120个 clean 状态，来自作者构造的有限样本。表内数值是作者文档所报比例按样本数换算为整数，未重新运行真实模型。

| 单陈述阈值 | bracketed 检出 | prose 检出 | clean 误报 |
| --- | ---: | ---: | ---: |
| 0.20 | 39/40 | 13/24 | 1/120 |
| 0.10 | 40/40 | 15/24 | 7/120 |
| 0.05 | 40/40 | 20/24 | 23/120 |

限制：样本小、同源合成构造、没有真实用户基率，未知其他模型及语种的泛化。单陈述测试仅涉及 INJECTED_INSTRUCTION，不能把此表解释为默认双陈述筛查的精确效果。源码测试 tests/test_guards.py 主要使用可控的模拟 StatementBackend 验证接口合同、阈值边界、空输入和无 statement path 回退；这组测试没有运行真实模型来证明对新型攻击的泛化能力。作者其他基准报告有真实模型运行记录，但仍属于作者报告而非本轮独立执行。

对照另一个容易误读的指标：作者 test 基准报告的总体 state_injection 变体准确率与专门 embedded-instruction 子集表现不同。基准生成器的变体标签涵盖多个任务族，不能仅凭聚合指标宣称模型抗注入。作者在 PROGRESS.md 记录 base 模型对 embedded instruction 的准确率0，在 authority injection 变体上的总体准确率约0.436；这两个指标分母和语义不同，不应直接相减为攻击成功率。

## 4. 本轮独立基率敏感性计算

用 JavaScript 数值计算上述三个阈值在**人工设定**的环境中的筛查告警精确率。明确假设：真实输入中攻击占1%，其中 bracketed 与 prose 各占一半；正常输入占99%；各类条件检出率和误报率机械沿用上表。按 Bayes 公式 PPV = prevalence×recall / (prevalence×recall+(1-prevalence)×FPR)。

| 单陈述阈值 | 人工混合攻击召回 | 正常误报率 | 假设攻击占1%时告警精确率 | 每1万输入的预期误报 |
| --- | ---: | ---: | ---: | ---: |
| 0.20 | 75.83% | 0.83% | 47.89% | 82.5 |
| 0.10 | 81.25% | 5.83% | 12.33% | 577.5 |
| 0.05 | 91.67% | 19.17% | 4.61% | 1897.5 |

这些都是假设环境中的数学推演，不能当成 OpenDecision 生产环境的测量值，也不能作为普适阈值建议。攻击比例、攻击样式、模型版本、语言和场景一旦变化，精确率将变化。该推演说明仅报告注入召回率会掩盖人工审核负担。

另用原生 JavaScript 构建可控评分的简化 screen 复刻，执行12项断言，12项通过，覆盖阈值相等时标记、max 陈述选择、低阈值增加标记、空输入、非法阈值、以及基率推演方向。**这只是接口逻辑及公式的独立合成检查，未运行 Python 包或模型权重。**

## 5. 科学证据与安全候选控制

SOURCE_CODE_MARKET_E1：固定 guards.py、tests/test_guards.py、SECURITY.md，直接支持实现与合同测试范围。
AUTHOR_MEASUREMENT_MARKET_E1：固定 patterns.md、PROGRESS.md 和作者 test 报告；结果未在本轮复跑。
SYNTHETIC_MATH_MARKET_E1：12项 JS 简化断言与人工基率计算。
EXTERNAL_METHOD_CONTEXT：NIST AI 600-1 原始风险管理文件（2024-07-26 发布，2026-04-08 网页更新）及 PIDS-Bench 2026-09 论文摘要，作为独立方法背景，**没有验证 OpenDecision 本产品**。
MARKETING_E0：任何未经外部验证的“安全决策”“可信概率”“自动防注入”泛化。
REAL_USER_VALIDATION：NOT_FOUND_IN_REVIEW；真人 E2=0，历史 E3=0，外部独立模型验证=0。

候选控制 MKT033-C1：将用户授权的指令、外部状态文本和可执行权限分层。检测结果只能触发复核，不授予支付、医疗、账户操作等权限。
MKT033-C2：记录任务类别、来源、检测语句、模型/版本、阈值、攻击召回、正常误报、告警精确率、人工审核容量及覆盖率。不同场景应独立验证。
MKT033-C3：保留人工拒绝、人工复核和不确定性提示；不得将 guard 输出 probability 直接称为“攻击概率”。
MKT033-C4：保护本地模型服务和离线报告中的状态文本，禁止未审查外网暴露与私密基准公开；限制第三方输入传播。
MKT033-C5：防止把基准合成文本结果升级为真实个人决策改善证据；引入新语言、模型或任务时重新评估误报和漏报。

这些都是未来候选方法储备，不改变冻结协议、人生效用权重或 R 主线顺序，不提前开发个人决策产品。

## 6. E 当日治理增量与 F 本周状态

E：2026-10-25 的 E002 和 E003 已完成每日实质只读审计。本轮额外核对 R163 第三方法：先冻结于 9ea466577063eb8d331ec1e46c0d6d933104fec9，再执行并发布于 992eec7b6e4bb3b1333188f963e20597f609bc49，随后 B 轨归档独立 Python Fraction oracle 9d3f05fb82e4bb3bcca9726c8ddabf4049be4920 及限制说明 6846e41cd3d7fab30a568d829b7db887b3f14214。报告为18人工上下文、7个观测等价、11个可区分，B 独立复核总数及选定对比，尚未逐一复核全部18组概率。原 R163 内部 E1 不等于真人 E2。直接通过 Actions REST head_sha 查询科学报告与 B 限制说明提交，均返回 total_count=0；新 CI 未核验通过。理论轨最新 TH036 仅为有限原始文献审读。R136 既有冻结负对照失败继续开放，original239 v7.8 的154项逐项证据审计待办继续保留。没有执行全仓冻结哈希检查，不声称全仓无变更。没有代替 R/B/TH 修改科研结论或共享索引。

F：2026-W43 F001 已在 research/privacy_safety/F001_HUMAN_OVERRIDE_AND_DATA_MINIMIZATION_2026-W43.md 完成。本轮没有重复开设周专题。为下一周 F002 增加候选风险：误报过多导致人工审查疲劳；漏报将污染决策输入；双陈述 OR 规则和单陈述作者性能不能混用；误把检测分数当作真实概率。F002 主方向仍为授权撤销、缓存及衍生数据生命周期，并将输入信任分层列为候选子项。未接入个人敏感数据。

## 7. 费用、阻塞与下一项

本轮只读 GitHub 与非中文公开资料，执行轻量 JS 合成算术，没有购买产品、论文、云服务、GPU、订阅、付费 API 或启动 GitHub CI。主动新增费用为零；账户账单和免费额度未独立核验。

阻塞：缺少独立真实模型执行、真实用户输入分布、真实攻击基率、跨语种误报率和生产端权限验证；GitHub 免费额度未经核实所以不启动 CI。

下一轮 MKT034：优先检查 OpenDecision 是否对 guard 的双陈述 OR 规则给出独立实测，或对外部意见污染、候选顺序敏感性有可复算测试；若没有可核实新证据，转向 ARDA 的本地隐私控制或其他开源个人决策记录系统。保持 R 系列全部完成后再分类，最后模型熔炼。

## 8. 原始公开来源（非中文）

1. https://github.com/GuilhermeBianeck/OpenDecision/blob/e5e096e9a96eea14375ce5ee0554e46d7aa32eb4/src/opendecision/guards.py
2. https://github.com/GuilhermeBianeck/OpenDecision/blob/e5e096e9a96eea14375ce5ee0554e46d7aa32eb4/tests/test_guards.py
3. https://github.com/GuilhermeBianeck/OpenDecision/blob/e5e096e9a96eea14375ce5ee0554e46d7aa32eb4/docs/patterns.md
4. https://github.com/GuilhermeBianeck/OpenDecision/blob/e5e096e9a96eea14375ce5ee0554e46d7aa32eb4/docs/benchmarks.md
5. https://github.com/GuilhermeBianeck/OpenDecision/blob/e5e096e9a96eea14375ce5ee0554e46d7aa32eb4/benchmarks/datasets/manifest.json
6. https://github.com/GuilhermeBianeck/OpenDecision/blob/e5e096e9a96eea14375ce5ee0554e46d7aa32eb4/benchmarks/reports/README.md
7. https://github.com/GuilhermeBianeck/OpenDecision/blob/e5e096e9a96eea14375ce5ee0554e46d7aa32eb4/PROGRESS.md
8. https://github.com/GuilhermeBianeck/OpenDecision/blob/e5e096e9a96eea14375ce5ee0554e46d7aa32eb4/SECURITY.md
9. https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence
10. https://arxiv.org/abs/2609.15017
