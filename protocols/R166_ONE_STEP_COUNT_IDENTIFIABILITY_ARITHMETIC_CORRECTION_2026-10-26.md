# R166 第三方法预定网格计数错误透明勘误

日期：2026-10-26 Asia/Singapore
状态：POST_FIRST_EXECUTION_ARITHMETIC_CORRECTION
原始冻结文件：protocols/R166_ONE_STEP_COUNT_IDENTIFIABILITY_THIRD_METHOD_FREEZE_2026-10-26.md
原始冻结提交：5704ad07c3c61ffe7293ec8c97f4521727989853

## 发生经过
事前冻结文档将非中性单步比较条件写成“2*(5+9)*2=56”。该乘法实际为28。
独立 JS 枚举第一次执行触发断言 `unexpected observational partition`，未归档 PASS，未提交该失败程序。
检查原 R166 冻结 JSON 中12个矩阵后确认：N=4 有5种初始 k，N=8 有9种，非中性方向2种，每个条件比较 selection 与 transformation 这一对机制。
因此预定非中性比较总数严格为 (5+9)*2=28。中性对照为5+9=14。
两个非中性方向下完整分布相等的条件为8个，分布不等的条件为20个。此项观察发生于修正前，不能伪装为盲态事前预测。

## 影响边界
所有预先选定的 N、k、方向、公式、观察 J、TV、Bayes 风险、原始12个核矩阵、独立枚举算法和错误机制负对照完全不变。
仅修正错误的比较计数与由此导致的断言。无数据筛选、阈值调优或模型参数修改。
原始冻结文件保持不变，后续报告必须同时引用本勘误，报告第一次 FAILED 和最终重新执行结果。
由于这一项修正发生在首次执行后，标记为 `PASS_WITH_DISCLOSED_POSTEXEC_ARITHMETIC_AMENDMENT`，不能声称所有预期计数事前正确。
