# R238 历史文本词向量：九个人工双时期词嵌入世界、144完整词义来源与坐标对齐非识别

日期2026-10-23（Asia/Taipei）。原239目录实际 **10-012 Historical Text Embeddings（P2）**。本项科研范围 `CLOSED_BOUNDED_E1_ARTIFICIAL_DIAchronic_EMBEDDING_ALIGNMENT_AND_HIDDEN_SENSES`。所有模型只有4个无语义词符号、两个人工时期、2维有理坐标和冻结2个潜在sense组件，未训练或调用历史文本语料，新增真人E2与真实历史E3皆0。

## 原始论文与有效证据界限

Hamilton, Leskovec & Jurafsky (2016), [*Diachronic Word Embeddings Reveal Statistical Laws of Semantic Change*](https://aclanthology.org/P16-1141/), ACL 2016:1489–1501, DOI [10.18653/v1/P16-1141](https://doi.org/10.18653/v1/P16-1141)。原论文基于多个语言和历史语料训练PPMI、SVD及word2vec并进行跨时对齐，对有已知语义变化的词及频率、多义性提出经验研究；本R不宣称复算其语料、模型训练、统计法律或跨语言结论。Kim et al. (2014), [*Temporal Analysis of Language through Neural Language Models*](https://aclanthology.org/W14-2517/)，ACL 2014 Workshop:61–65，说明时间切片嵌入建模的已有方法；当前只测试几何坐标机制，没有训练神经词向量。

[冻结九世界和144来源完整协议](../../protocols/R238_HISTORICAL_EMBEDDINGS_9_WORLDS_144_FULL_SENSE_ATOMS_PRESCORE_FREEZE_2026-10-23.md)在编写源码及计算评分前独立提交 [73765386](https://github.com/edwardsage419/Psychohistory-Research/commit/7376538692ef9c468e21a2366e69db7d238f2a76)。完整预冻结参数和验收阈值没有随结果修订。

## 完整有限原词—隐sense模型

词符号A/B/C/D、两个人工时期0和1，每词每期各两种1/2概率的人工隐sense，九模型×2时期×4词×2隐sense＝**144条完整原来源**，全部正质量，每世界16条概率合计1。完整人工token质量`P(time,word,sense)=1/2×word_count(time)/12×1/2`，默认每期词计数(4,4,2,2)，频率改变世界的time1词计数(8,2,1,1)，各总数12。**144原类型不是144篇历史文档**。

固定3个非目标词原人工true sense向量A=(1,0)、B=(0,1)、C=(1,1)，目标D的两个底层隐sense为(0,−1)与(2,−1)，隐sense中心(1,−1)，其二维隐sense协方差矩阵为diag(1,0)。真正目标漂移世界将两个目标隐sense都沿x+1，中心变(2,−1)；重配置世界仅time1改成(1,−2)与(1,0)，平均中心仍(1,−1)但隐sense内部协方差变成diag(0,1)。这些hidden sense来源仅为人工设定，无真实语言意义验证。

实际观测在每时期的各词只有**两个隐sense平均后**的二维词嵌入值、词数频率、time和word ID；隐sense来源与真正变化Oracle只在科研复算中可见。世界中特别设定time1的**观察向量**可统一乘正交有理矩阵 `Q=[[3/5,−4/5],[4/5,3/5]]`（QᵀQ=I,det=1）或者统一乘尺度2，而真正隐sense与人工潜在词义可不变。跨时期对齐事前采用锚词A和B的两个time1观察列向量`H=[v_A,v_B]`求有理逆`H^−1`，使两锚词恢复基向量；这叫**事前固定两锚词线性校准**，不是原作者通用正交Procrustes优化算法，且两个锚词是否稳定本身正是本研究的检验对象。

## 独立积分、数学不变量与具体结果

第一路线直接用原16隐sense来源按time/word条件质量积分得到两期每个观察词2D向量，计算完整每期4×4共16格Gram内积、原目标D跨期平方距离、用两锚词H逆校准后的目标平方距离、每期词频加权词向量质心与跨期位移，以及人工oracle真正目标sense中心位移与内部sense协方差。第二条独立路线**不使用完整原来源行**，直接从冻结真实sense模板、词频变化和观察Q/尺度算每个word/time的2D观察中心、频率质心、所有Gram及hidden sense真协方差，与第一路线Fraction逐格相符。

| 人工世界 | 目标D对齐前平方位移 | 两锚词校准后平方位移 | 真实人工D隐sense中心平方改变 | 语料词频加权质心平方移动 |
|---|---:|---:|---:|---:|
| STABLE_BASE | 0 | 0 | 0 | 0 |
| GLOBAL_ROTATION | 8/5 | 0 | 0 | 4/9 |
| TARGET_SEMANTIC_DRIFT | 1 | 1 | 1 | 1/36 |
| ROTATED_TARGET_DRIFT | 5 | 1 | 1 | 17/36 |
| GLOBAL_SCALE_2 | 2 | 0 | 0 | 5/9 |
| FREQUENCY_COMPOSITION_ONLY | 0 | 0 | 0 | 1/18 |
| FREQUENCY_PLUS_TARGET_DRIFT | 1 | 1 | 1 | 13/144 |
| ANCHOR_DRIFT_FALSE_ALIGNMENT | 0 | 8/5 | 0 | 8/45 |
| SENSE_RECONFIGURATION_ALIAS | 0 | 0 | 0 | 0 |

“语料质心”在旋转、整体尺度模型中可能因**数字坐标表示**改变而变动，并不代表内容变化。质心变化只能在跨时间已具有可比较坐标和稳定词频目标的条件下才可能有语义含义；本表主要作为观察不同来源贡献的人工计算。

**全局坐标伪漂移与正确对齐：** GLOBAL_ROTATION仅将time1全部可见词向量乘Q，真正四词隐sense不动。time0/time1全部4×4 Gram严格相同，但直接比较同词D坐标平方位移是8/5。以预先固定且真实稳定的两个锚词A/B的精确逆Qᵀ对齐，D平方位移回到0。GLOBAL_SCALE_2把全部time1观察向量乘2，原目标未真实移动，未经校准D平方位移2；两锚词确定的线性尺度逆变换后为0，而time1全部Gram为time0的4倍。**正交不变性不能消除整体尺度，本文采用的线性H逆也不是标准正交旋转对齐。**

**真正目标漂移与坐标变换可分离：** TARGET_SEMANTIC_DRIFT真正D的中心从(1,−1)变(2,−1)，两稳定锚词保持不动，对齐前后平方位移均1。ROTATED_TARGET_DRIFT具有同一个真实变化，但全时点词向量还乘Q，其对齐前D平方位移升至5、正确校准后还原至1；这两世界time1的**完整4×4 Gram完全相同**，表示同一内积结构允许不同的坐标基表示。

**锚词污染制造假变化：** ANCHOR_DRIFT_FALSE_ALIGNMENT的time1仅锚词A/B本身乘Q，而非锚目标D和C实际坐标稳定，D未经对齐平方位移0。因为锚词变化，算法从H=Q得出“必须用Qᵀ校准”，使实际稳定的D被错误转换，报告平方位移8/5，而D原真sense中心位移仍0。此反例具体揭示依赖单独两锚且其本身移动的对齐机制可能产生**人为跨时期伪变化**。在这里存在独立第三词C和D可用来识别锚点失效，但只有在额外假设这些词稳定时这种诊断才有意义。

**频率组成与目标漂移可分离：** FREQUENCY_COMPOSITION_ONLY的四个词向量与全部隐sense跨期完全稳定、真正D变化0，单把count从(4,4,2,2)改成(8,2,1,1)就使词频加权全体质心发生平方位移1/18。FREQUENCY_PLUS_TARGET_DRIFT中频率与D真正漂移同时出现，质心移动平方量13/144，无法仅凭质心变化代数归因到唯一真实语义改变。词频亦不是独立语义知识证据。

**最强完全观察等价：** SENSE_RECONFIGURATION_ALIAS与STABLE_BASE的每个time/word的**完整可见词ID、频率和2D观察嵌入都一模一样**，整个`P(time,word,observable_vector,frequency)`完全相同、Gram一致、所有目标漂移统计均0。但SENSE_RECONFIGURATION_ALIAS的D在time1的两个潜在true sense点从(0,−1)/(2,−1)改成(1,−2)/(1,0)，同样聚合中心(1,−1)，隐sense二维协方差矩阵从diag(1,0)变成diag(0,1)；这是**人工潜在词义混合的内部几何变化**，单一词聚合向量本身不能检测。该隐真值属于构造参数，不能当作词义在真实历史上发生此类变化的证据。

## CI、永久来源与研究状态

[独立Python源码](r238_exact_historical_embedding_geometry.py) · [144条完整人工词—hidden sense原来源](R238_ALL_144_ORIGINAL_HIDDEN_SENSE_AND_OBSERVED_EMBEDDING_SOURCES.csv) · [九世界有理向量/Gram/锚点及source结果](R238_EXACT_RESULTS.json) · [SHA256源凭证](R238_FINAL_MACHINE_ACCEPTANCE.json)。

[GitHub Actions run39886353202](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39886353202)总体completed/success，三项job全部completed/success；Python3.11和3.12真实日志各`Ran 84 tests`及`OK`，**168次真正测试执行通过**。第三原来源归档job独立核验9×16源概率/唯一性、原词频及坐标、两期Gram、锚点逆变换、隐藏sense Cov、全观察等价、SHA256，真实输出`R238_ALL_144_HIDDEN_SENSE_ATOMS_AND_ROTATION_ALIGNMENT_FREQUENCY_ALIASES_VERIFIED`；机器人永久完整原资料提交 [e7ce8a83](https://github.com/edwardsage419/Psychohistory-Research/commit/e7ce8a838272ca89101ae9cc37264fae60fb7ac8)。

全原CSV SHA256 `a3939283f67d40fc74d289daecde449566870cdeb1943a8431ae6d27457feceb`；九世界JSON SHA256 `b0c408797bf9f4e9b5e7553e290d092b973c879d5dcbfe7dff50636ee1d1aa11`。

**不可外推范围：** 本R仅数学几何和人工测量生成式；没有真实语料共现建模、神经向量训练、语义标注、跨文化历史文本对齐、真实词义变化判断、任何已知历史研究复现或时间外预测。新增真人E2=0、真实历史E3=0；R073与PESEN v0.1保持冻结。下一原239目录 `10-013 Qualitative Comparative Analysis`（拟R239），须完成本文后从原目录再次核验。所有者研究顺序不变：全部原R研究→统一归纳分类→最后熔炼。
