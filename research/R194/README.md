# R194 马尔可夫链：一阶与二阶记忆的观测等价及留出轨迹预测

2026-10-21，原239候选目录P1/08-018 Markov Chains。科研等级 **CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_MARKOV_CHAIN_ORDER**。

[事前冻结协议](../../protocols/R194_MARKOV_24_WORLDS_2064_TRAJECTORIES_PRESCORE_FREEZE_2026-10-21.md)固定六个二元状态过程：IID（一步保持率1/2）、SWITCH（1/4）、PERSIST（3/4）、STICKY（7/8）、LAG2_SWITCH（二步保持率1/4）、LAG2_REPEAT（二步保持率3/4）。轨迹长度L=3/4、彼此独立训练轨迹m=1/2，共**24人工来源世界、2064套原有序训练轨迹集及196种无序等价完整候选拟合配置**。所有来源完整路径概率由直接按序转移概率与独立前缀状态动态生成两套Fraction算法完全相等，转移事件完整Counter频数法与逐次路径似然一致，所有真实人工训练轨迹组概率严格和1。候选选择固定原始IID→SWITCH→PERSIST→STICKY→LAG2_SWITCH→LAG2_REPEAT最优有理数似然，平局取第一个。

预冻结数学识别反例：所有六源任意时刻P(X=1)=1/2；两种二步源与真正一阶IID全部相邻状态组合(00,01,10,11)各概率1/4，即**单时与相邻时点分布完全一样，但二步源后续状态对前两步有依赖**。对于真LAG2_REPEAT，知道真正二阶条件转移的未来独立新轨迹最后一步Brier=3/16=0.1875、logloss≈0.562335；只用IID候选Brier=1/4=0.25、logloss≈0.693147。模型于**短训练样本最大似然拟合**则可能更差：L3训练m2时真LAG2_REPEAT模型被选中概率9/32≈28.125%，拟合模型期望新轨迹末步Brier≈0.296143，反而高于永远预测IID的0.25；真IID同条件平均Brier≈0.317383，反映极短样本过拟合风险。严禁把人工oracle规律与真实识别成功或真人长记忆证据混淆。

[正式科学报告](R194_SCIENTIFIC_REPORT_2026-10-21.md)、[24世界完整概率与留出评分JSON](R194_EXACT_RESULTS.json)、[2064组原轨迹训练CSV](R194_ALL_2064_ORDERED_TRAINING_TRAJECTORY_SETS.csv)、[196候选精确拟合库](R194_ALL_196_MARKOV_FIT_PROFILES.json)、[机器验收](R194_FINAL_MACHINE_ACCEPTANCE.json)、[代码与33项单测](r194_exact_binary_markov_order.py)、[源码协议全部结果ZIP](R194_24_Exact_Markov_Trajectory_Worlds.zip)已永久归档。[GitHub Actions39583695440](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39583695440) Python3.11/3.12各33项单测共66次及真实完整轨迹风险评分和全部CSV/ZIP归档三个job全success，[结果提交37c8bf0b](https://github.com/edwardsage419/Psychohistory-Research/commit/37c8bf0b6890074183841cc2f697dc937a9b9b01)。

一手背景：[Kemeny/Snell1960](https://link.springer.com/book/9780387901923)、[Anderson/Goodman1957](https://doi.org/10.1214/aoms/1177707039)。只有E1人工链条研究，新增真人E2及外部历史E3均0；R073与PESEN v0.1冻结。下一 **R195 P1/08-019 Markov Chain Monte Carlo**；全R先完成、之后统一归纳分类、最后熔炼。
