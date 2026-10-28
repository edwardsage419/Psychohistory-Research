# R247 S43：观察家族人口历史对第三代存活预测的有限信息价值

日期：2026-10-29（Asia/Singapore）。证据：E1_SYNTHETIC。原R247正式资格 `CLOSED_BOUNDED_E1_EXACT_FINITE_GALTON_WATSON_AND_CORRELATED_FAMILY_SHOCKS` 保持不变。

## 计算前冻结及不可变来源
先行协议 `protocols/R247_S43_OBSERVED_GENERATION3_SURVIVAL_BRIER_PRESCORE_FREEZE_2026-10-29.md`，冻结提交 `5a5f82b57f499486a0ff6ecdafa06c188bf74dda`。R轨使用原R247 `R247_EXACT_RESULTS.json` blob `33c948db4a5c3b0104f233fd8e03daa79faebccf` 中四代可见路径联合概率。B轨独立使用原R247 `R247_ALL_2304_ORIGINAL_BINARY_TREE_FAMILY_SOURCES.csv` blob `42de5332f4aafae65487a71f03fc0dce5beb59df`，每个world 256个完整八bit人工来源。

目标 `T=1{Y3>0}`。合法前缀F0无信息、F1只含Y1、F2只含Y2、F12含Y1和Y2。预测是已知人工全分布的精确oracle概率，评分为条件Brier风险。禁止未来Y3、隐藏H/U/K或潜在节点外生bit作为合法输入。

## 九世界精确结果

| 人工世界 | F0 | F1 | F2 | F12 |
| --- | ---: | ---: | ---: | ---: |
| IID_FAIR_0_OR_2 | 3471/16384 | 975/8192 | 111/2048 | 111/2048 |
| IID_SUBCRITICAL_0_OR_1 | 7/64 | 3/32 | 1/16 | 1/16 |
| IID_SUPERCRITICAL_1_OR_2 | 0 | 0 | 0 | 0 |
| DETERMINISTIC_ONE | 0 | 0 | 0 | 0 |
| DETERMINISTIC_TWO | 0 | 0 | 0 | 0 |
| GLOBAL_SHARED_ENVIRONMENT | 1/4 | 0 | 0 | 0 |
| GENERATION_SHARED_SHOCK | 7/64 | 3/32 | 1/16 | 1/16 |
| SIBLING_ANTICORRELATED_OFFSPRING | 15/64 | 3/32 | 3/32 | 3/32 |
| STATIC_HIDDEN_TREE_SENSOR_ALIAS | 3471/16384 | 975/8192 | 111/2048 | 111/2048 |

**发现1：已知第二代可见人口，在九世界中均没有因再加入第一代人数而改善第三代存活的Brier风险。** F2和F12的风险在九世界全部相等。此结果限于预冻结的九个有限人工机制和该二元预测目标；不能推论任意非IID分支过程都具有Markov性。某些world的F12支持单元数比F2多，但额外细分没有降低本目标风险。

**发现2：共同环境导致早期观察可完全揭示下一代是否存活。** GLOBAL_SHARED_ENVIRONMENT的F0风险1/4，观察Y1后风险0；同一潜在共同冲击支配整个三代树。该结论依赖冻结人工环境，不是历史社会扩散因果证据。

**发现3：可见人口历史无法验证真实隐藏家族。** IID_FAIR_0_OR_2和STATIC_HIDDEN_TREE_SENSOR_ALIAS全部合法风险和支持单元数一致，后者隐藏H3始终为0。风险相同不意味着传播机制相同。IID独立offspring的PGF不能用于GLOBAL、GENERATION_SHARED或SIBLING_ANTICORRELATED真实机制。

## 执行与限制
R轨独立从四代观察联合概率逐路径平方误差积分，实际完成118项程序检查，失败0。B轨另从2304条完整人工CSV按可见前缀分组，以成功数s和组质量m计算 `sum s(m-s)/(256m)`，完成2350项检查；两路线对九世界四前缀的36项风险与36项支持数共72项完全一致。收据变异值999被拒绝。把目标Y3泄漏进信息集可得到0风险，单列非法负对照。

R程序：`research/validation/r247_s43_observed_survival_brier_20261029.js`；机器收据：`research/validation/R247_S43_SURVIVAL_FORECAST_EXACT_RECEIPT_2026-10-29.json`。Node复算：`node research/validation/r247_s43_observed_survival_brier_20261029.js`。B轨审计见 `research/evidence_audit/B_R247_S43_INDEPENDENT_SCIENTIFIC_AUDIT_2026-10-29.md`。

程序性独立复核属于同一研究项目内部，外部研究团队复现0。真实人类E2新增0、历史E3新增0。没有样本外拟合、现实校准、因果验证、无限代灭绝推断。R073模型评分及PESEN v0.1冻结；完成全部R系列后再分类，最后熔炼。新增CI须先确认免费额度，未获确认前不启动。