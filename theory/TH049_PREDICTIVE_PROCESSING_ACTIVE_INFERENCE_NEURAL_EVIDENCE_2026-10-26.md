# TH049 预测加工、主动推断与神经机制竞争

研究日期、英文文献检索日期：2026-10-26（Asia/Shanghai）。状态：THEORY_NOTE_BOUNDED。纯理论储备。未开展R系列拟合、神经数据复算、个人数据读取、产品开发或模型熔炼。

## 一、原始文献与阅读等级

[A，原刊公开正文重点章节] Clark, Andy (2013). “Whatever next? Predictive brains, situated agents, and the future of cognitive science.” *Behavioral and Brain Sciences* 36(3):181–204. DOI https://doi.org/10.1017/S0140525X12000477 。原刊 https://www.cambridge.org/core/journals/behavioral-and-brain-sciences/article/whatever-next-predictive-brains-situated-agents-and-the-future-of-cognitive-science/33542C736E17E3D1D44E8D03BE5F4CD9 。直接审读§1.4–1.5、§2.3、§3.1–3.4及§5的重要原文；未逐页审计全部引文。

[A，作者公开全文] Aitchison, Laurence & Máté Lengyel (2017). “With or without you: predictive coding and Bayesian inference in the brain.” *Current Opinion in Neurobiology* 46:219–227. DOI https://doi.org/10.1016/j.conb.2017.08.010 。作者稿 https://pmc.ncbi.nlm.nih.gov/articles/PMC5836998/ 。直接审读预测编码、贝叶斯推断、algorithmic motif、直接变量编码与结论等完整正文重点段落。文中所引实验未全部独立审读。

[B，出版社摘要与关键点] Friston, Karl (2010). “The free-energy principle: a unified brain theory?” *Nature Reviews Neuroscience* 11:127–138. DOI https://doi.org/10.1038/nrn2787 。出版社 https://www.nature.com/articles/nrn2787 ，PubMed https://pubmed.ncbi.nlm.nih.gov/20068583/ 。正式全文跳转访问授权页，本轮仅核验原刊摘要和出版社关键点。

[B，机构摘要与公开稿入口] de Lange, Floris P., Micha Heilbron & Peter Kok (2018). “How Do Expectations Shape Perception?” *Trends in Cognitive Sciences* 22(9):764–779. DOI https://doi.org/10.1016/j.tics.2018.06.002 。作者接受稿 https://discovery.ucl.ac.uk/id/eprint/10056291/ 。核验机构摘要，全文待审。

[B，原始实验摘要] Kok, Peter, Janneke F. M. Jehee & Floris P. de Lange (2012). “Less Is More: Expectation Sharpens Representations in the Primary Visual Cortex.” *Neuron* 75(2):265–270. DOI https://doi.org/10.1016/j.neuron.2012.04.034 。PubMed https://pubmed.ncbi.nlm.nih.gov/22841311/ 。仅核验原刊摘要，未复算fMRI数据。

[B，批判性综述摘要] Heilbron, Micha & Maria Chait (2018). “Great Expectations: Is there Evidence for Predictive Coding in Auditory Cortex?” *Neuroscience* 389:54–73. DOI https://doi.org/10.1016/j.neuroscience.2017.07.061 。作者机构 https://www.mpi.nl/publications/item3697304/great-expectations-there-evidence-predictive-coding-auditory-cortex ，开放全文入口 https://discovery.ucl.ac.uk/id/eprint/1569685/ 。仅核验机构摘要，全文待审。

等级：A表示直接阅读原作者论文的指定章节或全文，B表示原刊或作者机构摘要，M表示本项目推导。网站均为英文来源。无付费访问。

## 二、十项命题、机制、竞争解释与适用边界

**P01 预测误差是一种候选神经表征。** 前提：输入存在可预测结构。机制：表示实际输入与预测的差值可减少冗余。证据[A] Aitchison与Lengyel 2017“Predictive coding”。竞争：直接变量编码与除法归一化。边界：误差信号本身无法证明贝叶斯推断或自由能原理。

**P02 贝叶斯计算目标与神经实现需分别识别。** 前提：给定先验、似然和潜在原因。机制：相同后验可由预测编码、概率编码、对数概率编码、直接变量编码或采样近似实现。证据[A] Aitchison与Lengyel 2017“Bayesian inference without predictive coding”。反例：同样的选择准确率可以来自不同神经回路。边界：行为拟合不能单独确认神经实现。

**P03 感觉精度可调节先验与输入的相对权重。** 前提：先验和感觉噪声有可测差异。机制：较可靠的输入获得更大更新权重。证据[A] Clark 2013 §2.3；[B] de Lange等2018。竞争：注意增益、刺激选择和适应。边界：精度若由模型结果反推，将存在识别循环。

**P04 主动推断提出行动改变未来感觉输入。** 前提：存在动作和感知闭环及目标相关先验。机制：行动产生更接近预期的本体感觉或其他输入。证据[A] Clark 2013 §1.5；[B] Friston 2010。竞争：最优反馈控制、强化学习、习惯控制。边界：动作后误差下降不唯一识别主动推断。

