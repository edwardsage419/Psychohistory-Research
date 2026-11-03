# MKT237 实验3原始预注册核对：请求者子集与事前分析边界

track: market
target_key: (market,second-opinion-human-AI,arxiv-2401.07058-v1,experiment3-original-preregistration-vs-requester-subgroup)
baseline_main: 99ef7cbdedf36dd7744874df3c90f7795c46d721
date_utc: 2026-11-03
status: COMPLETE_BOUNDED_PRIMARY_REGISTRATION_COMPARISON
evidence_grade: MARKET-E2_AUTHOR_REPORTED_RANDOMIZED_EXPERIMENT_WITH_PRIMARY_PREREGISTRATION
participant_data_reanalysis: NOT_RUN
ci_dispatch: NOT_RUN

## 新增独立来源

直接读取实验3原始 AsPredicted 记录 #103727，2022-07-31 01:54 PT 登记，明确声明登记时尚未收集该实验数据。原始登记入口 https://aspredicted.org/MWC_PH1 ，当前可读页面 https://aspredicted.org/MWC_PH1 。正式预印本 v1 日期 2024-01-13：https://arxiv.org/html/2401.07058v1 。

预注册明确三组：AI建议无第二意见、允许请求高一致性同伴意见、允许请求低一致性同伴意见。预期每组100名有效参与者；发表论文实验3实际通过注意力检查者336名。预注册主分析为全体随机分组的单因素ANOVA及事后比较，指标包括过度依赖、依赖不足、适当依赖即最终准确率、时间、信心。预注册时间异常值剔除规则为高于第95百分位数。

## 关键核对：请求者子集分析属于事前登记的探索性分析

原始预注册第8项明确写明，将参与者按是否请求过同伴意见分组，并重复分析。故论文报告的请求者子集比较**不能一概称为未预注册或事后临时提出**。这是一项实质纠偏。

然而该子集划分发生在随机分配之后，实际请求行为由参与者选择，分组可受认知能力、信任和任务困难程度影响。预注册并不能消除这一选择偏差。请求者子集对照不能直接识别提供请求选项对全部随机参与者的平均因果效应。

论文实验3全体随机参与者分析未证明最终准确率显著改善；较有利的请求者子集结果仅出现在高一致性第二意见条件。两个结论必须并列呈现。原始研究是20条电影评论的短时情感判断任务，无法证明长期个人决策效用。

## 尚未闭合

尚未逐项核对实验3正式论文所有ANOVA数值、预注册第8项所有探索分析与发表表格的逐项对应；尚未独立复算参与者级数据；尚未核对实验1与2的完整预注册原件。未执行实际商业产品、未读取任何个人敏感资料。

## E与F关联

E: 本轮只读查询main基线SHA如上，开放PR 12项全部draft，未合并；main protected=false。R272此前P0未取得关闭证据，维持OPEN。未复算正式待核队列，净变化UNKNOWN。
F: 研究强调第二意见请求行为本身可能造成选择偏差，未来人工控制的有效性评价应以随机分配全体样本的最终结果为主要依据。本周F010已完成登记，本轮没有创建新F编号。

## 费用与权限

仅公开英文论文及公开预注册，未使用付费服务或触发Actions。GitHub账单和免费额度NOT_VERIFIED。
