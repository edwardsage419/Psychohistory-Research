# R210 随机对照实验09-001：六人有限总体、20种完整随机分配与干扰反例，事前冻结

日期2026-10-22（Asia/Taipei）。**实际原239目录** `09-001`，中文随机对照实验，英文Randomized Controlled Experiment，优先级P0，现正式登记研究编号R210。对应目录 `docs/MODEL_CANDIDATE_CATALOG_v0.1.json` 逐条机器核验，不沿用已勘误的08-032/08-033虚假后缀。本研究全人工E1，聚焦有、无干扰情况下的设计型因果估计，不模拟真实参与者或确证外部效应。

## 学术源与数学口径
Neyman, J. (1923; D. M. Dabrowska & T. P. Speed英文译1990), *On the Application of Probability Theory to Agricultural Experiments. Essay on Principles. Section 9*, Statistical Science 5(4):465–472, https://doi.org/10.1214/ss/1177012031 ，基于有限潜在结果与随机化估计均值差的期望和方差。Rubin, D. B. (1974), *Estimating causal effects of treatments in randomized and nonrandomized studies*, Journal of Educational Psychology 66:688–701, https://doi.org/10.1037/h0037350 ，讨论潜在结果、随机分配与观察设计。Fisher 1935《The Design of Experiments》的sharp null随机化检验为本实验第三检验关口，本研究只用固定六人均衡完全随机分配的精确置换，不推断任意人口参数。

## 设计与全部原始分配来源

固定有限六名人工单位i=0..5，恰3名被分到处理z_i=1、另外3名对照z_i=0，从六人选择处理三名的C(6,3)=**20条完整带标签随机分配**严格等概率1/20。所有世界都用**同一套20个分配序列**，但世界是不同人工潜在结果设计条件，不是140名真正不同真实参与者。不得将不同分配直接当独立实验场次，尽管按设计它们是可能实现的互斥事件。

冻结6种满足SUTVA/无干扰的人工有限潜在结果世界，各六人潜在对照结果Y_i(0)和潜在处理结果Y_i(1)=Y_i(0)+τ_i：
1. RAMP_NULL: Y0=(0,1,2,3,4,5), τ=(0,0,0,0,0,0)。
2. OUTLIER_NULL: Y0=(0,0,0,0,0,12), τ全0。
3. RAMP_CONST_TWO: Y0=(0,1,2,3,4,5), τ全2。
4. RAMP_SINGLE_HET: Y0=(0,1,2,3,4,5), τ=(0,0,0,0,0,6)。
5. RAMP_ZERO_ATE_HET: Y0=(0,1,2,3,4,5), τ=(3,-3,2,-2,1,-1)，真ATE0但“每人无处理效果”的**Fisher sharp null不成立**。
6. OUTLIER_HET: Y0=(0,0,0,0,0,12), τ=(0,1,2,3,4,5)。

另设第7种 **PAIR_INTERFERENCE**，无固定Y_i(z_i)一元潜在结果的干扰生成函数：六人配成三对(0,1),(2,3),(4,5)，对每个分配向量z的真实人工观测Y_i(z_all)=i+2z_i+3z_peer(i)，同伴处理有额外3社会溢出。固定他人分配条件下改变自身处理的**控制直接效应**始终2，但是每组完全随机分配3/3下，将处理组观察值均值减对照组均值的常规估计量的随机化期望并不是2：精确由条件邻居处理概率 P(peer treated|zi=1)=2/5、P(peer treated|zi=0)=3/5 推出2+3(2/5−3/5)=**7/5**。该世界不满足无干扰，明确**禁止套用Neyman无干扰有限总体方差公式、个体ATE Y_i(1)−Y_i(0)解释或声称Fisher sharp-null随机化检验的真实有效性**。输出对应字段null和明确的assumption_break标记。总体**7世界×20随机分配=140条原人工随机设计记录**，各世界完整来源权重1/20并归一。

