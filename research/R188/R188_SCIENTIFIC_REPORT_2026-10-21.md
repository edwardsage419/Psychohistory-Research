# R188 多层线性模型：180人工六群组世界的完整组内、组间、上下文与准去均值敏感性审计

日期：2026-10-21。原239候选目录 P0/08-012 Multilevel Linear Models。正式科学等级 **CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_MULTILEVEL_LINEAR**，新增真人E2=0、独立历史E3=0。

## 理论材料与实证边界

Mundlak (1978), [On the Pooling of Time Series and Cross Section Data](https://doi.org/10.2307/1913646), Econometrica 46(1):69–85，给出组内、组间变量及合并面板分析的基础问题。Laird and Ware (1982), [Random Effects Models for Longitudinal Data](https://pubmed.ncbi.nlm.nih.gov/7168798/), Biometrics 38(4):963–974，明确层级与重复观测中的随机效应分析动机。Bell and Jones (2015), [Explaining Fixed Effects: Random Effects Modeling of Time-Series Cross-Sectional and Panel Data](https://doi.org/10.1017/psrm.2014.7), Political Science Research and Methods 3(1):133–153，进一步讨论群组间差异、单位内效应及解释量与群组效应相关时的回归建模。本项目只构造受控的**人工分层数据**进行Fraction准确数学检验，未复现原文真实面板、教育、健康或社会实验样本，未执行随机截距方差组件MLE，也未对历史过程作推断。

## 完整冻结因子设计和透明算术更正

[原始计算前冻结协议](../../protocols/R188_MULTILEVEL_90_WORLDS_4320_ROWS_PRESCORE_FREEZE_2026-10-21.md)首先于提交`08276a5ae3769e64b3f00d6ac39a8eab8b717754`入库。它从最初就固定3种六群组暴露设计、2个a、2个b、5个c、3个e，但数量乘积误写成90世界。首个CI[39565973693](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39565973693)中31项单元测试有29项成功，两项仅因180≠90及8640≠4320的**静态数量断言**失败，完整研究结果没有被结题归档。

为保护预冻结参数选择，随后建立[独立算术更正档案](../../protocols/R188_PRE_SCORE_FACTORIAL_ARITHMETIC_ERRATUM_2026-10-21.md)，提交`2b23e2355e4bf2dfcf90b52ef2e3b4f67d0d277e`，原提交与首次失败记录全部永久保留。正确计算为3×2×2×5×3=**180个人工世界**，每世界六群组×八观察=48行，所以**8640行人工记录**。固定四档去均值强度，构成**720种斜率拟合**。其后订正源码数量常量、错误协议路径及确定性ZIP中同时包含冻结协议与更正档案的溯源，未变动任何自变量、真响应、评分公式、解释假设或样本筛选。中间修复版本的失败运行仍保留，最终正式验收CI[39566340477](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39566340477)三个job全部success。原协议的文件名因历史冻结标识仍留90/4320，**内容与实际正式机器验收均按180/8640/720执行**。

## 180个六群组人工来源与三层效应

每个人工世界严格有G=6个群组，每群组n=8个二元暴露观察x∈{0,1}。群组内暴露人数x=1固定分布：

1. BALANCED: (4,4,4,4,4,4)；
2. WEAK_BETWEEN: (2,2,4,4,6,6)；
3. STRONG_BETWEEN: (2,2,2,6,6,6)。

所有源样本按已知有理数`y=a+b*x+c*xbar_g+eps`构建。a∈{0,1}，b∈{1/4,1/2}为真正组内正系数，c∈{−4,−2,0,2,4}为人工群组均值的源系数，eps在每(group,x)细胞中严格一半+e、一半−e，e∈{0,1/4,1/2}。因此群组内部的残差与均值、x、群组标识精确正交，不存在随机采样数值误差。每组必有正暴露与正对照个体，所有模型都用同一批完整来源，不额外构造后验有利数据。

四类相互连接的估计：

* POOLED: 将48个人工观察全部放到带截距的y~x回归；分别以x=1与0条件均值差、以及独立Fraction 2×2正规方程解算，全部世界严格一致。
* WITHIN_FE: 每个群组内部去群均值的固定效应斜率，另用各群组x=0/1条件均值差乘以精确权重`k_g(8−k_g)/8`独立验算。全180世界均严格恢复b。
* BETWEEN: 在六个群组均值间拟合`ybar_g~xbar_g`，两套独立正规方程与组均值协方差计算一致。只在WEAK_BETWEEN及STRONG_BETWEEN存在组均值变动时可识别，其斜率为b+c；BALANCED因六组xbar完全相同而精确rank deficiency，程序明确报告`UNIDENTIFIED_NO_BETWEEN_VARIATION`。
* CORRELATED_CONTEXTUAL: 拟合`y~1+x+xbar`，非平衡组均值条件下按直接3×3 Fraction正规方程严格得到(a,b,c)，另由BETWEEN和WITHIN_FE差独立推导，逐分数一致。BALANCED设计因xbar与截距完全共线，完整上下文回归不可唯一识别。

额外固定`θ=0,1/2,3/4,1`四档个体观测准去均值，`x'=x−θ*xbar`、`y'=y−θ*ybar`，各自用直接变换后回归与独立组内/组间方差分解两方法求得**720个完全Fraction一致的斜率**。其中`Vbetween=E_g[(xbar_g−mean_x)^2]`、`Vwithin=E_g[xbar_g(1−xbar_g)]`，系数严格满足`βθ=b+c*(1−θ)^2 Vbetween / (Vwithin+(1−θ)^2 Vbetween)`。θ=0还原POOLED，θ=1还原WITHIN_FE，θ=1/2与3/4**不声称是从数据拟合得到的有效随机截距方差或广义最小二乘模型**，只是预冻结层级假设敏感性。

## 预先冻结的方向反转与层级别名

固定STRONG_BETWEEN，a=0、b=1/4、c=−4、e=1/4。群组内部x次数(2,2,2,6,6,6)使`Vbetween=1/16`、`Vwithin=3/16`。所有48个源响应、两套独立斜率算法和原残差交叉积准确满足：

| 准去均值θ / 层级 | 人工x斜率 |
| --- | ---: |
| POOL θ=0 | −3/4 = −0.75 |
| θ=1/2 | −3/52 ≈ −0.057692 |
| θ=3/4 | 33/196 ≈ +0.168367 |
| WITHIN_FE θ=1 | +1/4 = +0.25 |
| BETWEEN group means | −15/4 = −3.75 |

完整180世界里，**36个世界**出现合并回归斜率为负但源真组内斜率b依然为正；在BALANCED组别构成中，所有θ都给出相同的b，没有这种由不同xbar组间构成造成的偏差。无需观察不可靠的真人数据，这些结果已经在已知生成方程的人工概率代数层严格证明。

更重要的机制识别边界：真实响应方程写成`y=a+b*x+c*xbar_g+eps`，另一个带自由群组截距的模型`y=a+b*x+u_g+eps`，令`u_g=c*xbar_g`，则**所有原始8640行人工数据逐行完全相同**。因此若允许任意群组截距且没有额外限制，就不能仅凭观察数据决定c代表可识别的上下文因果效应，还是相关的组间未观测差异。已知人工真c属于生成代码的参数，不等同于真实应用中从数据已经识别其因果含义。

## 正式验证、完整文件与科研资格

[GitHub Actions39566340477](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39566340477)：Python3.11与3.12各执行31种单测，共**62次全部成功**；第三job完成180世界8640行、720个Fraction准去均值回归、层级别名与固定符号反转、数学秩退化负对照、SHA和带明确更正档案的确定性ZIP，三个job全部success。正式原始结果自动归档提交[e31e31f](https://github.com/edwardsage419/Psychohistory-Research/commit/e31e31f703da88b04740c8cd345feb374752d9f0)。

* [R188_EXACT_RESULTS.json](R188_EXACT_RESULTS.json)：全部180世界组内、组间、上下文与四档准去均值详细人工结果，SHA256`a59a34f3523688ba818f09d5eba885166ca9c56b9f96dbf778e21dfa96ae69b7`。
* [R188_ALL_8640_HIERARCHICAL_ARTIFICIAL_ROWS.csv](R188_ALL_8640_HIERARCHICAL_ARTIFICIAL_ROWS.csv)：全部8640人工原始数据，均含群组、个体x、组构成xbar、y和单元残差以及等价的任意组截距表达，SHA256`683e038d94f74612f90f35b310be1c134338662018568efbb6727b85d1e8af4d`。
* [R188_FINAL_MACHINE_ACCEPTANCE.json](R188_FINAL_MACHINE_ACCEPTANCE.json)：独立数学验收、原始源数量、正反例和E1真实资格标记。
* [r188_exact_multilevel_linear.py](r188_exact_multilevel_linear.py)：有理数层级数学、源记录和31项双路径验证。
* [R188_180_Exact_Multilevel_Linear_Worlds.zip](R188_180_Exact_Multilevel_Linear_Worlds.zip)：原冻结协议、独立订正文件、完整程序、人工源CSV、结果JSON及机器验收的六项固定时间戳归档。
* [首次冻结协议](../../protocols/R188_MULTILEVEL_90_WORLDS_4320_ROWS_PRESCORE_FREEZE_2026-10-21.md)及[算术更正审计](../../protocols/R188_PRE_SCORE_FACTORIAL_ARITHMETIC_ERRATUM_2026-10-21.md)共同构成可核验的研究决策历史。

本项正式科研证据仅限**E1人工分层代数、层级效应方向、参数不可识别性**。未经任何真实个体或群组观察测试，不能声称估计了真实随机效应、完成外部预测或识别因果效应；新增真人E2=0、独立历史E3=0。R073与PESEN v0.1保持冻结。下一原目录为 **R189 P1/08-013 Multilevel Generalized Linear Models**。维持先完成全部R系列、再统一归纳分类、最后熔炼的长期研究顺序。
