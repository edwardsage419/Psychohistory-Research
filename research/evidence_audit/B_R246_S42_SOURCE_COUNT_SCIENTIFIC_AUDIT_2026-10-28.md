# B轨 R246 S42 独立来源计数科学审计

日期：2026-10-28（Asia/Singapore）。审计目标为R246 S42第4格事件预测风险。审计性质：同项目内部不同数学算法的程序性独立复核，E1_SYNTHETIC，外部独立复现0。

## 冻结与输入

事前冻结协议 `protocols/R246_S42_HISTORY_FORECAST_BRIER_PRESCORE_FREEZE_2026-10-28.md`，冻结commit `350d3fcb6853716fb442263f63916615aec1fa9c`。B轨只读取原R246完整CSV `research/R246/R246_ALL_4608_ORIGINAL_BINNED_EVENT_SOURCES.csv`，Git blob `f817b78f833cf13ea589bc5ab732bc6947d66a3a`。R轨从独立的原观察PMF计算；B轨从逐条原始人工来源计数，不调用R轨概率风险函数。

B轨按world与合法历史信息集分组，整数统计每组m条来源和s个第4格正事件，风险 `sum s(m-s)/(512m)`。全部来源每world 512条，每条概率1/512。检查九位外生来源唯一、二元事件、原累计计数和全来源总量，禁止使用U、隐藏H或生成hazard作为预测特征。

## 实际复算

在隔离JavaScript V8执行与归档脚本同源的计算函数，实际读取GitHub原CSV的4608行。显式执行 **37669项程序检查，失败0**。完成九世界36项Brier风险与27项历史收益逐项比较，全部与R轨机器收据一致；四种信息集的正支持前缀组数也逐项一致。两观察别名世界按同一九位来源逐行比较，512条观察路径全部相同。

负例1：人为把IID_LOW世界F0收据改为999，独立结果比较检出异常。
负例2：故意把未来目标Y4当作预测信息，九世界分组内目标都为常数，计算风险退化为0；这属于未来信息泄漏，不计入合法成绩。
校准范围：人工oracle按完整已知分布给出条件概率，校准为代数自洽。没有训练集、独立真人留出、现实样本量、真实预测校准曲线、场次聚类置信区间或跨实验泛化，均记为NOT_TESTED。程序断言数量不等于独立科学假设数量。

## 归档与未完成

脚本：`research/evidence_audit/b_r246_s42_integer_source_brier_20261028.js`。
机器收据：`research/evidence_audit/B_R246_S42_SOURCE_COUNT_AUDIT_RECEIPT_2026-10-28.json`。
运行：`node research/evidence_audit/b_r246_s42_integer_source_brier_20261028.js`，默认读取原R246 CSV和R轨收据。独立Node CLI与新CI未运行，不能冒称已通过。R073、PESEN v0.1和原R246正式验收不变；新增E2/E3各0；无付费服务或额外费用。
