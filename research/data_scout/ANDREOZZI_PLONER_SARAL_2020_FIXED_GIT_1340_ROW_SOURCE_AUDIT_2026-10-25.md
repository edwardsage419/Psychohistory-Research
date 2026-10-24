# A：Andreozzi、Ploner、Saral 2020 真人社会困境数据固定来源与逐行结构核验

日期：2026-10-25。证据状态：公开真人原始行为数据结构已实际读取；尚未开展模型评分，E2预测新增0，E3新增0。

## 一手来源、固定身份和许可
研究：Andreozzi, Ploner & Saral (2020), *The Stability of Conditional Cooperation: Beliefs Alone Cannot Explain the Decline of Cooperation in Social Dilemmas*, Scientific Reports 10, 13610, DOI 10.1038/s41598-020-70681-z。
作者公开仓库：`seyhunsaral/stabilitycondcoop`，固定 master HEAD `979abf87b5d3cfb7aa8be13b81ef233076c3bb75`。
直接读取 `data/csv/subjects.csv`，Git blob `bd4c1550002621bee7dfb50e0d15d317764d1ea9`，文件425,701字节；仓库同时公开六份按实验时间命名的 z-Tree `data/rawdata/*.xls`、清洗脚本 `code/process_raw_data.R`、问卷 `quest.csv` 和操作事件 `decbehav.csv`。
仓库 `LICENSE` Git blob `a7d26c9987564e97e270547d50707d7093ada753` 明确规定文档与数据 CC BY 4.0、软件 MIT。必须保留署名与许可信息。仅存档数据结构核验和指向源仓库的引用，避免无必要复制个人级行为记录。

## 实际CSV读取和结构检验
通过GitHub连接器直接取得完整 `subjects.csv` 字节，独立CSV状态机解析带双引号字段及逗号，核验1340行、67列、全部行列宽67。
* 六个 `session`，行数分别为 220、220、220、200、240、240。
* 十个 `period`，每个场次内均存在第1至第10轮。
* `session,subject` 共134个唯一参与者键，`session,period,subject` 共1340个唯一行动键，无重复。
* `session,period,group` 共670个配对回合键。每条记录可在同场次同回合找到 `opp` 指向的对手记录，且两条记录互指、组别一致、双方行动互为 `action` 和 `opp_action`；1340/1340条通过。
* 处理 `CondInfo` 660条，`NoCondInfo` 680条。
* 实际行动 `action` 为0（687条）、50（427条）、100（226条），`opp_action` 的频数相同。
* 关键身份/回合/行为字段 `session,period,subject,group,opp,action,opp_action,subject_unq,session_unq,opp_unq` 均无缺失。
* `opp_action_lag1` 在首轮134条为NA。其余1206条均与同一参与者上轮的 `opp_action` 精确相同，1206/1206通过，首轮没有非NA的未来信息。需继续核对其它派生特征是否使用当轮或未来变量。

## R073冻结协议适用性与泄漏风险
数据具有逐回合行动、身份、对手与独立场次，适合开展后续真人社会互动模型研究。但行为编码是三水平0/50/100，原实验具有条件合作和角色选择结构；R073既有双人二元动作模型与评分协议不能直接无改动套用。不得事后将0/50/100随意二分并声称冻结复现。 `opp_action` 属于同回合结果，在预测本回合前不可作为特征；只允许严格滞后的历史值。一个双人配对回合对应两条参与者记录，不能误计为两次独立配对。

## 复现准备结果
`SOURCE_ACCESS=PASS`; `LICENSE=CC_BY_4_0_CONFIRMED`; `SESSION_AND_OPPONENT_KEYS=PASS`; `LAG1_AUDIT=PASS`; `R073_UNMODIFIED_SCORE=BLOCKED_INCOMPATIBLE_THREE_ACTION_AND_ROLE_STRUCTURE`; `INDEPENDENT_EXPERIMENT_DEDUP=PROVISIONAL_NEEDS_R073_TO_R110_SOURCE_CROSSCHECK`; `NEW_HUMAN_E2_SCORE=0`。

下阶段如研究三行动群体互动，应先另行冻结任务、保留场次留出、训练集拟合与独立预测评分，核对 R 系列既有来源去重。不得改变 R073/PESEN v0.1。
