# R184 泊松回归：45组有限人工计数来源的真实离散度与测试风险

日期2026-10-21，原候选模型P1/08-008 Poisson Regression。科研状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_POISSON_GLM**。

[事前冻结协议](../../protocols/R184_POISSON_GLM_45_WORLDS_PRESCORE_FREEZE_2026-10-21.md)先于程序评分入库，严格沿用R177固定SHA的一手人工计数概率源，3种n×3组真边际概率对×5种计数机制，完整45人工世界、4125原始人工训练计数对。两种独立数学算法检验真实计数源方差与Poisson工作似然极大值的存在性；每个世界真实训练样本概率全穷举，未来另外独立计数事件的平方风险与Poisson对数评分分别独立复核。

**最重要反例**：在n=8，p0=p1=1/4的人工世界，ZIB结构零1/8的数据计数均值为2、方差为2，故泊松离散比Var/Mean恰好为1；但真实零事件概率**18.429%**，显著不同于Poisson(2)的**13.534%**。因此即使一二阶矩满足泊松模型，也不保证真正生成分布为泊松。组内相关强时，离散比可以达到2.5，真实零事件概率达37.094%。

固定Poisson log链接工作MLE`λhat=K`，所有45世界均因零计数训练有正概率，面对独立未来正计数测试的无条件Poisson预测logloss为正无穷。固定改为`λ=K+1/2`后未来logloss有限，但未来原始计数平方误差**在全部45世界都严格增加1/4**；这属于两个评分标准之间的人工模型取舍，不宣称平滑全面优越。

[完整科研报告](R184_SCIENTIFIC_REPORT_2026-10-21.md)、[45世界全部结果JSON](R184_EXACT_RESULTS.json)、[4125原始样本CSV](R184_ALL_4125_ARTIFICIAL_TRAINING_COUNT_PAIRS.csv)、[机器验收](R184_FINAL_MACHINE_ACCEPTANCE.json)、[完整源码和25种单测](r184_poisson_count_glm_exact.py)、[源码协议及结果ZIP](R184_Exact_Poisson_45_Worlds_Source_Audit.zip)已归档。[GitHub Actions39562030829](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39562030829) 双Python各25单测共50次及第三job全部45世界实际评估三job全success。[完整结果提交e0213c1](https://github.com/edwardsage419/Psychohistory-Research/commit/e0213c1d4f2a36280b2df726d96bca50e9ffed67)。

原始来源：[Nelder/Wedderburn1972](https://doi.org/10.2307/2344614)、[Cameron/Trivedi2013](https://doi.org/10.1017/CBO9781139013567)。仅人工E1，E2/E3新增0，R073与PESEN v0.1冻结。下一R185 P1/08-009 Negative Binomial Regression。全部R研究后统一归纳分类，再模型熔炼。
