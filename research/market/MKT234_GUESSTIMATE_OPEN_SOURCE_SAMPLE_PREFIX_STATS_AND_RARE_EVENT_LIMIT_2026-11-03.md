# MKT234：Guesstimate开源概率表格的样本前缀统计与稀有风险可见性审查

track: market
subflow: commercial_product_mechanism_and_independent_code_review
run_date_utc: 2026-11-03
local_date: 2026-11-03 Asia/Singapore
target_key: (market,Guesstimate,upstream-main-36b5f217,first-2000-of-5000-summary+rare-event-detection+privacy)
baseline_main_before_write: f6c7b3f36b6a026a41fd7643f66465e3cbadfe37
status: COMPLETE_BOUNDED_SOURCE_AUDIT_AND_TRANSLATED_DETERMINISTIC_COUNTEREXAMPLES
evidence_grade: MARKET-E1_OFFICIAL_DOCS_AND_PINNED_OPEN_SOURCE; LOCAL_SYNTHETIC_CODE_PATH_CHECK
product_native_runtime: NOT_RUN
upstream_test_suite: NOT_RUN
real_user_outcome: NOT_VERIFIED
external_independent_product_effect: NOT_FOUND_IN_THIS_BOUNDED_REVIEW
new_R_E2_E3: 0
sensitive_user_data: NOT_ACCESSED
paid_operations: NONE
CI_dispatch: NOT_RUN
billing_and_free_quota: NOT_VERIFIED

## 1. 去重与来源版本

已检索仓库既有市场工作：Exist有MKT135、MKT194、MKT207；最近MKT232和MKT233为退休历史回测。Guesstimate在本轮仓库提交文本搜索未发现对应既有研究。选取真实开源概率表格，直接核对官方现行文档与固定版本源码，重点为用户看见的统计摘要能否代表全部模拟样本。研究不涉及个人决策产品开发。

上游仓库：https://github.com/getguesstimate/guesstimate-app
固定上游main快照：`36b5f217022fb8d85f06d5ace70ea28c10e6fb37`。
直接读取以下固定Git blob：
* `src/lib/engine/simulation.ts` blob `6da2b477da9db0995cca25ba4e80daede13479a8`。
* `src/lib/dataAnalysis.ts` blob `776e187bf6ef4f0350f3a27ef1d620b62c38c910`。
* `src/lib/guesstimator/samplers/Simulator.ts` blob `f23a43734cf0fbdc11e20f0e4692047ea2ec186d`。
* `src/lib/guesstimator/samplers/tests/Simulator-test.ts` blob `6a591891227dddf2926651cd65072ecd38aab1d1`。
* `README.md` blob `8378baf3873ee535c713590796a2bb1f4352268f`。

## 2. 真实产品与工作流

Guesstimate允许用户在表格单元输入单值、范围、经验样本或分布函数，用公式连接其他单元，按模拟样本传播不确定性。官方2026-06-21文档及源码常量`NUM_SAMPLES=5000`说明随机表达式一般使用5000样本；确定性表达式可能按输入周期缩减执行样本数，不能概括为每个单元总是5000。用户可以检查期望值、百分位数、敏感性散点图，修改假设并重新计算。用途包括项目时间、成本、业务和其他不确定数量估计。未发现产品专属独立前瞻校准或长期人生决策改善的真人证据。

官方当前文档提供免费公开模型，私有个人和组织模型属于收费计划。上游README仍写“Everything is public”，是旧文本与当前文档的版本差异；应以现行产品文档解释目前权限。不得把公开免费模型用于私人健康、财务或关系参数。当前具体收费金额未在本轮官方资料确认；没有注册、登录、付费、试用或输入私人数据。

来源：
* https://docs.getguesstimate.com/docs/Introduction
* https://docs.getguesstimate.com/docs/basic_modeling/input_types
* https://docs.getguesstimate.com/docs/theory/monte_carlo_simulations
* https://docs.getguesstimate.com/docs/basic_modeling/analysis_mode
* https://docs.getguesstimate.com/docs/basic_modeling/interpreting_your_results
* https://docs.getguesstimate.com/docs/FAQ

## 3. 直接源码发现：5000个模拟值与2000个摘要值

固定`simulation.ts`中`addStats`首先将全部非`SAMPLE_FILTERED`的`possibleValues`保留，然后执行：

```ts
const sortedValues = sortDescending(possibleValues.slice(0, 2000));
```

`dataAnalysis.ts`中`sortDescending`实际按数值升序排列。后续`sampleMeanAndStdev(possibleValues)`使用全部保留样本，而`percentile(sortedValues,...)`、`adjustedConfidenceInterval`依赖前2000个值。若前2000值的跨度小于`1e-15`且少于10个不同值，程序还会将`possibleValues`缩为首个值，进入单值统计分支。

这是一项可从固定源码直接确认的**不同样本覆盖范围**。尚未运行生产应用或上游完整测试，无法断言通常随机生成顺序会导致实际错误展示，也不能确认当前线上部署的精确提交身份。