**P05 变分自由能是给定生成模型下的数学上界。** 前提：模型p(o,s)和近似后验q(s)固定。机制：F=KL(q(s)||p(s|o))−ln p(o)，因此F≥−ln p(o)。来源[B] Friston 2010出版社关键点及[M]独立推导。反例：任意拟合的生成模型也能给出类似形式。边界：数学恒等式不能证明神经系统实际优化该量。

**P06 预期可同时降低神经幅度和提高表征质量。** 证据[B] Kok等2012报告V1平均BOLD幅度下降、MVPA表征增强，部分行为改善与表征增强相关。竞争：适应、注意、非线性读出。边界：摘要层级，本项目未读取原始逐被试数据。

**P07 期待效应与专属预测误差神经元的证据强度不同。** 证据[B] Heilbron与Chait 2018：听觉领域期待与层级组织得到支持，分离预测单元和误差单元缺少充分证据，振荡及精度研究结果混合。竞争：刺激特异性适应和直接编码。边界：限于该综述覆盖的领域与时间。

**P08 直接变量编码可解释部分所谓预测编码特征。** 前提：神经活动可编码潜变量或后验采样。机制：不确定性改变反应变异，经非线性变换可改变平均幅度。证据[A] Aitchison与Lengyel 2017“Bayesian inference without predictive coding”。竞争：预测误差单元与混合编码。边界：需事前固定试次变异和时间动力学预测。

**P09 预测误差编码优势可能随信噪比反转。** 证据[A] Aitchison与Lengyel 2017引述低光照视网膜中心周边整合的竞争机制。机制：两个带噪信号相减可能增加输出噪声。竞争：其他视觉适应。边界：本轮未独立核验综述所引原始实验。

**P10 从感知机制到社会历史的桥接仍是假设。** 证据[A] Clark 2013 §3.3–3.4、§5讨论文化脚手架和认知架构的未决问题。[M] 候选桥接需分别测量信息传递、制度激励、长期环境漂移。反例：共同信息也可能产生群体分歧。边界：本轮没有跨个体、群体、制度、历史的因果识别。

## 三、四项数学识别反例（M，人工构造）

**M01 自由能界限与实证检验分离。** 设p(o)=0.5，真实后验p(s|o)=(0.5,0.5)，近似q=(0.9,0.1)。KL(q||p)=0.9ln1.8+0.1ln0.2≈0.368064，惊讶度−ln0.5≈0.693147，F≈1.061211。若q=真实后验则F≈0.693147。该计算只验证代数，不证明神经优化。

**M02 相同后验均值无法唯一识别精度。** 观察y=2。模型甲先验N(0,1)，观测噪声方差1，后验均值1、方差0.5。模型乙先验N(0.5,1)，观测噪声方差2，后验均值(0.5+1)/1.5=1、方差2/3。仅观察点估计不足以区分先验和精度；额外测量后验方差及多噪声条件可增加识别力。

**M03 期待与适应的单一对比不可识别。** 若预期条件平均神经反应比非预期条件低0.2，模型甲期待效应为−0.2、适应为0，模型乙期待为0、适应为−0.2，均完全匹配。需要独立操纵期待概率与刺激重复，并控制频率、间隔和注意。

**M04 行动后误差下降无法识别决策算法。** 假设|观察−目标|从2降至0。主动推断、反馈控制、强化学习与环境自发变化都可能生成同一结果。随机操纵动作可用性、动作结果映射和外部扰动，才可能分离解释。

## 四、竞争理论、四层连接与未来检验

预测编码关注独立误差单元、层级反馈和精度加权；直接变量编码关注潜在原因的神经表征和采样变异；适应与归一化提供不依赖专属误差单元的解释；主动推断需要与反馈控制和强化学习比较。保留全部竞争预测，禁止从单一平均神经反应选择胜者。

个体层：感知预测、注意、动作、学习。群体层：共享期待和信息传播作为待测机制。制度层：奖励规则、信息可信度与反馈延迟可能改变学习条件。历史层：文化技术与制度环境变迁可能改变生成分布。后三层均属研究假说，没有实证跨层外推。

候选验证清单：①事前冻结先验、似然、精度与神经信号映射；②同条件比较预测编码、直接编码、适应、归一化及控制模型；③正交操纵期待、重复、噪声、注意和动作；④同时测量平均幅度、解码、变异与时间动力学；⑤使用留出参与者、留出刺激和独立预测评分；⑥记录参数等价类与失败案例；⑦未获公开合法数据时记录阻塞，不得声称复现。

## 五、研究日历、证据缺口和下一主题

C：2026-10-26 C003已完成，保持只读；下一研究日研究动态效用权重、多目标偏序与鲁棒决策。D：2026-W44 D002已完成，保持只读；下一研究周研究人口转型、迁移冲击与制度适应。R系列继续独立推进，先完成全部R系列，随后统一分类归纳，最后模型熔炼。

READING_GAP：Friston 2010完整正文、de Lange等2018接受稿、Heilbron与Chait 2018开放原刊、Kok等2012原始数据尚未逐页核验或复算。没有为此付费。

新增真实数据因果估计0，独立预测复验0，模型熔炼0，个人敏感资料读取0，新增费用0，主动运行CI 0。

下一主题TH050：预测加工的反证设计、感觉适应与注意竞争，深读Heilbron与Chait 2018、de Lange等2018、Kok等2012，形成可区分的预注册预测。
