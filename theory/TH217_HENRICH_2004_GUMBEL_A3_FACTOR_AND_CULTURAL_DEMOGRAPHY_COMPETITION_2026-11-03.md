# TH217 人口规模与累积文化演化：2004年Gumbel原刊A3积分缺项及竞争证据

track: theory
subflow: main
run_date: 2026-11-03 (Asia/Singapore)
target_key: (theory,Henrich2004+Vaesen2016+HenrichEtAl2016+Fay2019,2004-original+2016-published+2016-author-accepted+2019-published,Gumbel-A3-normalization-vs-effective-learners-and-empirical-counterevidence)
status: ORIGINAL_FORMULA_IMAGE_CHECK_COMPLETE; MATHEMATICAL_CORRECTION_COMPLETE_BOUNDED; EMPIRICAL_LITERATURE_REVIEW_COMPLETE_BOUNDED; FORMAL_ERRATUM_NOT_VERIFIED
observed_main_before_write: fdf51d0ae145b9d8f6710b048110d18f454b0e97
source_access_date: 2026-11-03
CI: NOT_RUN
billing: new_paid_operations=0; account_and_free_quota=NOT_VERIFIED

## 1. 原著及实际读取范围

[A1] Joseph Henrich (2004), *Demography and Cultural Evolution: How Adaptive Cultural Processes Can Produce Maladaptive Losses: The Tasmanian Case*, *American Antiquity* 69(2):197至214, DOI 10.2307/4128416。直接阅读作者哈佛机构存档的原刊扫描，印刷pp197至205、209至210的正文、式(1)至(4)、附录A和附录B。**直接目视核验p201 Figure 1与p210原始影像的式(A3)、(A4)、(A7)**。其余页仅检索局部段落，未逐页全文审计。来源 https://coevolution.fas.harvard.edu/sites/g/files/omnuum5841/files/culture_cognition_coevol_lab/files/henrich_2004-2.pdf 。版权仍属原权利人；只链接，不复制PDF。

[A2] Krist Vaesen, Mark Collard, Richard Cosgrove, Wil Roebroeks (2016), *Population size does not explain past changes in cultural complexity*, *PNAS* 113(16):E2241至E2247, DOI 10.1073/pnas.1520288113。直接阅读埃因霍温理工大学机构存档的**正式出版PDF**，印刷E2241至E2245的理论假设、塔斯马尼亚考古争议、8项既有比较研究及讨论；其余尾页只核书目。来源 https://www.pnas.org/content/pnas/113/16/E2241.full.pdf 。

[A3] Henrich、Boyd、Derex、Kline、Mesoudi、Muthukrishna、Powell、Shennan、Thomas (2016), *Understanding cumulative cultural evolution*, *PNAS* 113:E6724至E6725, DOI 10.1073/pnas.1610005113。直接阅读UCL存档**作者最终接收稿2页**，尚未逐字对照正式出版排版。来源 https://discovery.ucl.ac.uk/id/eprint/1522548/1/Shennan_Understanding%20cumulative%20cultural%20evolution_final_revised_RPS.pdf 。

[A4] Nicolas Fay、Naomi De Kleine、Bradley Walker、Christine A. Caldwell (2019), *Increasing population size can inhibit cumulative cultural evolution*, *PNAS* 116(14):6726至6731, DOI 10.1073/pnas.1811413116。直接阅读斯特灵大学机构存档的**正式出版PDF**，印刷pp6726至6729的引言、方法、结果、Figure 1至3说明及Discussion。pp6730至6731仅检索局部，SI及OSF原始数据未读。来源 https://storre.stir.ac.uk/bitstream/1893/28993/1/6726.full.pdf 。原文声明CC BY 4.0。

[B] Vaesen等(2016) *Reply to Henrich et al.* DOI 10.1073/pnas.1613074113，仅核对正式书目和公开页面；**回复全文未直接阅读**。2004年正式勘误也未找到，不声称出版社已经确认错误。

## 2. 原刊p210可逐式验证的印刷问题

Henrich2004 p210式(A3)在原始扫描中印刷为：

z_h = N ∫ x exp((a−x)/β) [exp(−exp((a−x)/β))]^N dx，积分范围为负无穷至正无穷。

这是最大值密度积分，但其被积函数**缺少1/β因子**。对标准参数化的Gumbel分布，F(x)=exp[−exp((a−x)/β)]，β>0，独立抽取N个样本的最大值M的分布为F_M(x)=F(x)^N，故

f_M(x)=(N/β) exp((a−x)/β) exp[−N exp((a−x)/β)]。

所以正确的期望最大值积分应是原刊(A3)的1/β倍。原刊(A7)沿用同一个积分表达式，因此也继承该归一化缺项。**这是对印刷积分的数学审计，不推断作者实际数值程序一定采用了错误表达式**。

进一步利用Gumbel分布的最大值封闭性：

F_M(x)=exp{−exp[−(x−(a+β ln N))/β]}，
E[M]=a+β(γ+ln N)，其中γ≈0.5772156649。

这正是原刊(A4)的结果。在**独立同分布且参数化如上的Gumbel假设内**，(A4)是精确恒等式；原刊将其称作高精度近似，属于可收紧的数学措辞。离开iid Gumbel假设，不能宣称其仍精确。

