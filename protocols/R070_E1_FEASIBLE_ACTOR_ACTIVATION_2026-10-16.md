# R070 E1：先选不满意者 vs. 先选可迁移不满意者——完整激活机制对照

2026-10-16；**本协议先于任何本轮 30,240 个实验结果产生而冻结**。本轮只改变**代理执行激活顺序**，不改变之前任何版本的局部满意度或四种迁居目的地/距离规则。所有研究对象为不涉及现实身份信息的 A/B 数学代理，不能称真人/社会地位实验。

## 不可改动的历史基线

[R070 先前 15,120 配对结果](../research/R070/R070_E1_DISTANCE_COMPETITION_RESULTS.json)于 [GitHub Actions run 38884013460](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38884013460) 跑通 27 项测试。固定源函数 `research/R070/r070_distance_competitors.py` Git blob `e44101fa9bf638eadebe13aec1930d72a524af8c`；原始 `research/R070/r070_schelling_spatial_migration.py` Git blob `b18d07d7fd489033c936dfe553149f2e3dbf6ff6`；棋盘全集 `research/R070/r070_exhaustive_3x3.py` Git blob `de4da4671aada3c950fa6193163fbe306627b835`。不允许改写这些文件及其先前的来源结果或失败记录。

统一配置：3×3、A=2、B=2、空=5，完整 `C(9,2)C(7,2)=756` 初态；`tau={0, .25, .5, .75, 1}`。距离政策 `GLOBAL_ROW_MAJOR`、`RADIUS_1`、`RADIUS_2`、`NEAREST_SATISFICING` 沿用上述代码，按曼哈顿距离计算（后者**无**强制半径）。时间不产生随机顺序，迭代最多 **40** 次。严格 `2 激活机制 ×4 距离政策 ×5 阈值 ×756 初态=30,240` 机制轨迹。每个阈值与距离政策下，旧激活策略的 **756 条逐步轨迹和停止信号必须与原函数 `run_policy` 完全一致**，否则 FAIL_CLOSED。

## 唯一新增微观机制

- `FIRST_UNHAPPY`（严格历史规则）：行优先选择第一个当前不满意者，如果此人没有符合本距离政策与满意阈值的空位，则**立即终止** `STALLED_FIRST_SELECTED_UNHAPPY` 的科学解释。程序兼容实际旧状态名称 `STALLED_NO_SATISFYING_VACANCY`，绝不回写之前的输出。
- `FIRST_FEASIBLE_UNHAPPY`（本轮新规则）：沿同一行优先不满意列表逐个考察候选空位，遇到**第一个至少有一个合法目的地的人**才移动；对同一人仍按旧 `candidate_destinations` 决定落点，且仍必须有占用邻居、移动后同类比例 ≥tau。若全部不满意者都没有合法迁居目的地才标 `STALLED_ALL_UNHAPPY_IMMOBILE`；全部满意才 `STABLE_ALL_SATISFIED`；预算耗尽而仍不满意则 `MAX_STEP_BUDGET`。严禁把“当前搬不了”改成“允许搬向不满意位置”，也不允许孤立迁入/交换。
- 记录每次实际迁移时**跳过几名之前的不满意且不可移动者**，只输出累计跳过事件数、至少一次跳过的初态数量、首次字典序证据示例（纯抽象棋盘与聚合迁移计数）。两个激活机制的区别仅是候选移动者先选谁，不能混入随机效用、距离收费或跨地点优先。

## 完全配对验收与反例

每个 tau×距离政策×756 产生旧与新各 756 轨迹；报告每政策稳定/旧式首代理停滞/新式所有代理均不能移动/预算耗尽数量，成功案例之差、`old STALLED → new STABLE`，反向 `old STABLE → new STALLED`、`old STABLE → new MAX_BUDGET`、旧停滞而新预算耗尽、终局不满意人数增加/减少/相同、终局版面相同/不同、迁移步数增/减/相同、宏观相邻异类型比例可配对的上升/下降/相同或 null、是否出现 repeated visited board 等。若两种规则同样满意也不表示轨迹相同；保留不同局面的计数。还需给出首个源配置字典序例子，**包括新规则更差的情形，若存在**。

因为 `FIRST_FEASIBLE_UNHAPPY` 比旧规则“跳过堵塞者”，这不保证新规则**全局必定更好**：改变迁移次序可改变后续可行空位与满意度。要求在对照结果中允许并诚实记录新规则导致更多不满意者、更多预算耗尽、宏观异类型邻接比例上升、或新规则失败旧规则成功。禁止从某单个阈值的纯合成“成功数更多”推导一般人类政策效果。

## fail-closed 工程与可复核性

- 运行新策略要检查每一步**只有1名 A/B 换到原本空位**，4 个 A/B 计数、5 个空格不变；所有迁入目标属于来自冻结函数的同一候选列表，落点与候选优先相同；终止状态必须与全体此时不满意/可搬迁条件一致。历史基线每条完整轨迹必须精确复核 `run_policy`。
- 对 `tau=0` 的全部 4×756×2=6,048 组合必须 `STABLE_ALL_SATISFIED` 且零迁移；还必须完整运行其它所有阈值，不得筛选初态。
- 40 步后未达终止判 `MAX_STEP_BUDGET`；如果观察到重复版面或周期，只单列 `cycles_or_revisited_states`，本实验不声称本算法必然收敛。
- 纯合成高于 **20 项**的测试，检查真实阻塞反例、在合法其他代理存在时应跳过、不允许同一源/终点、RADIUS_1/2 限制、最近优先的单独逻辑、无可移动时标签、tau 0 恒等、人口与空位守恒、预算、null 宏观比例、基准完整轨迹一致、完整 30,240 个实验及绝不输出真实身份。
- GitHub Actions 真正执行测试及全量实验，报告源 commit、运行 id/状态、匿名工件 ID，存正式 JSON 结果和中文报告，并每次提交同步 GitHub。

研究等级上限 `R070_E1_AGENT_ACTIVATION_COMPETITION_PASS`；真人逐动作 E2 继续 `BLOCKED_EVENT_LEVEL_SOURCE_AND_RULE_PARITY`，独立 E3 `OPEN`，`PESEN_v0.1=FROZEN`。文献动机 Schelling 1971 DOI 10.1080/0022250X.1971.9989794，但本确定性执行政策是本项目自行定义的 toy 实现，不宣称原作者真实模型。
