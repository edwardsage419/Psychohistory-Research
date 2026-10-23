# R241 常微分方程：九人工有理精确初值流、180完整原轨道点与真实状态—动态测量观察等价；事前冻结

日期2026-10-23（Asia/Taipei）。原始239目录真实 `11-001 Ordinary Differential Equations`（P0），正式连续研究编号R241。此前R239、R240已完成有限研究。本项建立一维非线性常微分方程的明确解、局部唯一性适用域、原初值敏感性、连续时间流半群以及无法仅据完整可见轨道判定是否真状态改变的人工机制。全部人工E1，新增真人E2和真实历史E3均0；R073/PESEN v0.1冻结。尚不合并任何模型。

## 原生方法与数学事实边界

MIT OpenCourseWare 18.03SC [*Basic DE's and Separable Equations*](https://ocw.mit.edu/courses/18-03sc-differential-equations-fall-2011/pages/unit-i-first-order-differential-equations/basic-de-and-separable-equations/) 和 MIT 18.100B [*Existence & Uniqueness for ODEs: Picard–Lindelöf Theorem*](https://learn.mit.edu/?resource=17174&resource_title=lecture-22-differentiating-and-integrating-power-series) 讲授分离变量、初值解、局部唯一性。人工函数右端为常数函数或二次多项式，任意有限有界状态附近局部Lipschitz，因此经典局部唯一性适用；不能由此断言增长二次ODE全时间有界或全球唯一延拓。非线性增长`x'=x²`可在`t*=1/x0`有限时间发散，本研究对所有初值只在安全时间范围检验。

## 冻结初值 × 采样时间 × 机制全集

同一人工cohort初值 `x0∈{1/4,1/2,3/4,1}`，人工time `t∈{0,1/8,1/4,3/8,1/2}`，每world 4×5=**20条完整唯一人工观测轨道来源**，每来源概率/结构权重1/20，九世界**180条**。这些“时间采样点”不是180个真实时间序列观测者，也不是历史资料。每原源保留真实oracle hidden state`h(t)`及真ODE rhs、真解析导数，实际观察数值`y(t)`、人工cohort初值索引及time、传感器观测导数、可见初值灵敏度。精确Fraction，不用浮点ODE解算器。

## 九个完整人工ODE与观测机制

1. `DECAY_L1`: h'=−h²，h(0)=x0，`h(t)=x0/(1+x0 t)`，y=h。
2. `DECAY_L2`: h'=−2h²，h(0)=x0，`h(t)=x0/(1+2x0 t)`，y=h。
3. `DECAY_HIDDEN_DOUBLE_COORDINATE`: h'=−h²/2，h(0)=2x0，`h(t)=2x0/(1+x0 t)`，y=h/2。全可见y与1逐初值、逐时间完全相同，但隐藏状态单位不同；**仅人工坐标重参数化，不是实际潜在动力学改变证据**。
4. `CONSTANT_STATE_TIME_DRIFT_SENSOR_DECAY`: h'=0，h(0)=x0，h(t)=x0；观察传感器随时间改变`y=h/(1+h t)`。其整条有理观察轨道和1、3逐原点完全相同，但真隐藏h没有变化。该观测等价依赖传感器明确允许时间漂移；不能在外部已校准不变传感器的模型下随意使用此别名。
5. `GROWTH_L1`: h'=+h²，h(0)=x0，`h(t)=x0/(1−x0 t)`，在t<1/x0有效，最小发散时间1；y=h，全部冻结时点≤1/2均有效。
6. `CONSTANT_STATE_TIME_DRIFT_SENSOR_GROWTH`: h'=0，h(0)=x0，观察传感器`y=h/(1−h t)`，全部冻结时点与5完整观察轨道同分布，隐藏真h却恒定；该测量算子自身在t=1/h发散，不能将表面失控自动指认真隐藏状态物理发散。
7. `STATIONARY`: h'=0，h(0)=x0，y=h。
8. `CONSTANT_RATE_PLUS1`: h'=1，h(0)=x0，h(t)=x0+t，y=h。
9. `DECAY_NONLINEAR_SENSOR`: h'=−h²，h(0)=x0，真h同1，但可见y=h²，观测导数`y'=−2h³`而不等于真状态h'。单一观察量的动力规律需要观测映射的chain rule，不能将y和h混用。

## 数学复验、可观察等价与严格范围

A. 逐全部人工来源以冻结显式解精确计算h(t)和y(t)，独立解析微分表达式验证`dh/dt=f(h)`在每原点严格等式，`dy/dt=∂g/∂t+(∂g/∂h)f(h)`与独立直接对显式y公式求导严格相同。独立第二路线按冻结初值与时间直接算实际y而**不读取原源数据**，与来源观察逐字相等。
B. 事先冻结三观察等价组合：DECAY_L1/DECAY_HIDDEN_DOUBLE_COORDINATE/CONSTANT_STATE_TIME_DRIFT_SENSOR_DECAY的整个`P(cohort,t,y)`每格完全一致，且对所有正t的真隐藏h分别随时衰减、单位重标定衰减、严格恒定；GROWTH_L1与CONSTANT_STATE_TIME_DRIFT_SENSOR_GROWTH全部可见轨道逐原点完全一样，但真隐藏h前者增长、后者恒定。
C. 解析初值灵敏度`∂y/∂x0`：一般decay λ为`1/(1+λx0t)²`，growth为`1/(1−x0t)²`，stationary与constant rate为1，非线性sensor为`2x0/(1+x0t)³`；所有别名组合的y初值灵敏度逐时间一致，但真隐藏机制不同。真正oracle衰减初值导数随时间降低，增长型随时间提高。
D. 对全部自主真状态ODE验证流半群`Φ_{t+s}(h0)=Φ_s(Φ_t(h0))`，其中`t,s`来自冻结时间网格且t+s≤1/2；构造解析流`Φ_τ(h)=h/(1+λ h τ)`、增长λ<0可写同型，stationary恒等、constant rate加τ；两漂移sensor世界只针对真实恒定状态半群，不把随时间变的观察映射伪装为自主真状态流。
E. GROWTH_L1在x0=1时真解析发散时间t*=1，人工冻结样本最大t=1/2；数值轨道外推t≥1不在定义域内。显示有限截面拟合即使在全部样本点精确成功，不会自动识别机制、传感器变化或外推有效时间域。
F. 全180人工来源CSV、各世界全轨道、观察联合、真状态与观察导数、semigroup、初值灵敏度JSON及SHA256。双Python3.11/3.12各≥45项单测，第三独立原源验收job验证上列要求与SHA并机器人永久归档main，成功后才发布正式报告与结题。
G. 仅有限人工E1、没有人口调查、复杂系统真实参数拟合、历史轨道证据、微分方程求解器稳定性误差界或未来社会预测。下一原239目录需核验 `11-002`，不提前改研究顺序。
