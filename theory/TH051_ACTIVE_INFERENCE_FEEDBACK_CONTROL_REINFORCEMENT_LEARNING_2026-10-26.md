# TH051 主动推断、最优反馈控制与强化学习：目标函数、信息价值及可区分预测

日期及英文来源检索日：2026-10-26（Asia/Shanghai）。状态：THEORY_NOTE_BOUNDED。研究范围为纯理论与方法审计。与R系列拟合复现、实证数据搜集及商业分析分轨；C、D按日历核验后只读。

## 一、原始书目、链接、阅读等级及版本

A为本轮直接审读公开原文指定章节；B为原作书目与摘要核验；M为本项目独立数学构造。所有资料均为英文来源，检索日期2026-10-26。

1. [A] Todorov, Emanuel & Michael I. Jordan (2002). “Optimal Feedback Control as a Theory of Motor Coordination.” *Nature Neuroscience* 5:1226–1235. DOI https://doi.org/10.1038/nn963 。作者实验室公开正式原刊PDF https://roboti.us/lab/papers/TodorovNatNeurosci02.pdf 。直接审读pp.1226–1229的最小干预、信号相关噪声、冗余方向及成本函数推导。后续实验的底层数据尚未复算。
2. [A] Friston, Karl J., Jean Daunizeau & Stefan J. Kiebel (2009). “Reinforcement Learning or Active Inference?” *PLOS ONE* 4(7):e6421. DOI https://doi.org/10.1371/journal.pone.0006421 。正式开放原刊 https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0006421 。直接审读Introduction、Methods及mountain-car演示。此文为模型计算演示，不能冒充跨任务真人验证。
3. [A] Friston, Karl & Ping Ao (2012，2011在线发表). “Free Energy, Value, and Attractors.” *Computational and Mathematical Methods in Medicine* 2012:937860. DOI https://doi.org/10.1155/2012/937860 。开放原刊 https://onlinelibrary.wiley.com/doi/10.1155/2012/937860 。直接阅读Introduction、Ensemble Dynamics、Markov blanket相关模型假设。
4. [A] Sajid, Noor, Philip J. Ball, Thomas Parr & Karl J. Friston (2021). “Active Inference: Demystified and Compared.” *Neural Computation* 33(3):674–712. DOI https://doi.org/10.1162/neco_a_01357 。UCL作者稿 https://discovery.ucl.ac.uk/id/eprint/10119277/ ；原作者预印稿可读全文 https://ar5iv.labs.arxiv.org/html/1909.10863 。直接审读Introduction、RL对比及认识价值段落。预印稿与2021正式排版未逐页校勘；作者明确表示FrozenLake是概念演示，比较器不包含全部RL方法。
5. [A，预印稿] Millidge, Beren, Alexander Tschantz, Anil K. Seth & Christopher L. Buckley (2020). “On the Relationship Between Active Inference and Control as Inference.” arXiv:2006.12964，https://ar5iv.labs.arxiv.org/html/2006.12964 。直接阅读Formalism、Control as Inference、Active Inference概率推导。独立同行评审状态未核实。
6. [B] Friston, Karl, Spyridon Samothrakis & Read Montague (2012). “Active Inference and Agency: Optimal Control Without Cost Functions.” *Biological Cybernetics* 106:523–541. DOI https://doi.org/10.1007/s00422-012-0512-8 。开放出版社页面 https://link.springer.com/article/10.1007/s00422-012-0512-8 。本轮核验原刊摘要，正文PDF未成功提取。作者在摘要中明确指出奖励与成本被吸收到状态转移和终态先验。
7. [B] Da Costa, Lancelot, Thomas Parr, Noor Sajid, Sebastijan Veselic, Victorita Neacsu & Karl Friston (2020). “Active Inference on Discrete State-Spaces: A Synthesis.” *Journal of Mathematical Psychology* 99:102447. DOI https://doi.org/10.1016/j.jmp.2020.102447 。UCL开放正式版本 https://discovery.ucl.ac.uk/id/eprint/10115398/ 。书目与摘要已核，全文下载本轮超时。
8. [B] Todorov, Emanuel (2009). “Efficient Computation of Optimal Actions.” *PNAS* 106(28):11478–11483. DOI https://doi.org/10.1073/pnas.0710743106 。原刊 https://www.pnas.org/doi/10.1073/pnas.0710743106 ，作者书目 https://roboti.us/lab/papers.html 。只核摘要，关于线性可解控制的结论须限制在论文所述结构化问题。

