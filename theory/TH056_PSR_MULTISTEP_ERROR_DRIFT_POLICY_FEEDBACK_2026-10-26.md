# TH056 预测状态多步误差、环境漂移与行为反馈的外推边界

日期：2026-10-26（Asia/Shanghai）；状态：THEORY_NOTE_BOUNDED。纯理论与方法学储备，独立于R系列模型拟合、真人实证和商业分析。C003今日与D002本周已经完成，本轮只读。无私人敏感数据、付费资源及主动CI。

## 一、原始来源与审读边界

A：开放原刊或作者接受稿指定章节直接审读。B：原作者或出版机构摘要及书目核验。M：本项目独立人工算例，绝不计入原作者数据复算。全部网站使用英文内容。

1. [A1] Venkatraman, Arun, Martial Hebert & J. Andrew Bagnell (2015). “Improving Multi-Step Prediction of Learned Time Series Models.” *AAAI 29*, pp.3024–3030. DOI: 10.1609/aaai.v29i1.9590。原刊 https://ojs.aaai.org/index.php/AAAI/article/view/9590/9449 。直接审读Theorem 1的Lipschitz误差传播、Data as Demonstrator（DaD）算法、Theorems 2–3及理论保证的样本要求。未复算实验。
2. [A2] Talvitie, Erik (2017). “Self-Correcting Models for Model-Based Reinforcement Learning.” *AAAI 31*, pp.2597–2603. DOI: 10.1609/aaai.v31i1.10850。原刊 https://ojs.aaai.org/index.php/AAAI/article/view/10850/10709 。直接审读Lemmas 1–4、Propositions 5–6、Theorems 8、10、实验与限制。较强的自我纠正误差界以确定性环境及blind rollout policy等为条件。
3. [A3] Jiang, Nan, Alex Kulesza & Satinder Singh (2016). “Improving Predictive State Representations via Gradient Descent.” *AAAI 30*. DOI: 10.1609/aaai.v30i1.10270。原刊 https://ojs.aaai.org/index.php/AAAI/article/view/10270/10129 。直接审读PSR谱初始化、式(5)至(7)负概率与归一化问题、对比散度、合成HMM及Wikipedia实验。未复算实验。
4. [A4] Gama, João, Indrė Žliobaitė, Albert Bifet, Mykola Pechenizkiy & Abdelhamid Bouchachia (2014). “A Survey on Concept Drift Adaptation.” *ACM Computing Surveys* 46(4), Article 44. DOI: 10.1145/2523813。作者机构接受稿 https://eprints.bournemouth.ac.uk/22491/1/ACM%20computing%20surveys.pdf 。直接审读§2.1真实与虚拟漂移、时间形态及§3.2变化检测。接受稿页眉显示2013年，正式出版按2014年；44页全文未逐段通读。
5. [B5] Ross, Stéphane & J. Andrew Bagnell (2012). “Agnostic System Identification for Model-Based Reinforcement Learning.” *ICML 2012*, pp.1905–1912。作者机构摘要 https://publications.ri.cmu.edu/agnostic-system-identification-for-model-based-reinforcement-learning ，预印本 https://arxiv.org/abs/1203.1007 。仅核验摘要：迭代学习保证仍需要低误差模型及良好探索分布。
6. [B6] Talvitie, Erik (2014). “Model Regularization for Stable Sample Rollouts.” *UAI 2014*, pp.568–577。原刊 https://proceedings.mlr.press/r12/college14a.html 。本轮只核验摘要，2017年理论扩展见A2。
7. [B7] Downey, Carlton, Ahmed Hefny & Geoffrey Gordon (2017). “Practical Learning of Predictive State Representations.” arXiv:1702.04121。作者预印本 https://arxiv.org/abs/1702.04121 。仅核验摘要：谱参数估计目标与最终推断损失可能不一致；全文与正式发表版本待查。

## 二、十项条件性理论命题

