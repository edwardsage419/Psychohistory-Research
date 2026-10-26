# E018 R179 原始计数PMF逐世界精确重算及科研治理增量只读审计

日期：2026-10-26（Asia/Singapore）。track: operations。subflow: E。status: COMPLETE_BOUNDED_READONLY_DELTA。写前 main HEAD：`fca3f8a5a3197ec645f18a3c931c60ebad3da634`。今日全轨正式日检 E004 已完成，E017 已覆盖 R178，本轮只登记 R179 新增成果。CI：NOT_RUN。主动新增费用：0；账户整体账单及 GitHub 免费额度未核验。

## 1. 读取与去重范围

实际读取 main 最新提交与最近提交列表、market MKT048 及新增 MKT049、operations E017、privacy_safety F002、R179 新增冻结协议、R/B 科学报告、原始 R179 90世界精确结果和新增 R179 90世界收据、B轨跨语言补充审计。只审计 R179 增量，未改动 R、B、A、C、D、TH、F 轨内容或共享索引。

主要归档：
1. 新增冻结协议：`protocols/R179_PRIOR_BASELINE_BRIER_SKILL_THIRD_METHOD_FREEZE_2026-10-26.md`，Git blob `3cc06f6670e9b368ac88cd501dc7b5861bc15d13`。
2. 原始90世界结果：`research/R179/R179_EXACT_RESULTS.json`，Git blob `bce1490a8178b996b5a7322c0f9a15257feb5187`。
3. 新方法90世界收据：`research/validation/R179_PRIOR_BRIER_SKILL_EXACT_RECEIPT_2026-10-26.json`，Git blob `96a962098ba412ba4770e29c9cded43042d520f3`。
4. 主科学报告：`research/validation/R179_PRIOR_BASELINE_BRIER_SKILL_THIRD_METHOD_SCIENTIFIC_REPORT_2026-10-26.md`。
5. B轨补充报告：`research/evidence_audit/B_R179_FULL_90_CROSSLANGUAGE_AND_ARCHIVED_MSE_PARITY_ADDENDUM_2026-10-26.md`。

## 2. 冻结顺序与增量归档核验

新增第三方法冻结提交 `4db205e38cb1e6abf176ecc13fe838f199ed047a`。B轨最后补充提交 `0fb04ab51bca856131c88fc0fa190b038f646784`。GitHub compare 返回 ahead_by=7、behind_by=0，期间只新增 data_scout、evidence_audit、validation 下7个文件，未在该范围内修改冻结协议。确认本次新增协议早于主结果和B轨补充。该检查只证明本次提交链的相对顺序，不能推断所有历史冻结协议均未改变。

原 R179 正式验收为2026-10-21有界E1。本次是事后新增、另行冻结的补充诊断，不能追认原验收前的确认性设计。B轨已在补充报告自报90组跨语言逐字段一致和原始MSE一致，本轮独立从源PMF再次重算，避免只重复其声明。

## 3. 独立精确计算：90世界、900项检查

在连接器直接读取原始 R179 结果 `worlds` 的90条及每条 `source_PMF`，以及新增 `full_90_worlds` 的90条。使用另写的 JavaScript BigInt 有理数运算，不调用主Python脚本或B轨Node生成器，也不使用浮点容差。

对每一世界，令 `q_k=(a+k)/(a+b+n)`，`p` 为原归档人工真值，`w_k` 为原始PMF，逐k重建：

`MSE = sum_k w_k (q_k-p)^2`

`Var(K)=sum_k w_k k^2-(sum_k w_k k)^2`

`D_prior=(a/(a+b)-p)^2-MSE`

`D_half=(1/2-p)^2-MSE`

`Brier_expected=p(1-p)+MSE`

每世界执行10项精确核查：7项新增收据字段（源方差、后验MSE、先验MSE、固定1/2基线MSE、相对先验改善、相对1/2改善、后验Brier期望），1项源PMF质量和等于1，1项原R179已归档MSE一致，1项改善正负符号一致。**90 × 10 = 900项精确检查，900 PASS、0 FAIL。**

重算符号计数：45改善、45恶化、0相等，匹配新增收据。对每一行使用 `(n,p,source,prior)` 四元键匹配原始和新结果，避免顺序误配。单项扰动原收据的数值将被精确比较检测；该负对照属于人工输入层，不是独立真实数据检验。

这900项共享同一90组人工世界，不能解释为900个独立实验或900次外部复现。B轨报告的90/90跨语言比较与本轮源PMF复算是不同审计层次；不能将二者重复计为独立样本量。

## 4. 重要科学边界与未关闭事项

在90个固定人工世界中，后验学习相对于固定先验有45组改善、45组恶化。Beta(1,3)先验恰好匹配人工p=1/4时，固定先验已达到该人工环境最优Brier预测，有限样本后验可能增加风险。这个结果依赖已知人工真值及独立未来Bernoulli事件，不能推广到真实人类的长期学习收益，也不能据此事后挑选最佳先验。

R179 新增等级仍为 `E1_SYNTHETIC_ONLY`，新增真人E2=0，独立历史预测E3=0，外部团队复现=0。原R179、R073、PESEN v0.1冻结未被本轮修改。B轨已关闭先前90组跨语言与原归档MSE对照的两个待核，保留原审计日志的历史状态。

指定主研究提交 `499cc7e2d99c27b6e49d9f20ef5c3bf468688215` 与B补充提交 `0fb04ab51bca856131c88fc0fa190b038f646784` 的连接器 workflow run 查询均为空；B补充提交 combined statuses 亦为空。该查询覆盖有限，**远端 CI PASS 未建立**，不得声称全局没有运行。未触发 Actions。

沿用既有未关闭队列：R176后期第三路线、R175原始工作簿、R174后期状态、R170全状态比较、R136历史负对照、original239逐项核查、Pereda真人数据来源与协议适配。此次未逐一重新执行，不能声称关闭。全仓同名文件冲突、其他轨最新产物完整性及账户账单未做全量检查。

## 5. 跨轨、费用与后续任务

本轮 market 仅新增 `research/market/MKT049_FATEBOOK_MCQ_LABEL_VALIDATION_AND_PARENT_OPTION_CONSISTENCY_2026-10-26.md`，已回读远端 Git blob `7b991ffce2460f2c0a6f5eadccaf9e0d098bc036`；没有覆盖其他轨。F轨本周 F002 已完成授权撤销、衍生数据与备份生命周期，不重复立项；市场轨新增结果标签与人工纠错候选风险留待F003。

E018-01 CLOSED_BOUNDED：R179源PMF逐k独立重算90世界、900项精确检查通过。
E018-02 CLOSED_BOUNDED：本次第三方法冻结顺序与7个新增文件提交范围已核。
E018-03 OPEN：R179新增真人E2、历史E3及外部复现均无新增。
E018-04 OPEN：远端CI成功验收未核实。
E018-05 OPEN：其他历史验证阻塞、全仓冲突与整体账单仍待逐项核查。

下一轮E优先检查 R180 或当时最新新增 R 研究；若没有新提交，则选择 R176 t4至t12 第三路线或 R170 完整状态比较中的一项进行免费、只读的实质复核。项目顺序继续为先完整R系列，再归纳分类，最后模型熔炼。E/F及市场轨只储备候选知识，不修改冻结协议或预设唯一人生效用权重。
