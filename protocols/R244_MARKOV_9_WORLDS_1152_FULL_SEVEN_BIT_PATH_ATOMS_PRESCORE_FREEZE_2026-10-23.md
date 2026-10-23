# R244 马尔可夫随机过程：九人工二态三步完整路径、1152原来源、隐藏转移率使观察非马尔可夫；计算前冻结

日期2026-10-23 Asia/Taipei。真实239原目录 `11-004 Markov Stochastic Processes`（P1），研究编号R244。只针对有限二态三步人工过程的`P(Y0,Y1,Y2,Y3)`、真实有限条件马尔可夫性、时间齐次性和隐藏类别混合导致的历史依赖做严格Fraction检验。不涉及真人E2或历史E3，原R主线不改变，R073/PESEN v0.1冻结。

## 研究一手背景

MIT OCW 18.366 [*Lecture 13: Discrete and Continuous Stochastic Processes*](https://www.ocw.mit.edu/courses/18-366-random-walks-and-diffusion-fall-2006/d53e40fbfc776b5d616fa87b424731ce_lec13.pdf) 给出离散状态条件转移与Chapman–Kolmogorov结构；Fortini, Ladelli, Petris & Regazzini (2002), [*On mixtures of distributions of Markov chains*](https://doi.org/10.1016/S0304-4149(02)00093-5), *Stochastic Processes and their Applications* 100:147–165，研究不同Markov链混合及部分可交换性背景。本R不是其无穷过程表征定理的复现，仅具体计算一个有限隐混合反例。Markov性质在此严格采用`P(Y3|Y2,Y1)=P(Y3|Y2)`，只在相关条件质量正的已支持事件上检验，不将不可观察事件中的条件概率设为0。

## 冻结完整人工来源及观察定义

7个互独立Bernoulli(1/2)外生源`U,R11,R12,R21,R22,R31,R32`，U为个体隐藏转移类型，三步各独立的两位`R_k=(2Rk1+Rk2)∈{0,1,2,3}`。每world完整2^7=128个原source，每source质量1/128，共9×128=**1152条**。人工观察路径从Y0=0起，全部源存Y0…Y3四态完整序列与隐藏oracle H0…H3、U、三步2位噪声和原质量。实际统计仅使用`(Y0,Y1,Y2,Y3)`，绝不把U或oracle机制读入识别器；完整path PMF（8可能路径）精确积分，缺少概率支持的paths保留0信息但不计算非法条件比。

每步有两态对称**stay**概率s（否则flip），用新独立2位R`stay iff R<4s`（固定s∈{1/4,1/2,3/4,1}），全Fraction可精确表示，无Monte Carlo随机误差。ABSORB_ONE状态1 stay1、状态0 stay1/2。

## 九机制

1. `IID_FAIR`：无记忆对称状态翻转/stay概率1/2，真实Y过程时间齐次Markov。
2. `PERSISTENT_3OF4`：每步stay概率3/4，真时间齐次Markov。
3. `ANTIPERSISTENT_1OF4`：每步stay概率1/4，真时间齐次Markov。
4. `ABSORB_ONE`：从0每步以1/2进入1，达到1后绝不离开，真时间齐次Markov但非严格正的全状态转移。
5. `TIME_ALTERNATING_RATE`：第1/3步stay3/4，第2步stay1/4，**仍满足时间指定的Markov条件独立**，但不是时间齐次一矩阵。
6. `LATENT_RATE_MIXTURE`：U=0时个体每步stay3/4，U=1时stay1/4；U整条三步路径保持同一个隐藏类型。给定(Y,U)是扩展状态Markov；只看Y的有限过程通常非Markov。**预冻结强反例**：事件Y2=0时，`P(Y3=0|Y2=0,Y1=0)=7/10`，`P(Y3=0|Y2=0,Y1=1)=3/10`，并且`P(Y3=0|Y2=0)=1/2`；同当前可见状态，过去路径携带有关隐藏U的信息。
7. `STATIC_HIDDEN_SENSOR_ALIAS`：真实H_n=0所有时间不变，观察传感器读取与PERSISTENT_3OF4由同一R生成的完整Y路径；逐原source可见相同而隐藏真实动力不同。
8. `COMPLEMENT_HIDDEN_COORDINATE_ALIAS`：真实内部H_n=1−Y_n，观察把0/1隐藏坐标再取互补，全部source实际Y和PERSISTENT_3OF4相同；隐藏标号是单纯重参数化，不应视为不同社会机制。
9. `FIXED_SWITCH_POLICY`：U=0则每步坚持原状态、U=1则每步严格翻转；三步其余R位仍完整保留但不改变机制。可见只有0000、0101两种四时点路径，各概率1/2。给定Y2=0，若Y1=0则Y3=0必然，若Y1=1则Y3=1必然，因此观察Y非Markov（隐藏U完整扩展状态则Markov）。第一步观察Y1边际与IID_FAIR完全相同但后续路径截然不同。

## 事前冻结评价、算法和验收门槛

A. 第一路线逐128原源模拟所有隐藏H与完整可见Y，积分出8可能4元观察路径联合PMF。第二路线**不得使用原来源CSV/模拟函数**，独立直接按每条完整观察path的逐步转移概率之积计算：齐次Markov常数s、非齐次随k变化的s；LATENT_RATE_MIXTURE是U=0和U=1的两种整路径产品的1/2混合；FIXED_SWITCH_POLICY是两条确定path各1/2。对全部八条可能观察序列精确逐格校验。动态随机观察别名只是指定同一路径产生式，传感器隐藏H的差异须另由oracle验证。
B. 为所有世界计算每个t0..3的P(Y_t=1)。检验在支持为正的`Y1,Y2`条件下`P(Y3=1|Y1,Y2)`与`P(Y3=1|Y2)`的分数差；**Markov defect**定义为这些合法条件对的最大绝对差（所有Fraction），不能因没有支持的组合设置虚假的错误标志。对于IID、PERSISTENT、ANTI、ABSORB、TIME_ALTERNATING、STATIC_SENSOR及COMPLEMENT别名，固定defect=0；LATENT_RATE_MIXTURE及FIXED_SWITCH_POLICY必须strict>0。三步有限检验只能验证有限条件分布，不证明全时间无限过程。
C. 对homogeneous Markov世界的2×2核`P`检验第一、第二和第三步真实条件转移与同一矩阵，及`P²`Chapman–Kolmogorov二步传播。TIME_ALTERNATING_RATE只做矩阵时段产品`P1 P2`，不错误要求P1=P2，且有支持的`P(Y1=0|Y0=0)=3/4`与`P(Y2=0|Y1=0)=1/4`明显不同。
D. 对LATENT_RATE_MIXTURE两不同过去给定Y2=0后的Y3条件概率必须精确为7/10与3/10，而只给当前Y2的概率1/2。FIXED_POLICY对应这两过去的P(Y3=0)为1与0；观测短轨迹的单步边际P(Y1=0)=1/2与IID_FAIR相同并不等于完整路径过程相同。
E. PERSISTENT_3OF4与STATIC_HIDDEN_SENSOR_ALIAS及COMPLEMENT_HIDDEN_COORDINATE_ALIAS在每条相同七比特原来源上完整观察Y0…Y3逐点相同；隐藏H0…H3分别真正Markov改变、始终0与逐位坐标互补。**观察Markov性不独立确认潜在状态就是被观测状态**。
F. 128×9完整原source、JSON完整路径及Markov defect/源oracle、SHA256机读收据，GitHub Python3.11/3.12各≥45实际单测、独立第三job重新生成完整1152原源核验条件概率和Markov性质、概率归一/路径解析公式及SHA后机器人永久归档main；真实CI成功再写报告并标记E1有界完成。
G. 全部人工二态有限路径不代表社会系统真正Markov、没有真实人类决策长序列或历史E3；隐藏类别混合非Markov反例不否定完全观测并满足正确前提下的Markov链应用。下一原239目录需R244结题后查询11-005。
