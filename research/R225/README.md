# R225 自然实验设计（09-016）：六人工配额世界576原来源E1正式结题

日期2026-10-22。真实239目录 `09-016 Natural Experiment Designs`（P1），科学结论限定 `CLOSED_BOUNDED_E1_FINITE_ARTIFICIAL_NATURAL_EXPERIMENT_DESIGNS`。无真人E2或历史E3新增。

[独立预冻结协议](../../protocols/R225_NATURAL_EXPERIMENT_6_WORLDS_576_ORIGINAL_SOURCE_PRESCORE_FREEZE_2026-10-22.md) · [完整科学报告](R225_SCIENTIFIC_REPORT_2026-10-22.md) · [完整576原来源CSV](R225_ALL_576_ORIGINAL_NATURAL_ASSIGNMENT_SOURCES.csv) · [原生Python](r225_exact_natural_experiment.py) · [六人工世界精确Fraction结果](R225_EXACT_RESULTS.json) · [原SHA机器验收](R225_FINAL_MACHINE_ACCEPTANCE.json) · [最终有界科研验收](R225_FINAL_ACCEPTANCE_STATUS.json)。

预设四单位、任意恰好两个处理的六种分配、16种完整四人独立后期Rademacher冲击，六世界×96来源=576条完整原源。**外生自然配额真实处理效果1**与**内生潜在未来冲击导致的零处理效果**两个世界具有完全相同可观察`(Z四向量,pre四向量,post四向量)`分布，且前期平衡值均0、DiD期望均1。这限制了单靠外部安排和平衡安慰剂建立“近似随机”的能力。可见选择、提前响应、异质真ATE单列独立反例。

首次[CI run39791326559](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39791326559)因将观察等价世界的真实偏差/MSE误要求相同，归档验收断言失败；两Python单测均success。此错误仅修复于[提交73be44a0](https://github.com/edwardsage419/Psychohistory-Research/commit/73be44a093c671e61f166d35dcbb0d255ef37051)，保持来源结构、科学机制、预先冻结统计不变。正式[CI run39791457285](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39791457285)三作业全部success，Python3.11/3.12各43 tests合计86次，永久原资料提交[a60f4d6f](https://github.com/edwardsage419/Psychohistory-Research/commit/a60f4d6fc658b65f596469d346a3df2d54585311)。

R073与PESEN v0.1保持冻结。下一实际原目录：`09-017 Selection versus Influence Identification`，拟R226。全R先完成，后归纳分类，再进行模型熔炼。
