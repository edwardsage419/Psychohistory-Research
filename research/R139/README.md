# R139 Gordon 1954：共同资源困境的自由进入与有限博弈

**2026-10-20｜既定目录 P1 / 05-015 Common Pool Resource Dilemma。**

本轮严格区分**1954年原作者的资源经济静态模型**与**本项目新增的有限用户分摊产出博弈**。一手论文Gordon, *The Economic Theory of a Common-Property Resource: The Fishery*, JPE 62(2):124–142, DOI https://doi.org/10.1086/257497；真正核对[UCSB保存原刊扫描](https://faculty.econ.ucsb.edu/~tedb/Courses/Ec100C/Readings/ScottGordonFisheries.pdf)原印刷130页Fig1、131页Fig2、141页原Eq(1)/(2)、142页Eq(3)/(4)及作者明确的努力最优解。

原作者P=a−bL、L=cEP、R=L−E；本项目以beta代表b、gamma代表c、q为努力单位成本（原q=1），严格推出L(E)=gamma*a*E/(1+gamma*beta*E)；在gamma*a>q下社会最优E*=(√(gamma*a/q)−1)/(gamma*beta)，零租金自由进入Eopen=(gamma*a/q−1)/(gamma*beta)。

**本项目自造主例** a=9,gamma=1,beta=1/4,q=1：
- 社会最优：总努力8，捕获量24，存量3，净经济租金16；
- 自由进入：总努力32，捕获量32，存量1，净经济租金0。

**额外原创项目假设**：n个人同时选择努力，按各自努力份额获得平均捕获收入，个人效用u_i=e_i*(gamma*a/(1+gamma*beta*Σe_j)−q)。独立推导对称NE多项式，使用100步有理Fraction根区间核验**12组生产参数×8种n=96**例。n=3的连续对称努力总量约21.856406，n=8约28.061422，n=32约31.003558；区间数学精确，显示小数只是近似，n趋大逼近32。项目另演示n=3时社会最优边际费4/3每努力单位，是本项目自建收费政策而非Gordon原政策试验。

**单独离散新博弈**：三人每人可选0,2,...,16，枚举9³=729个配置×每人8项不同单侧偏离=**17,496**项真实Fraction比较。唯一三种纯NE为(6,8,8)的排列，总努力22，社会净租金**110/13**；社会净租金最大16，对应总努力8的15种行动配置。连续n=3、离散n=3、开放准入极限三者不能混淆。

**与R047去重**：R047先前研究De Geest/Kingsley公开真人CPR原数据；R067核实128人、32四人组、16轮非二元提取、1920条去练习记录。R139不读取或新拟合这些真实人的数据，也没有新E2个人预测；E3历史事件概率验证0。R073和PESEN v0.1继续冻结。

正式交付：
- [事前冻结协议](../../protocols/R139_GORDON_1954_FISHERY_OPEN_ACCESS_FINITE_PLAYERS_EXACT_PRESCORE_FREEZE_2026-10-20.md)
- [一手原刊与数学边界科学报告](R139_GORDON_1954_ORIGINAL_FISHERY_AND_FINITE_N_EXTRACTION_EXACT_REPORT_2026-10-20.md)
- [原生Python、70项unittest及完整机器结果ZIP](R139_Gordon1954_70_Tests_Exact_Source.zip)
- [正式机器验收](R139_FINAL_ACCEPTANCE_STATUS.json)
- [原生GitHub Actions CI](../../.github/workflows/r139-gordon1954-cpr-70-tests.yml)

ZIP解压后 `python -m unittest -v test_r139_gordon1954_exact.py` 与 `python r139_gordon1954_exact.py`；仅依赖Python标准库。完成既定全部R后再统一分类、归纳，最后熔炼。

**远端结题验收完成**：[GitHub Actions run39386412139](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39386412139) completed/success，运行源码commit `303a88137b6a155b1cd92b0bcd6cb5509e14fec3`。Python3.11 job118507201489执行70项单测5.327s，Python3.12 job118507201862执行70项4.449s。每任务4个SHA256均OK、全96组区间及17496项离散比较重新执行且JSON字节完全对照，累计140次实际单测、0失败。[远端机器验收收据](R139_PHASE_A_140_REAL_TESTS_96_ROOT_BRACKETS_17496_NE_CI_RECEIPT.json)。有界结题并非实际渔业或群体历史预测。
