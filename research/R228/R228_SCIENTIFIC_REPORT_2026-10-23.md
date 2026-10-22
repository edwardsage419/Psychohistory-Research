# R228 项目反应理论：八个有限二元IRT模型、384条完整人工结构来源与独立新题预测

日期：2026-10-23（台北时间）。对应原始239目录 **10-002 Item Response Theory（P1）**。科研状态：**CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_ITEM_RESPONSE_THEORY**。仅对八个人工生成世界构建可复核的Fraction数学证据，不产生真实人类心理量尺或真实历史因果预测E2/E3。

## 原始方法依据与冻结顺序

Birnbaum (1967), [*Statistical Theory for Logistic Mental Test Models With a Prior Distribution of Ability*](https://www.ets.org/research/policy_research_reports/publications/report/1967/hpod.html)（ETS Research Bulletin RB-67-12），官方原摘要讨论贝叶斯能力后验、观测题型与得分及其矩。Rasch (1960), *Probabilistic Models for Some Intelligence and Attainment Tests* 的等区分度模型，以及 Lord/Novick/Birnbaum (1968) 对两参数模型的历史贡献，为模型机制定位；本轮不声称已取得原作者全部图表/底层人级资料并端到端复现。

本轮严格先行冻结[八世界原始机制、预测目标及验收协议](../../protocols/R228_IRT_8_WORLDS_384_ORIGINAL_RESPONSE_ATOMS_PRESCORE_FREEZE_2026-10-23.md)，独立提交 [ed9aa23b](https://github.com/edwardsage419/Psychohistory-Research/commit/ed9aa23bfb634beb9dbf1aa1efb1cbb6ab4711da)，随后才提交源代码、测试和机器结果。冻结八世界、三项目的二元响应、六种(group,ability-index)均匀结构来源、固定未来第四题及其Brier风险比较均未事后更换。

## 有限原源与精确logit

每世界可观察群体G=0或1各先验1/2，潜在能力索引k∈{-1,0,1}各先验1/3，三道题完整响应y∈{0,1}³共有8格，因此每世界2×3×8=48原结构源，八世界**384**结构格。通常IRT条件独立模型采用精确底数2的logistic概率 `P(Yj=1|θ,G)=2^{aj(θ−bjG)}/(1+2^{aj(θ−bjG)})`，其中θ及bjG为特定有限整数，这仅是把线性预测量以ln2为单位标定。所有机率皆可用分数严格表示。LOCAL_DEPENDENT_CLONE让第三题直接复制第一题，因此同一有限(g,k)条件下有一半潜在反应格不可能出现，保留24条零概率结构格。384结构格中实际正概率格**360**；结构性来源行不能混称384真人测试或384次随机实测。结果JSON与CSV每行保留G、潜在k、人工真θ、三个实际答案、总分、理论项目概率、原来源概率以及零质量标记，保证观察与人工oracle界线可核查。

## 原序八世界结论

| 世界 | 总分充分性违反格数 | G间第二题DIF | 新题完整模式Brier | 只用总分Brier |
|---|---:|---|---:|---:|
| BASE_RASCH | 0 | 无 | 73/296 | 73/296 |
| LOCATION_SHIFT_ALIAS | 0 | 无 | 73/296 | 73/296 |
| TWO_PARAMETER_UNEQUAL | 12 | 无 | 9913/40600 | 93791/383264 |
| DIF_SECOND_ITEM | 0 | 有 | 12915380163381/52357556443664 | 相同 |
| EQUAL_ITEM_DIFFICULTY | 0 | 无 | 1778339/7217100 | 相同 |
| LOCAL_DEPENDENT_CLONE | 0 | 无 | 394535/1593648 | 相同 |
| SCALE_HIGH_DISCRIM | 0 | 无 | 761/3144 | 761/3144 |
| SCALE_LOW_DISCRIM_ALIAS | 0 | 无 | 761/3144 | 761/3144 |

**充分性对照与独立预测**：Rasch各世界在固定群体G与总分S的条件下，具体三题响应模式概率完全不依赖潜在θ；每格从原完整来源的条件比例求出，又独立使用`P(y|S,G) ∝ 2^{-a Σ_j bjG yj}`精确相符。后者是对全部三题采用相同区分度a、条件独立的特殊形式。TWO_PARAMETER_UNEQUAL的第二题区分度设为2，其余为1，因此同一总分下不同项目模式保留θ信息，观察模式条件随θ变化的格共**12**个。

同一人工结构中的第四道未来题在给定潜在索引k下按固定`P(Z=1|k)=2^k/(1+2^k)`独立生成。已知固定模型参数后，按完整模式/G生成的Bayes预测Brier风险为`9913/40600`，按总分/G为`93791/383264`，完整模式改善为**183/330400**。两项未来风险均经直接枚举Z=0/1得分与独立条件误差恒等式`E[(Z−p)^2|k]=q(1−q)+(q−p)^2`逐源完全核对。Rasch世界两种预测风险严格相同。这里属于在人工生成分布已知条件下的真正独立新题概率风险计算，未用实际人类留出样本，E1等级不晋升。

**能力原点与量尺别名**：BASE_RASCH与LOCATION_SHIFT_ALIAS通过θ和全部难度同时平移+1，完整可观察P(G,Y1,Y2,Y3)及逐k条件响应分布完全相同。SCALE_HIGH_DISCRIM的区分度整体为2、θ及难度网格{-1,0,1}；SCALE_LOW_DISCRIM_ALIAS改用区分度1、θ及难度网格{-2,0,2}，得到同样的完整观察概率。两个等价对说明潜在能力数值原点与尺度需由外部锚定才能报告为绝对量尺。两组等价对是真正数学重参数化，不能误标为互斥的心理因果机制。

**DIF与局部依赖**：DIF_SECOND_ITEM两群体被设定为具有同样的能力索引先验，但G1第二题的固定难度更高。因此跨群体第二题呈现真实人工差异，然而分别在每个群体内总分对潜在能力仍满足该Rasch构造的条件充分性。LOCAL_DEPENDENT_CLONE第三题复制第一题，各个(g,k)条件下第一与第三题协方差严格正值，违反局部独立；在其固定三题形式中**总分唯一确定所有正概率可见模式**，故条件模式对θ不变的检验仍为0违反。这个额外反例表明总分充分性测试通过不能单独验证项目条件独立结构，须分别检查两个假设。

## 冻结执行、机器与独立验收

1. [原生Python标准库源码](r228_exact_item_response_theory.py)、[384完整原结构来源CSV](R228_ALL_384_ORIGINAL_IRT_RESPONSE_ATOMS.csv)、[八世界Fraction结果](R228_EXACT_RESULTS.json)、[SHA机读凭证](R228_FINAL_MACHINE_ACCEPTANCE.json)。正常概率均使用Fraction，无logistic浮点拟合、参数搜索或真实受试者数据。
2. [GitHub Actions run39812796743](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39812796743)：run完成且结论success，三个作业completed/success；Python3.11/3.12各实际跑`Ran 61 tests`并返回`OK`，合计**122次测试执行通过**。第三作业真实输出`R228_ALL_384_ARTIFICIAL_IRT_SOURCES_AND_INDEPENDENT_PREDICTION_VERIFIED`，独立核验结构源数量、两对观测别名、Rasch总分/2PL预测差、DIF及SHA。
3. 完整原资料已由机器归档提交[81148f11](https://github.com/edwardsage419/Psychohistory-Research/commit/81148f1172190ee969f7f66e23da125e4fb387b4)。原CSV SHA256为`a806be476e230266787eabd167f2751ab751af9b537085bf598d1ebbec219901`，结果JSON为`663d174186dd1f33463fb60be3ed33ab03c09928f309409d47436040cd8fea76`。

## 有界解释和下一模型

全部只有人工E1，不包括真实测验受试者、题型对实际人群效度、能力与环境的交互、学习迁移、跨文化差异、猜测参数估计、真实自动测验适应性或真实历史决策预测。冻结的未来第四题生成和已知概率模型使独立预测有严格解析可检验性，但不能外推现实评分优势。新增真人E2=0、真实历史E3=0，R073和PESEN v0.1不变。

下一条经原239目录确认应为 **10-003 Rasch Model（R229）**。继续完成原R系列后统一归纳分类，最终才进行模型熔炼。
