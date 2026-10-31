# TH187 有限群体条件随机化、平局概率与网络暴露映射误设

研究日期及英文来源检索日期：2026-11-01（Asia/Singapore）。状态：THEORY_NOTE_BOUNDED。目标键：(theory,PuelzBasseFellerToulis1910.10862v2026+BasseFellerToulis1709.08036+Schroeder2602.03459,theory-v1,conditional_randomization_ties_fixedK_misspecified_exposure)。非盲态：已阅读TH186、理论索引、C009、D002、近期main提交及开放Codex PR标题摘要。本轮研究为开放原稿审读与独立人工数学审计，未读取受试者数据。

## 原始来源与核验范围

1. [A，作者开放原稿直接阅读] Puelz D, Basse G, Feller A, Toulis P. A Graph-Theoretic Approach to Randomization Tests of Causal Effects Under General Interference. arXiv:1910.10862，2019年首次提交，网页版本标注2026-08-09。https://ar5iv.labs.arxiv.org/html/1910.10862 和 https://arxiv.org/abs/1910.10862 。阅读第2.3、3.1、3.2、4.1、4.2、5.1、7.3节和附录B.1。原始PDF访问超时，公式符号只核验了开放HTML，标记PDF_SYMBOL_CHECK_OPEN。
2. [A，作者开放原稿直接阅读] Basse GW, Feller A, Toulis P. Conditional randomization tests of causal effects with interference between units. arXiv:1709.08036，开放HTML显示2026-03-22更新。https://arxiv.org/abs/1709.08036 。阅读第1、2.1、2.3节。2019年正式发表为Randomization tests of causal effects under interference，Biometrika 106(2):487–494，DOI:10.1093/biomet/asy072。收费正式全文未逐页阅读。开放稿第2.1节使用包含平局的大于等于尾部，声明零假设检验水平上界。
3. [A，作者2026预印本直接阅读] Schröder M, Oprescu M, Feuerriegel S, Kallus N. Causal Inference on Networks under Misspecified Exposure Mappings: A Partial Identification Framework. arXiv:2602.03459，2026-02-03，https://arxiv.org/abs/2602.03459 。阅读摘要、第1、2、3.1和3.2节。同行评审状态及性能声明未独立验证。
4. [B，机构作者稿与正式书目] Athey S, Eckles D, Imbens GW. Exact p-Values for Network Interference. JASA 113(521):230–240，DOI:10.1080/01621459.2016.1241178。MIT机构开放稿 https://dspace.mit.edu/entities/publication/8ab135cd-0a3d-443e-aa8f-52ec2b18426b 。本轮访问受频率限制，只核验机构摘要与开放稿存在，未阅读全文。
5. [B，正式机构摘要] Aronow PM, Samii C (2017). Estimating Average Causal Effects Under General Interference, with Application to a Social Network Experiment. Annals of Applied Statistics 11(4):1912–1947，DOI:10.1214/16-AOAS1005。https://isps.yale.edu/resource/estimating-average-causal-effects-under-general-interference-with-application-to-a-social 。本轮复核摘要，TH186已阅读作者稿第1至3节。

来源全部为非中文网站。A表示直接阅读的开放原稿章节，B表示书目与摘要。不得将作者预印本视为经本项目独立验证的因果证据。

## 十八项条件性命题与反例

TH187-01 [原作] 网络干扰下，单位的潜在结果可依赖整个处理分配向量。已知随机化设计和暴露映射共同决定可插补的反事实结果。

TH187-02 [原作] 全局无效应锐原假设可使用通常的Fisher随机化检验。仅排除邻居溢出的假设一般无法对全部分配插补结果，需要条件化焦点单位及分配支持集。

TH187-03 [原作] Puelz等提出零暴露二部图与完整二部子图。只要原假设在所选焦点单位与分配集合上锐化，并使用正确条件分配概率，便可建立有限样本检验。

TH187-04 [原作] Basse、Feller、Toulis的条件机制允许根据观察到的分配构造比较集合。随意事后挑选显著的焦点或使用错误的条件权重可能破坏检验水平。

TH187-05 [人工设计] 8个节点中4个焦点永远不处理，另4个候选恰好随机处理2个。合法条件支持集大小C(4,2)=6。无溢出原假设使四个焦点的结果在六个分配下保持可插补。

TH187-06 [人工设计] 四个焦点结果固定为8、4、2、1，各自只连接一个不同候选。统计量为被处理候选对应的焦点结果之和，六个合法值精确为3、5、6、9、10、12。

