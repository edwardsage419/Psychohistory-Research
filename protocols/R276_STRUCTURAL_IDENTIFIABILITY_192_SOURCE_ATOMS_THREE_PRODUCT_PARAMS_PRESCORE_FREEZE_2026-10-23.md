# R276 模型可辨识性：三个同产品参数点、两个观测通道、192完整原source；先冻结后计算

日期2026-10-23 Asia/Taipei。原239模型目录12-006 Model Identifiability（P0），研究R276。主要原文：Rothenberg, T.J. (1971), *Identification in Parametric Models*, Econometrica 39(3):577–591, DOI https://doi.org/10.2307/1913267；可公开核读原文 https://pages.stern.nyu.edu/~dbackus/Identification/id/Rothenberg_id_Econometrica_71.pdf 。另见观测等价的正式定义 https://pmc.ncbi.nlm.nih.gov/articles/PMC4978781/ 。本项自建有限参数可辨识性实验，没有复现原论文实证内容。

## 冻结机制与两种观测设计
三个固定参数结构θ=(θ1,θ2)：
* PARAM_A=(1/2,1/2)
* PARAM_B=(1/4,1)
* PARAM_C=(1,1/4)
全部都满足θ1·θ2=1/4。在每个模型下，首先生成四条Y_t独立Bernoulli(q=θ1θ2)，t=1,...,4；另生成两条潜在附加测量Z_s独立Bernoulli(θ1)，s=1,2；Y与Z相互独立。每个模型完整六bit(Y1...Y4;Z1,Z2)有2^6=64种原source，按q^K(1−q)^(4−K)θ1^J(1−θ1)^(2−J)精确概率；三结构共**192个完整带机制标识的人工原source类型**，包括结构PARAM_C在Z不为11时的零概率源，非零source共64+64+16=144。零质量原source仅用于形式全集，不是生成样本。

OBSERVE_Y_ONLY：看见四个Y的**整个联合分布**，三模型均相同，每种四bit Y来源质量q^K(1−q)^(4−K)，参数θ不可辨；等先验1/3 MAP所有Y观测并列按字母序选择PARAM_A。三真实结构条件正确率A=1，B=0，C=0；等权平均1/3。任何未来增大Y样本长度但不加新通道，因Y真概率始终产品θ1θ2=1/4，仍然不能在三参数中区分。

OBSERVE_Y_AND_Z：完整Y和两条Z；候选结构likelihood为Y联合质量×`θ1^J(1−θ1)^(2−J)`。Y因三个结构q相同而完全约去，分类结果仅由Z的二bit组成：
- Z=00：三个Z似然A=1/4、B=9/16、C=0，MAP选择B。
- Z=01或10：A=1/4、B=3/16、C=0，MAP选择A。
- Z=11：A=1/4、B=1/16、C=1，MAP选择C。
在三结构均等先验时，新通道MAP条件分类正确率：A有一半概率观察混合Z，因此1/2；B有9/16概率观察00，因此9/16；C必观察11，因此1；合计均等先验正确率(1/2+9/16+1)/3=**11/16**。非零参数点θ1互不相同，Y加Z的总体联合分布各不相同，因此这三个**离散候选结构在分布层面可辨识**；即便如此，样本仅有两条Z时分类仍有重叠错误，严格区别结构/全分布可辨识性与有限样本无误识别。

例示后验（等先验）：
- Z00：A4/13、B9/13、C0；
- Z01/10：A4/7、B3/7、C0；
- Z11：A4/21、B1/21、C16/21。
上述后验与观察的任意Y向量完全无关（因公共Y似然约去）。

## 两条独立数学路线及第三机器审计
路线A逐机制穷举六bit的全部64原source，记录Y四bit、Z二bit、六bit、真机制原质量、三候选对每种观测通道的likelihood与后验、每source MAP及是否分类正确（包括零质量占位）。准确Fraction来源积分两种方案机制正确率。
路线B不调用完整六bit source枚举，从四bit Y的Bernoulli(1/4)共同分布与三结构Z的Binomial(2,θ1)独立解析质量直接验证Y_ONLY等价和Z=00/混合/11三类别选择概率，得所有正确率和后验的冻结表达式。
路线C GitHub Actions独立第三job读取原CSV，核验全部192原source与zero support、精确概率、两种likelihood、后验与MAP、每机制质量和Y四bit边缘、所有封闭解析Fraction结论及SHA256。
必须先冻结本协议到main并引用SHA，再提交无第三方依赖执行器，Python3.11/3.12各≥45项真单测、第三独立来源审计、全192原CSV/结果JSON/SHA256永久GitHub归档，三job全部completed/success后才能E1有限正式结题。实验严格只涵盖三个离散参数点，**不能由此断言θ∈连续二维开区间上的全局可辨识**；无真人E2或真实历史E3，不改变R073和PESEN v0.1，按全R后分类熔炼顺序。下一原目录12-007 Model Misspecification Checks（拟R277）。
