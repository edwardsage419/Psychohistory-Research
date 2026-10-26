# B轨 R202未来时间阈值独立解析复算

日期：2026-10-27。状态PASS_INTERNAL_INDEPENDENT_ANALYTIC_AGGREGATION。

主程序从原R202的96条训练源读取已选倍率，对四个未来阈值逐项枚举事件概率及两种结果的平方损失。B程序 research/evidence_audit/b_r202_horizon_transport_independent_20261027.js 独立读取原R202正式结果 research/R202/R202_EXACT_RESULTS.json 的六世界已选候选概率质量，使用B=p(1-p)+(q-p)^2解析式直接计算新阈值的期望风险。

24个世界的120项字段精确比较全部一致。24项候选选择概率质量归一化通过。原正式H=3六世界结果全部重现。篡改新增R收据的selected_brier会被B脚本检出；篡改原六世界选模概率会因归一化失败被检出。两项负对照均已执行。

机读收据 research/evidence_audit/B_R202_HORIZON_TRANSPORT_120_EXACT_AUDIT_RECEIPT_2026-10-27.json 固定输入Git blob身份和检验结果。

B轨验证的是同一研究主体内不同算法的程序性复核。人工训练与新测试独立由冻结生成机制保证。未完成真人样本外预测、真实概率校准、删失偏差评估、外部研究者独立复现。E1内部有限通过，新增E2预测=0、E3预测=0、外部复现=0。原R202验收不变。R073和PESEN v0.1继续冻结。没有主动运行可能产生费用的GitHub Actions。
