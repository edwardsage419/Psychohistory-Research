# A 数据侦察：Andreozzi 等 2020 行为数据的预测时点泄漏与对手滞后语义复核

日期：2026-10-25。状态：COMPLETE（字段级新增核验），R073外部复现评分 BLOCKED。

## 固定来源与范围

Andreozzi, Ploner, Saral (2020), *The Stability of Conditional Cooperation: Beliefs Alone Cannot Explain the Decline of Cooperation in Social Dilemmas*, *Scientific Reports* 10:13610, DOI 10.1038/s41598-020-70681-z。

作者英文公开仓库 `seyhunsaral/stabilitycondcoop`，固定提交 `979abf87b5d3cfb7aa8be13b81ef233076c3bb75`。本轮重新通过 GitHub 连接器直接读取 `data/csv/subjects.csv` 完整425701字节，Git blob `bd4c1550002621bee7dfb50e0d15d317764d1ea9`，1340条记录、67列。原作者仓库许可为数据 CC BY 4.0，软件 MIT；引用与署名保留。先前结构审计见 `research/data_scout/ANDREOZZI_PLONER_SARAL_2020_FIXED_GIT_1340_ROW_SOURCE_AUDIT_2026-10-25.md`。

## 本轮新增可复算的确定性关系

对1340条逐行执行整数相等检查：

1. `earning_kept = 100 - action`，1340/1340成立。以 `earning_kept` 预测同一轮 `action` 等于直接读取目标值。
2. `earning_received = 3 * opp_action`，1340/1340成立。以 `earning_received` 预测同轮对手行为等于直接读取目标值。
3. `earning_game = earning_kept + earning_received`，1340/1340成立，属于本轮收益结果。

这些是后验结果字段。若目标为回合开始前的行动预测，必须将 `earning_kept`、`earning_received`、`earning_game`、`opp_action` 排除出同轮预测特征。其它 `earning_*`、`exp_pay_*`、`cond_class_*`、`isCC/isS/isHS` 等字段的观测时点需按实验指令和清洗脚本另行确认，不能先验认定可用。

## 对手滞后变量的实际语义

按 `session,period,subject` 唯一键将每个参与者第2至10轮与自己前一轮记录连接，实际可比1206条：

| 检查 | 一致条数 |
| --- | ---: |
| `opp_action_lag1` = 同一参与者上一轮的 `opp_action` | 1206/1206 |
| `opp_cond_type_lag1` = 同一参与者上一轮的 `opp_cond_type` | 1206/1206 |
| `opp_cond_class_wide_lag1` = 同一参与者上一轮的 `opp_cond_class_wide` | 1206/1206 |
| `first_player_lag1` = 同一参与者上一轮的 `first_player` | 1206/1206 |
| 当前对手与上一轮对手为同一人 | 56/1206 |
| `opp_cond_class_wide_lag1` = 当前对手上一轮的 `cond_class_wide` | 391/1206 |

因此 `opp_*_lag1` 的对象是“该参与者上一轮遇到的对手”，不能未经身份连接就当作“本轮当前对手的上一轮历史”。当前对手通常发生变化。56条同对手重复仅是当前与上一轮对手相同的计数，不等于全局唯一配对或独立场次数。

六个session各自只有一种处理：session1、4、5为CondInfo；session2、3、6为NoCondInfo。若进行条件差异评估，处理与session完全嵌套，必须在session层面处理聚类及留出，避免将1340行误当1340个独立处理单位。

## 复现准备与证据边界

`SOURCE_ACCESS=PASS`；`IDENTITY_AND_LAG_SEMANTICS=PASS`；`SAME_ROUND_TARGET_PROXY_LEAKAGE=CONFIRMED`；`SESSION_TREATMENT_CONFOUNDING=DESIGN_NESTING_CONFIRMED`；`R073_UNMODIFIED_BINARY_SCORE=BLOCKED_THREE_ACTIONS`；`INDEPENDENT_EXPERIMENT_DEDUP=PROVISIONAL`；`NEW_E2=0`；`NEW_E3=0`。

R073与PESEN v0.1冻结。下一步检查研究档案来源去重、原实验任务时间顺序和其他派生变量生成过程，之后如另行研究三水平行动，应事前冻结新协议。不得把本次字段审计写成真人预测提升。
