# R143 — Arthur 1989：正反馈、路径依赖与随机技术锁定的精确审计
日期2026-10-20｜目录P1/06-001 Institutional Path Dependence｜**E1理论模型；新增E2/E3均0**。

## 原刊一手证据及适用范围
W. Brian Arthur (1989), *Competing Technologies, Increasing Returns, and Lock-In by Historical Events*, Economic Journal 99(394):116–131, DOI https://doi.org/10.2307/2234208。原刊 PDF https://www.rochelleterman.com/ir/sites/default/files/arthur%201989.pdf 。本期真正可视阅读原印刷p118 Table1、p120 Eq(1)–(3)/Fig1、p121 Table3、p122有关吸收、非遍历性、潜在低效率与灵活性。**原作者的对象是技术采用，不是现实制度变化的受试者数据**；本期将其用于“制度路径依赖”只是明确注明的跨学科理论类比。未复现原作者所有非线性、多技术、理性预期拓展。

## 原Table1的固定子模型及两路线验证
按入场者类型R/S，技术A/B收益为R:(2+r*nA,r*nB)，S:(s*nA,2+s*nB)。本期r=s=1、R/S独立各1/2出现，收益平局时两技术各选1/2。注意**原文r、s按采用者类型指定且同一类型对两技术共用斜率**，并非技术特有的增长系数。令d=nA−nB，R选择A的收益差d+2、S为d−2。只有d≥3或d≤−3才分别永久锁定A/B；d=±2仍有平局，不是吸收状态。

瞬态d∈{-2,-1,0,1,2}，下一次A概率依次1/4,1/2,1/2,1/2,3/4。独立以Fraction高斯消元精确解(I-Q)p=b、(I-Q)t=1，并由独立概率比值积公式重算最终A吸收概率，五状态完全一致：

|初始d|最终锁A概率|首次锁定期望剩余次数|
|---:|---:|---:|
|-2|1/14|7/3|
|-1|2/7|16/3|
|0|**1/2**|**19/3**|
|1|5/7|16/3|
|2|13/14|7/3|

更强的独立首达时间公式：若从d0=0出发，τ只取3,5,7,…，P(τ=3+2j)=(3/8)(5/8)^j，故期望=3+2*(5/3)=19/3。对T∈{1,2,3,4,5,6,8,10,12}的**完整(nA,nB)存量动态规划**与另写的d过程前向递推完全一致。T=12锁A/B概率各29643/65536，未锁3125/32768；无限未来对称模型锁A/B各1/2。该结果是数学随机过程分布，不是现实制度锁定概率的估计。

## 同样采用者构成、不同到达顺序
20种包含3R/3S的六步固定排列全部以两个不同算法（合并重复存量DP；不合并、逐个平局树分支）精确核验。RRRSSS→(6A,0B)及SSSRRR→(0A,6B)，各于第三步锁定；RSRSRS→(3A,3B)，RRSSRS→最终A=3或6各1/2。20顺序等权**条件分布**到第6次锁A、锁B各3/16，未锁5/8。不能把“固定有3R和3S”误称为“每次R/S独立入场”的无条件过程。

与无反馈r=s=0对照：同样20排列六步全部得到(3A,3B)，IID入场时任意T的A计数分布严格为Binomial(T,1/2)，程序核验T≤12所有质量。负反馈r=s=-1下T≤12的|d|不超过3，是有限时间检查，不冒称完整原作者遍历性定理。

## 显式非原Table1的反事实效率扩展
**另外自建**技术A采用收益斜率1、技术B斜率2的子模型，R:(2+nA,2*nB)、S:(nA,2+2*nB)。前三位均R使nA3/nB0后两类新人均偏好A，出现局部锁定；但两技术如果分别开发到3次采用，R收益A5/B6，S收益A3/B8，B反事实潜力较高。此比较不是现实累计福利差，更不是原作者Table1中的r/s形式。给B固定奖励2时，在(3,0) S可转B；在(6,0) R/S仍都偏好A。不能以“锁定”夸称任何规模的政策干预均无法逆转。

## 身份校验、代码与科学资格
计算前冻结协议[protocol](../../protocols/R143_ARTHUR_1989_INCREASING_RETURNS_PATH_DEPENDENCE_EXACT_ABSORBING_FREEZE_2026-10-20.md)，GitHub commit 79c3d777223dc5f14bfda4b4c79922eaf49b377c。完整[Python源程序、86项unittest及JSON结果ZIP](R143_Arthur1989_Path_Dependence_86_Tests.zip)仅依赖标准库、全部用Fraction算概率。要求先SHA256核验ZIP及两份.py与JSON，再在Python3.11和3.12真跑86项测试及输出JSON逐字节重算。没有真人数据、制度政策实地介入、因果历史事件检验；**E2=0/E3=0**。R073和PESEN v0.1继续冻结。全部R结束后再统一分类、最后熔炼。
## 已完成的GitHub远端机器验收（执行后写入的不可变收据）

真实[GitHub Actions run39395394113](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39395394113)，以源码commit `3b0ff26f9997af474d303fc3edb9f2c29ab6c150`运行，status completed/conclusion success。Python3.11 job118536757583实际86 tests in 0.077s，Python3.12 job118536757840实际86 tests in 0.100s，总共172次真实单元测试、0失败。两个任务各自校验GitHub存储的ZIP SHA256 `cc0005409d20b86f4a40df3d5b9fa0e208a834719f48fd7ddea4145d17579af6`、源程序 `250428ec84367ae1260e460730faccf5ad897044592911aaff9b75b0b987dae5`、测试 `751bcaab6597d4bda7f323b7de2b5204f5d485939f92062d0baf5c01664b544a`、机器结果JSON `201bba8040cbaa946289f1e25aec6a481d7dc3dba2806a927285e9a343239693`，每环境4项均OK；然后执行86项单元测试及完整20顺序/有限期随机过程JSON重算、与归档原文件字节完全相同，日志均确实输出“R143 PASS first-hand Arthur Table1 86 tests exact 20 paths and 19/3 lock time”。[正式验收收据](R143_PHASE_A_172_REAL_TESTS_ARTHUR_EXACT_ABSORBING_GITHUB_CI_RECEIPT.json)。严格保持一手数学复算 E1 与现实历史制度E3证据隔离。
