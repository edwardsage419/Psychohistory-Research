# R074: 冻结第二独立真人重复博弈来源的资格门

2026-10-17。R073 的 E2 真人内部留场次结果已归档，E3 外部实验验证仍为 OPEN。本协议于任何第二数据集的 R073 模型评分之前冻结。

## 无条件保留的 R073 比较规则

- 预测目标：个人在第 t 轮合作 C=1/背叛 D=0。teacher-forced，即前一轮真实且当时可见的历史可以用作特征；绝不使用本轮或未来结果。
- 同一局内使用 own(t-1)、opponent(t-1)、own(t-2)、opponent(t-2)。禁止跨 supergame 拼接历史。只有 t>=3 且完整历史的所有共同目标可进入评分。
- 固定七族 M0、M1(own last)、M2(opponent last)、M3(joint last)、M4(joint two lags)、M5(TFT)、M6(WSLS)，按 R073 冻结协议原定义。条件概率 (n_C,state + 20*p0)/(n_state+20)，p0 仅来自训练集中同处理的其他完整实验场次；M5/M6 固定误动作概率 0.05。
- Brier 为主要、log loss 为次要得分。对全部七族使用完全相同的留出目标，逐实验场次先算平均，再对场次等权平均。主要配对比较 M3-M1 与 M4-M3，展示每场胜负计数，允许负结果。
- R073 中每处理6场、其余5场训练及每人100轮是**该实验的样本结构**。不同实验不可伪造为12场/100轮。若真实来源的实验分层、局长或轮次不同，应在评分前声明外部传输规则，维持整场留出、同处理其他真实场次训练及 t>=3 同一共同风险集；任何变化必须单独报告，不能谎称严格相同样本设计。

## 来源审核 G1/G2/G3

G1：独立研究团队与真实受试者；原作者论文、原始实验数据、文档及固定哈希可核验。第三方加工包的数据不能冒称一手原始数据。

G2：逐人、逐局、逐轮的本人 C/D 和真实当时可观察的历史对手 C/D 可核对。区分选择意图与实际执行动作，尤其处理动作噪声。局之间禁止计算连续滞后。

G3：能够独立确定真实实验 session、处理标签及参与者是否重叠，完整 session 从训练中移除。参与者 ID、supergame ID 不得临时重命名成 session 代替独立实验单位。缺少原始 session 映射一律阻塞正式 E3 场次留出结果。

## 已找到的两项独立候选及精确二级来源

A. Dal Bó 与 Fréchette (2011), AER DOI 10.1257/aer.101.1.411，原作者复现 openICPSR DOI 10.3886/E112401V1。二级核查镜像 `cran/stratEst` Git commit `a6373b23d80dc816a63f18f973d372c9e8421914`，`data/DF2011.rda` Git blob `52e216b02e1a7ab7fb1a6e335b5f7e2ef6b7f5a0`。文档7358行，六字段 treatment,id,game,period,choice,other.choice；未列 session。原始作者数据列表中有 Stata 资料及 session 分析脚本，尚未核对原始 session 值。

B. Fudenberg、Rand 与 Dreber (2012), AER DOI 10.1257/aer.102.2.720，原作者复现 openICPSR DOI 10.3886/E112512V1。二级同镜像 `data/FRD2012.rda` Git blob `6b196ca1624081850b41dc2084c762257d59dd8f`。文档13126行，九字段 treatment,id,game,period,choice,last.choice,last.other,bc,error；未列 session。噪声处理下 intended/realized 语义需单独核实。

目前只授权**两个二级来源的精确文件一致性、字段、场次缺口、有效连续历史审计**，不授权用它们尝试训练M0..M6。未通过G1/G2/G3不得发表E3分数。不保存人类原始行、具体ID、逐人轨迹、细场分数。R073原有E2结果与PESEN v0.1均保持冻结。

`R074_SECOND_SOURCE_GATE=FROZEN_BEFORE_MODEL_SCORING`；`R073_E3=OPEN`；`PESEN_v0.1=FROZEN`。
