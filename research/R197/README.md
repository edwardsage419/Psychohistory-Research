# R197 时间序列 ARIMA：六种固定机制的短训练与独立未来预测

日期2026-10-21，原239目录P1/08-021 ARIMA。正式状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_PREQUENTIAL_ARIMA**。

[事前冻结协议](../../protocols/R197_ARIMA_24_WORLDS_1944_TRAINING_PRESCORE_FREEZE_2026-10-21.md)锁定六种人工过程WHITE、AR1(φ1/2)、RW、DRIFT(每步+1)、DIFF_AR1(差分φ1/2)、DIFF_MA1(差分θ1/2)，各由独立创新−1/0/+1和概率1/4/1/2/1/4生成，从Y0=0启动；训练T4/5、独立未来h1/2。共有**24完整人工世界、1944条全部真实训练路径、3888套条件测试配置、23328个全六候选Fraction未来预测风险**。每条训练历史仅在t2..T按真实已经发生的历史做六候选单步prequential平方误差选模，绝不查看未来样本；由逐前缀预测器和完全独立的在线直接递推，两套Fraction训练得分全等。随后独立新创新3^h全枚举与不读取未来样本的真条件均值+解析噪声方差双数学计算，对全部23328预测风险逐Fraction相等，全部真源原训练概率严格和1。

**固定真实反例**：在真随机游走RW的短训练T5下，正确固定RW未来1步/2步oracle MSE分别1/2与1，但若在这六个给定候选之间用prequential训练误差选模型，真正未来MSE上升到≈0.67216和1.32096；真DRIFT下h2固定错误RW误差5.0，训练选模1.65516，正确真模型oracle1.0，说明模型丰富性既可能纠正错误漂移假设，也可能在训练数据过少时过拟合。真AR1虽然φ=1/2稳定、Y0固定0并不等于平稳初态。真差分AR1、MA1的未来h2理论方差均13/8，不可同真实h1风险直接比较。

[正式科研报告](R197_SCIENTIFIC_REPORT_2026-10-21.md)、[全部24世界机器结果](R197_EXACT_RESULTS.json)、[1944完整有序原训练创新/状态CSV](R197_ALL_1944_ORDERED_TRAINING_PATHS.csv)、[3888条未来配置含23328风险CSV](R197_ALL_3888_INDEPENDENT_HELDOUT_RISK_PROFILES.csv)、[最终机器验收](R197_FINAL_MACHINE_ACCEPTANCE.json)、[原生源码与37单元测试](r197_exact_prequential_arima.py)、[完整源/协议/原数据ZIP](R197_Exact_24_Prequential_ARIMA_Worlds.zip)永久归档。[GitHub Actions39588989130](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39588989130)两个Python各37单测共74次及第三job全部数学风险/两CSV/ZIP归档三项全success，[机器原结果提交d01e1a42](https://github.com/edwardsage419/Psychohistory-Research/commit/d01e1a42aa793f2037befe1d668253d540296991)。

原理论来源：[Box/Jenkins1970](https://books.google.com/books/about/Time_Series_Analysis.html?id=qsnaAAAAMAAJ)、[Box等Wiley2015](https://www.wiley.com/en-us/time-series-analysis-forecasting-and-control-5th-edition-p-9781118675021)。严格人工E1，未估计未知连续ARIMA参数、新增真人E2/历史E3=0，R073/PESEN v0.1冻结。下一 **R198 P1/08-022 State Space Models**；全部R完成后才统一归纳分类，再模型熔炼。
