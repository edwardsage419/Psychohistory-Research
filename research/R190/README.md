# R190 广义加性模型：10个五位置人工曲线与5500次精确平滑拟合

日期2026-10-21。原目录P1/08-014 Generalized Additive Models。正式状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_DISCRETE_GAM**。

[事前冻结协议](../../protocols/R190_DISCRETE_GAM_10_WORLDS_1375_TABLES_PRESCORE_FREEZE_2026-10-21.md)固定五个有序解释位置、每位置n=1/2个独立训练二值±1响应，FLAT、LINEAR、HUMP、VALLEY、ALTERNATE五种人工源形状，组成**10个人工世界与1375张完整人工训练计数表**。四档二阶差分曲率惩罚λ=0、1、4、16，共**5500次有理数受罚平滑拟合**。使用5×5正规方程与独立3×3对偶公式、第三条平滑矩阵映射，三路对每完整训练表的预测逐Fraction相等。所有训练输入的人工来源PMF由封闭二项公式及独立事件DP全部一致。未来独立新观察均方风险由全部训练联合概率枚举与独立的平滑矩阵偏差方差公式逐Fraction严格一致，保留8套完整5×5平滑矩阵与所有训练表风险。

**预冻结正反例**：每位置n=2时，真FLAT曲线λ0未来MSE1.500000、λ16为1.201815，真LINEAR曲线λ0=1.312500、λ16=1.042804；两者二阶差分为0，加强平滑可降训练预测方差。真HUMP曲线λ1=1.080380优于λ16=1.123571；高频交替ALTERNATE曲线λ1=1.092310、λ16=1.126078，强平滑甚至劣于零平滑λ0=1.125000。全体10源×4档已冻结计算结果全保留，所有比较仅人工identity-link单项离散平滑，不代表一般二元GLM/GAM概率模型已复现。

[正式科学报告](R190_SCIENTIFIC_REPORT_2026-10-21.md)、[10世界全部精确风险JSON](R190_EXACT_RESULTS.json)、[1375原始表及5500次拟合CSV](R190_ALL_1375_ARTIFICIAL_SMOOTHING_TRAINING_TABLES.csv)、[8套完整Fraction平滑矩阵](R190_ALL_8_FRACTION_SMOOTHING_MATRICES.json)、[科研机器验收](R190_FINAL_MACHINE_ACCEPTANCE.json)、[原生算法与30项测试](r190_exact_discrete_gam_smoothing.py)、[全部源码协议结果ZIP](R190_Exact_10_Discrete_GAM_Smoothing_Worlds.zip)均已永久归档。[GitHub Actions39572040903](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39572040903)双Python各30单测共60次及完整源评分归档三job全success，[结果提交e1ebe06](https://github.com/edwardsage419/Psychohistory-Research/commit/e1ebe06bec39e9d24fbf215147118bad985a1380)。

主要理论：[Hastie/Tibshirani1986](https://doi.org/10.1214/ss/1177013604)、[Eilers/Marx1996](https://doi.org/10.1214/ss/1038425655)。仅人工E1，E2/E3新增0，R073与PESEN v0.1不变。下一R191 P1/08-015 Mixed Effects Models；继续完成全部既定R系列，再统一归纳分类，最后熔炼。
