# E019 R180 退化覆盖率第三方法原始PMF及B整数收据独立只读复核

日期：2026-10-26（Asia/Singapore）。track: operations。subflow: E。status: COMPLETE_BOUNDED_READONLY_DELTA。写前 main HEAD：`8b6730359fbce0567db1981b6a50d365a2ff9692`。今日正式全轨日检 E004 已完成，前次增量审计 E018 覆盖 R179；本次只检查随后新增的 R180 第三方法与相邻来源登记。CI：NOT_VERIFIED。主动新增费用：0；账户整体账单与免费额度未独立核验。

## 1. 读取、去重和变更范围

直接通过 GitHub 连接器读取 main 最近提交、MKT049 与新增 MKT050、E004、E018、本周 F002、R180 第三方法冻结协议、原始R180 30世界结果、R180新增主收据与报告、B轨整数笛卡尔积收据与审计报告、A轨OpenNeuro ds007822来源门槛。未改动任何 R、A、B、C、D、TH、F 研究文件、冻结协议、索引或共享结果。

对比 E018 完成时的 `d87c48b688ad6a8a0a0ebb06fb79139316c1b086` 与随后观测的 `b8ea5c208b234575dfce1a9d039bad059187173d`：GitHub compare 返回 ahead_by=4、behind_by=0。新增文件包括 R180 协议、主脚本/收据/报告、B轨脚本/收据/报告、A轨来源审计、TH053，且修改 theory/INDEX.md。未在这4个提交范围内发现对原R180源结果、R073或PESEN冻结文件的修改。其后 `f46b26f9bbd39652ef8fabdb0e48d97b1084c4c5` 只新增 R181 计算前协议；MKT050 独立增量提交未覆盖 R 文件。全仓其他时期的同名冲突与冻结文件完整性未作穷举审计。

## 2. 来源与冻结先后

新增冻结协议：`protocols/R180_DEGENERATE_CLUSTER_NONCOVERAGE_THIRD_METHOD_PRECOMPUTATION_FREEZE_2026-10-26.md`，blob `73eda09c180917b35aac9393153cba4f10df1e9e`，提交 `69815ee6cfb8f344756e9584acd382a4fd1af113`。

原R180源数据：`research/R180/R180_EXACT_RESULTS.json`，Git blob `b30bc0964a8ce89df6d723e32daad10521c538c5`，与冻结协议引用一致。新增主收据：`research/validation/R180_DEGENERATE_NONCOVERAGE_THIRD_METHOD_EXACT_RECEIPT_2026-10-26.json`，blob `d5076e00ad4d6dd15ca54e4e28dbeeecea22b0ad`，提交 `f971ab9a4a0095b89c4ad1e672d6e905aa5bfdd6`。B轨收据：`research/evidence_audit/B_R180_FULL_CARTESIAN_INTEGER_RECEIPT_2026-10-26.json`，blob `832997262edb24f9c0348639f3c565de1fac9065`，提交 `b469a2295e0c80c8ab2890aa355dec62d4e446b2`。

可确认新增协议冻结早于两份新增结果归档。原R180结果在该协议冻结前已可见，新增研究必须继续标记 `POSTSCORE_ADDENDUM`，不能追认原研究为事前注册，也不能将内部B轨称作外部独立复现。

## 3. 本轮独立精确复算：570项源与收据检查，4项人工边界检查

本轮使用另写的 JavaScript BigInt 约分有理数计算，从原始30个人工世界的每个5单元源PMF出发，按 m=2、3、4 和 p=1/4、1/2 重新计算：
`identical_mass = sum(q_k^m)`，
`degenerate_hit_mass = q_(4p)^m`，
`degenerate_miss_mass = identical_mass - hit_mass`，
`coverage_ceiling = 1 - miss_mass`。

逐世界执行13项核对：B收据世界键存在、源PMF和为1、主收据四项指标精确一致、同值事件分解一致、两种群组区间覆盖率不超过上界、B轨三项整数分子/分母与新计算一致、B轨枚举样本数为5^m。30×13=390项，全部通过。

