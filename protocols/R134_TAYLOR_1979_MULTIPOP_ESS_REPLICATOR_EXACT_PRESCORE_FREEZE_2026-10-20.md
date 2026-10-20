# R134 计算前冻结：Taylor 1979 两类参与者 ESS 和跨群体复制子动力学

日期：2026-10-20；原目录 P2 / 05-010 Multi Population Evolutionary Games。下一项 R135 的序号延续既有R，原目录候选待下一期核对。

## 第一手原刊与核验页

Peter D. Taylor (1979), Evolutionarily Stable Strategies with Two Types of Player, Journal of Applied Probability 16(1):76–83; https://doi.org/10.2307/3213376 ，作者本人公开书目 https://sites.google.com/view/peter-taylor/biology/publications 的1979对应PDF https://static1.squarespace.com/static/5dc9917c4cdb1467e1e54c4c/t/6526a06fa3fe7456d63dd68d/1697030256664/1979%2Bevolutionarily%2Bstable%2Bstrategies%2Bwith%2Btwo%2Btypes%2Bof%2Bplayer.pdf 。原印刷77页Eq1及矩阵线性定义、78页Eq2/3/4/5均已逐页直接可视核阅。原1979论文包括更一般的同类型和交叉收益 A,B,C,D、以及79页以后非线性照料时间模型。本阶段准确复验77–78页一般线性与动态；不宣称已复现非线性亲代照料案例。

## 事前固定理论与假设

I、J两类群体内部策略概率 p,q；原刊 p77–78：第I类第i种策略适应度(Ap+Bq)_i，第J类第j种适应度(Cp+Dq)_j。原Eq5分别更新：
p'_i=p_i[(Ap+Bq)_i-p^T(Ap+Bq)]
q'_j=q_j[(Cp+Dq)_j-q^T(Cp+Dq)]。
这需要固定群体归属、每类内部随机比重和线性适应度，没有人口总量随环境改变的效度验证。
对于居民 (p,q)、变异者(r,s)、总入侵份额ε，将 pε=(1−ε)p+εr、qε=(1−ε)q+εs。Eq1的居民相对变异者优势记Δ(ε)：
Δ(ε)=((p−r)ᵀ(Ap+Bq)+(q−s)ᵀ(Cp+Dq))−ε{(r−p)ᵀ[A(r−p)+B(s−q)]+(s−q)ᵀ[C(r−p)+D(s−q)]}。
因此 Δ0>0 或 Δ0=0且二次型Q<0 才可抵抗给定(r,s)，整体 ESS 需抵抗全部可能变异者。对每种测试用独立直接代入原Eq1和展开多项式 Fraction 核验；对有限网格不声称得到一般全局必要充分证明。

冻结数学专用实例：
1. 协同扰动反例 self A=D=[[0,1],[1,0]]、cross B=C=[[2,0],[0,2]]，居民 p=q=(1/2,1/2)。对于任一单群体突变，严格二阶抗入侵，但 r=s=(3/4,1/4) 同时突变，Δ0=0,Q=1/4, Δ(ε)=−ε/4，故失败。两群体Eq5局部切平面 Jacobian [[−1/2,1],[1,−1/2]]，特征值 1/2 与 −3/2；独立给定另一群体各自线性收敛却合起来形成鞍点。此矩阵是**项目自造**，非作者1979论文的亲代实验数据。
2. 纯交叉零和Matching Pennies：A=D=0，B=[[1,-1],[-1,1]]，C=−Bᵀ。各群体内部初始份额x,y，连续dx/dt=2x(1−x)(2y−1)，dy/dt=−2y(1−y)(2x−1)；全内部状态保持 H=x(1−x)y(1−y) 守恒。选初始x=1/5,y=4/5，H=16/625；与x=4/5,y=1/5的同一池化频率z=(x+y)/2=1/2，两个dz/dt恰好符号相反，分别 +24/125 与 −24/125。另x=y=1/2同样z=1/2但dz/dt=0。源1979 Eq5为机制，具体B、C和数值是**项目自设**，本例不证明实际人群存在类似周期。验证双群体连续中心特征根±i。
3. 初始状态及算法舍入不能当真实社会历史。RK4轨迹只需检测数值偏差随步长下降；守恒 H 的数学原式以精确Fraction证明，数值输出本身不可视为精确守恒。

## 预先验收
- Python 3.11/3.12 标准库 Fraction 双路径严算与 unittest。固定有限网格：矩阵 A,B,C,D 每格从一个可审计的有界族取值，状态与变异方向做独立源式与展开式对照；保留每项实际比较数供CI日志。
- 真正 GitHub Actions 执行后方可声称远端测试成功；自动归档代码、测试、科学报告、SHA256证据。
- 新真人/动物逐行原始数据 E2=0、历史真实事件预测 E3=0；不升级理论数学为实际预测效度。
- R073 和 PESEN v0.1 原有冻结维持；全R完成后才汇总分类、熔炼。

状态：FROZEN_BEFORE_R134_PROGRAM_AND_CI。