# MKT237：AI辅助决策中的主动第二意见与强制第二意见

track: market
subflow: commercial_evidence
run_date_utc: 2026-11-03
target_key: (market,second-opinion-human-AI,arxiv-2401.07058-v1,optional-request-vs-always-shown-overreliance-underreliance)
baseline_main: 8c61b86ef64942c0e980a0b8b0ebd60d54adacbd
status: COMPLETE_BOUNDED_PRIMARY_ABSTRACT_AND_REPOSITORY_CHECK
evidence_grade: MARKET-E2_REPORTED_PREREGISTERED_RANDOMIZED_HUMAN_EXPERIMENTS
participant_level_data: NOT_ACCESSED
fulltext_tables: NOT_RUN
native_execution: NOT_RUN
ci_dispatch: NOT_RUN
billing_checked: ACCOUNT_BILLING_AND_FREE_QUOTA_NOT_VERIFIED

## 研究问题与实际新证据

Lu, Wang, Yin, *Does More Advice Help? The Effects of Second Opinions in AI-Assisted Decision Making*, arXiv:2401.07058v1, 2024-01-13。作者公开摘要明确报告三项预注册随机真人实验。若AI建议与第二意见始终一起呈现，参与者对错误AI建议的过度依赖下降，同时对正确AI建议的依赖不足上升；无论第二意见来自同伴还是另一AI，均观察到此类方向。允许用户主动请求同伴第二意见，在部分实验条件下能够缓解过度依赖而没有同步增加依赖不足。来源：https://arxiv.org/abs/2401.07058

以上为作者报告的实验结果，未从全文核对具体样本数、效应量、置信区间、预注册原始记录、实验任务和附录。因此不得写成“主动请求一定改善总准确率”或“产品长期有效”。研究操纵的是第二意见的提供方式，不能推广到真实高风险人生决策的净福利。

独立检索作者代码链接 https://github.com/ZhuoranLu/Second-Opinion-HAIDM ，仓库存在，默认main，当前根目录只见README.md（154字节），未发现可直接执行的公开实验数据或复算脚本；这只是根目录范围的核验，不能推断作者从未公开其他资料。没有执行模型或读取参与者数据。

## 与MKT236的增量关系

MKT236 PNAS司法实验发现提供AI建议提高与算法的一致性，却未显著改善分类准确率。MKT237进一步提出可以被随机试验检验的交互变量：第二意见是默认强制显示，还是由使用者按需索取。二者研究任务不同，不能合并效应量。未来候选评价应预先记录：建议正确性、用户采纳、错误建议采纳率、正确建议拒绝率、最终准确性、耗时、请求第二意见比例及可能的选择偏差。不得将作者摘要转化为已证实的产品设计规则。

## 产品映射与证据界限

本轮没有核实某款在售个人规划产品实际采用此机制，也没有核实其定价、隐私或算法。因此产品功能、价格和产品专属效果均 UNKNOWN。此研究属于可移植的交互机制证据，不等于任何产品效果。个人数据、本地优先、撤销删除与跨文化效果均未在本轮实验来源中验证。

## E与F只读交接

E: 本轮查询main为8c61b86ef64942c0e980a0b8b0ebd60d54adacbd，分支API protected=false；开放PR查询返回12项且均Draft，未见合并。E168已于本地2026-11-03完成实质审计，R272生产写权限及归档前像验收P0维持OPEN；本轮未运行B复算，待核队列未完整重算，净变化UNKNOWN。GitHub Actions近期有其他历史push运行，不以当前提交无检查推断全仓库无CI。

F: F010为本周既有专题；本轮新增只读方法关联：默认第二意见可能增加对正确建议的拒绝，保留用户选择权需要配套评估其真实决策后果。没有新增F专题、没有个人敏感资料或实际部署。

sources:
- https://arxiv.org/abs/2401.07058
- https://github.com/ZhuoranLu/Second-Opinion-HAIDM
- research/market/MKT236_PNAS_FULLTEXT_IDENTIFICATION_AND_ADOPTION_ADDENDUM_2026-11-03.md
- research/operations/E168_R272_ACTIVE_WORKFLOW_WRITE_PERMISSION_AND_GATE_ADOPTION_2026-11-03.md

next_action: 获取论文合法免费全文及预注册链接，核对三个实验的样本、条件、效果量和最终准确率；若无可复算材料，转向具有真实行为结果的其他产品。继续只读跟踪R272 P0及PR依赖。禁止自动合并、触发可能计费CI、修改冻结协议。
