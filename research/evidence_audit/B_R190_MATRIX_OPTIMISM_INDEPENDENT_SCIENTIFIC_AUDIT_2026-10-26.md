# B轨 R190平滑矩阵独立训练乐观差距审计

日期：2026-10-26。状态：PASS_BOUNDED_INTERNAL_E1_DIFFERENT_ALGORITHM。

计算前冻结协议 `protocols/R190_TRAINING_OPTIMISM_40_POSTSCORE_PRECOMPUTATION_FREEZE_2026-10-26.md`，冻结提交 `790af9290b12d86c4684ccd706d06d07b87aef9a`。

B程序 `research/evidence_audit/b_r190_matrix_optimism_20261026.js` 只读取原R190 8套Fraction平滑矩阵、10世界原始真条件均值和方差、以及待核主收据。完全不读取主程序所枚举的1375条训练表，也不调用主程序函数。独立使用BigInt有理数数组计算：

`R_train=(1/5)Σ_i[(μ_i-(Sμ)_i)^2+(1-1/n)v_i+(1/n)Σ_j(δ_ij-S_ij)^2v_j]`

`R_future=(1/5)Σ_i[v_i+(μ_i-(Sμ)_i)^2+(1/n)Σ_j S_ij^2v_j]`

`R_future-R_train=(2/(5n))Σ_i S_ii v_i`

10世界×4固定λ=40条件，对每条件核验训练、未来、差额及其独立恒等式，共160项精确比较，0不一致。另检查每个S的5行和等于1，共200项；40项乐观差距均严格正。预设负对照只在恒等式右侧错误增加 `(2/(5n))v_0/100`，40项全部实际检测到不一致，错误没有进入主收据。

机器收据 `research/evidence_audit/B_R190_MATRIX_OPTIMISM_40_EXACT_AUDIT_RECEIPT_2026-10-26.json` 包含全部40组解析结果。该结果属于同一项目内部不同算法的复核，外部独立复现=0。原R190已有人工E1正式验收未改变，新增真人E2预测=0，历史E3=0。没有独立样本校准或人群外推证明，R073及PESEN v0.1保持冻结。

本次未启动GitHub Actions，远端新增CI PASS未证实。主动新增费用0，账户免费额度及账单未独立核验。