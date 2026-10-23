# R271 预注册与注册报告：九人工有限零假设分析政策、13104完整原source与结果导向选择风险；计算前冻结

日期2026-10-23 Asia/Taipei。原239目录12-001 Preregistration and Registered Reports（P0），研究R271。第一来源Nosek et al. (2018), *The preregistration revolution*, PNAS 115(11):2600–2606, DOI https://doi.org/10.1073/pnas.1708274114；Chambers (2013), *Registered reports: a new publishing initiative at Cortex*, Cortex 49(3):609–610, DOI https://doi.org/10.1016/j.cortex.2012.12.016 。本研究仅是分析决策自由度的小型数学演示，**没有实际向注册平台提交方案，没有期刊Stage 1接收或Stage 2审查，没有采用原作者实证数据**。

## 冻结实验空间及九政策世界
真实世界零假设H0：所有独立二元观察X都是iid Bernoulli(1/2)。每个候选检验区块有4个原始独立bit；假设成功率大于1/2，单侧精确Binomial(4,1/2) p_value(K)=sum_{j=K}^4 C(4,j)/16。因此成功数K=0,1,2,3,4的p依次为1、15/16、11/16、5/16、1/16。冻结名义familywise阈值alpha=1/8。单次检验只有K=4时原始p≤alpha。

独立候选区块数m∈{1,2,3}，恰三政策：
* FROZEN_FIRST：无论其它候选观察如何，只对事前指定第一个区块进行一次检验并以raw p≤alpha决定报告。
* FLEXIBLE_ANY：观察m个区块后选择至少一个raw p≤alpha的阳性区块并报告“有显著发现”，忽略同时尝试的其它检验与结果导向选择。这里明确作为**未校正多重检验报告**，不能称为正确预注册。
* BONFERRONI_ANY：针对事前登记的整个m检验家族使用raw p≤alpha/m的Bonferroni阈值，仍允许择优报告但对尝试次数明示校正。这是统计政策基线，**并不是预注册的全部制度含义**。

每个m的独立原随机源配置全集为长度4m所有bit序列、原质量2^(-4m)，故原source类型数16、256、4096，各在三政策world记录一次；九world合计3×(16+256+4096)=**13104条带policy标签的完整人工原source**。真实原随机配置不同只有16+256+4096=4368个，不能说13104独立实验。逐source存储全部原bit、每block成功数和单侧原始精确p、各政策所报告的区块索引（无发现用-1）、是否声明发现、原source精确质量、家族大小与冻结阈值。

## 事前数学验收：所有世界精确假阳性率
单区块`P(raw p<=1/8 | H0)=1/16`，三个候选区块相互独立。
FROZEN_FIRST：全部m均1/16。
FLEXIBLE_ANY：m=1为1/16；m=2为`1-(15/16)^2=31/256`；m=3为`1-(15/16)^3=721/4096`，严格大于冻结familywise阈值1/8。
BONFERRONI_ANY：若m=1，alpha/m=1/8，误报1/16；m=2，alpha/m=1/16，只有K=4才符合，误报31/256（≤1/8）；m=3，alpha/m=1/24，比可用离散p最小值1/16还小，因此没有任何拒绝事件，误报0。该最后结果反映离散精确检验和Bonferroni的保守性，不能泛化为多重比较方法总是零发现。

## 三路核验与因果边界
路线A：逐world穷尽全部bit来源，真实计算每block K与完整精确单侧p，分别执行上述三冻结政策，按来源1/2^(4m)加权得拒绝概率；与逐source报告的模型选择及决策一致。
路线B：独立数学解析`P(K=4)=1/16`，m区块无命中概率`(15/16)^m`，用alpha/m独立确定Bonferroni可选择事件并产生上述九个Fraction闭式期望；不可调用路线A的枚举结果实现独立验证。
路线C：第三GitHub CI job从全部13104条CSV源逐项重建原bit、block二项检验概率、全source mass、policy reject及选择索引，重算精确世界级概率并核对源SHA256，杜绝只测试结果布尔值的空壳流程。

先将本协议提交main并固定其SHA，再建立Python3.11/3.12各≥45真实单测、原生完整CSV与概率JSON、来源和结果SHA256机器凭证、第三独立CI审计、永久机器人原始来源归档，三job全部completed/success方能发布正式有界E1结题。不能将统计演示等同于注册报告制度对发表偏差的真实因果效果；不能把先验无效的多重分析事后重命名为预注册。新增真人E2=0、真实历史E3=0，R073与PESEN v0.1保持冻结。下一候选原目录12-002 Out of Sample Prediction（拟R272），完成全部原R研究后再统一归纳分类与熔炼。
