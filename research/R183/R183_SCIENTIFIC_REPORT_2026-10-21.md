# R183 逻辑回归：45个固定计数机制世界的有限似然存在性、完全分离与独立预测风险

日期 2026-10-21。原目录P0/08-007 Logistic Regression。正式状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_LOGISTIC**。本研究的全部概率来自固定人工源模型，没有真实人类或历史事件训练/测试样本。

## 来源真实性与先冻结设计

Cox (1958), *The Regression Analysis of Binary Sequences*, https://doi.org/10.1111/j.2517-6161.1958.tb00292.x，提出二元序列与解释变量的关系分析；Albert and Anderson (1984), *On the Existence of Maximum Likelihood Estimates in Logistic Regression Models*, https://doi.org/10.1093/biomet/71.1.1，区分完全、准完全分离和参数存在性；Firth (1993), *Bias Reduction of Maximum Likelihood Estimates*, https://doi.org/10.1093/biomet/80.1.27，讨论惩罚似然的偏差修正。这里只验证自行设计的饱和二组工作逻辑回归，既未对原作者数据拟合，也未实现一般Firth修正算法。

[冻结协议](../../protocols/R183_LOGISTIC_SEPARATION_45_WORLDS_PRESCORE_FREEZE_2026-10-21.md)先于结果以Git commit `28623c4e53834a4572a69e563c1eb05426b37e88`写入main。项目已验证的人工R177源 `r177_four_finite_count_families_exact.py` Git blob SHA1 `2d032513ce84141214b6b3f84df9c0ed9976a02b` 和R177全量概率JSON SHA256 `57410cf2c110ce3117b7af72e4b7473cee0c3ffd013e6fb99fd43de62165a535` 每次实际计算前逐字节验证，输入改变则主动失败。

二元解释量x=0和x=1各对应一个独立训练**群组单元**，每组n∈{4,8,12}次潜在事件，组内可以有正相关或结构零。固定人工真边际概率对(p0,p1)∈{(1/8,1/4),(1/4,1/2),(1/4,1/4)}，最后一项真logit斜率严格为0。固定五种R177来源机制BIN、BetaBinomial浓度2和8、ZIB结构零1/8和1/4。3×3×5=**45组人工世界**，对每一组完整列举`(k0,k1)`支持点，合计**4125条训练计数对**及对应真实生成概率。

## 工作MLE的概率极大与有限系数区别

用两组饱和的`logit(q_x)=alpha+beta*x`形式建立独立Bernoulli工作似然；若组内行为有关联，它是一种错误指定的工作似然，不代表真实数据机制。每一观察组别在闭概率域上极大似然点为q=k/n。这一点同时由完整有理数似然网格`j/(2n)`逐点检验和独立原始score`k−nq=0`及边界符号检验通过。

**闭区间上有概率极大值，并不保证有限alpha,beta。** 只有两个组均0<k<n，二参数Logit MLE才能以有限系数实现；任一k=0或n，至少一个系数需沿极限发散。将两组一组全0、一组全n或其逆向专门标记为**完全分离**，严禁把所有边界样本都叫完全分离。每个世界都以真实人工PMF独立精确计算无限系数概率与完全分离概率，且与全部4125样本逐项加权枚举严格相同。

## 预先冻结的主对照：真实无组别效应

固定n=4且p0=p1=1/4，两组真实logit斜率**恰好为0**。

| 人工训练机制 | 无有限参数MLE的概率 | 完全分离概率 | 无收缩MLE未来Brier期望 | 半计数预测未来Brier期望 | 半计数未来期望logloss |
| --- | ---: | ---: | ---: | ---: | ---: |
| IID_BIN | 53.802% | 0.247% | 0.234375 | 0.220000 | 0.646543 |
| CLUSTERED_BB_C2 | 79.468% | 5.383% | 0.281250 | 0.250000 | 0.732948 |
| CLUSTERED_BB_C8 | 63.635% | 1.157% | 0.250000 | 0.230000 | 0.673958 |
| INACTIVE_ZIB_Z1_8 | 58.861% | 0.411% | 0.241071 | 0.224286 | 0.657763 |
| INACTIVE_ZIB_Z1_4 | 64.883% | 0.737% | 0.250000 | 0.230000 | 0.672858 |

