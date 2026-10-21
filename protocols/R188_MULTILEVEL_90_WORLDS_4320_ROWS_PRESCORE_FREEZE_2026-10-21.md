# R188 多层线性模型：180个人工六群组世界、8640行、720组固定准去均值拟合，计算前冻结

> **算术更正记录，2026-10-21**：保留原冻结协议文件名中历史的90/4320编号供追溯。原始Cartesian全因子集合完整乘积为180个人工世界、8640行、720个θ拟合。原始冻结提交为`08276a5ae3769e64b3f00d6ac39a8eab8b717754`，首次CI `39565973693` 因原数量常量错误失败，正式结果尚未产生。参见 [R188计算前算术更正审计](R188_PRE_SCORE_FACTORIAL_ARITHMETIC_ERRATUM_2026-10-21.md)。所有固定参数、评价方法及接受标准保持原设定，订正仅改变数量常量。

日期2026-10-21。原候选目录 P0/08-012 Multilevel Linear Models。状态 PRESCORE_FROZEN_E1_ARTIFICIAL_EXACT_HIERARCHICAL_LINEAR。协议必须先于任何完整R188评分、挑选情景或修改验收标准入库main。各级数据全部由明确有理数公式人工生成，未估计真实社会群体随机效应、未复现原作者数据或历史案例。

## 一手研究背景

1. Mundlak (1978), *On the Pooling of Time Series and Cross Section Data*, Econometrica 46(1):69–85, https://doi.org/10.2307/1913646，探讨将单位内、单位间差异联结的面板合并处理。
2. Laird and Ware (1982), *Random-Effects Models for Longitudinal Data*, Biometrics 38(4):963–974, PubMed https://pubmed.ncbi.nlm.nih.gov/7168798/，阐述每个单位内相关观测及二层随机效应的建模动机。
3. Bell and Jones (2015), *Explaining Fixed Effects: Random Effects Modeling of Time-Series Cross-Sectional and Panel Data*, Political Science Research and Methods 3(1):133–153, https://doi.org/10.1017/psrm.2014.7，明确区分组内、组间关联及群组效应与解释变量相关时的模型假设。本轮采用受控精确线性投影与准去均值敏感性**演示**；不声称实现完整随机截距模型的似然估计或方差组件估计。

## 六群组人工原始数据与完整180个世界

每个人工世界严格含G=6个带身份的群组，每组n=8个二元暴露x∈{0,1}个体。三种固定群组暴露次数设计，每个群组的x=1人数依次为：
* BALANCED: (4,4,4,4,4,4)；
* WEAK_BETWEEN: (2,2,4,4,6,6)；
* STRONG_BETWEEN: (2,2,2,6,6,6)。

所有组内暴露次数与未暴露次数均为正偶数，以便在每个(group,x)细胞内严格构造一半误差为+e、另一半为−e，从而使误差对所有群组和暴露单元的加总、交叉积都严格为0。人工连续响应
`y_ig = a + b*x_ig + c*xbar_g + eps_ig`，
其中`xbar_g`是群组内部x=1比例；参数a∈{0,1}, b∈{1/4,1/2}严格为正，群体水平系数c∈{−4,−2,0,2,4}，误差幅度e∈{0,1/4,1/2}。3设计×2a×2b×5c×3e=**180组完整人工世界**，每组48条带group ID和各层变量的原始数据，合计**8640条完整人工记录**。不能当作真人或实测样本，也不将eps的对称设定误称为随机效应真实估计。

## 冻结的四种层级解析与四档准去均值

对每个180人工世界，固定计算：

