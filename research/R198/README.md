# R198 状态空间模型：准确隐藏状态滤波、传感器噪声与末次观测缺失

2026-10-21。原239目录P1/08-022 State Space Models。科研状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_DISCRETE_STATE_SPACE**。

[计算前冻结协议](../../protocols/R198_STATE_SPACE_32_WORLDS_576_VISIBLE_HISTORIES_PRESCORE_FREEZE_2026-10-21.md)固定二元隐藏真实状态X，初始公平、每步保持率a∈{1/2,3/4,1/4,11/18}，二元传感器Y在真X条件下独立发射且正确率r∈{3/4,7/8}；两种观察T4/5，及FULL全观测或LAST_MISSING末尾Y_T确定性未观测，得到**32个人工来源世界、576个全部可见人工训练历史及2304项四候选真正新观测Brier风险**。两套完整独立的Fraction概率模型分别使用原生前向隐藏滤波与穷举2^(T+1)条隐藏状态原始路径，全部可见历史证据、末状态后验及下一期真观测概率完全一致；时间T−1的真实后向平滑由前向状态质量×末期观测likelihood独立计算，和全隐藏路径穷举的真正平滑结果逐Fraction一致。末期传感器缺失时，前缀样本来源概率等于完整观测两个Y_T结果的概率总和、后向平滑不额外更新历史状态，已见信息传播到下一期时也不会被当作新观测。

**识别正负例**：全部源单时观测P(Y=1)=1/2；A机制a3/4、r3/4与B机制a11/18、r7/8的观测相邻lag1协方差都1/32，但lag2分别1/64与1/144，故仅凭相邻观测联合分布无法判断隐藏状态保持性与观测测量质量。对每个世界完整PMF独立汇总的lag1、lag2与公式`Cov(Y_t,Y_{t+k})=(2a−1)^k(2r−1)^2/4`逐Fraction相同。对真a1/2时无条件、全历史、最新传感器或把观测当真隐藏状态四种预测均返回1/2、Brier1/4。对真a3/4、r7/8、T5时，FULL的真正下期观测Brier：全部历史滤波0.229116、只用最新传感器0.230225、把测量误当状态0.232422、无历史0.25；同样情景遮蔽最后Y5后最优滤波风险约0.244779。完整32世界都保留，严格仅限人工有限state space，不声称高斯Kalman滤波或真实社会状态已被识别。

[正式科研报告](R198_SCIENTIFIC_REPORT_2026-10-21.md)、[32世界全部原风险JSON](R198_EXACT_RESULTS.json)、[576原始人工可见历史/后验/四预测结果CSV](R198_ALL_576_EXACT_VISIBLE_HISTORIES.csv)、[8状态-噪声配置精确跨期相关库](R198_ALL_8_LATENT_OBSERVATION_MOMENT_DIAGNOSTICS.json)、[正式机器验收](R198_FINAL_MACHINE_ACCEPTANCE.json)、[原生源码与41单测](r198_exact_discrete_state_space.py)、[含原计算前协议及全部结果六文件ZIP](R198_32_Exact_Discrete_State_Space_Worlds.zip)均已永久归档。[GitHub Actions39590183957](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39590183957) 双Python各41单测共82次及第三job真正完整576源/2304未来风险与SHA/ZIP归档三job成功，[原结果提交64356846](https://github.com/edwardsage419/Psychohistory-Research/commit/64356846ec5271f182c1c1739e21b9e4c8d2f2f1)。

理论依据：[Kalman1960](https://doi.org/10.1115/1.3662552)状态空间思想、[Rabiner1989](https://doi.org/10.1109/5.18626)离散隐状态滤波。仅人工E1，真人E2、历史E3新增0，R073和PESEN v0.1不变。下一 **R199 P2/08-023 HMM Time Series**；全R完成后归纳分类，最后熔炼。