| ID | 命题、前提与机制 | 竞争解释、反例及证据边界 |
| --- | --- | --- |
| P01 | 自回归模型将预测输出重新作为输入；若更新映射Lipschitz常数L>1，误差上界可能随预测时域指数增长。[A1 Theorem 1] | L<1的收缩映射、主动纠错可产生不同趋势；上界并不意味着每个PSR实际指数发散。[M1] |
| P02 | 一步误差低可能与长时域误差高并存，模型滚动造成训练与应用输入分布错位。[A1,A2] | 直接多步监督、轨迹约束、重采样或鲁棒规划是竞争方法；需独立评估。[M2] |
| P03 | DaD把模型生成的状态与真实训练轨迹的后续状态配对，尝试减少滚动误差。[A1 Algorithm 1] | 依赖无遗憾学习、足够新轨迹及指定损失；作者实际复用轨迹，理论条件与实践有差异。 |
| P04 | 对确定性MDP及blind rollout policy，自我纠正误差与控制价值误差的关系可比普通一步误差界更紧。[A2 Theorem 8] | 对随机社会系统、非盲策略、未知奖励与不同规划器需重新证明。 |
| P05 | 即使模型完全正确，独立采样的随机模型轨迹也可能与真实轨迹不同。[A2 Proposition 5] | 样本路径差异可来自合法随机性；需比较条件分布或规定耦合。[M3] |
| P06 | 谱PSR在模型秩错设下可能无法最小化预测损失，谱初始化后的梯度优化在部分实验改善性能。[A3] | 对比散度、负概率修正、归一化与计算预算均影响比较；不能宣称普适改进。 |
| P07 | 真实漂移改变P(Y|X)，虚拟漂移改变P(X)而保持条件分布。[A4] | 标签口径变化、选择偏差和未记录动作也可产生类似观测变化。[M4] |
| P08 | 行为策略改变可以改变结果的边际分布，即使给定动作的环境响应不变。[A2,B5,M5] | 需分开审计行为策略、观测机制与环境动力学；缺行动日志时不可唯一识别。 |
| P09 | 模型部署影响行动选择，行动改变后续样本覆盖和模型可观察数据，形成内生反馈。[A2,B5] | 与外生环境漂移竞争；未知策略、零覆盖和制度断点可阻碍离策略推断。 |
| P10 | 概率预测、长时域校准、规划收益及心理机制识别需要分别验收。[A2,A3,B7] | 单一预测指标无法证明真实认知机制；从计算模型向社会历史层外推需独立因果与外部验证。[M6] |

## 三、六项独立人工算例

M1 误差增长：真实x(t+1)=0.8x(t)，拟合xhat(t+1)=1.05xhat(t)，起点均为1。t=1：0.8与1.05，差0.25；t=5：0.327680与1.276281563，差0.948601563；t=10：0.107374182与1.628894627，差1.521520444。此例为指定模型的数值行为，不能作为普遍PSR定理。

M2 模型排名反转：真实状态始终为0。A满足f_A(0)=0.01、f_A(0.01)=1、f_A(1)=1；B满足f_B(0)=0.05、f_B(0.05)=0.05。真实状态上的一步误差A为0.01、B为0.05；滚动3步误差A为1、B为0.05。A可以用有限陡度的分段连续函数实现。

M3 随机路径错配：环境与完美模型各自独立抛公平硬币，进入H或T吸收状态。两条轨迹不一致概率2×0.5×0.5=0.5；正确条件分布的总变差距离为0。与A2 Proposition 5相符。

M4 条件漂移：同一X下旧时期P(Y=1|X)=0.2，新时期为0.8。旧预测0.2在新时期的预期Brier为0.8×0.8²+0.2×0.2²=0.52，新时期最优概率0.8的预期Brier为0.16。单看X不能识别该变化。

M5 策略反馈：固定环境P(Y=1|a0)=0.2、P(Y=1|a1)=0.8。旧策略P(a1)=0.1时边际P(Y=1)=0.26；新策略P(a1)=0.9时为0.74。环境条件机制未变，边际数据已明显改变。

M6 目标不一致：假设训练日志99%执行a0，1%执行a1。模型A对a0准确率0.99、对a1为0；模型B对a0准确率0.95、对a1为1。加权准确率A=0.9801，B=0.9505；若关键高回报行动是a1，B仍可能具有更高决策价值。决策价值需要单独指定奖励及环境，不能由这些准确率自动推算。

以上均为本项目人工数学构造。真实数据复算、独立预测验证和因果估计均为0。

## 四、四层联系与未决问题

个体：行为、学习、测量误差与自我预测相互反馈；PSR预测状态不能直接视为已识别的真实心理实体。

群体：他人行为、网络结构及互动配对改变行动支持集和观测概率；边际相关不能直接识别社会影响。

制度：规则改变行动集合、收益和记录口径；需标注制度版本断点，并检验结构稳定性。

历史：人口、技术、生态与战争等变化可能破坏平稳条件。事件不可重复、共同冲击与长期数据缺口限制外推；不得从本轮模型断言具体未来事件。

## 五、未来验证清单

1. 事前冻结一步、3步、10步、20步时域，独立预序贯log score、Brier、校准、规划收益及失败率。
2. 在同等信息集和预算下比较teacher forcing、自由滚动、直接多步监督、DaD、自我纠正模型、谱PSR、谱加梯度PSR、有限记忆和隐藏状态模型。
3. 完整主体、场次与时间块留出，禁止验证数据回流至模型选择或训练。
4. 审计行动覆盖、行为策略、环境版本、重置条件、观测口径和标签变更。零覆盖记NOT_IDENTIFIED。
5. 分别设计外生动力学漂移、策略诱导变化、观测误差及奖励变化压力测试。
6. 随机环境优先比较条件分布及proper scores；路径差异必须说明耦合，不套用A2的确定性blind-policy保证。
7. 预冻结竞争机制、失败标准、敏感性和外部验证计划；未获得实证前维持THEORY_NOTE_BOUNDED。

## 六、工作流边界与下一项

C003（2026-10-26）与D002（2026-W44）只读，R系列独立推进。未读取健康、财务、关系等个人敏感数据，未开发决策产品，未主动运行CI，新增费用0。

TH057候选：策略干预、预测模型因果可迁移性与离策略评价。优先审读performative prediction、因果MDP及分布鲁棒性原始论文。
