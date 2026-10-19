# R114：条件性规范遵从与经验/规范预期冲突的数学识别

日期：2026-10-19（Asia/Taipei）。知识目录既定 P0 条目 03-008 Conditional Norm Compliance；R114 为独立研究归档编号。**CLOSED_BOUNDED_PRIMARY_SOURCE_SCOPE_AND_SYNTHETIC_FACTORIAL_IDENTIFICATION；LEARNING_COMPLETE_BOUNDED_PRIMARY_ABSTRACT_AND_MATHEMATICAL_IDENTIFIABILITY；真人原逐人行为E2=0。**

## 一手来源、结果与限制

1. [Bicchieri & Xiao (2009)，原出版方](https://doi.org/10.1002/bdm.621)、[宾夕法尼亚大学作者所属中心原论文网页](https://normsandbehavior.sas.upenn.edu/publication/do-right-thing-only-if-others-do-so)：开放**摘要**报告，在2009年独裁者实验中预期冲突时经验预期显著预测分配，控制其后规范预期额外预测不显著。未取得需授权全文、原2009逐人数据、原拟合参数和显著性原表；2008年online first/2009正式卷期属同一文章，不重复算独立来源。
2. [Bicchieri, Lindemans & Jiang (2014) 原作者全文](https://doi.org/10.3389/fpsyg.2014.01418)：开放原文明确指出规范类型要分经验预期、规范预期、参考人群和有条件的偏好；仅依赖经验预期的集体行为可对应描述性规范，不能仅凭共同动作宣布社会规范存在。

## 数学计算（自构教学机制，不是作者拟合模型）

四格 E,N∈{0,1} 均为人为低/高状态，合成概率由 logit P(A)=α+β_E E+β_N N+β_EN E N。冻结四组参数：DESCRIPTIVE=(-1,2,0,0)、NORMATIVE_ONLY=(-1,0,2,0)、BOTH_ADDITIVE=(-1,1,1,0)、INTERACTION=(-1,1,1,1)。

前两种机制在**E=N一致条件**p00≈0.26894，p11≈0.73106完全一样；在E1N0与E0N1冲突格出现相反方向，因此仅有一致条件时观察上不可识别经验还是规范预期为主要驱动。四格均存在且p严格在(0,1)时，可数学解出包括相互作用β_EN在内的四个logit参数，缺失一格不能自由识别四参数。BOTH_ADDITIVE说明两种预期都有关联不要求乘积交互非零；INTERACTION说明额外乘积交互不自动证明实际社会规范因果。

原研究与本模拟完全区分：R114没有任何真人个体原实验数据或拟合，没有真实规范因果E2；需要确证真实参考群体、信息可得性、实测预期、合法对照、选择/退出机制和实验分配才有进一步研究资格。R073/PESEN v0.1保持冻结。

## 正式测试与档案

GitHub Actions [run 39236924459](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39236924459) **success，30项纯合成测试通过、0项失败**，真实机读SHA收据已由CI提交并回读。

- [预冻结第一手来源及四格设计](../../protocols/R114_CONDITIONAL_NORM_COMPLIANCE_FIRSTPARTY_SOURCE_AND_DISCORDANT_EXPECTATIONS_SYNTHETIC_FREEZE_2026-10-19.md)
- [一手范围、推导与反例正式科学报告](R114_BICCHIERI_XIAO_CONDITIONAL_NORM_COMPLIANCE_AND_FACTORIAL_IDENTIFIABILITY_SCIENTIFIC_REPORT_2026-10-19.md)
- [数学程序](r114_conditional_norm_compliance_discordant_expectations.py)
- [30项数学合成测试](test_r114_conditional_norm_compliance_discordant_expectations.py)
- [自动运行与SHA机读收据](R114_PHASE_A_30_SYNTHETIC_NORM_EXPECTATION_CI_ACCEPTANCE.json)
- [正式科研验收](R114_FINAL_ACCEPTANCE_STATUS.json)

在仓库根执行：`PYTHONPATH=research/R114 python -m unittest -v research/R114/test_r114_conditional_norm_compliance_discordant_expectations.py`。

此项有界研究完成后继续原R系列候选；不提前将全部239项模型统一分类，不启动原创PESEN模型熔炼或个人决策体系。
