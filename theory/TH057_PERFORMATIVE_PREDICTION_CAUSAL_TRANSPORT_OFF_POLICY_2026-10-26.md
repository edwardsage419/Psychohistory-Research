# TH057 策略干预、预测反馈、因果可迁移性与离策略评价

研究及检索日期：2026-10-26（Asia/Shanghai）。状态：THEORY_NOTE_BOUNDED。研究轨道：纯理论；与 R 系列拟合复现、真人实证、商业产品分析分离。C003 今日与 D002 本周已完成，本轮只读。来源仅限英文原始出版网站及英文作者公开稿。没有个人敏感数据、收费资源、主动 CI 或产品开发。

## 一、原始书目与审读等级

A 表示已直接审读开放原文的指定章节、公式或定理；B 表示仅核对摘要或原始书目；M 表示本项目独立人工反例。原作研究结果与本项目计算不得混称。

1. [A1] Perdomo, Juan C., Tijana Zrnic, Celestine Mendler-Dünner & Moritz Hardt (2020). “Performative Prediction.” *Proceedings of the 37th International Conference on Machine Learning*, PMLR 119:7599–7609. 出版页 https://proceedings.mlr.press/v119/perdomo20a.html ；原刊 PDF https://proceedings.mlr.press/v119/perdomo20a/perdomo20a.pdf 。直接审读 pp.1–6 的分布映射、performative risk、stable fixed point、Theorem 3.5、Proposition 3.6 与实验性质说明。PMLR 页面未列正式 DOI；以原刊编号为准。作者半合成案例中的分布响应由模型构造，不能视为现实制度的独立因果验证。
2. [A2] Miller, John P., Juan C. Perdomo & Tijana Zrnic (2021). “Outside the Echo Chamber: Optimizing the Performative Risk.” *Proceedings of the 38th International Conference on Machine Learning*, PMLR 139:7710–7720. 出版页 https://proceedings.mlr.press/v139/miller21a.html ；原刊 PDF https://proceedings.mlr.press/v139/miller21a/miller21a.pdf 。直接审读 pp.1–4 的 stable/optimal 区别、Proposition 2.1、mixture dominance 与 Theorem 3.1。论文给出在明确结构条件下的凸性保证；不能推广为所有现实策略系统。
3. [A3] Pearl, Judea & Elias Bareinboim (2014). “External Validity: From Do-Calculus to Transportability Across Populations.” *Statistical Science* 29(4):579–595. DOI https://doi.org/10.1214/14-STS486 。作者公开版本 https://arxiv.org/pdf/1503.01603 （2015 年上传，正文标明 2014 年正式刊文）。直接审读 pp.6–12 的 Example 1/2、selection diagram Definition 4/5、Theorem 1 与直接可迁移性判据。原文的图结构与机制不变性属于识别假设。
4. [A4] Jiang, Nan & Lihong Li (2016). “Doubly Robust Off-policy Value Evaluation for Reinforcement Learning.” *Proceedings of the 33rd International Conference on Machine Learning*, PMLR 48:652–661. 原刊 https://proceedings.mlr.press/v48/jiang16.html ；PDF https://proceedings.mlr.press/v48/jiang16.pdf 。直接审读 pp.1–4 的有限时域设定、行为策略、累积权重、式(10)的 DR 递推及 Theorem 1 方差分解。该定理的无偏性依赖行为概率、覆盖及相关序贯假设；并非对任意隐藏混杂均有效。
5. [A5] Kallus, Nathan & Masatoshi Uehara (2020). “Double Reinforcement Learning for Efficient Off-Policy Evaluation in Markov Decision Processes.” *Journal of Machine Learning Research* 21(167):1–63. 原刊 https://www.jmlr.org/papers/v21/19-827.html ；PDF https://www.jmlr.org/papers/volume21/19-827/19-827.pdf 。直接审读 pp.1–5 的问题设定、sequential overlap Assumption 1、bounded reward Assumption 2 及作者摘要中的 cross-fitting、Q 函数和边际密度比；其余长篇证明及实验尚未逐页审读。
6. [B6] Hardt, Moritz & Celestine Mendler-Dünner (2025). “Performative Prediction: Past and Future.” 作者机构介绍 https://tue.ellis.eu/publications/hardt2023performative 。仅核验作者机构摘要，作为理论储备；不把综述当作独立实证。

所有检索时间为 2026-10-26。A1/A2/A4/A5 原始出版网站均为 PMLR 或 JMLR；A3 为作者公开原刊版本。无付费论文访问。

## 二、核心命题、前提、竞争解释与反例

