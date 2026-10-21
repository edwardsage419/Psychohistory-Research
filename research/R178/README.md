# R178 最大似然估计：错误独立假设下的30组有限样本精确研究

2026-10-21。原候选目录P0/08-002 Maximum Likelihood Estimation。正式状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_FINITE_MLE**。

本研究以原R177冻结源码Git blob `2d032513ce84141214b6b3f84df9c0ed9976a02b` 和完整计数结果SHA256 `57410cf2c110ce3117b7af72e4b7473cee0c3ffd013e6fb99fd43de62165a535` 作为完全固定的人工生成世界，依[事前冻结协议](../../protocols/R178_MLE_30_FINITE_SAMPLE_COUNT_WORLDS_PRESCORE_FREEZE_2026-10-21.md)计算3种样本量×2种真边际概率×5类数据生成过程，**30组270个原始计数支持单元**的精确最大似然估计风险。

在全部30种机制中，Bernoulli似然MLE k/n对边际p都严格无偏。然而错误独立性假设下的真实MSE可高于IID理论方差。固定n=8、p=1/4时，独立/强群内相关/弱群内相关/结构零1/8/结构零1/4对应真实MSE倍数1、10/3、16/9、4/3、16/9；名义95%双侧Wald区间的真实覆盖分别为87.26%、46.55%、71.61%、77.41%、65.48%。**无平滑MLE在所有30种人工有限样本世界中出现边界估计的概率均大于0，故在另一个独立边际Bernoulli(p)测试事件上的无条件期望负对数损失为正无穷**；另设固定Laplace平滑估计获得有限的数值分数并经过独立Decimal高精度核验。

[正式科研报告](R178_SCIENTIFIC_REPORT_2026-10-21.md)、[30世界完整结果JSON](R178_EXACT_RESULTS.json)、[机器验收](R178_FINAL_MACHINE_ACCEPTANCE.json)、[完整源码与25种测试](r178_finite_sample_mle_exact_risk.py)、[固定源码协议结果ZIP](R178_MLE_30_Finite_Count_Sample_Worlds_Exact_Audit.zip)永久入库。[GitHub Actions39554622255](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39554622255) Python3.11和3.12分别25种单测，共50次真实执行，加完整30世界第三job三job均success；[实际归档提交be0319c](https://github.com/edwardsage419/Psychohistory-Research/commit/be0319caae83c40e862205ffe3d46a96ccc0bd1f)。

引用[NIST二项MLE](https://www.itl.nist.gov/div898/handbook/eda/section3/eda366i.htm)、[Brown/Cai/DasGupta 2001比例区间](https://doi.org/10.1214/ss/1009213286)、[NIST Beta二项分布](https://www.itl.nist.gov/div898/software/dataplot/refman2/auxillar/bbnpdf.htm)。限于人工E1解析结果，没有真实人类行为与历史数据检验，新增E2/E3均0；R073和PESEN v0.1冻结。下一R179 P0/08-003 Bayesian Posterior Inference；完成所有R系列以后再分类，最后熔炼。
