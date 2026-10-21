# R188 多层线性模型：180人工层级世界的组内、组间与准去均值数学

日期2026-10-21，原239目录P0/08-012 Multilevel Linear Models。正式状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_MULTILEVEL_LINEAR**。

[事前冻结协议](../../protocols/R188_MULTILEVEL_90_WORLDS_4320_ROWS_PRESCORE_FREEZE_2026-10-21.md)最初固定3种六群组暴露设计×2截距×2真组内斜率×5群体背景效应×3残差幅度，原文件误算为90世界。[独立计算前数量更正](../../protocols/R188_PRE_SCORE_FACTORIAL_ARITHMETIC_ERRATUM_2026-10-21.md)在正式结果前透明更正真实乘积为**180个人工世界**，每世界6组×8行共**8640条原始人工观察**，4个准去均值参数θ产生**720条完全有理数层级系数敏感性计算**。保留初次GitHub Actions失败记录 `39565973693` 及原冻结提交历史，科学因子组合、全部代数预测和R研究优先级均未变动，也未选择性删除参数组合。

全部人工响应源为`y=a+b*x+c*xbar_g+eps`，研究分别从个体合并回归、独立两算法组内FE、组间均值回归、带xbar的上下文回归及θ∈{0,1/2,3/4,1}的准去均值计算真实人工分层条件与估计。强群组构成(2,2,2,6,6,6)、源真组内b=1/4、群组c=−4时，直接合并OLS系数**−3/4**，θ=1/2系数**−3/52**，θ=3/4系数**33/196**，完整组内FE为**+1/4**，组间回归为**−15/4**。全180世界有**36个合并回归负斜率、组内真斜率仍为正**。BALANCED源之间没有群构成变动时，组间及上下文系数明确标记不可识别，全部θ斜率均是b。

**识别负对照：** 在允许自由组截距u_g时，`y=a+b*x+c*xbar_g+eps`与`y=a+b*x+u_g+eps`（取u_g=c*xbar_g）在所有原始观察逐行完全一样。人工源真c已知仅因程序构造，观察资料若没有额外结构约束无法识别自由组截距与上下文效应是否不同。固定θ的中间斜率属于代数敏感性计算，不是一般随机截距模型方差组件拟合。

[正式科学报告](R188_SCIENTIFIC_REPORT_2026-10-21.md)、[全部180世界结果JSON](R188_EXACT_RESULTS.json)、[8640行完整人工群组记录](R188_ALL_8640_HIERARCHICAL_ARTIFICIAL_ROWS.csv)、[最终机器验收](R188_FINAL_MACHINE_ACCEPTANCE.json)、[原生代码与31种单测](r188_exact_multilevel_linear.py)、[同时包含原协议和更正的六文件ZIP](R188_180_Exact_Multilevel_Linear_Worlds.zip)已归档。[GitHub Actions39566340477](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39566340477) Python3.11和3.12各31种单元测试合计62次，第三job完整所有180世界/8640行/720数学拟合及归档SHA，三job全部success；[真实数据结果归档提交e31e31f](https://github.com/edwardsage419/Psychohistory-Research/commit/e31e31f703da88b04740c8cd345feb374752d9f0)。

理论来源：[Mundlak1978](https://doi.org/10.2307/1913646)、[Laird/Ware1982](https://pubmed.ncbi.nlm.nih.gov/7168798/)、[Bell/Jones2015](https://doi.org/10.1017/psrm.2014.7)。只达人工E1，E2/E3新增0，R073与PESEN v0.1始终冻结。下一R189 P1/08-013 Multilevel Generalized Linear Models；仍坚持原全部R系列完成后再统一归纳分类，最后熔炼。
