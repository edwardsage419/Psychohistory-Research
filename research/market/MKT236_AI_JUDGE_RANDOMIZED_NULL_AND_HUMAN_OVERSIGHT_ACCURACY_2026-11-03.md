# MKT236: AI建议增量效应的随机试验反例与人类监督局限

track: market
run_date_utc: 2026-11-03
target_key: (market,AI-assisted-decisions,PNAS-2025-e2505106122+PLOS-2024-e0298037,randomized-incremental-effect+human-override-failure)
baseline_main: b36ffeff4d9377f54bdc207a6986238c6e0ad6b6
status: COMPLETE_BOUNDED_PRIMARY_ABSTRACT_CROSSCHECK
evidence_grade: MARKET-E2_PUBLISHED_HUMAN_EXPERIMENTS; NO_PRODUCT_SPECIFIC_VALIDATION
participant_data: NOT_ACCESSED
native_replication: NOT_RUN
CI_dispatch: NOT_RUN
paid_services: NONE

## 问题及新证据

MKT235中的 Joint Insights 随机分配了整体工具，无法拆分AI预测的独立贡献。本轮寻找直接检验AI建议增量价值的独立真人实验，得到两项方向相反于「增加AI/人工监督必然提高决策质量」的公开正式论文。

1. Ben-Michael, Greiner, Huang, Imai, Jiang & Shin (2025), *Proceedings of the National Academy of Sciences* 122(38), e2505106122, “Does AI help humans make better decisions? A statistical evaluation framework for experimental and observational studies.” 作者正式发表摘要及2024年公开预印本描述：在审前保释风险评分的随机试验中，向法官提供算法风险建议，没有改善现金保释决策的分类准确性；对同一研究数据的算法独立决策比较，包括风险评分及大语言模型，表现更差。后者是研究框架下的估计比较，不应错误写成算法在现实中被随机分配作出保释决定。该结果有特定的司法制度、因果识别假设、错误成本及公平性限制，不能迁移成所有AI决策辅助无效。来源：https://imai.fas.harvard.edu/research/ai/ ; https://pubmed.ncbi.nlm.nih.gov/40961147/ ; https://arxiv.org/abs/2403.12108 。

2. Sele & Chugunova (2024), *PLOS ONE* 19(2), e0298037, “Putting a human in the loop: Increasing uptake, but decreasing accuracy of automated decision-making.” ETH Zurich开放正式版本摘要：292人在线预测实验中，66%选择委托给与人类同样准确的算法；允许监控和修改建议使选择算法的比例提高7个百分点。参与者更倾向遵循算法建议，却较少干预最不准确的建议；在该任务下人类参与设计增加算法采用而降低最终准确性。该实验是在线预测任务，不能作为司法、医疗或真实长期人生决策的效果估计。来源：https://www.research-collection.ethz.ch/entities/publication/ad89a0b9-3d43-4c76-b5f4-c6941c73f0dd ; https://doi.org/10.1371/journal.pone.0298037 。

## 与MKT235比较及应用边界

Joint Insights的随机对照支持包含教育、偏好评估和个性化预测的整体干预在特定临床场景改善部分指标；上述司法研究对单独提供算法建议的边际效果给出无改善证据；在线预测实验说明「可人工修改」这一界面权限不保证有效纠错。三项研究场景、目标变量、比较条件不同，不能直接合并效应量。

未来研究设计候选：预先测量无AI初始判断；随机分配是否展示AI建议；记录建议内容、最终选择、用户是否纠错及错误成本；按建议正确与否分层报告依赖；设置AI独立基线并对选择性观察的反事实结果作识别审查；分别评价短期分类准确性、真实行动后果和长期福利。此为方法储备，尚未实施产品开发或个人数据采集。

## 证据等级与开放问题

MARKET-E2限上述已发表人类实验的摘要级核验；本轮未读取完整论文统计表、随机化日志、原始数据或代码，未复算统计结果。司法研究的潜在结果识别假设与分类指标需要下一轮在免费全文中详细审查。产品级输入接口、模型权重、价格、数据删除和当前部署均未披露或未验证；本轮研究对象为实验决策系统，非已上市通用个人规划软件。厂商宣传等级不适用。不能把这两项研究升级为R E2/E3。

## E与F只读协调

本轮 main 基线 b36ffeff4d9377f54bdc207a6986238c6e0ad6b6，最新R/B报告 R272_P0_ISOLATED_CHILD_PROCESS_TRUST_BOUNDARY_REVIEW_20261103T0140Z 指出候选工作流的Python子进程没有隔离，-I只施加到父进程也不能自动保护子进程；本地临时脚本控制为合成反例，生产完整端到端伪造尚未证明。R272 P0保持OPEN，owner应先审查现行workflow contents:write及自动push路径。开放PR #1至#12仍为Draft且未合并；原239队列历史154项，本轮未重新逐项重算，净变化UNKNOWN。F010 2026-W45原始专题已只读确认COMPLETE，AI建议不可靠时形式化人工覆盖可能不足，沿用其人类实质控制研究，不新增F编号。无跨轨修改、无CI触发、无个人敏感数据、无费用支出；GitHub账单与Actions免费额度NOT_VERIFIED。

## 下一步

优先获取PNAS正式论文免费全文中的随机化和可识别性条件，核查AI-alone估计与人类+AI比较的误差指标；随后研究用户可以自主请求第二意见时是否优于强制显示第二意见。E继续只读追踪R272的子进程隔离、工作流触发覆盖和生产写权限，保持P0开放直至真实验收。
