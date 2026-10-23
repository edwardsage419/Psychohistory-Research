# R251 李雅普诺夫稳定性 — 九一维离散映射、405完整有理初值—时点来源；事前冻结

日期2026-10-23 Asia/Taipei。原239目录11-011 Lyapunov Stability（P2），R251。先所有R再分类再熔炼。冻结R073和PESEN v0.1不修改。所有数据仅人工E1，新真人E2/历史E3均0。

## 一手依据及推断边界

A. M. Lyapunov, *The General Problem of the Stability of Motion* (1892; English translation in *International Journal of Control*, 55(3), 1992), DOI https://doi.org/10.1080/00207179208934253；University of Washington ME547课程 *Discrete-time case: key concept of Lyapunov* https://faculty.washington.edu/chx/teaching/me547/2_1_stability_slides_Lyapunov_light.pdf 。这里仅研究自治一维离散时间映射x(k+1)=f(x(k))在平衡x*=0周围的V(x)=x²。若V正定且ΔV=V(f(x))−V(x)<0（在邻域内且能保持邻域），可证明局部渐近稳定；ΔV=0不能推出渐近吸引；ΔV在少量初值为负也不能无附加条件推出整个邻域稳定。局部非双曲的二次迭代证明与单步正定V审计严格分离。**不声称构造了全部九模型的全局李雅普诺夫函数或真实心理历史稳定性证据**。

## 原结构空间与九事前冻结世界

统一九初值集合S={-1/2,-1/4,-1/12,-1/24,0,1/24,1/12,1/4,1/2}、五时点n∈{0,1,2,3,4}。九世界×九轨道×五时点，共405条**人工初值—时点**原source，每世界45且每source设计权重1/45；不是405条独立真人数据。每source保存世界、x0、n、当前x_n、V_n=x_n²、f(x_n)、ΔV_n=f(x_n)²−x_n²、局部f′(x_n)、初值灵敏度D_n和权重。所有数用标准库Fraction实现，无浮点模拟误差。

1. HALF_CONTRACTION：f=x/2，ΔV=−3x²/4 <0 (x≠0)，0全局渐近吸引。
2. NEGATIVE_HALF_CONTRACTION：f=−x/2，ΔV=−3x²/4 <0，交替符号也收敛。
3. ZERO_MAP：f=0，ΔV=−x²，0一步到达且稳定。
4. DOUBLE_EXPANSION：f=2x，ΔV=3x²>0，0不稳定。
5. IDENTITY_NEUTRAL：f=x，ΔV=0，0 Lyapunov稳定但不渐近吸引。
6. SIGN_FLIP_NEUTRAL：f=−x，ΔV=0；0稳定但非渐近吸引，非零状态2周期。
7. CUBIC_LOCAL_INWARD：f=x−x³，V(f)=V(x)(1−x²)²，在0<|x|<1严格减小，0在(-1,1)局部渐近吸引，f′(0)=+1说明乘子临界。
8. CUBIC_OUTWARD：f=x+x³，ΔV=x^4(2+x²)>0 (x≠0)，0局部不稳定，虽然f′(0)=+1与第7例一致；**不能仅凭乘子+1或V=正定就判吸引**。
9. LOGISTIC_R3_CENTERED：在Logistic r=3的x*=2/3周围以y=x−2/3写f(y)=−y−3y²；单步`ΔV=y²[(1+3y)²−1]=6y³+9y⁴`，对小正y严格**增大**、小负y严格**减小**。因此V=y²不是两侧严格单步下降的局部Lyapunov证书，尽管二次迭代有`f²(y)=y−18y³−27y⁴=y[1−y²(18+27y)]`，在0<|y|≤1/12内严格每两步收缩。有限四步来源和独立形式多项式证明这一反例，同时声明二步下降与奇偶连续性给局部渐近吸引，但**单步候选V下降失败不能断言系统不稳定**。

## 预评分独立核验

A. 源生成器逐x0作确定性四步递推，并在每步用导数链式传播D(n+1)=f′(x_n)D_n，输出上述全变量、45唯一cohort-time类型/world，405全来源正权重归一。

B. 完全独立的第二数学路线，从冻结多项式f系数构造形式多项式复合f^{∘n}，Horner求值与形式微分D_n，并对原CSV里405源逐项核验V_n、ΔV_n、f′和敏感度。整个代码使用精确Fraction，不得以“两个实现用了同一递推”冒充独立。

C. 四个线性/零映射用`V(f)-V=(a²−1)x²`精确证明下降/上升/零；identity和sign flip是V不变但稳定非吸引；cubic inward通过整个0<|x|<1严格向内且限域不变证明吸引；cubic outward通过所有非零邻点严格外向证明不稳定。**仅九采样初值不能替代这些解析局部论证。**

D. LOGISTIC_R3_CENTERED用两个不同符号源（+1/12、−1/12）的单步ΔV分别正/负，和独立形式系数`f²(y)=(0,1,0,-18,-27)`、严格邻域因子`0<1−y²(18+27y)<1`（0<|y|≤1/12）并存。允许单步V局部非单调但二步严格下降，明示“给定V不符合单步充分条件”并不等于稳定性质不成立。

E. 对所有初值、n≤4独立验证半群f^{m+n}=f^m∘f^n（m+n≤4）；原来源只说明四步有限轨道，而局部吸引的无限时结论来自严格数学符号论证。

F. 执行GitHub Actions Python3.11/3.12各≥45实际单测；第三原source archive job严格核验所有405行、抽样算式、局部符号证据、SHA256、JSON限定范围且自动提交全CSV/JSON/机读收据main；完整CI成功并审阅日志后正式有界E1报告和验收。下一原目录11-012 Entropy and Information Theory (R252/P1)。
