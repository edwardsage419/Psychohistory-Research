# R207 Matrix Completion：126观察掩码、8064真源E1有界结题

2026-10-22。原239模型目录P2/08-031 Matrix Completion。最终科学状态**CLOSED_BOUNDED_E1_ARTIFICIAL_RANK_ONE_MATRIX_COMPLETION**。

[预先冻结方法及来源](../../protocols/R207_MATRIX_COMPLETION_126_MASKS_8064_ORIGINAL_RANK1_PRESCORE_FREEZE_2026-10-22.md) · [正式报告](R207_SCIENTIFIC_REPORT_2026-10-22.md) · [126世界JSON](R207_EXACT_RESULTS.json) · [8064原掩码×原因子来源完整CSV](R207_ALL_8064_ORIGINAL_MASK_AND_FACTOR_SOURCES.csv) · [结果机器SHA验收](R207_FINAL_MACHINE_ACCEPTANCE.json) · [完成正式结题机器收据](R207_FINAL_ACCEPTANCE_STATUS.json) · [原生Python+35单测](r207_exact_matrix_completion.py)。

自造六个{1,2}独立因子产生3×3正rank1，64条原原因子（不按相同矩阵去重）；九个元素中恰观察五个的全部C(9,5)=126种掩码，每掩码64条原来源总8064条、每条遮蔽四个同矩阵条目，共32256条精确有理数损失。全部126个观察二部图的BFS与UnionFind双法一致：81连通五边生成树、45不连通。已知真生成有限先验的posterior均值**连通Bayes隐藏均方风险0**、**不连通组平均303/640**；只观察均值填补分别为207/200与591/500。不连通在**强有限先验**下仍有7/80来源唯一补全概率，但连续正rank1空间存在两个正矩阵观测五值完全相同、四个隐藏值不同的严格反例。**不能混同结构可辨识性与正确来源先验的统计推断**，更不能把同张矩阵缺失四位置当新的独立未来个体。

[Actions run 39730928913](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39730928913) Python3.11和3.12各35项共70全成功、第三原全来源归档job success；全部实际机器原数据已[机器人提交14b790b1](https://github.com/edwardsage419/Psychohistory-Research/commit/14b790b1a2d2d81429ee67acad2fb85ec999988c)永久写回main。人工E1，新增真人E2=0、真实历史E3=0，R073与PESEN v0.1继续冻结。

下一项 **R208 P1/08-032 Network Centrality**，继续完成全部R系列后统一分类，最后熔炼。