| 编号 | 命题及作用机制 | 前提、竞争解释和限制 |
| --- | --- | --- |
| P01 | 预测一经用于决策，模型参数可通过行动影响未来数据分布 D(θ)；静态训练分布上的预测误差不能直接代表部署后表现。[A1] | 必须实际存在模型到行动再到结果的通道。外生冲击、测量变化、采样选择亦可造成漂移；只凭前后分布不同无法确认 performativity。[M6] |
| P02 | performative stability 是给定自身诱导分布后的再训练固定点，performative optimality 最小化部署所诱导的风险 PR(θ)。[A1,A2] | 两者优化问题不同。只有附加结构条件才能限制差距；人工平滑反例展示稳定点的风险仍可较高。[M1] |
| P03 | 在损失联合平滑、强凸与分布映射足够低敏感的条件下，重复风险最小化收敛到稳定点。[A1 Theorem 3.5] | 原文条件包含 ε<γ/β；放松任一条件可能出现不收敛反例。[A1 Proposition 3.6]；这不保证现实社会动力学稳定。 |
| P04 | 稳定点可能具有较差的 performative risk；Miller 等给出强凸损失下稳定点甚至为风险最大点的构造。[A2 Proposition 2.1] | 原作者为数学存在性构造；风险目标是建模者指定的损失，社会福利和公平需要另外评价。 |
| P05 | 源总体与目标总体的因果效应可在选择图中规定的机制不变性下重加权或通过 do-calculus 迁移。[A3] | 需要因果图、目标总体变量分布及足够的识别信息；代理变量变化可能破坏按层迁移。[A3 Example 2,M5] |
| P06 | 历史行为策略与目标策略不同，可用 importance sampling 对轨迹分布差异加权。[A4] | 目标策略支持集必须被历史行为策略覆盖，权重随时域累乘可能造成巨大方差。[M2,M3] |
| P07 | 序贯 doubly robust 估计结合模型价值预测和行为概率加权残差，在论文的可识别设定下可保持无偏并降低部分方差。[A4 Eq.(10), Theorem 1] | 行为概率错误与价值模型错误同时出现会导致偏差；即使价值模型准确，状态转移与奖励随机性仍贡献方差。[M4] |
| P08 | 使用交叉拟合的 Q 函数与边际密度比可在 Markov 设定下改善 OPE 的统计效率。[A5] | 原文 Assumption 1 要求 sequential overlap；隐藏状态、非平稳制度、无界奖励或不满足 Markov 性时保证不能直接套用。 |
| P09 | 离策略估计的统计无偏性无法单独消除未观测混杂、错误奖励定义或跨制度迁移偏差。[A3,A4,A5,M2] | 需要明确序贯可交换性、观察口径、策略记录与干预对象；不能由高拟合分数反推因果识别。 |
| P10 | 政策部署可能同时改变行为策略、观测机制和奖励结构，三种变化在汇总数据中可能混合。[A1,A3,M6] | 区分外生漂移、行为反应和政策改变，需记录制度版本、执行强度、干预时点与可比较的反事实。 |
| P11 | 不同个体之间的网络干扰可使独立个体 OPE 的稳定环境假设失效；群体反馈须明确处理单元与干扰范围。[A1 的反馈框架及本项目推断] | 属方法外推警示，未由本轮直接实证验证。应比较部分干扰、网络暴露映射和群体层随机化候选方案。 |
| P12 | 预测误差、因果政策价值、社会福利、群体公平及长期制度影响应使用不同目标与独立评分。[A1,A2,A3,A4] | 权重和目标本身涉及价值判断；不存在无需主观前提的普适唯一最优人生。四层历史外推须单独验证。 |

## 三、六项独立人工数学反例（M，不是原作者数据）

**M1：稳定点与部署风险最优点分离。** 人工设定 θ∈R，部署结果 y=0.5θ+1，损失 ℓ(y;φ)=(φ−y)^2+φ²。固定旧部署 θ 时的再训练最优解 G(θ)=(0.5θ+1)/2；固定点 θ_PS=2/3。部署风险 PR(θ)=(0.5θ−1)^2+θ²，直接求导得 θ_PO=0.4。PR(2/3)=8/9≈0.888889，PR(0.4)=0.8，差 4/45≈0.088889。映射平滑且损失强凸，收敛固定点仍与部署风险最优点不同。这是本项目自造例，区别于 A2 原作者 Proposition 2.1 的反例。

**M2：零覆盖使反事实价值不可识别。** 只有 X=0 时行为策略执行 a0，X=1 时执行 a1。日志中永远没有 (X=0,a1)。世界 W0 与 W1 在所有已观察 (X,a) 的奖励分布完全一致；对缺失组合，W0 设 E[R|X=0,do(a1)]=0，W1 设为1。目标策略在 X=0 选择 a1 时，两世界价值不同。无额外干预或结构假设，日志不能识别该目标策略价值。

**M3：低覆盖的重要性权重方差。** 单步目标策略必选 a1，行为策略以概率 p 选 a1，a1 奖励恒为1。单次 IS 估计以概率 p 为 1/p，否则为0；期望1、方差1/p−1。p=0.05 时方差19，100条独立日志的均值方差0.19、标准差约0.435890；p=0.5 时方差1，100条均值标准差0.1。若奖励随机或多步，方差结构更复杂。

