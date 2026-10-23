# R241 常微分方程：九个精确有理初值世界、180完整轨道来源与真实动力—传感器漂移不可识别

日期2026-10-23（Asia/Taipei）。原239目录 `11-001 Ordinary Differential Equations` **P0**，科学资格 `CLOSED_BOUNDED_E1_EXACT_RATIONAL_ODE_IVP_FLOW_SENSOR_ALIASES`。只研究完全设定的人工一维微分方程、有限四初值五时间网格及冻结观测测量函数。没有实际心理动态、真实社会历史时间序列、长期预测验证、微分方程数值求解器比较或真人E2/历史E3资料。

## 方法依据、真正数学结论与事前冻结

MIT OpenCourseWare [*18.03SC Basic DE's and Separable Equations*](https://ocw.mit.edu/courses/18-03sc-differential-equations-fall-2011/pages/unit-i-first-order-differential-equations/basic-de-and-separable-equations/) 介绍分离变量、初值问题及非线性解爆破；MIT [*18.100B Lecture 23: Existence & Uniqueness for ODEs*](https://learn.mit.edu/?resource=17174&resource_title=lecture-22-differentiating-and-integrating-power-series) 讨论Picard–Lindelöf型局部初值唯一性。本研究限定的原始右端`f(h)=−h²,−2h²,−h²/2,+h²,0,1`是多项式/常数函数，在任何有限有界区域局部Lipschitz；因此相应初值问题在明示的适当定义域内局部唯一。不能用局部唯一性声称对非线性增长ODE获得全时间有界解；本研究明示最早奇点时限。

[九个ODE和全部180时间来源评分前协议](../../protocols/R241_ODE_9_EXACT_IVP_WORLDS_180_FULL_SOURCE_TIMES_PRESCORE_FREEZE_2026-10-23.md)独立先提交 [65ca4f2c](https://github.com/edwardsage419/Psychohistory-Research/commit/65ca4f2cd300e911d68b624f7d7678936eafe50f)，随后才提交模型代码、CI工作流与全部原生成来源。参数、观察别名、数学导数和时间域全部来自前置冻结，不因运行结果更换假说。

## 精确初值源与两个独立求解路径

冻结四人工初值`x0∈{1/4,1/2,3/4,1}`、五时点`t∈{0,1/8,1/4,3/8,1/2}`，每世界4×5=20个完整cohort/时点人工来源，每个结构权重1/20，九世界合计**180条**。每源实际观察列为(cohort_x0,time,visible_y)、该可见y的解析时间导数和对初值敏感度；另在明确标注的人工Oracle列保存真实隐藏状态h(t)、其真实ODE右端f(h)、真实解析导数及隐藏状态变化。任何实际观察识别流程不能直接读取Oracle。

第一路线从冻结初值h0和ODE显式状态流`Φ_t(h)`算hidden h(t)，通过可见测量映射`g(t,h)`得到y(t)，按chain rule独立计算观察`y_t=g_t+g_h f(h)`。第二路线完全不调用隐藏状态流/观察传感器函数，直接从每一种world事前固定的有理式计算观察y(t)及其对时间直接求导；逐世界、全部20原时点二者严格Fraction逐项相同。此外再从解析ODE的真流`Φ_{t+s}(h0)=Φ_s(Φ_t(h0))`检查一切冻结时点t,s且t+s≤1/2的半群关系，真实隐藏状态确切满足；由于随时间变化的传感器不一定自主，不能把此隐藏流性质冒称为可见y的自主因果动力识别证明。

## 九个人工机制与真轨道

1. `DECAY_L1`：真实h'=-h²，h0=x0，观察y=h=`x0/(1+x0t)`。
2. `DECAY_L2`：真实h'=-2h²，y=h=`x0/(1+2x0t)`。
3. `DECAY_HIDDEN_DOUBLE_COORDINATE`：真h'=-h²/2，h0=2x0、h(t)=`2x0/(1+x0t)`，实际观察y=h/2，整个可见轨道与1完全相同，是**单纯潜在单位重标定**，非不同真实心理动力学证据。
4. `CONSTANT_STATE_TIME_DRIFT_SENSOR_DECAY`：真h'=0、h(t)=x0完全不动，观测传感器随时间漂移`y=h/(1+h t)`，整个可见轨道却与1、3逐原来源严格相同，真实隐藏状态变化为0。
5. `GROWTH_L1`：真h'=+h²、y=h=`x0/(1−x0 t)`，只在t<1/x0成立。全部冻结初值最早爆破时间为t*=1（初值x0=1）。
6. `CONSTANT_STATE_TIME_DRIFT_SENSOR_GROWTH`：真h'=0、h(t)=x0，观测`y=h/(1−h t)`。全部可见轨道与5相同，但隐藏真状态完全不动。观测映射本身在t=1/h发生极点，不应把可见测量爆破等同真物理状态爆破。
7. `STATIONARY`：真h'=0、y=h=x0。
8. `CONSTANT_RATE_PLUS1`：真h'=1、y=h=x0+t。
9. `DECAY_NONLINEAR_SENSOR`：真h'=-h²、真实h同1，但可见y=h²=`(x0/(1+x0 t))²`，所以观察导数不是状态f(h)，而是`dy/dt=-2h³`。

## 关键独立等式、来源检验和识别界限

**全观察等价族一：真实衰减与纯观测漂移。** `DECAY_L1`、`DECAY_HIDDEN_DOUBLE_COORDINATE`及`CONSTANT_STATE_TIME_DRIFT_SENSOR_DECAY`三个世界完整20种`(cohort,t,y)`联合概率逐格一致，所有实际观察变量、全部四初值来源、五时点及解析可见时间导数与初值敏感度也逐项一致。但是对初值x0=1的t=1/2，三者真实隐藏h分别2/3、4/3、1，隐藏变化分别−1/3、−2/3、0。由于模型允许随时间变的传感器，**即使观测轨道连续时间公式完全相同**，它也不独立识别隐藏状态真的衰减还是观测映射发生动态变化。独立传感器校准能排除某些别名，本研究没有模拟这样的独立外部校验。

**全观察等价族二：真实有限时增长与观测仪器的伪增长。** `GROWTH_L1`与`CONSTANT_STATE_TIME_DRIFT_SENSOR_GROWTH`在全部四初值、五时点显示同一完整观察轨道`x0/(1−x0t)`；前者真隐藏h上升，后者真实h严格恒定。x0=1、t=1/2时两者可见y都由1升至2，真实h变化分别+1与0；观察对初值敏感度均4。真正`h'=h²`解在x0=1下t→1−时增长无界，第二世界则是传感器自身在t→1−奇异，不是隐藏状态增长。由可见函数无法直接决定哪个物理机制真实，**但此反例明确依赖可以变化、甚至存在极点的测量机制**。

**数学初值敏感度：** 一般衰减`y=x0/(1+λx0t)`有`∂y/∂x0=1/(1+λx0t)²`，冻结t≥0时≤1；增长`y=x0/(1−x0t)`有`∂y/∂x0=1/(1−x0t)²`，冻结正时间时>1。对于x0=1,t=1/2，DECAY_L1可见初值敏感度4/9，DECAY_L2为1/4，GROWTH_L1为4。真实衰减与纯动态传感器别名的可见初值敏感度完全相同，不能作为隐藏状态机制的独立识别工具。非线性传感器y=h²则有`∂y/∂x0=2x0/(1+x0t)^3`，如果不知道测量映射就不能把观察的灵敏度直接解释为真实状态扰动。

**半群、局部唯一性与外推定义域：** 九个真隐藏ODE均为自治方程，全部冻结安全时间的流半群精确相符，解析导数与多项式/常数f(h)严格逐原源一致。对于GROWTH_L1，x0=1下的显式解`h(t)=1/(1−t)`只在t<1可成立；所有历史样本支持只有t≤1/2，不能把已经观察的前半时间拟合当作**任意晚期演化可预测性**。两个真机制虽共享可见轨道，但若能独立确认测量函数时间不变，别名比较的允许集合就不同。本研究只在这些特定假设边界下提出有限识别结论。

## 真实GitHub复验、机器SHA与科研资格

[完全可复现Python Fraction源码](r241_exact_rational_ode_ivp.py) · [全180条人工初值—时间原CSV](R241_ALL_180_EXACT_ODE_IVP_TIME_SOURCES.csv) · [九世界完整轨道/导数/敏感度/Oracle JSON](R241_EXACT_RESULTS.json) · [原来源SHA256机器收据](R241_FINAL_MACHINE_ACCEPTANCE.json)。

[GitHub Actions run39887913848](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39887913848)已核验总体completed/success、三job均completed/success；Python3.11及3.12真实日志各`Ran 85 tests`、`OK`，共**170次真实单元测试执行通过**。第三完整原源作业独立重算每世界20个全异初值时间组合、确切1/20概率、全部source中的h'与f(h)、所有隐藏半群及两个连续观察轨道别名、非线性测量导数、增长的最早奇点、全部原文件SHA，真实日志输出`R241_ALL_180_EXACT_ODE_ORIGINAL_SOURCES_SENSOR_ALIASES_AND_FLOW_SEMIGROUP_VERIFIED`。机器人把全部180原源/全部结果/SHA永久提交main，[60c29562](https://github.com/edwardsage419/Psychohistory-Research/commit/60c29562a33f95469217d8b81f137abc9c028c8c)。

全原CSV SHA256 `bfabe0b899e2cdce6e7587b7fa9affbedb3ee7cb71645d6ab9ca835ad5081ab2`；九世界结果JSON SHA256 `2f3c2428ce4778473ea2ec15eda78d01869d89a259aa4edacdfbb68806bcf903`。

全部结论仅人工数学E1，不构成真实心理制度群体长期变化的因果机制识别、真实ODE参数估计或历史事件外推。新真人E2=0、历史E3=0，R073与PESEN v0.1继续冻结。下一原239候选目录须按实际模型索引核验11-002，研究编号拟R242。原所有者方向：先完成全部R模型学习与有限研究，再统一归纳分类，最后正式熔炼。
