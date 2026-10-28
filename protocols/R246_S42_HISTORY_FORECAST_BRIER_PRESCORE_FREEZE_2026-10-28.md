# R246 S42：四格人工事件的历史信息与下一格概率预测，事前冻结

日期：2026-10-28（Asia/Singapore）。研究编号 R246 S42。原目录 11-006。证据 E1_SYNTHETIC。R073 评分与 PESEN v0.1 保持冻结。此增量不变更 R246 原正式验收。

## 不可更改的上游
原始九世界四格 Bernoulli 事件机制、4608 条完整来源：`research/R246/R246_ALL_4608_ORIGINAL_BINNED_EVENT_SOURCES.csv`，blob `f817b78f833cf13ea589bc5ab732bc6947d66a3a`。
独立冻结的完整观察四元路径 PMF：`research/R246/R246_EXACT_RESULTS.json`，blob `8aec1fd3f6dba6073f03e74f8f854f7d6a46a6c3`。
原 R246 先行协议 blob `9b4cad2b5da561eedb4cb4605ea3df6e591dc313`，原正式验收 `CLOSED_BOUNDED_E1_FINITE_BERNOULLI_EVENT_SELF_EXCITATION_SURROGATE`。
original239 v7.8 crosswalk blob `36f24235901172642c46853298aebb421f1a3552`，154项待核队列 blob `3b96d46b3d88ccafd779a08509c3cfd0e435772f`。

## 冻结问题与预测评分
预测目标 `Z=observed_event_Y4`，合法信息集严格为 F0=空、F3=(Y3)、F23=(Y2,Y3)、F123=(Y1,Y2,Y3)。只允许使用第4格之前观察到的事件 Y，严禁使用真实隐藏 U、真实事件 H、生成 hazard、原外生随机源位及第4格结果作为预测特征。未来结果加入信息集只用于单独的泄漏负例，不计入成绩。
对每个 world 的完整四元观察联合 PMF，条件预测为 `P(Z=1 | F)`。只对正支持的前缀条件评分；无支持前缀不能当成预测成功。严格有理数 Brier `R(F)=sum_x P(x) P(Z=1|x)(1-P(Z=1|x))`。分别输出 F0、F3、F23、F123 四个风险及三次嵌套收益。只做人工 oracle 风险，不拟合真实数据，不能称样本外预测或校准实证。
预注册检查：四个风险随信息增加非增、均在 [0,1/4]；F0 等于边际 Bernoulli 方差；IID_LOW、IID_HIGH、ALTERNATING_EXOGENOUS_RATE 历史收益均为0；SELF_EXCITING_LAG1 仅Y3已充分；SELF_EXCITING_TWO_LAG 在给定Y3后Y2仍有预测收益；SELF_EXCITING_LAG1 与 STATIC_HIDDEN_SELF_EXCITING_SENSOR_ALIAS 全四项风险严格相等。其它世界仅报告计算结果，禁止按结果更改预注册假设。

## 两条独立算法与负例
R路线从原 R246 冻结的完整16格观察 PMF 按条件质量计算风险，全部九世界及36项风险。B路线从原 R246 的4608条 CSV 原始来源逐行重新分组，用整数分组成功数和组内 `s(m-s)/m` 求风险，再除以每世界512；不调用R路线预测函数，结果计算完成后才与R路线收据比较。核对每世界512条不同9位外生来源、原概率1/512、Y字段二元、N累计一致、两观察别名完整路径逐source一致。验证故意篡改一项风险为999能被B路线拒绝；未来Z加入预测条件使风险人为变为0，只列为泄漏示例。
科学审计须标明同项目内部独立算法复核，不称外部独立复现。R报告路径 research/validation/；B报告 research/evidence_audit/；A来源 research/data_scout/。新增文件优先，发生并发冲突只记录，绝不覆盖共享文件。

## 解释边界与费用
此四格二元过程不是真实连续时间 Poisson 或 Hawkes；每格最多一次事件，不能代表同格多次事件、连续时间条件强度或真实历史因果。E1、E2、E3分别记录，真人E2与历史E3本轮均不得凭人工结果升级。仅使用现有免费资源，不触发 GitHub Actions 或收费 API；CI 状态以实际查询为准。先完成所有R目录再分类、最后熔炼，个人决策产品暂停。
