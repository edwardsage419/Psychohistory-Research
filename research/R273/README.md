# R273 跨群体验证（12-003，P0）

科研状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_CROSS_POPULATION_TRANSFER**。九种源群体a与目标群体b概率组合×三固定预测器，共27个人工world。每world由源四训练bit与目标两独立测试bit组成64完整原source，合计1728个带模型标识原配置，严格不等于真人或独立研究样本。

[事前冻结](../../protocols/R273_CROSS_POPULATION_27_WORLDS_1728_COMPLETE_SOURCES_PRESCORE_FREEZE_2026-10-23.md) · [可运行标准库源码](r273_exact_cross_population_prediction.py) · [全1728原source CSV](R273_ALL_1728_ORIGINAL_CROSS_POPULATION_SOURCES.csv) · [27世界完整风险结果JSON](R273_EXACT_CROSS_POPULATION_RESULTS.json) · [机器SHA凭证](R273_MACHINE_RECEIPT.json) · [正式科研报告](R273_SCIENTIFIC_REPORT_2026-10-23.md) · [有界正式验收](R273_FINAL_ACCEPTANCE_STATUS.json)。

群体源p=1/4、目标p=3/4时，SOURCE_ORACLE未来Brier 7/16，SOURCE_LAPLACE未来Brier 55/144，TARGET_ORACLE理论下界3/16。SOURCE_ORACLE与TARGET_ORACLE使用外部真概率，只提供数学比较基线，后者尤其不能当成可实施的源群体拟合模型。完整原来源和独立解析Binomial方法27world全部Fraction一致。

[GitHub Actions run39903300167](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39903300167)全部三job completed/success，Python3.11及3.12各172项真实测试共344通过，第三独立原来源审核、原CSV/JSON/SHA永久归档[1d57f507](https://github.com/edwardsage419/Psychohistory-Research/commit/1d57f5078d172d1feb4b6a07a68e8732c102edf6)。

新增真人E2与历史E3均0，R073/PESEN v0.1冻结；下一原目录12-004 Temporal Holdout Validation（拟R274）。先全R学习后统一分类，最后熔炼。