## 固定三类估计与验证

SUTVA各世界的目标真有限平均处理效应ATE=(Σ_i τ_i)/6。单个实际分配z只观察Yi(zi)，估计处理与对照的实测均值之差 `tau_hat = mean(Y_obs treated)-mean(Y_obs control)`，统计量无需拟合参数。对完整20个等概率分配求E_random[tau_hat]与Var_random[tau_hat]，分别与（a）ATE逐Fraction精确一致及（b）独立源公式
`Var_Neyman = S1²/3 + S0²/3 − S_tau²/6` 精确一致。S1²、S0²、Sτ²定义为6人**样本型有限总体方差分母5**的固定潜在向量的方差，而不是观测组3人的分母3。单条可观察分配的常用保守估计 `Vhat = s1_obs²/3 + s0_obs²/3`，两组分母均为2，完整20分配等权期望严格等于`S1²/3+S0²/3`，与真正Var_random之差为 `Sτ²/6`。常数处理效果时Sτ²=0，异质效果时正；只有人工潜在真值全知时才能写出真Sτ²，不准称从一份观察随机试验能独立识别出它。

Fisher sharp-null双侧精确置换：对每条已产生的真实人工**SUTVA观察分配**，仅在被检验 `H0: Y_i(1)=Y_i(0) for all i` 的**假设下**，将所有6个实测结果固定并完整枚举20种其他处理分配，重新计算处理均值减对照均值的绝对值，按 `P_sharp= #{|T(z')|≥|Tobs|} /20`（包含完全同分）得理性分数。这种p值是对Fisher个体效果均0的**尖锐零假设**做检验；对于真ATE0但效果异质不为0的世界，不得将其作为“ATE0准确检验”来宣称一类错误控制。对于PAIR_INTERFERENCE按定义不存在6个互相独立于他人分配的Y_i(zi)，禁止按同程序称为有效sharp-null参考分布。

预冻名义错误阈值α=1/20=0.05与α=1/10=0.1；在六人3/3、以绝对均值差构造的双侧置换中，每个实际分配的**互补分配**均产生相反方向但绝对值相同的统计量，因此精确双侧p最小为2/20=1/10，α=0.05时任何人工观察都不会触发拒绝。这个结果应以独立数学互补分配恒等式和全部原分配计算同时核实，避免出现“95%显著性完全验证失败”误述；只是设计最小分辨率/统计功效限制。对于真sharp-null的两个世界验证不同α下严格经验型设计拒绝率≤α。

## 第七干扰源关口

对于PAIR_INTERFERENCE每一条20来源先计算Y_i(z_all)，直接计算组间均值差，以及原随机分配来源概率、两组看到的真实同伴暴露率；完整20来源的平均估计偏差E[tauhat]−direct_effect2=−3/5，与组合概率2/5和3/5的单独解析演绎逐Fraction一致。验证如果错误地用无干扰ATE真值2来解释，在这个已知正溢出3的世界就出现系统偏差。禁用Fisher/Neyman SUTVA公式字段，用`null`或明确字符串`NOT_DEFINED_UNDER_INTERFERENCE`而非伪造计算零值。

## 归档/验收与外推边界

原生Python标准库Fraction，至少30项单测，完整140原随机分配CSV、7世界精确结果JSON、原20分配签名及SOURCE SHA机器验收。Python3.11/3.12两个CI测试job success，第三自动生成全部140条原设计赋值来源、验证六SUTVA公式及干扰反例、SHA并提交main，事后科学报告与最终结题收据才可标记**CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_RANDOMIZATION**。本研究是真正原目录09-001的**有界数学方法学习**，不等于完成对所有RCT设计、交叉效应真实实验以及现实因果识别的全面审计；没有真人E2或真实历史E3。R073、PESEN v0.1继续冻结。下一原目录 **09-002 Potential Outcomes Framework** 可编号R211，继续完成真实239项原目录才统一分类和熔炼。
