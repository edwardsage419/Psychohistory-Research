# R231 S27 有限样本四指标 tetrad 零值判别，预先冻结

日期：2026年10月28日，Asia/Singapore。研究证据等级仅 E1 人工，R231 既有正式验收保持不变。基准 main HEAD：b902fff7c17c0c746ac37d52f2c89ada4008e5b4。原始来源路径 `research/R231/R231_ALL_512_ORIGINAL_CFA_STRUCTURAL_ATOMS.csv`，原始 blob SHA `f56003f4b18f1dfcbdcd00aabc22fa0815205b64`；原结果 blob `740734d5c9489f0ee23514e1b593797b5c6b431b`。本增量不得修改任何原 R231 文件。

## 固定实验与统计量

沿用原 R231 八个人工世界，每世界64条独立等概率完整外生来源。只取四个观测列 X1..X4，隐藏 T/U/E 禁止进入样本判别统计量。对每个世界分别独立有放回抽取 n=2 与 n=3 个来源，按有序来源序列完整枚举，n=2 有 64²=4096，n=3 有 64³=262144。八世界共 2,129,920 条有序序列。各序列概率 64^(-n)，重复来源允许。无真人、无抽样随机种子。

每个序列计算采用分母 n 的样本协方差 C，保存整数矩 A_ij=n² C_ij=n sum_k X_ki X_kj − (sum_k X_ki)(sum_k X_kj)。计算三个有符号 tetrad 整数分子：
 tA=A12*A34−A13*A24；
 tB=A12*A34−A14*A23；
 tC=A13*A24−A14*A23。
三者全零记 ZERO，否则 NONZERO。三个表达式的第三个与前两个线性相关，不能算作三个独立检验。只计算 exact-zero 描述性频率，不使用统计显著性阈值、p 值或 CFA 拟合优度。

## 预定判据与反例

1. 每世界每 n 计数必须和 64^n 完全一致，ZERO+NONZERO 等于总数。
2. n=2 的所有世界 tetrad 必须全零，这是样本中心化矩阵秩最多1的代数结果。故人口 tetrad 非零的世界也会出现 100% 样本零值。
3. n=3 计算八世界 ZERO/NONZERO 的精确计数；人口 tetrad 全零的 ONE_FACTOR_VALID、ONE_FACTOR_SIGNED、ONE_FACTOR_UNEQUAL_LOAD 与 TETRAD_FALSE_REASSURANCE 也可能有 NONZERO 样本值。该“非零”不能被解释为真实总体单因子假设已被否证。
4. CORRELATED_RESIDUAL_METHOD 与 SECOND_FACTOR_SEMANTIC_ALIAS 的全部样本统计计数必须一致；保留二者仅语义别名的限定。R231 原始人口 tetrad 必须逐世界回归一致。
5. 主要 R 路线直接枚举有序来源序列。B 路线必须按相同可观察四元组聚合频数，以无序二元或三元多重集及排列重数独立复算；两路线按世界、样本量、ZERO/NONZERO 精确一致。故意改变一个收据计数必须被检测。
6. 输出精确整数计数与有理数比率，所有内部检查保留机器可读收据。任何计算异常、访问失败、并发冲突都登记，禁止覆盖现有文件。

## 证据界限与成本

这是人工 E1 的有限样本 tetrad 行为研究。没有真实问卷、没有 E2/E3、没有外部研究团队独立复现。内部 B 路线仅程序性独立复核。R073 冻结模型与评分规则、PESEN v0.1 不动。不得使用收费 API、收费 runner、付费数据。CI 只有在确认不产生费用后才允许启动，否则记 NOT_RUN。研究次序仍先完成 R 系列，再统一归纳分类，最后熔炼。
