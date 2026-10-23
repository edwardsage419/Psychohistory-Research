# R237 潜在语义主题模型：九个人工collapsed LDA世界、1944条完整来源与主题标签及先验非识别

日期：2026-10-23（Asia/Taipei）。原239目录真实 **10-011 Topic Models（P2）**。科学结题范围 **CLOSED_BOUNDED_E1_FINITE_ARTIFICIAL_COLLAPSED_LDA_IDENTIFICATION**。所有结果为完全人工有限离散词典的精确Dirichlet模型积分，不涉及真实历史文本、中文语义词典、跨时代语料、拟合优度估计或样本外预测评价，新增真人E2/真实历史E3均0。

## 一手原论文及前置冻结

Blei, Ng & Jordan (2003), [*Latent Dirichlet Allocation*](https://www.jmlr.org/papers/v3/blei03a.html), *Journal of Machine Learning Research* 3:993–1022，[原全文](https://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf)。原论文第三节定义每篇文档的Dirichlet主题比例θ、各token的隐主题z与词分布β；本研究限定词数N=3，并对θ做**精确Dirichlet积分**，不涉及原作者的变分EM或真实数据拟合。Hofmann (1999), [*Probabilistic Latent Semantic Analysis*](https://www.iro.umontreal.ca/~nie/IFT6255/Hofmann-UAI99.pdf), UAI'99，作为主题与共现潜在类方法的历史前驱。本研究没有复算Hofmann的tempered EM或经验文本结果。

明确的[计算前研究协议](../../protocols/R237_TOPIC_MODELS_9_COLLAPSED_LDA_WORLDS_1944_ORIGINAL_ATOMS_PRESCORE_FREEZE_2026-10-23.md)先于代码、CI及结果独立提交 [9551877b](https://github.com/edwardsage419/Psychohistory-Research/commit/9551877b185684dadf163de8c620acce4a80e939)。九世界参数、闭式协方差预测值、标签互换和非识别目标均在前置协议冻结，没有根据运行结果事后改变。

## 原结构来源及两条数学验证路径

固定每个文档三个有序词位置、三种无语义词符号0/1/2、两种纯数学隐主题0/1，每世界8个完整隐主题位置序列×27个实际有序词序列=**216条真实人工结构原来源**，九世界合计1944条。各world源`P(z,w)`用Fraction精确计算，全部严格正、各世界合计概率1。这些**是结构概率类型，不是1944篇历史文献或独立抽样语料**。

真机制：`θ∼Dir(α0,α1)`，z位置条件独立给定θ，w位置在固定z条件下以冻结β采样。θ积分后每个z序列质量`(α0)_{n0}(α1)_{n1}/(α0+α1)_3`。第一路线逐216种原源积分得27个`P(w1,w2,w3)`。完全独立第二路线不读取原来源，将θ积分换成顺序Pólya urn预测乘积`∏_i(α_zi+n_zi,before)/(α0+α1+i)`，再乘以对应β并对8种z和求各w质量，**全部27个词组合在9世界逐格一致**。

单个词0概率`p0=Eθ0·β0,0+Eθ1·β1,0`，同一文档第一和第二词是否为0的联合协方差`C00=Var(θ0)·(β0,0−β1,0)^2`，其中`Var(θ0)=α0α1/[(α0+α1)^2(α0+α1+1)]`。直接来源矩与这个独立解析公式逐世界严格一致。全部词序列概率在长度3固定的LDA下逐词位置置换严格相同（交换性），但共现Cov非零时并非边际独立，**不能据此宣称自然语言词序被成功建模**。

## 九个冻结世界：词0共现、边际和预测

| 人工机制 | 第一词为0边际 | 同文档前两位置0的协方差C00 | 前两词为0时第三词0的预测率 |
|---|---:|---:|---:|
| BASE_TOPICS | 1/3 | 1/108 | 5/13 |
| LABEL_SWAP_ALIAS | 1/3 | 1/108 | 5/13 |
| DUPLICATE_TOPICS_A | 1/2 | 0 | 1/2 |
| DUPLICATE_TOPICS_B | 1/2 | 0 | 1/2 |
| CONTRASTED_TOPICS | 5/12 | 1/48 | 85/168 |
| ALPHA_CONCENTRATED | 1/3 | 1/324 | 13/37 |
| ALPHA_SPARSE | 1/3 | 1/54 | 3/7 |
| UNIFORM_WORDS | 1/3 | 0 | 1/3 |
| ASYMMETRIC_ALPHA | 5/12 | 1/240 | 167/384 |

**完整观察等价一：标签切换。** BASE_TOPICS中`β0=(1/2,1/3,1/6)`、`β1=(1/6,1/3,1/2)`；LABEL_SWAP_ALIAS将两个主题标签及β整行对调，α=(1,1)不变。每个隐藏来源的主题指派z换成逐位互补z'后，`P(z,w)`与新模型`P(z',w)`严格逐来源相等；所以完整27个有序三词观察概率完全相同，尽管标签0现在表示原本标签1的统计词分布。以固定`w=(0,0,0)`为例，BASE`P(z=000|w)=27/40`，LABEL_SWAP`P(z=000|w)=1/40`；原因只是标签互换，其对应z'=111的后验在后者恰为27/40。由此不能把跨时期主题编号相同当作同一真实概念连续性证据，必须进行有理据的主题对齐。

**完整观察等价二：重复主题与不可见的Dirichlet先验。** DUPLICATE_TOPICS_A/B的两主题β完全相同，均为(1/2,1/3,1/6)，但α分别(1,1)与(3,1)。它们对全部27个有序文档的联合概率逐格相同，相同词在文档内边际独立，C00=0，第三词条件预测仍为1/2。然而真隐主题分配`P(z=000|w=000)`分别1/4和1/2，反映先验改变但全部可见词没有改变。故一旦两个主题的词分布真正重复，仅凭词语数据无法决定主题内部比例先验或这些重复主题应怎样划分。**这不是一般有区分词分布主题模型中α必然不可识别的证明。**

**相同词频但不同文档内依赖：** BASE、ALPHA_CONCENTRATED、ALPHA_SPARSE均使用相同的β、且α0=α1，故词0单词边际概率同为1/3。然而α=(4,4)的C00=1/324，α=(1,1)的C00=1/108，α=(1/4,1/4)的C00=1/54。观察相同两个词0后，第三词预测概率分别13/37、5/13、3/7。单一总体词频丢失文档内聚集信息；完整短文档联合能在**此已固定不同世界**检验这些共现结构，但不等于现实历史中已恢复唯一的语义主题数量与性质。

CONTRASTED_TOPICS增加两主题词0概率差，C00增至1/48；ASYMMETRIC_ALPHA改变总体主题权重、词0单词率升至5/12；UNIFORM_WORDS两个重复主题β都为均匀(1/3,1/3,1/3)，全部27个有序文档概率精确1/27。这些人工结果显示描述性词频、文档共现、主题先验与完整潜在分配属于不同层次的证据。

## 真实执行、源哈希与科研边界

[原生Fraction源码](r237_exact_collapsed_lda.py) · [1944条完整隐主题—观察词结构原CSV](R237_ALL_1944_ORIGINAL_LATENT_TOPIC_WORD_ATOMS.csv) · [九世界完整原概率及联合结果JSON](R237_EXACT_RESULTS.json) · [SHA256机器收据](R237_FINAL_MACHINE_ACCEPTANCE.json)。

[GitHub Actions run39885530463](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39885530463)总体completed/success，三个job均completed/success。Python3.11和3.12的实际日志各`Ran 96 tests`，`OK`，共**192次双版本真实单测执行成功**。第三独立原档审计确认每世界全部216不重复的(z,w)正概率原类型、完整质量1、每源`P(z,w)=P(z)P(w|z)`、观察全部27格归一、文档内位置交换性、两个全观察别名、九世界独立cov公式、预测顺序，以及原CSV与JSON文件SHA；日志真实输出`R237_ALL_1944_COLLAPSED_LDA_SOURCES_TWO_FULL_ALIASES_AND_DIRICHLET_PAIR_COVARIANCES_VERIFIED`。随后机器人永久源归档提交[a718dd9c](https://github.com/edwardsage419/Psychohistory-Research/commit/a718dd9cfb82b461f9e77f73524c264327451ed0)。

完整原CSV SHA256 `8fb107920ffa30de566ed8a67937f57255f02cbc6819323d752a3e6dd8b4f442`；完整九世界结果JSON SHA256 `791647faf7cf872c4af52dfaeabee5e1b4a0259b21db8817c8eb25f4e92f08ef`。

本研究仅人工三词文档长3、K=2、V=3、α和β全部已知、精确概率而非实际观测抽样，因此**没有实现通常历史语料主题推断所需的topic学习、模型选择、持出文本预测、历史词义标定、语义解释或人类编码一致性检查**。新增真人E2=0，真实历史E3=0，R073/PESEN v0.1冻结。

下一原239目录`10-012 Historical Text Embeddings`，拟R238。坚持先完整完成原R，再统一归纳分类，最终熔炼。
