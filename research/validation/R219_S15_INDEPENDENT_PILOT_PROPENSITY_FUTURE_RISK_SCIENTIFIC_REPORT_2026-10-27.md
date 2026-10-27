# R219 S15 独立小pilot倾向估计的样本外风险

日期：2026-10-27（Asia/Singapore）。证据级别E1人工有限研究，原239条目09-010。状态：COMPUTED_INTERNAL_TWO_ROUTE_EXACT_REPLAY / NEW_CI_NOT_RUN。原R219正式CLOSED_BOUNDED_E1验收不变。

## 冻结与来源

S15事前协议 `protocols/R219_S15_INDEPENDENT_PILOT_PROPENSITY_PRESCORE_FREEZE_2026-10-27.md`，独立提交 `b32f8c39948c108d7daa502f5c23d9a2143c9225`。复用原R219全部1281条人工未来赋值来源CSV，固定Git blob `fa14af5a46694c6cc23717f8e9ee9fa2acb9501d`。原八单位、六世界、真ATE2、真分配机制及原有R219正式评分均未改变。

新增一个与未来评价独立的四人工单位pilot，索引固定为(0,2,4,6)，分别来自两X层。四个pilot处理指示按原真个体Bernoulli率独立生成，全部16种pilot赋值精确加权。仅用每层两次pilot处理计数K_x构造e_hat=(K_x+α)/(2+2α)，预定α=1/2和1。未来八单位公共X倾向HT估计仅读取未来实际处理、实际结果和pilot得到的e_hat。隐藏U、真个体p、潜在Y0/Y1不得输入观察估计器。

六世界×两种α共12项条件。五个有原始共同支持的世界，每个16 pilot×256未来原赋值×2平滑，共40960个有效人工来源槽；原POSITIVITY_FAILURE世界另有32个pilot条件保持null，严禁平滑伪造共同支持。

## 精确风险结果

| 原人工世界 | 原公共已知e(X) HT MSE | pilot α=1/2 MSE | pilot α=1 MSE |
|---|---:|---:|---:|
| CORRECT_X | 17/6 | 3673/400 | 575/128 |
| HIDDEN_U_BOTH | 467/72 | 219211/12800 | 73045/8192 |
| HIDDEN_U_ASSIGNMENT_ONLY | 187/72 | 10013/1280 | 73115/18432 |
| WEAK_OVERLAP | 257/30 | 378193/163840 | 833717/524288 |
| HETEROGENEOUS_TAU_X | 3 | 2867/200 | 137/18 |
| POSITIVITY_FAILURE | null | null | null |

在CORRECT_X世界，即使真处理机制完全由X决定，独立pilot只有每层两次处理指示时，α=1的未来MSE仍由理论已知倾向基线17/6上升为575/128。pilot估计误差及倒数非线性影响未来风险。

WEAK_OVERLAP世界原公共HT最大权重16，理论已知e(X) MSE为257/30。α=1时pilot估计后MSE降为833717/524288，未来估计均值却为1365/512，大于真ATE2。风险降低伴随偏差，不能将该平滑估计描述为原ATE的无偏估计器。

HIDDEN_U_BOTH世界α=1时估计均值为613/192，真ATE仍为2，隐藏共同原因引起的混杂没有因pilot倾向估计消失。HETEROGENEOUS_TAU_X的pilot α=1/2估计均值为3，MSE达到2867/200，明显高于已知真X倾向的3。

本轮pilot与未来分配独立，结果为严格有限来源样本外人工评价。只有四个模拟pilot处理指示，不能外推为现实倾向模型训练样本大小或独立实验。没有真实人类E2、真实历史E3或外部验证。

## 程序与复核

R脚本 `research/validation/r219_s15_independent_pilot_future_ht_20261027.js` 逐项枚举16个pilot×原未来赋值并计算严格BigInt有理数HT、均值、方差和MSE；机器收据 `research/validation/R219_S15_INDEPENDENT_PILOT_12_CONDITION_EXACT_RECEIPT_2026-10-27.json` 含12条件、192个pilot条件及源数量和负对照记录。

B脚本独立使用Bernoulli条件矩与pilot混合全方差公式，不读取R逐来源分数。预冻结40项核心字段、12项支持状态、12项pilot概率质量，另增加480项pilot条件字段与30项原公共基线字段，共574项精确交叉核验，全部通过。远端重新读取两套脚本、原CSV和正式机器收据实际重放，R/B结果均逐字段一致。

新增GitHub Actions未运行，账户免费额度未核验，没有主动新增收费资源。原R219的CI验收不自动覆盖S15。原239目录完成计数不增加，R073/PESEN v0.1保持冻结，个人决策产品继续暂停。