**M4：双重稳健性有前提。** 单步 a1 真正均值0.8，目标策略必选 a1，模型预报 qhat=0.5，实际行为选择概率 p=0.2。用 DR=0.5+I(a1)/0.2×(R−0.5)，其期望0.8。若真实 p=0.1 而错误地仍以0.2加权，期望变为0.65。若价值模型恰好正确 qhat=0.8，尽管上述行为概率错报，期望仍为0.8。这说明“稳健”有指定模型正确性与识别条件，不能用于缺乏覆盖的状态。

**M5：总体结构改变使因果效应迁移错误。** 人工设两个层 z0、z1，假定层内因果效应在源与目标之间恒定，分别为0.1、0.5。源总体 P(z1)=0.2，源平均效应0.18；目标 P*(z1)=0.8，目标平均效应0.42。直接搬用源总体结果误差为−0.24。按目标构成重加权可得0.42，但需要层内效应不变及目标层比例可观测。

**M6：仅观察一次部署无法识别模型的政策效果。** 仅有 θ=1 部署后的结果 P(Y=1)=0.6。世界 A 在 θ=0 时概率0.2，部署效果+0.4；世界 B 在 θ=0 时概率0.6，部署效果0。两世界在已观察部署下数据相同。需要外部实验、有效自然实验、可辩护结构模型或额外观测，才能估计部署效果；前后变化亦可能含时间冲击。

所有数值由代数独立推导并做数值核算；不作为原作者论文实验复现，也不作为真人历史数据的因果证据。

## 四、跨四层连接与竞争理论

个体层：预测影响个人行动、信息搜寻与策略调整。竞争机制包括真正偏好变化、选择性披露、观测误差和对激励的短期反应。认知机制无法由部署后的预测准确率单独识别。

群体层：信息传播、模仿、网络干扰与他人策略可能改变 D(θ)；目标策略价值受互动对象及覆盖率影响。需要区分独立行动者假设与网络暴露条件。

制度层：规则、执行者、资源配置与绩效指标共同决定行动可行集及结果记录。预测性治理可能造成指标迎合、测量口径变化与政策反馈；理论上须区分模型参数干预、实际政策执行和组织响应。

历史层：跨年代的目标总体构成、制度版本、技术与环境冲击可能同时变化。选择图的机制不变性应作为可审计假设；长期事件不可重复时，保持多情景与部分识别，不宣称具体历史或未来事件由本轮模型确定。

竞争方法比较：静态监督学习适用于近似固定的决策环境；performative prediction 显式允许部署反馈；因果 transportability 解决跨总体因果效应迁移；OPE 解决在充分支持与识别条件下用旧策略日志评估新策略。四者研究对象不同，不能用其中一个框架的理论保证替代其他框架的前提审计。

## 五、候选验证与失败标准

1. 预先冻结目标：部署后的预测 proper score、performative risk、政策净收益、群体分配指标分别报告；主观福利权重公开记录且进行敏感性分析。
2. 画出模型 θ → 决策 a → 行为与环境 → Y 及观察/失访机制的候选因果图，列出可能的隐藏共同原因、网络干扰和版本断点。
3. 先查各状态动作组合的支持集及有效样本量；零覆盖直接标记 NOT_IDENTIFIED，不用 DR 或深度模型补成“有证据”。
4. 比较静态模型、重复再训练、显式反馈模型、直接 performative risk 优化、重要性采样、序贯 DR、交叉拟合 DRL；统一信息集、成本和时间窗。
5. 对跨实验、跨人口、跨制度时期的迁移，分别检查层内因果机制不变性、目标总体组成、测量一致性及选择图假设。无足够识别时只给界限或情景。
6. 采用主体/场次/制度时间块完整留出，事前冻结模型与评分；报告长期反馈下校准、覆盖、尾部损失和敏感性，不从样本内拟合断言机制。
7. 原作者的半合成实验、理论定理和本项目人工反例分别归档；未来若获得真实数据，另开独立实证轨道验证，禁止借理论笔记冒充验收。

## 六、研究边界、日历与下一项

本轮开放原始研究直接审读5份指定章节，综述摘要核验1份。新增数学反例6项；真人数据复算0、独立预测0、因果估计0、R系列模型熔炼0。原作者论文的实验与理论证明未由本项目独立重跑。无新增费用、无主动 GitHub Actions。

C003 2026-10-26 已完成 MNAR 缺失与纵向敏感性研究，本轮只读。D002 2026-W44 已完成工业电气化与制度适应，本轮只读。R系列最新记录按本轮写入前 main 核验，不占用其验收路径。

下一轮 TH058：战略分类、Goodhart/Campbell 指标反馈与制度性激励的可识别边界。优先核对 Goodhart 1975 原作、Campbell 1976/1979 原作、Hardt 等 2016 strategic classification 原作及对抗性反馈的实证证据。保留全部 R 系列完成后再统一分类和模型熔炼的既定顺序。
