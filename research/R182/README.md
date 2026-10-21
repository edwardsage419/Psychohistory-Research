# R182 线性回归：240个人工分层数据的完整最小二乘与遗漏变量反转

日期2026-10-21。原研究目录P0/08-006 Linear Regression，正式状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_OLS**。

本轮[计算前冻结协议](../../protocols/R182_OLS_FWL_240_WORLDS_PRESCORE_FREEZE_2026-10-21.md)固定四种二元x,z联合细胞配比×两种人工截距×两种真正向x斜率×五种组别z效应×三种对称残差幅度，构成**240个完整人工线性回归世界、2880条原始人工观测**。各世界先从原数据建立法方程以Fraction做Gauss Jordan消元，再独立使用Frisch Waugh Lovell双向残差化恢复完整系数，两个算法在全部240世界严格分数一致。模型拟合残差在截距、x、z上均精确正交，SSE恒等式和设计矩阵奇异拦截均通过。

**关键正反例：** 在联合细胞人数(6,2,2,6)，人工真结构斜率b=+1/4、z效应c=−2、对称噪声幅度e=1/4条件下，遗漏z的简单回归x系数为**−3/4**、SSE=13，而包含z的完整回归x系数为**+1/4**、SSE=1。同一个人工固定全量样本因为遗漏变量和分层选择相关而发生方向反转。全部240世界中共**54组**简单回归负斜率而完整模型真系数仍正，独立分层设计或零z效应的负对照没有反转。该数学模型没有真实社会因果识别能力。

[正式科研报告](R182_SCIENTIFIC_REPORT_2026-10-21.md)、[240完整世界结果JSON](R182_EXACT_RESULTS.json)、[2880行原始人工CSV](R182_ALL_2880_ARTIFICIAL_OBSERVATIONS.csv)、[机器科研验收JSON](R182_FINAL_MACHINE_ACCEPTANCE.json)、[双独立数学程序及27项测试](r182_exact_ols_fwl_omitted_variable.py)、[完整源码协议与实验结果ZIP](R182_Exact_240_OLS_FWL_Worlds.zip)已永久归档。[GitHub Actions39559935431](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39559935431) Python3.11/3.12各27种单测共54次执行、加完整240世界计算归档三job全success，[正式数据归档提交9f2aabe](https://github.com/edwardsage419/Psychohistory-Research/commit/9f2aabe4207fc766427ce38397222440be57fd8a)。

理论源文献：[Frisch/Waugh1933](https://doi.org/10.2307/1907330)、[Lovell1963](https://doi.org/10.1080/01621459.1963.10480682)、[Simpson1951](https://doi.org/10.1111/j.2517-6161.1951.tb00088.x)。本研究只取得E1人工精确回归结果，新增真人E2与外部历史E3均0，R073与PESEN v0.1仍冻结。下一R183经原239目录核实为 **P0/08-007 Logistic Regression（逻辑回归）**，继续既定R系列完成后再统一归纳分类，最后熔炼。