### 3.1 已执行的有限确定性反例

在独立JavaScript V8中翻译上述切片、升序、跨度判断、不同值数目、均值及95百分位分支，使用人工输入数组；执行结果：

| 输入5000值 | 全部5000均值 | 全部5000的95百分位 | 该代码路径摘要 |
| --- | ---: | ---: | --- |
| 前2000全0，后3000全1 | 0.6 | 1 | 前缀被识别为单值，均值0、样本数1 |
| 前2000交替0/1，后3000全100 | 60.2 | 100 | 均值60.2、摘要95百分位1 |

第二例前2000有两种不同值，跨度为1，故不触发单值折叠。上述为**翻译源码逻辑的人工反例**，并非原生调用`addStats`或产品运行收据。它证明该实现对特定样本排列不稳健，不能据此估计真实用户遭遇频率。后续如果开展独立原生测试，应固定源代码及依赖，构造相同输入并验证UI实际展示、错误传播与用户可见结果。

### 3.2 稀有事件样本数限制

官方与源码的一般5000次随机抽样，在**独立伯努利试验且真实风险概率为0.0001**的假设下，零次命中的概率为`(1-0.0001)^5000 = 0.6065154956247782`，即约60.65%。这是一项解析计算，表示即使真实风险为万分之一，单次5000次模拟也常看不到该事件。没有检验Guesstimate是否采用针对罕见事件的特殊重要性抽样或额外风险计算；因此这是样本量方法界限，不是产品实测故障。

## 4. 科学边界及对未来研究的价值

* MARKET-E1：当前官方产品机制和固定开源代码。独立代码阅读支持上述分支和样本覆盖差异。
* LOCAL_SYNTHETIC：两组人工序列及伯努利解析概率；均无真人数据、无产品原生执行。
* MARKET-E2/E3：未找到可将使用Guesstimate归因于客观决策改善、前瞻预测校准或长期福利的独立真人证据。本轮检索范围有限，状态NOT_VERIFIED。
* 未来评价任何概率型决策工具，应核对：输入假设、相关依赖、随机样本数、尾部事件分辨率、输出摘要使用的样本覆盖范围、重复运行稳定性、前瞻结果和不良后果。建议优先研究有真实客观结果的工具，不继续堆叠纯模拟阶段。
* 不修改R073或PESEN v0.1冻结；没有新增R科研E2/E3。

## 5. E每日治理只读复核

2026-11-03本地日期已有E168正式实质审计，故本轮不新增E编号。写前main `f6c7b3f36b6a026a41fd7643f66465e3cbadfe37`，最近R/B新增R077第四真人实验**既有归档**的独立宏观一致性复审：80/80数值比较与7/7人工篡改拒绝，但仅重算公开宏观收据，原始参与者级预测、场次独立性和外部复现均未完成；不得把事后sign-tail参考当确认性检验，也没有新增真人E2/E3。理论轨TH219已提交，C011当天及D003本周登记为COMPLETE，不能提高R证据等级。

本轮逐一重新读取PR #1至#12：12 open、12 draft、12 merged=false，均未具备自动合并授权。PR #3相对本轮main为diverged，main独有1234提交、PR独有1提交；PR #8/#9的R170历史字节身份依赖仍须单独验收。R272现行生产YAML blob `3132b08cf4ee64b55f5112d2249894ea0ec9d42d`仍包含`contents: write`、先`--emit`再内联`assert`和自动`git push`路径，且未接入单入口前像强制验收，P0仍OPEN。R333至R340组合强制验收缺乏新关闭证据。原239队列blob `3b96d46b3d88ccafd779a08509c3cfd0e435772f`、crosswalk blob `36f24235901172642c46853298aebb421f1a3552`均与E168相同，文件级净变化0；154项/P0 27/P1 82/P2 45为已核验版本的历史统计，本轮未重新逐行统计。

当前main combined status返回0条、commit PR-triggered workflow runs返回0条。后者不覆盖所有Actions触发类型，不能据此宣称整个CI历史没有运行。实际GitHub账单与免费额度未验证，不主动触发CI。

## 6. F本周专题及权限边界

F010在2026-W45已登记COMPLETE，本轮只读。Guesstimate公开免费模型的可见性说明：未来私人价值权重、财务计划或关系输入应避免直接放入公开模型；私有模型需要付费，不符合本项目零新增费用限制。当前仅研究产品文档与开源代码，未读取用户敏感数据、未运行真实安全测试、未创建F编号。

## 7. 下一高价值任务

优先寻找Guesstimate对前瞻估计质量的独立评价，或选择其他真实产品具有客观决策结果的独立实验。若对上述静态反例开展原生验证，先在无需安装付费依赖、不会触发Actions的本地固定源码环境执行，并保留输入、完整输出和运行环境；此项属于后续候选，当前NOT_RUN。E等待R272完整checkout验收、owner对生产写权限与分支保护的审查，PR保持Draft，F维持本周完成。GitHub提交、远端blob与CI状态以提交后的实际回读为准。
