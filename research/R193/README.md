# R193 有限混合模型：24人工世界的前两阶矩不可识别与第三阶识别

日期2026-10-21，原239目录P2/08-017 Finite Mixture Models。正式状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_FINITE_MIXTURES**。

[计算前冻结协议](../../protocols/R193_FINITE_MIXTURE_24_WORLDS_512_TABLES_PRESCORE_FREEZE_2026-10-21.md)先于源码/评分进入main。四个固定混合概率候选IID、对称S、非对称A、宽对称W × 每群n=1/2/3次条件独立二元试验 × 独立训练群组m=2/3，组成**24个人工世界、512个完整有序训练样本、53种唯一拟合配置**。固定候选同训练似然并列按IID→S→A→W选择，所有二项来源的完整计数PMF通过封闭组合和逐事件DP两个独立Fraction算法逐格完全一致；原始训练likelihood通过逐群乘积与组数Counter频数幂两法一致。对独立新群组积分其全新潜在成功率后的全部K值评分，由math.log和60位Decimal.ln交叉验证。训练样本与新群组完全独立。

**冻结关键反例**：S把(1/4,3/4)两潜在成功率各赋权1/2；A把1/3与7/8分别赋权9/13与4/13。两者真`E(Q)=1/2`、`Var(Q)=1/16`，n1/n2全部成功次数PMF完全相同，n2时P(K=0,1,2)=(5/16,3/8,5/16)，可见数据不能区分。尽管如此，同一K=1的真实高成功率潜在成分类别后验，S为1/2、A为7/39，只有人工真潜在标签下才有意义。n3时第三中心矩S为0而A为5/384，K3=3的完整概率从S的7/32改为A的89/384；**新的群内观测可以提供模型识别信息，但有限训练样本并不保证正确选中候选**。当n2,m2时S和A均选择IID概率39/64、W概率25/64，S/A均不被选；n2,m3时选择IID81/256、S225/512、W125/512，两源的全部模型选择概率及独立新群组预测风险完全相同。真实标签oracle Brier与可观察新群组预测分开记录，IID双标签仅是一种无语义的计算表达。

[正式科研报告](R193_SCIENTIFIC_REPORT_2026-10-21.md)、[全部24世界精确结果](R193_EXACT_RESULTS.json)、[512条完整人工原始训练CSV](R193_ALL_512_ORDERED_TRAINING_TABLES.csv)、[53组完整候选似然库](R193_ALL_53_EXACT_MIXTURE_FITS.json)、[机器科研验收](R193_FINAL_MACHINE_ACCEPTANCE.json)、[源程序与37项单测](r193_exact_finite_binomial_mixture.py)、[包含冻结协议和全量源码数据ZIP](R193_Exact_Finite_Mixtures_24_Worlds.zip)均永久归档。[GitHub Actions39582534746](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39582534746) Python3.11/3.12各37项测试共74次通过及第三job全部512源表/53配置/档案SHA三job成功，[原机器数据提交283dab77](https://github.com/edwardsage419/Psychohistory-Research/commit/283dab77aaaee649db074cf5cfeab7acd711063e)。

来源：[Teicher1963](https://doi.org/10.1214/aoms/1177703862)、[Lindsay1995](https://doi.org/10.1214/cbms/1462106013)。仅E1人工数学结题，新增真人E2、外部历史E3均0，R073及PESEN v0.1冻结。下一 **R194 P1/08-018 Markov Chains**；原既定全部R完成后才统一分类、再熔炼。
