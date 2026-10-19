# R116：规范性社会影响——公开/匿名行为、声誉动机与信息线索的原文学习及合成分辨协议

日期：2026-10-19（Asia/Taipei）｜状态：在模拟计算与测试前冻结｜项目原候选 P0 03-005 Normative Social Influence｜研究 R116。
本项目仍执行“全部既定R系列逐项学习 → 统一分类 → 最后熔炼”；不更改R073冻结模型、PESEN v0.1或其它R任务已有实证结论。

## 1. 第一手文献与可引用的证据等级

1. Solomon E. Asch (1955), *Opinions and Social Pressure*, Scientific American 193(5):31–35, DOI 10.1038/scientificamerican1155-31。出版方原刊目录 https://www.scientificamerican.com/article/opinions-and-social-pressure/ ，高校收藏的原刊全文副本 https://web.mit.edu/curhan/www/docs/Articles/15341_Readings/Influence_Compliance/required_readings/1Asch_1955_Opinions_and_social_pressure.pdf；冻结前已经实读原印刷第33页（PDF第3页，零基第2页）及开头。原作者文字记录18次判线任务中12次安排一致错误多数，123名受试者、错误多数意见下约36.8%的选择随多数；这仅为作者发表的汇总叙述，**本项目没有原始逐人试次表**。论文引述公开判断、人的自我怀疑与趋同，但**仅公开回答与多数一致不代表必然是规范性压力**；感知证据变化、表态策略和从众动机在该来源叙述中并存。
2. Morton Deutsch & Harold B. Gerard (1955), *A study of normative and informational social influences upon individual judgment*, The Journal of Abnormal and Social Psychology 51(3):629–636, DOI 10.1037/h0046408；PubMed原索引 https://pubmed.ncbi.nlm.nih.gov/13286010/；文章摘要在APA出版预览与学术镜像说明实验含面对面与匿名判断条件。只记录摘要/出版元数据，不宣称已独立读取全篇方法表及原始逐人实验结果。
3. B. Douglas Bernheim (1994), *A Theory of Conformity*, Journal of Political Economy 102(5):841–877, DOI 10.1086/261957，作者本人发布的公开摘要 https://bernheim.people.stanford.edu/publications/theory-conformity ，Haverford大学所托管完整原刊PDF https://www.haverford.edu/sites/default/files/Bernheim1994.pdf 。冻结前实读原印刷第842–843页与原摘：个体效用包含自身内在偏好与声誉/地位，人们通过公开行动推断不可观测偏好，地位在作者原模型中依观察者对**类型的信念**决定，公开行动通过信念*间接*影响地位，作者的严厉非从众惩罚是均衡内生而不是直接原始给定。

不得将下述**研究者自构的固定公开不一致成本**称为Bernheim1994原文的Bayesian类型信念、信号博弈或动态均衡重现。不得以作者公布36.8%作为项目新E2拟合值，也不得把该百分比当全部参与者顺从概率。

## 2. 预设的两个可计算通道和结构

基准私有信号取0（偏好/私人证据支持行为0），隐含二元事实状态V，先验均匀，自己的私有信号准确率 p_self = 3/5；后验 Pr(V=1|私有信号0)=2/5。
外部人群报告的共同线索指向行动1。若信息通道打开，**假设这一条群体线索是条件于V与个人私人信号独立的单次二元信号**，强线索可靠性 p_group = 3/4。则Pr(V=1|自身0,线索1)=2/3（绝不能把多名行动/同源报告当多个独立信号；仅一条来源）。弱群体线索对照 p_group = 11/20，后验Pr(V=1|自身0,线索1)=22/49。
若信息通道关闭，**看到人群的报告不改变私人信念**，始终Pr(V=1)=2/5，这是本玩具模型的固定假设而非人类认知现实。

两种选择行为0和1的内在期望收益分别是(1-q)与q（正确预测V得收益1，错误0）。研究者设定外在社会地位损失：当且仅当已看见群体意见、回答是可归因的公开表达、本人行动与群体意见相反，扣除固定 c = 1/4；匿名或未见意见则地位损失0。取最大期望净收益；精确相等时保守选择行动0。**此c是外生固定惩罚示范，不能冒充Bernheim内生地位/社会均衡。**

冻结四种对照“自构机制”：
- NO_INFLUENCE：信息false、status cost 0；
- NORMATIVE_ONLY：信息false、status cost 1/4；
- INFORMATIONAL_ONLY：信息true、status cost 0；
- BOTH：信息true、status cost 1/4。

## 3. 冻结的2×2观察设计及反例

因素A：是否看见人群选择（C0 / C1）；因素B：本人回答是否向群体/评价者可归因公开（ANON / PUBLIC）；观察行为、潜在私人后验和群体来源假设必须严格区分。

在强线索p_group=3/4、固定私人信号0条件下，四格选行为1的指示（顺序C0_ANON、C0_PUBLIC、C1_ANON、C1_PUBLIC）事前精确预测：
- NO_INFLUENCE: (0,0,0,0)。
- NORMATIVE_ONLY: (0,0,0,1)。
- INFORMATIONAL_ONLY: (0,0,1,1)。
- BOTH: (0,0,1,1)。

公开看见一致多数后，规范性与信息性机制**都选择1**，故只有C1_PUBLIC格完全无法区别其动机。即使有完整强线索四格，纯信息机制与两通道机制行动仍完全一致，社会地位成本不可由这些选择识别；因此不可声称2×2必定完成一般意义的因果识别。

弱线索p_group=11/20时C1_ANON的纯信息/两通道选择均0；C1_PUBLIC的INFORMATIONAL_ONLY=0，而 BOTH=1，这在上述固定人工参数下揭示已添加的地位成本。但这不是“干预已实现因果识别”：实际需独立随机化/测量并验证群体可信度与信息来源、表达公开性、实验依从性和个体私有信念。

另冻结形式化门槛：如果在该玩具模型中不更新信念，则公开服从的临界地位成本为 d=(1-q)-q=1/5；c=1/4>d；c=1/5严格效用平局时按定好的tie规则选择0。经手工可推导，CI需单测验证。必须检查社会压力成本不影响私人后验，信念变化不必改变公开/匿名状态，cue absence使群体信号根本不进入推断。

## 4. 失败守卫和验收标准

标准库Python3.11，所有概率/成本仅Fractions.Fraction，p_self与p_group严格1/2<p<1；公开/是否有线索/是否启用信息均为bool；私人信号与公开群体意向为显式int 0/1，布尔不准伪装行动。原本信息来源独立是假设而非由模拟估出。非法输入严拒、后验合一、两个cue方向对称、强/弱线索解析后验、状态与行为相互独立等价反例、2×2四类冻结表、边界成本、同样行为差异潜在信念、被误当作多个独立群体信号的风险都纳入不少于30项合成/数学测试。

只能声明SOURCE_ANALYTIC_AND_SYNTHETIC_E0/E1知识学习完成，不得声明独立真人E2/前瞻E3、Bernheim原方程拟合、1955原数据复算、完整规范/信息影响因果分离。必须先运行并通过GitHub CI、由CI机器发布摘要和源代码文件SHA，再记 LEARNING_COMPLETE_BOUNDED_PRIMARY_SOURCES_AND_STATUS_INFORMATION_IDENTIFIABILITY。

成功失败均保存真实机器记录；阶段成果上传并读取main HEAD。下一研究仍在既定R候选序列上推进，最后才统一分类及熔炼。