TH187-07 [人工计算] 最大值12的保守上尾Pr(T>=12|C)=1/6。六种观察分配的p值恰为1/6至6/6。逐个阈值精确枚举满足零假设拒绝概率不超过阈值，未使用正态近似。

TH187-08 [原稿网页文本与人工反例] Puelz等2026-08-09 HTML第2.3节定理1和第4.1节式(8)使用严格大于号，而定理2写出对任意α的等号。若按无随机平局处理的严格上尾直接实现，最大统计量的p值为0，α=0时零假设拒绝概率却为1/6；α=1/6时拒绝概率为2/6。全平局时严格上尾全部p值为0。此为网页转写的数学表述核验风险，可能涉及PDF排版、平局随机化约定或版本差异。原始PDF尚未核验，不能据此断言正式论文有错误。

TH187-09 [方法竞争] 随机平局打破需要额外独立随机数及明示规则。离散且无随机化的含平局尾部一般只保证水平上界，不能承诺任意α下严格相等。

TH187-10 [人工设计] 将固定选2的四候选设计误当作四个独立Bernoulli(1/2)，支持集由6变为16，观察(4,5)的上尾从1/6变成1/4。两种随机化机制不能直接互换。

TH187-11 [人工计算] 固定选2时，两个不同候选处理指示量的协方差为1/6-1/4=-1/12。随机化名额竞争本身可以引入负相关。

TH187-12 [人工误设] 真实焦点结果仅在候选B处理时为1，分析者却将候选A视作唯一邻居。E[Y|A=1]=1/3，E[Y|A=0]=2/3，错误暴露对比为-1/3；真正B暴露对比为+1。人工结构中固定B并单独切换A的效应为0。固定名额与错误网络映射可共同制造方向相反的关联。

TH187-13 [2026预印本] Schröder等提出对暴露映射误设进行部分识别敏感性分析。实际使用必须检查网络已知、暴露概率、误设程度和相关识别假设。本文未拟合其界限估计器，也未独立验证作者性能声明。

TH187-14 [竞争解释] 正确的随机化p值只约束给定原假设下的误拒概率。它无法自动证明网络边正确、真实传播机制已识别或跨社会制度运输有效。

TH187-15 [功效边界] 六个等概率分配的保守单侧p值最小为1/6。此人工检验无法在5%阈值拒绝。焦点单位数、有效分配数、统计量选择和群体异质性共同影响统计功效。

TH187-16 [外推边界] 固定名额设计不包含所有候选同时处理，全面推广的政策结果没有设计正概率。历史网络变化及制度重组会进一步改变暴露关系。

TH187-17 [四层联系] 个体层是处理、感知与潜在结果；群体层是邻居传播和群体异质性；制度层是固定名额、分配规则和统计目标；历史层是网络重组、制度演化与外推边界。跨层解释均需要独立可反驳证据。

TH187-18 [伦理] 本轮仅使用开放论文和人工数学世界。没有读取个人健康、财务、关系或受限ICPSR数据，没有实施个人实验或开发决策产品。

## 精确计算与科学证据边界

脚本theory/th187_conditional_randomization_audit.py使用Python标准库fractions、itertools、unittest。24项测试在普通与python -O模式分别通过，共48次测试执行、0失败。覆盖支持集唯一性、焦点未处理、六个p值排序、超均匀性、严格尾部反例、全平局反例、错误Bernoulli支持集、固定K负协方差及错误网络暴露的负向关联。所有结果为明确构造的人工数学反例。

真实微观数据复算、独立现实因果估计、历史留出验证、前瞻预测均为0。R系列E1/E2/E3新增科学验收均为0。代码测试通过仅证明人工设定与实现一致。Puelz原始PDF符号核验仍开放。

## C、D日历及三轨协作

2026-11-01 C009已归档，原始blob核对后只读，不重复创建C010。2026-W44 D002已归档，原始blob核对后只读；2026-W45从11月2日开始。最新main读取包含R322 S118与MKT182，TH187目标与其他轨当前问题不重叠。Codex开放PR #1的R257 S53检查器缺口、#3候选修复、#2协作协议及其他开放PR均仅作未合并待审证据。

下一理论专题TH188：文化演化中的规范传播、身份边界与网络选择，优先阅读原始理论和开放实验，扩大跨学科覆盖。另保留2026原稿PDF的严格不等号核验任务。C下一研究日再检查C010，D下一研究周检查D003。先完成全部R系列，再统一归纳分类，最后模型熔炼。未主动触发CI或新增收费服务，GitHub免费额度和账户计费未核验。