1. POOLED，带截距的个体层单变量OLS`y~x`，直接比较x=1/0条件均值；另以独立Fraction正规方程解出系数，逐项精确一致。
2. WITHIN_FE，群组固定截距的组内最小二乘斜率`β_FE=∑(x_ig−xbar_g)(y_ig−ybar_g)/∑(x_ig−xbar_g)²`；第二路径在每个群组对二元x分别求两类y条件均值差，并以`k_g(n−k_g)/n`作权重计算，必须与直接组内去均值Fraction一致。
3. BETWEEN，等群组权重回归群组均值`ybar_g~xbar_g`，并用两个独立公式协方差比与正规方程复核；若设计BALANCED所有xbar都相同，明确返回`UNIDENTIFIED_NO_BETWEEN_VARIATION`，禁止虚构组间斜率。
4. CORRELATED_CONTEXTUAL，原始行上拟合`y~1+x+xbar_g`，仅在xbar随组别变化时有满秩并精确恢复(a,b,c)；BALANCED时因xbar与截距完全共线必须明示不可识别。第二路径由FE斜率与组间斜率之差恢复c，完整代数一致。

为了审查合并模型和固定效应之间的假设敏感性，固定准去均值参数`θ∈{0,1/2,3/4,1}`：`x'_ig=x_ig−θ*xbar_g`, `y'_ig=y_ig−θ*ybar_g`。对θ<1使用带截距的Fraction OLS，在θ=1采用直接组内固定效应的零截距斜率。总共**180世界×4θ=720种斜率敏感性检查**，逐条验证其独立解析表达：

`β_θ=b + c * ((1−θ)² * V_between)/(V_within + (1−θ)² * V_between)`。

这里`V_between=E_g[(xbar_g−mean_x)²]`，`V_within=E_g[xbar_g(1−xbar_g)]`，每组大小相等。θ=0应与POOLED相同，θ=1应与WITHIN_FE相同，BALANCED所有θ斜率均是b。θ=1/2与3/4只是**预先固定的准去均值敏感性**，不是数据推断出的随机截距模型方差，也不把这些系数当作有效随机效应估计。

## 固定数学正反例与潜在层级不可识别

强群组设计STRONG_BETWEEN，锁定a=0, b=1/4, c=−4, e=1/4：

* 每组暴露人数(2,2,2,6,6,6)，真组内斜率b=+1/4。
* V_between=1/16，V_within=3/16。
* POOLED系数`1/4−4*(1/4)=−3/4`，方向与组内正系数相反。
* θ=1/2结果`1/4−4/13=−3/52`；θ=3/4结果`1/4−4/49=33/196`；θ=1恢复+1/4。
* BETWEEN斜率为b+c=−15/4。已知人工真来源条件下CONTEXTUAL调整斜率为+1/4、群组均值系数为−4。三个层级系数所回答的样本构成问题必须区分。
* 限定的负对照：在BALANCED设计中组间自变量完全没有变化，BETWEEN与包含xbar的上下文回归必须判秩不足；全部θ斜率严格=b；任何c都无法从包含任意群组截距的FE观察中单独识别。
* **潜在模型别名**：给定任意人工来源`y=a+b*x+c*xbar+eps`，另一个二层形式`y=a+b*x+u_g+eps`，设置自由组截距`u_g=c*xbar_g`，产生逐行完全相同的观察数据。故如果允许不受限制的组特定截距，单凭这一份观察数据不能决定c是真上下文效应或与组暴露构成相关的群截距；人工已知c只是源代码的真参数，不等于数据自身识别了其因果含义。

## 正式验收

两个相互独立的Fraction算法、所有层级残差正交及源数据精确可再生，至少25项单元测试在Python3.11/3.12各通过，完整180世界、8640行人工数据、720准去均值估计、固定数学方向反转与层级别名，均以机器JSON、全部CSV、原始源码、协议及固定时间戳ZIP永久归档main，并核验CI三job success，才能结题为`CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_MULTILEVEL_LINEAR`。

本轮E1人工代数研究，新增真人E2、真实历史E3均0。R073和PESEN v0.1持续冻结。下一R189原目录08-013 Multilevel Generalized Linear Models，进入前再次核验。原R系列全完成后再统一分类，最后熔炼。
