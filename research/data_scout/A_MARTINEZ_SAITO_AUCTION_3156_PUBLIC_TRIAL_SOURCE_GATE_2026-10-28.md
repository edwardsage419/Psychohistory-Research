# A轨：Martínez Saito 人类竞价实验公开数据的逐行来源资格审计

日期：2026年10月28日（Asia/Singapore）。本项仅登记公开科研来源，不复制原始参与者级记录。

## 固定公开来源
原作者 GitHub 仓库 https://github.com/mmartinezsaito/action-in-auctions ，默认分支 master，固定 Git tree `6c4b22a92cc8f12b5aa38f1616baec51158fde63`。原始CSV路径 `data/data.csv`，Git blob `4b70d6faaf932e32f626922a0ee803d0d6d7622c`，259162字节。另有 `data/PrerecordedData.csv`，Git blob `e23db54dc1bfa383be7ddd747e1e7a6eac486e27`，8101字节。README指向研究“Action in auctions: neural and computational mechanisms of bidding behaviour”，论文 DOI https://doi.org/10.1111/ejn.14492 。仓库根 LICENSE 为MIT软件许可证，Git blob `7a3231ea3093ea3c063e5dbeb4931954e3a56c5f`；参与者数据的单独再分发条款未核实，暂不转载数据。

## 本轮实际读取与统计
连接器实际完整读取 `data/data.csv` 259162字节，逐行按带引号的CSV字段分割。确认3156条数据、20列、47个公开伪名参与者编号、24个block_n标签、3种条件NC/SC/BC，每条件1052行。所有行列宽一致；(sid,block_n,snb)复合键重复0。每名参与者均有24个block标签，19人每人60条记录，28人每人72条记录。country字段有RU和CH两个编码，分别2196和960行；仅为公开原始编码，本轮未据此推断个人身份。

主要字段：sid（伪名参与者）、block_n（区块标签）、snb（条件）、bid（竞价）、b2_bid、s1_rp、s2_rp、outcome、rt、profit、out_bool、out_prev、out_aprev、bid_prev、bid_aprev、bid_next、bid_anext、dl。三个条件的outcome缺失分别112、112、113，共337行；对应有效非NA outcome为940、940、939，共2819行。bid和profit各缺失337行。rt缺失1477行。缺失是否代表未完成竞价、无响应或其他实验机制，须通过作者原实验代码与论文核对，不可自动当作零竞价或失败结果。

本轮仅从源文件统计字段与键；`block_n`是区块标签，尚不能将24个区块解释为独立实验场次。README说明 `PrerecordedData.csv` 为先前实验的预录对手行为，意味着部分互动对象可能为电脑代理；需先从实验流程确认真人对手身份与历史信息可见性。两种数据不能默认视为两个独立真人实验。

## 复现资格
A轨来源状态：`RAW_PUBLIC_READ_SUCCESS`；模式字段可解析；缺失机制、真人对手身份、独立实验场次、参与者级数据许可均为 `UNRESOLVED`。适合后续研究有反馈的多轮竞价与行为学习，须先冻结评分、区分受试者与block、建立时间前缀与独立留出。R073冻结的双人100轮囚徒困境协议不适用，`R073_DIRECT_SCORING_ELIGIBILITY=NO`。没有新E2正式预测或外部独立复现。数据不包含在本仓库，成本0。

## 复算方法与边界
读取固定blob，CSV行数减1为3156，列数20；按sid计数得到47；按snb聚合每组1052；按sid的24个block_n唯一值核对；对(sid,block_n,snb)检重；统计 `outcome === "NA"` 和 `bid === "NA"`。结果为项目内部一次数据处理检查，尚无独立第二实现及论文表格逐项复算。后续先查原作者竞价程序、数据使用范围和缺失机制，再决定是否建立独立真人E2任务。
