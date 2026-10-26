# B子流程：R177两独立群组判别错误率的第二条精确复算

日期：2026-10-26。预计算协议：`protocols/R177_TWO_INDEPENDENT_GROUP_BAYES_ERROR_THIRD_METHOD_FREEZE_2026-10-26.md`，冻结提交 `95fcf7536e31f2ab214c205bd6fdc5b03223d99d`。

固定来源：`research/R177/R177_EXACT_RESULTS.json` Git blob `8a8819e4d85989b518b9152cfc98336457c76a9c`。R程序逐格绝对差；本B程序单独实现有理数与最小重叠 `1−Σmin(P^⊗m,Q^⊗m)`，没有调用R程序的TV函数。

实际执行：405个固定配对的m1和m2均逐项有理数相等，0项不一致；交换候选机制顺序后m2值保持不变，405次通过。n2原冻结BB/ZIB均匀分布别名的m2 TV=0。原始B机器收据：`research/evidence_audit/B_R177_OVERLAP_EXACT_RECEIPT_2026-10-26.json`。B源码：`research/evidence_audit/r177_b_overlap_20261026.js`，无需第三方依赖。复算命令：`node research/evidence_audit/r177_b_overlap_20261026.js research/R177/R177_EXACT_RESULTS.json research/validation/R177_TWO_GROUP_BAYES_ERROR_EXACT_RECEIPT_2026-10-26.json`。

科学局限：输入是同一R177固定人工PMF档案，审计属于内部不同算法的程序性复核。它没有建立独立真人样本、训练外预测、概率校准、历史事件预测、模型因果识别或外部团队复现。405对共享90个参数世界，不能当作独立观测样本进行置信区间推断。未执行远端CI。E1内部精确核对，E2=0，E3=0，外部复现=0。