# MKT241 自我追踪缺失值处理的外部真实数据基准与决策指标边界

track: market
run_date_utc: 2026-11-03
target_key: (market,personal-informatics-missingness,arxiv-2610.41226-v1,goal-conditioned-imputation-vs-real-decision-benefit)
baseline_main: e9a84109ad7d0be54f54dfb9a2bc854339ded6fd
status: COMPLETE_BOUNDED_FULLTEXT_METHOD_REVIEW
evidence: MARKET-E1_EXTERNAL_EMPIRICAL_DATA_PLUS_SYNTHETIC_MASK_BENCHMARK
independent_real_user_decision_effect: NOT_VERIFIED
native_reproduction: NOT_RUN
paid_service: NONE
R_E1_E2_E3: NO_CHANGE

## 与 MKT240 去重及新增独立证据

MKT240 审查 Exist 官方对未输入日期的零值和缺失值规则。本轮新增来源是 Sahdra, Yacef, Lee, Kay, *Imputing Missing Data in Longitudinal Life-Logging Athlete Data*, arXiv:2610.41226, v1, 2026-10-30。它没有测试 Exist，也没有提供 Exist 的真实用户效果；它提供外部真实追踪数据上的不同缺失处理方法基准。

作者使用七组纵向追踪数据、231名个体、六种插补方法、四种人工缺失机制及10%至80%的人工缺失比例，比较单点误差、变量间关系和时间结构。方法包括 MICE、BRITS、GRU-D、WGAIN-VAE、PAIN、GRIN。原始数据来自公开研究/设备资料与作者个人记录；本轮未读取任何原始个人数据。

作者报告：PAIN在单点数值重建上通常较好；BRITS、GRIN、GRU-D在高缺失率下更能维持时间和多变量结构；PAIN在连续缺失区间下可能产生方差塌缩，关联恢复可能失败。不存在在所有任务上稳定最优的单一方法。作者提出按单点估计、关联分析、条件预测分别选择评价指标和候选算法。

## 重要限制及潜在误用

1. 作者先选取连续、近乎完整的时间窗作为参考，再人工遮蔽数值。这是基于真实来源数据的人工缺失实验，未验证真实长期未记录日期的真值。
2. 所选时间窗通常允许至多5%初始缺失，并先用类型对应规则处理；完整窗口选择可能偏向记录依从性高的个体。
3. 作者明确承认 MICE 五次插补被压成一个单一完成数据集，丢弃多重插补的不确定性优势。因此不能据此断言规范使用 Rubin 合并规则的 MICE 在所有真实任务中均劣于深度模型。
4. 缺失机制按预设规则分别生成；现实中多种机制可能混合。原研究按日聚合，设备测量真实性未独立验证。
5. 作者未随机检验真实使用者的行为改善、人生决策质量、净福利或产品付费价值；研究是方法基准，不是产品效果试验。
6. 原始代码与数据的逐项可运行复验本轮 NOT_RUN；不将作者模拟视为本轨独立运行结果。

## 对真实产品的可证伪问题

Exist 文档称相关性需要至少三周数据且每周更新，开发者API说明缺失日期可返回 null，手工 quantity/duration 的默认零规则已在MKT240记录。两者作用层次可能不同。需要核查数据源标识、显式零/默认零、观测掩码、导出文件、相关性样本选取，不能从API的 null 字段直接推断手工零值的生产处理方式。

对任何个人量化产品，单点重建准确率、变量间相关结构保真度、样本外预测、最终决策改善必须分开评分。算法可以准确补齐一个数值，却改变用户看到的相关性方向。长期决策净收益仍 UNKNOWN。

## E/F只读协调

当日 E168 已完成有界静态审计，R272 生产工作流写权限与验收门缺口按 OPEN 处理。F010 本周完成原始标准及隐私专题；本轮不新增F编号。缺失值与真实零值混合是未来数据真实性和用户解释风险，原则审查不代表安全部署。未读取健康、财务或关系私人资料。R073及PESEN v0.1冻结保持。

## 公开来源及审查范围

* 2026-10-30原始预印本全文：https://arxiv.org/abs/2610.41226
* Exist API 数据类型：https://developer.exist.io/reference/object_types/
* Exist 相关性数据门槛：https://kb.exist.io/article/18-how-long-does-it-take-to-find-correlations
* Exist 官方相关性接口：https://developer.exist.io/reference/correlations/
* 前次产品记录：research/market/MKT240_EXIST_MISSINGNESS_ZERO_IMPUTATION_CORRELATION_API_2026-11-03.md

下一步优先寻找独立随机研究验证个人追踪反馈是否改变客观决策结果，或取得免费公开复现脚本验证本论文方法局限。CI NOT_RUN；GitHub账单及免费额度 NOT_VERIFIED。
