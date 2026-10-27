# A轨：R073 原真人来源独立镜像核验与来源去重

日期：2026-10-27。状态：ORIGINAL_SOURCE_BYTES_VERIFIED_AND_NO_NEW_EXPERIMENT。原R073协议与评分冻结。

## 实际读取

通过GitHub公开仓库 `eladiomontero/PairwiseStrategies` 的 `submission` 固定提交 `4743f74d8a03a031b8f70aff64956f8ad5155182`，读取作者 `fix.csv` 与 `rand.csv` 原始文本并逐行检查。原Git blob：fix `3bf78bf85f6642afee18d6f1965dca7272582f40`（988279字节），rand `f5a86cd033b739da45d3fc7c5019068f612146a2`（1112614字节）。与仓库原R073冻结协议列出的两个Git blob完全一致，证明这是**同一批实验原来源**。没有复制、修改或重新分发任何参与者记录。

## 实际字段与行级结构核验

fix.csv 共9200行、24列，6个场次、92名匿名参与者；rand.csv 共9600行、25列，6个场次、96名匿名参与者。两处理共12场、188人、18800条真人二元行为。每人恰100轮，轮次从1到100连续，`action_player`只出现C或D。固定配对的合作选择5161条、背叛4039条；随机配对合作2738条、背叛6862条。两文件以场次、轮次和玩家ID建立行级唯一键，无重复。每一行的对手身份与行动，在同一场次同轮的对手行都能找到相互镜像且行动一致的记录，全部18800行检查通过。保留对手身份及每轮配对，适合历史行为时间变量复算。

字段包含`round`、`player`、`action_player`、`opponent`、`action_opponent`、`session`、`treatment`，以及预加工的历史字段。后者不能直接替代冻结R073按每个被试时间排序自行构造的lag特征，需防止衍生字段泄漏。

## 来源与复现资格

英文原论文 Montero-Porras et al. (2022), DOI 10.1038/s41598-022-11654-2；原作者GitHub `https://github.com/eladiomontero/PairwiseStrategies/tree/submission`；正式Dryad数据归档 DOI 10.5061/dryad.37pvmcvmk。Dryad公布fix.csv、rand.csv、README、实验说明，页面记录12场188人。其下载在本轮公开页面工具访问中返回403，终版Dryad文件与作者投稿版Git CSV字节是否相同仍未证实。Dryad通常以CC0提供数据，GitHub仓库未见单独LICENSE；本轮只进行公开来源只读分析，不推定两个版本的许可或字节自动相同。

本数据正是R073已使用的原真人实验，也已在 `research/data_scout/MONTERO_2022_R073_ORIGINAL_SOURCE_IDENTITY_HARD_EXCLUSION_2026-10-26.md` 明确排除。当前新增成果为对原数据的第二次逐行结构和配对一致性审计，不能作为R073第二个独立真人实验。R073模型和评分规则不变，没有重训、调参或新增E2预测分数。其他候选数据继续等待独立来源、场次身份、许可和冻结协议兼容性检查。

`SOURCE_ROW_MIRROR_PASS=18800/18800`；`SECOND_INDEPENDENT_R073_EXPERIMENT=NO`；`NEW_E2=0`；`NEW_E3=0`；`ADDED_COST=0`。
