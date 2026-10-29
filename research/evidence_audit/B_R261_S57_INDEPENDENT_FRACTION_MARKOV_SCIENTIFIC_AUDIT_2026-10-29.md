# B 轨 R261 S57 非盲态独立数学核审

UTC 2026-10-29。目标键：(B,R261,S57 commit 1003be30,前缀 Brier 与共同噪声联合概率)。R 事前冻结协议已在评分前独立提交。本 B 路线事前已阅读原 R261 的冻结机制、九世界、原始正式报告与本轮 R 的部分结果，因此属于 NONBLIND_INTERNAL_CROSS_METHOD，不能称盲态或外部独立复现。

## 独立路线
Python 3 Fraction 从 q(m) 及 K0→K1 三态 Markov 核直接推导，不读取 R 原始 9216 行 CSV，不导入 JS 或调用 R 函数。独立核为条件独立 ((1−q)²,2q(1−q),q²)，共同噪声为 (1−q,0,q)。由 K1 条件 q 算 P(Y2=1|K0)、前缀风险、oracle 风险、均场预测的额外平方风险，另直接推导 J1 联合概率与错误独立近似惩罚。

已归档源码 research/evidence_audit/b_r261_s57_independent_markov_oracle_20261029.py，Git blob fdb4413a648b8e6115f04dd73f7558c7fde7fd32，**与本地实际运行文件的 git hash-object 完全相同**。本地执行 Python 命令行 --selftest，27 组×16 字段=432 项精确 Fraction 自检通过。五项明确的负例均被拒绝：重复组、删组、改 Brier、E1 篡改为 E2、错报原来源数量。

## 已落盘 R 收据比较
GitHub 上 R 原 JSON blob 8efb576b3ef6e5868ad54854d721e97b8621c6a4。使用 GitHub 连接器直接从此持久化 JSON 抽取全部 27 组、每组 16 字段，按固定字段顺序保存为 research/evidence_audit/R261_S57_R_PERSISTED_COMPACT_27_GROUPS_2026-10-29.txt，Git blob 0dfdf5743b08925eac656fc468a4f3c2ebe8e9c9。该 blob 与本地复制后供 Python 运行的文本 git hash-object 相同。将投影还原为字段对象后，Python CLI --verify 实际输出 persisted_receipt_verified=true、exact_field_comparisons=432，0 不一致。

这证明 **已保存 R 计算收据的全部 27 组科学评分字段**与独立三态概率路线精确一致。当前核验对象为固定字段投影，完整原 JSON 的元数据所有字段尚未在本地以原文件原样调用 Python --verify；完整 JSON 直连 CLI=NOT_RUN。R 归档 JS 已由隔离 V8 执行并生成与原 JSON 17227 字符完全一致的输出，Node.js 原生 CLI=NOT_RUN。

## 解释边界
原始来源由 R 路线逐 9216 行检验并运行 5 个错误注入，B 未独立重审原 CSV 的每一原 bit；两个路线分别证明不同层次。当前科学结论属于 E1 人工两人两步模型内的精确算法一致性，没有真实留出、概率校准、独立真人样本、历史样本或外部团队复现。E2/E3 新增 0；R073/PESEN v0.1 不变。后续优先补完整原 JSON Python CLI、Node CLI、原 CSV 独立全量复核；无已核验的免费 Actions 额度，本轮不启动 CI。
