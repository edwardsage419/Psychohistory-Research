# R128 猎鹿博弈：合作阈值、群体相关性与重复博弈的转换——计算前冻结

日期2026-10-20。既定目录 P1 05-004 Stag Hunt Game。上轮R127已核验一般二人收益/风险占优，本次独立新增：原著印刷猎鹿收益及信念阈值、全员合作的n人扩展与联合信念、重复囚徒困境折现转换以及明确限定的离散群体动力学。先学完既定R系列后统一分类、最后熔炼；R073/PESEN v0.1继续冻结。

## 第一手文献的真实访问范围

Jean-Jacques Rousseau, Discourse on the Origin of Inequality (1755)，原法文逐段原文 https://athena.unige.ch/athena/rousseau/rousseau-discours-sur-l-inegalite.html 及1755早期版在线转录 https://www.rousseauonline.ch/Text/discours-sur-l-origine-et-les-fondemens-de-l-inegalite-parmi-les-hommes.php 。原作者确有猎鹿与野兔故事，但**并没有原始数值4/3/0或现代游戏矩阵**。

Brian Skyrms, The Stag Hunt and the Evolution of Social Structure (Cambridge University Press, 2004, ISBN0521826519): **出版社开放的第1章pp1–13扫描全文** https://assets.cambridge.org/052182/6519/sample/0521826519ws.pdf 。真正用PDF screenshot核验原印刷p3 (zero-based PDF page5) 4/3/0数值、p5 (PDF page7) 无限重复PD的Trigger/Foole表5、1.5、4.5、2.5、p10–12 (PDF pages12–14) population stag share=3/4的吸引域和动态外推边界。其余章节**未完成全书核阅**。原著把猎鹿/野兔的合作看成协调与信任，不是囚徒困境的同一Nash结构。

Battalio, Samuelson, Van Huyck (2001), Optimization Incentives and Coordination Failure in Laboratory Stag Hunt Games, Econometrica69(3):749–764 DOI https://doi.org/10.1111/1468-0262.00212；本次仅核实发行方/作者摘要关于不同优化收益差的原作者主张，**不重算其真实人类实验数据、拟合系数或显著性**。不将其论文中的人类实验归入R128新E2。

## 已冻结来源数值与本期新数学问题

(A) Skyrms原一手pp3的二人对称单期行收益，自己Stag对Stag=4, Stag对Hare=0, Hare无论对手=3。两个严格纯Nash (S,S)、(H,H)，收益占优S/S但风险占优H/H；任意主观合作信念q下两行动期望为4q、3，q>3/4选鹿、<3/4选兔、=3/4打平。

(B) **项目自设，而非书中人类实验或作者的全部n人方程**：n=2..8人全部鹿行动才能成功，鹿成功者4、任何有兔则鹿参加者0、兔行动人3。若另外n−1人**相互独立且同合作边际p**，自己鹿的成功概率p^(n−1)，临界条件p^(n−1)>3/4。用一套独立完整轮廓枚举所有其它人的鹿/兔联合情况及其乘积概率，和解析闭式严格Fraction一致。p=4/5时n2鹿收益16/5>3而n3鹿收益64/25<3，人数不是不加额外假设必然降低真人合作率。

(C) **同边际但联合不同的严格数学反例**：n3别人两人边际各4/5，独立合成四状态(SS,SH,HS,HH)=(16/25,4/25,4/25,1/25)→P都合作16/25→自己应选兔；完全同向相关(4/5,0,0,1/5)→P都合作4/5→自己选鹿；互补最低同现(3/5,1/5,1/5,0)→P都合作3/5→自己选兔。三者个人边际完全一样；此反例禁止假装能从个体边际推断群体共同合作概率，更不是实际人类相关性实测。

(D) Skyrms原p5真正印刷的单期PD行收益((2,0),(3,1))（C/D），只保留两策略Trigger（初始合作、如任何背叛以后始终D）、Foole（始终D）。每轮继续概率δ，须Fraction 0≤δ<1。独立无限折现解析TT=2/(1−δ), TF=δ/(1−δ), FT=3+δ/(1−δ), FF=1/(1−δ)。δ=3/5的原作者完整行矩阵严格是((5,3/2),(9/2,5/2))。另一算法逐回合构造前T≤12轮行为及其精确折现现金流，证明相对于闭式无限之尾项公式，不准把有限12轮近似说成无限恰相等。δ>1/2时仅在这两策略限制下有两个严格对角Nash；δ=1/2的TT不严格，δ<1/2非Nash；δ>1/2时混合信念对Trigger的无差阈值q=(1−δ)/δ，原δ=3/5时2/3。δ=2/3两均衡风险恰打平，超过2/3 Trigger风险占优、低于则Foole风险占优。这是**本项目由原表推导**，不是原书p5印刷全套一般风险门值或现实被试行为。

(E) 原书p10–11提及连续时间replicator及p=3/4的吸引域。项目额外建立明确标注的**自造离散收益比例更新** x'=[x·(4x)]/[x·(4x)+(1−x)·3]，x∈[0,1]严格Fraction；x∈(0,3/4)下降，(3/4,1)上升，{0,3/4,1}固定。仅是模型内演示，不是原作者完整动态拟合、亦非真实社会历史预测。必须区分个人主观信念与随机匹配人口份额，没有随机混合不能无条件同一。

## 验收数值门与边界

n2..8，p∈{0,1/4,1/2,3/4,4/5,1}的全部可枚举相邻行动轮廓，计6×Σ_(k=1..7)2^k=6×254=**1524组纯数学轮廓权重**，42个(n,p)组合的完整独立解析和枚举一致。≥40项独立标准库unit tests；原书数值与无限/有限折现双算法对照、信念耦合边界、收益单调动力学。真实GitHub Actions成功、机器人生成程序测试科研报告三份SHA256且接收记录回读，才能有限结题：LEARNING_COMPLETE_BOUNDED_SKYRMS_2004_STAG_HUNT_GROUP_TRUST_CORRELATION_AND_REPEATED_PD。新增真人E2=0，Skyrms2004只是作者来源理论与被引述实证背景，Battalio2001的全文实验数据未复验，历史E3=0。不得更改R073/PESEN v0.1。
