# R132 复制子动力学（Replicator Dynamics）：原始1978方程、完整轨迹及数值伪演化

日期：2026-10-20，原239目录P1 05-008。**正式科学状态**：CLOSED_BOUNDED_TAYLOR_JONKER_1978_REPLICATOR_EQ2_EQ3_EQ4_TRAJECTORIES_AND_NUMERIC_ARTIFACTS。
**限定学习完成状态**：LEARNING_COMPLETE_BOUNDED_TAYLOR_JONKER_1978_REPLICATOR_TRAJECTORIES_AND_NUMERICAL_ARTIFACTS。
**实际新真人E2=0、外部历史E3=0；R073及PESEN v0.1均冻结。** 用户规定的239候选R系列必须先完整逐项学习，再统一归类，最后熔炼；此前R131已完成局部雅可比与ESS不等价，R132研究不同问题：**非平衡状态的完整时间轨迹、吸引域和数值积分算法是否制造虚假长期趋势**。

## 真正一手源与公式审计

Taylor, Peter D. & Jonker, Leo B. (1978), [*Evolutionarily Stable Strategies and Game Dynamics*](https://doi.org/10.1016/0025-5564(78)90077-9), Mathematical Biosciences 40:145–156。由[第一作者本人公开研究文献主页](https://sites.google.com/view/peter-taylor/biology/publications)取得[12页真实原刊原始PDF](https://static1.squarespace.com/static/5dc9917c4cdb1467e1e54c4c/t/6526a5647942e33b89ab7af1/1697031525653/1978%2Bevolutionarily%2Bstable%2Bstrategies%2Band%2Bgame%2Bdynamics.pdf)。真正再次截图直接核查原印刷**149页Eq.(2) 连续微分方程、Eq.(3) 离散代和Eq.(4) 离散差分**，150页源循环三策略与过冲、151页源α矩阵相图。必须区分：
- 原Eq2连续：dx_i/dt = x_i[(Ax)_i − x^TAx]；
- 原Eq3**离散世代**：x_i_next=x_i[1+(Ax)_i]/[1+x^TAx]；
- 原Eq4**离散增量**：x_i_next−x_i=x_i[(Ax)_i−x^TAx]/[1+x^TAx]；
- 项目数值近似**Euler**：x_i_next=x_i+h×dx_i/dt；与独立的**四阶RK4**，二者不等于固定1978原Eq3，也不能称为一手原作者数值更新软件。

另检P. Schuster与K. Sigmund（1983）[*Replicator dynamics*](https://doi.org/10.1016/0022-5193(83)90445-9), Journal of Theoretical Biology 100:533–538，只确证出版社书目与摘要关于多学科均出现复制子方程，不虚称本期实际阅读并复算1983原稿全文。

## 完整精确理论不变式与时间结构

源码包含一套原Eq2按每种策略收益减群体平均收益的严格Fraction实现，以及**不调用原Eq2的独立成对策略收益差**实现。对原1978 p150循环 ε=1/2矩阵、p151 α=1矩阵及项目自造三型零和RPS矩阵各有28种合法simplex有理数状态（分母6），共**84个精确对照**；原Eq3与Eq4同样逐84组严格一致。还针对每组状态检查未出现的纯策略导数为0、该状态的离散一代更新仍不出现缺席种类。

若给A全体矩阵每项都加相同c，原连续dx_i/dt不变；若A全体项乘λ>0，则连续dx_i/dt按λ缩放、物理/社会时间因而只是模型内参数重新标度。三矩阵×28状态×3个不同c得**252项平移不变检查**，三矩阵×28状态×3个不同λ得**252项缩放检查**。数值误差和参数时间标尺均不得伪装成真实社会中经科学标定的变化速度。

## 三种来源层级独立标注的二策略吸引域

1. **项目自造常量优势**，行支付[[2,2],[1,1]]：两策略中A份额x有dx/dt=x(1−x)，全部内部0<x<1均单调向1增加。初值x0=1/4、时间t=2可严格数学求解析解 x(t)=1/[1+3exp(−t)]，用作独立于所有积分器的实际误差标杆。
2. **使用R128所核Skyrms2004原鹿兔支付**[[4,0],[3,3]]，但**此动态是项目自行添加，非Skyrms真人实验结果**：dx/dt=x(1−x)(4x−3)。中间分界x=3/4，低于此值向x=0、高于则向x=1，分界两侧是不同吸引域。
3. **项目复用R129的自设Chicken支付**[[-2,2],[0,1]]，属于纯数学而非1973原五策略Table1：dx/dt=x(1−x)(1−3x)，中间x=1/3为内点吸引点，低于向上、高于向下；两个纯边界虽然固定，但不从内部吸引。

以上三个向量场均以Fraction写出精确符号，并用两套独立通用3或2型场公式和专门的一维化简，在13个有理数初始份额×3个模型上做**39个精确交叉核查**。另外明确积分时间t=8的RK4轨迹从鹿份额1/2往下、4/5往上，鸡鹰份额1/10往上、4/5往下；不能把有限次RK4近似称作数学上已经精确吸收入固定点。

## 核心新增数值反例：循环结构中假外漂

项目**自设**而不是原1978 p150负对角的零和三策略反对称循环RPS矩阵：
[[0,−1,1],[1,0,−1],[−1,1,0]]，初始(x0,x1,x2)=(1/2,3/10,1/5)。由于A反对称，群体收益x^T Ax=0，各列和=0，所以**连续理论**有严格的无噪声不变量
d/dt ln(x0 x1 x2)=Σ_i (Ax)_i−3x^TAx=0，乘积初始**P=3/100**且沿每个全正真实数学轨道必须一直相同。另对10个全部坐标正的有理数格点严格Fraction审计该恒等式。

但电脑积分时：
| 步数n；固定最终时间T=12 | Euler 计算出的乘积误差 | RK4计算出的乘积误差 |
|---:|---:|---:|
| 40 | −0.010113456 | +0.0000001020974 |
| 80 | −0.004351948 | +0.00000000418475 |
| 160 | −0.001980490 | +0.000000000192915 |
| 320 | −0.000941619 | +0.00000000000991390 |

**此数值已通过真实GitHub Actions的机器收据回读**，不是未经验证的随意量级。Euler长期偏离严格不变量，可能把数学守恒的中性周期结构画成向外螺旋并让研究者误读为群体越来越靠近边界；RK4误差在这一特定网格下远小，**但RK4仍不是理论上严格守恒的专门几何积分法**。原Taylor/Jonker1978 Eq3一代复制不是这里普通Euler；严禁将此表具体误差说成原作者1978观测的生物种群轨迹。

## 真实CI、机器证据与阶段科学边界

[真实GitHub Actions运行39365994655](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39365994655) **completed success，70项真正标准库unittest全部通过，0项失败**。真正自动再核84原Eq2/3/4状态、252平移与252缩放核验、10个全正RPS理论守恒状态、39个二策略一维精确比较、常量优势t=2解析Logistic解在40/80/160/320步的双算法误差收敛以及RPS四网格人工漂移。320步RK4对真Logistic解绝对误差约**5.97×10^−13**，RPS乘积守恒漂移约**9.91×10^−12**，后者不是严格等于0。

CI运行成功后机器人真实写回源码、测试、科研报告三文件SHA256 [机器独立验收收据](R132_PHASE_A_70_TEST_84_EXACT_STATES_RPS_ARTIFACT_CI_ACCEPTANCE.json)，并由仓库连接器回读。归档：
- [事前冻结协议](../../protocols/R132_TAYLOR_JONKER_1978_REPLICATOR_TRAJECTORIES_AND_NUMERICAL_ARTIFACTS_PRESCORE_FREEZE_2026-10-20.md)
- [原刊来源审计与数值结果科学报告](R132_TAYLOR_JONKER_1978_REPLICATOR_TRAJECTORIES_AND_NUMERICAL_ARTIFACTS_SCIENTIFIC_REPORT_2026-10-20.md)
- [Python Fraction精确函数与标准库Euler/RK4动力学源码](r132_replicator_1978_exact_invariants_and_trajectories.py)
- [70项真正单元测试](test_r132_replicator_1978_exact_invariants_and_trajectories.py)
- [真实CI三文件SHA256及轨迹、守恒误差凭据](R132_PHASE_A_70_TEST_84_EXACT_STATES_RPS_ARTIFACT_CI_ACCEPTANCE.json)
- [正式科研和证据边界](R132_FINAL_ACCEPTANCE_STATUS.json)

复算：PYTHONPATH=research/R132 python -m unittest -v research/R132/test_r132_replicator_1978_exact_invariants_and_trajectories.py。

**证据边界：** R132严格复算1978原文复制子机制并为有限自行构造博弈求得数学趋势和数值误差，**没有从真人或动物逐行时间序列估计任何支付、更新速度或群体初始频率**，没有新人级独立预测E2，也没有外部历史事件E3。没有再现Taylor/Jonker1978全体连续相图或Schuster/Sigmund1983全文。下一R133独立专项检验进化稳定策略的一般严格判别，不将本轮三型特例冒称该领域的全模型证明。全R系列完成后才统一归类，再熔炼；R073/PESEN v0.1保持冻结。
