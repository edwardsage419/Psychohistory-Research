# R238 历史文本词向量：九个有限跨期嵌入世界、144完整潜在词义来源、锚词对齐及隐藏词义非识别，事前冻结

日期2026-10-23（Asia/Taipei）。真实239目录**10-012 Historical Text Embeddings（P2）**，R238。九个人工跨时词—潜在意义向量世界，**不包含历史语料词向量训练、真实跨时代语义变化、真实历史E3、人类被试E2**。研究目标仅为跨期词向量的正交坐标任意性、尺度变换、频率组成效应、失效锚点造成的假漂移，以及不可由聚合词向量识别的内部词义混合机制。R073与PESEN v0.1保持冻结。前置冻结本协议必须作为独立commit先于模型源码、评分结果和CI提交。

## 一手论文与本R边界

Hamilton, Leskovec & Jurafsky (2016), [*Diachronic Word Embeddings Reveal Statistical Laws of Semantic Change*](https://aclanthology.org/P16-1141/), ACL 2016:1489–1501, DOI https://doi.org/10.18653/v1/P16-1141。其真实方法涉及历史语料PPMI/SVD/word2vec向量、跨时间正交对齐、已知语义变化验证、频率及多义性分析，本R不对其四语言六语料结果作任何复现宣称。Kim et al. (2014), [*Temporal Analysis of Language through Neural Language Models*](https://aclanthology.org/W14-2517/), ACL Workshop 2014:61–65，对时间切片训练及语义变化提供历史方法背景；本R没有训练神经向量。

## 人工生成结构、完整观测与隐语义

两个人工时期t=0,1，词典`A,B,C,D`四个不带历史含义的标记，二维有理人工潜在坐标：
`A=(1,0), B=(0,1), C=(1,1), D=(1,-1)`。D是关注目标，A/B是事先选择的两个锚词，C留作锚点外独立稳定性检查。所有字词非零向量，允许Fraction表示全部旋转及频率。

每个(t,word)含两种等概率人工潜在“词义模式”`sense∈{0,1}`，每模式先验1/2。对非目标A/B/C，两个sense真实坐标同上。对D在时期0，两个真实sense向量为`(0,-1),(2,-1)`，平均恰`(1,-1)`，人工内部sense方差矩阵为`[[1,0],[0,0]]`。时期1默认这两个sense保持不变，若目标整体漂移的世界则它们各自向x正方向+1、平均目标D变`(2,-1)`；单个特殊`SENSE_RECONFIGURATION_ALIAS`不改变总体平均，但把时期1两个sense改为`(1,-2),(1,0)`，平均仍`(1,-1)`而隐藏sense方差矩阵变为`[[0,0],[0,1]]`。**这是人工oracle内部多义性变化，并非任何历史语义经验验证。**

所有词实际“观察向量”一律是其人工两sense平均经可能的时期1坐标变换得到的二维`observed_v`，观察可用字段为`(time,word,embedding_x,embedding_y,word_frequency)`，隐藏sense原坐标和senses方差只是oracle。词频每期原整数计数默认`(A,B,C,D)=(4,4,2,2)`（12总），频率变化世界第二期改为`(8,2,1,1)`（总12）。原人工源质量 `P(t)=1/2 × P(word|t)=count/12 × P(sense|t,word)=1/2`，每个世界共2时期×4词×2sense=16条完整原源，九世界**144条**，每世界完整源概率合计1，所有正质量。观察变量分布通过边缘化隐藏sense计算，因实际观察向量对每word固定等于平均sense，数据结构要保存所采样的潜在sense与平均后同一个观察向量，不可当作独立真实语料。

正交旋转固定`Q=[[3/5,-4/5],[4/5,3/5]]`，QᵀQ=I，det=1；只在注明的world的第二期对所有观察均值向量施加Q，真实内部sense原值不旋转，标记为“坐标表述差异”。纯观察倍率2同理仅改变数字表示尺度。锚词拟合对齐矩阵定义为把time1两个已观察锚词A/B的二维列向量作为矩阵`H`，取有理精确逆`H^−1`将其映射回time0单位基。H必须det≠0（九世界均满足）。这是一种**预先选定两锚词确定的线性坐标校准**，不能伪称已经实施原论文通用正交Procrustes估计器、也不能宣称单词2D例子有统计方差或抽样显著性。

## 九个冻结人工世界

1. `STABLE_BASE`：time1全部隐藏sense、观察嵌入和词频与time0一致。
2. `GLOBAL_ROTATION`：time1全部已观察嵌入乘Q，原内部真实sense不变；未经对齐的目标位移非0，但准确锚点逆变换后目标位移0，time1完整四词Gram与time0一致。
3. `TARGET_SEMANTIC_DRIFT`：time1 D内部两个sense均向x+1，真目标sense平均由(1,-1)变(2,-1)，其余三锚词不变；对齐后目标平方位移1。
4. `ROTATED_TARGET_DRIFT`：与3真正的隐藏sense变化相同，但观察time1全体乘Q；time1各项Gram与3相同，对齐后目标平方位移仍1。
5. `GLOBAL_SCALE_2`：time1全部观察向量倍增2、内部sense不变，未经对齐目标平方位移2，锚点线性校准后位移0；所有time1同词余弦保持、完整Gram相对time0放大4倍。
6. `FREQUENCY_COMPOSITION_ONLY`：内部sense与观察词向量全部稳定，仅第二期词频由(4,4,2,2)转(8,2,1,1)，两期**按词频加权语料质心**改变，但词D本身观察向量不漂移，对齐后目标位移0。
7. `FREQUENCY_PLUS_TARGET_DRIFT`：第二期频率改变与TARGET_SEMANTIC_DRIFT共同发生；按词频加权质心的改变混合词的真实位置变化与语料组成变化，不可把该质心移动全算在目标语义上。
8. `ANCHOR_DRIFT_FALSE_ALIGNMENT`：time1仅两个锚A/B的实际语义均值乘Q，非锚C/D保持原坐标、真实D隐藏sense不变；锚点H=Q，线性校准会错误地给非锚D引入平方位移`8/5`，而完全不对齐时其平方位移0。该反例表明锚词本身变化会让锚点法对其他实际稳定词制造虚假的对齐后变化；它不是对现实Procrustes任何锚选机制必然失效的证明。
9. `SENSE_RECONFIGURATION_ALIAS`：全部实际观察向量和实际频率与STABLE_BASE对所有时期/词完全相同，但D在time1两人工sense分布改为(1,-2),(1,0)，隐藏D的内部sense协方差矩阵方向改变；仅聚合观察词向量无法识别此限定潜在词义分布变化。

## 完整评分、双算法与科学关口

A. 对每个world直接从**16条完整原源**按time与word条件概率积分获得两期四词实际观察质心向量、各期频率（分布归一）、对每期四词所有16个Gram格`v_i·v_j`、两个锚点确定的精确有理H逆、原未经对齐与锚点对齐后目标D的欧氏平方位移。再算两期按词频加权的全语料2D质心及其欧氏平方位移（混合组成统计量，不叫语义真改变）。
B. 与上述源积分完全独立第二条解析路线仅由冻结单词真实sense模板+各world漂移、坐标变换与频率参数直接生成两时期观察质心，再逐世界每个word与实际源路径精确核对；H逆另用手写2×2矩阵高斯/伴随矩阵代数证书，锚点A/B映射后必须精确等于基向量，全部可见4×4Gram源/解析两路相同。
C. Oracle隐藏D内部sense平均变动的平方位移：STABLE、GLOBAL_ROTATION、GLOBAL_SCALE、FREQUENCY_ONLY、ANCHOR_DRIFT、SENSE_RECONFIG为0；TARGET_SEMANTIC_DRIFT、ROTATED_TARGET_DRIFT、FREQUENCY_PLUS_TARGET_DRIFT为1。与实际观察目标变化明确分开。SENSE_RECONFIG隐藏内部Cov从diag(1,0)到diag(0,1)，但**观察所有time-word-embedding-frequency四列逐source sense忽略前后与STABLE完全相同**。
D. 前置确证强约束：GLOBAL_ROTATION未经对齐D平方位移8/5而锚点校准后0；GLOBAL_SCALE未经对齐D平方位移2而锚点校准后0；ANCHOR_DRIFT未经对齐D平方位移0但错误地对齐后平方位移8/5；TARGET_SEMANTIC_DRIFT与ROTATED_TARGET_DRIFT锚点校准后目标D平方位移均1；GLOBAL_ROTATION与STABLE两期Gram相同，GLOBAL_SCALE第二期Gram=4倍，TARGET_SEMANTIC_DRIFT与ROTATED_TARGET_DRIFT第二期Gram相同。
E. 原词频组成`(4,4,2,2)/12`与改组成`(8,2,1,1)/12`的精确质心需要两条独立算法核验，频率改变的模型目标D自身不漂移时质心仍移动。这证明组成引起总体均值变化，与实际语义漂移独立；不能外推成人类历史文档的因果解释。
F. 必须验证九模型16完整原来源均正质量、sourceProbability和1；全144 CSV、九模型精确结果JSON及SHA256收据，由Python3.11/3.12各至少45真实测试及GitHub Actions第三完整独立来源归档job验收。模型完整数学源、CI、机器人归档成功后才正式有界结题。
G. 未训练任何PPMI/SVD/word2vec、未做实际cross-time模型评估、没有历史文本、人类语义标注或E3社会解释；此人工oracle定义本身不是经验因果证明。原239下一`10-013 Qualitative Comparative Analysis`，拟R239，需本R完成后重新实查。原R全部完成后才统一分类和熔炼。