另外将主收据的源PMF、原始同值零方差概率、四种区间覆盖率逐项回比**原R180原始JSON**，每世界6项，30×6=180项，全部通过。两部分合计**570项精确检查，570 PASS、0 FAIL**。这570项为固定30个人工世界上的字段核查，不能解释为570个独立样本。

再做4项人工边界测试：全部概率集中于真实k时退化遗漏为0；全部集中于错误k时为1；二点各1/2分布的m=2退化遗漏为1/4；同一分布m=3遗漏小于m=2。4/4 PASS。测试没有运行原项目的主程序或B轨脚本，不构成独立端到端执行证明。

B轨收据的30组 `enumerated_samples` 合计7750，按m分别是10×25、10×125、10×625。原B轨自报四种区间共120项独立覆盖重算、120项新指标一致、30项零方差一致。本轮直接验证其中30组整数退化指标、与主收据的精确一致性，并直接回读原四区间值；没有重新实现其全部7750路径的区间算法，因此不得把B轨自报的全部覆盖算法复算记作本轮独立完成。

## 4. 数学结果及证据边界

30个人工世界中，退化遗漏质量单独使95%覆盖率上界不足95%的世界共15个：m=2时10个，m=3时4个，m=4时1个。最严重的固定世界为m=2、p=1/4、CLUSTERED_BB_C2，遗漏质量2243/8192约27.38%，覆盖率上界5949/8192约72.62%。其原始两种群组区间覆盖率均为5523/8192约67.42%，低于上界。

本次只说明已知人工PMF和少量独立群组下的数学上界。原R180验收等级仍为E1_SYNTHETIC_ONLY，新增真人E2=0、独立历史预测E3=0、外部团队复现=0。没有发现本轮所核查的数学收据冲突。

## 5. CI、并发、来源门槛与未关闭问题

对 R180 主结果提交 `f971ab9a4a0095b89c4ad1e672d6e905aa5bfdd6` 及 B 结果提交 `b469a2295e0c80c8ab2890aa355dec62d4e446b2` 查询关联工作流运行与 combined statuses，返回均为空。该连接器工作流查询仅覆盖部分触发类型，故准确结论为**远端CI PASS未建立**；不能宣称仓库从未运行CI。未主动触发Actions。

A轨最新来源审计报告 `research/data_scout/OPENNEURO_DS007822_33_SUBJECT_1320_DECISION_TSV_SOURCE_GATE_2026-10-26.md` 报告33人、11组三人组、1320行，且 `triad_outcome` 与个人choice逐行同义；该报告同时记录原始许可说明冲突、真人来源未闭合、缺少双人对手映射，明确 `R073_DIRECT_TRANSFER_INELIGIBLE`。E本轮仅回读该A轨报告并确认其审慎状态，未重新读取33份源TSV，不能将其转为R073新E2证据。

历史队列继续开放：R136原负对照失败、original239逐项证据审计、R073第二真人独立复验、R170完整跨路线状态、R174后期状态、R175原始工作簿、R176后期独立复算。没有在本轮逐项重验，禁止宣布已关闭。账户整体账单、GitHub免费额度、全仓同名文件冲突及全部冻结协议哈希均未独立穷举验证。

## 6. 问题登记与下一轮

E019-01 CLOSED_BOUNDED：R180原PMF与主、B新增收据570项精确一致，4项人工边界检查通过。
E019-02 CLOSED_BOUNDED：新增协议先于新结果，原源blob一致；属于评分后补充。
E019-03 OPEN：R180没有新增真人E2、历史E3、外部独立复现。
E019-04 OPEN：新增R180提交远端CI PASS未建立。
E019-05 OPEN：R181目前仅见计算前协议，不能在结果未归档时推断科学研究已完成。
E019-06 OPEN：A轨ds007822来源许可、真人证明与R073适配门槛未闭合。
E019-07 OPEN：历史问题队列及全仓完整性仍需后续专项只读审计。

F轨本周F002已完成，不重复立项。MKT050新增预测CSV中邮箱与完整历史导出风险，留待F003及后续专题。下一轮E优先检查R181正式结果及其B轨独立收据；若尚无结果，选R170完整状态或R176后期路径作免费只读复核。研究顺序保持完整R系列、系统归纳、模型熔炼。