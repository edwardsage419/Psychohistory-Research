# B 独立证据审计：R074 与 R075 的 E3 标签语义冲突

日期：2026-10-25。性质：证据分类与结论范围审计，原有结果、程序、冻结协议及文件一律保持不变。

## 实际读取的原始档案

`research/R074/README.md` 明确描述第二个不同作者真人重复囚徒困境实验的18个场次内留出，M3 对 M1 的 Brier 差为负，M4 对 M3 的差为正。原始机器状态 `research/R074/R074_FINAL_ACCEPTANCE_STATUS.json` Git blob `6fe05c642a1d64f8fc292315f34574c274091f55`，`study_type=INDEPENDENT_REAL_HUMAN_EXTERNAL_AUTHOR_EXPERIMENT_INTERNAL_SESSION_LOSO_E3`，且明确 `historical_social_evolution=NOT_STUDIED`。
`research/R075/README.md` 描述第三个独立作者真人实验，18场次内留出，M3 相较 M1 改善，M4收益依处理而异。机器状态 `research/R075/R075_FINAL_ACCEPTANCE_STATUS.json` Git blob `1241ad79fd1f19195eb591ce60b56668ead8cd76`，`study_type=THIRD_INDEPENDENT_REAL_HUMAN_AUTHOR_EXPERIMENT_WITHIN_STUDY_FULL_SESSION_LOSO_E3`，并明确 `long_historical_multiscale_prediction=NOT_STUDIED`。

## 分类冲突与最小修复规则

项目当前统一分类要求 `E1=合成数学证据`，`E2=真人行为证据`，`E3=真实历史证据`。R074 与 R075 历史文件里的 `E3` 是按“外部独立真人实验/第三阶段跨实验验证”的旧语义使用，不能直接转换为当前的“真实历史演化”E3。研究档案自身已经明确未研究历史演化。
建议在后续滚动汇总中将 R074/R075 计入 `E2_EXTERNAL_HUMAN_EXPERIMENT_TRANSFER`，附注原文件的旧 `E3` 名称以保留溯源。当前历史E3计数不得因这两项真人实验增加。此建议仅影响后续新报告的分类口径，**不修改**历史已冻结的JSON或其科学预测结果。

## 科学结论范围

R074与R075分别是不同来源的真人实验预测验证，具备实证价值，但仍属于项目内部执行的跨实验评估，不能冒充外部研究团队独立复现。两项均使用各自来源内其他场次训练参数，`zero-shot` 数值参数跨实验直接转移尚未检验。现有预测相关性不能证明心理记忆因果机制。R074 的两轮记忆负结果应永久保留，不能以 R075 正结果替代。
这项审计为 `EVIDENCE_TAXONOMY_DISCREPANCY_RECORDED`，没有新增 E1/E2/E3 预测分数，没有外部复现。待统一归档阶段由研究治理口径决定是否制作单独映射表；在 R 系列完成前不得提前进行模型熔炼。