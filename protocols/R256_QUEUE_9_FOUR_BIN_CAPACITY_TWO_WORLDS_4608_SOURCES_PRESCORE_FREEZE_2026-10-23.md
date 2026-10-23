# R256 排队理论：九人工四时格有限容量单服务台、4608完整外生来源；事前模型冻结

日期2026-10-23（Asia/Taipei）。原239候选目录`11-016 Queueing Models`（P2），研究编号R256。用户顺序继续：完成全部原R→统一分类→最后熔炼。所有模型仅有限人工数学E1，新增真人E2/历史E3=0，R073及PESEN v0.1冻结。

## 参考及严格不复现条件

D. G. Kendall (1953), [*Stochastic Processes Occurring in the Theory of Queues and their Analysis by the Method of the Imbedded Markov Chain*](https://doi.org/10.1214/aoms/1177728975), *Annals of Mathematical Statistics*, 24(3):338–354。Kendall A/S/c 排队表示与离散嵌入链有关。本R**不是**真正的无限容量连续时间M/M/1：不存在指数服务时间、泊松可同一时间段多次到达、完整实际客户等待时间或平稳长期稳态；本项目只用长度4时间格、每格最多一次到达、最多一次服务、容量2（含正在服务位置）来严格研究有限状态、顺序效应、到达异质性和记录失真。任何模拟队长Q是时间格末的人工整数，不能声称历史公共资源服务系统的经验需求。

## 全部原9位随机结构
每个world`(U,A1,S1,A2,S2,A3,S3,A4,S4)∈{0,1}^9`，每位独立公平、每world完整512原外生结构类型，九world共**4608条完整原source**，每源质量1/512。U是固定4格的潜在类别，其余各时格有独立原arrival bit A_i和service bit S_i；各world冻结确定映射成实际“请求到达”a_i∈{0,1}与“本格可提供服务”s_i∈{0,1}，不是按现实arrival/service定律估计。四格的可见末尾队长`Q1,Q2,Q3,Q4`与人工执行的服务/拒收记录须存全源，oracle真隐藏H1..H4另列。初始Q0=0，最大Q=2，无实体可大于2或小于0。实际可观察只限人工报告Y=Q，不将U及原bits当参与者真实私人类型。

## 9冻结机制
1 IDLE_NO_ARRIVALS：a_i=0，s_i=S_i，先服务后到达，队长始终0。
2 FAST_SERVICE_HALF_ARRIVAL：a_i=A_i，s_i=1，先服务后到达。
3 BALANCED_INDEPENDENT_HALF_HALF：a_i=A_i，s_i=S_i，先服务后到达。
4 DEMAND_ALWAYS_HALF_SERVICE：a_i=1，s_i=S_i，先服务后到达。
5 NO_SERVICE_HALF_ARRIVAL：a_i=A_i，s_i=0，先服务后到达。
6 DEMAND_ALWAYS_NO_SERVICE：a_i=1，s_i=0，先服务后到达，精确轨迹(Q1,Q2,Q3,Q4)=(1,2,2,2)，累计拒收2、服务0，末Q4=2。
7 ARRIVAL_FIRST_BALANCED_HALF_HALF：a_i=A_i，s_i=S_i，**先到达（队满则拒绝），再服务；本格新到者允许同格被服务**。
8 SHARED_DEMAND_ENV_HALF_HALF：a_i=U在四格恒定、s_i=S_i独立公平，先服务后到达。每时格边际请求概率均1/2，但请求序列按同一U跨期相关，不得误称独立同分布Bernoulli到达。
9 STATIC_EMPTY_TRUE_QUEUE_SENSOR_ALIAS：人工“真实物理”隐藏队列始终0，无真实服务与到达；但报告器对相同完整原bit运行BALANCED_INDEPENDENT_HALF_HALF队长算法来产生观察Q1..Q4、报告服务/拒收。故观察队长全路径逐原source与world3完全相同而H_i=0。这只在可伪造报告的假设下构成测量非识别，不表明真实服务系统会误报。

服务优先更新：
`served=min(Q_previous,s)`，
`after_service=Q_previous−served`，
`admitted=a if after_service<2 else 0`，
`rejected=a−admitted`，
`Q_next=after_service+admitted`。
到达优先：
`admitted=a if Q_previous<2 else 0`；
`rejected=a−admitted`；
`served=min(Q_previous+admitted,s)`；
`Q_next=Q_previous+admitted−served`。
所有源的守恒核验`Q_previous + a = Q_next + served + rejected`、总拒收Σreject与服务Σserved、无负队长，并保存4格全部状态。注：两政策的服务都以事件发生顺序来定义，非连续时间服务率，不可直接当现实公平调度优劣结论。

## 独立条件Markov理论和冻结判断
A. 首路线按原9bit枚举512源，全四格具体到达/服务事件确定性执行队列，精确计数所有3^4可能队长路径联合PMF，每条原source权重1/512。
B. **第二理论路线不得调用第一原bit生成器或队列更新函数**：为每个模型直接定义独立状态转移核`T_w(q,q') = Σ_{a=0}¹Σ_{s=0}¹ P(a)P(s) 1{q'=queue_rule(q,a,s)}`，对于shared U world按U=0或U=1的两个条件到达率0、1分别构造T_u并用1/2外混合**全四步路径似然**`(1/2)Π_{t=1}^4 T_u(q_{t−1},q_t)`。不得把shared U世界错误视作边际p=1/2独立到达Markov核。对9个模型的全部81种队长路径，两路线逐项Fraction严格相等，包含零质量路径。
C. 解析预冻结对照：IDLE报告四格全零。DEMAND_ALWAYS_NO_SERVICE报告(1,2,2,2)、服务0、总拒收2、末队长2。BALANCED_INDEPENDENT_HALF_HALF先服务后到达，首格Q1=A1，`P(Q1=1)=1/2`；ARRIVAL_FIRST_BALANCED_HALF_HALF先到达再可服务新人，首格`Q1=A1(1−S1)`，P(Q1=1)=1/4。故同样边际请求/服务概率，事件次序会改变观察队长，禁止将两种政策编码混为一体。
D. Shared U在Q0=0先服务后到达下，Q1=U，故`P(Q1=0,Q2=1)=0`；独立平衡world`P(Q1=0,Q2=1)=1/4`，即使每个时格请求边际1/2、服务边际1/2相同，时间相关性亦可从队长完整历史辨识。**它们的完整队长联合并非完全相同**；不能把特定2阶统计差错写成全路径非识别。
E. STATIC_EMPTY_TRUE_QUEUE_SENSOR_ALIAS的实际物理H_i全0，却在同一原9bit上逐source观察四格Q与BALANCED_INDEPENDENT_HALF_HALF完全相等；若有独立真实到达/服务核查，则人工观测别名可被排除。无真实实验数据，不把此例当现实欺诈事件证据。
F. 第三独立验收同时核对所有原9bit源唯一性/每源1/512、全81队长路径联合、4格守恒、总拒收、服务和最终库存的守恒、两政策和隐藏U反例、完全观察别名、JSON/CSV SHA256；GitHub Actions Python3.11/3.12各≥45真实测试及第三全源永久main归档完成后，再发布有界E1科学报告/科研状态。下一原目录需从239候选继续核实11-017。
