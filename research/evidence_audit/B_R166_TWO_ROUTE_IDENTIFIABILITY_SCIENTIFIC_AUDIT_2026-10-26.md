# B 独立科学审计：R166 单步计数辨别能力的两种精确计算

日期：2026-10-26 Asia/Singapore
状态：PASS_BOUNDED_INTERNAL_E1_WITH_DISCLOSED_AMENDMENT
审计对象：research/validation/R166_ONE_STEP_COUNT_IDENTIFIABILITY_THIRD_METHOD_SCIENTIFIC_REPORT_2026-10-26.md
冻结对象：research/R166/R166_EXACT_RESULTS.json，Git blob 998c80ccb4398d65424bbfccfa6d36c51696a9da。

## 独立性与执行事实
方法一为独立 JS BigInt 有理数、加权示范者票数及独立复制转化分支，枚举每个群体下一代所有 2^N 个二元子代组合。对原 R166 已归档12个矩阵共84行逐元素精确核对。实际28个非中性条件、14个中性对照，非中性8个完全相等、20个不同。
方法二以二项分布单调似然比所蕴含的最佳计数阈值检验，取完整累计分布的最大绝对差。实际28个条件全部与方法一 TV 精确一致，8个为0。
方法二从冻结原始矩阵读取计数分布，并与方法一归档收据逐项比较；两者的数学归约不同，数据源和研究执行主体相同。不能称作外部团队独立复现。

## 事前协议、失败与纠正
原始事前冻结协议提交 5704ad07c3c61ffe7293ec8c97f4521727989853。原协议将 (5+9)*2 错写为56。首次 JS 执行断言 `unexpected observational partition` 失败。独立读取原始 R166 矩阵后确认比较条件实际28。追加 `protocols/R166_ONE_STEP_COUNT_IDENTIFIABILITY_ARITHMETIC_CORRECTION_2026-10-26.md`，原冻结文件不修改；所有 N、k、方向、参数、TV 和负对照不变。最终实际执行成功。属于事后算术纠正，已在主报告明示。
第一版 Python 程序包含原错误断言，保留用于审计；后续 Python 修正版已归档，但本轮没有 Python 运行或远端 CI 成功证据。

## 风险、反例与适用范围
1. 数据泄漏：本轮只有预先给定的人工核矩阵，没有训练、测试数据或真实预测标签。没有可报告的真人样本外泄漏检验。
2. 基线：等先验二元机制最优 Bayes 分类错误率 (1-TV)/2 是理论基线，不能解释为现实预测性能。没有拟合基线或概率校准。
3. 负例：中性14组全部 TV=0；非中性 p=1/2 的两个机制在单步观察下等价。错误转换率1/4变异实际产生 TV=8161/110592，负对照可检出。
4. 不确定性：所有分数来自精确有限枚举，没有 Monte Carlo 抽样误差；也没有现实抽样不确定性的置信区间或场次重采样。
5. 观测条件：完整下一代总计数 J 仅一代观察，已知 p、N 和机制参数。观察更多代、观察个体示范者或未知参数是另一个统计任务。
6. 来源依赖：原 R166 已有内部精确枚举，新增 JS 穷举属于代码独立实现；CDF 阈值是本轮不同数学路线。二者均不能验证 Mesoudi 原作者连续状态 EMG 实现或现实文化传播因果机制。

## 实际归档
`research/evidence_audit/r166_b_independent_exhaustive_20261026.js`
`research/evidence_audit/B_R166_ONE_STEP_EXHAUSTIVE_EXECUTION_RECEIPT_2026-10-26.json`
`research/evidence_audit/r166_b_cdf_threshold_20261026.js`
`research/evidence_audit/B_R166_CDF_THRESHOLD_EXECUTION_RECEIPT_2026-10-26.json`
上述两份收据含实际计算输出、源码及原始 JSON Git blob 身份，可再次运行复核。GitHub Actions 本轮没有主动触发；费用账单未核验。

## 证据判定
内部 E1 数学一致性：PASS_BOUNDED_WITH_AMENDMENT。
真人 E2 样本外预测：0。历史 E3：0。外部团队独立复现：0。
R166 原正式有界验收保持；R073 和 PESEN v0.1 冻结。继续 R 系列逐项研究，不修改共享索引或其他工作流。
