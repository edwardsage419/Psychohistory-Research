# B轨：R193有限混合观测粗化的独立算法审计

日期：2026-10-27。状态：PASS_BOUNDED_INTERNAL_E1_DIFFERENT_ALGORITHM。先验冻结协议：protocols/R193_S_A_OBSERVATION_COARSENING_BAYES_ERROR_THIRD_METHOD_FREEZE_2026-10-27.md。

R主程序使用显式二项系数和完整有序观察序列。B程序独立从伯努利状态动态规划得到单群组PMF，再使用无序计数直方图、多项式重数求TV。B未导入R程序函数，只读取已生成的主收据进行结果比对。两算法使用同一固定人工机制，不构成外部研究团队复现。

实际核验16组条件，每组TV、Bayes错误率、S和A的PMF共64项精确字段，全部逐Fraction一致；无序直方图配置合计131项。两个预先冻结负对照均检出：将n=2观测等价错误套用于n=3会遗漏严格正TV；只观察全部成功时的n=3,m=1 TV严格小于完整计数TV。

执行脚本：research/evidence_audit/b_r193_histogram_dp_audit_20261027.py。机器收据：research/evidence_audit/B_R193_HISTOGRAM_DP_AUDIT_RECEIPT_2026-10-27.json。审计范围涵盖概率归一、粗化信息损失、群组数单调性、完整有序与无序加权等价。没有真人数据、独立预测概率校准、独立实验、历史证据或外部复现。新增E2=0，E3=0。远端CI未运行，不能将内部PASS视为CI PASS。
