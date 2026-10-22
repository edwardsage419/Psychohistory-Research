# R230 探索性因子分析：八有限载荷结构、256完整人工外生来源与旋转及误差非识别，事前冻结

日期2026-10-23，Asia/Taipei。真实原始239目录 **10-004 Exploratory Factor Analysis（P1）**。研究号R230；人工E1。方向是固定三观测项的因子模型真实完整总体矩、相关结构、已知误差方差后的低秩分解、正负载荷、旋转不唯一、共享方法误差与稳定特征的观察等价，测量信噪比。**不做真实问卷的样本EFA优化、平行分析、探索性旋转搜索或模型选择成功声明**。R073与PESEN v0.1保持冻结。

## 原始文献与当前可核阅范围

Spearman (1904), *“General Intelligence,” Objectively Determined and Measured*, *American Journal of Psychology* 15(2):201–292, DOI https://doi.org/10.2307/1412107，可由JSTOR及原研究经典全文 https://psychclassics.yorku.ca/Spearman/chap1 核对；Thurstone (1938), *A New Rotational Method in Factor Analysis*, *Psychometrika* 3:199–218, DOI https://doi.org/10.1007/BF02287928，出版方摘要涉及因子旋转；Thurstone (1947), *Multiple-factor Analysis*, University of Chicago Press，原书书目信息 https://books.google.com/books/about/Multiple_factor_Analysis.html?id=l9YGzQEACAAJ 。此外Goretzko (2025), *How many factors to retain in exploratory factor analysis? A critical overview of factor retention methods*, DOI https://doi.org/10.1037/met0000733，反映真实研究中因子数量选择的不确定性。本阶段只检验这类数学机制的有限实例，不伪称已复算1938/1947原作者真实材料。

## 完整固定外生来源

独立U,V,E1,E2,E3∈{−1,+1}，每个32种等概率完整外生配置且P=1/32。八世界共有**256个完整原来源**，每条包括两种人工因子指标F1,F2、人工U,V、三误差来源、完整观测三变量(X1,X2,X3)、固定实际载荷L、每项独立特异误差系数d_j及世界标签。基础测量结构 (X_j=L_{j1}F_1+L_{j2}F_2+d_j E_j)。在ROTATED_CROSS_ALIAS中定义F'=Q(U,V)，L'=L Q^T且Q为正交有理旋转 `[[3/5,-4/5],[4/5,3/5]]`，故逐外生来源的X严格与CROSS_LOADING相同。F'的协方差为单位阵，但在有限Rademacher离散源下不必具有独立分量分布；不虚称旋转维持潜变量独立。其它世界F=(U,V)。

## 八个冻结世界

1. ONE_COMMON_TRAIT：L行(1,0),(1,0),(1,0)，d=(1,1,1)，三项目有共同人工稳定U。
2. COMMON_METHOD_ALIAS：L和d、所有实际X方程与1完全相同，U在此被**解释为一次施测的共享方法因子**，没有单次观测可以区分两种语义；无需伪造时序与真稳定性测量。
3. TWO_FACTOR_BLOCK：L行(1,0),(1,0),(0,1)，d=(1,1,1)，两组独立人工因素。
4. CROSS_LOADING：L行(1,0),(1,1),(0,1)，d=(1,1,1)，第二题跨载荷。
5. NO_COMMON_FACTOR：L三行(0,0)，d=(1,1,1)，三个观测量完全独立，无公共因子。
6. BIPOLAR_LOADING：L行(1,0),(-1,0),(1,0)，d=(1,1,1)，有反向载荷和负相关项。
7. ROTATED_CROSS_ALIAS：以上CROSS_LOADING的Q有理正交重参数化，L'与F'如前；观察三项X在逐来源层面完全相同，因子载荷和坐标不同。
8. HIGH_UNIQUENESS：L同ONE_COMMON_TRAIT，d=(2,2,2)，测量噪声方差4，协方差同样含真实共同U，但相关系数及主成分方差结构变化。

## 冻结可重复分析与结果关口

1. 对每世界完整32人工源计算真实总体均值 `E[X]`、三项方差和3×3协方差 `Σ=E[(X−EX)(X−EX)^T]`，Fraction不舍入。第二条独立理论路线只由固定 L、载荷因子协方差I及误差对角系数D获得 `Σ=LL^T+diag(d²)`；逐3×3格严格相同。对ROTATED_CROSS_ALIAS独立证明Q Q^T=I，以及 `L'Q(U,V)=L(U,V)` 对四种U,V逐项成立。
2. 计算观察协方差矩阵的迹、三个二阶主子式之和、行列式，给定**事前预设三特征根列表**进行三项基本对称多项式精确核验；不得将有理特征根验算谎称通用数值PCA算法或无限大样本采样结果。预设谱依次：ONE=(4,1,1)，METHOD_ALIAS=(4,1,1)，TWO_BLOCK=(3,2,1)，CROSS=(4,2,1)，NO=(1,1,1)，BIPOLAR=(4,1,1)，ROTATED=(4,2,1)，HIGH=(7,4,4)。
3. 在**已知真实噪声方差Oracle**时，计算 `Σ−diag(d²)=LL^T` 与其精确代数秩、严格比较1/2/0个公共方向。Oracle噪声并不可从任意真实问卷直接观察，此秩不是从单次测量自动可识别的因子数量推断。
4. 对ONE/METHOD与CROSS/ROTATED两个机制对分别核对完整联合分布 `P(X1,X2,X3)`，必须逐观察格Fraction完全一致，并解释各自语义/参数非唯一性；CROSS/ROTATED更要求源点级别X完全相同。HIGH世界对照ONE相关比率从1/2降至1/5；说明同真公共载荷但特异误差更大时观察相关可降低。
5. 警告：单一谱信息无法识别潜变量的心理意义、潜在因素一定独立、观测变量因果方向、独立特异误差条件是否实际成立。不给源数据之外的真实心理解释。
6. Python标准库Fraction、不依赖NumPy或外部拟合包。Python3.11和3.12两个CI job各至少40测试，第三作业生成全部256原人工来源CSV、八世界精确协方差及观察联合JSON、SHA256机器验收并永久提交main。只有真实通过后才发表有界科学报告/正式验收。冻结协议先入仓，之后才允许模型及其评分。
7. 全部人工E1，真人E2新增0、历史E3新增0。R073、PESEN v0.1冻结。下一原目录由真实239 JSON再确认，预计10-005 CFA（R231）。
