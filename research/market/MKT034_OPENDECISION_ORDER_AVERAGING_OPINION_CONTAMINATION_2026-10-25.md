# MKT034 OpenDecision 选项顺序平均与无证据意见污染的分离审计

date: 2026-10-25 (Asia/Singapore)
track: market
subflow: product
status: COMPLETE_BOUNDED_FIXED_SOURCE_AND_SYNTHETIC_AUDIT
observed_main_head_before_write: 3585975b70aa584887dedc9540daa2402d8c14ce
upstream_fixed_revision: GuilhermeBianeck/OpenDecision e5e096e9a96eea14375ce5ee0554e46d7aa32eb4
output_path: research/market/MKT034_OPENDECISION_ORDER_AVERAGING_OPINION_CONTAMINATION_2026-10-25.md
ci_status: NOT_RUN
billing_status: 本轮主动新增费用0；账户账单及 GitHub 免费额度未独立核验
commit_sha: 写入后以 GitHub 返回值与远端核验为准

## 1. 去重和新增问题

开始读取 GitHub main HEAD、market MKT001 至 MKT033 文件名、MKT033 完整正文、E002/E003 与 F001 登记，以及最新 R164 和 R136 纠正性科研文件。MKT032 已审校准与拒答，MKT033 已审单陈述注入检测和基率。本轮新问题是**选项排列偏差**与**无证据外部意见污染**是否可以由同一种干预修复。读取 OpenDecision 固定提交的 docs/consistency.md、九份 consistency JSON、src/opendecision/consistency.py、src/opendecision/backends/decoder.py、tests/test_consistency.py、tests/test_order_averaging.py、docs/benchmarks.md、基准生成器。未修改其他研究轨或冻结协议。

## 2. 固定源码和作者实测

输入：文本/字段状态、问题、有限候选及其排列；在意见污染探针中，状态追加一句来自没有核实资料的同事的建议。状态由调用方交给本地评分模型。候选排列测试对同一基础选择题做反序与两种固定随机种子的打乱，按选项标签对齐输出。意见污染测试追加一个模型原先未选择的选项建议，随后比较选项是否翻转。两种探针测试的是不同机制。

算法：lettered decoder 按候选排列打分。参数 permutations=K 对多个循环旋转顺序计算各选项分数并求平均，K 增加模型推理工作量；原有单顺序校准配置在 K>1 时失效。NLI backend 逐候选独立评分，拒绝开启 order averaging。tests/test_order_averaging.py 的常规单元测试使用模拟后端检验旋转去重、参数与校准失效；tests/test_consistency.py 的真实权重顺序敏感性回归需要显式 OPENDECISION_TEST_MODELS 和本地权重，否则跳过。源码没有独立执行支付/医疗等高风险权限控制。

作者固定 JSON 报告针对 352 个基础选择题的汇总如下。每题测试三个非原始排列，flip 指任一排列改变首选项。下列整数由 JSON 的 rate × 352 还原，本轮独立进行精确算术核对。

| 后端与设置 | 顺序翻转数 / 352 | 无证据意见翻转数 / 352 | 无证据意见被跟随数 / 352 |
| --- | ---: | ---: | ---: |
| base NLI K=1 | 0 | 276 | 272 |
| qwen35 K=1 | 71 | 245 | 244 |
| qwen35 K=2 | 21 | 未单独报告 | 未单独报告 |
| qwen35 K=3 | 25 | 268 | 268 |
| lightning K=1 | 20 | 9 | 4 |
| lightning K=2 | 2 | 8 | 5 |

注意：作者的 qwen35 K=2 JSON 没有 appended_context 字段，不能推测它的意见污染表现。作者文档对 lightning K=2 记录了 opinion_flip 8/352、follow 5/352，且 K=2 的无关评论翻转为 8/352；本轮直接读原始 JSON。作者文档还报告 qwen35 K=1 在 test 子集 94 题中有 20 题翻转，lightning K=1 为 11 题；K=2 汇总的352题覆盖多个数据拆分，不能等同一个事先隔离、独立选择 K 的外部测试。

顺序平均的作者测量：qwen35 K=1 到 K=2 翻转由71降到21，净减少50题，约70.4%；lightning 由20降到2，净减少18题，90%。仅凭聚合总数，不能证明每个原来翻转的题都被修复；也不能证明改动后真实用户决策更正确。qwen35 K=3 为25题，高于 K=2 的21题，说明更大的 K 并非在该样本上单调改善。作者记录 qwen35 K=1 到 K=2 的 p50 约69ms到142ms，lightning 约107ms到267ms，硬件与任务特定。K=2 可能提高延迟及资源消耗，且需要重新评估概率校准。

