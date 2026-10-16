# R070 正式有界结题：局部迁移偏好、空间格局与执行规则的分离

日期 2026-10-16。按照[研究统一六门验收标准](../../protocols/RESEARCH_ACCEPTANCE_STANDARD_V1_2026-10-16.md)，本研究对**纯抽象 Schelling 类代理机制 E1、两类迁移约束竞争及真人实验来源/规则可识别性审计**形成限定完整可重放研究包，正式状态 `CLOSED_BOUNDED`。**这不是对人类现实居住隔离、歧视心理、历史住房政策的实证机制验证成功；R070 E2 仍 BLOCKED，E3 OPEN。**

## 1. 主科学问题与版本边界

主问题：个体对占用 Moore 8 邻域中同类比例的满意度、空位可达性、候选目的地排序与被激活的执行顺序，能否单独改变宏观异类型空间接触结构和“全员满意”终局？原始思想来自 Thomas Schelling 1971, *Dynamic Models of Segregation*, DOI `10.1080/0022250X.1971.9989794`。本项目自定义有限确定性过程，并非原作者所有模型完整复算；抽象 A/B 不代表现实种族、阶级或其它人口身份。

一开始 R070 [固定 4×4 基线协议](../../protocols/R070_SCHELLING_SPATIAL_MICRO_MACRO_2026-10-16.md)。随后每个新科学问题**在看见相应结果前分别冻结**：[全 3×3 3780 个初态—阈值](../../protocols/R070_E1_EXHAUSTIVE_SMALL_BOARD_ROBUSTNESS_2026-10-16.md)，[四迁居距离目的地规则 15120 条](../../protocols/R070_E1_MOVEMENT_DISTANCE_COMPETITOR_2026-10-16.md)，[两种代理执行/激活规则 30240 条](../../protocols/R070_E1_FEASIBLE_ACTOR_ACTIVATION_2026-10-16.md)。这些累积的范围**不是 R070 一开始就预注册的全套题目**，正式结题的限定范围为事后汇总决议，必须标 `RETROSPECTIVE_SCOPE_DECISION`，但每一后续子实验有自己的真实事前冻结记录。

## 2. 真正运行的 E1 证据：基线、反例与竞争机制

1. **4×4 初始数学机制**。[CI 38879457522](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38879457522) 22 tests PASS；tau=.5、2A+2B+12空格的一个固定棋盘，3 次确定性满意空位迁移后全体满意、四邻接占用格异类型边比例从 .5 到 0；tau=0 不迁居。[来源代码与报告](README.md)。
2. **3×3 完整数学状态穷举**。[CI 38882124414](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38882124414) 17 tests PASS；严格 C(9,2)×C(7,2)=756 种初态，五个满意阈值共 **3780** 条，最长40步。tau=.5 旧算法下 642 个全员满意、114 个旧规则停滞，tau=.75 或 1 下 210 个满意、546 个停滞；tau=.25 中至少24个初态末态异类型接触比例反而升高，反证“个体向满意位置移动必单调降低宏观异类型接触”的绝对命题。[穷举报告与勘误](R070_E1_3780_CASES_ROBUSTNESS_AND_MODEL_SCOPE_REPORT.md)、[机读全状态摘要](R070_E1_EXHAUSTIVE_3780_SUMMARY.json)。
3. **四种目的地与距离政策对照**。[CI 38884013460](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38884013460) 27 tests PASS；756×5×4=**15120** 条配对，逐一核对原始不限距离 row-major 轨迹完全一致。tau=.5时旧行优先不限距离642个成功、曼哈顿半径1仅294个、半径2有528个、无限距离最近优先有646个。该实验发现以前的“第一名不满意者搬不了”**并不等于系统全体不满意者都搬不了**：tau=.5 原 114 个停滞**全部**还有后续其他可动者；tau=.75 的546个停滞中428个如此。[正式竞争机制和先前解释勘误](R070_E1_DISTANCE_POLICY_COMPETITION_AND_ORDERING_ERRATUM.md)。
4. **两种激活/执行规则的完整新对照**。[CI 38889203300](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38889203300)，**23 tests PASS，30240条完整 E1 合成轨迹成功**。唯一改变是：旧规则遇第一位不满意者不能搬就停，新规则跳过其并选下一个**有合法满意空位**者。对 tau=.5 不限距离，成功从642→**756/756**，tau=.75 不限距离210→**570/756**，余186是真正当前状态所有不满意者均无满意目的地；半径1 tau=.5仅294→362，表明空间可达限制没有因切换激活顺序消失。旧停滞的新可移动反例、规则完整定义与失败证据见[报告](R070_E1_ACTIVATION_30240_COMPLETE_AUDIT.md)、[20 组摘要与最初反例 JSON](R070_E1_FEASIBLE_ACTOR_ACTIVATION_RESULTS.json)及 [完整固定字节所有结果 JSON](R070_E1_FEASIBLE_ACTOR_ACTIVATION_COMPLETE_30240.json)。

