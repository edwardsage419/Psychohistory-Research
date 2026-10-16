# R070 竞争机制：曼哈顿距离限制与最近可行空位

冻结日期 2026-10-16，**在第一次取得真实 3×3 全量竞争模型结果之前**。本协议是一项原作者思想启发的、独立构造的确定性 E1 敏感性实验，不复制 Gambetta et al. (2023) 的随机 gravity 分布、不拟合任何真实居民迁居数据、不改动此前 R070 严格固定的行优先基线。

## 已有模型/文献锚

冻结的原模型 `research/R070/r070_schelling_spatial_migration.py` Git blob `b18d07d7fd489033c936dfe553149f2e3dbf6ff6`。冻结全量 756 初态枚举 `research/R070/r070_exhaustive_3x3.py` Git blob `de4da4671aada3c950fa6193163fbe306627b835`。原始作者文献：Schelling (1971) DOI `10.1080/0022250X.1971.9989794`; 竞争机制参考 Gambetta, Mauro & Pappalardo (2023) *Mobility constraints in segregation models*, DOI `10.1038/s41598-023-38519-6`, [作者 GitHub](https://github.com/dgambit/mobility_schelling) 固定提交 `08e51e8592db813b05e93d9a98f43dd5e62d9572`，`models/schellingmob.py` Git blob `2ab1dc0e75c4f7d1ea9b66d7f37c4a355457998f`。其原论文讨论按距离与地点吸引力概率选择空位；此处故意**只**研究步长可达性/确定性近邻优先，不可声称复制其完整实现/统计结论。

## 固定全集和四种政策

棋盘 3×3、抽象代理 A=2、B=2、空=5，精确 `C(9,2)C(7,2)=756` 初态 × `tau∈{0,.25,.5,.75,1}`，每种政策 **3780** 运行，共 **15120** 个初态—阈值—政策运行。每条至多 40 次移动，禁止随机数。

所有政策共享原函数 `validate`, `happy`, `fraction`, `metrics`，使用**同一个不满意者候选：当时行优先的第一个不满意代理**。移动者在暂时腾空原位后，按每政策允许的空位候选试探；空位必须具有至少一个占用邻居，且把代理移入后同类比例 ≥tau。空邻居为0不构成可满足的候选，原位置腾空后若本来不满意也不能靠原地移动骗取成功。若当前首个不满意者找不到合法空位，返回明确 `STALLED_NO_SATISFYING_VACANCY`，**绝不**尝试暗中让别的代理移动；另做一个匿名诊断，统计是否存在**其它不满意者**仍可找到合法迁入位置，因此区别“行优先执行锁定”和“全局全部移动都无解”。

候选位选择规则（曼哈顿距离 `|r2−r1|+|c2−c1|`，不环绕）：

- `GLOBAL_ROW_MAJOR`：**原程序的完全不变结果**，任何空位、按行优先选第一个满意目标。须在全部 3780 情况下调用**原函数 run**并对本次新实现的 unrestricted 逐轨迹完全一致校验；绝不能为使两者一致而更改原模型。
- `RADIUS_1`：仅候选曼哈顿距离 ≤1，仍行优先选第一个满意目标。
- `RADIUS_2`：仅候选曼哈顿距离 ≤2，仍行优先选第一个满意目标。
- `NEAREST_SATISFICING`：全范围所有合法满意目的地，优先曼哈顿距离最短，相同距离再按行列序。与 `RADIUS_1/2` 的**不可远迁**约束不同，最近优先从来不拒绝更远的唯一可达满意空位；不能将最近优先误写成硬限制。

每一步都不改变抽象类型人口（2/2）及空位数（5），迁居后新位置必须满意；模型不允许因为移动成本而去一个不满意位置。四类 `STABLE_ALL_SATISFIED`、`STALLED_NO_SATISFYING_VACANCY`、`MAX_STEP_BUDGET` 结束信号的语义按原模型处理，不可把“不可搬迁”=“总体满意”。

## 逐一配对指标与反证

各政策、各 tau 输出全局稳定数量/停滞数量/步数用尽数量、总移动数/平均移动数、最终不满意代理数量累计值、具有前后均有四邻接占用边的布局中宏观异类型接触比例的**配对均值**，并报告末态异类型四邻接边比例高于初态案例数（分母缺失则单列，不插值）。

对每一个初态 tau，计算每个竞争政策与 `GLOBAL_ROW_MAJOR` 的配对指标：`unrestricted stable but competitor stalled`、`unrestricted stalled but competitor stable`、`different terminal boards`、`competitor fewer moves`、`more moves`、`equal moves`、`competitor final unhappy higher/lower/equal`；每种“区别”可保存第一条**词典序**纯合成板面反例供独立回放。若对手在某一配置优于基线，不得隐匿或删除。

尤其要记录 `STALLED_FIRST_AGENT_WHILE_ANOTHER_CAN_MOVE` 的案例数，这可能暴露之前论文结论中原程序的**行优先执行政策**局限；不要将此结果归因于代理偏好或住房制度。对所有 3×3 布局 tau=0 所有 4 政策都必须立即稳定且0移动。

验收：至少 20 项合成正反例，包括 baseline source parity、候选曼哈顿距离、两个半径的不可远移、最近优先不等于不可远移、明确的因首名不满意者被锁住而停滞、4×756×5=15120 全量、类型/空位守恒、阈值0、max budget、无邻居、终点幸福性、概率不适用、宏观 null、不能输出或暗指真人个体，以及 CI 在全量数值上的实际 success。**任何**数学不变量失败必须 FAIL_CLOSED，不能从 15120 里删除难解配置。

证据最高 `R070_E1_DISTANCE_COMPETITION_PASS`，`R070_HUMAN_E2=BLOCKED_EVENT_LEVEL_SOURCE_AND_RULE_PARITY`，`R070_E3=OPEN`，`PESEN_v0.1=FROZEN`。
