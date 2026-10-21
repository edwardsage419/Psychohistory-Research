# R197 时间序列 ARIMA：六种离散过程、24人工世界、完整事前选模与真正未来创新预测

日期：2026-10-21。原候选目录 P1/08-021 ARIMA。科学结题范围 **CLOSED_BOUNDED_E1_ARTIFICIAL_PREQUENTIAL_ARIMA**，真人行为E2和历史预测E3新证据均为0。

## 原始来源及模型适用界限

Box and Jenkins (1970), [Time Series Analysis: Forecasting and Control](https://books.google.com/books/about/Time_Series_Analysis.html?id=qsnaAAAAMAAJ), Holden-Day，创立使用自回归、差分/积分与移动平均进行时间序列建模和预测的经典工作体系。Box, Jenkins, Reinsel and Ljung (2015), [Time Series Analysis: Forecasting and Control, Fifth Edition](https://www.wiley.com/en-us/time-series-analysis-forecasting-and-control-5th-edition-p-9781118675021), Wiley，提供经典ARIMA及扩展的系统讨论。R197是自构造**固定已知参数、三点离散独立创新的六种条件ARIMA机制**，目标为短序列平方误差与条件期望独立风险。它不是原著数据复算，不代表统计软件一般ARIMA(p,d,q)未知参数极大似然估计、滚动真实经济序列预测或长期历史解释。所取稳定AR1源强制Y0=0，不处于其非退化平稳初始分布，必须严格区分稳定AR动力学与已经平稳的实际样本。

[计算前冻结协议](../../protocols/R197_ARIMA_24_WORLDS_1944_TRAINING_PRESCORE_FREEZE_2026-10-21.md)先以commit`a27983af1a3231c91ccb3523dadd0813c9b559c8`提交main，之后才编码、评分及生成完整报告。所有研究时间序列、生成系数、噪声分布、候选次序、选模评分及未来评估方式均按原协议执行，未因结果修改。

## 六种受控过程及完整人工训练来源

各原始真实创新ε_t∈{−1,0,+1}，概率(1/4,1/2,1/4)，独立，E ε=0、Var ε=1/2；全部人工轨迹从Y0=0开始。六真实生成过程及固定工作候选为：

* WHITE：Y_t=ε_t；ARIMA(0,0,0)，预测0。
* AR1：Y_t=Y_{t−1}/2+ε_t；稳定系数的ARIMA(1,0,0)，预测h步为(1/2)^h Y_T。
* RW：Y_t=Y_{t−1}+ε_t；ARIMA(0,1,0)，预测Y_T。
* DRIFT：Y_t=Y_{t−1}+1+ε_t；带固定漂移1的ARIMA(0,1,0)，预测Y_T+h。
* DIFF_AR1：ΔY_t=ΔY_{t−1}/2+ε_t，初始ΔY1=ε1；条件ARIMA(1,1,0)，预测`Y_T+[Σ_{j=1}^h (1/2)^j]ΔY_T`。
* DIFF_MA1：ΔY_t=ε_t+ε_{t−1}/2，ε0=0；条件ARIMA(0,1,1)。工作预测只能从已观察差分递推残差`e_t=ΔY_t−e_{t−1}/2`，两步预测均为`Y_T+e_T/2`，不知道真实生成标签或潜在真实创新。

每个真机制独立生成完整有序训练历史T∈{4,5}（不计起点），并在相同训练历史上留出1步或2步未来：6真源×2训练长度×2预测范围=**24个受控人工世界**。每个真源/T完整枚举全部3^T种训练创新路径，合计6×(3^4+3^5)=**1944条人工原始训练序列**，将每条用于两个冻结h时有**3888套原样本/未来风险配置**，六候选分别测试未来独立风险合计**23328个Fraction正确计算的预测误差**。每条原始训练数据有确切来源概率，所有真源/T样本空间原始概率之和逐Fraction严格为1，没有Monte Carlo近似或实验选样。

## 完全不读取未来信息的prequential模型选择

对每条训练序列，从已观察Y0,Y1后，对t=2,...,T逐期用**严格前缀Y0..Y_{t−1}**构造六个候选对Y_t的单步预测，再以已实际观察的Y_t平方损失累加。仅凭各候选过去逐期训练平方误差选模型，最优训练总误差并列固定候选优先WHITE→AR1→RW→DRIFT→DIFF_AR1→DIFF_MA1，绝不使用未来预测误差、真实生成机制名或真实创新序列决定选模。所有训练prequential SSE通过两个独立实现逐Fraction验算：一是逐时点调用完整历史预测器，二是直接在线递推模型条件状态和MA滤波创新，两套对所有1944条历史×六候选**完全一致**。

特别需要澄清，有限训练的prequential平方误差优越不等于模型生成规律的真伪，也不等于独立未来误差低；现有世界只比较固定预选候选，对未知参数拟合或更大的统计结构并无正式科研结论。

## 真正未来独立创新风险：两套Fraction验证

对每个训练历史、预测范围h=1或2、每个候选，用**完全独立新抽取的未来真实创新ε_{T+1},...,ε_{T+h}**完整枚举3^h种结果，计算真条件未来平方误差`E[(Y_{T+h}−f_model(history,h))²|history]`。第二条独立来源生成数学路线仅使用真未来条件均值μ_true与创新冲击响应系数给出已知真方差V_h，计算`V_h+(μ_true−f_model)²`。完整23,328个候选风险**逐Fraction严格相同**；两路线不读取未来样本用于训练选模，真正已知来源预测的oracle风险恰为V_h。预冻结真条件未来方差如下：

| 人工真来源 | 未来1步oracle MSE | 未来2步oracle MSE |
| --- | ---: | ---: |
| WHITE | 1/2 | 1/2 |
| AR1 | 1/2 | 5/8 |
| RW | 1/2 | 1 |
| DRIFT | 1/2 | 1 |
| DIFF_AR1 | 1/2 | 13/8 |
| DIFF_MA1 | 1/2 | 13/8 |

该检验将误差不确定性与选错工作模型造成的额外均值偏差完全分离。全部24世界另保存实际有限训练选中的六模型概率、真来源被选中概率、训练选择预测器的完整未来MSE、固定RW比较基线和已知真来源oracle误差。任何原始风险数字都能从源码和两份原CSV重放。

## 事前冻结的稳定与积分过程对照：过度选模风险

包括WHITE、AR1、RW、DIFF_AR1、DIFF_MA1在内的五个来源，都有同样第一条观测Y1=ε1；仅凭第一条观测不能识别差分、AR或MA真实结构。DRIFT有E(Y1)=1，其水平漂移信息是另外一种可辨现象。AR1虽然系数稳定且长期回归均值，但初始状态Y0=0，不应把这批短轨迹当成“严格平稳抽样”；RW/DRIFT/DIFF_AR1/DIFF_MA1都有单位根积分关系，单做一阶差分不会自动决定未来差分过程是否有条件动量或移动平均相关。

训练长度T=5时，全部真来源轨迹完全加权后如下（MSE越低越好）：

| 真生成机制 | 未来范围 | 真来源模型被选中 | 选模后未来MSE | 固定RW未来MSE | 真来源oracle未来MSE |
| --- | ---: | ---: | ---: | ---: | ---: |
| WHITE | 1步 | 76.76% | 0.57679 | 1.00000 | 0.50000 |
| AR1 | 1步 | 39.45% | 0.67424 | 0.66650 | 0.50000 |
| RW | 1步 | 33.01% | 0.67216 | 0.50000 | 0.50000 |
| DRIFT | 1步 | 83.30% | 0.66736 | 1.50000 | 0.50000 |
| DIFF_AR1 | 1步 | 37.21% | 0.69140 | 0.66650 | 0.50000 |
| DIFF_MA1 | 1步 | 43.55% | 0.72626 | 0.62500 | 0.50000 |
| WHITE | 2步 | 76.76% | 0.56311 | 1.00000 | 0.50000 |
| AR1 | 2步 | 39.45% | 0.94567 | 0.99963 | 0.62500 |
| RW | 2步 | 33.01% | 1.32096 | 1.00000 | 1.00000 |
| DRIFT | 2步 | 83.30% | 1.65516 | 5.00000 | 1.00000 |
| DIFF_AR1 | 2步 | 37.21% | 2.13784 | 1.99963 | 1.62500 |
| DIFF_MA1 | 2步 | 43.55% | 2.17320 | 1.75000 | 1.62500 |

真正随机游走RW来源下，先固定正确RW预测器，未来1步真实MSE=0.5、2步=1；如果依据短训练序列的逐期prequential SSE从六候选挑选，真正未来MSE上升为≈0.67216、1.32096，说明在极短序列里引入多个候选且根据训练表现选模可能损害预测。真DRIFT来源中，包含正确的带漂移候选明显好于错误固定RW（h2 1.65516 vs 5.0），展示额外模型复杂性有时具有重要预测价值；但是同样由于有限训练误选，仍高于真来源oracle h2=1。不能通过“含漂移更好”就声称真实历史趋势有某个确定漂移。

**不能仅比较h1和h2误差大小得出优劣**，因为h不同、真未来噪声累积方差不同。更合理比较是同一个真来源和同一预测h下，各预先确定预测器的独立风险或相对oracle超额损失。R197数据保留固定RW和完整六候选，供未来模型分类时重新分析，不在当前研究阶段进行模型融合。

## GitHub三个CI job与完整不可变原始档案

[GitHub Actions39588989130](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39588989130)在Python3.11和3.12各运行37项原生单元测试，共**74次success**；第三job真正执行24世界、1944原始训练轨迹、3888独立未来配置、23328未来测试风险的全部数学Fraction验证，核验完整两CSV的行数、真实源机器验收SHA和固定时间六文件ZIP并永久提交main，三个jobs均success。正式结果提交[d01e1a42](https://github.com/edwardsage419/Psychohistory-Research/commit/d01e1a42aa793f2037befe1d668253d540296991)。

* [R197_EXACT_RESULTS.json](R197_EXACT_RESULTS.json)：全部24世界真实选模分布、固定RW与oracle基线、完整模型风险、差分与短期记忆对照，SHA256`72a233ddc6823c43f3a22e36660c47bf7769ed9b6ce400e46b01487763de7931`。
* [R197_ALL_1944_ORDERED_TRAINING_PATHS.csv](R197_ALL_1944_ORDERED_TRAINING_PATHS.csv)：完整1944条原始创新序列、五步内真实人工观测水平、生成概率和六模型prequential训练分数，SHA256`0fdcfcc7b34571d2669a9014bd410b9f72bfd3bdef1c5ca5e85915a323fd65ca`。
* [R197_ALL_3888_INDEPENDENT_HELDOUT_RISK_PROFILES.csv](R197_ALL_3888_INDEPENDENT_HELDOUT_RISK_PROFILES.csv)：完整1944原始训练×h1/h2共3888条配置，记录真实未来条件均值和方差、六模型预测数值和全部23328个Fraction独立新创新风险，SHA256`ba7414db22ad1a369a52790fadbaf4676d8bc211f1bd976ef0b81eb9e261f92c`。
* [R197_FINAL_MACHINE_ACCEPTANCE.json](R197_FINAL_MACHINE_ACCEPTANCE.json)：双训练与双真实未来评分数学证明、全部数据SHA与E1限界。
* [r197_exact_prequential_arima.py](r197_exact_prequential_arima.py)：六固定ARIMA型人工生成机制、MA可逆残差、严格过去prequential训练、独立未来创新枚举与oracle解析风险及37项测试。
* [R197_Exact_24_Prequential_ARIMA_Worlds.zip](R197_Exact_24_Prequential_ARIMA_Worlds.zip)：冻结协议、完整源码、两份原CSV、结果JSON和正式机器验收的可重放固定时间ZIP。

研究证据仅达**E1人工短序列ARIMA型预定参数过程的机制和留出未来新创新预测**，没有实际拟合/评估真实人类、长期经济/制度历史或社会时间序列，新增E2/E3均为0。R073与PESEN v0.1继续冻结。下一既定原目录 **R198 P1/08-022 State Space Models（状态空间模型）**；全部R研究完成之后统一归纳分类，最后熔炼。
