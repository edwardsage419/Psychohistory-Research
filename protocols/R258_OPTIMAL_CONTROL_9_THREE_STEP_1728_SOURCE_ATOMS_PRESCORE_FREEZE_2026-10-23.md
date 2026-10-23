# R258 最优控制：九有限三阶段随机状态控制世界、1728完整外生来源，Bellman递推与512反馈策略独立穷举；评分前冻结

日期2026-10-23（Asia/Taipei）。原239候选目录`11-018 Optimal Control`（P2），拟研究编号R258。用户顺序继续全部原R→统一归类→最后模型熔炼，暂缓个人决策系统；R073及PESEN v0.1冻结。全部只是人工数学E1，新真人E2=0、真实历史E3=0。

## 一手文献、有限模型与前瞻性决策约束
Richard Bellman, *Dynamic Programming* (1957), Princeton University Press, [Dover reprint publisher](https://store.doverpublications.com/products/9780486317199)，动态规划、Markov多阶段决策与最优性原理。R258研究**明确三步、三状态、两个动作、独立二元随机扰动**的折现率1有限时域随机最优控制；不是一般连续时间Pontryagin控制、无约束连续动作LQR或现实政策干预验证。关键是agent在每时点先看到当前状态x_t，选择u_t，然后才看到当期随机扰动d_t；绝不能使政策在决策时读取未来噪声d_t或未来全路径。独立穷举的所有比较对象必须遵守同一非预知信息集。

## 九固定参数world与完整外生结构
冻结初始状态`x0∈{0,1,2}`，对每world的三个时间格t=0,1,2，各有两独立公平原bit`(R0a,R0b,R1a,R1b,R2a,R2b)∈{0,1}^6`，每组两bit形成均匀整数0..3，固定扰动到达`d_t=1 iff (2Rta+Rtb)<4p`，p∈{0,1/4,1/2,3/4,1}。每world全部3初始状态×64六原bit=**192完整来源类型**，九world总**1728原人工结构类型**；world内结构设计权重1/192，但给定某一x0后64外生bit的条件概率必须是每源1/64。每row保存原六bit、x0、三阶段每期x_t、事前控制u_t、事后扰动d_t、x_{t+1}、三期成本、终端成本与总路径成本、原质量。3个x0是设计分层，而非随机抽样的真人初始状态。

所有world冻结状态空间X={0,1,2}、动作U={0,1}（允许x=0时进行预防性动作）、状态转移
[
x_{t+1}=min(2,max(0,x_t+d_t-u_t))
]
与阶段代价`c_t=x_t²+κ u_t`、终端`c_3=τ x_3²`，无额外动态摩擦，也没有社会因果数据。行动总在扰动之前，此转移可能包含状态上限2带来的人工溢出截断，不能充作真实系统等待损失。

冻结九组`(p,κ,τ)`：
1 NO_SHOCK_EXPENSIVE=(0,2,1)
2 NO_SHOCK_CHEAP=(0,1/4,1)
3 HALF_SHOCK_LOW_ACTION=(1/2,1/4,1)
4 HALF_SHOCK_MEDIUM=(1/2,1,1)
5 HALF_SHOCK_HIGH=(1/2,4,1)
6 QUARTER_SHOCK_MEDIUM=(1/4,1,1)
7 THREEQUARTER_SHOCK_MEDIUM=(3/4,1,1)
8 ALWAYS_SHOCK_MEDIUM=(1,1,1)
9 HALF_SHOCK_NO_TERMINAL=(1/2,1,0)。

## 冻结待复算精确解析值
所有动作若期望成本严格相同，以动作u=0（不干预）破平手。第一数学路线自终端`V_3(x)=τ x²`倒推
[
V_t(x)=min_{uin{0,1}}ig[x²+kappa u+
  (1-p)V_{t+1}(mathrm{clip}(x-u))+
  pV_{t+1}(mathrm{clip}(x+1-u))ig]
]
，并对每个t=0,1,2、x=0,1,2冻结输出18? 即九个策略位（3×3）。**策略只读取t与当前x**，绝不窥视当期或未来R/d的实际实现。针对九world的全部64原六bit×三初始状态，真实执行该反馈策略并记录1728条原路径，按每world×每初态64公平原bit重新积分控制总成本，必须逐x0恰等于该Bellman V0(x0)。

第二独立路线不得调用Bellman递推、原source运行器或前馈动作决策函数：独立穷举所有`2^(3×3)=512`种确定性Markov反馈策略`π(t,x)∈{0,1}`，每一策略使用各初态x0及所有8个三次二元扰动d0,d1,d2的独立Bernoulli路径质量`Π_t p^(d_t)(1-p)^(1-d_t)`直接模拟，精确分数计算期望完整总成本。对每world每x0，512策略风险的最小值须严格等于Bellman V0(x0)，且冻结Bellman策略的成本也是这一全域值。另枚举所有`2³=8`个不依赖当期状态、只按时点预定动作的open-loop控制方案，确保`V_feedback≤V_openloop`，不允许把能看见未来的clairvoyant策略当最优可行方案。

九world预冻结三个x0的V0和最优open-loop值如下（顺序x0=0,1,2）：
- NO_SHOCK_EXPENSIVE: V0=[0,3,9], open=[0,3,9]。
- NO_SHOCK_CHEAP: V0=[0,5/4,11/2], open相同。
- HALF_SHOCK_LOW_ACTION: V0=[3/4,21/8,77/8], open相同。
- HALF_SHOCK_MEDIUM: V0=[5/2,9/2,47/4], open=[5/2,19/4,95/8]；x0=1时最优反馈比最佳open-loop低`1/4`，x0=2低`1/8`。
- HALF_SHOCK_HIGH: V0=[35/8,75/8,16], open相同。
- QUARTER_SHOCK_MEDIUM: V0=[5/4,13/4,293/32], open=[53/32,117/32,603/64]；x0=0时严格改进13/32。
- THREEQUARTER_SHOCK_MEDIUM: V0=[11/4,45/8,949/64], open=[11/4,367/64,959/64]。
- ALWAYS_SHOCK_MEDIUM: V0=[3,7,16], open相同。
- HALF_SHOCK_NO_TERMINAL: V0=[3/2,7/2,10], open=[3/2,15/4,10]，x0=1时反馈改进1/4。

此些值来自固定数学规格的事前独立演算，必须由正式原生Python及独立512政策穷举严格重新验证，否则拒绝结题。不得把反馈在某些参数下严格优于无反馈的有限数学事实升格为现实政策建议/用户实证结果。κ变化影响成本/最优策略，p变化影响不确定性，终端τ变化影响末期控制；由于其他world同时改变一些参数，不得随意宣称跨world的单因素因果已识别。

## 完整证据合同
A. 全1728原source必须保留所有六外生bit与3初态，权重1/192、同x0条件六bit各1/64，所有阶段状态严格0..2、动作0/1、扰动0/1，原状态方程和总成本精确Fraction守恒；不作未经独立测试的真实噪声分布拟合。
B. 自Bellman递推源生成过程与**穷举512不同合法反馈策略**的第二数学路线彼此独立，逐world逐x0 V0精确一致；先前R256有限队列可作为概念对照但不可重用其source或将其经验外部有效性继承到本R。
C. 对全部8 open-loop行动序列独立求每初态期望总成本，与所有反馈最优做严格非负差比较，并对HALF_SHOCK_MEDIUM预冻结`1/4,1/8`反馈优势和各world上述V0预期值逐项确认。
D. Python3.11/3.12各至少45个实际单测+第三CI独立archive job读原完整CSV/JSON、核对source数/原bit唯一性/质量、状态转移、总成本、Bellman及512策略独立最优、open-loop不等式和SHA256，成功后永久bot提交main，形成有界E1科学报告与正式验收。下一原目录11-019 Multi Objective Optimization（拟R259，P2），继续全部原R→归类→熔炼。
