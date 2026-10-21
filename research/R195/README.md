# R195 马尔可夫链蒙特卡洛：三态精确目标、有限时间收敛与有效样本量

日期2026-10-21，原239模型目录P1/08-019 Markov Chain Monte Carlo。正式状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_MCMC**。

[评分前冻结协议](../../protocols/R195_MCMC_24_WORLDS_9288_EXACT_CELLS_PRESCORE_FREEZE_2026-10-21.md)固定四类目标UNIFORM(1,1,1)、CENTER(1,4,1)、BIMODAL(4,1,4)、SKEW(1,2,4)、两种三态路径对称proposal q=1/8或1/4、三个单点起始状态，合计**24个人工世界、8个独立MH核及24×129×3=9288个原始Fraction分布单元**。proposal+接受拒绝与对称边流量两套独立有理数矩阵构造完全一致，八核均逐项满足详细平衡与πT=π。全部24起点0..128步迭代分布与固定9时间点的独立矩阵二分快速幂逐Fraction一致，原始概率/总变差全归档。

核心结论：相同π不保证相同收敛速度。BIMODAL π=(4/9,1/9,4/9)从状态0开始，要使真实状态分布与目标TV≤1%，q1/8时首次是第124步，q1/4时是第61步。真平稳启动、对`f=1{X=2}`的**连续64状态样本均值**计算精确有限样本ESS，由63阶真实自协方差与完全独立的逐状态访问计数一二阶矩DP两法逐Fraction同值：UNIFORM的q1/8→1/4 ESS5.8254→11.8916，CENTER5.5517→11.3219，BIMODAL**1.9370→2.9754**，SKEW4.7137→9.2758。上述是特定f、给定N=64、真平稳启动时的**理论ESS**，绝不是仅通过经验R-hat验证真实采样的结论。

另完整执行**96条可重放固定随机种子数值路径**，每条从已指定状态先64次burn，随后2048次采样，统计三态频数、样本f均值及与π2的差，均不设人为误差合格阈值。BIMODAL目标的96模拟中对应24条路径平均绝对误差≈0.05378、最大≈0.18321，反映短模拟与黏滞条件下有限随机实现不能替代真正精确理论目标；不推断真人或社会数据的实际误差。

[正式科学报告](R195_SCIENTIFIC_REPORT_2026-10-21.md)、[24世界完整机器结果](R195_EXACT_RESULTS.json)、[9288个Fraction概率单元CSV](R195_ALL_9288_EXACT_DISTRIBUTION_CELLS.csv)、[8个精确MH核与ESS库](R195_ALL_8_EXACT_MCMC_KERNELS_AND_ESS.json)、[96个固定seed模拟源CSV](R195_ALL_96_SEEDED_MCMC_REPLICATES.csv)、[正式机器验收](R195_FINAL_MACHINE_ACCEPTANCE.json)、[原生程序及33项单元测试](r195_three_state_metropolis_exact.py)、[源码协议所有人工结果七文件ZIP](R195_24_Exact_ThreeState_MCMC_Worlds.zip)均在main永久归档。[GitHub Actions39585843192](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39585843192) Python3.11/3.12各33项单测共66次，第三job全部完整分布/ESS/96模拟源评分及永久结果归档，三个job均success，[实际数据提交36b84e68](https://github.com/edwardsage419/Psychohistory-Research/commit/36b84e68aa4c95803adfe52e127a5f89e8cd9b17)。

依据[Metropolis et al.1953](https://doi.org/10.1063/1.1699114)、[Hastings1970](https://doi.org/10.1093/biomet/57.1.97)、[Geyer1992](https://doi.org/10.1214/ss/1177011137)。科研分级仅人工E1，新增真人E2、历史E3均0，R073和PESEN v0.1冻结。下一 **R196 P2/08-020 Variational Bayes**；继续原R全研究、后统一归纳分类、最后熔炼。
