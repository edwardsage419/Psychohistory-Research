# R301 S97 科学报告：固定风险先验误设与第五次观测的独立预测风险

UTC 2026-10-30。研究状态 PARTIAL_NONBLIND_INTERNAL_E1。冻结先于本轮评分，commit b18d1cd4e149a60ebfe3732f38f09f1cb6d94e7a。原R301正式有界E1验收不变。R073及PESEN v0.1冻结。

## 研究问题及来源

Adams与MacKay（2007）Bayesian Online Changepoint Detection原论文 https://arxiv.org/abs/0710.3742 ，原R301协议在 protocols/R301_BAYESIAN_ONLINE_CHANGEPOINT_BERNOULLI_192_SOURCE_PRESCORE_FREEZE_2026-10-23.md 。本次新增固定错误变点先验对真正未观察的第五位人工数据的预测风险检验。

原模型Beta(1,1) Bernoulli分段。真实风险率h*与假定风险率h各取0、1/4、1/2。每个真实风险率穷举16条四位历史，再枚举第五位y∈{0,1}，用真实联合概率加权Brier损失(q_h-y)^2。共3×3×16×2=288条人工来源，九组候选风险。每个真实风险率仅有32个独特联合原子，候选共用这些原子，不能把288行视为独立人类样本。候选风险率事先固定，未进行拟合或调参。恒定1/2预测基线风险为1/4。

## 精确结果

| 真实风险率 | 假定0 | 假定1/4 | 假定1/2 | 恒定基线 |
|---|---:|---:|---:|---:|
| 0 | 0.194444444 | 0.204443363 | 0.219695825 | 0.250000000 |
| 1/4 | 0.238389757 | 0.228592450 | 0.232179255 | 0.250000000 |
| 1/2 | 0.261574074 | 0.245102124 | 0.242146345 | 0.250000000 |

表格为小数展示，机器JSON保留完整Fraction。当真实风险率1/2，错误假设风险率0时，Brier风险精确为113/432，约0.261574，超过无信息基线0.25。正确风险率1/2的风险约0.242146。当真实风险率0，假定1/2使风险从7/36升至约0.219696。错误的合法风险参数可能造成比恒定预测更差的结果。

九组均严格满足 Brier候选风险减oracle风险=Σ四位历史P_true(history)×(q_candidate-q_true)^2。正确风险率超额风险精确为0，其他超额风险非负。该恒等式检验的是有限人工生成模型中的预测一致性，不能说明哪种风险率适合现实社会。

## 程序及验收边界

R路线采用运行长度递推，8项unittest实际通过，生成288条CSV和九组JSON。B路线完全独立枚举四位历史的2^3分段及五位历史的2^4分段，逐项精确复核288条原子、九组风险和超额风险。B路线9项测试通过，其中1项完整正例、7项错误注入拒绝、1项归一化检查。归档数据SHA256见 R301_S97_RECEIPT.json。

复算命令：

`python research/validation/r301_s97_hazard_heldout.py --test`

`python research/validation/r301_s97_hazard_heldout.py --emit research/validation`

`python research/evidence_audit/b_r301_s97_independent_segmentation.py --test`

`python research/evidence_audit/b_r301_s97_independent_segmentation.py --folder research/validation`

证据仅为人工E1。没有真人E2、历史E3、经验概率校准、真实变点标签、外部独立团队复现。没有运行GitHub Actions。完整来源归档与科学有效性分开判断，S97状态PARTIAL_NONBLIND_INTERNAL_E1。
