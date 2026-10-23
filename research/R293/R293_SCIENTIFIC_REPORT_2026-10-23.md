# R293 科学报告：Schwartz 十类价值的测量校正、共同评分风格与中心化相关性反例

日期：2026-10-23 Asia/Taipei。原始239候选目录编号01-016（P1），新增独立研究包R293。**只达到人工数学E1，未完成Schwartz原1992跨国真人研究、ESS PVQ21真实数据复算或文化普遍性检验。**

## 一、原作者来源与测量口径

Schwartz (1992), *Universals in the Content and Structure of Values: Theoretical Advances and Empirical Tests in 20 Countries*, *Advances in Experimental Social Psychology* 25:1–65, DOI https://doi.org/10.1016/S0065-2601(08)60281-6。Schwartz (2012), *An Overview of the Schwartz Theory of Basic Values*, DOI https://doi.org/10.9707/2307-0919.1116。Schwartz (2021), *A Repository of Schwartz Value Scales with Instructions and an Introduction*, https://scholarworks.gvsu.edu/orpc/vol2/iss2/9/。

重要的一手量表技术说明：[GESIS英文ESS Human Values Scale](https://zis.gesis.org/s/skala/Schwartz-Breyer-Danner-Human-Values-Scale-%28ESS%29?lang=en)：实际ESS PVQ21对21个题项按指定权重与编码生成十类价值分数；建议个人价值优先级比较时扣除个人全题均值，某些结构/内部一致性分析适合直接使用未中心化原始条目。必须区分研究目的与样本测量方式。**本研究十个槽位仅模仿“个人十种相对价值”的处理方式，没有任何真实PVQ21题项、受访者或原1992数据。**

## 二、R013历史归档去重

10月18日旧知识叠加表给01-016一个未核实的first_hand_source_id=R13，却同时标记无逐项研究链接。本轮重读仓库真实[历史R013原ZIP](../../archives/library-originals/心理史学_R013_正式研究包_2026-10-14.zip)，完整SHA256=`d18eaa9a721fe9850ba93590fd9c112be70ae7282e7cc7b1341ee53f2e265d8c`；完整7个成员逐项CRC PASS并全部按大小格式条件全文检索。七成员实际主要是《预注册指标与受试者单位审计》，没有Schwartz关键词命中，也无专属价值模型源码。依据[原始ZIP成员JSON取证](../../docs/R293_R013_ORIGINAL_ZIP_MEMBERS_SCHWARTZ_EVIDENCE_AUDIT_2026-10-23.json)与[真实成功CI](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39918778414)，**R013不应自动计为01-016独立研究证明**；该单档案有限搜索也不能证明历史其他所有文件从未提及Schwartz。

## 三、先行协议、数学世界与源级完整性

[R293预先冻结完整研究协议](../../protocols/R293_SCHWARTZ_TEN_VALUE_MEASUREMENT_2112_SOURCE_PRESCORE_FREEZE_2026-10-23.md)，GitHub提交[44ede9c4](https://github.com/edwardsage419/Psychohistory-Research/commit/44ede9c449b06fa221c51bdbbc2008c5492aed06)，早于源程序及任何结果。

两个人工总体，每人十个潜在槽位值V_i为0/1，加入独立共同评分风格S∈{0,2}，均为1/2概率。观测原始值X_i=V_i+S，个人中心化C_i=X_i−(ΣX)/10：

* INDEPENDENT：十个潜在值独立等概率取0/1，2^10×2=**2048条**全部原始来源；
* OPPOSED_PAIRS：五个潜在0/1位与另外五个逐位互补，2^5×2=**64条**全部来源。这个“第i项与i+5项”的人工配对不声称符合Schwartz原版十类的精确真实角度与实测对立强度。

每一世界所有来源质量恰好为1；共2112条独立带概率、潜在向量、原始向量、中心化向量的**人工配置**，不是2112位被试。Python Fraction逐源算全部10×10原始与中心化协方差矩阵，各100元素×2世界×2计分类型合计400项，第三不导入主模型的独立数学审计再次全部重算。精确差值X_i−X_j=C_i−C_j=V_i−V_j和ΣC_i=0在每一原source成立。

## 四、独立可复算发现与理论边界

| 冻结人工总体 | 原始评分同槽方差 | 指定两槽原始相关 | 中心化同槽方差 | 指定两槽中心化相关 |
|---|---:|---:|---:|---:|
| 10潜在价值独立 | 5/4 | **4/5** | 9/40 | **−1/9** |
| 指定五对互补 | 5/4 | **3/5（互补对）** | 1/4 | **−1（互补对）** |

在独立总体中，任意两个潜在槽位Cov(V_i,V_j)=0，却因共同S具有Cov(X_i,X_j)=Var(S)=1以及raw rho=4/5；个人中心化消除S后，各i≠j的Cov(C_i,C_j)=−1/40，rho=−1/9。后者是减去十维共用平均引入的闭合约束，**不能据此独立证明潜在价值有动机冲突**。

在人工互补配对总体中，互补潜在Cov=−1/4；共同S使原始互补Cov=3/4、rho=3/5，产生与潜在相反的表观正相关。中心化后原互补结构保留rho=−1，其他不成对槽位之间中心化Cov=0。这是按设定保证的世界，并不能验证现实Schwartz环状结构。

准确的研究结论是**共同评分风格和中心化操作都可能显著改变协方差矩阵，二者适用解释不同**。对真实ESS/PVQ21是否适用，以及跨文化测量不变性、被试水平推断、统计不确定性，均需使用真实问卷、正确项目映射与样本设计独立检验。本轮没有为任一真人/国家/历史案例计算效应量。

## 五、执行、原始来源保全与正式边界

[主程序及153项真实数学单测](r293_exact_value_centering.py)、
[2112全部原始人工source CSV](R293_ALL_2112_ORIGINAL_TEN_VALUE_STYLE_SOURCES.csv)、
[完整两世界协方差矩阵与Fraction结果](R293_EXACT_VALUE_CENTERING_RESULTS.json)、
[原CSV和结果JSON的SHA256机器凭证](R293_MACHINE_RECEIPT.json)、
[完全独立原source的13项逆向审计](../catalogue_audit/independent_r293_source_audit.py)。

[GitHub Actions run39918965106](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39918965106)三job completed/success；Python3.11及3.12每个运行153主单测、13项独立审计，第三独立作业再次重算全部来源与400协方差并归档源数据/JSON/SHA。[永久GitHub归档提交812d757f](https://github.com/edwardsage419/Psychohistory-Research/commit/812d757f95374495bb732c15d270be4f1de5334f)。

正式限定结论：**CLOSED_BOUNDED_E1_ARTIFICIAL_R293_STYLE_AND_CENTERING**。新增真人E2=0，历史E3=0，未证明Schwartz的十价值普遍性或个人价值理论效度，也不能把旧R013提级为01-016原文复现。R073与PESEN v0.1继续冻结；原R研究全面完成并逐项核验后才统一分类，最后进行模型熔炼。
