# Henrich与Boyd（2001）附录离散稳定性与索引核查

track: theory
run_date: 2026-11-07 (Asia/Singapore)
target_key: (theory,Henrich-Boyd-2001,10.1006/jtbi.2000.2202,appendix-discrete-stability-index-audit)
observed_head: 2b3e91d3343afc9b2de1352aeab9729a6a6f5c8e
status: PRIMARY_APPENDIX_IMAGE_READ; ANALYTIC_BOUND_COMPLETE; NO_FULL_JACOBIAN_REPLICATION

## 原著来源与直接阅读范围
Joseph Henrich and Robert Boyd (2001), Why People Punish Defectors, Journal of Theoretical Biology 208:79–89, DOI https://doi.org/10.1006/jtbi.2000.2202 。直接查看作者公开原刊PDF印刷页89的整页图像，核对附录通用递推、收益差、特征值及末句；另核对印刷页83的传播参数归一化说明及印刷页85的局部稳定条件。来源 https://henrich.fas.harvard.edu/sites/g/files/omnuum5811/files/henrich/files/henrich_boyd_2001.pdf 。正文其他页沿用此前已归档阅读，未重新声称全文逐字审计。

## 独立解析核查：离散更新的稳定性判据
原文给出 Δp_j = p_j(1-p_j)[(1-α)βΔb_j+α(2p_j-1)]。在边界均衡处，文中列出增长率线性化特征值 λ_j，并以最大 λ_j<0 作为局部稳定条件。因为实际状态更新为 p(t+1)=p(t)+Δp(t)，严格的离散时间局部稳定判据应为 |1+λ_j|<1，即 -2<λ_j<0，而不能在任意离散系统中仅检查 λ_j<0。

对原文给出的具体归一化，0≤α<1/2 且 β=1/max|Δb_j|（在其选定的收益差上界下），故 |βΔb_j|≤1。边界点的线性化特征值形式为 λ_j= -α+(1-α)βΔb_j（末阶惩罚方向取对应收益差；其余边界方向同理），因此 λ_j≥-α-(1-α)=-1。于是原模型允许的参数域内，λ_j<0 足以推出 -2<λ_j<0，离散映射在相应方向上局部收缩。这是对原文稳定性判据的有条件辩护，不构成发现原模型错误。若未来扩展模型取消 β 归一化或使用更大的时间步长，则须恢复 |1+λ_j|<1 的完整判据。

## 原刊索引疑点
原刊印刷页89附录末句将稳定点印为 (p_0,p_i,...,p_{i+1})=(1,1,...,0)，而前文定义仅包含阶段0至i共i+1个状态变量，印刷页85亦将合作均衡描述为 p_0=...=p_i=1。此处 p_{i+1} 超出前文定义的状态维数，疑似排印或索引笔误。只记录原文内部不一致；未获得作者勘误，不能擅自确定其原意。后续如需引用应以明确列出的状态变量和特征值条件为准。

## 证据与限制
这是原始排印图像核对及条件性解析证明。没有执行完整Jacobian矩阵逐项微分、程序数值特征值检验、原作者代码复算或任何真人/历史预测。与前次同一文献的 e<1/N 条件审计属于互补的离散时间数学判据和原刊索引核查，不创建新的TH编号。C013当日已完成于2026-11-07，D003本周已完成于2026-11-02；不新增C/D编号。R073与PESEN v0.1冻结状态、R与MARKET证据等级保持不变。CI NOT_RUN；未主动调用收费服务，实际账单NOT_VERIFIED。

next_action: 如需继续验证，独立求导原始完整Jacobian并检查每一特征值及归一化β的全局定义；理论主线随后转向其他学科，避免在同一篇原著无限细化。
