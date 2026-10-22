# R220 双重稳健估计：7世界、1537完整分配来源与条件性DR结论

日期2026-10-22。真实原239目录 **09-011 Doubly Robust Estimation（P2）**，正式状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_AIPW**。本项只有人工数学E1，新增真人E2=0、历史E3=0；不是原作者真实实验或实际临床/社会因果效应识别。

## 原文与计算前协议
Bang and Robins (2005), [Doubly Robust Estimation in Missing Data and Causal Inference Models](https://doi.org/10.1111/j.1541-0420.2005.00377.x), *Biometrics* 61:962–973，提出在适当假设下倾向与结果模型至少一者正确的DR估计性质；Cole and Hernán (2008), [Constructing Inverse Probability Weights for Marginal Structural Models](https://doi.org/10.1093/aje/kwn164), *AJE* 168:656–664，讨论交换性、正值性与极端权重。本项不是原作者模型全部实现，也不提供实际数据训练、样本外真人预测、交叉拟合或一般渐近一致性证明。

[完整来源与模型评分的预先冻结协议](../../protocols/R220_DOUBLY_ROBUST_7_WORLDS_1537_ORIGINAL_ASSIGNMENTS_PRESCORE_FREEZE_2026-10-22.md)于代码与实际评分前正式提交[e08f0091](https://github.com/edwardsage419/Psychohistory-Research/commit/e08f0091af0ca48f8e6c56a8e572b9a2b8e7986e)，没有根据评分调整模型正确/错误定义。

## 七个人工真总体、权限与1537条来源

固定8名人工单位，公共X=(0,0,0,0,1,1,1,1)，隐藏U=(0,0,1,1,0,0,1,1)。真潜在结果各世界相同，Y0=2X+2U，Y1=Y0+2，真有限ATE=2。真正有限X层潜在均值分别m0_correct(X)=2X+1、m1_correct(X)=2X+3；错误结果模型锁定m0_wrong=0、m1_wrong=1。公共倾向q在真p(X0/X1)=1/4、3/4时可正确指定为真p，或故意统一错设q=1/2。七世界：
1. BOTH_CORRECT：q正确、m正确；
2. PROP_CORRECT_OUTCOME_WRONG：q正确、m错误；
3. PROP_WRONG_OUTCOME_CORRECT：q错误、m正确；
4. BOTH_WRONG：两模型皆错；
5. HIDDEN_U_BOTH：真个体p按(X,U)为1/8、3/8、5/8、7/8，但公开q(X)仍是正确的X层处理概率1/4、3/4，m(X)仍是真正X层潜在均值；U同时影响处理与潜在结果，交换性不成立；
6. WEAK_OVERLAP：真p与公开q在X层为1/16、15/16，m错误；
7. NO_POSITIVITY：真p与公开q在X层为0、1，虽然m预先指定为正确，但没有观察支持来识别跨处理反事实。

前六世界各2^8=256条独立Bernoulli处理向量Z来源，第七世界1条唯一可能的Z，合计 **1537条原人工处理分配历史**。每世界来源概率完整和1，全部原记录保留真实p/Y0/Y1仅供人工oracle审计、实际Z/Yobs、公共q和m、五方法实际输出与其平方误差。1537不是1537名真人、独立试验或新的历史场次。公共估计器只读观察X、实际Z、实际Yobs与**预先固定**的q,m；真实隐藏U与真反事实不能进入其计算。

## 估计与两路独立验收

固定`PUBLIC_AIPW = (1/8)Σ[m1−m0 + Z(Yobs−m1)/q − (1−Z)(Yobs−m0)/(1−q)]`；对照`PUBLIC_HT = (1/8)Σ[ZYobs/q−(1−Z)Yobs/(1−q)]`和`PUBLIC_OUTCOME_ONLY=(1/8)Σ(m1−m0)`。另保留两项严格标记为**不可供现实观察者使用的oracle**：知道每人真p的`PRIVILEGED_TRUE_P_AIPW`和知道每人全部Y0/Y1的`PRIVILEGED_TRUE_Y_AIPW`。后者因为残差为0，对每个真原Z均等于ATE2，方差0，这不是现实可实施的方法结果。

对每一个真0<p<1的六个世界，分别以（A）256条原真赋值逐Fraction真实概率求出估计均值、方差与ATE的MSE；（B）**不枚举Z**，独立应用Bernoulli矩公式
`E(AIPW)=(1/8)Σ[m1−m0+p(Y1−m1)/q−(1−p)(Y0−m0)/(1−q)]`
及
`Var(AIPW)=(1/64)Σp(1−p)[(Y1−m1)/q+(Y0−m0)/(1−q)]²`，HT另用其专属方差公式、结果模型常数方差0。全部6×5方法=**30组Fraction均值及方差逐项一致**，各方法MSE严格等于方差+偏差²。这里没有任何模型参数从单条样本拟合，因此只是**明确固定人工来源下的设计平均性质**，不应当作通用有限样本统计无偏或真实实证能力。

## 主要结果

所有世界真ATE=2。表中数值是完整真Bernoulli赋值来源的设计期望，不是某一次实际观察的因果估计。

|世界|公共AIPW期望|AIPW随机化方差|公共HT期望|纯结果模型期望|
|---|---:|---:|---:|---:|
|BOTH_CORRECT|2|2/3|2|2|
|PROP_CORRECT_OUTCOME_WRONG|2|125/24|2|1|
|PROP_WRONG_OUTCOME_CORRECT|2|3/8|3|2|
|BOTH_WRONG|**3**|99/32|3|1|
|HIDDEN_U_BOTH|**8/3**|11/18|8/3|2|
|WEAK_OVERLAP|2|1937/120|2|1|
|NO_POSITIVITY|不可识别|不可识别|不可识别|不可识别|

1. 当公共真p逐人正确而m错误，PUBLIC_AIPW仍期望2，修正了纯结果预测1的偏差，不过方差变125/24。另一方向，当q错设1/2而正确的X层有限均值m保留时，因真p在层内均一、人工残差层内和为0，PUBLIC_AIPW仍期望2，修正了纯HT期望3。这是**该来源预设条件下的双重稳健**，不是随便设两模型都有效。
2. 当q和m都错，PUBLIC_AIPW的期望**3**，对真ATE产生偏差+1；所谓“双重稳健”不允许任何两模型都错仍无条件一致。
3. HIDDEN_U_BOTH中公开q确实是条件于X的真实平均处理概率，m也是真实X层潜在均值，但U同时导致分配与结局而给定X不交换，PUBLIC_AIPW期望**8/3**；知道每人真p的人工oracle才期望2。正确的“可见条件均值”**不能代替未观测混杂的可交换性假设**。
4. WEAK_OVERLAP中q=p正确但m错误，AIPW期望仍2，方差为**1937/120≈16.1417**。跨世界与BOTH_CORRECT的2/3比较并不独立隔离弱重叠，因为m正确性也改变；不能说这两差别全由p引起。数学无偏不代表极端权重下精度高。
5. NO_POSITIVITY中没有任何X层可在两种处理均观察的真源，全部公共HT/AIPW/预设结果模型外推、特权p与Y估计**均返回null，标明UNIDENTIFIED_NO_POSITIVITY**。只有人工oracle知道真ATE2；事先声称模型数值正确，不是由观察数据识别真反事实的证据。

## 实际原程序与正式三作业归档

[原生标准库Python与38项单测](r220_exact_doubly_robust_aipw.py)，[GitHub Actions run39751096555](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39751096555) Python3.11及3.12各38单测，总**76成功**；第三作业真实重新枚举7世界、1537原来源、两路Bernoulli数学与文件SHA，三个job均success。[原数据机器人永久提交54491d77](https://github.com/edwardsage419/Psychohistory-Research/commit/54491d772cc93116d826a4ad4da68a25327c0930)至main。

- [七世界完整机读结果](R220_EXACT_RESULTS.json)，SHA256 `dd9c82e688b914ebb114a9384797d2cf638b977340bd799375724d096d8b4ac5`。
- [全部1537原人工治疗来源及五种方法逐原来源实际平方损失CSV](R220_ALL_1537_ORIGINAL_AIPW_ASSIGNMENT_SOURCES.csv)，SHA256 `d6b5b795b8472c5b44580bf5c0c5d5d255255ba546ab7f51c724a95ee600fc09`。
- [真实文件SHA机器验收](R220_FINAL_MACHINE_ACCEPTANCE.json)及[正式结题科研状态收据](R220_FINAL_ACCEPTANCE_STATUS.json)。

**R220=CLOSED_BOUNDED_E1_ARTIFICIAL_AIPW**，只能外推到事前明示的有限人工分配模型；真人E2、真实历史E3仍为0，R073/PESEN v0.1均继续冻结。下一真实原目录 **09-012 Causal Mediation Analysis（R221）**，继续先完成全部R研究，再统一分类，最后熔炼。
