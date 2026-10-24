# R136 纠正性负对照科学报告

日期：2026-10-25。证据E1，项目内部方法复核。事前纠正协议：research/validation/R136_Q_ORDER_DIRECT_TRANSITION_CONTROL_CORRECTIVE_PROTOCOL_FREEZE_2026-10-25.md。历史错误负对照永久保留 FAILED_NONDISCRIMINATING。

## 直接计算
读取已有1215行精确CSV，115527字节，SHA256 c1e5c7680314e8734d6388662aef322b1e03befd7111dd5e5596b2c9c40ee856。来源包括1134个敲诈策略条件、81个Equalizer条件。独立脚本 r136_corrective_q_marginal_cramer_audit.py 使用4阶行列式的Cramer公式重新求稳态分布，不导入此前树定理或Gauss–Jordan实现。

逐行构造状态 CC、CD、DC、DD 转移矩阵。正确对手合作概率必须按 (q1,q3,q2,q4) 映射。全部1215行的四状态边际，共4860项直接检查通过。Cramer方法独立重算全部1215行稳态及双方收益，逐行与原CSV精确相等。

810行满足q2≠q3，故意错误映射后全部810行被拒绝，检测到1620个状态边际不一致。另405行满足q2=q3，错误交换无法观察，明确记录为不可辨识，未当作负对照通过。冻结见证 χ=3、φ=1/20、q=(1/4,1/2,3/4,1/4)：正确收益(721/328,459/328)，错误收益(3413/1448,2103/1448)。两种情况下ZD收益等式仍成立，说明原负对照设计为何失效。

## 证据与边界
新增纠正性控制状态 PASS_CORRECTIVE_CONTROL_ONLY。原预注册负对照失败不可被事后更改。此次成功证明新的直接条件边际检查能检测该指定错误；没有证明所有可能的状态排序错误均可检测。

程序 Git blob 3c8bd80be1af5838764ff3c95c14e90be8a426b2；本地完整JSON收据SHA256 857cfea47a71364aea87c8026188c4d625a6544b4a66807794faac8d9b9501b0；GitHub存放紧凑收据。原1215行CSV已在本地保留，仓库可由既有树算法重建。本轮没有新CI，原R136正式第三方法验收仍需独立处理其历史偏差。E2=0、E3=0、外部独立复现=0。

复现：python research/validation/r136_markov_tree_independent.py --source research/R136/R136_MATHEMATICAL_RESULTS.json --output R136_MARKOV_TREE_1215_EXACT_ROWS.csv；随后 python research/validation/r136_corrective_q_marginal_cramer_audit.py R136_MARKOV_TREE_1215_EXACT_ROWS.csv。
