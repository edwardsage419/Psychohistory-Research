# R070 E2 真实空间迁居行为候选：论文可核验但逐动作原件尚不可复现

日期：2026-10-16。科学地位：**E2_HUMAN_EVENT_LEVEL_DATA_NOT_RECOVERED**；这是一份独立数据适用性审查，不是人类迁移行为的数值拟合。主要保护两类错误：把作者发表的实验结论当作本项目重复计算；把其他研究的代理模拟当作真人数据。

## 1. 真正的人类空间决策候选

Tsvetkova, M., Nilsson, O., Öhman, C., Sumpter, L., & Sumpter, D. (2016), *An experimental study of segregation mechanisms*, EPJ Data Science, 5:4，DOI [10.1140/epjds/s13688-016-0065-5](https://doi.org/10.1140/epjds/s13688-016-0065-5)，[官方完整开放论文](https://link.springer.com/article/10.1140/epjds/s13688-016-0065-5)。

依据论文 Methods 可直接核实的事实：

- **399 名**来自瑞典 **20 个高中班级**，年龄 **16–19 岁**。研究中可能包括未成年人，必须谨慎对待含个体决策/标识的任何原始记录；
- 实验是 **6×6** 棋盘，真实参与者在可见公开大屏上通过平板实时移动，限向上/下/左/右移动到**下一可用空格**，且被试可交流；
- 条件为 Same、Diverse、Same and Diverse、Same or Different 四种效用/游戏条件，各班按随机顺序进行；
- 论文称相似奖励组通常形成空间分隔，而促进差异或多样性的条件与结果不同；被试并不始终选择可用替代位置中分值最优者。这是**作者论文中的原报告**，不代表本项目独立重算出的真实动作。
- **目前研究中没有取得任何来源校验通过的逐人移动日志、离散时点的完整 6×6 位置表、全局空位表或明确再利用许可文件**。开放论文与辅助 PDF 不足以确认它们提供事件级原始数据。因此不把作者 399 人和本项目 R070 E2 PASS 画等号。

## 2. 为什么不能直接拿本文来验证 R070 4×4/3×3

本项目 [R070 冻结模型](r070_schelling_spatial_migration.py)是代理依序**选择当前最先不满意者**，随后行优先选择**任意位置**中第一个有占用邻居且能满足静态 tau 的空格。论文实验里的真实参与者**实时自主**移动，在 6×6 面板上位置约束、效用、可能沟通、被试决策顺序均不同；其模拟对照还使用“四向最近空位＋局部最佳动作”规则。两者不是相同的选择集合，不能直接拟合一个统一的 tau 再声称复现论文。

在今后能合法取得去标识的实验事件级数据前，要另外冻结：时间单位、参与者可见合法候选位置集合、实际收益函数（四种规则分别建模）、每轮完整同伴局部状态、可行动但不移动事件、初次和重复迁移、分组/班级留出（独立单位为班级而非每秒动作），并且要求实验数据使用许可和研究伦理边界。只有全部到位才进入 E2；没有数据时记录 `BLOCKED_EVENT_LEVEL_SOURCE_AND_RULE_PARITY`，不购买数据库/私下索取未授权未成年人的敏感记录。

## 3. 可复核但仅限模拟结果的独立竞争来源

Gambetta, D., Mauro, G., & Pappalardo, L. (2023), *Mobility constraints in segregation models*, Scientific Reports 13:12087，DOI [10.1038/s41598-023-38519-6](https://doi.org/10.1038/s41598-023-38519-6)。

公开代码 [dgambit/mobility_schelling](https://github.com/dgambit/mobility_schelling) Git commit `08e51e8592db813b05e93d9a98f43dd5e62d9572`；源 `models/schellingmob.py` Git blob `2ab1dc0e75c4f7d1ea9b66d7f37c4a355457998f`。仓库 README 直接声明数据是作者**自己模拟生成**，同时按代码区分距离、gravity 与空间相关性/位置吸引力的移动规则；论文明确指出**没有人类参与者**。这一来源有价值之处是提醒 R070 基准模型省略迁移成本、空间可达性与位置吸引力，不可以把源仓库中大量 CSV 当成真实居民移动。

研究现阶段不宣称复现 Gambetta 等人的完整 MESA 环境、实验结果或相同模型；把它作为**外部计算竞争模型设计**的证据，而非 E2 人类实证。

## 4. 决策和版本状态

- `R070_HUMAN_LAB_PUBLISHED_PAPER_SOURCE=VERIFIED_DESCRIPTION`；
- `R070_HUMAN_LAB_EVENT_LOG_BYTE_SOURCE=NOT_RECOVERED`；
- `R070_HUMAN_LAB_EXACT_RULE_PARITY=NOT_ESTABLISHED`；
- `R070_E2_HUMAN_MODEL_VALIDATION=BLOCKED_EVENT_LEVEL_SOURCE_AND_RULE_PARITY`；
- `R070_2023_EXTERNAL_MOBILITY_SIMULATION=SIMULATION_NOT_HUMANS`；
- `R070_E1_EXHAUSTIVE_3780=SEPARATE_MATHEMATICAL_EVIDENCE`；
- `R070_E3_EXTERNAL=OPEN`；`PESEN_v0.1=FROZEN`。
