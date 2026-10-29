# TH137 历史词义漂移、跨语言锚定与反证对照

研究及英文检索日期：2026-10-30（Asia/Singapore）。状态：THEORY_NOTE_BOUNDED。
目标键：(theory,HISTORICAL_SEMANTIC_DRIFT_CROSS_LANGUAGE_ANCHOR_NEGATIVE_CONTROLS,theory-v1,lexical meaning versus corpus composition and embedding geometry)。
基线main HEAD：c706ce309a242623bbbbae0321de8a310ad25683。
已读theory/INDEX.md、TH136、C007、R272 S68交接、开放Codex PR摘要及未合并同步协议。PR #1 R257 S53仍为待审查E1工程证据。本研究与R233/R234测量等值人工实验互补，已看先前结果，属于非盲态理论审阅；不改R协议或原始文件。

## 一、原始来源与实际阅读层级

S1 [A，直接审读开放原刊PDF引言、方法及结果] Hamilton WL, Leskovec J, Jurafsky D (2016), Diachronic Word Embeddings Reveal Statistical Laws of Semantic Change, ACL 54:1489–1501, DOI:10.18653/v1/P16-1141, https://aclanthology.org/P16-1141.pdf 。六历史语料、四语言、约两世纪，提出高频词变化较慢和多义词变化较快的条件性统计规律。
S2 [A，直接审读开放原刊PDF第2至5节、表1] Dubossarsky H, Weinshall D, Grossman E (2017), Outta Control: Laws of Semantic Change and Inherent Biases in Word Representation Models, EMNLP:1136–1145, DOI:10.18653/v1/D17-1118, https://aclanthology.org/D17-1118.pdf 。打乱年代与同年抽样对照揭示频率、SVD与多义性代理量的表示偏差，是S1的直接竞争证据。
S3 [A，直接审读开放原刊PDF方法、表1及结论] Fourrier C, Montariol S (2022), Caveats of Measuring Semantic Change of Cognates and Borrowings using Multilingual Word Embeddings, DOI:10.18653/v1/2022.lchange-1.10, https://aclanthology.org/2022.lchange-1.10.pdf 。罗曼语族和英语的同源词与借词；FastText跨语对齐不稳，mBERT在特定测试上较稳定；两组规模严重不平衡。
S4 [A，直接审读开放原刊PDF方法、表3、错误案例] Kutuzov A, Velldal E, Øvrelid L (2022), Contextualized language models for semantic change detection: lessons learned, DOI:10.3384/nejlt.2000-1533.2022.3478, https://aclanthology.org/2022.nejlt-1.9.pdf 。文档爆发、上下文变化和分词问题造成伪词义变化。
S5 [A，直接审读开放原刊PDF前3节、表1及表2] Schlechtweg D, McGillivray B, Hengchen S, Dubossarsky H, Tahmasebi N (2020), SemEval-2020 Task 1: Unsupervised Lexical Semantic Change Detection, DOI:10.18653/v1/2020.semeval-1.1, https://aclanthology.org/2020.semeval-1.1.pdf 。四语言、33队186系统、约10万人工判断，人工标注仍受语料与类别选择限制。
S6 [B，开放原刊摘要，PMC全文访问遇验证页] Pechenick EA, Danforth CM, Dodds PS (2015), Characterizing the Google Books Corpus: Strong Limits to Inferences of Socio-Cultural and Linguistic Evolution, PLOS ONE 10:e0137041, DOI:10.1371/journal.pone.0137041, https://pubmed.ncbi.nlm.nih.gov/26445406/ 。书籍与科学文本构成偏差。
S7 [B，ACL出版页摘要，未逐表阅读] Shoemark P, Liza FF, Nguyen D, Hale SA, McGillivray B (2019), Room to Glo: A Systematic Comparison of Semantic Change Detection Approaches with Word Embeddings, DOI:10.18653/v1/D19-1007, https://aclanthology.org/D19-1007/ 。全时间序列和对齐参考点影响检测。
S8 [B，PubMed摘要及作者PDF开头，未逐表复算] Garg N, Schiebinger L, Jurafsky D, Zou J (2018), Word Embeddings Quantify 100 Years of Gender and Ethnic Stereotypes, PNAS 115:E3635–E3644, DOI:10.1073/pnas.1720347115, https://pubmed.ncbi.nlm.nih.gov/29615513/ ，作者PDF https://gargnikhil.com/files/papers/garg_embeddings.pdf 。职业统计与语义关联具有描述价值，因果解释仍受语料代表性限制。

来源全部为非中文语言网站，检索日期同上。A级只覆盖已指明原刊段落，B级不视作全文阅读。无付费文献。

## 二、16项条件性理论命题、前提、机制及反证

