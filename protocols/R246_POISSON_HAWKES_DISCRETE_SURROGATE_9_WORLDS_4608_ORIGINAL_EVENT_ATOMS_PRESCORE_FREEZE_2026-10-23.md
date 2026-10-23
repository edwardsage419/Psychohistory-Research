# R246 泊松与 Hawkes 过程：九人工四时间格事件概率世界、4608完整来源、离散自激与潜在类别的统计辨别；评分前冻结

日期2026-10-23 Asia/Taipei。原239目录 **11-006 Poisson and Hawkes Processes（P1）**，研究编号R246。**严格科学资格限于四格、每格至多1次事件的Bernoulli离散事件概率代理**，绝非严格连续时间Poisson过程或Hawkes点过程。全部E1人工研究，新增真人E2/历史E3=0，R073、PESEN v0.1冻结，优先完整原R目录后分类最后熔炼。

## 论文来源及必须保留的模型边界

Hawkes, A. G. (1971), [*Spectra of some self-exciting and mutually exciting point processes*](https://doi.org/10.1093/biomet/58.1.83), *Biometrika* 58:83–90（原始自激点过程）。对照经典独立增量Poisson point process见 MIT 6.262 Chapter 2 [Poisson Processes](https://ocw.mit.edu/courses/6-262-discrete-stochastic-processes-spring-2011/pages/course-notes/)。**真正连续时间Poisson在正时间长度区间可能发生两个以上事件，其统计N(Δt)服从Poisson(λΔt)；真正Hawkes条件强度 λ(t)=μ+Σφ(t−ti)，事件可以在任意实数时间出现且其点过程似然含连续时间积分**。本R恰限制每格Yk∈{0,1}，使用2bit均匀数阈值决定条件Bernoulli事件概率，永远不模拟同格多重到达、指数等待时间、真实连续强度或高斯极限。本R出现的“自激”仅是有限时间格内被先前事件提高下一格Bernoulli hazard的**离散类比机制**，不能写作高斯/Poisson/Hawkes原过程实证复现，也不称hawkes branching比率。

## 原结构全集与统计输入

每world九个公平独立二元源`(U,R11,R12,R21,R22,R31,R32,R41,R42)`；Rk由2bit均匀取0,1,2,3，U是隐藏个体类别。每world**512条完整外生原来源**，九world共**4608条**，每行概率1/512。完整原来源记录U、每格2bit、实际可见事件Y1…Y4、当次真实生成的条件hazard1…4、隐藏真实事件H1…H4、实际累计计数N1…N4及原质量。**真实模型评价只用可见Y1…Y4路径，不能把U与生成hazard当作实际观测数据**。

## 九个冻结四格 Bernoulli event worlds

1. `IID_LOW`：独立各格 P(Y=1)=1/4，人工独立基准，不叫真实连续Poisson。
2. `IID_HIGH`：独立各格 P(Y=1)=3/4。
3. `SELF_EXCITING_LAG1`：第一格p=1/4，第k格p=1/4+(1/2)Y{k−1}，先前事件使下一格条件概率由1/4升至3/4。确切P(Y1=1)=1/4、P(Y2=1)=3/8、Cov(Y1,Y2)=3/32。
4. `REFRACTORY_LAG1`：第一格p=1/2，后续p=1/2−(1/4)Y{k−1}，最近事件抑制下一次到达，Cov(Y1,Y2)=−1/16。
5. `STATIC_LATENT_RATE_MIXTURE`：整条路径U固定，U=0时每格p=3/4、U=1时每格p=1/4，各个个体给定U后IID。观察Y1/Y2各边际1/2，但Cov(Y1,Y2)=1/16，且P(Y2=1|Y1=1)=5/8、P(Y2=1|Y1=0)=3/8。正相关来自**潜在异质性**，不是任何事件导致概率上升；该world不能被宣称已观察到Hawkes因果自激。
6. `ALTERNATING_EXOGENOUS_RATE`：每格独立，奇数格事件率1/4，偶数格3/4；随时期改变的基准率不能误写作历史自激。
7. `COMMON_SHOCK_ALL_BINS`：全部四格Y都由第一格R1阈值2决定，Y=(0,0,0,0)或(1,1,1,1)，各概率1/2，完全同一外源冲击造成聚集；仍不能宣称事件互相激发。
8. `STATIC_HIDDEN_SELF_EXCITING_SENSOR_ALIAS`：真实隐藏H1…H4全0，没有任何真实事件；实际观测事件Y却按照与3完全相同的原R路径报告。逐全部外生source观察Y完全一致，但真实潜在物理事件不同，这只有在允许观测设备产生伪事件时成立。
9. `SELF_EXCITING_TWO_LAG`：p1=1/4，后续p_k=1/4+Y{k−1}/4+Y{k−2}/4（不存在的过去为0），最大3/4；保留两格记忆。固定正支持条件：P(Y3=1|Y2=0,Y1=1)=1/2，P(Y3=1|Y2=0,Y1=0)=1/4，故只看最后一格不足。

## 冻结独立计算和外推限制

A. 完整源机制将真实p_k乘4成整数阈值，再用每格独立Rk<4pk生成Yk；COMMON复用第一格R1；STATIC_SENSOR生成Y但真H全部0。各world512完整原source正概率总质量1，观察Y1…Y4完整16模式PMF，来源中N1…N4是累计报告事件数，不代表真实物理多次事件。
B. **独立第二路线**不读取源CSV和阈值模拟函数，直接对16种可能event序列逐格计算条件Bernoulli路径似然`∏_k p_k(y1…y{k-1},U)^{yk}(1−p_k)^{1−yk}`；STATIC_SENSOR用3的观察p；COMMON仅0000/1111各质量1/2；混合率对U=0和U=1两个乘积分布按1/2平均。两条路径逐world全部16格严格Fraction相等。
C. 从已边缘化完整Y路径计算每格期望、各格累积均值、第一/第二事件协方差、P(Y2=1|Y1=1)与P(Y2=1|Y1=0)及在正支持内两个lag对第三格的额外预测。完整概率校准只在此人工有限场景自洽，不构成真正连续Hawkes补偿子或参数估计。
D. 冻结比较：IID_LOW Cov=0；SELF_EXCITING_LAG1 Cov=3/32；REFRACTORY_LAG1 Cov=−1/16；STATIC_LATENT_RATE_MIXTURE Cov=1/16；COMMON_SHOCK Cov=1/4，不能单凭正协方差判定真实自激。SELF_EXCITING_LAG1与STATIC_HIDDEN_SELF_EXCITING_SENSOR_ALIAS**每相同九位外生source**的实际Y1…Y4全相同，隐藏真H完全不同。
E. TWO_LAG指定的两个第三格条件概率1/2与1/4严格相符。不能把这有限二元路径后验误当作实际指数激发核参数。
F. 强制展示真正连续Poisson的单格P(N≥2)>0但本文代理恒为0（对于任意λΔt>0可由`1−e^(−λΔt)(1+λΔt)>0`解析证明）；因故明文标记`NOT_ACTUAL_POISSON_OR_HAWKES`，不输出虚假的“真实Poisson数据已模拟”。
G. Python 3.11/3.12各≥45真实单测，第三独立CI source审计重生全4608原source、16模式观察分布、正负协方差、二格记忆反例、三个不同正相关机制区别、原SHA256后永久机器人归档main；run success和完整原CSV存在后才能正式E1结题。
H. 下一目录11-007 Branching Processes（P1），拟R247，但需本项后实查。所有者既定顺序不变。
