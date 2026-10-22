# R215 双重差分（09-006）已完成：12个真实人工源世界与3264面板原来源

2026-10-22。原239模型目录 **09-006 Difference in Differences（P1）**，正式状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_TWO_PERIOD_DID**。

[原冻结两期DiD源协议](../../protocols/R215_DID_12_WORLDS_3264_EXACT_NOISE_SOURCES_PRESCORE_FREEZE_2026-10-22.md) · [正式科学报告](R215_SCIENTIFIC_REPORT_2026-10-22.md) · [24世界噪声结果JSON](R215_EXACT_RESULTS.json) · [3264完整原人工四单位面板来源CSV](R215_ALL_3264_ORIGINAL_PANEL_NOISE_SOURCES.csv) · [真实SHA和数量机读验收](R215_FINAL_MACHINE_ACCEPTANCE.json) · [正式结题收据](R215_FINAL_ACCEPTANCE_STATUS.json) · [纯Python、35项单测](r215_exact_did_panel.py)。

四个人工单位（处理组2、3；对照组0、1）、两期t0/t1、12个预冻人工政策世界、两种原噪声：每个单位期独立±1有2^8=256原来源，单个单位两期完全持久±1有2^4=16原来源，共12×272=3264完整面板来源。逐原来源评估只能读实际8个观测的DiD及POST_ONLY，真无政策潜在结果、ATT只供人工审计；全部源概率归一与MSE=Bias²+Var精确Fraction双路核对。

最关键反例：世界`VALID_CONSTANT_TWO`真ATT2，世界`SIMULTANEOUS_TREATED_SHOCK_NO_CAUSAL`真目标政策ATT0且存在+2外部同时间冲击，但**全部四人两期观察结果对每条原噪声源逐条完全相同、观察联合分布完全一致**；仅凭这套观察数据无法确定哪个是政策因果作用。真处理效应2时，处理组自然无政策趋势快2可导致DiD期望4；控制组+1溢出或处理组提前+1预期使真ATT2只被DiD估计为1。两期各单位独立噪声下DiD真方差2，单位内持久噪声下可完全差消，真方差0；这不能推广到现实多期统计标准误。

最终[GitHub Actions run39741076513](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39741076513) Python3.11与3.12各35单测共70通过，第三真实全部原面板资料与SHA归档成功；[GitHub机器人全部原来源提交1e58b4f6](https://github.com/edwardsage419/Psychohistory-Research/commit/1e58b4f67edb5155d5fab56c362b60d34d1321bb)。第一次CI因生成器均值辅助报错，随后只修复代码实现，不修改冻结世界、预测规则与评分。

仅自造数学E1，新增真人E2=0、真实历史E3=0；R073及PESEN v0.1冻结。下一真实239目录为 **09-007 Event Study Design（R216）**，仍按全原R模型完成后统一分类，最后熔炼。


## R215-3P 三期补充研究（不取代以上正式R215）

2026-10-22另有已先行计算前冻结的[三期补充人工协议](../../protocols/R215_DID_12_WORLDS_768_ORIGINAL_GROUP_TIME_SHOCKS_PRESCORE_FREEZE_2026-10-22.md)。该补充仅添加一项**处理前趋势诊断与三期外推的有限人工机制审计**，不改变本目录原两期研究和`R215_EXACT_RESULTS.json`、`R215_FINAL_ACCEPTANCE_STATUS.json`以及3264条正式原资料。

[三期补充独立科学报告](R215_3P_SUPPLEMENT_SCIENTIFIC_REPORT_2026-10-22.md) · [补充12人工世界结果](R215_3P_EXACT_RESULTS.json) · [768条完整原组六组时段噪声来源](R215_ALL_768_ORIGINAL_GROUP_TIME_SHOCK_PANELS.csv) · [补充独立机器SHA](R215_3P_FINAL_MACHINE_ACCEPTANCE.json) · [补充结题机器收据](R215_3P_FINAL_ACCEPTANCE_STATUS.json) · [补充程序及40项单测](r215_exact_three_period_did.py) · [最终GitHub Actions run39741554338](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39741554338)。

三期人工世界中PARALLEL_TAU_TWO真ATT2、POST_SHOCK_FALSE真ATT0与POST_SHOCK_WITH_TAU_MINUS_ONE真ATT−1，**完整三期两组实际观察联合分布完全相同**，处理前placebo期望均为0却真实因果不同；证明固定人工世界中**pre-trend为零不能单独验证政策后反事实平行趋势**。六组时段独立±1噪声下普通DID/pretrend诊断噪声方差各4、三期线性校正方差12，补充校正在稳定不同斜率时消除偏差但可能放大MSE，遇到t0提前反应也可能更差。双Python各40测试总80通过，三CI job success，[768条补充原数据机器人提交6f2a2d89](https://github.com/edwardsage419/Psychohistory-Research/commit/6f2a2d89a9d2060e25420a5679502473e64e7957)。

**R215-3P=独立E1有限补充研究，不新增原239目录已完成条目数量、不覆盖原R215证据。** E2=E3=0，R073/PESEN v0.1冻结。原目录下一条仍09-007 Event Study Design（R216）。
