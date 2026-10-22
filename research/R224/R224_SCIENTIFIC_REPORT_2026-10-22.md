# R224 负对照设计：八个有限人工SCM与4096完整外生来源，E1结题科学报告

日期 2026-10-22。原始239目录第 **09-015 Negative Control Designs**（P1）。本研究的科学结论仅限 **CLOSED_BOUNDED_E1_FINITE_ARTIFICIAL_NEGATIVE_CONTROLS**。各行是有限生成来源，既非真实参与者，也不是真实独立干预试验。

## 一手研究基础及边界

方法学背景是 Lipsitch, Tchetgen Tchetgen & Cohen (2010), *Negative controls: a tool for detecting confounding and bias in observational studies*, Epidemiology 21:383–388, DOI https://doi.org/10.1097/EDE.0b013e3181d61eeb，以及 Shi, Miao & Tchetgen Tchetgen (2020), *A Selective Review of Negative Control Methods in Epidemiology*, DOI https://doi.org/10.1007/s40471-020-00243-4。前者明确提醒负对照有信号只能帮助检测某些错误与混杂，具体偏差大小仍需额外条件；后者区分负对照检测与依严格因果、代理条件进行校正。Miao, Geng & Tchetgen Tchetgen (2018)的双代理秩条件结果（DOI https://doi.org/10.1093/biomet/asy038）仅列为后续方法背景，没有据此声称当前有限设计完成该定理或对应经验复现。

本研究在评分前单独提交冻结协议：[R224八世界4096来源协议](../../protocols/R224_NEGATIVE_CONTROLS_8_WORLDS_4096_EXOGENOUS_ATOMS_PRESCORE_FREEZE_2026-10-22.md)，提交 [0e6be857](https://github.com/edwardsage419/Psychohistory-Research/commit/0e6be85718a91939ee03e2be6bda0c344b903389)。先冻结后实现程序与CI，不根据结果重设机制。

## 原来源与两条独立算法

八个人工世界。每个世界二元U、四个独立均匀四值外生潜在源V_A,V_Z,V_W,V_Y，完整512来源、每行1/512、合计4096行。人工处理A、负对照暴露候选Z、负对照结果候选W、主要结果Y由事前整数阈值确定，每行分别保存实际观测A,Z,W,Y和oracle反事实。所有观测统计仅从**实际(A,Z,W,Y)**与来源概率求得，完整潜在结果只进入独立审计。真平均因果效应对应人工do(A)或do(Z)下维持其余外生源不变的完整来源差。独立第二数学路线直接用生成阈值的条件分布按U积分，重新复算每个观察风险差和真实干预效应，分数计算全为标准库Fraction精确值。

记 D_AY、D_AW、D_ZY 分别为观察到的两组结果概率差，真ATE_Y为同一完整人工来源下的A→Y平均干预差。

| 人工冻结世界 | D_AY | D_AW | D_ZY | 真ATE_Y | 解释边界 |
|---|---:|---:|---:|---:|---|
| RANDOMIZED_WITH_Z_SIGNAL | 0 | 0 | 1/4 | 0 | A独立U时Z仍能与Y相关 |
| HIDDEN_CONFOUNDED_NULL | 1/4 | 1/4 | 1/4 | 0 | 有效对照检测出人工A-Y混杂 |
| HIDDEN_CONFOUNDED_CAUSAL | 1/2 | 1/4 | 5/16 | 1/4 | 真因果与混杂同时存在 |
| INSENSITIVE_VALID_CONTROLS | 1/4 | 0 | 0 | 0 | 有效排除假设下对照仍可完全不敏感 |
| INVALID_OUTCOME_DIRECT_A | 0 | 1/2 | 0 | 0 | 实际A→W效应1/2，误判混杂 |
| INVALID_EXPOSURE_DIRECT_Z | 0 | 0 | 1/2 | 0 | 实际Z→Y效应1/2，违反负对照暴露假设 |
| CANCELLED_INVALID_OUTCOME | 1/4 | 0 | 0 | 0 | 真A→W=−1/4但观察A-W关联0，机制抵消 |
| MISMATCHED_VALID_OUTCOME | 1/4 | 1/8 | 1/4 | 0 | 有效W共享U但偏差强度不同，不能直接相减 |

最重要的否定性反例：INSENSITIVE_VALID_CONTROLS 的A-Y观察差1/4是无真实因果效应的混杂，候选W和Z都真正满足排除限制，却因不追踪该U而未发出任何统计信号。可观察“零负对照效应”因此**无法单独证明主效应因果有效**。INVALID_OUTCOME_DIRECT_A的A-W=1/2实际来自A对W的直接效应，若不核对负对照有效性会产生假混杂警报。

本研究另外审计了一种未经桥函数/比例识别的简单校正 `D_AY−D_AW`：HIDDEN_CONFOUNDED_NULL恰为0、HIDDEN_CONFOUNDED_CAUSAL恰为1/4，与真实干预效应吻合只因为该人工世界特殊同幅混杂；MISMATCHED_VALID_OUTCOME的结果为1/8，真ATE却为0。实用中必须另行论证代理、排除、负对照敏感性与偏差映射，不能用特例校正成功证明一般识别。

## 可重演证据与归档

* 原生程序：[r224_exact_negative_controls.py](r224_exact_negative_controls.py)。观察量源枚举和独立阈值积分一致，干预oracle源枚举和独立阈值积分一致。
* 八世界 [4096条完整原来源CSV](R224_ALL_4096_ORIGINAL_NEGATIVE_CONTROL_SOURCE_ATOMS.csv)、[完整Fraction结果JSON](R224_EXACT_RESULTS.json)、[SHA机器验收](R224_FINAL_MACHINE_ACCEPTANCE.json)。
* CI [run39789956712](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39789956712) 整体completed/success，Python3.11与3.12日志分别均为`Ran 60 tests`、`OK`，合计120实际测试执行；三个job均completed/success。归档job再次验证每世界512原来源全部概率和、生成键唯一性、真干预限制、结果SHA并成功永久提交数据。
* 永久数据由机器人提交 [2bcd0bd6](https://github.com/edwardsage419/Psychohistory-Research/commit/2bcd0bd6ec87c7ed7fdf634d7c04c6d5a4ad5cdb)。SHA：来源 `cdbc43e01c115c20e551fa0088fed47962ac0b5547c8d4b74e4f257f16772f38`，结果 `05e10805da980875322458c8c902764a3dc58c0eb36a3e0dd628b70806942812`。

本研究仅有限人工E1。没有验证真实人类或群体、环境中负对照选择的有效性、未测U的实际测量、跨环境可迁移条件或双负对照一般非参数识别。新增真人E2=0，真实历史E3=0。R073与PESEN v0.1保持冻结。下一真实目录条目是 **09-016 Natural Experiment Designs**，计划编号R225，之后继续全部原239目录学习，最后才进行统一分类和熔炼。