更关键的机制差异：qwen35 K=3 时，无证据意见翻转由245/352增至268/352；base 对排列完全稳定却有276/352意见翻转。**顺序不变性与抵御外部意见是不同的性质**。这些数据是作者固定报告的有限合成基准测量，没有在本轮运行真实权重，也没有独立人类效能验证。无证据意见探针是一句显式建议，不代表所有真实社会影响或提示注入形式。

## 3. 本轮独立精确合成反例

使用 Python 标准库 Fraction 对四选项 A、B、C、D 构建完全人工的可复算评分规则。内容分数分别为 4/10、3/10、2/10、1/10；候选列表第一位置额外加 1/2；按四种循环顺序平均后，各选项分数为 A=21/40、B=17/40、C=13/40、D=9/40，首选 A。

然后向 D 注入未经验证的意见偏置 +3/5，同时保留同样四种排列平均。结果为 A=21/40、B=17/40、C=13/40、D=33/40，首选 D。所有排列平均均已消除该设定下的位置偏置，外部意见仍改变选择。这是抽象数学反例，**没有模拟或证明 OpenDecision 实际模型的这些具体分数**。

另核算作者汇总的精确整数及差值：qwen35 K=1/K=2/K=3 顺序翻转 71/21/25；lightning K=1/K=2 为20/2；qwen35 K=1/K=3 意见翻转 245/268；base 为276。此为独立算术检查，不构成原作者模型权重的独立复测。

## 4. 产品能力、隐私、费用和科学等级

目标与反馈：该开源库面向有限候选评分、概率、拒答、验证和测试；K 作为调用参数由使用者配置，现有资料没有部署后从真实人生结果自动学习、因果识别或稳定价值偏好的证据。解释性：可读分数、置信阈值和候选排列诊断，分数不是个人选择成功的真实概率。隐私：本地推理可在已有设备运行，但服务端口、外部模型下载、日志及应用层权限需要另审；本轮不下载权重、不部署、不输入个人数据。费用：代码 MIT 开源，模型权重各有许可和硬件需求；无需使用任何付费服务完成本轮审计。

证据分级：
* SOURCE_CODE_MARKET_E1：固定源码与测试直接支持排列平均实现、默认校准失效和集成测试开关。
* AUTHOR_MEASUREMENT_MARKET_E1：固定 consistency JSON 与 docs/consistency.md，包含作者测量和有限合成样本。
* SYNTHETIC_MATH_MARKET_E1：Fraction 反例及 352 分母算术核对。
* EXTERNAL_HUMAN_VALIDATION：未在本轮发现可直接验证该模型提升真实个人长期决策的独立研究；E2=0、历史 E3=0。
* MARKETING_E0：任何未经验证的“无偏人生决策”“抗社会操纵”“概率可靠”推广。

候选控制：
MKT034-C1 在未来决策方法验证中将选项排列一致性、外部意见污染、事实准确率、校准与拒答率分开测试。
MKT034-C2 对外部意见附加来源、证据等级、时间、利益关系；不允许无证据建议被直接合并为高可信事实。
MKT034-C3 排列平均后重新评估阈值、校准、资源成本，保留无法排序与人工否决。
MKT034-C4 对无真实独立证据的系统仅保留研究候选，不设唯一人生效用权重，不自动执行不可逆决策。
MKT034-C5 需要跨领域、跨语种、跨模型、独立来源及真正留出的人类样本评估，不能用352个作者合成题当作人类验证。

## 5. E 当日治理增量

