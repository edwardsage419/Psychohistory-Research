# R067 E2 原作者投稿固定版本：真人长期囚徒困境行为记录审计

冻结时间：2026-10-16。**第一次读取这一固定提交的两份完整 CSV 之前冻结**。前项 Dryad DOI `10.5061/dryad.37pvmcvmk` 的 DOI、目录与 CC0 已经验证，但是 Dryad 公开文件直接下载实际 HTTP 403、API 401，故记 `DRYAD_BYTES_NOT_VERIFIED`，不伪造成功。

## 备用独立原作者 GitHub 固定来源

作者 `eladiomontero/PairwiseStrategies`，不可变 tag `submission` 指向完整 Git commit `4743f74d8a03a031b8f70aff64956f8ad5155182`。固定两个实际 Git blob：
- `fix.csv` Git blob `3bf78bf85f6642afee18d6f1965dca7272582f40`，988279 字节；
- `rand.csv` Git blob `f5a86cd033b739da45d3fc7c5019068f612146a2`，1112614 字节。

这些可能是 2021/2022 作者的**投稿时期输入或经过筛选的数据结构**，尚**未经证明与 Dryad 最终 v8 的 `fix.csv`、`rand.csv` 按字节或按行相同**；即使来自同一研究，也应保留版本不可等价风险。

已见固定 CSV 表头包括 `round,player,action_player,opponent,action_opponent,payoff,time_php,time_js,who_played,treatment,session,player_id,context,prev,prev_player,prev_opp,y,prev_p,prev_o,prev_p2,prev_o2` 等。必须完整读取、按 git blob 严格校验，从而确认**非缺失行动值究竟为 C/D 还是还有其它代码**，统计合法观测数、处理/轮次/场次的**匿名规模与范围**、玩家去重数、每人每轮的重复记录风险；不可把 DataFrame 行天然等同不同人的一次行动。

## 具体执行门

1. 只下载固定标签 SHA 对应的两个文本 CSV，Python 标准库 UTF-8 解码；每文件上限 2 MB。验证 Git blob SHA1、准确字节、完整表头和行宽一致性，空字段按显式 `{"","NA","NaN",".","--"}` 规则标记（仅结构门用）。
2. 逐 CSV 记录匿名字段名、行数、合法玩家行动 C/D 数、相应 C/D 百分比、非法行动标签数（不可回显任何异常原始行动值）、`round` 的最小/最大及去重数、`session` 不同标识数、`player`/ `opponent` 唯一标识数以及每玩家每轮是否可能重复。不得输出参与者、Session 原始标识、个人策略序列、研究原文评论或个体头像。
3. 研究不是新的实验招募，没有新的 2026 数据。即使完全 PASS，最高只能说 `ORIGINAL_AUTHOR_SUBMISSION_DATA_AUDIT_PASS`；`ORIGINAL_DRYAD_FINAL_DATA_BYTE_EQUIVALENCE=OPEN`。不能在此步骤拟合原作者 HMM 或 R067 固定支付矩阵的跨时策略模型。
4. 后续 E2 预测协议若可执行，应使用作者论文真实 payoffs `R=3,T=4,S=0,P=1` 而**非 R067 E1 `T=5`**，并按身份/处理/轮次考虑 repeated pairing 与行为自相关；在尚未确认是否每轮有一个有效玩家选择前不能开展任何经验排名。
5. 若任一文件 SHA/解码失败，记录 `SOURCE_FAIL_CLOSED`；若行结构合法却存在非 C/D/重复用户轮次，则记录问题数量和 `ACTION_UNIVERSE_NEEDS_MAPPING`，不自行删去而宣称干净。所有真实数据只在临时 runner 内存/文件里，GitHub 仅保存匿名聚合。

`R067_AUTHOR_SUBMISSION_AUDIT_PROTOCOL=FROZEN`
`R067_REAL_TWO_STRATEGY_FIT=NOT_YET_AUTHORIZED`
`PESEN_v0.1=FROZEN`
