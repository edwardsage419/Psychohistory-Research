# R134：Taylor 1979 多群体演化博弈

日期：2026-10-20。原始目录 **P2 / 05-010 Multi Population Evolutionary Games**。独立于R133的演化稳定策略单一种群学习。

直接核阅Taylor 1979 *Evolutionarily Stable Strategies with Two Types of Player* 原刊p77–79；本期计算原p77 Eq1与p78 Eq2/3/4/5的两个群体线性适应度、严格入侵和动态，未复现原p79起非线性亲代照料时间模型。

阶段主要严格数学结果：

1. 项目自设同类A=D=[[0,1],[1,0]]与异类B=C=[[2,0],[0,2]]：单独扰动两个人口各自可抗入侵；两个群体同时从p=q=(1/2,1/2)朝(3/4,1/4)变化则居民优势D(ε)=−ε/4，联合Eq5局部特征值+1/2、−3/2。
2. 项目自设零和Matching Pennies两群体：连续H=x(1−x)y(1−y)严格守恒；相同聚合z=(x+y)/2=1/2的三个群体结构，可有z导数分别+24/125、−24/125、0。
3. 有界81组人工块矩阵×9组居民×16组变异者×3 ε = **34,992**项精确原Eq1与独立矩阵二次型一致；数值RK4的H误差同批审计。45项本地标准库unittest已成功；远端CI单独验收。

材料：

* [事前冻结协议](../../protocols/R134_TAYLOR_1979_MULTIPOP_ESS_REPLICATOR_EXACT_PRESCORE_FREEZE_2026-10-20.md)
* [完整研究报告](R134_TAYLOR_1979_MULTIPOP_ORIGINAL_ESS_JOINT_INVASION_AND_AGGREGATION_REPORT_2026-10-20.md)
* [完整Python源码与45项独立测试ZIP](R134_Taylor1979_source_and_45_tests.zip)
* [机读精确计算和RK4诊断](R134_PHASE_A_MATHEMATICAL_RESULTS.json)
* [真实GitHub Actions双Python CI](../../.github/workflows/r134-taylor1979-two-population-45-tests.yml)
* [正式科学验收状态](R134_FINAL_ACCEPTANCE_STATUS.json)

**证据限界**：81组均为项目人工参数，不是81组实验或受试群体；新真实人类/动物逐行E2=0、新历史事件E3=0，不证明社会历史变迁规律或实际预测效度。R073和PESEN v0.1始终冻结；全部既定R学完后才分类和熔炼。
