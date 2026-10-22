# R214-S2 回归不连续设计补充研究：离散支持下的连续性识别失败、7168条原噪声来源与精确偏差—方差

日期：2026-10-22（Asia/Taipei）。原239条目录09-005 Regression Discontinuity Design（RDD，P1）。本文件是**R214的独立补充研究R214-S2**，科学状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_DISCRETE_RDD_SUPPLEMENT**；**不替代原R214正式结题**、不另占239项目录计数，新增真人E2=0、真实历史E3=0。

## 来源文献、先验冻结与正式原R214的区别

Imbens and Lemieux (2008), [Regression discontinuity designs: A guide to practice](https://doi.org/10.1016/j.jeconom.2007.05.001), *Journal of Econometrics* 142(2):615–635；Lee and Lemieux (2010), [Regression Discontinuity Designs in Economics](https://doi.org/10.1257/jel.48.2.281), *Journal of Economic Literature* 48:281–355；McCrary (2008), [Manipulation of the running variable in the regression discontinuity design: A density test](https://doi.org/10.1016/j.jeconom.2007.05.005), *Journal of Econometrics* 142:698–714。经典RDD从门槛附近两侧条件结果极限及潜在结果连续性假设识别局部处理因果效应，并需要审查密度操纵、函数外推及支持。此次**没有执行McCrary密度检验**、真实调查或任何作者的原数据/程序；更不能从本次人工网格声称拥有阈值附近任意密集的观测。

R214此前已在[正式原报告](R214_SCIENTIFIC_REPORT_2026-10-22.md)完成**12种人工世界、固定四个X位置、192条完整原噪声来源**，原本正式验收由[原R214状态文件](R214_FINAL_ACCEPTANCE_STATUS.json)、[原R214机器SHA验收](R214_FINAL_MACHINE_ACCEPTANCE.json)和[原始完整结果](R214_EXACT_RESULTS.json)支撑。本项在原正式结题之后另行创建事前冻结协议[7人工世界×7168原来源S2协议](../../protocols/R214_RDD_7_WORLDS_7168_ORIGINAL_GRIDS_PRESCORE_FREEZE_2026-10-22.md)，提交[5232ca17](https://github.com/edwardsage419/Psychohistory-Research/commit/5232ca176681e13fdd06ea82db000da529addf42)，严格固定更大十点网格、七种全真潜在结果函数、1024条独立扰动向量、局部常数和局部线性两种方法、四个带宽、两路真实均方损失评价以及全部反例，先于代码和完整评分。

## 全部真实人工来源与冻结统计

固定阈值c=0、观测位置X=(-5,-4,-3,-2,-1,1,2,3,4,5)，真正观察**没有x=0，也没有−1到+1之间的任何位置**；单位按x符号接受sharp处理`D=1{x>0}`。人工七个真世界各拥有这些固定位置各一次观测，实际结果在已冻结真潜在结果均值上加独立等概率Rademacher噪声ε_x∈{−1,+1}。十个位置全部2^10=1024种完整原扰动向量、各概率1/1024；七真世界共**7168条实际完整人工原来源**。每条记录原十噪声、所有十实际观测结果及八个候选估计值和八个真正因果目标平方误差。不是7168个真人或7168次独立现实试验，也不是历史前瞻测试。

七固定源均从完整连续x函数构造潜在条件结果`Y0(x)=m0(x)+ε`、`Y1(x)=m0(x)+τ(x)+ε`。真阈值因果目标τ(0)从**人工SCM结构oracle**得出，观察估计器从未获准看到未知区间的基线、真实因果效应或真模型名称。七世界：
* FLAT_TAU2：m0=0，τ(x)=2。
* LINEAR_TAU2：m0=x，τ(x)=2。
* CURVED_TAU2：m0=max(0,x)^2，τ(x)=2。m0在0左右**一阶连续**，但右侧二阶曲率。
* HETEROGENEOUS_TAU2：m0=0，τ(x)=2+x。阈值真实τ(0)=2，但实际右侧处理效果随x升高。
* NULL_FLAT：m0=0，τ(x)=0。
* INVALID_BASELINE_STEP：m0=2·1{x>0}，τ(x)=0。潜在对照均值在阈值自身不连续，违反经典有效RDD的相关连续性条件。
* CONTINUOUS_HIDDEN_RAMP：τ(x)=0，m0=0 when x≤0；m0=2(6x⁵−15x⁴+10x³) when 0<x<1；m0=2 when x≥1。这个未处理潜在均值在0左右**连续且一阶与二阶导数连续**，但是实际网格没有任何x落在(0,1)，所以即使这种基线在0的真实极限仍为0，十个实测点右边都为2。

每侧取最近的h=2,3,4,5个位置，两种预冻估计器：LOCAL_CONSTANT取处理侧与对照侧两个平均数差；LOCAL_LINEAR在每侧用h点最小二乘拟合截距和一次项，取两个x=0边界截距之差。对每份实际人工来源，两种估计均依据观察十个Y独立计算，线性截距同时用**独立普通最小二乘正规方程**与**预冻结Fraction权重内积**两路核对，绝不把真实τ或潜在反事实混入。7世界×4带宽×2估计器=**56个完整条件评分**，全部原来源均保存。

风险为每原来源`(τhat−真实人工τ(0))²`，对各世界1024全部原噪声来源等权平均。额外完全解析Fraction独立检查：`E[τhat]=Σ_i w_iµ_i`，`Bias=E[τhat]−τ(0)`，`Var[τhat]=Σ_i w_i²`（每个独立ε_i方差1），`MSE=Bias²+Var`。**56种配置实际1024来源均方误差、均值、方差与独立解析式逐Fraction严格相等**。实验存在真实oracle的结果对照，但并未实际从该离散资料识别真实阈值因果参数。

## 七人工世界的固定评分（四带宽完整56项见JSON）

下表列出最小h=2和最大h=5的八个预冻组合中四个代表；统计目标是真实人工τ(0)，该值只有生成者在本实验才知道。LC为局部常数，LL为局部线性，越小表示对人工真目标平方误差越小。

|真世界|τ(0)|LC h2 MSE|LC h5 MSE|LL h2 MSE|LL h5 MSE|
|---|---:|---:|---:|---:|---:|
|FLAT_TAU2|2|1|2/5|10|11/5|
|LINEAR_TAU2|2|10|182/5|10|11/5|
|CURVED_TAU2|2|29/4|607/5|14|256/5|
|HETEROGENEOUS_TAU2|2|13/4|47/5|10|11/5|
|NULL_FLAT|0|1|2/5|10|11/5|
|INVALID_BASELINE_STEP|0|5|22/5|14|31/5|
|CONTINUOUS_HIDDEN_RAMP|0|5|22/5|14|31/5|

更细的各世界八种真实精确预期估计值、Bias、Var、MSE，连同全部十位置估计器权重及56条件的独立计算双路信息在[完整S2精确结果JSON](R214_S2_EXACT_RESULTS.json)；十原冲击与八估计及真评分在[7168条完整原来源CSV](R214_ALL_7168_ORIGINAL_TEN_POINT_SHOCK_SOURCES.csv)。

### 反例一：即使真未处理基线在阈值连续，只用有缺口的离散支持仍不可识别阈值因果效果

FLAT_TAU2、INVALID_BASELINE_STEP与CONTINUOUS_HIDDEN_RAMP在**所有十个实际可见X下完整潜在观察条件分布逐项完全相同**：每个x<0实际Y均值0、每个x≥1实际Y均值2；十个独立Bernoulli符号噪声全1024原来源一一对应。因此**全部任何仅用十个实际可见(X,Y)输入的模型给出相同分数/预测**，无论局部常数、局部线性还是更复杂黑盒模型，都不能从当前观察资料内部区分三种真生成机制。但实际阈值处理因果效应在FLAT是2，在另外两模型是0。

特别第三种HIDDEN_RAMP**没有任何潜在未处理基线在0处不连续**；五次幂smoothstep函数在(0,1)内部从0平滑增加至2，但研究样本恰缺少全部(0,1)支持，故它与存在真实处理效果的平坦模型在离散已观察点完全同分布。这比“仅潜在结果不连续才导致识别失败”多出一个独立条件：**仅仅在阈值处假设连续，不对离散观测点之间的函数变化施加更强光滑/曲率限制、或没有越来越密集地趋近阈值的观察支持时，无法非参数点识别tau(0)**。这个严格人工反例不能被当前来源内的随机验证消除，因为观察数据分布本身完全相同。

### 反例二：曲率与效应异质性引起真实外推误差

真LINEAR_TAU2时，局部常数h5的估计期望为8，与真效果2相差+6，其MSE=6²+2/5=182/5；局部线性h5恰消除人工一次斜率偏差，MSE只有方差11/5。可这并不说明更复杂永远更好：真平坦FLAT_TAU2时局部常数h5的方差/MSE为2/5，明显低于局部线性h5的11/5。

在CURVED_TAU2，处理前潜在基线在阈值处连续且导数也连续，但正侧的二次曲率使局部线性h2产生−2的外推偏差，MSE=10+4=14；增大带宽到h5，右侧局部一次拟合偏差为−7，MSE=49+11/5=256/5。局部线性在有限支持下不保证无偏，它只是与人工一次趋势兼容，而不是自动满足未知的真回归函数形式。

在HETEROGENEOUS_TAU2，真因果效果τ(0)=2，而正侧实际各点的处理效果为2+x；局部常数h2+h5的期望分别7/2和5，都不是阈值目标2；局部线性由于此次真源恰保持一次趋势，在两带宽都无偏。这个结果不适用于非线性处理效应函数或变量排序。

### 反例三：变更带宽并不使固定离散点自动贴近0

所有四个冻结带宽h=2,3,4,5包含的**最靠近阈值实际观察位置仍始终为±1**，即使从h5缩至h2，最近距离不变。在FLAT模型中局部常数h增加会降低噪声方差；在LINEAR中局部常数h增加使偏差更严重。不能将这两组有界人工风险经验误读成真实连续运行变量的最佳带宽公式，或声称本实验已经验证经典RDD的h→0极限理论。

## 执行、版本冲突审计与恢复

由于本R214-S2补充是在原R214已正式结题之后并行推进，最初的附加计算脚本意外采用了原R214的两个同名默认结果路径`R214_EXACT_RESULTS.json`和`R214_FINAL_MACHINE_ACCEPTANCE.json`。因此[第一批补充CI run39742862547](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39742862547)虽然计算上三job均成功，归档中却**暂时覆盖**了正式R214在相同路径下的192来源结果与机器收据。对此没有将原结果当作研究缺失或悄然调整科学数字。审计后先将全部S2结果保留为独立[新S2主结果](R214_S2_EXACT_RESULTS.json)与[新S2机器收据](R214_S2_FINAL_MACHINE_ACCEPTANCE.json)，然后从正式原R214机器人归档[af59326b](https://github.com/edwardsage419/Psychohistory-Research/commit/af59326bd3990d83e94e1d490ce5e839f2d5d3ce)**精确恢复原两个相同文件路径**，恢复分别提交[4ef75b1e](https://github.com/edwardsage419/Psychohistory-Research/commit/4ef75b1eeb8f42a37cc57cbaa723aa51160c70d8)与[7f105530](https://github.com/edwardsage419/Psychohistory-Research/commit/7f1055301b9acc76d0c02c31d6f490f3b411d078)。原R214科学报告、原12世界192来源CSV、原机器验收与正式结题状态不作覆盖；原正式结果SHA256仍为`c4b5ba7fbc8d4371a3c796e8bffb3890a286be9c114318bd4f3f2ee6b8a03465`。

为避免复发，另行修改补充脚本[cec5f0f9](https://github.com/edwardsage419/Psychohistory-Research/commit/cec5f0f9b73d37590c71062c97861a37356c6361)和补充工作流[6e993e71](https://github.com/edwardsage419/Psychohistory-Research/commit/6e993e716ab3946d4f49dbb6825facd9f7809d18)，**固定仅写S2独立前缀的结果与验收文件**。二者更新之间的过渡CI run39743146769因旧工作流与新脚本不匹配、归档job失败；这是一项真实的程序流程失败，不能算正式成功，也没有替换合法数据。最新[正式S2 GitHub Actions run39743169253](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39743169253) Python3.11及3.12各**40单测**、合计**80次成功**，第三审计7168完整原观测、56种评分、独立公式、官方原R214保留声明及S2结果SHA并**只向补充结果S2路径永久写入**，三job均success；机器人完成增量归档[73372995](https://github.com/edwardsage419/Psychohistory-Research/commit/73372995fd7eeb0c21b8829a7cfd181e549bb82c)。原R214正式结果与S2两个完整数学源现在同时存在。

## 全部证据文件与SHA

* [S2新增事前冻结协议](../../protocols/R214_RDD_7_WORLDS_7168_ORIGINAL_GRIDS_PRESCORE_FREEZE_2026-10-22.md)。
* [S2纯Python实现与40项单测](r214_exact_discrete_rdd.py)，`--test`或`--emit`。
* [S2完整七世界及56配置机读分数](R214_S2_EXACT_RESULTS.json)，SHA256 **`db406a60f006a9a149a4327dcd9c53198f7874c4b9877868a4db6e9e0e0ebeb6`**。
* [S2完整7168原扰动路径和实际估计/真误差](R214_ALL_7168_ORIGINAL_TEN_POINT_SHOCK_SOURCES.csv)，SHA256 **`3d8f2b65b19b38fab20317f514d950309bd3507abb7f1a6c5c034bb242f8424a`**。
* [S2机器原数据验收收据](R214_S2_FINAL_MACHINE_ACCEPTANCE.json)，保存原完整来源数、分析双路一致性及S2真实SHA。
* [S2正式有界E1结题记录](R214_S2_FINAL_ACCEPTANCE_STATUS.json)，与原正式[R214结题收据](R214_FINAL_ACCEPTANCE_STATUS.json)彼此独立。
* [正式原R214研究及192源科学报告](R214_SCIENTIFIC_REPORT_2026-10-22.md)，未改动，不因补充研究提升原R214的证据等级。

**结论**：R214-S2仅补充原RDD条目下另一种更严格的数学可辨识性反例；原R214仍维持原12世界192条有界E1正式结题，不能因新增7168来源重新算一次239条目录完成。新增真人E2、真实历史E3仍是0；R073/PESEN v0.1保持冻结。下一原主线应根据真实239目录和仓库当前进度核定；在本补充研究执行时，**R215 09-006 Difference in Differences正式研究及三期独立补充均已在main**，不能重复建立同ID研究；后续真实原目录按下一项继续。