E002/E003 已完成 2026-10-25 当日实质只读审计，本轮仅审新增变更。
* R136 的纠正性协议先于新执行归档：冻结提交 bea9dd0c2b946f0c8a0ef3ae46ecb69a988cf06e，科学报告 c3d96d1575b31ee7fd5342dbe3c0ab56aa274210。报告声称 1215 行稳态重算及4860项正确边际断言、810组错误排序检测。状态为 PASS_CORRECTIVE_CONTROL_ONLY。**原先冻结负对照 FAILED_NONDISCRIMINATING 仍保留，不能追溯转成通过**。完整1215行 CSV 路径在 main 的 contents 查询为404，不能独立核验原始 CSV 字节与 SHA256。
* R164 扩展先冻结 95bf2e51fef98ba96c9f3b88176e5b4a4fa550ac，之后形成72人工世界观测分区及 B 独立 BigInt 精确复核，B 提交 54109f4daa8a7b5fbebff4cc7d14e760db80a963。B 报告记载360项状态比较和67项适用突变检测，仍属内部 E1；新 Python 远端复跑待办。对 B 提交、R164 科学报告提交及 R136 纠正性报告提交分别查询 Actions head_sha，total_count 均为0。不能宣称新 CI 验收。
* A 数据侦察新记录 73ea28a864bd253832dc46d1e9f44209c3180f58 只登记 Zenodo 官方 MD5 元数据及授权许可缺口，未取得原始字节，也没有满足 R073 的双边逐回合真人行动要求。不得把这项研究作为新的 R073 独立实验。
* original239 的154项逐项证据审计待办、README 导航滞后、全仓冻结字节巡检仍开放。本轮未做全仓 SHA 审计，不能声称所有协议无变化。没有修改 R、A、B、TH、C、D、E、F 轨文件或索引。

## 6. F 本周状态及候选风险

2026-W43 F001 已归档 research/privacy_safety/F001_HUMAN_OVERRIDE_AND_DATA_MINIMIZATION_2026-W43.md；本轮不重复开题。下周 F002 仍研究撤销授权、缓存和衍生数据生命周期。新风险登记候选：同一模型可对候选顺序稳定而被无证据意见影响；外部建议在状态文本中缺乏来源标注；K>1 时原概率校准失效且推理成本上升。未来原则性控制为外部证据隔离、可撤销来源授权、人工拒绝及变更后重新验证。未接入任何敏感数据、未开发个人决策产品。

## 7. 归档、阻塞、下一轮

本轮仅用 GitHub 连接器、英文公开源码和轻量本地 Python Fraction 算术。没有购买产品、论文、云资源、GPU、计费 API、订阅或主动启动 CI。主动新增费用0，账户整体账单与免费权益额度尚未独立核验。写入前已重查 main HEAD、market 同名路径、operations 与 privacy_safety 登记。若远端 HEAD 在写入期间变化，提交后须单独核对 SHA 和提交改动文件，绝不假称无并发。

阻塞：没有真实权重的独立执行、作者双陈述 guard 的真实独立测量、外部意见真实基率、跨文化真人样本和真实个人长期结果；K=2 未有独立选定后全新外部测试。

下一轮 MKT035：调查新出现的本地优先 Decision Ledger 或 Arandu 的决策记忆、结果反馈、导出与撤权机制，优先固定源码和原始文档；与已归档 Dcider、ARDA、OpenDecision 做明确的输入和权限边界比较。保留 R 全系列完成后再系统归纳、最后熔炼的顺序。

## 8. 非中文原始来源

1. https://github.com/GuilhermeBianeck/OpenDecision/blob/e5e096e9a96eea14375ce5ee0554e46d7aa32eb4/docs/consistency.md
2. https://github.com/GuilhermeBianeck/OpenDecision/tree/e5e096e9a96eea14375ce5ee0554e46d7aa32eb4/benchmarks/reports/consistency
3. https://github.com/GuilhermeBianeck/OpenDecision/blob/e5e096e9a96eea14375ce5ee0554e46d7aa32eb4/src/opendecision/consistency.py
4. https://github.com/GuilhermeBianeck/OpenDecision/blob/e5e096e9a96eea14375ce5ee0554e46d7aa32eb4/src/opendecision/backends/decoder.py
5. https://github.com/GuilhermeBianeck/OpenDecision/blob/e5e096e9a96eea14375ce5ee0554e46d7aa32eb4/tests/test_order_averaging.py
6. https://github.com/GuilhermeBianeck/OpenDecision/blob/e5e096e9a96eea14375ce5ee0554e46d7aa32eb4/tests/test_consistency.py
7. https://github.com/GuilhermeBianeck/OpenDecision/blob/e5e096e9a96eea14375ce5ee0554e46d7aa32eb4/docs/benchmarks.md
8. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/validation/R136_CORRECTIVE_Q_ORDER_SCIENTIFIC_REPORT_2026-10-25.md
9. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/evidence_audit/B_R164_OBSERVATIONAL_PARTITION_INDEPENDENT_BIGINT_SCIENTIFIC_AUDIT_2026-10-25.md