具体反例取(a,β,N)=(4,2,100)。原刊(A4)给14.3647717018；按原刊印刷(A3)直接积分给28.7295434036；补回1/β后给14.3647717018。原刊Appendix B称参数范围3<a<12、0.1<β<5、10<N<10000时(A7)误差不超过10^−14。**上述参数位于该范围内，印刷积分却有约14.3648的差异**。β=1时缺项恰好不可见。原刊p210原始影像已目视确认；正式勘误是否存在保持OPEN。

使用Python标准库独立有限区间中点积分脚本 `theory/th217_gumbel_integral_audit.py`，在(a,β,N)=(4,1,100),(4,2,100),(4,0.5,100),(5,1.7,25)的4组人工参数上，8项积分恒等式检查及3项扩展反例检查全部PASS。有限积分容差1e−6；解析推导不依赖该数值测试。此处**没有真人行为实验、历史参数拟合或预测验证**。

## 3. 原模型机制与有条件反例

Henrich2004正文p202式(2)在固定α、β及完全识别最优示范者等条件下：

Δz̄ = −α + β(γ+ln N)。

其中N是可以相互学习的**有效示范者池**，并非人口普查人数；α表示模仿误差的模态偏移，β表示误差分散度。2004原文p202以塔斯马尼亚人口约4000人为起点，经劳动分工、年龄假设粗估N约800，不能将800当成直接测量值。不同技能具有不同α/β，模型没有宣称所有技能同速退化。

构造性条件扩展：若观察过多示范者使学习损失随规模增加，设α(N)=1/2+2 ln N，β=1，则

Δz̄(N)=γ−1/2−ln N。

N=1时约+0.077216；N=4时约−1.309079。若仍固定α=1/2，N=4则预测+1.463510。故**规模增加的单调优势依赖学习误差不随候选数量恶化**。这个α(N)是本轮构造假设，既非2004作者的原模型，也非2019实验拟合出的函数。现实是否如此，需随机操作候选数与注意时间后检验。

## 4. 竞争原作与不同层级证据

Vaesen等2016正式论文ppE2242至E2244指出，最优示范者选择（Best）及将技术复杂性等同于复制难度是可争论假设；在其汇总的8项比较研究中，仅2项支持人口规模与技术复杂性的正相关。其塔斯马尼亚考古论证认为，骨尖消失不代表篮筐、独木舟、仪式与其他技能同步丧失。8项为**作者文献审查结果**，本轮没有独立核验八套底层数据。其反对意见也不构成一切人口作用为零的证明。

Henrich等2016作者接收稿pp1至2反驳：有效文化人口规模与人口普查人数不同，技能偏向学习和跨群体连接有独立实验与田野证据；他们引用不同机制模型及实验。该回应为竞争原著，不能因为作者立场而忽略。Vaesen等同年进一步回复已确认书目，正文尚未阅读。

Fay等2019正式实验共543名参与者，纸飞机任务设置个人重复学习、1、2、4名上一代示范者。原刊p6727报告从第1代至第8代的飞行距离变化分别为+1.38、+1.21、+0.22、−0.23米（按上述四条件顺序）；2和4示范者条件未检出显著改善。较多示范者提供更多变异与较佳样本，仍可能伴随较低复制保真度。作者探索性解释涉及工作记忆负担、复杂度和协调问题，**未随机隔离这些中介机制**。原文指出个人学习条件每人实际制作8次，社会学习条件每人只制作1次，直接比较受任务经验不等价限制。25项离群观测占分析数据3.29%，不可误称占543名独立参与者3.29%。论文原始数据与R脚本虽列OSF地址，本轮没有运行。

证据层级：2004数学印刷审计为原刊图像加独立推导；2016为竞争理论及历史文献解释；2019为原作者已发表真人实验结果的直接阅读。本轨**未复算真人数据**，不能将这些来源提升为R轨新增E2/E3。考古材料的保存偏差、不同技术复杂性口径、文化网络规模、生态与迁移选择及技能分工仍未独立识别。

## 5. 覆盖、冻结与下一步

补强考古人类学、文化传播、人口网络、数学极值分布、技能复杂性定义及认知负荷竞争机制。与TH188频率从众与网络同质性仅局部关联，目标键不同；无项目级分类与熔炼。

C011: COMPLETE，2026-11-03，已回读，仅检查，无新增C编号。
D003: COMPLETE，2026-W45，实际2026-11-02，已回读，仅检查，无新增D编号。
R状态：main最近R127原始表审计，R272生产P0仍需独立验收；R073和PESEN v0.1冻结。R E1/E2/E3及MARKET等级均未变化；Codex开放PR未经合并不计入main。
CI: NOT_RUN；新增收费操作0；GitHub免费额度与账户计费NOT_VERIFIED。

next: 寻找Henrich2004正式勘误或作者代码/独立发表的A3公式校正；直接读Vaesen2016回复全文和Fay2019 SI，尤其核实注意时间、学习次数及复制保真度测量。之后轮换其他弱覆盖学科。严格先完成全部R系列，再统一分类，最后有条件熔炼。
