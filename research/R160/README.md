# R160 基因文化协同演化｜60组人工联合频率与遗传文化关联的精确模型

日期：2026年10月21日。原既定目录 **P2 / 07-002 Gene Culture Coevolution**。本阶段 **CLOSED_BOUNDED_E1**，只结题于本项目原创的2×2联合频率模型。人工G0/G1和C0/C1仅为无现实群体含义的中性标签。模型没有复制真实DNA、孟德尔遗传、社会文化采样、家系或人的基因型。

**一手资料：** [Feldman与Laland 1996 期刊原摘要](https://www.sciencedirect.com/science/article/pii/0169534796100525)、[Feldman与Zhivotovsky 1992 PNAS开放论文](https://pmc.ncbi.nlm.nih.gov/articles/PMC50672/)、[Laland等2010 Nature Reviews Genetics 原出版方关键内容](https://www.nature.com/articles/nrg2734)。直接核对这些记录和原文已公开的理论范围。原作者的垂直文化传递、多位点遗传机制、原始真实遗传数据与复杂选择机制均未在此重现。详细审计见[正式科学报告](R160_SCIENTIFIC_REPORT_2026-10-21.md)。

**冻结模型：** 五种初始基因文化联合表×两档关联选择系数×三档文化多数复制权重×两档横向更新比例，共60组，全部运行0至4代（300个联合状态时点）。人工联合概率p00、p01、p10、p11及其G1边际、C1边际与关联\(D=p_{11}-GC\)全部存入JSON。直接Fraction迭代与另外一套**穷举四种联合类和八组三示范者多数模式**的独立算法得到完全一致的1200个联合频率单元。

**关键反例：** 两个起点分别为(3/8,1/8,1/8,3/8)与(1/8,3/8,3/8,1/8)，单独观察到的G1和C1边际比例均是1/2，但联合关联分别是+1/8与−1/8。预设人工选择强度s=1/2时，下一代G1比例分别为**11/19**及**9/17**，因此只用两个边际频率无法确定未来演化。不存在实际人群遗传选择的推断。

**额外边界：** s=0时所有世代的基因边际保持不变；横向更新u=0时模仿权重h不影响轨迹，无法根据该轨迹识别h；s=0、u=1/4时，不同联合关联经过一期由±1/8缩小至±3/32，而两侧边际仍恒等于1/2。没有突变及创新时，起点全无C1永远不出现C1，起点全部C1仍恒为C1。

**CI双轮与永久归档：** 首轮[GitHub Actions 39524857411](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39524857411)，终轮[四项固定SHA256复验与归档 run39524960129](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39524960129)，均成功；Python3.11、3.12每轮各运行90种不同真实测试方法，独立归档任务另执行90项，总计450次、失败0。原始JSON与完整源码测试ZIP永久写入[归档提交7eab756](https://github.com/edwardsage419/Psychohistory-Research/commit/7eab7567e16fd1fdd89edfcb241eb40e9a3d6053)。

正式材料：[计算前冻结协议](../../protocols/R160_GENE_CULTURE_JOINT_SELECTION_LEARNING_60_FRACTION_WORLDS_PRESCORE_FREEZE_2026-10-21.md)（提交f9557ed）｜[科学报告](R160_SCIENTIFIC_REPORT_2026-10-21.md)｜[模型源码](r160_joint_gene_culture_exact.py)｜[90项测试源码](test_r160_joint_gene_culture_exact.py)｜[完整结果JSON](R160_EXACT_RESULTS.json)｜[源码测试结果ZIP](R160_Gene_Culture_60_Worlds_90_Tests.zip)｜[机器验收收据](R160_FINAL_MACHINE_ACCEPTANCE.json)。

固定SHA256四项：
* 源码：`a267dccfab5801533a48dc50e0f0ea89af02ff2792a7f9494425a1b0f1a4c59e`
* 测试：`b0a976cf9516569214139c676312c9034e57ac16569c51114cb1724008975673`
* JSON：`7073cfd2aa3cad37955065c619d9ad9da16ba5b63ad768c0ae226597e64536bc`
* ZIP：`aa68cc231970b2957bc7967d4e0538b8903a654b995ec9e635fc5c3afd8e07c1`

在 `research/R160` 运行 `python r160_joint_gene_culture_exact.py > R160_EXACT_RESULTS.json`，再执行 `python -m unittest -q test_r160_joint_gene_culture_exact.py`；全部标准库。

新增E2=0、E3=0；R073、PESEN v0.1维持冻结。下一原目录 **R161 P1/07-003 Conformist Transmission**。先完成全部既定R模型，再统一归纳分类，最后模型熔炼。
