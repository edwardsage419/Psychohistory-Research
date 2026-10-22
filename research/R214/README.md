# R214 回归不连续设计（09-005）：12真人工门槛世界与192原噪声来源，正式E1结题

日期2026-10-22。真实原239目录 **09-005 Regression Discontinuity Design（P1）**。**CLOSED_BOUNDED_E1_ARTIFICIAL_SHARP_RDD_DISCRETE_GRID**。

[完整科学报告](R214_SCIENTIFIC_REPORT_2026-10-22.md) · [计算前来源/模型/评分冻结](../../protocols/R214_RDD_12_WORLDS_192_ORIGINAL_NOISE_SOURCES_PRESCORE_FREEZE_2026-10-22.md) · [12世界完整结果JSON](R214_EXACT_RESULTS.json) · [192原完整独立四噪声来源CSV](R214_ALL_192_ORIGINAL_RDD_NOISE_SOURCES.csv) · [原SHA机器验收](R214_FINAL_MACHINE_ACCEPTANCE.json) · [正式结题机读收据](R214_FINAL_ACCEPTANCE_STATUS.json) · [原生Python与39单测](r214_exact_sharp_rdd.py)。

固定X=(-2,-1,1,2)、门槛0、D=1{X≥0}，人工12个真潜在结果来源模型×独立四个Rademacher±1噪声的全部16扰动可能，共192条真正有限来源。三个事先冻结的观测估计器GLOBAL、NEAREST、TWO_SIDED_LINEAR只读固定四X及实际Y，比较真结构oracle门槛处理效果tau的完整来源MSE。三个噪声方差严格为**1、2、10**。LINEAR_CAUSAL_TWO和BASELINE_STEP_FALSE_CAUSAL的四X处**所有完整观察联合分布精确一致**，但真tau分别**2和0**；无潜在结果连续性假设，观测跳跃不能唯一解释为处理因果效应。RIGHT_QUADRATIC即使未处理基线于0连续，固定四点两侧线性外推仍偏差−2；FLAT_TAU_TWO无复杂趋势时全局均值MSE1，小于两侧线性MSE10，展示人工固定网格上复杂估计未必降低MSE。该实验**没有密集门槛点**、没有McCrary密度跳跃检验，不可外推真实RDD证据。

[GitHub Actions run39740585568](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39740585568) Python3.11与3.12各39项单测共**78项测试全部成功**，第三完整12世界、192真原来源、独立Fraction方差与三文件SHA归档job也success；机器人[真正原始数据提交af59326b](https://github.com/edwardsage419/Psychohistory-Research/commit/af59326bd3990d83e94e1d490ce5e839f2d5d3ce)。

人工数学E1有界方法研究，新增真人E2=0、真实历史E3=0；R073/PESEN v0.1冻结。下一真实原目录 **09-006 Difference in Differences**，研究编号拟R215。完成全部原R系列后统一分类，最后熔炼。
