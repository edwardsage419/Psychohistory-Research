# R285 多重比较控制：两假设四次二元试验、Holm与BH的精确风险、2304完整原source；先冻结

日期2026-10-23 Asia/Taipei。原239候选目录最后一项12-015 Multiple Testing Correction（P1）。原始理论文献Holm (1979), *A Simple Sequentially Rejective Multiple Test Procedure*, Scandinavian Journal of Statistics 6(2):65–70；Benjamini & Hochberg (1995), *Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing*, JRSS B 57(1):289–300, DOI https://doi.org/10.1111/j.2517-6161.1995.tb02031.x 。本研究自建小规模离散二元例子以完整枚举家族错误率FWER和错误发现率FDR，**不是发表作者的数据复现，也不证明两种程序的一般条件下全局定理**。

## 全部冻结原source与测试模型
两个独立研究假设H1、H2，各有四次独立Bernoulli观察，总共`Y11 Y12 Y13 Y14 Y21 Y22 Y23 Y24`有序八bit。真实成功概率三个人工世界：
* BOTH_NULL：p1=p2=1/2，两原假设皆真。
* ONE_SIGNAL：p1=3/4、p2=1/2，H1非零、H2为真原假设。
* BOTH_SIGNAL：p1=p2=3/4，两原假设均假。
每world完整2^8=256有序原source，准确来源质量p1^k1(1−p1)^(4−k1) p2^k2(1−p2)^(4−k2)，每世界所有256来源皆正质量。两测试各固定以原假设p0=1/2及n=4进行单侧右尾确切离散p-value=Pr[Binomial(4,1/2)≥K]；K=0,1,2,3,4分别为1、15/16、11/16、5/16、1/16。家族目标水平刻意预冻结为`alpha=1/2`（为便于小n离散p值在不同规则下产生严格差异，**这不是推荐的真实研究显著性水平**）。

冻结三个比较政策：
* RAW_UNADJUSTED：各独立拒绝当 p_i≤α，未校正的家族基线。
* HOLM_FWER：按(p_i, hypothesis_index)升序排序，第一项必须p_(1)≤α/2，才继续检查第二项p_(2)≤α；依序首个不满足即停止。假设并列顺序ID H1优先。
* BH_FDR：按相同升序，找最大rank r∈{1,2}满足p_(r)≤rα/2，拒绝前r个；若不存在r则拒绝0个。重要区别：当两原检验p=5/16时，RAW两者拒绝、HOLM两者均不拒绝，而**BH通过第二rank阈值α=1/2拒绝两者**。这是数学上两个政策的明确不等价反例。
三机制×三政策=9world，每world256完整原八bit来源，合计**2304个带policy/世界标签完整来源类型**，不可称独立真人研究。单来源计算拒绝mask(R1,R2)、总拒绝R、真null误报数V、真信号发现数S、FWER指示1[V>0]、FDP=V/max(R,1)、所有原p值和精确来源概率，完整CSV归档。

## 冻结9world风险矩阵
世界级原质量积分给定 E[V]、E[S]、P(V>0)=FWER、E[V/max(R,1)]=FDR 和E[R]，全部使用有理Fraction：
|世界|政策|FWER|FDR|E[V]|E[S]|E[R]|
|---|---|---:|---:|---:|---:|---:|
|BOTH_NULL|RAW_UNADJUSTED|135/256|135/256|5/8|0|5/8|
|BOTH_NULL|HOLM_FWER|31/256|31/256|5/32|0|5/32|
|BOTH_NULL|BH_FDR|47/256|47/256|9/32|0|9/32|
|ONE_SIGNAL|RAW_UNADJUSTED|5/16|1615/8192|5/16|189/256|269/256|
|ONE_SIGNAL|HOLM_FWER|145/1024|647/8192|145/1024|351/1024|31/64|
|ONE_SIGNAL|BH_FDR|253/1024|1079/8192|253/1024|459/1024|89/128|
|BOTH_SIGNAL|RAW_UNADJUSTED|0|0|0|189/128|189/128|
|BOTH_SIGNAL|HOLM_FWER|0|0|0|7371/8192|7371/8192|
|BOTH_SIGNAL|BH_FDR|0|0|0|10287/8192|10287/8192|

解释：BOTH_NULL时所有拒绝都是false discoveries，故FWER=FDR；ONE_SIGNAL时FDR区别于FWER，因为有时真发现分摊了总拒绝分母；BOTH_SIGNAL时根本没有真null，故FWER=FDR=0，仍可比较检出数。以上严格只是n4、两独立检验、alpha1/2人工离散例子的执行特征，不用来断言所有相关依赖、所有alpha下BH的性质。

## 3路线、审计边界与验收
A全枚举2304原world-policy八bit来源，冻结三种决策规则，逐source求原质量与R,V,S,FDP、拒绝mask，然后有理质量加权9world五指标。
B完全不调用有序source生成器，仅按K1~Binomial(4,p1)、K2~Binomial(4,p2)独立25个计数类别计算p-value、冻结政策和指标，并与A全部九世界逐Fraction严格一致。
C第三GitHub Actions机器作业不导入运行程序，独立重读2304 CSV并重建源质量、两个p值、排序/tie-breaking、拒绝mask和V/S/FDP、25计数理论及SHA256。须Python3.11和3.12各≥45真实unittest、三job success、原CSV/JSON/机器收据机器人永久GitHub main归档后，方可人工数学E1有界结题。
新增真人E2=0、真实历史E3=0，R073/PESEN v0.1继续冻结。**完成原目录最后一项不自动证明此前239个原候选均已完成统一验收**；下一工作必须核对R全目录每项归档与科研状态，再依用户顺序决定是否可以统一归纳分类，最后再熔炼。
