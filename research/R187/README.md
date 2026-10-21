# R187 有序逻辑回归：12个人工世界中的比例优势假设及截点效应交叉

日期2026-10-21。原239候选目录P1/08-011 Ordinal Logistic Regression。正式状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_ORDINAL_LOGIT**。

[评分前冻结协议](../../protocols/R187_ORDINAL_PO_12_WORLDS_1950_TABLES_PRESCORE_FREEZE_2026-10-21.md)固定三等级结果Y∈{0,1,2}、两个解释组别与各组m=3/4个独立人工观察，六种已知累计赔率生成机制共**12个人工世界**、**1950个完整真实人工训练计数表**，以及**325个唯一训练表拟合profile**。比较共享阈值赔率倍率的40个PO候选，与拥有不同阈值倍率、严格包含PO的125个合法NONPO候选；两套独立Fraction公式重建完整类别概率，两套不同的训练概率乘法方式逐项验收有限网格最大似然，独立新等级测试logloss由float/Decimal双通道核对。

预冻结最重要数学反例：在CROSSED_THRESHOLDS源中，组别x=0的三级概率为(1/5,3/5,1/5)，x=1为(1/3,1/3,1/3)。因而P(Y≤0)随x上升增加2/15，而P(Y≤1)下降2/15；两个累计赔率比率分别为2和1/2，**共同的比例优势斜率数学上无法同时代表两个方向相反的阈值效应**。在m=4完整来源训练样本预期独立测试logloss上，PO为1.156010，NONPO为1.145730；但是NULL零真实组别差异条件下，PO为1.204374、NONPO为1.224308，说明更自由的模型在某些模型错误指定情景改善预测，也能因有限数据而过拟合。没有真实人类等级结果或因果证据。

[完整正式科研报告](R187_SCIENTIFIC_REPORT_2026-10-21.md)、[12世界结果JSON](R187_EXACT_RESULTS.json)、[1950完整原始计数表CSV](R187_ALL_1950_ORDINAL_TRAINING_TABLES.csv)、[325两模型完整拟合库](R187_ALL_325_ORDINAL_FIT_PROFILES.json)、[正式机器验收](R187_FINAL_MACHINE_ACCEPTANCE.json)、[完整程序及29种单测](r187_exact_ordinal_logit.py)、[源码协议数据与结果ZIP](R187_Exact_Ordinal_PO_12_Worlds_Archive.zip)均永久归档。[GitHub Actions39565081700](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39565081700) Python3.11/3.12各29项合计58次单测及第三job完整源评分和归档三job success，[正式数据归档6b35a56](https://github.com/edwardsage419/Psychohistory-Research/commit/6b35a564fc79c18ffcb0589b0af91a21065ec9db)。

文献：[McCullagh1980](https://doi.org/10.1111/j.2517-6161.1980.tb01109.x)、[Brant1990](https://doi.org/10.2307/2532457)。本轮只有E1人工有限计数研究，E2/E3新增0，R073与PESEN v0.1冻结。下一 **R188 P0/08-012 Multilevel Linear Models（多层线性模型）**，严格按原R序列继续，完成后再统一归纳分类、最后熔炼。
