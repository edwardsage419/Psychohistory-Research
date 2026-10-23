# R300 科学报告：02-008 HMM前向推断、完整隐藏路径验证与i.i.d.潜在状态负对照

日期2026-10-23 Asia/Taipei。原239候选项目 **02-008 Hidden Markov Model（P1）**。科学级别仅为**CLOSED_BOUNDED_E1_ARTIFICIAL_R300_HMM_FORWARD_FILTER**，没有真实人、动物或历史事件数据E2/E3，也未进行原作者声学分类效果的实证复现。

## 一手文献与理论归属

Rabiner (1989), *A Tutorial on Hidden Markov Models and Selected Applications in Speech Recognition*, *Proceedings of the IEEE* 77(2):257–286, DOI https://doi.org/10.1109/5.18626；[原始作者教程论文](https://web.mit.edu/6.435/www/Rabiner89.pdf)。该文综述了隐藏状态转移、观测发射、HMM前向概率计算、隐状态解码和参数估计的不同问题。R300只检验**已给定先验/转移/发射参数的前向后验过滤与下一期预测**，不实现Viterbi最大概率路径求解，不进行Baum–Welch的EM参数估计，不复现Rabiner论文的真实语音识别数据。

2026-10-18原239知识索引没有02-008的可靠主R来源。R297 Q Learning、R298 Model Based RL、R299 Model Free RL以及R063社会模仿学习的模型含状态变量，但没有直接构成以Rabiner HMM独立过滤为目标的受试者实证验证，故不会把这些模型的旧真人证据迁移作为R300新E2。

## 事前冻结合同与完全人工样本

[冻结完整研究协议](../../protocols/R300_HMM_FORWARD_FILTER_IID_NEGATIVE_CONTROL_128_SOURCES_PRESCORE_FREEZE_2026-10-23.md)，事前提交[ef56b01c](https://github.com/edwardsage419/Psychohistory-Research/commit/ef56b01c3c2b5da98e433f9d2fefdd61fd9028c3)，早于本体代码与结果。

两潜在状态H∈{0,1}、观测Y∈{0,1}，起始隐藏状态先验各1/2，观测与当前隐藏状态相同时发射概率3/4，不同时1/4。两个参数已给定的人工世界：
* **PERSISTENT_HMM**：下一隐藏状态与上一状态相同概率3/4；
* **IID_HIDDEN_NEGATIVE_CONTROL**：下一隐藏状态与上一状态相同概率1/2，表示实际独立潜在状态、无跨期记忆。

每世界穷举16个长度4观测字符串，每个字符串在长度1、2、3、4的四个时间前缀输出所有中间过滤状态，**2×16×4=128条完全标签化人工source**，不是128个独立受试者或独立观测轨迹。相同短前缀在多个完整4位字符串中出现时，归一化校验必须以**去重后的前缀**为计数单位，不允许把重复源行当成多个概率样本。全部采用Python Fraction精确分数。

每source包含完整序列、当前前缀、时点、转移持久性、发射概率、前向α_t(H=0/1)、观测前缀的完整联合概率、隐藏状态后验P(H_t=1|观测历史)、下一隐藏状态预测和下一观测为1的预测。

## 精确前向公式和独立验证

前向递推t1为先验1/2乘本期发射；其后将上期未归一化α经转移矩阵传播，再乘本期发射。每期观测证据L_t=α_t(0)+α_t(1)，后验α_t(1)/L_t。下一隐藏状态的预测由该后验×转移矩阵得到，下一观测的预测再乘发射矩阵。

第三方审计**完全不导入生产代码**，对每一个观测前缀穷举所有2^t隐藏路径，直接计算完整隐藏状态–观测联合质量，得到证据与后验；又穷举长度t+1的完整潜在路径以计算下一观测和潜在状态预测。结果与全部128个原source的前向递推值完全一致。两世界的每个时间t，所有去重观测前缀概率和均精确等于1。

### 同样最近观测、不同历史的概率反例

| 四期观察记录 | PERSISTENT HMM的末端隐藏状态1后验 | 预测第五期观察1的概率 |
|---|---:|---:|
| 1110 | **19/46**（约41.3%） | **11/23**（约47.8%） |
| 0000 | **3/22**（约13.6%） | **9/22**（约40.9%） |

两个历史最后观测均是0，但PERSISTENT模型仍利用以前的1或0形成不同的过滤后验和下一期预测。这是在**给定转移持久性3/4的人工世界**中的精确计算结果，不说明真实社会行为有该持久概率。

IID潜在状态世界中，任何时刻后验只取决于本期观测：观察1后H=1后验=3/4，观察0后H=1后验=1/4；无论之前观察，下一期观察1概率均=1/2。观察长度t的证据严格为(1/2)^t，作为没有历史影响的负对照。同样单期边缘观测概率两个世界均为1/2，故只比较单期频数不足以识别隐藏状态持续性。

**科学边界：** 这两个HMM的隐藏状态是人为标号，不表示客观心理类别；隐藏标签置换在相应重标记参数后不改变观测概率。原HMM适用假设需要独立评估，当前未对实际观察建立可识别性、分类效度、长期预测改进或任何因果机制。

## 完整原来源/代码、独立审计与验收

[原生HMM前向计算与394项真实单元测试](r300_exact_hmm_forward_filter.py)；
[128条原始完整观测前缀来源CSV](R300_ALL_128_ORIGINAL_HMM_PREFIX_SOURCES.csv)；
[两世界所有观测前缀后验与证据结果JSON](R300_EXACT_HMM_FORWARD_RESULTS.json)；
[完整CSV/JSON字节SHA256机器凭证](R300_MACHINE_RECEIPT.json)；
[独立穷举隐藏路径源码及16项逆向检验](../catalogue_audit/independent_r300_source_audit.py)。

[真实GitHub Actions run39927762571](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39927762571)三个job completed/success；Python3.11与3.12每个通过394项本体unit tests+16项独立审计，第三job重新跑全部hidden path穷举及SHA256并永久归档[commit38830d98](https://github.com/edwardsage419/Psychohistory-Research/commit/38830d98e6c12c891e5fc542903b39ca6976f4ec)。全研究新增真人/动物E2=0，历史E3=0；R073/PESEN v0.1继续冻结；原239科学全部完成尚未成立。
