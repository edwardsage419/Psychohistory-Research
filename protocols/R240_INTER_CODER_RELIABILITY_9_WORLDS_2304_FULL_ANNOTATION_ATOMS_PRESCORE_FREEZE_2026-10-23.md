# R240 内容分析编码一致性：九人工二元标注世界、2304完整原来源、κ/α与正确率的不可识别；正式计算前冻结

日期2026-10-23（Asia/Taipei）。真实原239目录`10-014 Inter Coder Reliability Models`（P1），R240。原R全系列先学完，随后统一分类，最后熔炼；R073/PESEN v0.1保持冻结。只对人工文档标签E1机制研究，无真实双人历史材料编码样本、新真人E2/历史E3证据。

## 一手方法依据及限定
Cohen (1960), [*A Coefficient of Agreement for Nominal Scales*](https://doi.org/10.1177/001316446002000104), *Educational and Psychological Measurement* 20:37–46，定义校正编码者边际预期随机一致性的`κ=(Po−Pe)/(1−Pe)`。Krippendorff (2004), [*Reliability in Content Analysis: Some Common Misconceptions and Recommendations*](https://doi.org/10.1111/j.1468-2958.2004.tb00738.x), *Human Communication Research* 30:411–433，批判了对一致性系数的过度解释；Artstein & Poesio (2008), [*Inter-Coder Agreement for Computational Linguistics*](https://aclanthology.org/J08-4004/), *Computational Linguistics* 34:555–596，梳理语义注释的一致性估计与α/κ适用条件。本R仅用冻结有限二元编码和两名编码者，不推断真实文章标注内容有效性、独立词义语义共识或真正人类编码者行为。

## 九个人工世界与全部256原源
八个等概率独立二元外生源`T,U,E1,E2,E3,E4,E5,E6`，每世界2⁸=256完整原人工文章类型、全世界9×256=**2304条完整原源**，全部每行1/256。隐藏`T`是真人工二元概念值，`U`未用作实际测量混杂、保留独立原源位置；两名观察编码者A/B取0/1，另人工纳入标志S决定实际双人编码是否在资料集中出现，若S=0可见编码A/B记−1，真A/B仍仅在人工oracle。每个world保存8原源、T、真实两个编码、被选标志、实际可见两编码及1/256源质量。完整观察证据为`P(S, observed_A, observed_B)`和S=1的2×2编表，计算不得读取T或真实被排除来源答案。

1. `PERFECT_TRUTHFUL`：A=B=T，真编码各准确率1、观察完全一致。
2. `PERFECT_SYSTEMATICALLY_WRONG`：A=B=1−T，真编码各准确率0，完整实际观察联合P(A,B)与1**完全一样**，Po=1且κ=1；实际真准确性不可由相互一致判断。
3. `SHARED_SYSTEMATIC_ERROR`：A=B=T XOR (E1∧E2)，每名编码者真准确率3/4，Po=1且κ=1，**完整观察分布仍与1、2完全一致**。
4. `INDEPENDENT_QUARTER_ERRORS`：A=T XOR (E1∧E2)、B=T XOR (E3∧E4)，真准确率各3/4，Po=5/8且κ=1/4。
5. `BALANCED_INDEPENDENT_RANDOM`：A=E1，B=E2，各边际Pr(1)=1/2，Po=1/2、κ=0。
6. `RARE_POSITIVE_INDEPENDENT_RANDOM`：A=E1∧E2∧E3、B=E4∧E5∧E6，各边际Pr(1)=1/8，独立；Po=25/32比世界5更高，但Pe=25/32、κ仍0，显示高原始一致率在稀少正类下可来自边际组成。
7. `ASYMMETRIC_FALSE_POSITIVE`：A=T，B=T∨(E1∧E2)，A真准确1、B真准确7/8；观察Po=7/8、κ=3/4，两编码者标记正类边际不同。
8. `SELECTIVE_MISSING_DISAGREEMENTS`：真A=T、真B=T XOR(E1∧E2)，S=1当且仅当真A=B；全部原来源的真实两编码一致率3/4，但实际入选双编码仅占原来源3/4、观察入选Po=1、κ=1。完整可见S的缺失率提供选择风险警示；不得把选择后的完美一致性当全体可靠性。保留真实被删案例但不准传入实际κ。
9. `OPPOSING_CODERS`：A=T、B=1−T，Po=0、边际Pe=1/2、κ=−1，显示负的超随机一致性。

## 冻结观测统计与独立真值

A. 每world完整原源256行、各自概率1/256。观察2×2 `n_ab`只计`S=1`可见A/B（不查Oracle），`N=Σn_ab`，`Po=(n00+n11)/N`，`Pe=[nA0*nB0+nA1*nB1]/N²`，`κ=(Po−Pe)/(1−Pe)`。所有world期望`Pe<1`，可用Fraction精确。N是**256种等概率结构来源型的完整枚举行数**，并非真实样本量。
B. 附加明确有限编码字节版nominal Krippendorff α（不宣称其等于Cohen κ）：仅包含**两人均有答案**的N个单位，观察无序pair不同率`Do=(n01+n10)/N`，全部2N个编码符号中0标签数量m0、1标签m1，有限总体无放回机会不同`De=2m0m1/[2N(2N−1)]`，`α=1−Do/De`。与人口有放回基线的κ不同，有限修正不能隐去；所有world需验证De>0。若想推断含缺失记录的Krippendorffα必须另行建模，本R只对完整配对作α。
C. 独立第二路径**不读归档源记录**，通过直接遍历八位原比特及冻结决策函数`coder_decisions()`给出2×2独立发生次数，与source CSV计数逐格一致；从锁定的真标签T计算每名编码者准确率，仅在Oracle审计中使用，不进入观察一致性公式。其原生成式中同一个T和误差结构不意味着两个实际真人编码者独立。
D. 三观察等价世界PERFECT_TRUTHFUL、PERFECT_SYSTEMATICALLY_WRONG、SHARED_SYSTEMATIC_ERROR完整的`P(S,A,B)`逐格相同、κ与α=1，但真实标签正确率分别1、0、3/4。观察共识不充分识别内容正确性；该反例限制在人工隐藏T未有金标准观测的场景。
E. 对RARE_POSITIVE_INDEPENDENT_RANDOM，冻结观察Po=25/32、Pe=25/32、κ=0；BALANCED_INDEPENDENT_RANDOM的Po=1/2、κ=0，两个世界真可靠性均不高。名义α须由独立2N码数复算，不能与κ机械设成相等。
F. SELECTIVE_MISSING_DISAGREEMENTS全原源Oracle Po=3/4、入选Po=1、入选率3/4，κ报告必须附带选中率和可能的非随机缺失，不得将人工缺失风险归结到真实历史史料。
G. 用Python3.11与3.12各≥45测试，独立GitHub Actions第三job重新生成完整2304来源、每世界2×2表、三观察别名、随机高原始一致的κ=0、全样本与选中差、文件SHA256，并机器人永久入库main；真实CI成功和源完整归档后才提交报告及正式结题。
H. 不对任何真实人工标注中的歧义解决、文档内容效度、标注员训练、真假标准建立做结论。跨入原目录11-001 Ordinary Differential Equations预计R241，完成此项后从真实目录再核对。
