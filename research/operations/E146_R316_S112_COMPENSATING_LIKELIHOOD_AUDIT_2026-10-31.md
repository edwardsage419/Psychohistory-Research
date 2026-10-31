# E146 R316 S112 来源概率补偿变异与跨轨只读治理
日期：2026-10-31 UTC。目标键：(operations,R316,S112_af948405,paired_within_bin_likelihood_compensation_receipt_invariance)。基线main d2fc0759ccec92a399d9e68cac6986122a88bdea。本轮非盲态已读R316 S112冻结、R原始Node评分器、原始128图JSON、归档六地图收据、B独立Python程序/报告、R轨交接、最近提交、TH181、MKT176/E145/F009 phase40和12个开放Codex PR。

## 新增互补动态反例
原始R316源JSON Git blob 36da587adbc6e1d92824a5fd39516e506569166c，R S112评分器Git blob 379cb2109808f60d41d449638315904b3cb77f4c，归档收据blob 410a9c173e020984fa61e7a2420dc0e0e90190ac。V8提取原始score函数执行，正常源数据输出与持久化收据完全一致。

在A机制同一(w=1,c=1)单元内，mask=3和mask=5原概率均81/4096；人工将其分别改为82/4096和80/4096，其他源字段、概率总和和图身份均不变。原始score函数仍接受输入，六种观察映射的全部收据字段完全不变。独立按六个Bernoulli因子重算，两个变异均违反固定来源概率公式。该补偿变异说明仅检查输出汇总和归一化无法独立证明原始每图似然正确。

重要边界：原始Node CLI在调用score之前核对原始Git blob，改动的输入会被该字节门拒绝；B轨已独立验证128项Bernoulli概率并拒绝单个wrong_likelihood变异。新反例是函数层语义守卫的补充压力测试，不能描述为当前完整CLI已失守，也不能描述为原始科研结果计算错误。未修改R或B程序、冻结协议、CSV、收据及共享索引。新增JS research/operations/e146_r316_s112_compensating_likelihood.js，核心V8动态测试通过，归档Node CLI未在本轮原生执行。

## E当日跨轨检查
main最新可见提交含R316 S112六映射收据与B独立binomial审计、A轨Mao et al. 2017来源访问403阻塞、理论TH181和市场MKT176。R316 S112原生Node和B Python普通/优化模式的通过由B轨归档报告支持，本轮未冒称重新运行。R316 S112状态PARTIAL_E1_EXTENSION，真实E2/E3均未建立。R344历史归档的CI run 40063860148由GitHub API独立只读核验：completed/success，python311、python312、independent三项job success，且冻结commit 000b7043早于source commit 0eb0967f；这仅支持R344有界人工E1，不能扩大科学验收。

Codex开放PR共12个，PR #1 R257 S53检查器反例和PR #3候选修复仍OPEN，PR #2同步协议仍OPEN；不当作main已合并。R315 S111四项来源元数据覆盖缺口沿用E145登记，未重跑。R299 S95历史协议问题仍OPEN，未重新实证核验。R轨交接报告引用original239 v7.8交叉索引239项和154待核队列，当前未重新遍历所有索引字节，故仅作已读归档范围。跨轨目标去重：E146检查补偿变异，区别于B轨独立原始数学计算。未发现本轮新写入路径与其他轨冲突。费用：无Actions调度、无付费API、无新增收费操作；实际账单及GitHub额度UNKNOWN。

## 后续
将函数层概率逐图核验与现有Git blob门并列为候选审计建议，交R/B轨自行评估。继续E147新R轨冻结和独立来源验证；仅内部非盲态E1，E2/E3增量0。