**精确成果归档与审计：** 完整激活结果 108904 bytes、SHA256 `213be6839db3067854d811a755ec9f3047d5f42def4e3df55f1fd56b835d1dcd`，通过 GitHub Actions [归档 CI run 38889607481](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38889607481) 重新生成与固定哈希比对成功，并自动提交到 **GitHub `main`**，不是只保留有到期限制的临时 artifact。自制源与测试脚本一并在 `research/R070/` 保留；既有 R070 生产源未被更改，合成反例测试显式拒绝虚假的全局稳定性/不满意迁移。

## 3. E2 的原始来源审计和不能完成的科学验证

[真人实验来源适用性审计](R070_E2_HUMAN_GAME_SOURCE_ELIGIBILITY_AUDIT.md)阅读 Tsvetkova et al. (2016), *An experimental study of segregation mechanisms*, DOI `10.1140/epjds/s13688-016-0065-5`，作者发表 399 位16–19 岁高中生、20班、四类6×6实时空间博弈。**本项目没有取得**合规可用于重算的逐人逐次移动日志、每次真实有效空位/可移动位置与激励函数、固定原始字节/再使用许可，因此不能把该论文作者的实证发现冒称本项目独立复现。且受试者可能未成年，应只使用受伦理边界保护的合法数据。另一来源 Gambetta et al. (2023) DOI `10.1038/s41598-023-38519-6` 的原作者代码和论文有迁移约束研究，但**明确无真人参与**，仅为竞争机制启发而非 E2 真人证据。

R070 当前证据全部为**E1 合成微观—宏观模型**和真实文献/源码来源可追溯的审计，不包含对房价、信贷、制度歧视、住房政策或真实迁居因果的识别。更大棋盘、更多代理、随机激活、真实规则可复现及外部独立 E3 参见[后续开放门](R070_POST_CLOSURE_OPEN_GATES.md)。不能将单个小棋盘的配对全量计数表述为对所有网络结构/现实群体的证明。

## 4. 统一六门限定交付验收

| 验收门 | 结果 | 限定对象及不能升格部分 |
|---|---|---|
| A01 问题与范围 | PASS | E1 三阶段有明确冻结配置、微观规则、实验范围；R070 首日起未一次预注册整个累积范围，限定结题属回顾性整合 |
| A02 来源与测量 | PASS | 原 Schelling 1971、Tsvetkova 2016 论文、Gambetta 2023 模拟仓库记录和相应 DOI/固定 Git blob；真人逐动作数据未取得，明确 `BLOCKED` |
| A03 实际计算与复现 | PASS | 原代码/额外三阶段程序、GitHub Actions 22/17/27/23 tests 真正通过，4×4、3780、15120、30240 全量输出及永久 GitHub 归档 |
| A04 失败与反例 | PASS | tau 高时旧执行顺序大量停滞，新规则仍存在完整不可动局面；宏观接触非单调；旧模型“全局不可迁居”的解释已出正式勘误 |
| A05 推断边界 | PASS | E1 数学不等于 E2 人类因果；不同宏观指标不同，停滞语义只适用于当前规则/局面；外部 E3 仍 OPEN |
| A06 结题与可移交存档 | PASS | 本文、源文件、合成测试、全量 JSON、后续阻塞清单、GitHub `main` 路径均公开且核验 |

六项 PASS 只表示**已声明有限证据包的来源、规则、真实已跑计算与留存负证据完备**。科学上 `REAL_HUMAN_MOBILITY_MECHANISM=NOT_ESTABLISHED`、`E3=OPEN` 不因为结题改变。

## 5. 最终状态与未来研究主线

`R070=CLOSED_BOUNDED`；
`R070_E1_THREE_MATH_PHASES=PASS`；
`R070_INITIAL_4x4=PASS`；
`R070_EXHAUSTIVE_3780=PASS`；
`R070_DISTANCE_15120=PASS`；
`R070_ACTIVATION_30240=PASS`；
`R070_REAL_PERSON_LEVEL_E2=BLOCKED_EVENT_LEVEL_SOURCE_AND_RULE_PARITY`；
`R070_E3=OPEN`；
`R070_HISTORICAL_INSTITUTIONAL_CAUSAL_PREDICTION=NOT_ESTABLISHED`；
`PESEN_v0.1=FROZEN`。

依标准将范围已完整的 E1 限定研究归档，不以 E2 缺源为由在一个编号下无限追加同型玩具实验。**R071 可转为群体规范形成、制度执行与惩罚合作等不同模型家族**；需要独立协议与新的真实可检验问题，不能把 R070 E1 转为主项目 PESEN 正式更新。
