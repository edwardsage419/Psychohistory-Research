# R196 变分贝叶斯：已知人工后验、格点均值场ELBO与依赖丢失

2026-10-21，原目录P2/08-020 Variational Bayes。科研状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_FINITE_VARIATIONAL_BAYES**。

[事前冻结协议](../../protocols/R196_FINITE_VB_24_WORLDS_408_CANDIDATES_PRESCORE_FREEZE_2026-10-21.md)定义2个二值潜变量z1,z2等概率4状态真先验，在人工六套likelihood权重中观测m=1/2次独立正例，完整真后验`P(z|data)∝w(z)^m`及联合证据由**两条独立Fraction方法**完全一致。COARSE与FINE两个嵌套均值场格点分别含9/25组乘积Bernoulli候选，构成**24评分世界、12真来源配置、408完整候选ELBO与反向KL评分**。全部ELBO以float的真实joint+entropy公式与70位Decimal的真log-evidence减KL双数值方式核验≤1e−12，源真后验、两个潜变量真边际与协方差和工作族q的零协方差全部永久归档。

**重要反例**：UNIFORM任意m与INDEPENDENT_SKEW m1完全落在两工作网格中，KL=0；同一INDEPENDENT_SKEW m2真实潜在边际p=r=1/10，真后验依然相互独立，但最优固定网格KL COARSE≈0.184663、FINE≈0.006487，说明非零误差可以只来自有限网格。POSITIVE_COUPLED m2真实后验`(128/257,1/514,1/514,128/257)`，两个潜在边际真值均1/2且相关正，FINE候选反向KL虽比COARSE从1.651817降到1.156513，但FINE最优p=r=1/8，估计边际严重偏离50%，独立工作族仍无真实协方差。NEGATIVE_COUPLED m2类似，FINE选择p=1/8、r=7/8并失去真实负相关。高ELBO/低KL并不自动意味着所有后验不确定性被完整恢复。

完整自动化先有纯实现问题：首CI[39587074398](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39587074398) 32测31过，细粗70位Decimal评分在默认28位上下文中比较发生假失败；[独立数值精度订正](../../protocols/R196_ELBO_DECIMAL_COMPARISON_PRECISION_ERRATUM_2026-10-21.md)明确记录，未改真源、候选及评分目标。中间CI[39587234039](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39587234039)源计算与双Python测试已成功但旧ZIP条目计数仍为6，档案现含订正后共7文件，故旧CI归档校验失败。最终[GitHub Actions39587254747](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39587254747)双Python各32项测试共64次及完整24世界408候选归档三job全success；[机器原数据提交c414342f](https://github.com/edwardsage419/Psychohistory-Research/commit/c414342f1814358f987394974179d299cc80b51d)。

[正式科研报告](R196_SCIENTIFIC_REPORT_2026-10-21.md)、[24世界ELBO/KL全结果](R196_EXACT_RESULTS.json)、[408候选原始CSV](R196_ALL_408_MEAN_FIELD_ELBO_CANDIDATES.csv)、[12真后验概率及互信息库](R196_ALL_12_EXACT_POSTERIOR_SOURCES.json)、[最终机器验收](R196_FINAL_MACHINE_ACCEPTANCE.json)、[完整源码与32单测](r196_finite_meanfield_variational_bayes.py)、[含原协议与误差审计的七文件ZIP](R196_24_Exact_Finite_Variational_Bayes_Worlds.zip)均永久归档。一手依据：[Jordan等1999](https://doi.org/10.1023/A:1007665907178)、[Blei等2017](https://doi.org/10.1080/01621459.2017.1285773)。

仅人工E1，不是连续参数全局VI或现实后验评价；新增真人E2、历史E3均0，R073及PESEN v0.1冻结。下一 **R197 P1/08-021 ARIMA**；依旧先完成全部R系列、然后统一归纳分类、最后熔炼。
