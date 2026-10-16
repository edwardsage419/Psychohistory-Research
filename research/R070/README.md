# R070：局部满意度、迁居行为与空间结构的微观—宏观机制

建立：2026-10-16。状态 **ACTIVE，E1 数学与有限代理模型通过，真实空间迁移数据 E2 OPEN、外部独立 E3 OPEN**。R070 接续 [R069 有界结题](../R069/R069_FINAL_ACCEPTANCE_AND_CLOSURE_2026-10-16.md)，研究另一族不同于“网络信息级联”的个体空间选择与群体模式形成机制。

## 原始文献与限定的研究范围

Schelling, Thomas C. (1971), *Dynamic Models of Segregation*, *Journal of Mathematical Sociology*, 1(2), 143–186，DOI [10.1080/0022250X.1971.9989794](https://doi.org/10.1080/0022250X.1971.9989794)。微观个体的局部满意度、空置位置与迁移顺序有可能形成非直观的总体空间结构，但**宏观分布不可以直接反推出个体心理动机**。本研究是具有清楚规则和反例的 4×4 Schelling-type 演示，不是 1971 年论文原版所有模拟或真实人口研究的完全复现。

[第一次运行前冻结的 R070 协议](../../protocols/R070_SCHELLING_SPATIAL_MICRO_MACRO_2026-10-16.md) · [纯标准库 Python 机制程序](r070_schelling_spatial_migration.py) · [22 项数学/边界/不变量测试](test_r070_schelling_spatial_migration.py) · [所有匿名合成数值与版面轨迹](R070_E1_SCHELLING_SPATIAL_RESULTS.json)。

## 已真实执行的 E1

[GitHub Actions run 38879457522](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38879457522) `completed/success`、**22 tests OK**。初始 4×4 棋盘只有 2 个 A、2 个 B 和 12 个空格，A/B 是**抽象无身份的数学代理**；Moore 8 邻域中同类占已占格邻居比例不足 `tau` 即不满意。每次只移动行优先第一个不满意 agent，迁往行优先第一个**有占用邻居**、移动后达到阈值的空格。

| 步骤 | 累计迁居次数（tau=0.5） | 不满意个体数 | 占用水平/竖直邻接边的异类型占比 |
|---|---:|---:|---:|
| 初始 | 0 | 4 | 0.5000 |
| 第 1 步 | 1 | 2 | 0.3333 |
| 第 2 步 | 2 | 1 | 0.3333 |
| 第 3 步 | 3 | 0 | **0** |

第一步核实原始 (0,0) A 的 Moore 同类比例 `1/3`，不满意，从 `(0,0)` 迁往第一个可行空位 `(2,0)`。第 3 步后所有 4 个代理局部满意，棋盘内横竖相邻的异类型占用连接数变为 0。同一棋盘 `tau=0` 对照全体一开始就满意、**0 次迁居**，板面不变。这说明同一初态依照**明示的局部移动规则**可以得到不同总体局部接触结构，但不等于一般网格规模必然分离或真实人群行为由这条机制决定。

## 后续 E2 实证识别门

真实空间变化研究至少需要可合法使用且能确认前后时间的**迁居记录、空置房、局部实际互动环境、经济/住房与制度约束**。一个时点的空间隔离程度不能确定迁居方向及真实人的容忍度，更不能在有历史结构性歧视、房价、收入/信贷、法律约束等未观测因素时直接从宏观分布归因于所谓“个人排外偏好”。在没有这样的来源及明确研究伦理/权限审查前：`R070_REAL_GROUP_PREFERENCE_CAUSAL_MECHANISM=NOT_ESTABLISHED`。

`R070_ACTIVE=YES`；`R070_E1_SYNTHETIC=PASS`；`R070_E2=OPEN`；`R070_E3=OPEN`；`PESEN_v0.1=FROZEN`。


## E1 穷举所有 3×3 板面及阈值反例（2026-10-16）

已先行冻结 [756 板面×5 阈值=3,780 次穷举协议](../../protocols/R070_E1_EXHAUSTIVE_SMALL_BOARD_ROBUSTNESS_2026-10-16.md)，然后实际通过 GitHub Actions [run 38881863192](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38881863192) 的完整批量运行（16 tests PASS）。后续专门加入“阈值 0.75 与 1.0 对两类各 2 人的小板面数学等价”测试，再经 [run 38882124414](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38882124414) **全部 17 tests SUCCESS**。完整可复现源程序 [r070_exhaustive_3x3.py](r070_exhaustive_3x3.py)，[研究全文、反例和边界](R070_E1_3780_CASES_ROBUSTNESS_AND_MODEL_SCOPE_REPORT.md)，[机读正式汇总](R070_E1_EXHAUSTIVE_3780_SUMMARY.json)。

在两类代理各 2 人/5 空位的**全体** 756 个布局中，阈值 0 和 0.25 有 756/756 个完全满意结束；阈值 0.5 有 **642 个满意 / 114 个不满意但无可行空位停滞**；阈值 0.75 和 1.0 都只有 **210 个满意 / 546 个停滞**。所有 3,780 案例均在 40 步内结束，无到达上限者。更重要，阈值 0.25 的 **24 个布局**末态水平/竖直邻接的异类型比例竟高于初始状态，明确推翻个体每次搬往满意位置就必然使宏观接触比例单调下降的过强命题。

此数学穷举是 **E1 固定模型内部反例**，非现实居住政策结论。另已完成[真人实验候选及来源适用性审计](R070_E2_HUMAN_GAME_SOURCE_ELIGIBILITY_AUDIT.md)：Tsvetkova et al. 2016 有**399 位 16–19 岁真实参与者**与 6×6 四类实时迁移游戏，但逐行动原始数据和使用许可尚未实际恢复，实验决策规则也不同于当前 row-major toy model；因伦理/数据身份、行为合约均未成立，**真实 E2=BLOCKED_EVENT_LEVEL_SOURCE_AND_RULE_PARITY**。Gambetta et al. 2023 的原作者 GitHub 模型虽可获取，其数据是模拟而非真人。不得改写为“真人机制验证成功”。R070 保持 **ACTIVE**，待额外竞争迁移机制或合法真实迁移事件数据；PESEN v0.1 保持 **FROZEN**。
