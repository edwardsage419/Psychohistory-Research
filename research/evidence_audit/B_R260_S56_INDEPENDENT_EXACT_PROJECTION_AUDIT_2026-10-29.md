# B轨审计：R260 S56 完整赢家集合的独立有限预算复算

日期2026-10-29 UTC。审计键：`(B,R260,original e04a1601 + S56 f1faa901,54-group exact transfer)`。已阅读原R260九个冻结成本矩阵、原报告、S56冻结协议以及R轨新收据，属于**非盲态内部不同语言算法复核**。

## 预设检查与实际执行
R路线在隔离V8执行环境读取GitHub原始540行CSV，验证完整源覆盖并计算54个训练预算赢家集合、135个行动预算行；实际保存收据 `research/validation/R260_S56_BUDGET_UNDERCOVERAGE_EXACT_RESULTS_2026-10-29.json`。B路线在Python 3标准库中从九个冻结成本矩阵直接枚举可行集合，使用`Fraction`检查公平四情景平均，逐世界构造情景最小成本、完整U2最坏成本及遗憾，独立计算54组赢家及五个评价字段。B没有调用R源码、CSV解析器或R函数。

实际执行命令：
`python /mnt/data/b_r260_s56_independent_budget_oracle_20261029.py --r-projection /mnt/data/r260_s56_r_projection.txt`
输出：
`PASS: all 54 R groups, every winner and 5 member metrics exact`
`PASS: mutated projection rejected`
`INDEPENDENT_B_ORACLE_54_GROUPS_PASS`

其中R投影来自GitHub已归档JSON的全部54组，按照`world|training_budget|objective|training_optimum|winners|action:worst_U2:regret_U2:excess_worst_U2:excess_regret_U2:fair_mean_num_over4`生成。R投影Git blob `fb8bdd14bdcb8c0bf2432b7c83d256880ed06a8b`与本地实际比较文件一致；B脚本远端Git blob `4ba4bd67babf31a52778ba6feb7f429d1b0e87d0`与本地实际执行源码一致。完整54行按顺序和字段**精确字符串比较**，全部一致。

负例：把第13行投影追加`|999`后执行同一Python CLI，退出非零并报告`FAIL: mismatch indices=[12], lengths=54/54`。R源路线五个原始CSV变异（删行、重复、成本、准入位、质量）均被拒绝。第一次B负例脚本用替换`:1:`为`:999:`，由于第1行没有匹配片段导致测试自身断言失败，随后改为确定性追加错误字段，重新通过。首次归档B源码还出现`ADDITIVE_COMMON_SHOCK`成本矩阵一个6被误抄为5，远端源码hash与实际执行的正确本地版本不符；经读取远端现有blob并使用带SHA条件的更新修复，最终两者Git blob一致。上述首次失败保留在GitHub提交历史。

## 六项科学审计范围
1. 数据泄漏：S56的U2评估使用同一人工成本矩阵的完整已知反事实表，是**确定性压力测试**；没有数据驱动拟合，不能解释为真实样本外泛化或盲态留出。
2. 基线：Γ2下同目标最优超额必为0，全部18个控制组通过。成本目标与遗憾目标分别设置不同oracle。
3. 预测与概率校准：本任务是成本决策，不产生概率预测。公平1/4仅为人工敏感性假设；概率校准、Brier、对数损失均不适用。
4. 独立性：54个赢家集合共享九个冻结成本矩阵，不是54个独立统计样本。没有外部团队复现。
5. 重采样与不确定性：全枚举无蒙特卡洛误差；没有真实总体、抽样方差或置信区间。Γ集合覆盖的假设风险仍OPEN。
6. 负例及范围：五项R源变异、两项B投影篡改控制通过。HIDDEN_JOINT_TAIL/ALIAS和TIED_WORST_CASE保留预算误设反例。新E2=0、新历史E3=0。

## 验收边界
`INTERNAL_NONBLIND_EXACT_54_GROUP_PASS`；`FULL_135_ACTION_ROW_B_ORACLE=OPEN`；`NODE_CLI_REPLAY=NOT_RUN`；`EXTERNAL_TEAM_REPLICATION=0`。S56补充研究不修改原R260有界E1正式状态，不采纳任何新真人模型。原R257 S53的盲态失败与Codex PR #1/#3仍保持独立记录，不能由本次复算解除。

归档：[B独立源码](b_r260_s56_independent_budget_oracle_20261029.py)、[固定R收据投影](R260_S56_R_EXACT_54_GROUP_PROJECTION_2026-10-29.txt)、[R计算收据](../validation/R260_S56_BUDGET_UNDERCOVERAGE_EXACT_RESULTS_2026-10-29.json)。无需收费API或GitHub Actions，本轮没有触发CI。
