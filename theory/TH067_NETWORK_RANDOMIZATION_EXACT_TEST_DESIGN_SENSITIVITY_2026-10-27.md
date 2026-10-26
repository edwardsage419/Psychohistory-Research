# TH067 网络干扰下的随机化推断、精确检验与设计敏感性

研究及非中文文献检索日期：2026-10-27（Asia/Shanghai）。轨道：纯理论。状态：THEORY_NOTE_BOUNDED。与R系列、实证数据、商业产品、C/D方法日历分离。

## 一、原始书目与实际审读范围

[A1 直接审读作者公开稿指定章节] Athey, Susan, Dean Eckles & Guido W. Imbens (2018). “Exact p-Values for Network Interference.” *Journal of the American Statistical Association* 113(521):230–240. DOI https://doi.org/10.1080/01621459.2016.1241178 。2015年作者开放稿 https://arxiv.org/pdf/1506.02084 。审读§1、§3、§4–5中非尖锐原假设、人工实验和随机化条件；MIT机构原稿 https://dspace.mit.edu/entities/publication/8ab135cd-0a3d-443e-aa8f-52ec2b18426b 。未逐页校勘2018正式版。

[A2 直接审读作者公开稿指定章节] Basse, Guillaume W., Avi Feller & Panos Toulis (2019). “Randomization Tests of Causal Effects under Interference.” *Biometrika* 106(2):487–494. DOI https://doi.org/10.1093/biomet/asy072 。2018年9月作者稿另题为“Conditional randomization tests of causal effects with interference between units”，https://arxiv.org/pdf/1709.08036 。审读§2、Theorem 2.1、§3、Theorem 3.1、§4中条件化机制、统计量可填补性和两阶段家庭实验。原刊书目 https://academic.oup.com/biomet/article-abstract/106/2/487/5306899 。开放稿与正式稿未逐字校勘。

[A3 直接审读作者公开稿指定章节] Puelz, David, Guillaume Basse, Avi Feller & Panos Toulis (2022). “A Graph-Theoretic Approach to Randomization Tests of Causal Effects under General Interference.” *Journal of the Royal Statistical Society Series B* 84(1):174–204. DOI https://doi.org/10.1111/rssb.12478 。2021年作者稿 https://arxiv.org/pdf/1910.10862 。审读§2–4、Proposition 1、零暴露图、双团分解及条件概率证明选段；正式出版书目 https://academic.oup.com/jrsssb/article/84/1/174/7056130 。完整51页未逐页通读。

[B1 书目与原始摘要核验] Bowers, Jake, Mark M. Fredrickson & Costas Panagopoulos (2013). “Reasoning about Interference between Units: A General Framework.” *Political Analysis* 21(1):97–124. DOI https://doi.org/10.1093/pan/mps038 。作者稿 https://arxiv.org/abs/1208.0366 ，机构原刊书目 https://experts.illinois.edu/en/publications/reasoning-about-interference-between-units-a-general-framework/ 。全文模型未审。

[B2 原刊摘要核验] Basse, Guillaume & Avi Feller (2018). “Analyzing Two-Stage Experiments in the Presence of Interference.” *Journal of the American Statistical Association* 113(521):41–55. DOI https://doi.org/10.1080/01621459.2017.1323641 。原刊摘要 https://www.tandfonline.com/doi/abs/10.1080/01621459.2017.1323641 。具体方差推导未审。所有来源均为非中文网站，未购买文献。A是原文指定章节，B仅摘要书目。

## 二、形式化假设与检验目标

有限总体n个单位，完整分配Z∈{0,1}^n，已知设计概率p(z)，潜在结果Yi(z)允许受他人处理影响。

H_global：每个i及任意z,z'都有Yi(z)=Yi(z')，即所有处理完全无效，是尖锐原假设。

H_no_spill：每个i，若zi=z'i则Yi(z)=Yi(z')，即没有溢出，但允许自身处理有效。它通常是非尖锐原假设。

Fisher随机化检验需要在所用分配支持集上填补检验统计量依赖的潜在结果。H_no_spill可通过选择焦点单位并固定其自身处理，或其他合法条件化机制使局部统计量可填补。若C为条件化事件，正确分配为p(z|C)∝p(C|z)p(z)。在原假设与可填补条件下，含平局的右尾p值Pr[T(Z;Yobs,C)≥Tobs|C]保证有限样本零假设拒绝率不超过α。A2开放稿有严格大于号的公式呈现；离散平局时需另行规定随机平局打破，本文使用保守的≥。

## 三、14项条件性命题及竞争解释

T01 [A1,A2] 完全无效与无溢出是不同检验对象。自身处理有效时，拒绝H_global不能解释为同伴传播。原检验对H_global仍可有效。

T02 [A1] 网络距离、边类型、邻居身份异质性约束属于不同原假设。拒绝距离约束也可能涉及共同资源、信息接触或测量误差。

T03 [A1] 人工实验通过限制焦点单位和允许分配使非尖锐假设局部可填补。焦点和分配支持集必须明确。

T04 [A2] 条件化机制可以依赖观察到的分配，但检验须使用由设计与条件机制共同决定的p(Z|C)，事后等权置换未必有效。

T05 [A2] 可填补性是必要门槛。随机化执行正确仍无法挽救错误的暴露映射或事后选择焦点。

