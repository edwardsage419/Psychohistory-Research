# B轨 R189双点隐藏率独立极端概率审计

日期：2026-10-26。状态 PASS_BOUNDED_INTERNAL_E1_INDEPENDENT_METHOD。计算前冻结协议 `protocols/R189_CLUSTER_EXTREME_TAIL_POSTSCORE_PRECOMPUTATION_FREEZE_2026-10-26.md`。

## 独立计算路线

R主程序从原R189已归档真群组计数PMF提取两个端点。B程序 `research/evidence_audit/b_r189_latent_extreme_20261026.js` 完全从o、t、h和x重建两个隐藏率p1=ot^x h/(1+ot^x h)、p2=(ot^x/h)/(1+ot^x/h)。使用BigInt有理数分别计算各潜在状态n次全失败或全成功的概率，再各取一半；独立基线采用平均隐藏率μ。全程不读取主程序用于构造真端点的PMF。

实际执行24人工世界×2条件×8个字段=384项精确身份比较，0项差异。预设负对照将一项独立基线μ加1/100，成功检出1项不一致。原h=1的24项零差额和h=3的24项严格正差额由独立计算同时支持。

完整机器审计收据 `research/evidence_audit/B_R189_LATENT_EXTREME_EXACT_AUDIT_RECEIPT_2026-10-26.json`。这属于同一项目内部不同方法复核，未获得外部研究团队独立复现，也未开展真人数据预测、历史数据检验、样本外校准或群组级不确定性重采样。新增E2=0，E3=0。

未主动运行GitHub Actions；本次新增提交的远端CI PASS未证实。主动新增费用0，账户账单与免费额度未核验。原R189正式验收、R073及PESEN v0.1冻结均未变更。
