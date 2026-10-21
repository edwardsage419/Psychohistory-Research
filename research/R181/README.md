# R181 置换检验：群组随机分配和错误逐条事件置换的精确对照

2026-10-21。原239候选目录P0/08-005 Permutation Test，正式状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_RANDOMIZATION**。

[计算前冻结协议](../../protocols/R181_EXACT_SIX_CLUSTER_RANDOMIZATION_42000_PROFILES_PRESCORE_FREEZE_2026-10-21.md)严格指定六个互相独立群组，每组有四次可能相关的二元事件，三个群组随机赋值处理，剩余三个对照。原R177固定SHA来源的五种计数机制×两个事件真概率构成10个零效应人工世界。源资料有序计数样本共5^6=15625种，使用210个无序profile与真实排列权重精确保存全概率；每profile计算C(6,3)=20种真正群组随机分配，全部**42,000条真实来源加权随机分配评价记录**。

**冻结主要结果：** 当p=1/2且组内强相关Beta二项浓度2时，名义10%的正确六群组Fisher双侧精确检验实际误报率为**5.6576%**，错误地把24条组内观察按个体随机重赋标签的误报率达到**20.1984%**。在固定反例群组计数(0,0,0,0,4,4)、实际处理组三群组包含两组各4次成功时，正确群组p=2/5=0.4，错误逐事件p=10/7429≈0.001346。两种真实群组置换算法、两种错误逐事件置换算法独立Fraction逐概率一致，正确组层sharp null在所有210 profile与两个阈值下均不超过名义误报水平。

[正式科学报告](R181_SCIENTIFIC_REPORT_2026-10-21.md)、[10人工生成世界全量结果](R181_EXACT_RESULTS.json)、[210种完整随机化条件分布库](R181_ALL_210_RANDOMIZATION_PROFILES.json)、[42,000条带权评价CSV](R181_ALL_42000_SOURCE_WEIGHTED_ASSIGNMENTS.csv)、[机器科研验收](R181_FINAL_MACHINE_ACCEPTANCE.json)、[源码与28项单测](r181_six_cluster_exact_randomization.py)、[完整源码结果及协议ZIP](R181_Six_Cluster_Exact_Randomization_42000_Assignments.zip)已归档。[GitHub Actions39558955703](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39558955703) Python3.11/3.12各28单测、共56次执行与独立实际计算/归档三job全success，[永久档案提交40d07a3](https://github.com/edwardsage419/Psychohistory-Research/commit/40d07a38fb61a476d360575b830f7b431d08e83d)。

原始统计来源：[Fisher1935](https://books.google.com/books/about/The_Design_of_Experiments.html?id=-EsNAQAAIAAJ)、[Imbens/Rubin2015](https://www.cambridge.org/core/books/abs/causal-inference-for-statistics-social-and-biomedical-sciences/fishers-exact-pvalues-for-completely-randomized-experiments/23AF990D2EF9C90D0A424D555FACE578)。仅有人工sharp null E1数学证明，没有任何真实心理、社会实验或历史因果效果推断；新增E2/E3均0。R073/PESEN v0.1不变。下一R182 P0/08-006 Linear Regression，继续原R研究目录，完成后统一分类，最后熔炼。
