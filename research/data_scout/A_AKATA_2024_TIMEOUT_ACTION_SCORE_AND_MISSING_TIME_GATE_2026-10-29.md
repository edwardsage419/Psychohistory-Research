# A轨：Akata 2024 真人与LLM实验超时行为、得分记录及测量可识别性

日期：2026-10-29 UTC。目标键：(A, eliaka/repeatedgames@224a605a21127cac69763f990e077f7b05abd422, original runtime, timeout action and score measurement)。这是对既有3900条公开真人CSV来源的源码语义追查；本轮未重新读取或复制参与者级CSV，新增真人预测为0。

## 本轮实际读取的英文原作者源码

* 实验 `human_experiment/experiment/js/script.js`，Git blob `4b7be85e8b3b964bfd0722d796f5ed6c2b8f0a19`：https://github.com/eliaka/repeatedgames/blob/main/human_experiment/experiment/js/script.js
* 原作者分析 `human_experiment/analysis/repeated_games.Rmd`，Git blob `ca9991b6d0917156672e1e2fea923548562d945e`：https://github.com/eliaka/repeatedgames/blob/main/human_experiment/analysis/repeated_games.Rmd
* 原作者CSV `human_experiment/analysis/repgames.csv`，既有审核固定Git blob `2dd67c6ff80f2d7aa07a70b470e26fe3592c6d95`：https://github.com/eliaka/repeatedgames/blob/main/human_experiment/analysis/repgames.csv
* 既有124条查表收益不一致审计：`research/data_scout/A_AKATA_2024_PD_LOOKUP_SOURCE_REPLAY_AND_VERSION_GATE_2026-10-29.md`。本轮不把该数字当作新的异常发现。

## 新增源代码级确认

1. 原JS第12至35行设置每游戏10轮，单独存储`xcollect`行动、`ycollect`回合收益、`timecollect`反应时间及`invalidPoints`。
2. 第319至335行明确：若倒计时已结束，按Enter将通过随机F/J选择调用`myfunc(0/1)`。第338至358行的主动F/J选择只有倒计时尚未结束时才生效。因此公开的行动字段可能同时包含主动选择与超时随机分配行动。
3. 第501至521行：`myfunc`将实际使用的行动追加到`playerChoices`，根据对手查表和收益矩阵计算`playerPoints`，随后将行动、计算收益和反应时间分别写入三个数组。第532至533行在超时路径额外累计`invalidPoints += playerPoints`，而第748至765行将`invalidPoints`与`actions`、`rewards`、`times`分别保存。超时导致的奖金无效由单独字段处理。
4. 第653至657行确认切换游戏区块时清空`playerChoices`，不能把BoS的历史行动作为PD查表前缀。第297至299行每轮重新随机选择Base或Prompted变体，不能默认每人整个PD区块使用单一变体。
5. 公开清洗CSV的七列为`id,game,action,score,opponent,guess,coordination`，没有`times`、`invalidPoints`或超时指示；原作者Rmd第30行直接读取该CSV。本轮没有取得从原始保存对象到清洗CSV的逐字段转换和原始时间戳。

## 对既有异常和未来复现的影响

既有第3061行`action=0,score=0`，按照当前仓库查表和该行重建历史，期望得分5。实验源码中的超时路径仍先按收益矩阵生成并保存`playerPoints`，仅在另一个字段中标记该收益不计入奖金。因此，单凭“超时没有奖金”不能直接解释清洗CSV中的0分；仍需原始采集对象、当时实际查表版本、清洗脚本及行顺序。既有124处查表不一致继续标为`DIAGNOSTIC_VERSION_OR_CHRONOLOGY_OPEN`，不可判定124个原实验记录错误。

清洗CSV中`action`可能包含随机分配的超时行动。没有`times`或有效性标志，不能把全部1950条PD行动无条件解释为受试者自主策略选择；任何条件概率、学习机制和预测评分必须先确认这一测量门槛。实验为真人对LLM、每人PD10轮，无法直接用于冻结的R073真人双人100轮评分。真人数据文件单独再分发许可仍为OPEN，本轮未复制私人或公开参与者行级数据。

结果：`RUNTIME_TIMEOUT_PATH_VERIFIED`；`RUNTIME_REWARD_VS_BONUS_SEPARATION_VERIFIED`；`CLEANED_CSV_TIMEOUT_IDENTIFIABILITY_OPEN`；`R073_DIRECT_REPLAY_NO`；`NEW_E2=0`；`NEW_E3=0`。没有购买、账户注册或收费操作。
