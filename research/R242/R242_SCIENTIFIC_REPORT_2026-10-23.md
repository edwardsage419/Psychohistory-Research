# R242 差分方程：九人工离散动力世界、180全初值来源与递推观测不可识别

日期2026-10-23 Asia/Taipei。实际239目录 `11-002 Difference Equations`（P0）。正式科学状态 `CLOSED_BOUNDED_E1_EXACT_DISCRETE_DIFFERENCE_SENSOR_ALIAS`。全部结论为冻结有限人工方程的精确计算，不涉及真实人口代际、历史序列或人类行为预测；新增真人E2和历史E3均为0。

## 原著、模型冻结与科学边界

May (1976), [*Simple mathematical models with very complicated dynamics*](https://www.nature.com/articles/261459a0), *Nature* 261:459–467, DOI [10.1038/261459a0](https://doi.org/10.1038/261459a0)，研究简单离散非线性映射产生的复杂动力表现；Strogatz *Nonlinear Dynamics and Chaos*（CRC Press）介绍迭代映射、固定点及其稳定性和分岔。当前R没有复现原作者真实生态或社会数据，也没有对长时期混沌、Lyapunov指数或实际分岔阈值做经验结论，仅构建有限4步、4初值、2参数的精确有理数数学反例。

[代码及评分前协议](../../protocols/R242_DIFFERENCE_EQUATIONS_9_FINITE_WORLDS_180_SOURCES_PRESCORE_FREEZE_2026-10-23.md)先行提交 [89a2a8d3](https://github.com/edwardsage419/Psychohistory-Research/commit/89a2a8d3a4166541bf34ed9a0fdf5fda52cc7762)，然后再提交Python计算与CI。冻结九种模型、完整原来源、递推半群、完整可见联合及三组别名条件均保持不变。

## 九机制、全集与双重数学复算

固定原初值`x0={1/4,1/2,3/4,1}`和离散时间`n={0,1,2,3,4}`，每world 20原有理初值×时间人工类型，各结构质量1/20，九world共**180条完整原来源**，均有严格正质量且各world原概率和1。注意这些是假定数学格点而不是180个真人样本或某个自然科学实验重复次数。

真实隐藏状态`h_n`服从冻结映射`h_{n+1}=f(h_n)`，实际观察`y_n=g(n,h_n)`可能因时间而异或非线性。第一路线从隐藏起点按冻结f逐步迭代，并用链式法则`∂h_{n+1}/∂x0=f'(h_n)∂h_n/∂x0`，结合各传感器g输出可见y和初值灵敏度。独立验证路线**不读取原来源**，用精确有理数一元多项式复合构造`f^{\circ n}`，再用Horner公式计算h和解析多项式导数，由观测映射转换成独立可见灵敏度。全部九世界四初值五时点**观察数值与灵敏度逐格一致**。对所有n,m且n+m≤4精确验证真隐藏自治映射的半群`f^{n+m}=f^m\circ f^n`，绝不把时变可见传感器误指认为隐藏自主动力。

九world：CONTRACTION_HALF的f(h)=h/2；CONTRACTION_SENSOR_ALIAS的隐藏f(h)=h而可见y=2^(-n)h；CONTRACTION_DOUBLE_COORDINATE_ALIAS的隐藏h0=2x0、f(h)=h/2、可见y=h/2；EXPANSION_DOUBLE的f(h)=2h；EXPANSION_SENSOR_ALIAS的隐藏f(h)=h而可见y=2^n h；SIGN_FLIP_SQUARED_SENSOR的f(h)=−h、可见y=h²；STATIONARY_SQUARED_SENSOR的f(h)=h、可见y=h²；LOGISTIC_R2的f(h)=2h(1−h)；LOGISTIC_R4的f(h)=4h(1−h)。

## 主要独立识别反例

**完整衰减观察等价（三机制）：** 对任一x0与全部n=0…4，前面三种收缩机制的可见输出严格等于`y_n=x0/2^n`，且全部可见初值灵敏度`2^{-n}`相同。以x0=1,n=4为例，三个实际可见值全是1/16，但隐藏h_4分别1/16、1、1/8，差异来自真衰减、隐藏恒定但动态传感器和单纯隐藏表征双倍单位。因前两机制有同一观察流，不能仅凭完整有限可见序列证明真实内部状态已经衰减；隐藏双倍世界则仅是单位坐标变化，不能作为另一种经验动力现象。

**完整扩张观察等价（两机制）：** EXPANSION_DOUBLE的真正隐藏递推h_{n+1}=2h_n，使x0=1到n=4变为16；EXPANSION_SENSOR_ALIAS的隐藏值始终为1，只有可见传感器随n乘2^n。两世界完整`P(x0,n,y_n)`逐原来源一致、所有可见初值灵敏度也一致，但隐藏状态扩张与否不同。

**非单射观测隐藏内部振荡：** SIGN_FLIP_SQUARED_SENSOR每步隐藏状态符号颠倒，x0=1时h_n依次1,−1,1,−1,1，传感器输出y=h²却始终1。STATIONARY_SQUARED_SENSOR隐藏h_n始终1，实际传感器输出同样始终1。两世界对全部初值时点及可见灵敏度`2x0`完全观察等价，但内部真实变化完全不同。该识别失败明确依赖平方观测无法区别隐藏正负值；具独立符号测量时并不适用。

**logistic 非线性与有限初值稳定性：** LOGISTIC_R2的初值x0=1/2严格固定在1/2，全四个未来步不变。LOGISTIC_R4的x0=1/2则取值(1/2,1,0,0,0)，x0=1/4取(1/4,3/4,3/4,3/4,3/4)。在r=4、x0=1/2时，第一步对初值的微分敏感度`4(1−2x0)=0`，以后链式乘积也为0；但是有限非零初值扰动仍可通过二阶项产生非零轨道差异，不能凭一次导数为0宣称普遍稳健。所有有限轨道是**四步精确结果，不是长期混沌统计证据**。

全部人工机制可以在观察层面生成相同的离散序列而隐藏动力不同，结论只对冻结可见传感器和构造初值支撑成立。不能据此一概否定真实世界在测量可信、有外部干预、长时间数据和有效动态限制下的机制识别。

## GitHub完整源、实际CI及结题

[原生Fraction精确源码](r242_exact_difference_equations.py) · [全180来源原CSV](R242_ALL_180_ORIGINAL_DIFFERENCE_EQUATION_ATOMS.csv) · [九机制完整可见/隐藏/灵敏度JSON](R242_EXACT_RESULTS.json) · [机器SHA256收据](R242_FINAL_MACHINE_ACCEPTANCE.json)。

[CI run39889143138](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39889143138)总体completed/success，三job均completed/success；Python3.11及3.12日志各`Ran 85 tests`、`OK`，共**170次实际测试通过**。第三归档作业独立核验九机制×20全部原源、原质量、logistic有理固定点与四步轨道、三全观察等价族及可见初值灵敏度、源文件SHA，真实日志输出`R242_180_ALL_ORIGINAL_FINITE_DIFFERENCE_ATOMS_AND_POLYNOMIAL_ALIASES_VERIFIED`；全部原CSV/JSON/机器收据已由机器人永久归档main，提交 [44f0bd90](https://github.com/edwardsage419/Psychohistory-Research/commit/44f0bd903d094175306348a24f5f6be8505e1336)。

全源CSV SHA256 `1d237f54ff1e9458127e4891aae8d3132b93e1da5830f6ef2bc2dc19e810136f`，全结果JSON SHA256 `b6c859d678f875c1cbe47c7ed46fbd45ad0f45088caffb50932fdd6382857995`。

当前结论为`CLOSED_BOUNDED_E1_EXACT_DISCRETE_DIFFERENCE_SENSOR_ALIAS`。没有实施真实历史离散社会演化模型估计、模型之间的样本外比较或长期预测，新增真人E2=0、真实历史E3=0；R073及PESEN v0.1仍冻结。

下一原目录 `11-003 Stochastic Differential Equations`（P2），编号拟R243。全原R先完成，再统一归纳分类，最后熔炼原创体系。
