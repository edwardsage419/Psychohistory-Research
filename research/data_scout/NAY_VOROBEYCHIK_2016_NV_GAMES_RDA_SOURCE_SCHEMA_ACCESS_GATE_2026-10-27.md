# A轨：Nay与Vorobeychik真人重复囚徒困境汇总数据来源与资格登记

日期：2026-10-27。状态：PUBLIC_BYTES_CONFIRMED_SCHEMA_DOCUMENTED_RDA_DECODE_AND_INDEPENDENCE_PENDING。未进行真人预测评分。

## 实际核验的来源

公开英文来源：Nay, J. J. 与 Vorobeychik, Y. (2016), Predicting Human Cooperation, PLOS ONE 11(5), e0155656，DOI https://doi.org/10.1371/journal.pone.0155656。数据再封装位于公开GitHub `JohnNay/datafsm` 的 `data/NV_games.rda`，Git blob `36a961908385a7fe33ba688479b5dfc7b0a6b609`。GitHub连接器实际读取了该文件base64编码内容，编码长度1032332字符，对应774249字节，文件头为XZ压缩格式。已核验文件字节可由公开仓库读取；本轮没有完成RDA解码，也没有逐行复算168386条记录。

数据字典 `man/NV_games.Rd` Git blob `be625b217505dd05781f5bd9c12925df673a7ac0`，与 `R/data.R` Git blob `2a1dc849c34036026f45d1238d586376b876ec5f` 一致声明168386行、51变量、30种重复囚徒困境变体。列包括 `period`、`my.decision`、`my.decision1..9`、`other.decision1..9`、双方前9轮收益、`risk`、`delta`、`r1`、`r2`、`error`、`data`、`group`、`contin` 与 `infin`。文档的 `data` 来源代码包括AM、BR、DB、DF、DO、FO、FR、KS，涵盖八组既有实验来源。必须按来源逐项去重，FO、FR等可能与本项目其他R研究共享实验；它们绝不可按30个处理变体直接声称30个独立实验。

## 资格门

时间单位：`period`为游戏内轮次，`contin`指示连续时间条件；实际时间精度尚未核实。行为：文档记录自身当期二元决策及对手历史决策；未在51字段说明中发现明确独立的参与者ID、实验场次ID或对手身份列，无法仅凭文档确认身份级与场次级留出。历史字段最多9期，需解码后重新按真实游戏边界检查，不可直接假定衍生lag无泄漏。许可：软件包DESCRIPTION写MIT，LICENSE文件仅列作者与年份；这不足以确认所汇总八项原实验数据的单独再分发授权。数据来源公开可读，许可及再分发资格仍待核查。无需购买、登录或收费账户。

对R073：本数据至少提供独立于Montero 2022的早期实验候选来源，但每局时长、玩家身份、场次及100轮协议兼容性尚未证实。当前`R073_SECOND_INDEPENDENT_EXPERIMENT_QUALIFIED=NO`，冻结模型与评分规则不变，不事后适配调参。后续先完成固定RDA解码、逐字段缺失率、身份与场次核验、来源去重、许可确认，再判断能否进入任何E2评分。

本轮仅新增来源字节可得性及文档结构证据。没有逐行行为复算，没有真实预测分数，没有原作者算法复现。新增E2=0，E3=0，新增费用0。
