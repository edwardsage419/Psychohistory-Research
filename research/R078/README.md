# R078：个体预测相同、因果作用不同、群体方差有条件可区分的精确反例

日期：2026-10-17。**状态 `CLOSED_BOUNDED`，证据等级 `E1_EXACT_SYNTHETIC_MATH`，无新增真人 E2/E3，无实际社会因果识别；PESEN v0.1 继续冻结。**

前期 R073–R077 四项不同作者真人重复博弈表现出上轮对手历史相对本人上轮历史的额外条件预测性，但**预测成功不等于对手动作对个人决定的因果效果**。R078设计并实跑两个竞争结构模型，在单人 `(X,O,Y)` 每个概率格、Bayes 最优 Brier 和 log loss **完全一致**的前提下，因果干预作用与预先指定组内独立性结构下的群体合作方差截然不同。

| 完全人工例子 | 模型A：对手历史直接影响 | 模型B：共享潜在原因，无直接影响 |
|---|---:|---:|
| 个体Brier（使用对手历史） | 0.21 | 0.21 |
| 个体Brier（不使用对手历史） | 0.25 | 0.25 |
| 仅从单人观测辨别两机制 | 不可能 | 不可能 |
| `do(O=1)−do(O=0)` 因果作用 | 0.4 | 0 |
| 10人群体合作率方差（**额外独立性假设下**） | 0.025 | 0.061 |

这只证明**一种明确假设下的数学不可识别性与可用来设计未来实验的群体差异**。群体方差必须观察真实配对/共同冲击后才能解释，不能把这些数字直接套用真人数据，不证明任何历史长时段演化模型。

正式研究包：
- [数学推导、四层框架接口、因果鉴定所需新证据与结题科学报告](R078_EXACT_OBSERVATIONAL_CAUSAL_NONIDENTIFICATION_AND_CROSS_SCALE_REPORT_2026-10-17.md)
- [精确测试运行前单独提交的研究协议](../../protocols/R078_PREDICTION_CAUSALITY_CROSS_SCALE_EQUIVALENCE_FREEZE_2026-10-17.md)，commit `b5702b4875339ebbefa741fa276c5292a96785f6`
- [纯标准库的有理数有限模型程序](r078_exact_micro_causal_macro_bridge.py)与[42项全部合成保护测试](test_r078_exact_micro_causal_macro_bridge.py)
- [GitHub Actions真实运行的两项CI均PASS](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38996053069)，两个独立运行输出字节一致
- [完全无真人原始行的2,463字节确定性数学结果JSON](R078_EXACT_SYNTHETIC_OBSERVATIONAL_EQUIVALENCE_E1_RESULTS.json)，Git blob `0291318a10c8aaefd9379e8deb13bbc326d5f307`
- [A01–A06有界验收](R078_FINAL_ACCEPTANCE_STATUS.json)

理论背景来自 [Manski 1993反射问题](https://doi.org/10.2307/2298123)、[Shalizi & Thomas 2011社会同质性/传播混淆](https://doi.org/10.1177/0049124111404820)及[Aral等2009辨别影响与同质性](https://doi.org/10.1073/pnas.0908800106)；本项目的0.3/0.7数学反例为本项目人工构造，并非这些论文的真人原始结果。

下一研究可在 R079 独立寻找具有真实组内重复采样、完整伙伴图与外生配对/反馈变化的资源数据，逐层检验“可预测历史→群体相关→可识别规则与制度效应”，不能跳过因果识别直接声称历史长期预测。

`R078=CLOSED_BOUNDED`；`R078_EVIDENCE=E1_ONLY`；`REAL_GROUP_EFFECT=NOT_MEASURED`；`REAL_CAUSAL_SOCIAL_EFFECT=NOT_IDENTIFIED`；`PESEN_v0.1=FROZEN`。