所有模型概率与Brier为Fraction精确数学求和；表内仅显示四舍五入小数，原精确分数保存在机器JSON。正相关明显提高训练样本落在极端边界的概率，增加可能误认为有确定性组别影响的完全分离样本。上述分离概率是指定人工生成过程下的概率，不可替代实证发生率。

## 真正独立测试单元的预测评价

测试采用与训练**单位独立**的新Bernoulli事件，每组各抽一个真实边际概率p_x的事件，随后对两组得分取平均。无收缩预测为q_MLE=k/n，固定比较基线是每组Beta(1/2,1/2)平均`q_H=(k+1/2)/(n+1)`。明确地说半计数预测与一般Firth多变量修正不是本研究声称的同一方法。

真实测试Brier公式为`p(1−q)^2+(1−p)q²`，全部45世界既从每个训练计数对及其联合概率直接累加，又独立从计数期望一阶、二阶矩推导解析Brier，**每个Fraction完全一致**。在锁定主对照中，半计数预测的平均Brier小于无收缩MLE；其余40世界的准确正负差均完整保存，不作普遍优越性的无证推断。

无收缩MLE在所有45世界对至少一个组出现边界概率正，因此面对独立的后续新事件，在真正p∈(0,1)时必有对立结果的正概率，而其对应测试logloss正无穷，从而**所有45世界无收缩MLE的无条件期望未来logloss为INF**。半计数预测始终在(0,1)，故其测试期望logloss有限，每个训练计数对同时用`math.log`和60位`Decimal.ln`计算，两种数值路径差小于1e−12，且45世界全部加权平均相符。正无限是对数评分严格要求与有正概率的边界事件共同引起的，不代表具体训练样本的未来损失必无限。

## 复验、归档与证据限制

[GitHub Actions39561106676](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39561106676) Python3.11和3.12各27项单元测试，**54次单元测试执行全部通过**，第三工作流真实穷举45世界4125行、全部Brier独立推导、边界与完全分离、源SHA以及确定性ZIP完整性；共三个job success。初始完整机器结果提交 [977743d](https://github.com/edwardsage419/Psychohistory-Research/commit/977743d70ef674ec7e3bb3b77b9f908aab6d74bd)。

* [R183_EXACT_RESULTS.json](R183_EXACT_RESULTS.json)：45世界全部人工概率、有限MLE存在率、完全分离率、完整未来Brier及数值logloss。SHA256 `40927bae4616a9d9fc91ed964257a9d436372d9196abd8fabceb40740189a000`。
* [R183_ALL_4125_TRAINING_COUNT_PAIRS.csv](R183_ALL_4125_TRAINING_COUNT_PAIRS.csv)：4125真实来源人工训练计数对、各自生成概率、每组MLE和半计数概率、分离/非有限类别以及真实测试Brier。SHA256 `1dcd2a85c2b241346e8fae8fe85727e2b8c0560fa2916c1e8ce01eb384acf285`。
* [R183_FINAL_MACHINE_ACCEPTANCE.json](R183_FINAL_MACHINE_ACCEPTANCE.json)：独立算法及SHA、样本总量、E1验收及E2/E3证据界限。
* [r183_logistic_separation_exact.py](r183_logistic_separation_exact.py)：完整两条Logit参数审核、双人工计数发生器、两种Brier推导、两种数值logloss及27单元测试。
* [R183_Logistic_45_Worlds_Exact_Separation_Archive.zip](R183_Logistic_45_Worlds_Exact_Separation_Archive.zip)：源代码、协议、原始计数对CSV、结果JSON及正式验收的固定时间戳ZIP。

R183按冻结标准**正式限定E1数学研究结题**。没有真实人群中逻辑分离发生率估计，亦无未经控制的社会事件预测、真实机制因果识别或历史外部检验。新增E2=0、E3=0，R073/PESEN v0.1继续冻结。

下一原目录 **R184 P1/08-008 Poisson Regression**。必须再次先审查原始模型与真实数据边界，坚持完成全部R系列后统一归纳分类、最后熔炼。