T06 [A2,B2] 两阶段家庭实验涉及家庭分配及成员分配；簇间无干扰与匿名簇内影响需要单独核验。

T07 [A3] 零暴露图把单位与处理分配相连。双团内的焦点结果在相应原假设下可填补；双团分解需匹配真实条件分布。

T08 [A3] 较大双团可能提高有效单位数与允许分配数，统计功效还取决于效应大小、噪声、统计量和权重，不能普遍保证最优。

T09 [A1,A3] 漏边、弱边剔除及二跳传播会改变原假设适用性。处理前网络与暴露距离应冻结并做敏感性分析。

T10 [A2,A3] 精确检验的有效性与平均溢出效应估计的准确性不同。拒绝无溢出不直接给出政策净收益。

T11 [A2] 更严格条件化可能减少分配支持集，使最小可达p值增大；小样本在5%水平可能没有拒绝能力。

T12 [A1,A2] 设计型精确性要求真实已知的随机化分配。观察性网络中的择友与共同冲击不能由该公式自动消除。

T13 [B1,A1,A3] 结构化传播模型可提出更具体的反事实假设，同时增加模型错设风险；较弱模型假设的条件化方法可能牺牲功效。

T14 [本项目推断] 个体行为、群体传播、制度执行和历史冲击间的迁移需要网络、处理版本、制度依从及时间稳定性证据。单次实验无法直接预测历史或未来事件。

## 四、七项人工有限枚举及反例

全部数值为人工构造，n≤4。不是原作者真实实验或数据复算。

E01 [非尖锐] 设四单位Yi(z)=1+zi。H_no_spill为真，H_global为假，因为Yi(1)=2而Yi(0)=1。

E02 [错误解释导致的误报] 四单位独立Bernoulli(1/2)，16个等概率分配。仍设Yi(z)=1+zi，错误地用H_global的尖锐检验冒充H_no_spill检验。统计量T(z,y)=Σzi·yi，观察k个处理者时Tobs=2k。保持观察y不变，只有原k名处理者在新分配中仍处理才达到Tobs，故p=2^(-k)。名义α=1/8时k≥3拒绝，真实H_no_spill下拒绝概率[C(4,3)+C(4,4)]/16=5/16=0.3125，高于0.125。错误来自原假设标签错置，不能据此说Fisher对H_global的检验无效。

E03 [正确条件化] 四节点星形网络，中心0为焦点，固定Z0=0，三个邻居独立Bernoulli(1/2)。H_no_spill下Y0(z)=1+z0=1。取T=Y0·(Z1+Z2+Z3)。8种分配的处理邻居数S=0,1,2,3频数为1,3,3,1，含平局右尾p依次为1、7/8、1/2、1/8。α=1/8时条件拒绝率恰为1/8；α=1/2时为1/2。

E04 [离散分辨率] E03的最小非零p为1/8，故α=0.05时所有可能分配都不能拒绝。有效性与功效需分开报告。

E05 [支持集不足] 若四单位实验固定恰好一人处理且条件Z0=0，三个邻居处理数恒为1，E03统计量恒定，p=1。该设计没有邻居处理数量的剂量对比。

E06 [错误等权] 两邻居独立处理概率为0.8和0.2，中心自身处理固定0。邻居状态(00,10,01,11)概率(0.16,0.64,0.04,0.16)。T为处理邻居数。观察T=2时正确右尾p=0.16，错误四状态等权得0.25；观察T=1时正确p=0.84，错误等权得0.75。

E07 [条件化敏感性] E03若额外固定一个邻居，只剩4个等概率分配，最小非零p升至1/4；固定全部邻居则统计量不再变化。更强的条件化可能维护可填补性，同时降低检验分辨率。

## 五、四层联系、验证清单与证据边界

个体层：预先定义焦点、行为结果、处理版本、观察窗口及异质性；不能从拒绝结果直接推断内部动机。群体层：冻结处理前网络、边权、干扰距离和随机化支持集，区分择友、共同冲击与真实传播。制度层：区分随机化、实施、覆盖率、依从性及跨组织传播，记录条件化概率。历史层：只提出条件性情景，历史记录通常缺少已知随机化机制，不得直接套用精确p值断言具体事件。

未来验证：①冻结H_global、H_no_spill和二跳等原假设；②记录焦点及m(C|Z)；③小图穷举p(Z|C)与可填补性；④报告平局处理、最小可达p值；⑤比较名义错误率、功效、统计量与计算成本；⑥审计漏边、动态网络、跨簇传播和不遵从；⑦跨新网络独立复验。

未决：动态网络下怎样构造可检验干扰假设？大型网络双团如何兼顾计算与功效？网络误测与不遵从如何进入识别界限？不同制度中哪些机制可以迁移？

本轮三份原作者开放稿指定章节直接审读，另两份原刊摘要核验。14项条件性命题，7项人工枚举。真人个体数据复算0，独立因果估计0，独立预测验证0，模型熔炼0。未审原作者全部定理证明和真实实验复现。

C今日C004已完成，D本周D002已完成，本轮只读。没有读取个人敏感资料，没有开发个人决策产品，没有付费API、收费文献、额外云服务或主动CI，新增费用0。既定顺序：完成全部R系列，再归纳分类，最后模型熔炼。

下轮TH068：网络实验中的处理不遵从、溢出机制错设与敏感性界限。