## 二、十项命题、前提、机制、竞争解释、反例与边界

**P01 最优反馈可保留任务无关方向的变异。** 前提：任务目标、状态动力学、运动噪声及努力成本明确。机制：仅纠正影响任务结果的偏离，其他方向允许变化。来源[A] Todorov & Jordan 2002 pp.1226–1229。竞争：目标轨迹跟踪及动态系统自组织。反例：任务要求每个状态分量精确到达指定值时冗余消失。边界：运动控制结果无法直接证明人生或历史决策机制。

**P02 最优反馈的结果依赖事先给定的成本。** 前提：终点误差、动作代价、传感噪声和约束均有独立依据。机制：成本到达函数决定反馈增益。来源[A] Todorov & Jordan 2002 pp.1227–1229。竞争：固定轨迹控制、简单启发式。反例：改变努力权重即可改变最优动作。边界：作者明确将神经实现和学习算法视为独立问题。

**P03 主动推断使用偏好先验引导行动。** 前提：有可描述的观测、隐藏状态、状态转移与偏好分布。机制：行动使预期观测符合生成模型中的偏好。来源[A] Friston et al. 2009；[B] Friston et al. 2012。竞争：显式奖励最大化。反例：偏好先验完全事后设定时可以解释多种选择。边界：数学可写成推断不等于神经系统必然执行同样计算。

**P04 “没有成本函数”仍需要价值来源。** 前提：目标终态、轨迹先验或偏好概率被约束。机制：成本可编码成负对数偏好或转移概率。来源[B] Friston et al. 2012摘要；[A] Friston & Ao 2012。竞争：外显效用函数。反例：未知先验与未知奖励可相互替代，选择行为难以识别。边界：价值编码位置变化不会消除主观权重。

**P05 主动推断与强化学习可能预测同一政策。** 前提：允许匹配策略温度、奖励与偏好映射及状态模型。机制：对数偏好与奖励可在特定条件下互相重参数化。来源[A] Friston et al. 2009；[A] Millidge et al. 2020。反例：模型行为相同，成功率无法确定认知机制。边界：此处为条件性等价，不能推断全部算法等价。

**P06 认识价值能够影响行动选择。** 前提：可通过行动获取关于隐藏状态的额外信息。机制：预期自由能目标可以包含预期信息增益。来源[A] Sajid et al. 2021作者稿；[A] Millidge et al. 2020。竞争：贝叶斯自适应RL、双重控制、内在动机RL同样能够探索。反例：若信息无后续决策价值，仍持续探索的原因需要另行识别。边界：探索行为本身不足以唯一支持主动推断。

**P07 RL比较须明确算法类别。** 前提：对比模型共享观测、动作集合、计算预算、训练数据与规划时域。机制：模型自由RL、模型基础RL及Bayes-adaptive RL的可用信息不同。来源[A] Sajid et al. 2021作者稿。反例：只比较Q-learning可能高估主动推断的相对优势。边界：FrozenLake示范不能代表全体RL方法。

**P08 Control as Inference与Active Inference都可把行动写为概率推断。** 前提：POMDP、策略先验与概率目标均已定义。机制：前者常引入最优性变量，后者在观测偏好中编码价值。来源[A] Millidge et al. 2020 §1–3。竞争：最大熵RL、KL控制。反例：两种模型的策略概率完全相同。边界：需逐式对齐不同作者的自由能符号和归一化假设。

**P09 机制确认需要过程指标和干预。** 前提：反应时间、信念、反馈增益或神经响应具有预先指定的观测模型。机制：扰动任务相关维度和冗余维度，比较不同控制器的纠正行为。来源[A] Todorov & Jordan 2002；[A] Sajid et al. 2021。反例：仅有终点正确率不能区分内部目标。边界：过程指标仍可能混杂，需预注册和跨任务留出。

