# R256 排队理论：九人工有限四时格双容量队列、4608全外生来源、事件次序和到达共同环境

日期2026-10-23（Asia/Taipei）。原239目录`11-016 Queueing Models`（P2）。正式状态`CLOSED_BOUNDED_E1_FINITE_CAPACITY_TWO_FOUR_SLOT_QUEUE_AND_MARKOV_PATHS`。本研究只复算明确指定的人工四格、容量2、每格最多一次到达和一次服务的离散队列概率，**绝非真实连续时间无限容量M/M/1**：无Poisson同格多到达、指数服务/等待时间或平稳稳态、没有可验证的真人窗口或历史公共资源数据。新E2=0、E3=0。R073与PESEN v0.1冻结。

## 一手来源、冻结范围与真实排队过程的区别

D. G. Kendall (1953), [*Stochastic Processes Occurring in the Theory of Queues and their Analysis by the Method of the Imbedded Markov Chain*](https://doi.org/10.1214/aoms/1177728975), *The Annals of Mathematical Statistics* 24(3):338–354，是马尔可夫嵌入链与排队理论的重要原始来源。本R只构建带明确容量和时间格更新顺序的**有限Markov队长路径**，虽借鉴嵌入链概念，但没有外推到真实M/M/1，不能据此宣称测出了现实系统利用率、拥堵时长、客户平均等待时间或制度公平性。

[事前冻结九world、全部外生原来源、两种事件次序和独立路径概率验收协议](../../protocols/R256_QUEUE_9_FOUR_BIN_CAPACITY_TWO_WORLDS_4608_SOURCES_PRESCORE_FREEZE_2026-10-23.md)先独立提交[d16f5d3c](https://github.com/edwardsage419/Psychohistory-Research/commit/d16f5d3c5cecade05e43c583573b34d0571801bb)，再实现源码、检验和归档。

## 完整九位外生源，原source及排队守恒

九个world各有一个公平U位（可作为全期隐藏类别）及四时格独立两位`A_t,S_t`（原到达bit、服务bit），即`(U,A1,S1,...,A4,S4)`独立公平，总共9位。每world完整2⁹=**512个原外生结构来源**、每来源概率1/512；九world**4608条完整原source**。不同world用冻结确定函数将原A/S/U映射到每格实际请求`a_t∈{0,1}`和可用服务`s_t∈{0,1}`，q初始0、最大2。源逐格保存请求、可提供服务、实际执行服务、接收、拒绝及队长Q1…Q4、真实隐藏H1…H4和全过程守恒凭据，非4608个真人客户。

每一格无论采取先服务还是先到达，源级守恒恒等式`Q_{t−1}+a_t=Q_t+served_t+rejected_t`且0≤Q≤2。累计全四格`Σ offered=Σ served+Σ rejected+Q4`。两个制度政策由**事件发生顺序**精确定义，而不是把服务规则作为可无视的细节：

- `SERVICE_FIRST`：既有队长q可先服务一名，空出位置后再决定是否接收本格新来任务。一个原本空队列中的新到者不在本格被服务。
- `ARRIVAL_FIRST`：先尝试接收新任务，若到达前满载则先拒收；随后提供的一份本格服务**可以处理本格刚加入的任务**。

除事件次序之外，BALANCED_INDEPENDENT_HALF_HALF与ARRIVAL_FIRST_BALANCED_HALF_HALF有同样的每格边际请求概率1/2和服务概率1/2；差异仅为更新协议，而不能未经条件披露把两者称为同一队列。

## 双独立路线完整队长路径分布

第一路线完全原9bit枚举，一步步计算每格实际a/s、服务优先或到达优先更新、所有保留和拒收，按原外生质量1/512积分可见队长Q1,Q2,Q3,Q4联合。第二路线**不读取完整原source也不调用源队列更新函数**，直接从冻结独立Bernoulli(a)、Bernoulli(s)及3状态q=0/1/2的代数更新关系枚举四组合概率，构造3×3 Markov核`T(q,q')`。把四格路径似然写为`Π_t T(q_{t−1},q_t)`并逐路径与512全源积分相符。对于共享固定U的world，不错误地将总体边际请求p=1/2当作跨期独立：理论路线分别在U=0/1条件下构造到达率0/1的核，随后计算`(1/2)ΠT_{U=0}+(1/2)ΠT_{U=1}`混合，完整81种可能的四位队长路径全部逐项Fraction相等（零支持路径恰0）。虚拟报告world只有可见队长走平衡核，oracle物理队列始终0，说明理论拟合的对象是**报告层分布**而不是真实物理队长。

## 九个人工排队世界的精确结果

| 冻结world | E[末时格Q4] | 四格E[实际服务] | 四格E[拒收] | 四格E[请求] |
|---|---:|---:|---:|---:|
| IDLE_NO_ARRIVALS | 0 | 0 | 0 | 0 |
| FAST_SERVICE_HALF_ARRIVAL | 1/2 | 3/2 | 0 | 2 |
| BALANCED_INDEPENDENT_HALF_HALF | 129/128 | 29/32 | 11/128 | 2 |
| DEMAND_ALWAYS_HALF_SERVICE | 15/8 | 3/2 | 5/8 | 4 |
| NO_SERVICE_HALF_ARRIVAL | 13/8 | 0 | 3/8 | 2 |
| DEMAND_ALWAYS_NO_SERVICE | 2 | 0 | 2 | 4 |
| ARRIVAL_FIRST_BALANCED_HALF_HALF | 165/256 | 325/256 | 11/128 | 2 |
| SHARED_DEMAND_ENV_HALF_HALF | 15/16 | 3/4 | 5/16 | 2 |
| STATIC_EMPTY_TRUE_QUEUE_SENSOR_ALIAS | 报告129/128、真0 | 报告29/32 | 报告11/128 | 报告2 |

所有表格数据均为完整512原source概率平均而非经验估计，逐world满足`E offered=E served+E rejected+E Q4`：例如平衡先服务模型`2=29/32+11/128+129/128`，到达先模型`2=325/256+11/128+165/256`。拒收预期在这两个四格人工设置中**恰好一样**11/128，但服务次数和末尾队长不同。因此**不同更新规则可以改变工作在第几格被处理，却在某个有界特例中产生相同总拒收均值**；不能只用一项总体指标断言政策等价或普遍优越。

### 事前冻结并已独立验收的具体反例

**事件先后顺序决定首格队长概率。** 平衡先服务world从Q0=0开始，本格没有旧任务可处理，无论S1如何，首格`Q1=A1`，所以`P(Q1=1)=1/2`。同样a/s边际但到达先world可在同一格服务新到任务，首格`Q1=A1(1−S1)`，因此`P(Q1=1)=1/4`。两种独立模型的完整四步联合PMF不同，不应将其平均或混成一个不可核查的“系统拥堵率”。

**单期到达边际相同，跨期U相关却可改变序列规律。** BALANCED_INDEPENDENT_HALF_HALF每格A独立公平；`P(Q1=0,Q2=1)=1/4`。SHARED_DEMAND_ENV_HALF_HALF令`a_t=U`四格固定且U仍公平：每个时间格的请求边际也仍为1/2，但若Q1=0必U=0，此后Q2=1不可能，所以`P(Q1=0,Q2=1)=0`。此结果强调历史观察对隐藏类别有后验信息，错误地强加“请求随时间独立”的Markov核会误算整个路径概率。**两个world的完整联合确实可区分**，这里并没有声称相同完整观测下异质性与独立过程严格等价。

**容量限制与记录真假。** DEMAND_ALWAYS_NO_SERVICE四个格都请求1、都不能服务，队长路径恒(1,2,2,2)，后两格各拒收一个，共拒收2，并有总请求4=最终队长2+拒收2。STATIC_EMPTY_TRUE_QUEUE_SENSOR_ALIAS在每条相同9bit原source上对外报告与平衡先服务world**逐四格完全一样**的Q轨迹，但oracle真实物理队列H1=H2=H3=H4=0。它需假定一个会模拟队列的伪报告器且没有可信物理核验，不能据此声称现实公共服务机构存在假排队，也不能证明用户真实受阻；只能说明队长报告与物理真值是不同的识别对象。

## CI失败更正、全部原来源和正式有界验收

[原生Fraction有限队列源与独立马尔可夫核程序](r256_exact_finite_queue.py) · [全部4608原九bit四格来源CSV](R256_ALL_4608_ORIGINAL_FOUR_SLOT_QUEUE_SOURCE_ATOMS.csv) · [九world全81队长路径/拒收服务结果JSON](R256_EXACT_RESULTS.json) · [原CSV与JSON SHA256机读收据](R256_FINAL_MACHINE_ACCEPTANCE.json)。

首轮[GitHub Actions run39896586661](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39896586661)Python3.12模型测试**failure**且3.11因matrix fail-fast取消，具体问题是结果JSON四队长元组字符串序列化误写`map(str(k))`，产生九项同源TypeError；直接队列生成、源守恒及独立Markov核本身没有被修改。只在结果组装中修成`map(str,k)`，冻结世界参数、原九bit来源及模型队列更新规则均不变，保留失败run和修复commit [e40d3b53](https://github.com/edwardsage419/Psychohistory-Research/commit/e40d3b53a05e19c28f29b495f2f98d69de0fd9f0)。

最终[GitHub Actions run39896631038](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39896631038)总体completed/success，全部三项job success；Python3.11及3.12实际日志各`Ran 82 tests`、`OK`，合计**164次真实双版本测试通过**。第三独立审计逐世界验证512个不同9bit来源、质量1/512、四时格容量与逐格守恒、全队长路径PMF归一、各期平均库存与服务拒收均值、首格服务先后概率1/2 vs1/4、U持久引起的0 vs1/4双格条件概率差、真实隐藏空队列/报告路径逐source同值，以及CSV/JSON SHA256。审计实际日志`R256_ALL_4608_ORIGINAL_FOUR_SLOT_QUEUE_SOURCE_PATHS_AND_MARKOV_PRODUCTS_VERIFIED`、`R256_ALL_4608_QUEUE_SOURCES_PERMANENTLY_ARCHIVED`。完整原CSV/结果JSON/机读SHA由GitHub bot永久归档main提交[559ea6cf](https://github.com/edwardsage419/Psychohistory-Research/commit/559ea6cf3ee4de82c2822526dee5d04941f0372a)。

原CSV SHA256 `8be5360465497321c15bffc554c7088fad48bcef71847e43e2ee2f714ed5119b`，完整结果JSON SHA256 `32c7811c073455f9af638d6090d259cec4abed307f693ba78413a11b0fe0d30a`。

正式科研资格`CLOSED_BOUNDED_E1_FINITE_CAPACITY_TWO_FOUR_SLOT_QUEUE_AND_MARKOV_PATHS`，未取得真人队长观测/服务效率因果识别/真实公共资源等待数据，也没有无限容量连续时间M/M/1稳态或Poisson服务复算。新增E2=0、E3=0，R073及PESEN v0.1冻结。下一原目录已核`11-017 Optimization Theory`（R257，P1），其后`11-018 Optimal Control`，依旧先完成全部原R，再分类和模型熔炼。
