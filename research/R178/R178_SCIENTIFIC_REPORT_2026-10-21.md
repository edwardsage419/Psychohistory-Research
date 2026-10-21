# R178 最大似然估计：30个有限样本世界的精确风险与覆盖率科研报告

日期：2026-10-21。原239候选模型P0/08-002 Maximum Likelihood Estimation。科研等级 **CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_FINITE_MLE**。所有结果来自固定的人工计数概率生成模型，无真实人类行为或历史事件预测证据。

## 概念、研究输入与预先冻结

[NIST独立二项分布与MLE](https://www.itl.nist.gov/div898/handbook/eda/section3/eda366i.htm)给出固定试次数n、成功次数k时独立Bernoulli似然的最大值在p_hat=k/n。[Brown, Cai, DasGupta 2001](https://doi.org/10.1214/ss/1009213286)评述比例区间的有限样本失配；[NIST BetaBinomial](https://www.itl.nist.gov/div898/software/dataplot/refman2/auxillar/bbnpdf.htm)和[He等2015](https://doi.org/10.1080/02664763.2015.1023270)提供相关事件与结构零机制背景。研究者自己的计数实验与原文理论边界必须区分。

[计算前冻结协议](../../protocols/R178_MLE_30_FINITE_SAMPLE_COUNT_WORLDS_PRESCORE_FREEZE_2026-10-21.md)先于任何R178完整结果以提交`1966134a3911638a75faef00bac2f4f799bd957f`归档。人工计数分布直接严格引用已经通过R177的固定研究来源：R177程序Git blob SHA1 `2d032513ce84141214b6b3f84df9c0ed9976a02b`，完整输出SHA256 `57410cf2c110ce3117b7af72e4b7473cee0c3ffd013e6fb99fd43de62165a535`；两个源字节标识由程序在运行前重新验证，来源更改即停止。

n=4、8、12，真实单位机会概率p=1/4、1/2，五类生成过程：独立二项、Beta二项浓度2、Beta二项浓度8、零膨胀二项结构零1/8、零膨胀二项结构零1/4。3×2×5=**30组世界**、共270个完整计数概率。所有世界生成的成功次数均满足真实边际均值np，但有不同组内依赖或潜在全零成员。拟合方法故意固定为**独立二项似然**，因此在后四类下属于标准误假设错误指定的参数估计模型，不能称为正确的完整生成分布MLE。

## 精确MLE和有限样本风险

每个可能成功次数k均严格采用估计p_hat=k/n，独立以所有分数网格j/(4n)检查同一个Bernoulli似然的极大位置。随后把真实训练计数完整分布视为权重，以Fraction精确求估计偏差、MSE、真实MSE相对IID理论方差的倍数、固定传统双侧1.96 Wald区间的真实覆盖率、边界MLE出现概率、Laplace固定平滑的MSE；只对独立未来Bernoulli(p)测试事件负对数损失采用高精度数值log，同时用Decimal.ln和math.log双算独立一致。

全部30世界MLE针对**边际p**的均值都严格等于p，即完全无偏。IID样本的真实MSE等于p(1-p)/n。对单位内正相关或结构零生成机制，尽管同样无偏，所有情景的真实MSE都高于错误假定的IID理论方差，计算比值与由生成机制推出的精确解析比值一一相同。

### 预先固定的n=8、p=1/4对照

| 训练数据实际机制 | 真实MLE MSE / IID声称理论方差 | 名义95% Wald区间实际覆盖 | 边界MLE发生概率 | 固定Laplace预测平均负对数损失 |
| --- | ---: | ---: | ---: | ---: |
| IID_BIN | 1 | 87.26% | 10.01% | 0.604894 |
| CLUSTERED_BB_C2 | 10/3=3.333 | 46.55% | 39.28% | 0.698845 |
| CLUSTERED_BB_C8 | 16/9=1.778 | 71.61% | 20.14% | 0.634461 |
| INACTIVE_ZIB_Z1_8 | 4/3=1.333 | 77.41% | 18.43% | 0.618983 |
| INACTIVE_ZIB_Z1_4 | 16/9=1.778 | 65.48% | 27.94% | 0.637063 |

此处Wald由`p_hat ± 1.96*sqrt(p_hat*(1−p_hat)/n)`定义，使用**有理数不等式**而非浮点阈值判定真值是否被覆盖。其“95%”只是大样本名义置信水平；即使IID正确，n=8亦未达到95%，不能把模型错误指定解释成全部偏差的唯一来源。Beta二项浓度2的覆盖率46.55%尤其揭示未经验证的独立性假设可能给出过窄的不确定性范围。

### 无平滑MLE的独立新观察评分陷阱

对于所有30组，训练成功计数为0或n的概率严格大于0。出现这两类训练样本时，未经平滑的MLE p_hat=0或1。研究设定未来测试行为Y来自**另一个独立单位事件、边际Bernoulli(p)**，真实p在(0,1)，所以与边界MLE相反的结果有正概率。其对数损失为正无穷，故所有30组未经平滑MLE的**无条件独立测试事件期望负对数损失均为正无穷**。这是无限损失评分的数学性质，不等于模型在任何具体未来测试中必然遭遇无穷损失。

事前另设Laplace平滑预测`(k+1)/(n+2)`，始终严格位于(0,1)。实际用30组完整训练计数概率加权得到有限的新测试事件对数损失，`Decimal.ln`和`math.log`两条数值路径差异均小于1e−12。此方法为外部竞争基线，不可把它对无限风险的修复回记给无平滑MLE。

## 独立计算、测试及永久档案

* 源R177的30组计数PMF均由封闭分布公式与逐次事件DP双路径完全一致。
* 对所有支持点进行完整MLE有理网格极大检验，对30×270完整样本概率计算偏差、MSE、Wald实际覆盖、边界概率及两个独立的Laplace期望预测得分路径。
* 单元测试共**25个不同方法**，Python3.11与3.12各成功完成25次，合计50次测试执行。主评价再单独运行完整30世界与散列/档案严格验收。
* [GitHub Actions39554622255](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39554622255)三job全部success，自动永久归档commit [be0319c](https://github.com/edwardsage419/Psychohistory-Research/commit/be0319caae83c40e862205ffe3d46a96ccc0bd1f)。

永久档案：[R178_EXACT_RESULTS.json](R178_EXACT_RESULTS.json)，30世界全部精确偏差、MSE、完整PMF、覆盖和预测得分；[R178_FINAL_MACHINE_ACCEPTANCE.json](R178_FINAL_MACHINE_ACCEPTANCE.json)包含验收与不可升级E2/E3的证据标签；[r178_finite_sample_mle_exact_risk.py](r178_finite_sample_mle_exact_risk.py)是原生全程序含25单测；[R178_MLE_30_Finite_Count_Sample_Worlds_Exact_Audit.zip](R178_MLE_30_Finite_Count_Sample_Worlds_Exact_Audit.zip)含协议、源码、JSON与机器验收。

## 正式科学结论及下一编号

R178严格证明：对同一边际成功率，即便独立Bernoulli MLE在不同群内生成机制下仍无偏，IID方差公式与小样本Wald覆盖也可能严重失配；无平滑边界MLE在对数评分下有特定无限期望风险。该结论是本项目对**全部人工生成样本空间**的数学验收，未形成真实群体相关性的估计、真人预测、真实历史概率或对原作者数据的复现。

新增E2=0、E3=0，R073和PESEN v0.1继续冻结。下一R179 P0/08-003 Bayesian Posterior Inference（贝叶斯后验推断），继续所有原R系列研究，全部完成后统一归纳分类，最后熔炼。
