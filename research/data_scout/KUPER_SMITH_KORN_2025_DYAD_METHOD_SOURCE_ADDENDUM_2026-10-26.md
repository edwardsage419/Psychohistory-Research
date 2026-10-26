# A：Kuper-Smith/Korn 真人重复博弈数据的原作者论文方法交叉核验

2026-10-26。固定来源 GitHub `dnhi-lab/losses_gains_2x2` commit `345348cdc0018e8e030b05fb47dc845fd3e0d29a`，原作者英文期刊论文2025-07-24正式发表：https://www.nature.com/articles/s44271-025-00288-5 （DOI 10.1038/s44271-025-00288-5）。

新增核验：原作者报告重复囚徒困境实验1、2、3的纳入分析人数分别为24、46、44，共114名真人。参与者以六人组进行互动，每人同其余五名参与者分别重复互动，每人300次决策，对每名对手有60次互动。实验1是先导研究，实验2和3为预注册重复实验。作者报告约79%决策与对手上一行动相同，该数值是论文结果，当前没有从原始CSV独立复算。作者明确使用 participant nested in group nested in experiment 处理非独立观察。

再次核验作者MATLAB字段说明：第4列对手ID，实验1该字段缺失；实验2/3有对手ID字段定义。第25、26列是双方合作行为，第30、31列是上一轮双方行为，第10至13列是收益矩阵。必须把互动双方可能的镜像记录锁在同一留出分组，按组或场次独立评价，禁止把逐人300次记录当独立实验。不同收益矩阵的迁移资格尚未冻结。

实际重试读取清洗CSV前3行，GitHub接口仍返回空内容。Git blob `ffd6776f3e9fd1444c84e50e4c61e3ff418a2488`，未核验原始行数、身份、缺失和实际配对。根目录MIT LICENSE覆盖软件及相关文档；真人行为CSV的专属授权范围仍未确定，论文CC BY不自动赋予数据许可。现阶段 `PEER_REVIEWED_HUMAN_SOURCE_CONFIRMED / DYAD_METHOD_CONFIRMED / RAW_ROWS_BLOCKED / DATA_LICENSE_PENDING / R073_TRANSFER_NOT_APPROVED`。新增E2预测0，费用0。