**P10 “最优”始终依赖环境与偏好条件。** 前提：动力学、信息约束、风险权重、偏好变化和成本已定义。机制：环境漂移可改变动作排名。来源[A] Friston & Ao 2012；[A] Todorov & Jordan 2002；[M] 本项目推论。反例：错误模型与非平稳环境会使理论最优行动失败。边界：不支持普适唯一最优人生。

## 三、五项人工数学反例（M，全部独立构造）

**M01 奖励与偏好选择等价。** p(A)=0.8、p(B)=0.2，按偏好抽样得P(A)=0.8。软最大化温度1、奖励r(A)=ln4、r(B)=0时，P(A)=4/(4+1)=0.8。动作比例不能确定目标函数表示；需独立测量偏好与奖励映射。

**M02 认识价值与信息成本。** 二元隐藏状态先验各0.5，检测正确率0.9。信息增益为ln2+0.9ln0.9+0.1ln0.1=0.368064 nats。检测成本0.1时，信息权重1的净值0.268064。只优化即时收益的贪婪控制器可拒绝检测；有未来收益的Bayes-adaptive RL也可能检测。

**M03 最小干预与轨迹跟踪。** 目标x1+x2=2，状态(0,2)与(1,1)的任务平方误差均为0。若增加偏离目标轨迹(1,1)的平方成本，前者损失2，后者损失0。是否纠正冗余偏离依赖成本定义。

**M04 价值、温度和先验不可识别。** 若P(A)=0.75，则logit(P(A))=ln3。模型一设置奖励差ln3、先验比1；模型二设置奖励差0、先验比3。两者相同，单一任务选择无法分离参数。

**M05 长期奖励也能产生信息探索。** 两步任务中，无测试只能猜测隐藏状态，第二步正确奖励1，期望0.5。测试正确率0.9、即时成本0.1，测试后最优选择的期望净收益为0.9减0.1等于0.8。Bayes-adaptive RL与主动推断均可能先测试，不能仅以探索证明其中之一。

## 四、未来候选验证协议（未实施）

设计隐藏状态推断×目标变更×任务相关扰动×信息成本的正交任务。事前冻结状态转移、偏好与奖励映射、观察噪声、行动限制、计算预算、训练量、规划时域、参数范围及主要指标。模型候选包括最优反馈控制、固定轨迹控制、模型自由RL、模型基础RL、贝叶斯自适应RL、主动推断、control as inference。比较留出参与者、完整任务结构及环境变化场次的log score、探索时机、扰动纠正增益、冗余方向变异与反应时。模型预测等价时记录不可识别。若偏好、奖励或认识价值需要事后调整才能拟合，则记录原冻结模型失败。尚无伦理审批、功效分析、实验数据或独立预测。

## 五、四层接口、证据边界与日历

个体层直接涉及感觉反馈、行动与信念更新。群体层可检验共享信息和相互依赖目标如何改变探索策略。制度层可检验规则、激励与反馈延迟如何改变可行控制集合。历史层可检验环境和制度非平稳性如何使策略失效。后三层仅为待验证桥接，不能由运动实验直接推断历史结果。

未决问题：偏好先验能否独立测量；认识价值与双重控制何时产生分歧；如何公平匹配资源预算；何种神经干预能区分潜在机制；跨环境预测何时失败。

原作者计算演示与理论原文已审读，原始运动或真人决策数据未复算。独立真实因果估计0，原始统计复算0，独立预测验证0，模型熔炼0，个人敏感资料读取0，新增费用0，主动CI运行0。

核验时main为9ea0508d6562b18530f885dda028dc404a6d8394，R系列最新活动涉及R178。2026-10-26的C003已完成，2026-W44的D002已完成，均保持只读。研究顺序仍为全部R系列完成、统一归纳分类、最后熔炼。

下一专题TH052：双重控制、实验性行动与信息价值的机制识别。优先审读Feldbaum 1961、Wittenmark 1995、DeGroot 1962及Bayes-adaptive POMDP原作。
