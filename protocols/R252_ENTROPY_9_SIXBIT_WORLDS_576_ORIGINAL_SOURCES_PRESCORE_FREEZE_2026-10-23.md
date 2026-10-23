# R252 熵与信息论：九人工六位联合变量世界、576全来源、精确log符号运算和条件互信息反例；评分前冻结

日期2026-10-23 Asia/Taipei。原239目录已核 `11-012 Entropy and Information Theory`（P1），研究编号R252。项目先完成全部原R，再归纳分类，最后熔炼；R073/PESEN v0.1冻结；真人E2和真实历史E3新增0。

## 一手理论

Claude E. Shannon (1948), [*A Mathematical Theory of Communication*](https://doi.org/10.1002/j.1538-7305.1948.tb01338.x), *Bell System Technical Journal* 27(3):379–423，及[part II](https://doi.org/10.1002/j.1538-7305.1948.tb00917.x), 27(4):623–656。对有限联合分布，`H(X)=−Σ_x p(x)log₂ p(x)`，`I(X;Y)=H(X)+H(Y)−H(X,Y)`，`I(X;Y|Z)=H(X,Z)+H(Y,Z)−H(Z)−H(X,Y,Z)`。所有人造源权重1/64；**每个精确熵都须保存为有理系数与log₂整数素数的有限线性组合，而不是将浮点近似冒称精确数学**。所有真实数据新增0，互信息≠因果信息、观察相关≠干预响应、对称信息≠心理语义“理解”。

## 完整六位人工原来源

全source`(U,A,B,C,D,E)∈{0,1}^6`，各位独立公平，9world×64=**576条完整原来源**、每源1/64。每world保存六原bit、观察变量X,Y,Z（Y允许值2表示擦除）、oracle do(X←1−X) 后的Y反事实值、结构名字与原质量。实际可观测只(X,Y,Z)，不能把U、A…E与生成器反事实当作真人观测数据。U/D/E某些world未影响输出，完整保留源，但不冒称64条不同观察路径。

## 九预冻结世界

1. `INDEPENDENT_BITS` X=A,Y=B,Z=C；三变量完全独立，所有单个熵1，I(X;Y)=I(X;Y|Z)=0，联合熵3。
2. `DIRECT_COPY` X=A，Y=X，Z=C；I(X;Y)=I(X;Y|Z)=1、H(X,Y,Z)=2；干预do(X←1−A)时Y也随之翻转。
3. `HIDDEN_COMMON_CAUSE_ALIAS` X=A，Y=A由共同未观察父变量A独立生成（无X→Y箭头），Z=C；每相同全六位原source可见X,Y,Z与DIRECT_COPY**完全同值**，但对do(X←1−A)的Y仍等于A；说明完全相同的观测联合分布和信息统计不能单独区分X→Y与共同原因A→X,A→Y。这里A为人工外生源，只是因其未给观察者才叫隐藏。
4. `XOR_SYNERGY` X=A,Y=B,Z=A XOR B；I(X;Y)=0，I(X;Y|Z)=1；两个原本独立二元变量可在给定其XOR后变得完全相关。
5. `ERASURE_HALF` X=A，Y=A if C=1 else symbol2，Z=C；H(Y)=3/2，I(X;Y)=1/2，I(X;Y|Z)=1/2。不可将擦除值2误当正常二元事件值。
6. `BINARY_SYMMETRIC_QUARTER` X=A，Y=A XOR (B AND C)，Z=B；总体P(Y≠X)=1/4，`I(X;Y)=1−H_b(1/4)=(3/4)log₂3−1`比特（非有理，保留符号），`I(X;Y|Z)=1/2`。
7. `COLLIDER_AND` X=A,Y=B,Z=A AND B；I(X;Y)=0，给定碰撞结果Z后`I(X;Y|Z)=(3/4)log₂3−1>0`（不要把碰撞选择引起的条件依赖称作因果传播）。
8. `XOR_MASK_REPARAM` X=A,Y=A XOR B,Z=B；与XOR_SYNERGY的(X,Y,Z)**整观察联合分布完全一样**（四条偶校验三位模式各概率1/4），但对每个相同A,B人工source的Y生成结构不同；条件I(X;Y|Z)=1、无条件I(X;Y)=0。相同分布不能唯一推断生成方向。
9. `CONSTANT_REPORTER` X=A,Y=0,Z=C；H(Y)=0，I(X;Y)=I(X;Y|Z)=0，观察通道可完全丢弃X信息而不改变其边际H(X)=1。

## 精确熵代数与验收边界

A. 原路线穷举全部64公平六bit，根据人工结构输出(X,Y,Z)、do反事实；边缘化计算完整联合PMF p(x,y,z)，再计算各1、2、3元联合熵。任意概率质量都是计数n/64，故`H=6−Σ (n/64)log₂ n`；将每个n做小整数素因子分解，log₂ 2精确折入有理常数，其余log₂素数以Fraction符号系数保存。**原始数学验收比较符号系数完全相等**，使用math.log2只是便于报告近似，不充当符号证明。
B. 第二路线**不读取source原bit/模拟器**，按每个world事前独立列举完整理论p(X,Y,Z)：INDEPENDENT全8三元模式质量1/8；DIRECT/COMMON 4种(x,x,z)各1/4；XOR/XOR_MASK四个满足z=x XOR y的三元模式各1/4；ERASURE四种（z=0,y=2或z=1,y=x）各1/4；BSC：z=0,y=x各1/4；z=1,y=x各1/8、z=1,y≠x各1/8；COLLIDER四个(x,y,z=x AND y)各1/4；CONSTANT四个(x,0,z)各1/4。独立理论完整观察PMF与全部原source积分逐格严格Fraction相等。
C. 依据完整PMF，独立生成H(X),H(Y),H(Z),H(XY),H(XZ),H(YZ),H(XYZ),I(X;Y),I(X;Y|Z),I(X;Z),I(Y;Z)，及interaction=I(X;Y)−I(X;Y|Z)。用符号运算精确检验上述冻结反例以及链式`H(XYZ)=H(Z)+H(XY|Z)`等恒等式；符号表达式`(3/4)log₂3−1`严格正，可用`3³=27>16=2⁴`比较证明，不能把浮点1e-16残差误判为信息依赖。
D. 干预比较只在人工结构真值Oracle单独报告，特别DIRECT_COPY与HIDDEN_COMMON_CAUSE_ALIAS的观察(X,Y,Z)逐source完全等价，而Y在人工do(X←1−X)下的反事实不同；不得用观察I的数值推断现实因果效应。
E. XOR_SYNERGY与XOR_MASK_REPARAM在完整观测三元PMF分布等价，却来自不同字母结构方程。XOR/COLLIDER条件互信息大于无条件，并不违反信息处理不等式：条件事件能够制造或揭示依赖，不能将条件互信息机械解释为传播增益。
F. 原576完整六位source、符号熵及独立PMF来源JSON、SHA256必须由GitHub Actions在Python3.11/3.12各≥45实际单测，第三独立job验证全部源、独立概率、所有冻结信息恒等式、干预Oracle、SHA并永久提交main后，才能标记有限数学E1正式结题。下一原目录11-013 Information Cascade（R253）须保持顺序。