TH137-01 [S1,S2] 前提为历史语料可比较。频率与变化率的负关联可能来自语言演化，也可能来自采样噪声；年代打乱后仍出现同向关联是反证。适用边界为所用语料和表示算法，未决为跨语言稳健性。
TH137-02 [S2] 前提为打乱年代保持总体用法与分箱大小。无历史变化仍有非零余弦距离；对照无法排除所有其他偏差。未决为作者与体裁聚类抽样影响。
TH137-03 [S2] 前提为表示维度固定。截断SVD重新引入频率依赖；原始PPMI关联较弱是竞争结果。未决为维度与训练种子敏感性。
TH137-04 [S1,S2] 前提为多义性代理量可靠。多义性与频率共同影响语境数量；打乱年代仍有多义性效应。未决为人工词义标签能否替代网络代理。
TH137-05 [S5] 前提为词义标签固定。新增词义与既有词义比例变化属于不同目标；cell示例区分二元与连续变化。未决为历史词典标准漂移。
TH137-06 [S4] 前提为文档来源可追踪。单篇文本集中出现会形成假语义簇；删去重复文档应削弱信号，但本轮未独立执行。未决为作者权重。
TH137-07 [S4] 前提为分词规则稳定。don’t被异常拆分导致don假变化；反证需重分词。边界为词形规范化可能也删除真实差异。
TH137-08 [S4,S7] 前提为至少三个时间切片。持续上下文多样性与暂时事件爆发可在两期数据中混淆；全序列与留一时期检验有帮助。未决为共同冲击。
TH137-09 [S3] 前提为词源关系与英语gloss可靠。跨语向量对齐偏差可冒充语义差异；FastText与mBERT对照提供竞争证据。边界为特定语系和模型。
TH137-10 [S3] 前提为借词与同源词样本可比较。组间规模相差约两个数量级，可能产生估计偏差；需匹配样本量再验证。未决为小样本方差。
TH137-11 [S5] 前提为人工标注作外部参照。OCR、词形规范化、体裁与时代覆盖差异影响跨语言可比性；人工一致性也不证明社会构念等值。未决为标注者漂移。
TH137-12 [S6,S8] 前提为出版文本代表目标人群。书籍作者、科学题材和职业构成变化均影响词向量刻板印象关联；需独立调查和人口统计反证。边界为相关性研究。
TH137-13 [S1,S3,S5] 前提为锚定词稳定。锚词整体漂移会导致跨期坐标标尺错位；更换锚词集和人工复核是反证。未决为无外部锚时的多解。
TH137-14 [S4,S5] 前提为文本体裁具有共同支持。题材分布变化可与词义变化观察等价；按体裁重加权、文档去重和人工复标是反证。未决为无重叠体裁。
TH137-15 [S3,S5] 前提为翻译等价与历史语言阶段可标记。借词和文化特有概念会破坏跨语言问卷锚定；双语专家独立释义可部分检验。边界为词典相似不保证心理量表等值。
TH137-16 [S1至S8，方法推断] 前提为文本可连接四层社会过程。个体表达、群体传播、制度筛选、历史语言变化共同决定观测语料；跨体裁、跨时期和外部行为负对照必需。未决为跨层因果识别。

## 三、8项公开原刊算术及人工反例审计

E137-01 [S2表1] PPMI+SVD单频率回归解释方差真实67%、年代打乱56%，差11个百分点；56/67≈83.58%。比例仅描述表内数值，不等于已证明83.58%的因果效应是假的。
E137-02 [S2表1] 标准化频率系数真实−0.91、打乱−0.75，差−0.16；差值不能自动视为净因果效应。
E137-03 [S2表1] 加多义性后解释方差真实68%、打乱60%，差8个百分点；相对单变量分别增加1和4个百分点。模型比较受条件限制。
E137-04 [S2表1] 未经SVD的PPMI单频率解释方差真实8%、打乱0%；表示算法选择对结论影响明显，仍不足以独立确认真实变化。
E137-05 [S3原刊] 英语gloss两种构造的平均余弦相似度0.61与0.67，相差0.06；不是准确率提高6个百分点。
E137-06 [S4原刊] indirectly与hold共现句1990年代27条、1980年代1条，来自特殊文本爆发。各年代总分母未取得，不计算真实发生率比。
E137-07 [S5表1] cell三义项前期12、18、0，共30；后期4、11、18，共33。phone义项0%变为18/33≈54.55%，chamber从12/30=40%变4/33≈12.12%。原刊示例，非本轮原始语料复算。
E137-08 [人工两种反例] 体裁A与B中某义项概率固定0.9和0.1；A的语料占比从20%升至80%，总体义项率从0.26升至0.74，变48个百分点，体裁内部完全不变。另一例中同一含义被独立嵌入坐标(1,0)与(0,1)，未对齐余弦距离为1，正确旋转后为0。两者均为人工构造，不是历史估计。

## 四、四层联系、竞争解释与验证清单

个体：词汇理解、态度、语言表达和问卷反应标准。群体：语义传播、社交网络和作者群构成。制度：出版审查、语料收录、档案数字化、OCR、翻译、教育及调查规则。历史：人口与体裁构成变化、技术及制度冲击、长期语义演化。以上联系为待检验假说，不能据此断言具体历史事件的因果机制。

必须同时保留真实词义变化、语料构成、词频和估计误差、锚词漂移、分词OCR、翻译、单文档爆发及制度共同冲击等竞争解释。未来最小验证设计：固定语料版本与抽样单位，真实年代对照年代打乱，按频率与体裁匹配，独立人工复标，检验锚词替换，留一作者和留一文档，跨期共同支持重加权，多期负对照，与外部独立调查或制度史材料比较。所有实验应预先冻结评分和失败标准，优先免费公开资源。

## 五、C、D与科研验收边界

C：2026-10-30 C007已完成并核读，今日保持只读；C008动态偏好留作未来日历增量。D：2026-W44 D002已有归档，保持只读。未接入用户个人健康、财务或关系数据，未开发决策产品。

本轮真实原始语料逐条复算0、词向量重训0、独立因果估计0、前瞻预测0。R系列E1/E2/E3新增均0。S2的反证不足以证明全部语义变化方法无效。SemEval公开基准入口已定位，尚未核验原始数据文件字节和使用条件。CI未运行，未引入费用。下一可执行专题TH138：历史语料抽样偏差与词义漂移的部分识别界，优先核验SemEval公开人工标注基准的文件级证据和体裁负对照设计。
