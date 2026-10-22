# R230 探索性因子分析：八有限因子世界、256原完整来源与观察等价的旋转载荷

日期：2026-10-23（Asia/Taipei）。实际原始239目录 **10-004 Exploratory Factor Analysis（P1）**。科学状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_FACTOR_COVARIANCE_ROTATION**。只使用完全构造的人工概率分布，不具有任何真实受试者、问卷、真实历史数据或跨环境外部效度。

## 原始资料与设计顺序

Spearman (1904), [*“General Intelligence,” Objectively Determined and Measured*](https://doi.org/10.2307/1412107), *The American Journal of Psychology* 15:201–292，刊物及[历史正文镜像](https://psychclassics.yorku.ca/Spearman/chap1)可以确认原研究关于共同因素的讨论。Thurstone (1938), [*A New Rotational Method in Factor Analysis*](https://doi.org/10.1007/BF02287928), *Psychometrika* 3:199–218，原出版方摘要讨论因子载荷旋转；Thurstone (1947), [*Multiple-factor Analysis*](https://books.google.com/books/about/Multiple_factor_Analysis.html?id=l9YGzQEACAAJ), University of Chicago Press，作为传统多因素方法的历史定位。Goretzko (2025), [*How many factors to retain in exploratory factor analysis?*](https://doi.org/10.1037/met0000733) 为因子保留方法的不确定性提供较新综述。本工作未把这些研究的经验量表/拟合代码称为自身已复现结果。

本R独立[计算前冻结协议](../../protocols/R230_EFA_8_FACTOR_WORLDS_256_ORIGINAL_LATENT_SOURCES_PRESCORE_FREEZE_2026-10-23.md)，先行提交[63b7a6a0](https://github.com/edwardsage419/Psychohistory-Research/commit/63b7a6a05cfbd71bd49a59d559c8299256c3abf3)，随后才创建模型、评分及CI，所有八世界、源类型、三指标载荷与噪声、旋转矩阵及预期特征谱保持不变。

## 原人工源与两套独立数学验收

各世界固定两个人工外生潜因子U,V和三个互相独立Rademacher误差E1,E2,E3，均匀取±1。故每世界2⁵=32条完整来源，每条1/32，八世界合计**256条**。实际观察三指标X由固定载荷矩阵与特异噪声形成。独立第一算法直接将32源实际X向量的加权人口均值、总体3×3协方差用Fraction精确枚举；第二算法完全不读取源矩，以固定载荷L及误差幅度d计算 `Σ=LLᵀ+diag(d²)`，每一格严格一致。

对于ROTATED_CROSS_ALIAS，冻结旋转矩阵 `Q=[[3/5,−4/5],[4/5,3/5]]`，新因子 `F'=Q(U,V)`、载荷 `L'=LQᵀ`。验证 `QQᵀ=I` 且对四种U,V来源 `L'F'=L(U,V)`，包括实际三个观察指标在每个完整人工来源上逐项完全相同。新因子在这个有限非正态结构中仍不相关且方差单位，但旋转后的两个因子可以统计依赖；不误以为未经高斯假设旋转总能保持独立。

## 协方差、谱与真实已知特异误差下的公共因子秩

| 世界 | 精确协方差特征根 | 已知特异误差下真实公共矩阵秩 | 三项公共方差比例 |
|---|---|---:|---|
| ONE_COMMON_TRAIT | 4,1,1 | 1 | 1/2,1/2,1/2 |
| COMMON_METHOD_ALIAS | 4,1,1 | 1 | 1/2,1/2,1/2 |
| TWO_FACTOR_BLOCK | 3,2,1 | 2 | 1/2,1/2,1/2 |
| CROSS_LOADING | 4,2,1 | 2 | 1/2,2/3,1/2 |
| NO_COMMON_FACTOR | 1,1,1 | 0 | 0,0,0 |
| BIPOLAR_LOADING | 4,1,1 | 1 | 1/2,1/2,1/2 |
| ROTATED_CROSS_ALIAS | 4,2,1 | 2 | 1/2,2/3,1/2 |
| HIGH_UNIQUENESS | 7,4,4 | 1 | 1/5,1/5,1/5 |

全部预设特征根均经观察协方差的迹、二阶主子式之和、行列式三条**独立精确对称多项式系数**严格核对。这是三个预先固定、在本人工对称矩阵中可有理因式分解的特征根验算，不声称实现了通用数值PCA求根或适用于任意真实EFA矩阵。

真实因子个数栏的秩是 **使用人工oracle明确已知的特异噪声方差diag(d²)** 之后，对公共协方差 `Σ−diag(d²)` 进行Fraction高斯消元得到的。现实探索性因素分析的特异误差未知，不能把本行当作无监督从仅有样本协方差已自动证明潜在维度的结果。

## 观察等价与科学限制

**观察等价对一：** ONE_COMMON_TRAIT与COMMON_METHOD_ALIAS的全部32原源X以及完整`P(X1,X2,X3)`相同。两种潜在因子语义分别指定稳定特征与同次施测共享方法项；此构造仅表示**一次测量不能从相同概率分布决定共同来源的时间稳定性与心理含义**，没有生成或复验真人纵向测量。若增加合格的独立重复施测或新任务、排除限制，未来可能产生区分信息，但本R不提供该证据。

**观察等价对二：** CROSS_LOADING与ROTATED_CROSS_ALIAS对每个固定U,V,E1/E2/E3结构原源的三个实际X完全相同，完整联合观察分布及协方差也逐格相等；其对外报告的载荷数值、潜因子坐标不同。该人工反例证实未经旋转约束时，**因素载荷坐标和因素解释不是由观察协方差唯一固定**。就连在本例中具有两个因子共同秩也无法决定独特的旋转角或特征概念。

**信噪比与假设诊断：** HIGH_UNIQUENESS与ONE具有完全相同的共同人工载荷，但误差幅度从1增加至2，特异误差方差从1增加至4，使每题公共方差比例从1/2降到1/5，未标准化非对角协方差仍为1、相关系数从1/2降到1/5，观察谱从(4,1,1)变(7,4,4)。BIPOLAR_LOADING则展示部分指标负载荷时能够出现负的项间协方差，而总体公共矩阵秩仍为1。NO_COMMON_FACTOR的三个独立噪声指标特征根(1,1,1)和公共矩阵秩0；这只是在人工指定真实误差结构下的结论。

这些机制并不能证明某个现实量表的探索性因素个数、构念真实性、因子独立性、因果方向、旋转约束或抽样稳定性。也没有对真实样本进行极大似然EFA、平行分析、因子保留准则比较、bootstrap或任何效度外推。

## 代码、CI、真实归档证据

[原生Python Fraction程序](r230_exact_finite_factor_analysis.py) · [256条完整原外生来源CSV](R230_ALL_256_ORIGINAL_FACTOR_EXOGENOUS_SOURCES.csv) · [八世界协方差/观察联合及特征根机读结果JSON](R230_EXACT_RESULTS.json) · [两个文件SHA256机器验收](R230_FINAL_MACHINE_ACCEPTANCE.json)。

[GitHub Actions run39824693913](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39824693913)总体completed/success、三作业分别completed/success，Python3.11与3.12真实日志各显示 `Ran 60 tests`及 `OK`，合计120项测试执行通过。第三完整原资料作业日志输出 `R230_ALL_256_FULL_FACTOR_SOURCES_ROTATION_AND_SPECTRAL_CERTIFICATES_VALID`，独立检查每世界32源的真实概率、完整观测等价、固定有理旋转逐源响应、Oracle低秩、特征根及SHA；机器人真正永久原资料归档提交 [2d5cddf1](https://github.com/edwardsage419/Psychohistory-Research/commit/2d5cddf19c6490167cda754d19ce37131686811e)。

最终原CSV SHA256 `d8567285a4c5cc100efd6351999f11e2e8634fdb2d873b2a510145096a3d4efa`；JSON结果SHA256 `bbc4a52a1a7da84e839103483d803d127648cdd6c1b8c3180b64d5b4c9f7956f`。

全阶段仅人工E1，真人E2与真实历史E3新增0，R073和PESEN v0.1保持冻结。下一实际原239目录条目预计 **10-005 Confirmatory Factor Analysis（R231）**，须独立核对原始目录后继续学习，既定顺序始终是完成全部R再统一归纳分类、最终熔炼。
