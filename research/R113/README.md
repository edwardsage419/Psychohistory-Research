# R113：经验预期、规范预期与社会规范测量的限定学习

日期：2026-10-19（Asia/Taipei）。对应原有239候选知识目录 **P0 / 03-007 Empirical and Normative Expectations**。独立R研究编号R113。**正式科研状态：CLOSED_BOUNDED_FIRST_PARTY_CONCEPTS_PUBLISHED_AGGREGATE_AND_SYNTHETIC_IDENTIFIABILITY；限定学习完成，真人原微观E2=0；PESEN v0.1与R073维持冻结。**

## 一手来源及阅读范围

- [Bicchieri, Lindemans & Jiang (2014), 原作者开放方法研究](https://doi.org/10.3389/fpsyg.2014.01418)，原文Table 1、Table 2、Table 3；本轮真实核读原正式开放文章。
- [Bicchieri (2017) *Norms in the Wild*, Chapter 2](https://doi.org/10.1093/acprof:oso/9780190622046.003.0002)，出版方摘要限定，未读需授权章全文。
- [Bicchieri & Xiao (2009) 发表论文](https://doi.org/10.1002/bdm.621)，出版方摘要和2014原作者回顾实验信息，不曾取得2009原逐人行为数据。

## 机制及证据

2014作者Table 1将个人规范信念、关于他人行为的经验预期、关于他人应该如何的规范预期，与非社会事实信念分类区分。规范存在诊断还要检验选择是否随社会预期变化，不能从相同群体行为推定社会规范机制。

原作者2014已公开Table 2三选项：真实行为44/12/44%，回应者经验预期44/28/28%，回应者个人规范信念100/22/52%，提议者规范预期100/10/79%。本轮**只重算作者已发表汇总表的算术**：经验减行为0/+16/−16个百分点，规范预期减个人规范信念0/−12/+27个百分点。后两类属于允许多选的公平性判断，合计174%、189%，**不能当作互斥选项概率归一化**。未接触作者2013原逐人实验数据，未重新估计真人效应。

本研究另有明确标为**非作者原模型**的教学反例：一种行为独立于社会预期，一种行为依赖经验和规范预期，但两世界观察到EE=NE=0.8时选择完全相同。将两个预期改变到0.2，前者行动不变，后者行动改变；由此证明单一情境下的观察行为不足以识别机制。此反例为纯合成，不构成真实实验干预、社会心理因果或实证证据。

## 运行核验和正式档案

GitHub Actions [39234703188](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39234703188) 成功，25项真正执行的标准库数学、已发表汇总算术与合成识别反例单元测试全通过。机器结果与代码/报告SHA256已自动提交 [R113 第一手公开汇总及合成验收机读收据](R113_PHASE_A_AGGREGATE_AND_SYNTHETIC_VERIFIED_ACCEPTANCE.json)。

- [冻结原始问题、文献范围、Table 2 数字和边界](../../protocols/R113_EMPIRICAL_NORMATIVE_EXPECTATIONS_FIRST_PARTY_MEASUREMENT_AND_SYNTHETIC_IDENTIFIABILITY_FREEZE_2026-10-19.md)
- [机制学习、汇总表复核及研究报告](R113_FIRST_PARTY_BICCHIERI_SOCIAL_EXPECTATIONS_BOUNDED_MECHANISM_SCIENTIFIC_REPORT_2026-10-19.md)
- [源公开汇总算术与合成反例的计算程序](r113_social_norm_expectations_identifiability.py)
- [25项独立单元测试](test_r113_social_norm_expectations_identifiability.py)
- [正式状态](R113_FINAL_ACCEPTANCE_STATUS.json)
- [实际机器验收收据](R113_PHASE_A_AGGREGATE_AND_SYNTHETIC_VERIFIED_ACCEPTANCE.json)

复算：Python 3.11标准库，在仓库根运行 `PYTHONPATH=research/R113 python -m unittest -v research/R113/test_r113_social_norm_expectations_identifiability.py`。不需要原始真人数据，不联网，不宣称新的原行为复验或因果研究。后续沿原R系列其他尚未验收模型学习继续，所有R系列学完后才系统归类和融合。
