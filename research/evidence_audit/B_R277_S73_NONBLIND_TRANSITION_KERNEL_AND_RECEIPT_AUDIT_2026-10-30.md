# B 独立方法审计：R277 S73 时间下采样、有限分类及持久化收据
日期：2026-10-30（Asia/Singapore）。目标键：(B,R277,S73-freeze-53e3b18b,independent-kernel-and-receipt-check)。
这是同一研究流程内的非盲态独立算法复核，研究者已读R277原始Markov设定与S73结果，外部独立团队复现数为0。

## 固定对象及来源
原R277冻结：923a161bbdc012c138e53f1fa316e6085ff2704e。
本轮S73评分前冻结：53e3b18b28d46c0c5e26194dd8e85bc408450af6。
R完整六位原来源积分JS：research/validation/r277_s73_temporal_subsampling_20261030.js，Git blob 6d250fe671cba6307af7275ff4ef35648020f04f。
持久化72行CSV：research/validation/R277_S73_OBSERVED_TRIPLETS_72_ROWS_2026-10-30.csv，Git blob 0ed6a96fcbdbd4b5d361e1db14fd8c90dd18a791。
持久化完整JSON：research/validation/R277_S73_EXACT_RESULTS_2026-10-30.json，Git blob 2580b4dd7f7ab5e53e0cbdc4d47cde0f7a3e193a。
B独立审计程序：research/evidence_audit/b_r277_s73_transition_kernel_receipt_audit_20261030.js。

## 独立算法
R路线直接积分每个真实模型64条六位原来源，共192个带模型标签的人工配置。
B路线从对称二态转移核推导间隔d的相同概率q_d=[1+(2s-1)^d]/2，对三个观测位的两个可见间隔直接连乘；**不调用R的六位来源枚举函数**。
B路线独立计算72个可见观测配置概率、27个真实机制×预测机制混淆矩阵单元、9个两模型TV距离，并验证每窗口的8个概率归一化、MAP平局顺序及宏平均正确率。
实测全部一致：相邻窗口宏正确率13/24，隔一期窗口B/C均为73/192；相邻反持续与持续模型TV=1/2，间隔一期则TV=0。B/C下两模型的完整可见三位分布完全相同，有限分类器的PERSISTENT预测列为0源于预设平局顺序。

## 实际运行与错误注入
通过GitHub连接器重新读取上述R源码、CSV及JSON。V8实际执行远端R源码的run()与csv()，完整JSON对象与CSV字节逐项相等。独立B校验器实际执行并核验72个观测概率、27个混淆矩阵单元、9个TV距离及72条CSV唯一键。
对持久化对象实际执行8项篡改负例，全部被独立校验器拒绝：观测概率、混淆矩阵、TV距离、证据等级升级、冻结SHA错误、删除窗口、CSV重复记录、CSV遗漏记录。没有静默更改原收据。
归档B JS在V8执行PASS。**原生Node命令行读取远端完整CSV/JSON的执行仍NOT_RUN**，故原生CLI门保持开放；本轮没有触发GitHub Actions，因为免费额度未核实。

## 科学边界
内部精确算法一致与持久化收据一致均为PASS；外部团队盲态复现NOT_RUN，真实人类样本外预测NOT_RUN，真实历史预测NOT_RUN。S73仍属探索性人工E1，原R277正式验收状态不变。R073及PESEN v0.1冻结。
A轨Andreozzi会话切分属于真人数据资格审计，不能作为S73 Markov机制的E2验证。后续可做真实数据上的事前冻结依赖诊断，但需核验测量误差、时间间隔及组内相关。
