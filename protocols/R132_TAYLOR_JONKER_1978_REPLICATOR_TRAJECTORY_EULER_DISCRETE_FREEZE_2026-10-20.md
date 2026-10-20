# R132 原刊复制子方程、连续时间轨迹与数值伪灭绝——计算前冻结协议

日期2026-10-20。原模型目录P1 05-008 Replicator Dynamics；R131完成Taylor/Jonker1978两个三策略局部稳定反例，本阶段要研究真实连续路径、吸引域、独立积分交叉检查以及不当数值离散制造的伪灭绝。R133单独专题一般ESS。坚持先完成全部原R系列再分类、最后熔炼；R073/PESEN v0.1冻结。

## 一手源与不可越界的事实

Peter D. Taylor, Leo B. Jonker (1978), Evolutionarily Stable Strategies and Game Dynamics, Mathematical Biosciences 40:145–156, DOI 10.1016/0025-5564(78)90077-9，1978原刊全文 https://public.ek-cer.hu/~szabo/EGT20/library/taylor_mbs78.pdf ，作者出版主页 https://sites.google.com/view/peter-taylor/biology/publications 。**已直接按原刊影像核验印刷p149**：原Eq2连续dx_i/dt=x_i[F_i−Fbar]、原Eq3真正离散世代x_i_next=x_i(1+F_i)/(1+Fbar)、Eq4两者的增量关系；印刷p150原论文比较连续与离散局部稳定及过冲。论文为一般模型来源，并**未测量本项目三款toy的真人/动物数据或真实人口演化轨迹**。Hofbauer/Schuster/Sigmund1979 10.1016/0022-5193(79)90058-4 仅核原书目/摘要，未直接读全文，不作为已复算一手定理。

## 三个明确项目参数而非原刊数值

二人对称矩阵[[a,b],[c,d]]，A占比x，B占比1−x。F_A=ax+b(1−x), F_B=cx+d(1−x)。原Eq2简化f(x)=x(1−x)(alpha*x+beta)，alpha=a−b−c+d, beta=b−d。

Hawk-Dove项目基于R129矩阵[[-2,2],[0,1]]，alpha=−3,beta=1，内点1/3在连续动力全内部初值下稳定。Stag-Hunt项目基于R128矩阵[[4,0],[3,3]]，alpha=4,beta=−3，内部门3/4，低于门向0、高于门向1。另完全新设Logistic控制矩阵[[2,2],[1,1]]，alpha=0,beta=1，显式真解x(t)=1/(1+[(1−x0)/x0]*exp(−t))。各矩阵是项目纯数学参数，不冒充Taylor1978原199?行为观察。没有随机匹配/一致信念假设时，人口比例x不能自动等同个人主观信任概率q。

## 两条不互相调用的连续轨迹计算

方法A：严格双精度固定步长RK4，真实各子步的x必须在[0,1]，不作clamp。方法B：按微分方程分离变量，beta及alpha+beta非零时确切积分原函数
G(x)=(1/beta)*ln(x)−[1/(alpha+beta)]*ln(1−x)−[alpha/(beta*(alpha+beta))]*ln|alpha*x+beta|，
其在不含固定点的分支有G(x(t))−G(x0)=t。对Hawk与Stag通过独立单调二分反求x(t)，对Logistic用显式闭式求x(t)（与RK4不互相调用）；遇固定点0、1、Hawk内部1/3、Stag内部3/4则返回静止轨迹。三款游戏×6初始份额{1/10,1/4,2/5,3/5,4/5,9/10}×12时间{1/4,1/2,1,2,3,4,5,6,8,10,12,16}共**216个独立真解对照**，RK4步长≤1/120且误差≤10^-6。显式记录所有观察最大误差；不把数值近似写为数学恒等。

## 原Eq3与研究者Euler数值器不是同一种系统

显式Euler仅仅近似原连续Eq2：x_next=x+h*x(1−x)(1−3x)；项目Hawk x0=1/2，原真实瞬时导数−1/8，数值步长h=4错误地产生x1=0“灭绝”。真实连续解在任何有限t内始终保留x(t)>1/3，不能一次触到0。Hawk内点1/3的连续局部线性因子f'=-2/3，Euler线性倍率1−2h/3，h=1倍率1/3稳定但h=4倍率−5/3局部不稳。**严禁把Euler误标原Taylor1978的Eq3，严禁把负概率clamp再称合法复制子解**。

对原Eq3：保持项目Hawk原行支付矩阵并把全部四支付加同样k。原连续Eq2因只依赖F_A−F_B不变，但原离散Eq3的分母1+Fbar+k不同。固定x0=1/2，k=0真实原Eq3一步=**2/5**，k=3一步=**8/17**。在某些原支付状态，1+F_H<0，出生倍数非法必须fail closed；只在两种潜在策略倍数都非负且总倍数>0的范围使用Eq3，不应偷偷补充背景增长、归一化或更改原1978源式。比较不同k时，**不能**称两种原离散出生机制完全相同。

## 验收门与证据

独立确切Fraction两路径验证连续场：一条按单个支付F_A和Fbar算xdot，另一条直接用三次多项式，3矩阵×x=k/24 k=0..24=**75个精确比较**；独立以原Eq3和Eq4关系核对离散增量。216个数值连续轨迹端点的RK4与解析隐式/显式解误差，分支方向和边界吸收测试；Euler伪灭绝及原离散出生k=0/3差异。所有非法float/bool、负时间、非法概率、Euler越界等失败拒绝。≥50项真正Python标准库unittest。真实GitHub CI成功后自动提交代码、测试、科研报告3个SHA256及机器收据，再独立GitHub main回读后才能限定结题，状态LEARNING_COMPLETE_BOUNDED_TAYLOR_JONKER_1978_REPLICATOR_TRAJECTORY_BASINS_AND_NUMERICAL_ARTIFACTS。此研究**无真人新E2=0、历史预测E3=0**，不复现1978全部三策略相图，R073/PESEN v0.1冻结。
