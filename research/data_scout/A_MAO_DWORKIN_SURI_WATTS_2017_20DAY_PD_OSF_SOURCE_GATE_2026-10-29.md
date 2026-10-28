# A轨：Mao等2017长期真人重复囚徒困境公开数据来源审计

日期：2026-10-29。新候选来源登记，未获得原始逐轮数据，未执行真人预测。来源仅使用英文正式论文及原作者公开代码。

## 一手论文和实验单位

Mao, A., Dworkin, L., Suri, S. & Watts, D. J. (2017), *Resilient cooperators stabilize long-run cooperation in the finitely repeated Prisoner's Dilemma*, Nature Communications 8, 13800. DOI https://doi.org/10.1038/ncomms13800 。原作者正式论文 https://www.nature.com/articles/ncomms13800 ，公开数据登记 https://osf.io/64z8u/ ，原作者实验程序 https://github.com/TurkServer/long-run-cooperation 。

正式论文报告94名参与者参与分析，实验设计持续20个工作日，每日20场，每场10轮，最多400场十轮重复博弈。两名玩家在每场内相互博弈，场与场之间重新随机配对；因此400场不可合并成同一双人4000轮，也不能将20天视为独立受试者。论文还说明开始招募113人，分析样本94人的关系需以正式排除规则复验。

## 实际核验的原作者程序字段

已读取GitHub仓库 `TurkServer/long-run-cooperation` 的 `README.md`、`library.py`、`model.py`。公开源码 `library.py` Git blob `c331ba695c3846935c5e3e640e53569e78208c28`，`model.py` blob `0da8d8a69ce5dd6235c2033bc117145e8b7fe769`。源码中 `NUMROUNDS=10`、`NUMGAMES=20`，读取 `db.actions` 的 `_groupId`、`roundIndex`、`action`、`userId`；`db.ts.experiments` 保存实例与结束原因，`db.ts.assignments` 用于参与者跨日关联。代码区分finished与abandoned并有惩罚性填补路径，实际复算必须先冻结是否纳入填补及缺失记录的规则。原始MongoDB结构属于软件预期结构，尚未证明OSF归档文件具有同样字段。

## 数据获取、许可、隐私与R073资格

论文明确指向OSF项目 `64z8u`，但本轮OSF文件目录/API无法通过当前公开检索渠道访问，未取得文件名、文件级校验值、文件级许可或任何原始行。原作者GitHub仓库公开的是实验程序，不等于论文逐轮真人原始数据。不得把软件字段冒充已读到的原始数据字段。参与者匿名身份及跨日链接需要单独隐私审查，不得公开原始worker ID、邮箱或其他可识别信息。论文开放许可不能自动推定OSF数据文件的再分发许可。

实验有真实双人10轮场次和长期追踪价值。R073冻结的双人100轮独立场次评分不能直接把不同对手的十轮场次拼接成100轮，`R073_DIRECT_REPLAY=NO`。后续其他纵向E2研究可能需要独立冻结新协议，但当前研究顺序要求先完成R系列。

## 明确复现准备结果

`PAPER_AND_CODE_VERIFIED`，`RAW_OSF_UNREAD`，`ACTOR_ROUND_SCHEMA_FROM_CODE_ONLY`，`SESSION_IDENTIFIERS_RAW_UNVERIFIED`，`FILE_LEVEL_LICENSE_UNKNOWN`，`HUMAN_SOURCE_CANDIDATE`，`R073_DIRECT_REPLAY_NO`，`NEW_E2=0`，`NEW_E3=0`。

后续仅通过免费只读渠道取得OSF文件清单与许可，先冻结真实原始列、身份去标识化、每场10轮配对唯一性、跨日重复参与者去重、退出/填补、时间顺序和留出分组审计。若OSF仍不可访问，保留阻塞。不得使用收费API、注册付费账户或非公开私人数据。
