# B轨 R191二元后验预测与新群迁移独立科学审计

日期：2026-10-26。状态：PASS_BOUNDED_INTERNAL_E1_DIFFERENT_ALGORITHM。

审计依据：计算前冻结协议 protocols/R191_BINARY_EVENT_PREDICTIVE_CALIBRATION_24_POSTSCORE_FREEZE_2026-10-26.md，冻结提交 0e9191bb50a45bf8b86c52c1b4e507739c0fd4f3。原R191 24世界生成参数从 research/R191/R191_EXACT_RESULTS.json 读取，原始结果Git blob 31f3cb89bbe502640f78407bb68c564d4701f95a。

B程序 research/evidence_audit/b_r191_binary_event_histogram_20261026.js 不读取R主程序、不读取原1136个可见后验profile。按U=±τ、三点误差分布构造潜在条件似然，以直方图频数和多项式重数合并相同可见观测，独立计算 S=((a_plus−a_minus)^2/8)Σ_h (L_plus−L_minus)^2/(L_plus+L_minus)，其中L含多项式重数，零分母项跳过。总计308个非零直方图配置。

每世界比较先验事件概率、同群Bayes Brier、同群全局Brier、同群收益、新群正确Brier、新群错误复用Brier，共24×6=144个精确有理数字段，全部一致，0差异。各世界直方图总概率严格为1。

事前负对照：把同群后验Brier错误用于独立新群；16个S>0世界均与正确新群风险严格不同，8个τ=0世界保持无差异。该负对照检出16项预期错误。未对新数据调参或改变冻结评分。

主要风险边界：数据生成参数和新群独立性均为人工已知；新群迁移Brier以独立U为前提；后验预测使用完整原始训练信息且不接触未来标签。尚无外部人类样本、概率校准曲线、真实群组留出或外部团队复现。新增E2=0，E3=0。R073与PESEN v0.1未修改。未主动启动Actions，远端CI PASS尚未确立。主动新增费用0，账户实际费用未核验。
