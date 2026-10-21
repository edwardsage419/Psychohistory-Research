# R184 泊松回归：45个人工计数世界的工作似然离散度、零强度边界与真正独立预测风险

日期2026-10-21。原目录P1/08-008 Poisson Regression。正式科学状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_POISSON_GLM**。没有新增真人E2或真实历史E3。

## 一手理论、固定来源与明确边界

Nelder and Wedderburn (1972), [Generalized Linear Models](https://doi.org/10.2307/2344614)提出一般化线性模型的统一推断框架；Cameron and Trivedi (2013), [Regression Analysis of Count Data](https://doi.org/10.1017/CBO9781139013567)系统区分泊松均值方差假设、真实计数过度离散、复杂异质性和混合分布。本轮只使用R177固定人工数据，未复现上述原论文和教材示例、真实因变量计数与任何历史模型。

计算前冻结[R184正式协议](../../protocols/R184_POISSON_GLM_45_WORLDS_PRESCORE_FREEZE_2026-10-21.md)，在结果计算前以提交`bdf9f290bd1e4e64e2d9d85dfcd5c4dcc790fc3a`入库。人工计数数据全部来自R177固定原程序blob SHA1 `2d032513ce84141214b6b3f84df9c0ed9976a02b`、评分JSON SHA256 `57410cf2c110ce3117b7af72e4b7473cee0c3ffd013e6fb99fd43de62165a535`，每次执行须重新核验完整字节和独立源模型PMF两种生成方法，否则fail closed。

每个世界中有两个互相独立人工计数训练单元，x=0与x=1各包括n=4、8、12次潜在二元事件，组内依源生成机制可能有关联。固定真边际概率对(1/8,1/4)、(1/4,1/2)、(1/4,1/4)，五种R177生成机制为独立二项BIN、Beta二项浓度2或8、零膨胀二项结构零1/8或1/4，组成**45人工世界**，每世界穷举两个单元的全部原始成功次数计数对，合计**4125条真实源联合概率记录**。

## 工作Poisson回归与真实离散度

独立Poisson工作似然令 `log(λ_x)=α+βx`，工作模型声称单个计数的条件方差等于条件均值。然而全部来源的真实样本空间是固定最多n次的有限二元事件计数，其支持与无限Poisson支持不一致；模型是有意可能错误指定的*工作模型*。对两组分别在闭集λ≥0求MLE，取得`λhat_x=K_x`，对源计数每种可能K逐一用数值log似然半整数网格和独立score`K−λ`的内点根与边界符号审核，两算法一一相同。若某一训练K=0，其log链接的至少一个回归系数需趋于负无穷；本研究对每种人工来源计算非有限二参数概率并通过全部4125概率样本枚举与独立解析`1−(1−P(K0=0))(1−P(K1=0))`严格一致。

全部人工源计数的实际方差Var(K)由原真实PMF精确计算，与R177的原理论方差公式对每个n、p、机制全部Fraction相等。真实离散比D=Var(K)/E[K]依来源机制而变，可以小于、等于或大于1。

### 事前固定n=8、p0=p1=1/4全来源比较

每个人工训练/测试计数的边际均值都严格为2，下表按研究源完整概率得分排列。

| 原始计数生成机制 | 真实D=Var/E | 实际零事件概率 | 同均值Poisson P0 | 原MLE独立测试计数MSE | 固定强度+1/2测试计数MSE |
| --- | ---: | ---: | ---: | ---: | ---: |
| IID_BIN | 0.750000 | 10.011% | 13.534% | 3 | 3.25 |
| CLUSTERED_BB_C2 | 2.500000 | 37.094% | 13.534% | 10 | 10.25 |
| CLUSTERED_BB_C8 | 1.333333 | 20.000% | 13.534% | 16/3≈5.333 | 67/12≈5.583 |
| INACTIVE_ZIB_Z1_8 | 1.000000 | 18.429% | 13.534% | 4 | 4.25 |
| INACTIVE_ZIB_Z1_4 | 1.333333 | 27.926% | 13.534% | 16/3≈5.333 | 67/12≈5.583 |

最重要的**预冻结机制反例**是结构零z=1/8：原始计数方差与均值严格相等，但真实零频率为18.429%，比理论Poisson零概率13.534%高约4.9个百分点。**仅凭Var≈E[K]这一矩条件不足以识别真实计数分布为Poisson。** 虽然Poisson模型也在均值上被正确指定，这不修复对零频率、尾部概率或误差结构的拟合问题。

## 独立测试计数的两个评分指标

未来测试源于另一独立的、与训练同分布的人工计数单位Y_x。原工作MLE`λhat=K_train`，若训练K=0，其对任何未来Y>0的Poisson预测质量为0，故出现正无穷负对数损失。每个源世界训练K=0与未来Y>0同时具有正概率，因此**全部45世界未经平滑MLE的无条件样本外Poisson期望logloss均为INF**。

固定正强度预测`λ_H=K_train+1/2`确保预测的Poisson概率在任意非负整数Y上为正。所有45世界未来测试负对数损失通过`λ_H−μ logλ_H+E[log(Y!)]`进行数值积分，使用Python `math.log/lgamma`及60位`Decimal.ln`与整数阶乘求和两套独立实现逐个计数与全部期望复验，所有差异绝对值不超过1e−12。

人工真正生成过程下未来原始计数平方误差采用**Fraction完整概率枚举**与独立的训练/测试二阶矩推导两路一致。源训练K与独立未来Y拥有相同真均值μ与方差v，因此

* `E[(Y−K)^2]=2v`，原生MLE计数预测的完整测试平方风险；
* `E[(Y−(K+1/2))²]=2v+1/4`，固定正强度预测平方风险严格更大。

这项**负向对照**是本研究的一项正式结论：增加半个伪计数解决Poisson未来logloss的无限边界问题，同时在所有45种预设世界使均方计数误差增加1/4。不得从解决无限logloss推断该方法对所有损失函数或现实数据更准确。

## 完整自动化复验与永久归档

[GitHub Actions39562030829](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39562030829)两个测试job分别在Python3.11、3.12各执行25项单元测试，合计**50次通过**；第三个job单独完整运行45世界、4125人工计数源记录、两路径Poisson工作似然及计数方差验收、数值Poisson评分复核、源SHA及确定性ZIP检验，三个job全success。真实结果提交至main [e0213c1](https://github.com/edwardsage419/Psychohistory-Research/commit/e0213c1d4f2a36280b2df726d96bca50e9ffed67)。

正式档案包括：

* [R184_EXACT_RESULTS.json](R184_EXACT_RESULTS.json)：45个完整世界的真实来源概率、离散度、非有限回归概率及两评分体系，SHA256 `99aadab9ac6e0b051a5aca2375d5df5f4d5aeee80f8fa5a8ef6d0a16ef2eaff9`。
* [R184_ALL_4125_ARTIFICIAL_TRAINING_COUNT_PAIRS.csv](R184_ALL_4125_ARTIFICIAL_TRAINING_COUNT_PAIRS.csv)：全部4125带来源概率的训练计数对、MLE和正强度预测与原始计数测试平方误差，SHA256 `a66c95ef6be38d5be945573c11e730669a015afaca26ce3a3af82f7952190a07`。
* [R184_FINAL_MACHINE_ACCEPTANCE.json](R184_FINAL_MACHINE_ACCEPTANCE.json)：锁定来源、两路工作似然和真方差验收、完整评分SHA及人工E1/E2/E3边界。
* [r184_poisson_count_glm_exact.py](r184_poisson_count_glm_exact.py)：完整自建有限源计数Poisson工作GLM参数解析、两种预测风险和25项测试。
* [R184_Exact_Poisson_45_Worlds_Source_Audit.zip](R184_Exact_Poisson_45_Worlds_Source_Audit.zip)：冻结协议、源码、全样本CSV、实际机器JSON及验收的确定性ZIP。

正式结题等级**限定人工E1**。未获得新的真实人类计数行为E2、真实历史事件预测E3，也没有检验真实文化传播过程是否是泊松过程。R073及PESEN v0.1始终冻结。下一R185原目录P1/08-009 Negative Binomial Regression（负二项回归），仍保持优先完成所有R系列后统一归纳分类，最后原创模型熔炼。
